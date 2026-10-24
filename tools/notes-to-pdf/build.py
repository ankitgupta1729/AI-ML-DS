#!/usr/bin/env python3
"""Build revision PDFs from the course notes listed in catalog.json.

    python tools/notes-to-pdf/build.py                 # every note in the catalog
    python tools/notes-to-pdf/build.py 47 55           # only modules 47 and 55
    python tools/notes-to-pdf/build.py --list          # show what would be built

The Markdown sources are only read, never written. See README.md for details.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse

from pypdf import PdfReader, PdfWriter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

from notes_pdf import images, ocr  # noqa: E402
from notes_pdf.align import is_transcript_doc, realign  # noqa: E402
from notes_pdf.parse import Block, parse  # noqa: E402
from notes_pdf.render import Renderer  # noqa: E402
from notes_pdf.titles import annotate, tidy_headings  # noqa: E402

# image bytes per volume; PDFs come out ~15% larger, i.e. comfortably under GitHub's 50 MB warning
MAX_VOLUME_BYTES = 38 * 1000 * 1000
MODULE_DIR = re.compile(r"^\d{2}\.")
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "AI-ML-DS", "__pycache__", "50.Andrew-Ng-Course-Material"}


def find_modules() -> dict[str, str]:
    """Map module folder name (e.g. '47.Coursera-...') to its path, wherever it lives."""
    found = {}
    for dirpath, dirnames, _ in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        keep = []
        for d in dirnames:
            if MODULE_DIR.match(d):
                found[d] = os.path.join(dirpath, d)
            else:
                keep.append(d)
        dirnames[:] = keep if os.path.relpath(dirpath, ROOT).count(os.sep) < 2 else []
    return found


def load_catalog() -> list[dict]:
    with open(os.path.join(HERE, "catalog.json"), encoding="utf-8") as f:
        cat = json.load(f)
    mods = find_modules()
    jobs = []
    for entry in cat["notes"]:
        module = entry.get("module", "")
        if "path" in entry:  # a repository doc rather than course notes
            src = os.path.join(ROOT, entry["path"])
            meta = dict(cat["categories"][entry["category"]])
            meta.update({k: v for k, v in entry.items() if k not in ("path", "out_dir")})
            meta.update(category=cat["categories"][entry["category"]]["label"], category_key=entry["category"],
                        repository=cat.get("repository", ""), author=cat.get("author", ""), module=module,
                        src=src, sources=[{"path": src}], module_dir=os.path.dirname(src),
                        out_dir=os.path.join(ROOT, entry["out_dir"]), doc=True)
            jobs.append(meta)
            continue
        if module not in mods:
            print(f"! module not found: {module}", file=sys.stderr)
            continue
        sources = entry.get("sources") or [{"path": entry["source"]}]
        for s in sources:
            s["path"] = os.path.join(mods[module], s["path"])
        missing = [s["path"] for s in sources if not os.path.exists(s["path"])]
        if missing:
            print(f"! note not found: {missing}", file=sys.stderr)
            continue
        src = sources[0]["path"]
        meta = dict(cat["categories"][entry["category"]])
        meta.update({k: v for k, v in entry.items() if k not in ("module", "source", "sources")})
        meta["sources"] = sources
        meta["category"] = cat["categories"][entry["category"]]["label"]
        meta["category_key"] = entry["category"]
        meta["repository"] = cat.get("repository", "")
        meta["author"] = cat.get("author", "")
        meta["src"] = src
        meta["module"] = module
        meta["module_dir"] = mods[module]
        meta["out_dir"] = os.path.join(mods[module] if len(sources) > 1 else os.path.dirname(src), "pdf")
        jobs.append(meta)
    return jobs


def split_volumes(blocks: list[Block], size_of) -> list[list[Block]]:
    """Cut at top-level sections so each volume's images stay under the size budget."""
    levels = Renderer({"title": ""}, ROOT, lambda p: None).plan_levels(blocks)
    top = next((k for k, lv in levels.items() if lv == 1), None)
    sections, cur = [], []
    for b in blocks:
        if b.kind == "heading" and b.hkind == top and cur:
            sections.append(cur)
            cur = []
        cur.append(b)
    if cur:
        sections.append(cur)
    vols, vol, size = [], [], 0
    for sec in sections:
        s = sum(size_of(b) for b in sec)
        if vol and size + s > MAX_VOLUME_BYTES:
            vols.append(vol)
            vol, size = [], 0
        vol.extend(sec)
        size += s
    if vol:
        vols.append(vol)
    return vols


def section_range(blocks: list[Block]) -> str:
    nums = [b.num for b in blocks if b.kind == "heading" and b.hkind in ("marker", "numtitle") and b.num]
    if nums:
        return f"Sections {nums[0]}–{nums[-1]}" if nums[0] != nums[-1] else f"Section {nums[0]}"
    heads = [b for b in blocks if b.kind == "heading"]
    return f"{len(heads)} sections" if heads else ""


