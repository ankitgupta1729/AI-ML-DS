#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md_to_pdf.py — Convert a Markdown (.md) file into a polished, professional PDF.

This reproduces the design used for the AI-ML-DS knowledge-base PDFs:
a gradient cover band, blue section headings, syntax-highlighted code,
styled tables/blockquotes, embedded & auto-downscaled images, and
page numbers in the footer.

------------------------------------------------------------------------------
HOW TO USE
------------------------------------------------------------------------------
1. Set INPUT_MD below to the .md file you want to convert (absolute or relative
   path). You can also pass the path on the command line, which overrides it:

       python3 md_to_pdf.py
       python3 md_to_pdf.py "../23.LangChain/Notes.md"

2. The PDF is written NEXT TO the .md file with the SAME name:
       Notes.md  ->  Notes.pdf
   If that PDF already exists, a new name is used instead (the original is
   never overwritten):
       Notes-formatted.pdf, Notes-formatted-2.pdf, ...

------------------------------------------------------------------------------
ONE-TIME SETUP (dependencies)
------------------------------------------------------------------------------
   pip3 install markdown pygments playwright pillow

   # Rendering uses your installed Google Chrome (no browser download needed).
   # If Playwright is unavailable, the script automatically falls back to
   # driving Chrome directly (page numbers are omitted in that fallback mode).
   #
   # `pillow` is optional; on macOS the built-in `sips` tool is used to
   # downscale images, so Pillow is only needed on Linux/Windows.
