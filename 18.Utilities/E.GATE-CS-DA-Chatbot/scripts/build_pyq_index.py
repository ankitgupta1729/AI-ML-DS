#!/usr/bin/env python3
"""Build a lookup of GateOverflow question URLs for the previous-year-question
(PYQ) PDFs in ``data/GATA-Data/``.

GateOverflow's compiled PYQ PDFs embed each question's thread as a *hyperlink
annotation* whose canonical form is ``https://gateoverflow.in/<id>/<slug>``
(e.g. .../2324/gate-cse-1993-question-28). This script collects those per page
and writes ``storage/pyq_urls.json``:

    { "<pdf path>": { "<page>": [ ["<url>", "<label>"], ... ] } }

The chat engine uses it at query time to show the exact GateOverflow link(s) at
the end of an answer for a retrieved PYQ chunk — **no re-embedding required**.
Run once (and again if you add/replace PYQ PDFs):

    python scripts/build_pyq_index.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gate_chatbot.config import get_settings  # noqa: E402

# Canonical "question" URL: numeric id + a descriptive slug (excludes /tag/,
# /user/, and bare-id duplicates).
CANON = re.compile(r"https?://(?:www\.)?gateoverflow\.in/(\d+)/([a-z0-9][a-z0-9-]{3,})", re.I)
_UP = {"gate": "GATE", "cse": "CSE", "it": "IT", "da": "DA", "ec": "EC",
       "ee": "EE", "me": "ME", "ce": "CE", "isro": "ISRO", "nielit": "NIELIT",
       "ugcnet": "UGC-NET", "tifr": "TIFR", "question": "Question", "set": "Set"}


def label_from_slug(slug: str) -> str:
    words = [_UP.get(w, w) for w in slug.split("-")]
    return " ".join(words)[:80]


def page_question_urls(page) -> list[tuple[str, str]]:
    """Canonical (url, label) pairs on a page, deduped by question id."""
    seen: dict[str, tuple[str, str]] = {}
    for a in page.get("/Annots") or []:
        try:
            uri = str((a.get_object().get("/A") or {}).get("/URI") or "")
        except Exception:  # noqa: BLE001
            continue
        m = CANON.search(uri)
        if not m:
            continue
        qid, slug = m.group(1), m.group(2)
        if qid in seen:
            continue
        url = f"https://gateoverflow.in/{qid}/{slug}"
        seen[qid] = (url, label_from_slug(slug))
    return list(seen.values())


def main() -> int:
    from pypdf import PdfReader

    settings = get_settings()
    pyq_dir = settings.data_dir / "GATA-Data"
    if not pyq_dir.exists():
        print(f"⚠️  PYQ folder not found: {pyq_dir}")
        return 1

    index: dict[str, dict[str, list]] = {}
    total = 0
    pdfs = sorted(pyq_dir.glob("*.pdf"))
    for pdf in pdfs:
        try:
            reader = PdfReader(str(pdf))
        except Exception as exc:  # noqa: BLE001
            print(f"  skip {pdf.name}: {exc}")
            continue
        per_page: dict[str, list] = {}
        for i, page in enumerate(reader.pages, start=1):
            qs = page_question_urls(page)
            # Skip index/TOC pages (an unusually long link list) to reduce noise.
            if qs and len(qs) <= 12:
                per_page[str(i)] = [[u, lbl] for u, lbl in qs]
                total += len(qs)
        if per_page:
            index[str(pdf.resolve())] = per_page
        print(f"  {pdf.name}: {sum(len(v) for v in per_page.values())} question links "
              f"on {len(per_page)} content pages")

    out = settings.vector_dir.parent / "pyq_urls.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(index), encoding="utf-8")
    print(f"\n✅ Wrote {out}  ({total} question links from {len(pdfs)} PDF(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
