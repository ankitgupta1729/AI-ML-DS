"""Recover readable titles from slide OCR.

Bare ``N.`` markers give a section no name, which makes for a useless table of
contents. The first slide of a section almost always shows its title at the
top, so we take the first OCR line that looks like real words. "Real" means
most of its words also occur in the section's own transcript, which filters
out OCR noise, logos and watermarks without needing a dictionary.
"""
from __future__ import annotations

import re
from collections import Counter

from .align import sentences, words
from .parse import Block

NOISE = re.compile(r"stanford|deeplearning|andrew ng|udemy|coursera|online|copyright|©|www\.|http", re.I)
COMMON = set("a an and are as at be by for from how in is it of on or the to vs what when why with your you "
             "we our this that use using".split())


STOP = set("""
a about above after again against all almost along already also although always am among an and another any
anyone anything are around as ask at away back be because been before being below between both but by can
cannot could did do does doing done down during each either else enough even ever every example
few first for from further get gets getting give given go goes going gonna good got great had has have
having he her here him his how however i if in into is it its itself just keep kind know known last later
least less let like likely little look looking lot lots made make makes making many may maybe me mean
means might more most much must my need needs new next no not now of off often ok okay on once one only
or other others our out over own part people perhaps pretty probably put quite rather really right said
same say saying says see seen she should show shown since so some something sometimes sort still such
sure take talk talked talking tell than that the their them then there these they thing things think
this those though three through thus to today together too took two under until up us use used useful
uses using very video videos want wanted wants was way ways we well went were what when where whether
which while who whole why will with within without would yeah yes yet you your yourself also actually
basically called lecture lectures course courses section slide slides week again hey hi hello welcome
thanks thank let's i'm you're we're it's that's there's don't can't doesn't isn't i've you'll we'll
going want gonna wanna couldn't here's what's let's okay alright cover covered next previous going
learn learned learning's simply different important specific certain actual
zero one two three four five six seven eight nine ten eleven twelve twenty thirty forty fifty
hundred thousand million first second third point dot minus plus equals
times comma colon bracket brackets parenthesis parentheses underscore quote quotes line lines box
someone something everyone everything somebody anybody coming come comes came idea ideas case cases
step steps long short big small high low
""".split())
SMALL = set("a an and as at but by for from in into nor of on or per the to vs via with".split())


def title_case(text: str) -> str:
    """Book-style title case that leaves acronyms, code and symbols alone."""
    out = []
    for i, w in enumerate(text.split()):
        core = w.strip("()[]{}\"'“”‘’:,;.!?")
        if not core or any(c.isdigit() for c in core) or (core.upper() == core and len(core) > 1):
            out.append(w)
        elif any(c.isupper() for c in core[1:]) or "_" in core or "." in core.strip("."):
            out.append(w)  # camelCase, snake_case, file.names
        elif i and core.lower() in SMALL and not out[-1].endswith(":"):
            out.append(w.replace(core, core.lower()))
        else:
            out.append(w.replace(core, core[0].upper() + core[1:]))
    return " ".join(out)


def keyphrase_titles(sections: list[str], top: int = 2) -> list[str]:
    """A short descriptive title per section from its most distinctive phrases.

    Candidate phrases are 1–3 word runs without stop words (``of`` is allowed
    inside, as in "bag of words"); each is scored by frequency in the section
    times rarity across sections, with longer phrases preferred.
    """
    import math
    docs = []
    for text in sections:
        ws = re.findall(r"[a-z][a-z0-9+\-']*", text.lower())
        grams: Counter = Counter()
        for n in (1, 2, 3):
            for i in range(len(ws) - n + 1):
                g = ws[i:i + n]
                if g[0] in STOP or g[-1] in STOP or len(g[0]) < 3 or len(g[-1]) < 3:
                    continue
                if any(t in STOP and t != "of" for t in g[1:-1]):
                    continue
                grams[" ".join(g)] += 1
        docs.append(grams)
    df: Counter = Counter()
    for g in docs:
        df.update(g.keys())
    n_docs = max(1, len(docs))
    casing = _casing(" ".join(sections))
    titles = []
    for grams in docs:
        scored = []
        for g, tf in grams.items():
            k = g.count(" ") + 1
            if tf < (2 if k > 1 else 4):
                continue
            idf = math.log((1 + n_docs) / (1 + df[g])) + 1
            scored.append((tf * idf * (0.8, 2.0, 2.4)[k - 1], g))
        scored.sort(reverse=True)
        picked: list[str] = []
        best = scored[0][0] if scored else 0
        for sc, g in scored:
            if len(picked) == top or sc < 0.75 * best:
                break
            if any(g in p or p in g for p in picked):
                continue
            picked.append(g)
        cased = [" ".join(casing.get(w, w) for w in g.split()) for g in picked]
        titles.append(title_case(" and ".join(cased)) if cased else "")
    return titles


