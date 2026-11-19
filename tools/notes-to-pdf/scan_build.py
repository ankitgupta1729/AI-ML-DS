#!/usr/bin/env python3
"""Build a clean-scan edition of a handwritten notebook from phone photos.

    python tools/notes-to-pdf/scan_build.py PHOTOS_DIR
    python tools/notes-to-pdf/scan_build.py PHOTOS_DIR --manifest tools/notes-to-pdf/scans/<name>.json

PHOTOS_DIR holds one photo per notebook page; sorted by file name they must be
in notebook order (e.g. ``pdftoppm -jpeg notebook.pdf PHOTOS_DIR/pg`` or
``pdfimages -j``). The manifest gives the title, which photos were taken
sideways, the parts and sections of the topic index, and how to split the
result into volumes. Each photo is cleaned by ``notes_pdf.scan`` (levelled,
background blanked, paper whitened; nothing on the paper is cropped) and
placed on its own A4 page together with a cover, contents with page numbers,
a divider for every part, running headers and PDF bookmarks.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import html
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor

import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

from build import finish_pdf, page_map, render  # noqa: E402

from notes_pdf import scan  # noqa: E402
from notes_pdf.render import font_css  # noqa: E402

DEFAULT_MANIFEST = os.path.join(HERE, "scans", "ds-ml-handwritten-notes.json")
LONG_SIDE = 1700  # px; ~165 dpi on A4, sharp for handwriting at a sensible file size
JPEG_QUALITY = 62
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
PHOTO_EXT = (".jpg", ".jpeg", ".png")

CSS = """
.sheet { break-after: page; height: 259mm; display: flex; flex-direction: column; }
.sheet:last-child { break-after: auto; }
.sec-head { flex: none; display: flex; align-items: baseline; gap: 3mm; margin: 0 0 3.5mm;
  padding: 0 0 2.5mm; border-bottom: 1px solid var(--hair); }
.sec-head .no { font: 700 7.6pt var(--sans); letter-spacing: .14em; text-transform: uppercase;
  color: var(--accent); white-space: nowrap; }
.sec-head h2 { margin: 0; font: 700 14pt/1.2 var(--display); color: var(--ink); letter-spacing: -.01em; }
.page-img { flex: 1 1 auto; min-height: 0; display: flex; align-items: center; justify-content: center; }
.page-img img { display: block; max-width: 100%; max-height: 100%; width: auto; height: auto;
  border: .3mm solid var(--hair); border-radius: 1.5mm; }
.page-cap { flex: none; margin-top: 2.5mm; display: flex; justify-content: space-between;
  font: 500 7.4pt var(--sans); color: var(--muted); letter-spacing: .02em; }
.page-cap b { color: var(--accent); font-weight: 700; letter-spacing: .1em; text-transform: uppercase; font-size: 7pt; }

