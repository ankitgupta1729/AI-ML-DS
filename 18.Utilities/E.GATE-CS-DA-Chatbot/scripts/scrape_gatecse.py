#!/usr/bin/env python3
"""Polite scraper for **gatecse.in** (the GATE CSE wiki/blog by the GateOverflow
team) via its public WordPress REST API.

gatecse.in has a permissive robots.txt (Allow: /) and a clean REST API, so this
fetches every post and page in a structured form and writes:

  data/gatecse/gatecse.db                 — SQLite (table: content)
  data/gatecse/gatecse_content.jsonl      — one JSON record per line
  data/gatecse/<type>-<slug>.md           — clean Markdown for RAG ingestion

Then run `python scripts/ingest.py` to embed it into the chatbot's index.

Polite by design: a real User-Agent, a short delay between requests, timeouts,
and resilient error handling. Use the scraped content for your own study tool
and respect gatecse.in's terms / copyright.

NOTE: gateoverflow.in is intentionally NOT scraped here — it is behind an active
Cloudflare bot challenge and its robots.txt sets `ai-train=no`. Use the official
GateOverflow PYQ PDFs (already ingested) and the per-question links instead.

    python scripts/scrape_gatecse.py
"""

from __future__ import annotations

import html
import json
import re
import sqlite3
import sys
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "gatecse"
API = "https://gatecse.in/wp-json/wp/v2"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36 GateOverflowChatbot/1.0")
DELAY = 0.5  # seconds between requests (be polite)


# --------------------------------------------------------------------------- #
# HTML → clean text/markdown (dependency-free)                                #
# --------------------------------------------------------------------------- #
class _TextExtractor(HTMLParser):
    BLOCK = {"p", "div", "section", "article", "ul", "ol", "table", "tr",
             "h1", "h2", "h3", "h4", "h5", "h6", "br", "blockquote", "pre"}
    SKIP = {"script", "style", "noscript", "svg"}
    HEAD = {"h1": "# ", "h2": "## ", "h3": "### ", "h4": "#### ",
            "h5": "##### ", "h6": "###### "}

    def __init__(self):
        super().__init__()
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self._skip += 1
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag in self.HEAD:
            self.parts.append("\n\n" + self.HEAD[tag])
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip:
            self._skip -= 1
        elif tag in self.BLOCK or tag in self.HEAD:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self._skip and data.strip():
            self.parts.append(data)

    def text(self) -> str:
        t = html.unescape("".join(self.parts))
        t = re.sub(r"[ \t]+", " ", t)
        t = re.sub(r"\n[ \t]+", "\n", t)
        t = re.sub(r"\n{3,}", "\n\n", t)
        return t.strip()


def html_to_text(raw: str) -> str:
    p = _TextExtractor()
    try:
        p.feed(raw or "")
    except Exception:  # noqa: BLE001
        return re.sub(r"<[^>]+>", " ", raw or "")
    return p.text()


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return s[:80] or "untitled"


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


def fetch_all(kind: str) -> list[dict]:
    """Fetch every item of a WordPress collection (posts/pages), paginated."""
    items: list[dict] = []
    page = 1
    fields = "id,slug,date,modified,link,title,content,categories"
    while True:
        url = f"{API}/{kind}?per_page=50&page={page}&_fields={fields}"
        try:
            batch = fetch_json(url)
        except Exception as exc:  # noqa: BLE001 - end of pages returns 400
            if page > 1:
                break
            print(f"  ✗ {kind} page {page}: {exc}")
            break
        if not isinstance(batch, list) or not batch:
            break
        items.extend(batch)
        print(f"  {kind}: page {page} (+{len(batch)}, total {len(items)})")
        if len(batch) < 50:
            break
        page += 1
        time.sleep(DELAY)
    return items


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(OUT / "gatecse.db")
    db.execute(
        "CREATE TABLE IF NOT EXISTS content ("
        "id INTEGER, type TEXT, slug TEXT, title TEXT, url TEXT, "
        "date TEXT, modified TEXT, text TEXT, PRIMARY KEY (type, id))"
    )
    jsonl = (OUT / "gatecse_content.jsonl").open("w", encoding="utf-8")

    total = 0
    for kind in ("posts", "pages"):
        print(f"📥 Fetching {kind} …")
        for it in fetch_all(kind):
            title = html.unescape((it.get("title") or {}).get("rendered", "")).strip()
            text = html_to_text((it.get("content") or {}).get("rendered", ""))
            if not (title or text):
                continue
            rec = {
                "id": it.get("id"), "type": kind[:-1], "slug": it.get("slug", ""),
                "title": title, "url": it.get("link", ""),
                "date": it.get("date", ""), "modified": it.get("modified", ""),
                "text": text,
            }
            db.execute(
                "INSERT OR REPLACE INTO content VALUES (?,?,?,?,?,?,?,?)",
                (rec["id"], rec["type"], rec["slug"], rec["title"], rec["url"],
                 rec["date"], rec["modified"], rec["text"]),
            )
            jsonl.write(json.dumps(rec, ensure_ascii=False) + "\n")

            # Markdown file for RAG ingestion
            md = (f"# {title}\n\n"
                  f"_Source: [{rec['url']}]({rec['url']}) · gatecse.in · "
                  f"updated {rec['modified'][:10]}_\n\n{text}\n")
            (OUT / f"{rec['type']}-{slugify(rec['slug'] or title)}.md").write_text(
                md, encoding="utf-8")
            total += 1

    db.commit()
    db.close()
    jsonl.close()
    print(f"\n✅ Scraped {total} items from gatecse.in")
    print(f"   • SQLite : {OUT / 'gatecse.db'}")
    print(f"   • JSONL  : {OUT / 'gatecse_content.jsonl'}")
    print(f"   • Markdown for RAG: {OUT}/*.md")
    print("\nNext: python scripts/ingest.py   (embeds the new material)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
