"""Turn parsed (and realigned) blocks into a print-ready HTML document."""
from __future__ import annotations

import datetime as _dt
import html
import os
import re

from markdown_it import MarkdownIt
from mdit_py_plugins.tasklists import tasklists_plugin
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name, guess_lexer

from .align import sentences
from .parse import FENCE, INLINE_IMG, Block, resolve_path

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(os.path.dirname(HERE), "fonts")
FONT_FACES = [  # family, file, weight, style
    ("NP Sans", "Inter-Regular", 400, "normal"), ("NP Sans", "Inter-Medium", 500, "normal"),
    ("NP Sans", "Inter-SemiBold", 600, "normal"), ("NP Sans", "Inter-Bold", 700, "normal"),
    ("NP Sans", "Inter-Italic", 400, "italic"), ("NP Sans", "Inter-SemiBoldItalic", 600, "italic"),
    ("NP Display", "InterDisplay-SemiBold", 600, "normal"), ("NP Display", "InterDisplay-Bold", 700, "normal"),
    ("NP Serif", "SourceSerif4-Regular", 400, "normal"), ("NP Serif", "SourceSerif4-SemiBold", 600, "normal"),
    ("NP Serif", "SourceSerif4-Bold", 700, "normal"), ("NP Serif", "SourceSerif4-Italic", 400, "italic"),
    ("NP Serif", "SourceSerif4-SemiBoldItalic", 600, "italic"),
    ("NP Mono", "JetBrainsMono-Regular", 400, "normal"), ("NP Mono", "JetBrainsMono-SemiBold", 600, "normal"),
]


def font_css() -> str:
    # static TrueType files: Chromium embeds these as real fonts (OTF/variable become Type 3)
    return "\n".join(
        f'@font-face{{font-family:"{fam}";src:url("file://{os.path.join(FONTS, f)}.ttf");'
        f"font-weight:{w};font-style:{st};}}" for fam, f, w, st in FONT_FACES)
JUNK = [
    re.compile(r"-*\s*\[\s*FreeCourseWeb\.com\s*\]\s*-*", re.I),
    re.compile(r"GetFreeCourses\.Co[-\s]*", re.I),
    re.compile(r"\.en\s*$"),
    re.compile(r"^\d{3}\s+"),  # "001 Introduction" (video file numbering)
    re.compile(r"^\[(?:slides|\d+)\]\s*-\s*", re.I),  # "[Slides] - …", "[1] - …"
]


def clean_heading(text: str) -> str:
    for rx in JUNK:
        text = rx.sub("", text)
    text = re.sub(r"[*_`]+", "", text)
    return text.strip(" -:#")


def _highlight(code: str, lang: str, _attrs) -> str:
    try:
        lexer = get_lexer_by_name(lang) if lang else guess_lexer(code)
        if not lang and lexer.name in ("Text only", "ABAP", "Tera Term macro"):
            lexer = TextLexer()
    except Exception:
        lexer = TextLexer()
    return highlight(code, lexer, HtmlFormatter(nowrap=True))


def _md(breaks: bool) -> MarkdownIt:
    # hand-written notes rely on single line breaks; keep them
    md = (MarkdownIt("commonmark", {"html": True, "linkify": False, "typographer": True, "breaks": breaks,
                                     "highlight": _highlight})
          .enable(["table", "strikethrough"]).use(tasklists_plugin))
    return md