------------------------------------------------------------------------------
"""

import os
import re
import sys
import html as html_lib
import shutil
import hashlib
import subprocess
import tempfile

# ============================================================================
# CONFIG — set your input Markdown file here (command-line arg overrides it).
# ============================================================================
INPUT_MD = "REPLACE/WITH/PATH/TO/your_file.md"

# Image downscaling: max dimension (px) and JPEG quality for embedded images.
IMAGE_MAX_DIM = 1100
IMAGE_JPEG_QUALITY = 78
# Only downscale images larger than this many bytes.
IMAGE_MIN_BYTES = 120 * 1024


# ============================================================================
# Print theme (mirrors the AI-ML-DS knowledge-base PDF design).
# ============================================================================
THEME_CSS = r"""
:root{
  --ink:#1b232e; --ink-soft:#3d4756; --muted:#6b7686;
  --accent:#2563eb; --accent-2:#7c3aed; --accent-3:#0d9488;
  --rule:#e3e8ef; --rule-soft:#eef1f6; --code-bg:#f7f9fc;
  --code-ink:#243042; --quote-bg:#f7f9fc; --table-head:#eef3fb; --table-zebra:#f8fafc;
  --note-bd:#2563eb; --note-bg:#eff4ff; --tip-bd:#0d9488; --tip-bg:#ecfdf7;
  --warn-bd:#d97706; --warn-bg:#fff7ec; --ex-bd:#7c3aed; --ex-bg:#f6f3ff;
}
@page { size: A4; margin: 20mm 16mm 18mm 16mm; }
*{ box-sizing:border-box; }
html{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }
body{
  font-family:"Charter","Georgia","Iowan Old Style","Palatino Linotype",serif;
  color:var(--ink); font-size:10.7pt; line-height:1.66; margin:0;
  text-rendering:optimizeLegibility; font-feature-settings:"kern" 1,"liga" 1;
}
.cover{
  margin:0 0 24px 0; padding:28px 30px 24px 30px; border-radius:16px;
  background:radial-gradient(120% 140% at 0% 0%, #eef4ff 0%, #f6f0ff 45%, #ecfdf8 100%);
  border:1px solid var(--rule); page-break-inside:avoid;
}
.cover .eyebrow{
  font-family:"SF Pro Text",-apple-system,"Segoe UI",Roboto,sans-serif;
  text-transform:uppercase; letter-spacing:.15em; font-size:8pt; font-weight:800;
  color:var(--accent); margin:0 0 8px 0;
}
.cover h1.doc-title{
  font-family:"SF Pro Display",-apple-system,"Segoe UI",Roboto,sans-serif;
  font-size:25pt; line-height:1.1; font-weight:800; letter-spacing:-0.015em;
  color:var(--ink); margin:0 0 10px 0; border:none; padding:0;
}
.cover .desc{ font-family:"SF Pro Text",-apple-system,sans-serif; font-size:10pt;
  color:var(--ink-soft); margin:6px 0 2px; font-style:italic; }
.cover .meta{
  font-family:"SF Pro Text",-apple-system,"Segoe UI",Roboto,sans-serif;
  font-size:8.6pt; color:var(--muted); display:flex; flex-wrap:wrap; gap:6px 14px; margin-top:6px;
}
.cover .meta b{ color:var(--ink-soft); font-weight:700; }
.cover .accent-bar{ height:4px; width:70px; border-radius:4px; margin:4px 0 0 0;
  background:linear-gradient(90deg,var(--accent),var(--accent-2),var(--accent-3)); }
h1,h2,h3,h4,h5,h6{
  font-family:"SF Pro Display",-apple-system,"Segoe UI",Roboto,sans-serif;
  color:var(--ink); line-height:1.25; font-weight:800; margin:1.45em 0 .5em; page-break-after:avoid;
}
h1{ font-size:18.5pt; letter-spacing:-0.015em; padding-bottom:.24em; border-bottom:2.5px solid var(--accent); }
h2{ font-size:14.5pt; color:var(--accent); padding-bottom:.18em; border-bottom:1px solid var(--rule); }
h3{ font-size:12.4pt; color:var(--accent-2); }
h4{ font-size:11.2pt; color:var(--ink-soft); font-weight:700; }
h5{ font-size:10.2pt; color:var(--ink-soft); font-weight:700; }
h6{ font-size:9.4pt; color:var(--muted); font-weight:700; text-transform:uppercase; letter-spacing:.06em; }
h2::before{ content:""; display:inline-block; width:9px; height:9px; margin-right:10px;
  border-radius:2.5px; background:linear-gradient(135deg,var(--accent),var(--accent-3)); vertical-align:middle; }
a.headerlink, a.toclink{ display:none; }
p{ margin:.55em 0; }
strong,b{ font-weight:800; color:var(--ink); }
em,i{ font-style:italic; }
mark{ background:#fff3a8; color:inherit; padding:.02em .22em; border-radius:3px; }
a{ color:var(--accent); text-decoration:none; border-bottom:1px solid rgba(37,99,235,.3); }
del{ color:var(--muted); }
hr{ border:none; height:2px; margin:1.7em 0; border-radius:2px; opacity:.5;
  background:linear-gradient(90deg,var(--rule),var(--accent) 50%,var(--rule)); }
ul,ol{ margin:.5em 0 .75em; padding-left:1.55em; }
li{ margin:.25em 0; }
li::marker{ color:var(--accent); font-weight:700; }
code,kbd,pre,samp{ font-family:"JetBrains Mono","SFMono-Regular","Menlo","Consolas",monospace; }
:not(pre) > code{ background:#fdeef3; color:#b5345f; padding:.12em .42em; border-radius:5px;
  font-size:.85em; border:1px solid #f6d9e4; }
pre, .codehilite pre, .codehilite{
  background:var(--code-bg) !important; color:var(--code-ink); border:1px solid var(--rule);
  border-left:3.5px solid var(--accent); border-radius:9px; padding:13px 15px; overflow-x:auto;
  font-size:8.7pt; line-height:1.55; margin:.9em 0; page-break-inside:avoid;
  white-space:pre-wrap; word-wrap:break-word; box-shadow:0 1px 2px rgba(16,24,40,.04);
}
.codehilite{ padding:0; border:none; }
.codehilite pre{ margin:0; }
pre code{ background:none; border:none; padding:0; color:inherit; font-size:inherit; }
kbd{ background:#fff; border:1px solid #c6ccd6; border-bottom-width:2px; border-radius:5px;
  padding:.05em .45em; font-size:.82em; color:var(--ink); }
blockquote{ margin:1em 0; padding:.6em 1.05em; background:var(--quote-bg); border-left:4px solid var(--accent-3);
  border-radius:0 9px 9px 0; color:var(--ink-soft); page-break-inside:avoid; }
blockquote p{ margin:.32em 0; }
blockquote.callout-note{ background:var(--note-bg); border-left-color:var(--note-bd); }
blockquote.callout-tip{ background:var(--tip-bg); border-left-color:var(--tip-bd); }
blockquote.callout-warning{ background:var(--warn-bg); border-left-color:var(--warn-bd); }
blockquote.callout-example{ background:var(--ex-bg); border-left-color:var(--ex-bd); }
blockquote.callout-note strong:first-child{ color:var(--note-bd); }
blockquote.callout-tip strong:first-child{ color:var(--tip-bd); }
blockquote.callout-warning strong:first-child{ color:var(--warn-bd); }
blockquote.callout-example strong:first-child{ color:var(--ex-bd); }
table{ border-collapse:separate; border-spacing:0; width:100%; margin:1.1em 0; font-size:9.3pt;
  font-family:"SF Pro Text",-apple-system,"Segoe UI",Roboto,sans-serif; page-break-inside:avoid;
  border:1px solid var(--rule); border-radius:9px; overflow:hidden; box-shadow:0 1px 2px rgba(16,24,40,.04); }
thead th{ background:var(--table-head); color:var(--ink); font-weight:800; text-align:left;
  border-bottom:1.5px solid #d5deec; }
th,td{ border-bottom:1px solid var(--rule); border-right:1px solid var(--rule-soft);
  padding:8px 11px; vertical-align:top; }
th:last-child, td:last-child{ border-right:none; }
tbody tr:last-child td{ border-bottom:none; }
tbody tr:nth-child(even){ background:var(--table-zebra); }
figure{ margin:1.2em auto; text-align:center; page-break-inside:avoid; }
img{ max-width:100%; height:auto; border-radius:9px; display:block; margin:1em auto;
  border:1px solid var(--rule-soft); box-shadow:0 2px 8px rgba(16,24,40,.08); }
figure img{ margin:0 auto; }
figcaption{ font-family:"SF Pro Text",-apple-system,"Segoe UI",Roboto,sans-serif;
  font-size:8.4pt; color:var(--muted); font-style:italic; margin-top:7px; line-height:1.4; }
.katex{ font-size:1.02em; } .katex-display{ margin:.85em 0; overflow-x:auto; overflow-y:hidden; }
"""

# KaTeX (math) auto-render from CDN — renders $...$ / $$...$$ when online.
KATEX_HEAD = (
    '<link rel="stylesheet" '
    'href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">'
    '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>'
    '<script defer '
    'src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" '
    'onload="renderMathInElement(document.body,{delimiters:['
    "{left:'$$',right:'$$',display:true},"
    "{left:'$',right:'$',display:false},"
    "{left:'\\\\[',right:'\\\\]',display:true},"
    "{left:'\\\\(',right:'\\\\)',display:false}],throwOnError:false});\"></script>"
)

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]


def find_chrome():
    env = os.environ.get("CHROME_PATH")
    if env and os.path.exists(env):
        return env
    for c in CHROME_CANDIDATES:
        if os.path.exists(c):
            return c
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        p = shutil.which(name)
        if p:
            return p
    return None


# ----------------------------------------------------------------------------
# Frontmatter (simple YAML key: value) parsing.
# ----------------------------------------------------------------------------
def parse_frontmatter(src):
    if not src.startswith("---"):
        return {}, src
    end = src.find("\n---", 3)
    if end == -1:
        return {}, src
    raw = src[3:end].strip()
    body = src[end + 4:]
    if body.startswith("\n"):
        body = body[1:]
    data = {}
    for line in raw.split("\n"):
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            continue
        v = m.group(2).strip()
        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            v = v[1:-1]
        data[m.group(1)] = v
    return data, body


def clean_seg(s):
    s = re.sub(r"^[0-9]+\.\s*", "", s)
    s = re.sub(r"^[A-Z]\.\s*", "", s)
    s = re.sub(r"[-_.]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def derive_title(body, data, fallback):
    if data.get("title"):
        return data["title"]
    m = re.search(r"^\s*#\s+(.+?)\s*$", body, re.M)
    if m:
        return re.sub(r"[#*`_]", "", m.group(1)).strip()
    return fallback


def strip_leading_h1(body, title):
    lines = body.split("\n")
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i < len(lines) and re.match(r"^#\s+", lines[i]):
        h = re.sub(r"[#*`_]", "", re.sub(r"^#\s+", "", lines[i])).strip()
        if h.lower() == str(title).lower():
            return "\n".join(lines[i + 1:])
    return body


# ----------------------------------------------------------------------------
# Image downscaling (sips on macOS, Pillow elsewhere) -> cached JPEG copies.
# ----------------------------------------------------------------------------
def downscale_image(abs_src, cache_dir):
    try:
        size = os.path.getsize(abs_src)
        if size < IMAGE_MIN_BYTES:
            return abs_src
        key = hashlib.sha1(
            (abs_src + ":" + str(size) + ":" + str(os.path.getmtime(abs_src))).encode()
        ).hexdigest()
        out = os.path.join(cache_dir, key + ".jpg")
        if not os.path.exists(out):
            if sys.platform == "darwin" and shutil.which("sips"):
                subprocess.run(
                    ["sips", "-s", "format", "jpeg", "--setProperty", "formatOptions",
                     str(IMAGE_JPEG_QUALITY), "-Z", str(IMAGE_MAX_DIM), abs_src, "-o", out],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True,
                )
            else:
                from PIL import Image  # type: ignore
                im = Image.open(abs_src)
                if im.mode in ("RGBA", "P", "LA"):
                    bg = Image.new("RGB", im.size, (255, 255, 255))
                    im = im.convert("RGBA")
                    bg.paste(im, mask=im.split()[-1])
                    im = bg
                else:
                    im = im.convert("RGB")
                im.thumbnail((IMAGE_MAX_DIM, IMAGE_MAX_DIM))
                im.save(out, "JPEG", quality=IMAGE_JPEG_QUALITY)
        if os.path.getsize(out) < size:
            return out
        return abs_src
    except Exception:
        return abs_src


def shrink_images(html, base_dir, cache_dir):
    def repl(m):
        pre, src, post = m.group(1), m.group(2), m.group(3)
        if re.match(r"^(https?:|data:|file:)", src, re.I):
            return m.group(0)
        from urllib.parse import unquote
        rel = unquote(src)
        abs_src = os.path.normpath(os.path.join(base_dir, rel))
        if not os.path.exists(abs_src):
            return m.group(0)
        shrunk = downscale_image(abs_src, cache_dir)
        return pre + "file://" + shrunk + post

    return re.sub(r'(<img\b[^>]*\bsrc=")([^"]+)(")', repl, html)


# ----------------------------------------------------------------------------
# Tasteful, content-preserving HTML enhancements (callouts + image captions).
# ----------------------------------------------------------------------------
def enhance_html(html):
    def callout(m):
        lead, word = m.group(1), m.group(2)
        w = word.lower()
        kind = "note"
        if re.search(r"warning|caution|important", w):
            kind = "warning"
        elif re.search(r"tip|hint|remember", w):
            kind = "tip"
        elif re.search(r"example|use case", w):
            kind = "example"
        return '<blockquote class="callout callout-%s">%s%s' % (kind, lead, word)

    html = re.sub(
        r"<blockquote>(\s*<p>\s*(?:<(?:strong|b|em|i)>\s*)?)"
        r"(Note|Tip|Hint|Remember|Warning|Caution|Important|Example|Use Case|Key Takeaways?)\b",
        callout, html, flags=re.I,
    )

    def figure(m):
        img = m.group(1)
        am = re.search(r'\balt="([^"]*)"', img)
        alt = am.group(1).strip() if am else ""
        generic = re.match(r"^(image|img|images|picture|screenshot|diagram|figure|fig|pic)\s*[0-9]*$", alt, re.I)
        cap = ("<figcaption>%s</figcaption>" % alt) if (alt and len(alt) >= 3 and not generic) else ""
        return "<figure>%s%s</figure>" % (img, cap)

    html = re.sub(r"<p>\s*(<img\b[^>]*>)\s*</p>", figure, html)
    return html


# ----------------------------------------------------------------------------
# Markdown -> HTML
# ----------------------------------------------------------------------------
def render_markdown(body):
    import markdown  # pip install markdown
    from pygments.formatters import HtmlFormatter

    md = markdown.Markdown(
        extensions=[
            "extra",          # tables, fenced_code, def lists, footnotes, attr_list, etc.
            "sane_lists",
            "codehilite",     # pygments highlighting
            "admonition",
            "toc",
            "nl2br",
        ],
        extension_configs={
            "codehilite": {"guess_lang": False, "css_class": "codehilite"},
        },
        output_format="html5",
    )
    rendered = md.convert(body)
    pyg_css = HtmlFormatter(style="friendly").get_style_defs(".codehilite")
    return rendered, pyg_css


def build_html(body, data, eyebrow, title, src_name):
    body = strip_leading_h1(body, title)
    rendered, pyg_css = render_markdown(body)
    rendered = enhance_html(rendered)

    eb = eyebrow or "AI · ML · Data Science"
    if data.get("category"):
        eb = re.sub(r"[-_]+", " ", data["category"]).strip().title()

    date = data.get("date") or data.get("pubDate") or data.get("pubdate")
    tags = data.get("tags")
    if tags and re.match(r"^\[.*\]$", tags.strip()):
        tags = ", ".join(
            t.strip().strip("\"'") for t in tags.strip()[1:-1].split(",") if t.strip()
        )

    esc = html_lib.escape
    meta = ['<span><b>Source:</b> %s</span>' % esc(src_name)]
    if date:
        meta.append('<span><b>Date:</b> %s</span>' % esc(date))
    if data.get("author"):
        meta.append('<span><b>Author:</b> %s</span>' % esc(data["author"]))
    if tags:
        meta.append('<span><b>Tags:</b> %s</span>' % esc(tags))
    desc = ('<div class="desc">%s</div>' % esc(data["description"])) if data.get("description") else ""

    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<style>%s</style><style>%s</style>%s</head><body>
  <header class="cover">
    <div class="eyebrow">%s</div>
    <h1 class="doc-title">%s</h1>
    %s
    <div class="accent-bar"></div>
    <div class="meta">%s</div>
  </header>
  <main>%s</main>
</body></html>""" % (
        THEME_CSS, pyg_css, KATEX_HEAD,
        esc(eb), esc(title), desc, "".join(meta), rendered,
    )


# ----------------------------------------------------------------------------
# Output filename: same name, else -formatted / -formatted-N (never overwrite).
# ----------------------------------------------------------------------------
def unique_pdf_path(md_path):
    base = os.path.splitext(md_path)[0]
    cand = base + ".pdf"
    if not os.path.exists(cand):
        return cand
    cand = base + "-formatted.pdf"
    if not os.path.exists(cand):
        return cand
    i = 2
    while os.path.exists("%s-formatted-%d.pdf" % (base, i)):
        i += 1
    return "%s-formatted-%d.pdf" % (base, i)


def footer_template(title):
    t = html_lib.escape(title)[:90]
    return (
        '<div style="font-family:-apple-system,Segoe UI,Roboto,sans-serif;font-size:7pt;'
        'color:#9aa3b2;width:100%;padding:0 15mm;display:flex;justify-content:space-between;'
        'align-items:center;"><span style="max-width:70%;overflow:hidden;text-overflow:ellipsis;'
        'white-space:nowrap;">' + t + '</span><span>Page <span class="pageNumber"></span> / '
        '<span class="totalPages"></span></span></div>'
    )


def header_template():
    return (
        '<div style="font-family:-apple-system,Segoe UI,Roboto,sans-serif;font-size:7pt;'
        'color:#c2c9d6;width:100%;padding:0 15mm;text-align:right;">AI-ML-DS · Knowledge Base</div>'
    )


def to_pdf_playwright(tmp_html, out_pdf, title, chrome_path):
    """Best quality: page numbers + header/footer via Playwright + system Chrome."""
    from playwright.sync_api import sync_playwright
    launch_kwargs = {"args": ["--no-sandbox", "--font-render-hinting=none"]}
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel="chrome", **launch_kwargs)
        except Exception:
            browser = p.chromium.launch(executable_path=chrome_path, **launch_kwargs)
        page = browser.new_page()
        try:
            page.goto("file://" + tmp_html, wait_until="load", timeout=30000)
        except Exception:
            pass
        page.pdf(
            path=out_pdf, format="A4", print_background=True,
            display_header_footer=True, header_template=header_template(),
            footer_template=footer_template(title),
            margin={"top": "22mm", "bottom": "18mm", "left": "15mm", "right": "15mm"},
        )
        browser.close()
    return True


def to_pdf_chrome_cli(tmp_html, out_pdf, chrome_path):
    """Fallback: Chrome headless --print-to-pdf (no footer page numbers)."""
    for flag in ("--headless=new", "--headless"):
        try:
            subprocess.run(
                [chrome_path, flag, "--disable-gpu", "--no-sandbox",
                 "--no-pdf-header-footer", "--print-to-pdf=" + out_pdf,
                 "file://" + tmp_html],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                timeout=120, check=True,
            )
            if os.path.exists(out_pdf) and os.path.getsize(out_pdf) > 1000:
                return True
        except Exception:
            continue
    return False


def convert(md_path):
    md_path = os.path.abspath(md_path)
    if not os.path.isfile(md_path):
        sys.exit("ERROR: input file not found: %s" % md_path)
    if os.path.getsize(md_path) == 0:
        sys.exit("ERROR: input file is empty: %s" % md_path)

    with open(md_path, "r", encoding="utf-8") as f:
        src = f.read()

    data, body = parse_frontmatter(src)
    parent = os.path.basename(os.path.dirname(md_path))
    base = os.path.splitext(os.path.basename(md_path))[0]
    if re.match(r"^(notes?|note|readme|index|instructions|chainlit)\s*[0-9]*$", base, re.I):
        fallback = clean_seg(parent) or base
    else:
        fallback = clean_seg(base) or base
    title = derive_title(body, data, fallback)
    eyebrow = clean_seg(parent) if parent else None

    out_dir = os.path.dirname(md_path)
    cache_dir = os.path.join(tempfile.gettempdir(), "md_to_pdf_imgcache")
    os.makedirs(cache_dir, exist_ok=True)

    html = build_html(body, data, eyebrow, title, os.path.basename(md_path))
    html = shrink_images(html, out_dir, cache_dir)

    # Temp HTML lives in the output dir so relative image paths resolve via file://.
    tmp_html = os.path.join(out_dir, "." + base + ".__md2pdf__.html")
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html)

    out_pdf = unique_pdf_path(md_path)
    chrome = find_chrome()
    try:
        engine = None
        try:
            import playwright  # noqa: F401
            to_pdf_playwright(tmp_html, out_pdf, title, chrome)
            engine = "Playwright + Chrome (with page numbers)"
        except ImportError:
            if not chrome:
                sys.exit("ERROR: Google Chrome not found and Playwright not installed.\n"
                         "Install Chrome, or run: pip3 install playwright")
            if to_pdf_chrome_cli(tmp_html, out_pdf, chrome):
                engine = "Chrome headless (install 'playwright' for page numbers)"
            else:
                sys.exit("ERROR: PDF generation failed via Chrome CLI.")
    finally:
        try:
            os.remove(tmp_html)
        except OSError:
            pass

    print("OK  ->  %s" % out_pdf)
    print("    engine: %s" % engine)


def main():
    md = sys.argv[1] if len(sys.argv) > 1 else INPUT_MD
    if md == "REPLACE/WITH/PATH/TO/your_file.md":
        sys.exit("Set INPUT_MD at the top of this script, or pass a path:\n"
                 "    python3 md_to_pdf.py path/to/file.md")
    convert(md)


if __name__ == "__main__":
    main()
