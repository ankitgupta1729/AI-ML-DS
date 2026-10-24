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
import ssl
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "data" / "open_resources"

# A real browser UA — some hosts (e.g. Microsoft Research) 403 a bare UA.
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

# (key, filename, url, licence, subject-subfolder)
#
# Licence legend used below:
#   "CC …"          — Creative-Commons / open educational resource (safe to share)
#   "free for study"— author-provided free PDF, copyright retained (personal use)
CATALOGUE: list[tuple[str, str, str, str, str]] = [
    # ---- Foundational mathematics ------------------------------------- #
    (
        "mml",
        "mathematics_for_machine_learning.pdf",
        "https://mml-book.github.io/book/mml-book.pdf",
        "Free for personal use (Deisenroth, Faisal, Ong — CUP)",
        "data_science_ai/math",
    ),
    (
        "mfcs",
        "mathematics_for_computer_science_mit6042.pdf",
        "https://courses.csail.mit.edu/6.042/spring18/mcs.pdf",
        "CC BY-SA (MIT 6.042 — Lehman, Leighton, Meyer)",
        "computer_science/discrete_math",
    ),
    (
        "dmoi",
        "discrete_mathematics_an_open_introduction.pdf",
        "https://discrete.openmathbooks.org/pdfs/dmoi3-tablet.pdf",
        "CC BY-SA 4.0 (Oscar Levin)",
        "computer_science/discrete_math",
    ),
    (
        "bookofproof",
        "book_of_proof_hammack.pdf",
        "https://richardhammack.github.io/BookOfProof/Main.pdf",
        "CC BY-ND (Richard Hammack)",
        "computer_science/discrete_math",
    ),
    (
        "convex",
        "convex_optimization_boyd.pdf",
        "https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf",
        "Free for study (Boyd & Vandenberghe — CUP)",
        "data_science_ai/math",
    ),
    (
        "itila",
        "information_theory_inference_learning_mackay.pdf",
        "https://www.inference.org.uk/itprnn/book.pdf",
        "Free for study (David MacKay — CUP)",
        "data_science_ai/math",
    ),
    # ---- Core computer science ---------------------------------------- #
    (
        "algorithms",
        "algorithms_jeff_erickson.pdf",
        "https://jeffe.cs.illinois.edu/teaching/algorithms/book/Algorithms-JeffE.pdf",
        "CC BY 4.0 (Jeff Erickson)",
        "computer_science/algorithms",
    ),
    (
        "ods",
        "open_data_structures.pdf",
        "https://opendatastructures.org/ods-cpp.pdf",
        "CC BY 2.5 (Pat Morin)",
        "computer_science/data_structures",
    ),
    (
        "ossc",
        "operating_systems_three_easy_pieces.pdf",
        "https://pages.cs.wisc.edu/~remzi/OSTEP/book.pdf",
        "Free online textbook (OSTEP, Arpaci-Dusseau)",
        "computer_science/operating_systems",
    ),
    # ---- Machine learning / statistics -------------------------------- #
    (
        "cs229",
        "cs229_main_notes.pdf",
        "https://cs229.stanford.edu/main_notes.pdf",
        "Stanford CS229 lecture notes (free for study)",
        "data_science_ai/machine_learning",
    ),
    (
        "islr",
        "introduction_to_statistical_learning.pdf",
        "https://hastie.su.domains/ISLR2/ISLRv2_corrected_June_2023.pdf",
        "Free for study (James, Witten, Hastie, Tibshirani)",
        "data_science_ai/machine_learning",
    ),
    (
        "esl",
        "elements_of_statistical_learning.pdf",
        "https://hastie.su.domains/ElemStatLearn/printings/ESLII_print12_toc.pdf",
        "Free for study (Hastie, Tibshirani, Friedman)",
        "data_science_ai/machine_learning",
    ),
    (
        "prml",
        "pattern_recognition_and_machine_learning_bishop.pdf",
        "https://www.microsoft.com/en-us/research/uploads/prod/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf",
        "Free PDF (Bishop — released by Microsoft Research)",
        "data_science_ai/machine_learning",
    ),
    (
        "uml",
        "understanding_machine_learning.pdf",
        "https://www.cs.huji.ac.il/~shais/UnderstandingMachineLearning/understanding-machine-learning-theory-algorithms.pdf",
        "Free for study (Shalev-Shwartz & Ben-David — CUP)",
        "data_science_ai/machine_learning",
    ),
    # ---- Deep learning / NLP / CV / RL / data mining ------------------ #
    (
        "d2l",
        "dive_into_deep_learning.pdf",
        "https://d2l.ai/d2l-en.pdf",
        "CC BY-SA 4.0",
        "data_science_ai/deep_learning",
    ),
    (
        "nlp",
        "speech_and_language_processing_jurafsky.pdf",
        "https://web.stanford.edu/~jurafsky/slp3/ed3book.pdf",
        "Jurafsky & Martin draft — free for study",
        "data_science_ai/nlp",
    ),
    (
        "cv",
        "computer_vision_algorithms_and_applications_szeliski.pdf",
        "http://szeliski.org/Book/drafts/SzeliskiBook_20100903_draft.pdf",
        "Free draft for study (Richard Szeliski — Springer)",
        "data_science_ai/computer_vision",
    ),
    (
        "rl",
        "reinforcement_learning_an_introduction_sutton_barto.pdf",
        "http://incompleteideas.net/book/RLbook2020.pdf",
        "Free PDF (Sutton & Barto — MIT Press)",
        "data_science_ai/reinforcement_learning",
    ),
    (
        "mmds",
        "mining_of_massive_datasets.pdf",
        "http://infolab.stanford.edu/~ullman/mmds/book.pdf",
        "Free for study (Leskovec, Rajaraman, Ullman — CUP)",
        "data_science_ai/data_mining",
    ),
    (
        "fods",
        "foundations_of_data_science.pdf",
        "https://www.cs.cornell.edu/jeh/book.pdf",
        "Free for study (Blum, Hopcroft, Kannan — CUP)",
        "data_science_ai/data_science",
    ),
    (
        "pml1",
        "probabilistic_machine_learning_an_introduction_murphy.pdf",
        "https://github.com/probml/pml-book/releases/download/2025-04-18/book1.pdf",
        "Free PDF release (Kevin Murphy — MIT Press)",
        "data_science_ai/machine_learning",
    ),
    (
        "cph",
        "competitive_programmers_handbook.pdf",
        "https://raw.githubusercontent.com/pllk/cphb/master/book.pdf",
        "CC BY-SA (Antti Laaksonen — GitHub pllk/cphb)",
        "computer_science/algorithms",
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
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            try:
                resp = urllib.request.urlopen(req, timeout=180)
            except ssl.SSLCertVerificationError:
                # A few academic hosts have mis-matched certs; retry without
                # verification (we only fetch public, openly-listed PDFs).
                print("   ⚠️  cert verify failed — retrying without verification")
                resp = urllib.request.urlopen(
                    req, timeout=180, context=ssl._create_unverified_context()
                )
            with resp as r, open(out, "wb") as f:
                f.write(r.read())
            print(f"   saved → {out.relative_to(ROOT)}  ({lic})")
        except Exception as exc:  # noqa: BLE001
            print(f"   ❌ failed: {exc}", file=sys.stderr)
            out.unlink(missing_ok=True)
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