class Renderer:
    def __init__(self, meta: dict, base_dir: str, image_info):
        self.meta = meta
        self.base = base_dir
        self.image_info = image_info  # src path -> prepared image dict
        self.md = _md(breaks=not meta.get("transcript"))
        self.toc: list[tuple[int, str, str, str]] = []  # level, id, label, title
        self.fig_no = 0
        self.sec_no = 0
        self.sec_fig = 0
        self.n_figures = 0
        self._ids = 0

    # ----- heading levels -------------------------------------------------
    def plan_levels(self, blocks: list[Block]) -> dict[str, int]:
        # numbered ATX section headings sometimes switch depth mid-file ("### 08 …", "## 09 …");
        # put them all on the shallowest depth used
        numbered = [b for b in blocks if b.kind == "heading" and b.hkind.startswith("atx")
                    and re.match(r"^\d+[.)]?\s", b.text)]
        depths = {b.hkind for b in numbered}
        if len(depths) > 1:
            for b in numbered:
                b.hkind = min(depths)
        order: list[str] = []
        for b in blocks:
            if b.kind == "heading" and b.hkind not in order:
                order.append(b.hkind)
        atx = sorted([k for k in order if k.startswith("atx")])
        it = iter(atx)
        order = [next(it) if k.startswith("atx") else k for k in order]
        # course sections written as ATX headings between per-lecture "N." markers
        # (far fewer of them) belong above the markers, whatever comes first
        if "marker" in order and atx:
            count = lambda k: sum(1 for b in blocks if b.kind == "heading" and b.hkind == k)
            top_atx = atx[0]
            if count(top_atx) <= count("marker") / 2 and order.index(top_atx) > order.index("marker"):
                order.remove(top_atx)
                order.insert(order.index("marker"), top_atx)
        return {k: min(i + 1, 4) for i, k in enumerate(order)}

    def _new_id(self) -> str:
        self._ids += 1
        return f"h{self._ids}"

    # ----- blocks ----------------------------------------------------------
    def heading(self, b: Block, level: int, transcript: bool) -> str:
        hid = self._new_id()
        if b.hkind == "marker":
            label, title = f"{'Lecture' if transcript or level > 1 else 'Section'} {b.num}", b.extra.get("title", "")
        elif b.hkind == "numtitle":
            label, title = f"{b.num}", clean_heading(b.text)
        elif "num" in b.extra:  # "## 16. Spark Web UI" (see titles.tidy_headings)
            label, title = b.extra["num"], clean_heading(b.extra["bare"])
        else:
            label, title = "", clean_heading(b.text)
        if b.extra.get("doctitle") or (not title and not label):
            return ""
        title = title[:1].upper() + title[1:]
        if level == 1:
            self.sec_no += 1
            self.sec_fig = 0
        self.toc.append((level, hid, label, title))
        tag = f"h{level + 1}"
        breaks = level == 1 and (transcript or b.hkind == "part")
        cls = f"lvl{level}" + (" page-break" if breaks else "")
        inner = ""
        if level == 1:
            num = b.num if b.hkind in ("marker", "numtitle") else b.extra.get("num", f"{self.sec_no:02d}")
            m = re.match(r"^(\d{1,3})[.)]?\s+(\S.*)$", title) if b.hkind not in ("marker", "numtitle") else None
            if m:  # "02 Installing Anaconda" -> kicker 02, title "Installing Anaconda"
                num, title = m.group(1), m.group(2)
                self.toc[-1] = (level, hid, label, title)
            kicker = {"numtitle": "Topic", "part": "Part",
                      "marker": "Lecture" if transcript else "Section"}.get(b.hkind, "Section")
            inner = f'<span class="kicker">{kicker} <b>{html.escape(num)}</b></span>'
            if b.hkind == "marker":
                inner += f'<span class="title">{html.escape(title) if title else "&#8203;"}</span>'
            else:
                inner += f'<span class="title">{self.inline(title)}</span>'
        else:
            text = f"{label} · {title}" if label and title else (title or label)
            inner = self.inline(text)
        return f'<{tag} id="{hid}" class="{cls}">{inner}</{tag}>'

    def inline(self, text: str) -> str:
        return self.md.renderInline(text)

    def figure(self, b: Block) -> str:
        info = self.image_info(b.src) if b.src else None
        if not info:
            return ""
        self.fig_no += 1
        self.sec_fig += 1
        self.n_figures += 1
        cap = f"Figure {self.sec_no}.{self.sec_fig}" if self.sec_no else f"Figure {self.fig_no}"
        alt = b.alt.strip()
        if alt and not re.match(r"^\s*(img|image|pic|screenshot)?\s*\d*\.?(png|jpe?g|gif|webp)?\s*$", alt, re.I):
            cap += f" — {html.escape(alt)}"
        elif b.extra.get("title"):
            cap += f'<span class="cap-title">{html.escape(b.extra["title"])}</span>'
        ratio = info["w"] / max(1, info["h"])
        shape = "wide" if ratio >= 1.25 else ("tall" if ratio < 0.8 else "square")
        return (f'<figure class="shot {shape}"><img src="file://{html.escape(info["path"])}" '
                f'width="{info["w"]}" height="{info["h"]}" alt="">'
                f'<figcaption>{cap}</figcaption></figure>')

    def paragraph(self, b: Block) -> str:
        text = b.text
        sents = sentences(text) if (b.extra.get("transcript") or len(text) > 900) else None
        if sents and len(text) > 700:
            chunks, cur, size = [], [], 0
            for s in sents:
                cur.append(s)
                size += len(s)
                if size > 650 and len(cur) >= 3:
                    chunks.append(" ".join(cur))
                    cur, size = [], 0
            if cur:
                chunks.append(" ".join(cur))
            return "".join(self._md_block(c) for c in chunks)
        return self._md_block(text, b.extra.get("base"))

    def _md_block(self, text: str, base: str | None = None) -> str:
        # images embedded inside prose (hand-placed) keep their position
        def sub(m):
            src = resolve_path(base or self.base, m.group("src"))
            if not src:
                return ""
            return "\n\n" + self.figure(Block("img", src=src, alt=m.group("alt"))) + "\n\n"
        text = INLINE_IMG.sub(sub, text)
        return self.md.render(text)

    # ----- document --------------------------------------------------------
    def body(self, blocks: list[Block], transcript: bool) -> str:
        levels = self.plan_levels(blocks)
        # give bare "N." markers a title from the heading that follows them
        for i, b in enumerate(blocks):
            if b.kind == "heading" and b.hkind == "marker":
                for nb in blocks[i + 1:i + 40]:
                    if nb.kind == "img":
                        continue
                    if nb.kind == "heading" and nb.hkind != "marker" and levels.get(nb.hkind, 9) > levels["marker"]:
                        b.extra["title"] = clean_heading(nb.text)
                        nb.extra["merged"] = True  # shown in the section title already
                    break
        parts = []
        for b in blocks:
            if b.kind == "heading":
                if not b.extra.get("merged"):
                    parts.append(self.heading(b, levels[b.hkind], transcript))
            elif b.kind == "img":
                parts.append(self.figure(b))
            elif b.kind == "code":
                parts.append(self.md.render(b.text))
            elif b.kind == "para":
                parts.append(self.paragraph(b))
            else:
                parts.append(self._md_block(b.text, b.extra.get("base")))
        return "\n".join(p for p in parts if p)

    def toc_html(self, page_of: dict[str, int] | None) -> str:
        top = min((lv for lv, *_ in self.toc), default=1)
        many = sum(1 for lv, *_ in self.toc if lv == top) > 30
        rows = []
        for lv, hid, label, title in self.toc:
            if lv > top + (0 if many else 1):
                continue
            pg = str(page_of.get(hid, "")) if page_of else "000"
            lab = f'<span class="toc-label">{html.escape(label)}</span>' if label else ""
            short = title if len(title) <= 72 else title[:70].rsplit(" ", 1)[0].rstrip(",;:.") + "…"
            ttl = html.escape(short) if title else ""
            rows.append(f'<li class="toc-l{lv - top}"><a href="#{hid}">{lab}'
                        f'<span class="toc-title">{ttl}</span><span class="toc-dots"></span>'
                        f'<span class="toc-page">{pg}</span></a></li>')
        if len(rows) < 2:
            return ""
        cls = "toc two-col" if len(rows) > 40 and all(len(t) < 40 for *_, t in self.toc) else "toc"
        return (f'<section class="{cls}"><h2 class="toc-head">Contents</h2>'
                f'<ol>{"".join(rows)}</ol></section>')

    def cover_html(self, pages: int | None) -> str:
        m = self.meta
        stats = []
        if self.sec_no:
            stats.append(f"<div><b>{self.sec_no}</b><span>sections</span></div>")
        if self.n_figures:
            stats.append(f"<div><b>{self.n_figures}</b><span>figures</span></div>")
        if pages:
            stats.append(f"<div><b>{pages}</b><span>pages</span></div>")
        vol = ""
        if m.get("volume"):
            vol = f'<div class="vol">Volume {m["volume"]} of {m["volumes"]} · {html.escape(m.get("range", ""))}</div>'
        date = _dt.date.today().strftime("%B %Y")
        return f"""
<section class="cover">
  <div class="cover-art"></div>
  <div class="cover-top"><span class="badge">{html.escape(m.get('category', 'Notes'))}</span>
    <span class="brand">AI · ML · DS &nbsp;/&nbsp; Revision Notes</span></div>
  <div class="cover-main">
    <div class="provider">{html.escape(m.get('provider', ''))}</div>
    <h1>{html.escape(m['title'])}</h1>
    <p class="subtitle">{html.escape(m.get('subtitle', ''))}</p>
    {vol}
  </div>
  <div class="cover-foot">
    <div class="stats">{''.join(stats)}</div>
    <div class="meta">Compiled {date}<br>github.com/ankitgupta1729/AI-ML-DS</div>
  </div>
</section>"""

    def document(self, body: str, page_of=None, pages=None) -> str:
        css = open(os.path.join(HERE, "style.css"), encoding="utf-8").read()
        pyg = HtmlFormatter(style="friendly").get_style_defs(".highlight, pre code")
        accent = self.meta.get("accent", "#4f46e5")
        css_str = lambda t: t.replace("\\", "\\\\").replace('"', '\\"')  # inside <style>: no HTML escaping
        short = css_str(self.meta.get("short", self.meta["title"]))
        vol = f" · Vol. {self.meta['volume']}" if self.meta.get("volume") else ""
        return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{html.escape(self.meta['title'])}</title>
<style>{font_css()}
:root{{--accent:{accent};}}
{css}
{pyg}
@page {{ @top-left {{ content: "{short}{vol}"; }}
         @bottom-left {{ content: "{css_str(self.meta.get('provider', 'Revision notes'))}"; }} }}</style></head><body>
{self.cover_html(pages)}
{self.toc_html(page_of)}
<main>{body}</main>
</body></html>"""