def _casing(text: str) -> dict[str, str]:
    """Preferred spelling of each word: keep acronyms and brand casing (AI, TensorFlow)."""
    forms: dict[str, Counter] = {}
    for w in re.findall(r"[A-Za-z][A-Za-z0-9+\-']*", text):
        if w[1:] != w[1:].lower():  # only AI, GPUs, TensorFlow, ... count
            forms.setdefault(w.lower(), Counter())[w] += 1
    out = {}
    for low, c in forms.items():
        form, n = c.most_common(1)[0]
        lower_uses = len(re.findall(r"\b" + re.escape(low) + r"\b", text))
        if n >= 2 and n >= 0.5 * lower_uses:
            out[low] = form
    return out


SENTENCE_START = set("if to have so and but now this that these let we you it then because when "
                     "here there what how values just make is are".split())


DANGLING = SMALL | set("a an the that this these those which who whose its their his her our your is are was "
                       "were be been can will would should has have had also than then when where while "
                       "because so very more most such it they we you i".split())


def heading_like(title: str) -> bool:
    """Slide lines that read as headings rather than sentence fragments."""
    ws = title.split()
    if not (1 < len(ws) <= 7) or "," in title or ". " in title or (title.endswith("?") and len(ws) > 6):
        return False
    if ws[0].lower() in SENTENCE_START or title.rstrip().endswith(":"):
        return False
    if ws[-1].lower().strip(".:;!?") in DANGLING:
        return False  # "Reduces the", "A Technique That": cut-off sentences
    if re.match(r"^\d+(\.\d+)+", title):
        return False  # "1.2. Downloading ..." is a step, not a title
    for w in ws:
        core = w.strip("()[],.:;?!'\"")
        if len(core) == 1 and core.lower() != "a":
            return False
        if core[:1].islower() and any(c.isupper() for c in core[1:]):
            return False  # OCR case noise like "iS"
    return True


PROSE = re.compile(r"\b(is|are|was|were|has|have|uses|use|means|takes|gives|helps|allows|makes)\s+"
                   r"(a|an|the|very|two|three|many|some|it|this|that|to|not|been|used)\b", re.I)


def tidy_slide_title(title: str) -> str:
    """'ELU (Exponential Linear Units): This function …' -> 'ELU (Exponential Linear Units)'."""
    head, sep, tail = title.partition(":")
    if sep and tail.split() and tail.split()[0].lower() in SENTENCE_START | DANGLING:
        return head.strip()
    return title


def slide_title(ocr: dict, vocab: set[str]) -> str:
    sub = set(words(ocr.get("sub", "")))
    for raw in (ocr.get("full") or "").split("\n")[:6]:
        line = raw.strip(" .,;|_-—=~*'\"`©®°")
        if not re.fullmatch(r"[A-Z0-9][A-Za-z0-9 '’:,?&/()+.\-]*", line) or NOISE.search(line):
            continue
        ws = re.findall(r"[A-Za-z][A-Za-z0-9'’+\-]*", line)
        if not (2 <= len(ws) <= 9):
            continue
        lw = [w.lower() for w in ws]
        if any(a == b for a, b in zip(lw, lw[1:], strict=False)) or line.count("(") != line.count(")"):
            continue
        letters = sum(c.isalpha() or c == " " for c in line)
        if letters / max(1, len(line)) < 0.85:
            continue
        known = sum(1 for w, lo in zip(ws, lw, strict=True)
                    if lo in vocab or lo in COMMON or (w.isupper() and len(w) <= 5))
        real = sum(1 for w, lo in zip(ws, lw, strict=True) if (lo in vocab or lo in COMMON) and not w.isupper())
        if known / len(lw) < 0.7 or real < 2:
            continue
        if sum(1 for w in lw if w in sub) / len(lw) > 0.5:
            continue  # this is the subtitle strip, not the slide title
        if len(line) > 70:
            continue
        return re.sub(r"\s+", " ", line)
    return ""


