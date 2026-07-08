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
The repository uses multiple dependency management systems depending on the module.

### Main Python Environment
- **Install dependencies**: `pipenv install` or `pip install -r requirements.txt`
- **Python version**: 3.11 (as specified in `Pipfile`)

### Sub-module Environments
- **uv (15.uv_demo)**: Uses `uv` for fast environment management.
- **Pipenv**: Several directories (e.g., `20.LlamaIndex`, `23.LangChain`) have their own `Pipfile`.
- **Go (19.Go)**: Standard Go commands like `go run <file>.go`.

## Coding Style & Naming Conventions
- **Language Dominance**: Python is the primary language, often used in Jupyter Notebooks (`.ipynb`) for interactive learning.
- **VS Code Integration**: Recommended settings are stored in `.vscode/settings.json`, with `python.terminal.activateEnvironment` disabled to allow manual control.

## Commit & Pull Request Guidelines
- **Commit Messages**: Use concise, descriptive messages. Common patterns in the repo include "added content" or "Add [topic] setup".
- **Workflow**: Direct commits are common for adding new learning materials. No specific PR template is enforced.
