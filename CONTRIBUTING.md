# Contributing

Corrections and suggestions are welcome — this repository gets better every time
someone spots a mistake.

## Where things go

The repository is organised by **domain**, then by **module**:

```
<category>/<NN>.<Module-Name>/
```

| Category | Holds |
| --- | --- |
| `foundations/` | Python, SQL, theory notes |
| `data-engineering/` | PySpark, Databricks |
| `machine-learning/` | Classical ML courses (Andrew Ng specialization, AI Nanodegree) |
| `deep-learning/` | TensorFlow and PyTorch courses, CNNs, GANs, computer vision |
| `nlp/` | NLP and transformers |
| `generative-ai/` | LLMs, RAG, LangChain, LangGraph, agents, Claude Code |
| `mlops/` | ML in production, MLflow, CI/CD, cloud |
| `dev-tools/` | Git, Docker, debugging, uv, pipenv, everyday tools |
| `programming-languages/` | Go |
| `career/` | Interview preparation, blogs, talks, retrospectives |
| `projects/` | Standalone utilities and side projects |
| `resources/` | Reference books and links |
| `docs/` | Repository-level guides |
| `tools/` | Repository tooling (PDF builder, layout migration) |

A new course gets the next free module number and goes into the matching
category, e.g. `deep-learning/62.My-New-Course/`. Inside a module:

```
62.My-New-Course/
├── Note.md          # your notes (screenshots referenced from images/)
├── images/          # screenshots: 1.png, 2.png, …
├── pdf/             # generated revision PDF(s) — do not edit by hand
└── *.ipynb, *.py    # code and notebooks
```

## Revision PDFs

After adding or editing course notes, rebuild their PDF:

```bash
python tools/notes-to-pdf/build.py 62        # rebuild module 62's PDF(s)
python tools/notes-to-pdf/build.py --verify  # check every generated PDF
```

New courses need one entry in `tools/notes-to-pdf/catalog.json`; see
[`tools/notes-to-pdf/README.md`](tools/notes-to-pdf/README.md).

## Spelling fixes

Corrections to the course notes (typos, misheard technical terms in transcripts) are
recorded in [`tools/spelling/corrections.tsv`](tools/spelling/corrections.tsv) and applied with
`python tools/spelling/apply.py` — see [`tools/spelling/README.md`](tools/spelling/README.md).
Add a row there rather than editing a transcript by hand, so the fix is reviewed and repeatable.

## Conventions

- **Commits** — short and descriptive (`Add <topic> notes`, `Fix typo in LangGraph notes`).
- **Notebooks** — clear large outputs and anything secret before committing.
- **Secrets** — keep API keys in a local `.env` (git-ignored); never commit them.
- **Large files** — GitHub rejects files over 100 MB. Datasets that notebooks
  download again belong in `.gitignore`, not in the repo.
- **Environments** — prefer a module-local `pyproject.toml`/`Pipfile` when a
  module needs its own dependencies.

## Checks

CI runs these on every pull request; run them locally before pushing:

```bash
ruff check --config tools/ruff.toml tools/   # lint the repository tooling
python tools/check_links.py                  # every link in the docs resolves
```

## Pull requests

1. Fork the repository and create a branch: `git checkout -b feature/your-topic`
2. Make the change in the right category/module
3. Open a pull request describing what changed and why
