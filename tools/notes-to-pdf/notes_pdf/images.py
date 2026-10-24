"""Prepare screenshots for print: the full frame, as captured, downscaled to print size as JPEG."""
from __future__ import annotations

import hashlib
import json
import os

from PIL import Image, ImageOps

MAX_W = 1400
QUALITY = 72


def file_hash(path: str) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def prepare(src: str, cache_dir: str) -> dict:
    """Return {'path', 'w', 'h', 'bytes'} for a print-ready copy of ``src``.

    The picture itself is left exactly as captured (no cropping or retouching);
    only its resolution and encoding change, to keep the PDFs a sensible size.
    """
    os.makedirs(cache_dir, exist_ok=True)
    key = file_hash(src)
    out = os.path.join(cache_dir, f"{key}-full-{MAX_W}-{QUALITY}.jpg")
    meta = out + ".json"
    if os.path.exists(out) and os.path.exists(meta):
        with open(meta) as f:
            return json.load(f)
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    im.save(out, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    info = {"path": out, "w": im.width, "h": im.height, "bytes": os.path.getsize(out)}
    with open(meta, "w") as f:
        json.dump(info, f)
    return info


def _prepare_one(args):
    src, cache_dir = args
    try:
        return src, prepare(src, cache_dir)
    except Exception as e:  # a broken image is skipped, not fatal
        return src, e


def prepare_many(srcs: list[str], cache_dir: str, workers: int = os.cpu_count() or 2) -> dict:
    """Prepare images in parallel; returns {src: info or Exception}."""
    from multiprocessing import Pool
    with Pool(workers) as pool:
        return dict(pool.imap_unordered(_prepare_one, [(s, cache_dir) for s in srcs], chunksize=4))