def render(jobs: list[tuple[str, str]]) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump([{"html": h, "pdf": p} for h, p in jobs], f)
    try:
        subprocess.run(["node", os.path.join(HERE, "render_pdf.js"), f.name], check=True, cwd=HERE)
    finally:
        os.unlink(f.name)


def page_map(pdf: str) -> tuple[dict[str, int], int]:
    r = PdfReader(pdf)
    out = {}
    for name, dest in (r.named_destinations or {}).items():
        try:
            out[name.lstrip("/")] = r.get_destination_page_number(dest) + 1
        except Exception:
            pass
    return out, len(r.pages)


def finish_pdf(path: str, toc: list[tuple[int, str, str, str]], meta: dict) -> None:
    """Add bookmarks (from our own heading list) and document metadata."""
    reader = PdfReader(path)
    pages = {}
    for name, dest in (reader.named_destinations or {}).items():
        try:
            pages[name.lstrip("/")] = reader.get_destination_page_number(dest)
        except Exception:
            pass
    writer = PdfWriter(clone_from=reader)
    if len(reader.pages) > 1:
        writer.add_outline_item("Contents", 1)
    parents: dict[int, object] = {}
    for level, hid, label, title in toc:
        if hid not in pages or level > 3:
            continue
        text = f"{label} · {title}" if label and title else (title or label)
        parent = next((parents[lv] for lv in range(level - 1, 0, -1) if lv in parents), None)
        parents[level] = writer.add_outline_item(text, pages[hid], parent=parent)
        for deeper in [lv for lv in parents if lv > level]:
            del parents[deeper]
    title = meta["title"] + (f" — Volume {meta['volume']} of {meta['volumes']}" if meta.get("volume") else "")
    writer.add_metadata({
        "/Title": title,
        "/Author": meta.get("author", ""),
        "/Subject": meta.get("subtitle", ""),
        "/Keywords": ", ".join(k for k in (meta.get("category"), meta.get("provider"), "revision notes") if k),
        "/Creator": "AI-ML-DS tools/notes-to-pdf",
    })
    writer.page_mode = "/UseOutlines"
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        writer.write(f)
    os.replace(tmp, path)


def build(meta: dict, work: str, img_cache: str) -> list[str]:
    src = meta["src"]
    blocks = []
    for s in meta["sources"]:
        if s.get("title"):
            blocks.append(Block("heading", text=s["title"], hkind="part"))
        blocks.extend(parse(s["path"]))
    blocks = tidy_headings(blocks)
    transcript = is_transcript_doc(blocks)
    meta["transcript"] = transcript
    if transcript:
        ocr.warm([b.src for b in blocks if b.kind == "img" and b.src])
        blocks, stats = realign(blocks, lambda p: ocr.cached(p, compute=False))
        print(f"  realigned {stats['images']} screenshots in {stats['units']} units")

    # names for bare "N." sections: slide titles (transcripts) or the opening sentence
    annotate(blocks, (lambda p: ocr.cached(p, compute=False)) if transcript else (lambda p: {}))
    prepared: dict[str, dict] = {}
    srcs = sorted({b.src for b in blocks if b.kind == "img" and b.src})
    for p, res in images.prepare_many(srcs, img_cache).items():
        if isinstance(res, Exception):
            print(f"  ! image skipped {p}: {res}", file=sys.stderr)
            res = None
        prepared[p] = res

    def info(p):
        if p not in prepared:
            try:
                prepared[p] = images.prepare(p, img_cache)
            except Exception as e:
                print(f"  ! image skipped {p}: {e}", file=sys.stderr)
                prepared[p] = None
        return prepared[p]

    def size_of(b):
        i = info(b.src) if b.kind == "img" and b.src else None
        return i["bytes"] if i else len(b.text)

    vols = split_volumes(blocks, size_of)
    os.makedirs(meta["out_dir"], exist_ok=True)
    stem = meta["file"]
    outputs = []
    for vi, vblocks in enumerate(vols, 1):
        vmeta = dict(meta)
        if len(vols) > 1:
            vmeta.update(volume=vi, volumes=len(vols), range=section_range(vblocks))
        name = f"{stem}.pdf" if len(vols) == 1 else f"{stem}-Vol{vi}.pdf"
        final = os.path.join(meta["out_dir"], name)
        r = Renderer(vmeta, os.path.dirname(src), info)
        body = r.body(vblocks, transcript)
        h1, p1 = os.path.join(work, f"{stem}-{vi}-a.html"), os.path.join(work, f"{stem}-{vi}-a.pdf")
        with open(h1, "w", encoding="utf-8") as f:
            f.write(r.document(body))
        render([(h1, p1)])
        pages_of, total = page_map(p1)
        h2 = os.path.join(work, f"{stem}-{vi}-b.html")
        with open(h2, "w", encoding="utf-8") as f:
            f.write(r.document(body, pages_of, total))
        render([(h2, final)])
        finish_pdf(final, r.toc, vmeta)
        os.remove(p1)
        mb = os.path.getsize(final) / 1e6
        print(f"  -> {os.path.relpath(final, ROOT)}  ({total} pages, {mb:.1f} MB)")
        outputs.append(final)
    # drop volumes left over from an earlier, differently split build
    for old in os.listdir(meta["out_dir"]):
        p = os.path.join(meta["out_dir"], old)
        if re.match(re.escape(stem) + r"(-Vol\d+)?\.pdf$", old) and p not in outputs:
            os.remove(p)
    return outputs


