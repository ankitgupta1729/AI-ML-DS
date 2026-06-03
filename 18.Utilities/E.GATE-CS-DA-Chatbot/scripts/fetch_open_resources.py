#!/usr/bin/env python3
"""Download a curated set of **free / openly-licensed** CS & DS/ML/AI study
material into ``data/open_resources/`` so the chatbot starts knowledge-rich.

We only list sources that are genuinely free to download for study:
Creative-Commons textbooks, official syllabi, and authors' free PDFs. Always
respect each work's licence for redistribution — this script downloads copies
for *your own* local study/index, it does not redistribute them.

Usage
-----
    python scripts/fetch_open_resources.py            # list the catalogue
    python scripts/fetch_open_resources.py --download # actually download
    python scripts/fetch_open_resources.py --download --only mml d2l
"""

from __future__ import annotations

import argparse
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "data" / "open_resources"

# (key, filename, url, licence, subject-subfolder)
CATALOGUE: list[tuple[str, str, str, str, str]] = [
    (
        "mml",
        "mathematics_for_machine_learning.pdf",
        "https://mml-book.github.io/book/mml-book.pdf",
        "Free for personal use (Deisenroth, Faisal, Ong — CUP)",
        "data_science_ai",
    ),
    (
        "d2l",
        "dive_into_deep_learning.pdf",
        "https://d2l.ai/d2l-en.pdf",
        "CC BY-SA 4.0",
        "data_science_ai",
    ),
    (
        "cs229",
        "cs229_main_notes.pdf",
        "https://cs229.stanford.edu/main_notes.pdf",
        "Stanford CS229 lecture notes (free for study)",
        "data_science_ai",
    ),
    (
        "ossc",
        "operating_systems_three_easy_pieces.pdf",
        "https://pages.cs.wisc.edu/~remzi/OSTEP/book.pdf",
        "Free online textbook (OSTEP, Arpaci-Dusseau)",
        "computer_science",
    ),
    (
        "nlp",
        "speech_and_language_processing_jurafsky.pdf",
        "https://web.stanford.edu/~jurafsky/slp3/ed3book.pdf",
        "Jurafsky & Martin draft — free for study",
        "data_science_ai",
    ),
]


def _print_catalogue() -> None:
    print("📚 Open-resource catalogue (free / openly-licensed):\n")
    for key, fname, url, lic, sub in CATALOGUE:
        print(f"  • {key:6s} → {sub}/{fname}")
        print(f"           {url}")
        print(f"           licence: {lic}\n")
    print("Run with --download to fetch them into data/open_resources/.")
    print("⚠️  Verify each licence before any redistribution.")


def _download(only: set[str] | None) -> int:
    items = [c for c in CATALOGUE if not only or c[0] in only]
    if not items:
        print("Nothing matched --only", file=sys.stderr)
        return 1
    DEST.mkdir(parents=True, exist_ok=True)
    failures = 0
    for key, fname, url, lic, sub in items:
        out = DEST / sub / fname
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            print(f"✓ {key}: already present ({out.relative_to(ROOT)})")
            continue
        print(f"⬇️  {key}: downloading {url} …")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as r, open(out, "wb") as f:
                f.write(r.read())
            print(f"   saved → {out.relative_to(ROOT)}  ({lic})")
        except Exception as exc:  # noqa: BLE001
            print(f"   ❌ failed: {exc}", file=sys.stderr)
            failures += 1
    print(
        "\nDone. Now build the index:  python scripts/ingest.py"
        if not failures
        else f"\nCompleted with {failures} failure(s)."
    )
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--download", action="store_true", help="Download the files.")
    ap.add_argument("--only", nargs="*", default=None, help="Subset of keys to fetch.")
    args = ap.parse_args()
    if not args.download:
        _print_catalogue()
        return 0
    return _download(set(args.only) if args.only else None)


if __name__ == "__main__":
    raise SystemExit(main())
