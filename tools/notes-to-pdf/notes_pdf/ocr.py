"""OCR a screenshot twice: whole frame, and the subtitle band in isolation.

Results are cached as JSON keyed by the image's SHA-1, so moving or renaming
files never forces a re-run.
"""
from __future__ import annotations

import gzip
import json
import os
import subprocess
import sys
import tempfile
from multiprocessing import Pool

from PIL import Image, ImageChops, ImageFilter

from .images import file_hash

CACHE = os.environ.get("NOTES_PDF_OCR_CACHE", os.path.join(os.path.dirname(__file__), "..", ".cache", "ocr"))
# OCR of every screenshot in the repo, shipped so a fresh clone needs no Tesseract run
BUNDLE = os.path.join(os.path.dirname(__file__), "..", "ocr-cache.json.gz")
_bundle: dict | None = None


def _bundled(key: str) -> dict | None:
    global _bundle
    if _bundle is None:
        try:
            with gzip.open(BUNDLE, "rt", encoding="utf-8") as f:
                _bundle = json.load(f)
        except OSError:
            _bundle = {}
    return _bundle.get(key)


def export_bundle(cache: str = CACHE, out: str = BUNDLE) -> int:
    """Pack the per-image cache into the shipped bundle (sorted, so diffs stay small)."""
    data = {}
    for name in sorted(os.listdir(cache)):
        if name.endswith(".json"):
            with open(os.path.join(cache, name)) as f:
                data[name[:-5]] = json.load(f)
    with gzip.GzipFile(out, "wb", mtime=0) as g:
        g.write(json.dumps(data, sort_keys=True, separators=(",", ":")).encode())
    return len(data)


def _tess(img: Image.Image, psm: int) -> str:
    with tempfile.NamedTemporaryFile(suffix=".png") as t:
        img.save(t.name)
        r = subprocess.run(["tesseract", t.name, "-", "--psm", str(psm)], capture_output=True,
                           text=True, timeout=60, env=dict(os.environ, OMP_THREAD_LIMIT="1"))
        return r.stdout


def subtitle_full_res(im: Image.Image) -> str:
    """Second subtitle pass at full resolution: white *and* unsaturated pixels only,
    opened to drop speckle. Reads subtitles over busy slides the first pass garbles."""
    w, h = im.size
    band = im.crop((0, int(h * 0.70), w, int(h * 0.97)))
    _, sat, val = band.convert("HSV").split()
    mask = ImageChops.multiply(val.point(lambda v: 255 if v > 200 else 0),
                               sat.point(lambda v: 255 if v < 40 else 0))
    mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
    mask = mask.resize((max(1, w // 2), max(1, mask.height // 2)))
    return _tess(ImageChops.invert(mask), 6)


def ocr_image(path: str) -> dict:
    im = Image.open(path).convert("RGB")
    sub2 = subtitle_full_res(im)
    w, h = im.size
    if w > 1600:
        im = im.resize((1600, int(h * 1600 / w)))
        w, h = im.size
    full = _tess(im.convert("L"), 3)
    band = im.crop((0, int(h * 0.70), w, int(h * 0.97)))
    # burned-in subtitles are near-white glyphs: keep only those, black on white
    r, g, b = [c.point(lambda v: 255 if v > 225 else 0) for c in band.split()]
    sub = _tess(ImageChops.invert(ImageChops.multiply(ImageChops.multiply(r, g), b)), 6)
    return {"full": full, "sub": sub, "sub2": sub2}


def cached(path: str, cache: str = CACHE, compute: bool = True) -> dict:
    os.makedirs(cache, exist_ok=True)
    key = file_hash(path)
    out = os.path.join(cache, key + ".json")
    res = None
    if os.path.exists(out):
        with open(out) as f:
            res = json.load(f)
    else:
        res = _bundled(key)
    if res is not None and ("sub2" in res or not compute):
        return res
    if res is not None:  # cache from before the second subtitle pass: top it up
        res["sub2"] = subtitle_full_res(Image.open(path).convert("RGB"))
        with open(out, "w") as f:
            json.dump(res, f)
        return res
    if not compute:
        return {}
    res = ocr_image(path)
    with open(out, "w") as f:
        json.dump(res, f)
    return res


def _work(args):
    path, cache = args
    try:
        cached(path, cache)
    except Exception as e:  # keep going; a missing OCR only means "no anchor"
        print("OCR failed:", path, e, file=sys.stderr)


def warm(paths: list[str], cache: str = CACHE, workers: int = os.cpu_count() or 2) -> None:
    with Pool(workers) as pool:
        for i, _ in enumerate(pool.imap_unordered(_work, [(p, cache) for p in paths], chunksize=4)):
            if i % 250 == 0:
                print(f"  ocr {i}/{len(paths)}", flush=True)
