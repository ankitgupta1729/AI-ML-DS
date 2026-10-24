"""Split a course-notes Markdown file into typed blocks.

The notes in this repo follow a few loose conventions rather than one strict
format, so the parser is deliberately forgiving:

* bare ``N.`` lines mark a lecture/section;
* ATX (``#``) and setext (``===`` / ``---``) headings both occur;
* screenshots are written as ``![x](./images/1.png)``, ``! [x](...)`` or even a
  plain link ``[1.png](./images/1.png)``;
* image folders are spelled ``images`` or ``Images``.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

IMAGE_EXT = r"(?:png|jpe?g|gif|webp|svg)"
IMG_LINE = re.compile(
    r"^\s*!?\s?\[(?P<alt>[^\]]*)\]\(\s*<?(?P<src>[^)>]+?\." + IMAGE_EXT + r")>?\s*\)\s*$",
    re.I,
)
INLINE_IMG = re.compile(r"!\s?\[(?P<alt>[^\]]*)\]\(\s*<?(?P<src>[^)>\s]+)>?\s*\)")
MARKER = re.compile(r"^\s*(\d{1,3})\.\s*$")
NUM_TITLE = re.compile(r"^\s*(\d{1,3})\.\s+(\S.{1,90})$")
ATX = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
LIST_START = re.compile(r"^\s*(?:[-*+]\s|\d+[.)]\s|>|\||<|\t| {4})")


@dataclass
class Block:
    kind: str  # img | marker | heading | code | para | other
    text: str = ""
    level: int = 0  # heading flavour, see HeadingKind
    hkind: str = ""  # marker | atx1..6 | setext1/2 | numtitle
    src: str = ""  # resolved image path
    alt: str = ""
    num: str = ""
    extra: dict = field(default_factory=dict)


def resolve_path(base: str, ref: str) -> str | None:
    """Resolve ``ref`` relative to ``base``; fall back to a case-insensitive match."""
    ref = ref.strip().replace("%20", " ")
    if re.match(r"^[a-z]+://", ref):
        return None
    p = os.path.normpath(os.path.join(base, ref))
    if os.path.exists(p):
        return p
    cur = base
    for part in os.path.normpath(ref).split(os.sep):
        if part in (".", ""):
            continue
        if part == "..":
            cur = os.path.dirname(cur)
            continue
        try:
            hit = [x for x in os.listdir(cur) if x.lower() == part.lower()]
        except OSError:
            return None
        if not hit:
            return None
        cur = os.path.join(cur, hit[0])
    return cur


def _is_num_title(line: str) -> bool:
    """``3. Model Deployments:`` on its own line works as a heading in hand-written notes."""
    m = NUM_TITLE.match(line)
    if not m:
        return False
    t = m.group(2).strip()
    return (len(t) <= 60 and len(t.split()) <= 8 and not t.endswith((".", "?", "!", ";", ","))
            and "`" not in t and "http" not in t and ". " not in t)


def _classify(lines: list[str], out: list[Block]) -> None:
    """Classify one blank-line separated chunk of non-image lines."""
    i = 0
    buf: list[str] = []

    def flush():
        if not buf:
            return
        first = buf[0]
        text = "\n".join(buf)
        if len(buf) == 1 and _is_num_title(first):
            m = NUM_TITLE.match(first)
            out.append(Block("heading", text=m.group(2).rstrip(": "), hkind="numtitle", num=m.group(1)))
        elif LIST_START.match(first):
            out.append(Block("other", text=text))
        else:
            out.append(Block("para", text=text))
        buf.clear()

    while i < len(lines):
        line = lines[i]
        m = ATX.match(line)
        if m:
            flush()
            out.append(Block("heading", text=m.group(2), hkind=f"atx{len(m.group(1))}"))
            i += 1
            continue
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if line.strip() and re.match(r"^\s*={3,}\s*$", nxt):
            flush()
            out.append(Block("heading", text=line.strip(), hkind="setext1"))
            i += 2
            continue
        if (line.strip() and re.match(r"^\s*-{3,}\s*$", nxt) and not LIST_START.match(line)
                and not buf):
            out.append(Block("heading", text=line.strip(), hkind="setext2"))
            i += 2
            continue
        buf.append(line)
        i += 1
    flush()


def parse(md_path: str) -> list[Block]:
    base = os.path.dirname(os.path.abspath(md_path))
    with open(md_path, encoding="utf-8", errors="replace") as f:
        lines = f.read().replace("\r\n", "\n").replace(" ", " ").split("\n")

    blocks: list[Block] = []
    chunk: list[str] = []

    def flush():
        if chunk:
            _classify(chunk, blocks)
            chunk.clear()

    i = 0
    while i < len(lines):
        line = lines[i]
        fm = FENCE.match(line)
        if fm:
            flush()
            fence = fm.group(1)
            body = [line]
            i += 1
            while i < len(lines):
                body.append(lines[i])
                if lines[i].strip().startswith(fence[0] * len(fence)) and len(body) > 1:
                    i += 1
                    break
                i += 1
            code = "\n".join(body)
            # an empty ``` ``` pair is noise, not content
            if any(line.strip() for line in body[1:-1]):
                blocks.append(Block("code", text=code))
            continue
        im = IMG_LINE.match(line)
        if im:
            flush()
            src = resolve_path(base, im.group("src"))
            blocks.append(Block("img", src=src or "", alt=im.group("alt"), extra={"ref": im.group("src")}))
            i += 1
            continue
        if not line.strip():
            flush()
            i += 1
            continue
        mk = MARKER.match(line)
        if mk:
            flush()
            blocks.append(Block("heading", hkind="marker", num=mk.group(1)))
            i += 1
            continue
        chunk.append(line)
        i += 1
    flush()
    for b in blocks:
        b.extra.setdefault("base", base)
    return blocks
