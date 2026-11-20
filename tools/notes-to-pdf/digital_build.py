#!/usr/bin/env python3
"""Typeset a set of Markdown notes (with maths and diagrams) as a revision PDF.

    python tools/notes-to-pdf/digital_build.py [--manifest tools/notes-to-pdf/scans/<name>.json]

Used for the digital edition of the handwritten notebook: the manifest's
``digital`` block lists the Markdown files (one per part) and the output. The
Markdown may contain

* ``# Part title`` once per file (a part divider page) and ``##``/``###``/``####``
  topics and sub-topics (contents, bookmarks and running headers come from these);
* ``<!-- pages: 12-14 -->`` right under a heading: the notebook pages it was
  transcribed from (printed as a small source tag);
* TeX maths, ``$inline$`` and ``$$display$$`` (rendered with KaTeX at build time);
* fenced ``mermaid`` blocks (diagrams, drawn by Mermaid in Chromium);
* tables, lists, code, block quotes and images, as usual.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import html
import json
import os
import re
import subprocess
import sys

from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

from build import finish_pdf, page_map, render  # noqa: E402

from notes_pdf.render import font_css  # noqa: E402

DEFAULT_MANIFEST = os.path.join(HERE, "scans", "ds-ml-handwritten-notes.json")
NODE = os.path.join(HERE, "node_modules")
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
PAGES_RX = re.compile(r"^<!--\s*pages:\s*([0-9][0-9,\s–-]*)\s*-->\s*$", re.M)

CSS = """
h1.part-title { display: none; }
h2.topic { break-before: auto; margin: 11mm 0 4mm; padding: 0 0 3mm; border-bottom: 1px solid var(--hair);
  font: 700 17pt/1.2 var(--display); color: var(--ink); letter-spacing: -.015em; }
h2.topic.first { margin-top: 0; }
h2.topic .no { display: block; font: 700 7.6pt var(--sans); letter-spacing: .16em; text-transform: uppercase;
  color: var(--accent); margin-bottom: 1.6mm; }
h3 { font: 700 12.4pt/1.3 var(--display); color: var(--ink); margin: 7mm 0 2.5mm; padding-left: 3mm;
  border-left: 3px solid var(--accent); }
