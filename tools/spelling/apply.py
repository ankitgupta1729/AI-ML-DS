#!/usr/bin/env python3
"""Apply the reviewed corrections in corrections.tsv to the course notes.

    python tools/spelling/apply.py --check   # show what would change, write nothing
    python tools/spelling/apply.py           # apply the corrections

Only the course notes listed in tools/notes-to-pdf/catalog.json are edited, and
only their prose: fenced code blocks, inline `code`, URLs and link/image
targets are never touched. Rebuild the PDFs afterwards.
"""
from __future__ import annotations

import argparse
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "notes-to-pdf"))

import build  # noqa: E402

# protected spans: fenced code, inline code, link/image targets, bare URLs
PROTECTED = re.compile(
    r"(?ms)^[ \t]*(```|~~~).*?^[ \t]*\1[^\n]*$"
    r"|`[^`\n]*`"
    r"|\]\([^)\n]*\)"
    r"|https?://[^\s)>\]]+"
)


def load_rules(path: str) -> list[dict]:
    rules = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                sys.exit(f"{path}:{n}: expected scope<TAB>find<TAB>replace")
            scope, find, repl = parts[:3]
            words = [re.escape(w) for w in find.split()]
            rx = re.compile(r"(?<!\w)" + r"\s+".join(words) + r"(?!\w)", re.I)
            rules.append({"line": n, "scope": None if scope == "*" else {s.strip().zfill(2) for s in scope.split(",")},
                          "find": find, "repl": repl, "rx": rx})
    # longer phrases first, so "Tenzer board" wins over "Tenzer"
    rules.sort(key=lambda r: -len(r["find"]))
    return rules


def fix_case(match: str, repl: str, sentence_start: bool) -> str:
    # speech-to-text capitalises misheard words ("a look at Col's"), so a capital
    # is only carried over at the start of a sentence or heading
    if sentence_start and match[:1].isupper() and repl[:1].islower():
        return repl[:1].upper() + repl[1:]
    return repl


def at_sentence_start(text: str, pos: int) -> bool:
    before = text[:pos].rstrip(" \t")
    return not before or before[-1] in ".!?:\n#*>-|\"("


def correct(text: str, rules: list[dict], hits: collections.Counter) -> str:
    out, pos = [], 0
    for m in PROTECTED.finditer(text):
        out.append(_prose(text[pos:m.start()], rules, hits))
        out.append(m.group(0))
        pos = m.end()
    out.append(_prose(text[pos:], rules, hits))
    return "".join(out)


def _prose(chunk: str, rules: list[dict], hits: collections.Counter) -> str:
    for r in rules:
        def sub(m, r=r, chunk=chunk):
            hits[r["line"]] += 1
            return fix_case(m.group(0), r["repl"], at_sentence_start(chunk, m.start()))
        chunk = r["rx"].sub(sub, chunk)
    return chunk


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="report changes without writing")
    ap.add_argument("--rules", default=os.path.join(HERE, "corrections.tsv"))
    args = ap.parse_args()
    rules = load_rules(args.rules)
    hits: collections.Counter = collections.Counter()
    changed = 0
    for job in build.load_catalog():
        if job.get("doc"):
            continue
        module = job["module"][:2]
        active = [r for r in rules if r["scope"] is None or module in r["scope"]]
        for src in job["sources"]:
            path = src["path"]
            with open(path, encoding="utf-8") as f:
                before = f.read()
            after = correct(before, active, hits)
            if after != before:
                changed += 1
                print(f"{'would fix' if args.check else 'fixed'}: {os.path.relpath(path, build.ROOT)}")
                if not args.check:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(after)
    unused = [r for r in rules if not hits[r["line"]]]
    for r in unused:
        print(f"! rule on line {r['line']} matched nothing: {r['find']!r}")
    print(f"{sum(hits.values())} corrections in {changed} file(s); {len(rules)} rules, {len(unused)} unused")
    return 1 if unused else 0


if __name__ == "__main__":
    sys.exit(main())