def annotate(blocks: list[Block], ocr_of) -> None:
    """Set extra['title'] on screenshots and on untitled section markers."""
    sections: list[tuple[int, int]] = []
    start = 0
    for i, b in enumerate(blocks):
        if b.kind == "heading" and b.hkind == "marker" and i:
            sections.append((start, i))
            start = i
    sections.append((start, len(blocks)))
    texts = [" ".join(b.text for b in blocks[s:e] if b.kind in ("para", "other")) for s, e in sections]
    phrases = keyphrase_titles(texts)
    for n_sec, ((s, e), text, phrase) in enumerate(zip(sections, texts, phrases, strict=True)):
        vocab = set(words(text)) | {w for b in blocks[s:e] if b.kind == "heading" for w in words(b.text)}
        marker = blocks[s] if blocks[s].kind == "heading" and blocks[s].hkind == "marker" else None
        found = []
        for b in blocks[s:e]:
            if b.kind == "img" and b.src:
                t = slide_title(ocr_of(b.src), vocab)
                if t:
                    b.extra["title"] = title_case(tidy_slide_title(t))
                    found.append(b.extra["title"])
        if marker is None or marker.extra.get("title"):
            continue
        counts = Counter(found)
        # a line on a single slide is often body text: hold it to a stricter standard
        found = [t for t in found if heading_like(t) and (counts[t] > 1 or not PROSE.search(t))]
        if found:
            # the title most slides of the lecture share; ties go to the earliest
            counts = Counter(found)
            marker.extra["title"] = max(found, key=lambda t: (counts[t], -found.index(t)))
        elif phrase:
            opening = " ".join(sentences(text)[:2]).lower()
            intro = n_sec <= 1 and re.search(r"\bwelcome to\b", opening)
            marker.extra["title"] = f"Welcome — {phrase}" if intro else phrase
        elif text.strip():
            first = sentences(text)[0] if sentences(text) else text
            ws = first.split()
            marker.extra["title"] = first if len(ws) <= 9 else " ".join(ws[:8]).rstrip(",;:") + "…"


def tidy_headings(blocks: list[Block]) -> list[Block]:
    """Presentation-only fixes for headings in hand-written notes (text is never reworded).

    * a lone top-level ``#`` title duplicates the cover, so it is hidden;
    * ``# lowercase`` lines after the title are unfenced code comments, not headings;
    * numbers are split off (``## 16. Spark Web UI`` -> label 16, title "Spark Web UI");
    * a heading that is only a number gets a title from its section's key phrases.
    """
    heads = [b for b in blocks if b.kind == "heading" and b.hkind.startswith("atx")]
    out: list[Block] = []
    seen_heading = False
    for b in blocks:
        if b.kind == "heading" and b.hkind.startswith("atx") and seen_heading and b.text[:1].islower():
            out.append(Block("para", text=f"`# {b.text}`", extra=dict(b.extra)))
            continue
        if b.kind == "heading":
            seen_heading = True
        out.append(b)
    # "## Course Title" written where lecture "1." belongs (markers then start at 2)
    markers = [b for b in out if b.kind == "heading" and b.hkind == "marker"]
    first_head = next((b for b in out if b.kind == "heading"), None)
    if (markers and markers[0].num == "2" and first_head is not None and first_head.hkind.startswith("atx")
            and sum(1 for b in out if b.kind == "heading" and b.hkind == first_head.hkind) == 1):
        first_head.extra["title"] = first_head.text.strip()
        first_head.hkind, first_head.num = "marker", "1"
    h1 = [b for b in out if b.kind == "heading" and b.hkind == "atx1"]
    if heads and len(h1) == 1 and next(b for b in out if b.kind == "heading") is h1[0]:
        h1[0].extra["doctitle"] = True
    # split leading numbers; collect sections of number-only headings
    empty: list[int] = []
    for i, b in enumerate(out):
        if b.kind != "heading" or not b.hkind.startswith(("atx", "setext")):
            continue
        m = re.match(r"^\s*(\d{1,3})[.)]\s*(.*?)\s*:?\s*$", b.text)
        if m:
            b.extra["num"] = m.group(1)
            b.extra["bare"] = m.group(2)
            if not m.group(2):
                empty.append(i)
    if empty:
        def section_text(i):
            parts = []
            for nb in out[i + 1:]:
                if nb.kind == "heading":
                    break
                if nb.kind in ("para", "other", "code"):
                    parts.append(nb.text)
            return " ".join(parts)
        texts = [section_text(i) for i in empty]
        for i, text, phrase in zip(empty, texts, keyphrase_titles(texts, top=1), strict=True):
            first = sentences(text)[0] if sentences(text) else ""
            ws = first.split()
            out[i].extra["bare"] = phrase or (first if len(ws) <= 9 else " ".join(ws[:8]).rstrip(",;:") + "…")
    return out