h4 { font: 600 10.8pt/1.35 var(--display); color: var(--ink); margin: 5mm 0 1.8mm; }
.src { display: inline-block; margin: -1.5mm 0 4mm; font: 600 7pt var(--sans); letter-spacing: .08em;
  text-transform: uppercase; color: var(--muted); background: #f1f5f9; padding: .8mm 2.2mm; border-radius: 1mm; }
.katex { font-size: 1.06em; }
.katex-display { margin: 2.5mm 0 3.5mm; overflow: hidden; }
p .katex, li .katex { white-space: nowrap; }
.diagram { margin: 3mm 0 5mm; padding: 4mm; border: 1px solid var(--hair); border-radius: 2mm; background: #fcfcff;
  break-inside: avoid; text-align: center; }
.diagram svg { max-width: 100% !important; height: auto; max-height: 120mm; }
table { font-size: 8.6pt; }
td .katex, th .katex { font-size: 1em; }
li > p { margin: 0 0 1.2mm; }
ul ul, ol ol, ul ol, ol ul { margin-bottom: 1mm; }
blockquote strong:first-child { color: var(--accent); }
.two-figs { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; align-items: end; break-inside: avoid; }
.two-figs .diagram { margin: 0; }
figure.sketch { margin: 3mm 0 5mm; text-align: center; break-inside: avoid; }
figure.sketch img { max-width: 92%; max-height: 95mm; border: .3mm solid var(--hair); border-radius: 1.5mm; }
figure.sketch figcaption { margin-top: 1.5mm; }

.divider { page: divider; break-before: page; break-after: page; position: relative; overflow: hidden;
  width: 210mm; height: 296.5mm; padding: 34mm 24mm 24mm; color: #fff; font-family: var(--sans);
  background:
    radial-gradient(110mm 110mm at 90% 0%, color-mix(in srgb, var(--accent) 70%, white) 0%, transparent 60%),
    linear-gradient(165deg, #0b1020 0%, color-mix(in srgb, var(--accent) 50%, #0b1020) 100%); }
.divider .kicker { font: 700 9pt var(--sans); letter-spacing: .22em; text-transform: uppercase;
  color: color-mix(in srgb, var(--accent) 30%, white); }
.divider .num { font: 700 64pt/1 var(--display); margin: 6mm 0 4mm; opacity: .95; }
.divider .ptitle { font: 700 28pt/1.12 var(--display); color: #fff; margin: 0 0 12mm; letter-spacing: -.02em;
  max-width: 150mm; text-wrap: balance; }
.divider ol { list-style: none; margin: 0; padding: 0; border-top: 1px solid rgba(255,255,255,.25); }
.divider li { display: flex; gap: 4mm; align-items: baseline; padding: 2.4mm 0; margin: 0;
  border-bottom: 1px solid rgba(255,255,255,.14); font: 500 10pt/1.35 var(--sans); }
.divider li .n { flex: none; width: 9mm; font: 700 8pt var(--sans); opacity: .65; }
.divider li .t { flex: 1 1 auto; }
@page divider { margin: 0; @top-left { content: none; } @top-right { content: none; }
  @bottom-left { content: none; } @bottom-right { content: none; } }
.part { break-before: page; }
.toc .toc-l0 { margin-top: 1.8mm; padding: 1.1mm 0; }
.toc .toc-l1 { padding: .3mm 0 .3mm 6mm; }
.toc-note { margin-top: 6mm; padding: 3.5mm 4.5mm; border-left: 3px solid var(--accent); background: var(--soft);
  font: 400 8.6pt/1.55 var(--sans); border-radius: 0 2mm 2mm 0; }
.toc-note p { margin: 0 0 1.5mm; text-align: left; }
.toc-note p:last-child { margin: 0; }
"""


def slug(text: str, used: set[str]) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "s"
    base, i = s, 2
    while s in used:
        s, i = f"{base}-{i}", i + 1
    used.add(s)
    return s


def katex(items: list[tuple[str, bool]]) -> list[str]:
    if not items:
        return []
    res = subprocess.run(["node", os.path.join(HERE, "katex_render.js")], input=json.dumps(items),
                         capture_output=True, text=True, check=True, cwd=HERE)
    if res.stderr:
        sys.stderr.write(res.stderr)
    return json.loads(res.stdout)


def css_str(t: str) -> str:
    return t.replace("\\", "\\\\").replace('"', '\\"')


class Doc:
    def __init__(self, m: dict):
        self.m = m
        self.d = m["digital"]
        self.used: set[str] = set()
        self.toc: list[tuple[int, str, str, str]] = []
        self.parts: list[dict] = []  # {id, title, topics: [(id, title)]}
        self.math: list[tuple[str, bool]] = []
        md = MarkdownIt("commonmark", {"html": True, "typographer": True}).enable(["table", "strikethrough"])
        md.use(dollarmath_plugin, allow_space=True, double_inline=True)
        md.add_render_rule("math_inline", self._math(False))
        md.add_render_rule("math_inline_double", self._math(True))
        md.add_render_rule("math_block", self._math(True))
        md.add_render_rule("math_block_label", self._math(True))
        md.add_render_rule("fence", self._fence)
        md.add_render_rule("heading_open", self._heading_open)
        md.add_render_rule("image", self._image)
        self.md = md
        self.base = ROOT
        self.n_topics = 0

    def _math(self, display: bool):
        def rule(renderer, tokens, idx, options, env):
            self.math.append((tokens[idx].content.strip(), display))
            return f"\x00MATH{len(self.math) - 1}\x00"
        return rule

    def _fence(self, tokens, idx, options, env):
        t = tokens[idx]
        if t.info.strip() == "mermaid":
            return f'<div class="diagram"><pre class="mermaid">{html.escape(t.content)}</pre></div>\n'
        return f"<pre><code>{html.escape(t.content)}</code></pre>\n"

    def _image(self, tokens, idx, options, env):
        t = tokens[idx]
        src = t.attrGet("src") or ""
        path = src if os.path.isabs(src) else os.path.normpath(os.path.join(env["dir"], src))
        cap = html.escape("".join(c.content for c in (t.children or [])) or t.content or "")
        return (f'<figure class="sketch"><img src="file://{html.escape(path)}" alt="{cap}">'
                f'<figcaption>{cap}</figcaption></figure>')

    def _heading_open(self, tokens, idx, options, env):
        t = tokens[idx]
        title = tokens[idx + 1].content
        plain = re.sub(r"\$[^$]*\$", "", title).replace("*", "").strip()
        hid = slug(plain, self.used)
        level = int(t.tag[1])
        if level == 1:
            pi = len(self.parts)
            self.parts.append({"id": hid, "title": plain, "topics": []})
            self.toc.append((1, hid, f"Part {ROMAN[pi]}", plain))
            env["topic"] = 0
            return f'<h1 id="{hid}" class="part-title">'
        if level == 2:
            env["topic"] = env.get("topic", 0) + 1
            pi = len(self.parts) - 1
            self.parts[-1]["topics"].append((hid, plain))
            self.toc.append((2, hid, "", plain))
            self.n_topics += 1
            cls = "topic first" if env["topic"] == 1 else "topic"
            env["pending_no"] = f'<span class="no">{ROMAN[pi]}.{env["topic"]}</span>'
            return f'<h2 id="{hid}" class="{cls}">' + env.pop("pending_no")
        if level == 3:
            self.toc.append((3, hid, "", plain))
        return f'<{t.tag} id="{hid}">'

    def body(self) -> str:
        out = []
        for path in self.d["sources"]:
            full = os.path.join(ROOT, path)
            with open(full, encoding="utf-8") as f:
                text = f.read()

            def tag(mo):
                pages = mo.group(1).strip().replace("-", "–")
                word = "page" if re.fullmatch(r"\d+", pages) else "pages"
                return f'<div class="src">Notebook {word} {pages}</div>\n'
            text = PAGES_RX.sub(tag, text)
            env = {"dir": os.path.dirname(full)}
            n_before = len(self.parts)
            rendered = self.md.render(text, env)
            if len(self.parts) == n_before:
                sys.exit(f"{path}: needs a '# Part title' heading")
            out.append(("PART", len(self.parts) - 1, rendered))
        htmls = katex(self.math)
        result = []
        for _, pi, rendered in out:
            rendered = re.sub(r"\x00MATH(\d+)\x00", lambda mo: htmls[int(mo.group(1))], rendered)
            result.append(self.divider(pi) + f'<section class="part" style="page: part{pi}">{rendered}</section>')
        return "\n".join(result)

    def divider(self, pi: int) -> str:
        p = self.parts[pi]
        items = "".join(f'<li><span class="n">{ROMAN[pi]}.{k}</span><span class="t">{html.escape(t)}</span></li>'
                        for k, (_, t) in enumerate(p["topics"], 1))
        return (f'<section class="divider"><div class="kicker">{html.escape(self.m["short"])}</div>'
                f'<div class="num">{ROMAN[pi]}</div><div class="ptitle">{html.escape(p["title"])}</div>'
                f'<ol>{items}</ol></section>')

    def contents(self, page_of) -> str:
        rows = []
        for lv, hid, label, title in self.toc:
            if lv > 2:
                continue
            pg = str(page_of.get(hid, "")) if page_of else "000"
            lab = f'<span class="toc-label">{html.escape(label)}</span>' if label else ""
            rows.append(f'<li class="toc-l{lv - 1}"><a href="#{hid}">{lab}<span class="toc-title">'
                        f'{html.escape(title)}</span><span class="toc-dots"></span>'
                        f'<span class="toc-page">{pg}</span></a></li>')
        note = self.d.get("note", "")
        note_html = f'<div class="toc-note">{note}</div>' if note else ""
        return f'<section class="toc"><h2 class="toc-head">Contents</h2><ol>{"".join(rows)}</ol>{note_html}</section>'

    def cover(self, total) -> str:
        m, d = self.m, self.d
        stats = [f"<div><b>{len(self.parts)}</b><span>parts</span></div>",
                 f"<div><b>{self.n_topics}</b><span>topics</span></div>"]
        if total:
            stats.append(f"<div><b>{total}</b><span>pages</span></div>")
        date = _dt.date.today().strftime("%B %Y")
        return f"""
<section class="cover">
  <div class="cover-art"></div>
  <div class="cover-top"><span class="badge">{html.escape(m.get('category', 'Notes'))}</span>
    <span class="brand">AI · ML · DS &nbsp;/&nbsp; Revision Notes</span></div>
  <div class="cover-main">
    <div class="provider">{html.escape(d.get('provider', ''))}</div>
    <div class="cover-title" role="heading" aria-level="1">{html.escape(d['title'])}</div>
    <p class="subtitle">{html.escape(d.get('subtitle', ''))}</p>
  </div>
  <div class="cover-foot">
    <div class="stats">{''.join(stats)}</div>
    <div class="meta">Compiled {date}<br>{html.escape(m.get('repository', ''))}</div>
  </div>
</section>"""

    def document(self, body: str, page_of=None, total=None) -> str:
        base = open(os.path.join(HERE, "notes_pdf", "style.css"), encoding="utf-8").read()
        kcss = open(os.path.join(NODE, "katex", "dist", "katex.min.css"), encoding="utf-8").read()
        kcss = kcss.replace("url(fonts/", f"url(file://{NODE}/katex/dist/fonts/")
        named = "\n".join(f'@page part{pi} {{ @top-left {{ content: "Part {ROMAN[pi]} · {css_str(p["title"])}"; }} }}'
                          for pi, p in enumerate(self.parts))
        mermaid = os.path.join(NODE, "mermaid", "dist", "mermaid.min.js")
        accent = self.m.get("accent", "#4f46e5")
        return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{html.escape(self.d['title'])}</title>
<style>{font_css()}
{kcss}
:root{{--accent:{accent};}}
{base}
{CSS}
@page {{ @top-right {{ content: "{css_str(self.d['short'])}"; }}
         @top-left {{ content: "{css_str(self.d.get('provider', ''))}"; }}
         @bottom-left {{ content: "Digital edition of the handwritten notes"; }} }}
{named}</style>
<script src="file://{mermaid}"></script></head><body>
{self.cover(total)}
{self.contents(page_of)}
<main>{body}</main>
<script>
window.__ready = (async () => {{
  mermaid.initialize({{ startOnLoad: false, theme: 'base', securityLevel: 'loose', fontFamily: 'NP Sans',
    flowchart: {{ htmlLabels: true, curve: 'basis', useMaxWidth: true }},
    themeVariables: {{ primaryColor: '#f1ecff', primaryBorderColor: '{accent}', primaryTextColor: '#0f172a',
      lineColor: '#64748b', fontSize: '13px', secondaryColor: '#eef6ff', tertiaryColor: '#fff7ed' }} }});
  await document.fonts.ready;
  await mermaid.run({{ querySelector: 'pre.mermaid' }});
}})();
</script>
</body></html>"""


def build(m: dict, work: str) -> str:
    d = m["digital"]
    doc = Doc(m)
    body = doc.body()
    out_dir = os.path.join(ROOT, d["out_dir"])
    os.makedirs(out_dir, exist_ok=True)
    final = os.path.join(out_dir, d["file"] + ".pdf")
    stem = d["file"]
    h1, p1 = os.path.join(work, f"{stem}-a.html"), os.path.join(work, f"{stem}-a.pdf")
    with open(h1, "w", encoding="utf-8") as f:
        f.write(doc.document(body))
    render([(h1, p1)])
    page_of, total = page_map(p1)
    h2 = os.path.join(work, f"{stem}-b.html")
    with open(h2, "w", encoding="utf-8") as f:
        f.write(doc.document(body, page_of, total))
    render([(h2, final)])
    os.remove(p1)
    finish_pdf(final, doc.toc, {"title": d["title"], "author": m.get("author", ""), "subtitle": d.get("subtitle", ""),
                                "category": m.get("category", ""), "provider": d.get("provider", "")})
    print(f"  -> {os.path.relpath(final, ROOT)}  ({total} pages, {os.path.getsize(final) / 1e6:.1f} MB)")
    return final


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", default=DEFAULT_MANIFEST)
    ap.add_argument("--work", default=os.path.join(HERE, ".cache", "digital"))
    args = ap.parse_args()
    with open(args.manifest, encoding="utf-8") as f:
        m = json.load(f)
    os.makedirs(args.work, exist_ok=True)
    print(f"* {m['digital']['title']}")
    build(m, args.work)


if __name__ == "__main__":
    main()
