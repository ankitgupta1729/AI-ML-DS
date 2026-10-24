"""Place each lecture screenshot next to the sentence it illustrates.

Most course notes were captured as "all screenshots of a lecture first, then the
full transcript". Every screenshot carries the lecturer's burned-in subtitle,
so OCR of a screenshot contains words spoken at the exact moment it was taken.
We find where those words occur in the transcript and move the screenshot
there.

Within one *unit* (an image run plus the prose that follows it, up to the next
image run) every screenshot gets a score for every sentence slot. Screenshots
must keep their original order, so the final placement is the monotone
assignment with the highest total score (a small dynamic programme).
Screenshots with no reliable match stay right after the previous placed one,
which keeps them in the same spot they had in the source when nothing matches.
"""
from __future__ import annotations

import re
from collections import defaultdict

from .parse import Block

WORD = re.compile(r"[a-z0-9]+")
SENT_SPLIT = re.compile(r"(?<=[.!?])[\"')\]]*\s+(?=[\"'(\[]?[A-Z0-9])")
ANCHOR_MIN = 2.5


def words(text: str) -> list[str]:
    return WORD.findall(text.lower())


def sentences(text: str) -> list[str]:
    text = re.sub(r"[ \t]*\n[ \t]*", " ", text.strip())
    return [s for s in SENT_SPLIT.split(text) if s.strip()]


def is_transcript_doc(blocks: list[Block]) -> bool:
    """True when screenshots are dumped in runs rather than placed by hand."""
    runs, cur = [], 0
    for b in blocks:
        if b.kind == "img":
            cur += 1
        elif cur:
            runs.append(cur)
            cur = 0
    if cur:
        runs.append(cur)
    total = sum(runs)
    clustered = sum(r for r in runs if r >= 2)
    return total >= 12 and clustered / total >= 0.6


def _ngrams(ws: list[str], n: int):
    return [tuple(ws[i:i + n]) for i in range(len(ws) - n + 1)]


class _Unit:
    def __init__(self, images: list[Block], body: list[Block]):
        self.images = images
        self.body = body
        # slots: (body index, sentence index or None, text)
        self.slots: list[tuple[int, int | None, str]] = []
        for bi, b in enumerate(body):
            if b.kind == "para":
                for si, s in enumerate(sentences(b.text)):
                    self.slots.append((bi, si, s))
            else:
                self.slots.append((bi, None, b.text if b.kind in ("code", "other") else ""))
        self.pos_slot: list[int] = []
        toks: list[str] = []
        for k, (_, _, t) in enumerate(self.slots):
            w = words(t)
            toks.extend(w)
            self.pos_slot.extend([k] * len(w))
        self.idx: dict[int, dict[tuple, list[int]]] = {2: defaultdict(list), 3: defaultdict(list)}
        for n in (2, 3):
            for p, g in enumerate(_ngrams(toks, n)):
                self.idx[n][g].append(p)

    def score(self, ocr: dict) -> list[float]:
        m = len(self.slots)
        sc = [0.0] * m
        sub = words(ocr.get("sub", "")) + ["\0"] + words(ocr.get("sub2", ""))
        full = words(ocr.get("full", ""))

        def add(grams, n, w, max_occ):
            seen = set()
            for g in grams:
                if g in seen:
                    continue
                seen.add(g)
                occ = self.idx[n].get(g)
                if not occ or len(occ) > max_occ:
                    continue
                for p in occ:
                    sc[self.pos_slot[p]] += w / len(occ)

        sub3 = _ngrams(sub, 3)
        add(sub3, 3, 3.0, 8)
        add(_ngrams(sub, 2), 2, 0.6, 3)
        add([g for g in _ngrams(full, 3) if g not in set(sub3)], 3, 1.0, 6)
        return sc

    def place(self, ocr_of) -> list[int]:
        """Return the slot index each image is inserted *before*."""
        m = len(self.slots)
        if m == 0:
            return [0] * len(self.images)
        scores = [self.score(ocr_of(im.src)) if im.src else [0.0] * m for im in self.images]
        anchored = [i for i, s in enumerate(scores) if max(s) >= ANCHOR_MIN]
        # monotone DP over anchored images: cur[k] = best total with image j at slot k
        pos = {}
        if anchored:
            n = len(anchored)
            back = [[0] * m for _ in range(n)]
            prev = [0.0] * m
            for j, i in enumerate(anchored):
                s = scores[i]
                run_best, run_arg = float("-inf"), 0
                cur = [0.0] * m
                for k in range(m):
                    base = prev[k] if j else 0.0
                    if base > run_best:
                        run_best, run_arg = base, k
                    cur[k] = run_best + s[k]
                    back[j][k] = run_arg
                prev = cur
            k = max(range(m), key=lambda x: prev[x])
            for jj in range(n - 1, -1, -1):
                pos[anchored[jj]] = k
                k = back[jj][k]
            # an image pushed off its match by the order constraint is not anchored
            for i in list(pos):
                if scores[i][pos[i]] < ANCHOR_MIN:
                    del pos[i]
        # unanchored screenshots between two anchors are spread evenly over the text
        # between them; trailing ones stay right after the last anchor
        out = [0] * len(self.images)
        known = sorted(pos)
        for i in range(len(self.images)):
            prev = max((k for k in known if k < i), default=None)
            nxt = min((k for k in known if k > i), default=None)
            if i in pos:
                out[i] = pos[i]
            elif nxt is None:
                out[i] = pos[prev] if prev is not None else 0
            else:
                lo, hi = (pos[prev], prev) if prev is not None else (0, -1)
                frac = (i - hi) / (nxt - hi)
                out[i] = lo + round(frac * (pos[nxt] - lo))
        for i in range(1, len(out)):  # keep the original order
            out[i] = max(out[i], out[i - 1])
        return out


