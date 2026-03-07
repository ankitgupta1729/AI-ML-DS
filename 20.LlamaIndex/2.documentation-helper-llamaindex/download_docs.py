from collections import deque
from pathlib import Path
from urllib.parse import urljoin, urlparse, urldefrag

import requests
from bs4 import BeautifulSoup

START_URL = "https://developers.llamaindex.ai/python/framework/"
OUTPUT_DIR = Path("./llamaindex-docs")
MAX_PAGES = 300
TIMEOUT_SECONDS = 20


def normalize_url(url: str) -> str:
    clean, _ = urldefrag(url)
    return clean.split("?")[0]


def is_crawlable(url: str, allowed_netlocs: set[str], required_path_prefix: str) -> bool:
    parsed = urlparse(url)
    if parsed.netloc not in allowed_netlocs:
        return False
    if not parsed.path.startswith(required_path_prefix):
        return False
    if parsed.scheme not in {"http", "https"}:
        return False
    if parsed.path.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf", ".zip")):
        return False
    return True


def output_path_for(url: str, required_path_prefix: str) -> Path:
    parsed = urlparse(url)
    rel = parsed.path
    if rel.startswith(required_path_prefix):
        rel = rel[len(required_path_prefix) :]
    rel = rel.lstrip("/")
    if not rel or rel.endswith("/"):
        rel = f"{rel}index.html"
    if "." not in Path(rel).name:
        rel = f"{rel}.html"
    return OUTPUT_DIR / rel


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    start = normalize_url(START_URL)
    start_parts = urlparse(start)
    allowed_netlocs = {start_parts.netloc, "gpt-index.readthedocs.io"}
    required_path_prefix = "/python/"

    queue = deque([start])
    seen = set()
    downloaded = 0

    session = requests.Session()
    session.headers.update({"User-Agent": "docs-crawler/1.0"})

    while queue and downloaded < MAX_PAGES:
        url = queue.popleft()
        if url in seen:
            continue
        seen.add(url)

        try:
            response = session.get(url, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()
        except Exception as exc:
            print(f"skip {url} ({exc})")
            continue

        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        file_path = output_path_for(url, required_path_prefix)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(response.text, encoding="utf-8")
        downloaded += 1
        print(f"downloaded {url} -> {file_path}")

        for link in soup.find_all("a", href=True):
            absolute = normalize_url(urljoin(url, link["href"]))
            if (
                is_crawlable(absolute, allowed_netlocs, required_path_prefix)
                and absolute not in seen
            ):
                queue.append(absolute)

    print(f"done: downloaded {downloaded} html pages into {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