.divider { page: divider; break-before: page; break-after: page; position: relative; overflow: hidden;
  width: 210mm; height: 296.5mm; padding: 34mm 24mm 24mm; color: #fff; font-family: var(--sans);
  background:
    radial-gradient(110mm 110mm at 90% 0%, color-mix(in srgb, var(--accent) 70%, white) 0%, transparent 60%),
    linear-gradient(165deg, #0b1020 0%, color-mix(in srgb, var(--accent) 50%, #0b1020) 100%); }
.divider .kicker { font: 700 9pt var(--sans); letter-spacing: .22em; text-transform: uppercase;
  color: color-mix(in srgb, var(--accent) 30%, white); }
.divider .num { font: 700 64pt/1 var(--display); margin: 6mm 0 4mm; opacity: .95; }
.divider h2 { font: 700 28pt/1.12 var(--display); color: #fff; margin: 0 0 12mm; letter-spacing: -.02em;
  max-width: 150mm; text-wrap: balance; }
.divider ol { list-style: none; margin: 0; padding: 0; border-top: 1px solid rgba(255,255,255,.25); }
.divider li { display: flex; gap: 4mm; align-items: baseline; padding: 2.6mm 0;
  border-bottom: 1px solid rgba(255,255,255,.14); font: 500 10pt/1.35 var(--sans); }
.divider li .t { flex: 1 1 auto; }
.divider li .p { flex: none; font: 600 8pt var(--sans); opacity: .7; font-variant-numeric: tabular-nums; }
@page divider { margin: 0; @top-left { content: none; } @top-right { content: none; }
  @bottom-left { content: none; } @bottom-right { content: none; } }

.toc .toc-l0 { margin-top: 1.8mm; padding: 1.1mm 0; }
.toc .toc-l1 { padding: .35mm 0 .35mm 6mm; }
.toc-note { margin-top: 5mm; padding: 3.5mm 4.5mm; border-left: 3px solid var(--accent); background: var(--soft);
  font: 400 8.6pt/1.55 var(--sans); color: var(--text); border-radius: 0 2mm 2mm 0; }
.toc-note p { margin: 0 0 1.5mm; text-align: left; }
.toc-note p:last-child { margin: 0; }
"""


def css_str(t: str) -> str:
    return t.replace("\\", "\\\\").replace('"', '\\"')


def load_manifest(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        m = json.load(f)
    sections = []  # (start page, part index, section index, title)
    for pi, part in enumerate(m["parts"]):
        for si, (start, title) in enumerate(part["sections"]):
            sections.append((int(start), pi, si, title))
    starts = [s[0] for s in sections]
    if starts != sorted(starts) or len(set(starts)) != len(starts) or starts[0] != 1:
        sys.exit("manifest: section start pages must be unique, ascending and begin at page 1")
    m["_sections"] = sections
    return m


def turns_for(m: dict, page: int) -> int:
    for r in m.get("quarter_turns", []):
        if r["pages"][0] <= page <= r["pages"][1]:
            return r["turns"]
    return 0


def _clean_one(job: tuple[str, str, int]) -> str:
    src, dst, turns = job
    img = cv2.imread(src)
    if img is None:
        raise ValueError(f"cannot read {src}")
    out, _ = scan.process(img, turns)
    h, w = out.shape[:2]
    f = LONG_SIDE / max(h, w)
    if f < 1:
        out = cv2.resize(out, (round(w * f), round(h * f)), interpolation=cv2.INTER_AREA)
    tmp = dst + ".tmp.jpg"
    cv2.imwrite(tmp, out, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY, cv2.IMWRITE_JPEG_OPTIMIZE, 1])
    os.replace(tmp, dst)
    return dst


def clean_pages(m: dict, photos: list[str], cache: str) -> list[str]:
    """Clean every photo once; results are cached by photo content + settings."""
    os.makedirs(cache, exist_ok=True)
    jobs, out = [], []
    for i, src in enumerate(photos, 1):
        turns = turns_for(m, i)
        h = hashlib.sha1()
        with open(src, "rb") as f:
            h.update(f.read())
        h.update(f"{turns}|{LONG_SIDE}|{JPEG_QUALITY}|{scan.VERSION}".encode())
        dst = os.path.join(cache, f"p{i:03d}-{h.hexdigest()[:12]}.jpg")
        out.append(dst)
        if not os.path.exists(dst):
            jobs.append((src, dst, turns))
    if jobs:
        print(f"  cleaning {len(jobs)} photo(s)")
        with ProcessPoolExecutor() as pool:
            for _ in pool.map(_clean_one, jobs, chunksize=4):
                pass
    return out


class Edition:
    def __init__(self, m: dict, pages: list[str], first: int, last: int, vol: int, vols: int):
        self.m, self.pages, self.first, self.last, self.vol, self.vols = m, pages, first, last, vol, vols
        secs = m["_sections"]
        self.secs = []  # (start, end, part, sec_index, title) within this volume
        for k, (start, pi, si, title) in enumerate(secs):
            end = (secs[k + 1][0] - 1) if k + 1 < len(secs) else len(pages)
            if start >= first and start <= last:
                self.secs.append((start, min(end, last), pi, si, title))
        self.parts = sorted({s[2] for s in self.secs})
        self.toc: list[tuple[int, str, str, str]] = []

    def part_label(self, pi: int) -> str:
        return f"Part {ROMAN[pi]}"

    def cover(self, total: int | None) -> str:
        m = self.m
        vol = ""
        if self.vols > 1:
            a, b = ROMAN[self.parts[0]], ROMAN[self.parts[-1]]
            rng = f"Parts {a}–{b}" if a != b else f"Part {a}"
            vol = (f'<div class="vol">Volume {self.vol} of {self.vols} · {rng} · '
                   f'notebook pages {self.first}–{self.last}</div>')
        stats = [f"<div><b>{self.last - self.first + 1}</b><span>notebook pages</span></div>",
                 f"<div><b>{len(self.secs)}</b><span>topics</span></div>"]
        if total:
            stats.append(f"<div><b>{total}</b><span>PDF pages</span></div>")
        date = _dt.date.today().strftime("%B %Y")
        return f"""
<section class="cover">
  <div class="cover-art"></div>
  <div class="cover-top"><span class="badge">{html.escape(m.get('category', 'Notes'))}</span>
    <span class="brand">AI · ML · DS &nbsp;/&nbsp; Revision Notes</span></div>
  <div class="cover-main">
    <div class="provider">{html.escape(m.get('provider', ''))} · clean-scan edition</div>
    <div class="cover-title" role="heading" aria-level="1">{html.escape(m['title'])}</div>
    <p class="subtitle">{html.escape(m.get('subtitle', ''))}</p>
    {vol}
  </div>
  <div class="cover-foot">
    <div class="stats">{''.join(stats)}</div>
    <div class="meta">Compiled {date}<br>{html.escape(m.get('repository', ''))}</div>
  </div>
</section>"""

    def contents(self, page_of: dict[str, int] | None) -> str:
        rows = []
        for pi in self.parts:
            pid = f"part-{pi + 1}"
            pg = str(page_of.get(pid, "")) if page_of else "000"
            rows.append(f'<li class="toc-l0"><a href="#{pid}"><span class="toc-label">{self.part_label(pi)}</span>'
                        f'<span class="toc-title">{html.escape(self.m["parts"][pi]["title"])}</span>'
                        f'<span class="toc-dots"></span><span class="toc-page">{pg}</span></a></li>')
            for start, _end, p2, _si, title in self.secs:
                if p2 != pi:
                    continue
                sid = f"sec-{start}"
                pg = str(page_of.get(sid, "")) if page_of else "000"
                rows.append(f'<li class="toc-l1"><a href="#{sid}"><span class="toc-title">{html.escape(title)}</span>'
                            f'<span class="toc-dots"></span><span class="toc-page">{pg}</span></a></li>')
        other = ""
        if self.vols > 1:
            rest = [f"{self.part_label(pi)} {html.escape(p['title'])}" for pi, p in enumerate(self.m["parts"])
                    if pi not in self.parts]
            if rest:
                other = f"<p><b>In the other volume:</b> {'; '.join(rest)}.</p>"
        note = (f'<div class="toc-note"><p>Every page is a photo of the notebook, cleaned up '
                f'(levelled, background removed, paper whitened) with nothing cropped from the paper. '
                f'Where a photo also caught part of the neighbouring page, it was kept as it is. '
                f'Each page is labelled with its notebook page number.</p>{other}</div>')
        return (f'<section class="toc"><h2 class="toc-head">Contents</h2><ol>{"".join(rows)}</ol>'
                f'{note}</section>')

    def body(self) -> str:
        out = []
        sec_by_start = {s[0]: s for s in self.secs}
        part_started = set()
        current = None
        for n in range(self.first, self.last + 1):
            if n in sec_by_start:
                current = sec_by_start[n]
                start, end, pi, si, title = current
                if pi not in part_started:
                    part_started.add(pi)
                    out.append(self.divider(pi))
            start, end, pi, si, title = current
            head = ""
            sid = f"sec-{start}"
            if n == start:
                self.toc.append((2, sid, "", title))
                head = (f'<div class="sec-head" id="{sid}"><span class="no">{ROMAN[pi]}.{si + 1}</span>'
                        f'<h2>{html.escape(title)}</h2></div>')
            span = f"pages {start}–{end}" if end > start else f"page {start}"
            img = html.escape("file://" + self.pages[n - 1])
            out.append(
                f'<section class="sheet" style="page: s{start}">{head}'
                f'<div class="page-img"><img src="{img}" alt="Notebook page {n}: {html.escape(title)}"></div>'
                f'<div class="page-cap"><span><b>Notebook page {n}</b></span>'
                f'<span>Topic {ROMAN[pi]}.{si + 1} · notebook {span}</span></div></section>')
        return "\n".join(out)

    def divider(self, pi: int) -> str:
        pid = f"part-{pi + 1}"
        part = self.m["parts"][pi]
        self.toc.append((1, pid, self.part_label(pi), part["title"]))
        items = []
        for start, end, p2, _si, title in self.secs:
            if p2 == pi:
                rng = f"p. {start}–{end}" if end > start else f"p. {start}"
                items.append(f'<li><span class="t">{html.escape(title)}</span><span class="p">{rng}</span></li>')
        return (f'<section class="divider" id="{pid}"><div class="kicker">{html.escape(self.m["short"])}</div>'
                f'<div class="num">{ROMAN[pi]}</div><h2>{html.escape(part["title"])}</h2>'
                f'<ol>{"".join(items)}</ol></section>')

    def document(self, body: str, page_of=None, total=None) -> str:
        base = open(os.path.join(HERE, "notes_pdf", "style.css"), encoding="utf-8").read()
        vol = f" · Vol. {self.vol}" if self.vols > 1 else ""
        named = []
        for start, _end, pi, _si, title in self.secs:
            named.append(f'@page s{start} {{ @top-left {{ content: "{self.part_label(pi)} · '
                         f'{css_str(self.m["parts"][pi]["title"])}"; }} '
                         f'@bottom-left {{ content: "{css_str(title)}"; }} }}')
        return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{html.escape(self.m['title'])}</title>
<style>{font_css()}
:root{{--accent:{self.m.get('accent', '#4f46e5')};}}
{base}
{CSS}
@page {{ @top-right {{ content: "{css_str(self.m['short'])}{vol}"; }}
         @top-left {{ content: "{css_str(self.m.get('provider', ''))}"; }}
         @bottom-left {{ content: "Clean-scan edition"; }} }}
{chr(10).join(named)}</style></head><body>
{self.cover(total)}
{self.contents(page_of)}
<main>{body}</main>
</body></html>"""


def build(m: dict, photos_dir: str, work: str) -> list[str]:
    photos = sorted(os.path.join(photos_dir, f) for f in os.listdir(photos_dir) if f.lower().endswith(PHOTO_EXT))
    want = m["volumes"][-1][1]
    if len(photos) != want:
        sys.exit(f"expected {want} photos in {photos_dir}, found {len(photos)}")
    pages = clean_pages(m, photos, os.path.join(work, "pages"))
    out_dir = os.path.join(ROOT, m["out_dir"])
    os.makedirs(out_dir, exist_ok=True)
    outputs = []
    vols = m["volumes"]
    for vi, (first, last) in enumerate(vols, 1):
        ed = Edition(m, pages, first, last, vi, len(vols))
        body = ed.body()
        stem = m["file"] if len(vols) == 1 else f"{m['file']}-Vol{vi}"
        final = os.path.join(out_dir, stem + ".pdf")
        h1, p1 = os.path.join(work, f"{stem}-a.html"), os.path.join(work, f"{stem}-a.pdf")
        with open(h1, "w", encoding="utf-8") as f:
            f.write(ed.document(body))
        render([(h1, p1)])
        page_of, total = page_map(p1)
        h2 = os.path.join(work, f"{stem}-b.html")
        with open(h2, "w", encoding="utf-8") as f:
            f.write(ed.document(body, page_of, total))
        render([(h2, final)])
        os.remove(p1)
        meta = {k: m.get(k, "") for k in ("title", "author", "subtitle", "category", "provider")}
        if len(vols) > 1:
            meta.update(volume=vi, volumes=len(vols))
        finish_pdf(final, ed.toc, meta)
        print(f"  -> {os.path.relpath(final, ROOT)}  ({total} pages, {os.path.getsize(final) / 1e6:.1f} MB)")
        outputs.append(final)
    return outputs


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("photos", help="folder with one photo per notebook page, in notebook order by file name")
    ap.add_argument("--manifest", default=DEFAULT_MANIFEST)
    ap.add_argument("--work", default=os.path.join(HERE, ".cache", "scan"))
    args = ap.parse_args()
    m = load_manifest(args.manifest)
    os.makedirs(args.work, exist_ok=True)
    print(f"* {m['title']}")
    build(m, args.photos, args.work)


if __name__ == "__main__":
    main()