def pdfs_of(meta: dict) -> list[str]:
    if not os.path.isdir(meta["out_dir"]):
        return []
    rx = re.compile(re.escape(meta["file"]) + r"(-Vol(\d+))?\.pdf$")
    hits = [f for f in os.listdir(meta["out_dir"]) if rx.match(f)]
    return [os.path.join(meta["out_dir"], f)
            for f in sorted(hits, key=lambda f: int(rx.match(f).group(2) or 0))]


def update_readme(jobs: list[dict]) -> None:
    """Regenerate the PDF index between the markers in the top-level README."""
    readme = os.path.join(ROOT, "README.md")
    with open(readme, encoding="utf-8") as f:
        text = f.read()
    start, end = "<!-- pdf-index:start -->", "<!-- pdf-index:end -->"
    if start not in text or end not in text:
        sys.exit("README.md has no pdf-index markers")
    with open(os.path.join(HERE, "catalog.json"), encoding="utf-8") as f:
        order = list(json.load(f)["categories"])
    lines = []
    for cat in order:
        rows = [j for j in jobs if j["category_key"] == cat and pdfs_of(j) and not j.get("doc")]
        if not rows:
            continue
        lines += ["", f"#### {rows[0]['category']}", "",
                  "| Course | Source | PDF | Pages |", "| --- | --- | --- | ---: |"]
        for j in rows:
            files = pdfs_of(j)
            pages = sum(len(PdfReader(p).pages) for p in files)
            links = " · ".join(
                f"[{'PDF' if len(files) == 1 else f'Vol. {i}'}]"
                f"({urllib.parse.quote(os.path.relpath(p, ROOT))})" for i, p in enumerate(files, 1))
            lines.append(f"| {j['title']} | {j['provider']} | {links} | {pages} |")
    block = "\n".join(lines).strip("\n")
    text = text[:text.index(start) + len(start)] + "\n" + block + "\n" + text[text.index(end):]
    with open(readme, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"README.md index updated ({sum(1 for j in jobs if pdfs_of(j) and not j.get('doc'))} courses)")


def verify(jobs: list[dict]) -> int:
    """Check every generated PDF; returns the number of problems found."""
    problems = 0
    for j in jobs:
        files = pdfs_of(j)
        if not files:
            print(f"✗ {j['file']}: no PDF built")
            problems += 1
            continue
        for path in files:
            name = os.path.relpath(path, ROOT)
            issues = []
            size = os.path.getsize(path)
            if size >= 50 * 1000 * 1000:
                issues.append(f"{size / 1e6:.1f} MB (GitHub warns at 50 MB)")
            r = PdfReader(path)
            if len(r.pages) < 2:
                issues.append("fewer than 2 pages")
            if not r.outline:
                issues.append("no bookmarks")
            if not (r.metadata or {}).get("/Title"):
                issues.append("no title metadata")
            if len(r.pages) > 1 and re.search(r"\b000\b", r.pages[1].extract_text() or ""):
                issues.append("contents page numbers not filled in")
            fonts = set()
            for page in r.pages[:3]:
                for f in ((page.get("/Resources") or {}).get("/Font") or {}).values():
                    fonts.add(f.get_object().get("/Subtype"))
            if "/Type3" in fonts:
                issues.append("Type 3 fonts embedded")
            print(("✗ " if issues else "✓ ") + name + (": " + "; ".join(issues) if issues else ""))
            problems += bool(issues)
    print(f"{problems} problem(s)")
    return problems


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("only", nargs="*", help="module numbers or folder names to build")
    ap.add_argument("--list", action="store_true", help="list catalog entries and exit")
    ap.add_argument("--readme", action="store_true", help="only refresh the PDF index in README.md")
    ap.add_argument("--verify", action="store_true", help="check the generated PDFs and exit")
    ap.add_argument("--work", default=os.path.join(HERE, ".cache", "work"))
    ap.add_argument("--images", default=os.path.join(HERE, ".cache", "images"))
    args = ap.parse_args()
    jobs = load_catalog()
    if args.only:
        jobs = [j for j in jobs if any(j["module"] == o or j["module"].split(".")[0] == o.zfill(2)
                                       or j["file"] == o for o in args.only)]
    if args.readme:
        update_readme(load_catalog())
        return
    if args.verify:
        sys.exit(1 if verify(load_catalog()) else 0)
    if args.list:
        for j in jobs:
            print(f"{os.path.relpath(j['src'], ROOT)}  ->  {j['file']}.pdf")
        return
    if not shutil.which("node"):
        sys.exit("node is required (see README.md)")
    os.makedirs(args.work, exist_ok=True)
    for j in jobs:
        print(f"* {os.path.relpath(j['src'], ROOT)}")
        build(j, args.work, args.images)
    if not args.only:
        update_readme(load_catalog())


if __name__ == "__main__":
    main()
