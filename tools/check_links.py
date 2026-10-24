#!/usr/bin/env python3
"""Check that relative links in the repository's own Markdown docs point at real files.

    python tools/check_links.py            # exit code 1 if any link is broken

Only repository-level docs are checked (READMEs, CONTRIBUTING, AGENTS, docs/,
tools/); course notes and third-party material are left alone. Targets are
resolved against ``git ls-files``, so this also works in a sparse checkout.
The PDF catalog (tools/notes-to-pdf/catalog.json) is validated the same way.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.parse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CATEGORIES = ["foundations", "data-engineering", "machine-learning", "deep-learning", "nlp",
              "generative-ai", "mlops", "dev-tools", "programming-languages", "career", "projects"]
LINK = re.compile(r"\]\(\s*<?([^)\s>]+(?:\\\)[^)\s>]*)*)>?(?:\s+\"[^\"]*\")?\s*\)")


def docs() -> list[str]:
    files = ["README.md", "CONTRIBUTING.md", "AGENTS.md"]
    files += [f"{c}/README.md" for c in CATEGORIES]
    for base in ("docs", "tools"):
        for dirpath, _, names in os.walk(os.path.join(ROOT, base)):
            files += [os.path.relpath(os.path.join(dirpath, n), ROOT) for n in names if n.endswith(".md")]
    return [f for f in files if os.path.exists(os.path.join(ROOT, f))]


def tracked() -> set[str]:
    """Every tracked file and directory, relative to the repo root."""
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
    paths = set()
    for f in out.decode("utf-8").split("\0"):
        while f:
            paths.add(f)
            f = os.path.dirname(f)
    return paths


def exists(path: str, known: set[str]) -> bool:
    rel = os.path.relpath(path, ROOT)
    return rel in known or os.path.exists(path)


def check_catalog(known: set[str]) -> int:
    with open(os.path.join(ROOT, "tools", "notes-to-pdf", "catalog.json"), encoding="utf-8") as f:
        cat = json.load(f)
    modules = {}
    for p in known:
        name = os.path.basename(p)
        if re.match(r"^\d{2}\.", name) and p.count("/") == 1:
            modules[name] = p
    bad = 0
    for e in cat["notes"]:
        if "path" in e:  # repository doc
            if e["path"] not in known:
                print(f"catalog: doc not found -> {e['path']}")
                bad += 1
            continue
        if e["module"] not in modules:
            print(f"catalog: module not found -> {e['module']}")
            bad += 1
            continue
        for s in e.get("sources") or [{"path": e["source"]}]:
            if f"{modules[e['module']]}/{s['path']}" not in known:
                print(f"catalog: note not found -> {e['module']}/{s['path']}")
                bad += 1
        if e["category"] not in cat["categories"]:
            print(f"catalog: unknown category {e['category']!r} for {e['module']}")
            bad += 1
    print(f"{len(cat['notes'])} catalog entries checked, {bad} problems")
    return bad


def main() -> int:
    known = tracked()
    broken = check_catalog(known)
    checked = 0
    for doc in docs():
        text = open(os.path.join(ROOT, doc), encoding="utf-8").read()
        text = re.sub(r"```.*?```", "", text, flags=re.S)  # code samples are not links
        text = re.sub(r"`[^`\n]*`", "", text)
        for target in LINK.findall(text):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            path = urllib.parse.unquote(target.split("#")[0]).replace("\\(", "(").replace("\\)", ")")
            checked += 1
            if not exists(os.path.normpath(os.path.join(ROOT, os.path.dirname(doc), path)), known):
                print(f"{doc}: broken link -> {target}")
                broken += 1
    print(f"{checked} links checked")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
