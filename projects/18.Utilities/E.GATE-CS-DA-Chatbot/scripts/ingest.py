#!/usr/bin/env python3
"""Build (or rebuild) the vector index from documents in ``data/``.

Usage
-----
    python scripts/ingest.py            # incremental upsert
    python scripts/ingest.py --reset    # wipe the store and re-index everything
    python scripts/ingest.py --stats    # just print how many chunks are indexed
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Make ``src`` importable when run directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gate_chatbot.config import get_settings  # noqa: E402
from gate_chatbot.ingestion import build_index  # noqa: E402
from gate_chatbot.vectorstore import collection_size  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete the existing index before building.",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Print the number of indexed chunks and exit.",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s  %(levelname)-7s  %(message)s"
    )

    settings = get_settings()
    if not settings.openai_api_key:
        print("❌ OPENAI_API_KEY is not set. Copy .env.example to .env first.")
        return 1

    if args.stats:
        print(f"📊 Indexed chunks: {collection_size(settings)}")
        return 0

    print(f"📂 Scanning {settings.data_dir} …")
    summary = build_index(settings, reset=args.reset)
    skipped = summary.get("skipped", 0)

    if summary["files"] == 0 and skipped == 0:
        print(
            "⚠️  No documents found. Add PDFs / DOCX / PPTX / TXT / MD files "
            f"under {settings.data_dir} and run again."
        )
        return 1

    if summary["files"] == 0:
        print(f"✅ Up to date — {skipped} files already indexed, nothing to embed.")
    else:
        print(
            f"✅ Indexed {summary['chunks']} chunks from {summary['files']} "
            f"new/changed file(s) into '{settings.collection_name}' "
            f"({skipped} unchanged file(s) skipped)."
        )
    print(f"📊 Total chunks now indexed: {collection_size(settings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
