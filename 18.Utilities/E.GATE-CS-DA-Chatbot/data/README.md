# 📚 Knowledge Base — `data/`

Drop your study material here. Everything under this folder is read, chunked,
embedded and made searchable by the **GateOverflow Chatbot** when you run:

```bash
python scripts/ingest.py
```

## What's already here

- **`seed/`** — dense starter notes across the GATE CS & DA syllabus, shipped
  with the repo so the bot is useful immediately (these are committed).
- **`GATA-Data/`** — the previous-year-question (PYQ) PDFs you added
  (`aptitude`, `filter1_volume1-3`, `isro`, `nielit`, `tifr`, `ugcnet`).
  These are large and are **git-ignored** — they live on your machine, get
  embedded locally, and are never committed.

The top-level folder name becomes the `subject` tag shown in citations.

## Get more free, open material

Run the bundled fetcher to download openly-licensed textbooks (Mathematics for
ML, Dive into Deep Learning, CS229, OSTEP, Jurafsky & Martin) into
`data/open_resources/`:

```bash
python scripts/fetch_open_resources.py            # list the catalogue
python scripts/fetch_open_resources.py --download # download them
```

## Supported formats

`.pdf` · `.docx` · `.pptx` · `.txt` · `.md` / `.markdown`

## Recommended layout

Put files under a **subject sub-folder** — the folder name becomes the
`subject` tag shown in citations and is handy for filtering later.

```
data/
├── computer_science/      # GATE CS material
│   ├── algorithms/
│   ├── operating_systems/
│   ├── dbms/
│   ├── computer_networks/
│   ├── toc_compilers/
│   └── previous_year_papers/
├── data_science_ai/       # GATE DA material
│   ├── probability_statistics/
│   ├── linear_algebra/
│   ├── machine_learning/
│   ├── deep_learning/
│   └── previous_year_papers/
└── seed/                  # small starter notes shipped with the repo
```

You can nest folders as deep as you like — ingestion scans recursively.

## Where to get reliable, free, and authentic material

Only use authoritative sources so the bot gives trustworthy answers:

| Source | What | Link |
|---|---|---|
| **Official GATE website** | Syllabus, exam pattern, previous papers | <https://gate.iitX.ac.in> (current organising IIT) / <https://gate.iisc.ac.in> |
| **NPTEL** | Free university lectures & notes for every CS/DA subject | <https://nptel.ac.in> |
| **GATE Overflow** | Curated previous-year questions with solutions | <https://gateoverflow.in> |
| **MIT OpenCourseWare** | CS & math course notes / problem sets | <https://ocw.mit.edu> |
| **Stanford CS229 / CS231n** | Machine learning & deep learning notes | <https://cs229.stanford.edu> · <https://cs231n.github.io> |
| **"Dive into Deep Learning" (d2l.ai)** | Free, citable DL textbook | <https://d2l.ai> |
| **"Mathematics for Machine Learning"** | Free textbook (Deisenroth et al.) | <https://mml-book.github.io> |
| **GeeksforGeeks GATE** | Topic-wise notes (verify before trusting) | <https://www.geeksforgeeks.org/gate-cs-notes-gq> |

> ⚠️ **Copyright:** only ingest material you are licensed to use (public-domain,
> CC-licensed, official, or your own notes). This repo ships **no** copyrighted
> textbooks — you add what you are entitled to use.

After adding or changing files, re-run `python scripts/ingest.py`
(or `python scripts/ingest.py --reset` for a clean rebuild).