def realign(blocks: list[Block], ocr_of) -> tuple[list[Block], dict]:
    """Return a new block list with screenshots moved next to their sentences."""
    stats = {"images": 0, "anchored_moves": 0, "units": 0}
    if not is_transcript_doc(blocks):
        return blocks, stats
    out: list[Block] = []
    i, n = 0, len(blocks)
    while i < n and blocks[i].kind != "img":
        out.append(blocks[i])
        i += 1
    while i < n:
        imgs = []
        while i < n and blocks[i].kind == "img":
            imgs.append(blocks[i])
            i += 1
        body = []
        while i < n and blocks[i].kind != "img":
            body.append(blocks[i])
            i += 1
        unit = _Unit(imgs, body)
        where = unit.place(ocr_of)
        stats["units"] += 1
        stats["images"] += len(imgs)
        stats["anchored_moves"] += sum(1 for w in where if w > 0)
        out.extend(_emit(unit, where))
    return out, stats


def _emit(unit: _Unit, where: list[int]) -> list[Block]:
    before: dict[int, list[Block]] = defaultdict(list)
    for im, k in zip(unit.images, where):
        before[k].append(im)
    res: list[Block] = []
    pending: list[str] = []
    pending_bi = None

    def flush_para():
        nonlocal pending_bi
        if pending:
            res.append(Block("para", text=" ".join(pending), extra={"transcript": True}))
            pending.clear()
        pending_bi = None

    for k, (bi, si, text) in enumerate(unit.slots):
        if before.get(k):
            flush_para()
            res.extend(before[k])
        if si is None:
            flush_para()
            res.append(unit.body[bi])
        else:
            if pending_bi is not None and pending_bi != bi:
                flush_para()
            pending.append(text)
            pending_bi = bi
    flush_para()
    res.extend(before.get(len(unit.slots), []))
    # images assigned past the last slot (only possible with no slots)
    for k in list(before):
        if k > len(unit.slots):
            res.extend(before[k])
    return res
