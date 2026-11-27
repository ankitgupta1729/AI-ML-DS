# Repository Guidelines

## Project Overview
This repository is a comprehensive collection of tutorials, practice exercises, and utilities covering AI, Machine Learning, Data Science, and modern software engineering tools. It includes hands-on materials for Python, PySpark, SQL, Go, Docker, LangChain, and LlamaIndex.

## Project Structure & Module Organization
The repository is organized into numbered directories, each dedicated to a specific topic:
- **Python & DS Basics**: `1.Python`, `3.SQL`, `4.Theory`
- **Big Data & Infrastructure**: `2.PySpark`, `11.Docker`, `14.Databricks`
- **LLM & AI Orchestration**: `20.LlamaIndex`, `23.LangChain`, `24.LangChain2`
- **Utilities & Tooling**: `18.Utilities` contains various helper scripts like `images_to_pdf.py` and `send-mail.py`.
- **Tutorials**: `25.Claude-Code-Deep-Dive` contains specific agent-related learning materials.

## Build, Test, and Development Commands

### Python Environment (one for the whole repo)

- **Single venv**: the root `.venv/`, defined by `pyproject.toml` and pinned by `uv.lock`. Python version is in `.python-version` (3.12).
- **Install / update**: `uv sync` at the repo root. **Add a package**: `uv add <pkg>` at the root.
- **Jupyter kernel**: `ai-ml-ds` (→ `.venv/bin/python`). Every notebook's `metadata.kernelspec.name` must be `ai-ml-ds`, including new ones.
- **Do not** create per-folder venvs, Pipfiles or requirements files for running code. The `Pipfile` / `requirements.txt` / `pyproject.toml` files inside course folders (e.g. `15.uv_demo`, `21.pipenv-course`, `24.LangChain2`) are course material only.
- Some course notebooks use CRLF line endings, so keep them unchanged when editing notebook JSON.

### Other languages

- **Go (19.Go)**: Standard Go commands like `go run <file>.go`.

## Coding Style & Naming Conventions
- **Language Dominance**: Python is the primary language, often used in Jupyter Notebooks (`.ipynb`) for interactive learning.
- **VS Code Integration**: Recommended settings are stored in `.vscode/settings.json`, with `python.terminal.activateEnvironment` disabled to allow manual control.

## Commit & Pull Request Guidelines
- **Commit Messages**: Use concise, descriptive messages. Common patterns in the repo include "added content" or "Add [topic] setup".
- **Workflow**: Direct commits are common for adding new learning materials. No specific PR template is enforced.
