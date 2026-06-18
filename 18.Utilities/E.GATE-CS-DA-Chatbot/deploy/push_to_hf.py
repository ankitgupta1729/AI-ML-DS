#!/usr/bin/env python3
"""Push the GateOverflow Chatbot to a Hugging Face **Docker Space** — no
git / git-lfs required (uses the ``huggingface_hub`` API, which handles large
files automatically).

What it uploads (mirrors deploy/setup_hf_space.sh):
  api/ src/ scripts/  ·  frontend/ (minus node_modules & dist)
  requirements.txt · .dockerignore
  Dockerfile           (copied from Dockerfile.prod — HF builds "Dockerfile")
  README.md            (copied from deploy/huggingface-space-README.md)
  storage/chroma/ + storage/pyq_urls.json   (the prebuilt vector index)

Credentials & target are supplied by YOU at run time — nothing is written to
disk or committed:

    export HF_TOKEN=hf_xxxx        # a *write* token from huggingface.co/settings/tokens
    python deploy/push_to_hf.py --space <user-or-org>/gateoverflow-chatbot \
        [--private] [--set-openai-key]

``--set-openai-key`` reads OPENAI_API_KEY from your local .env and stores it as
an **encrypted Space secret** (never baked into the image, never logged).
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _stage(staging: Path) -> None:
    """Assemble the exact file tree the Space should contain."""
    for d in ("api", "src", "scripts"):
        shutil.copytree(ROOT / d, staging / d,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for f in ("requirements.txt", ".dockerignore"):
        shutil.copy2(ROOT / f, staging / f)
    shutil.copy2(ROOT / "Dockerfile.prod", staging / "Dockerfile")
    shutil.copy2(ROOT / "deploy" / "huggingface-space-README.md",
                 staging / "README.md")

    # Frontend source (built inside the image) — skip node_modules & dist.
    shutil.copytree(
        ROOT / "frontend", staging / "frontend",
        ignore=shutil.ignore_patterns("node_modules", "dist", "*.log"),
    )

    # Prebuilt retrieval assets (the large files; the Hub stores them via LFS).
    chroma = ROOT / "storage" / "chroma"
    if not chroma.exists():
        sys.exit(f"❌ {chroma} not found — run: python scripts/ingest.py")
    shutil.copytree(chroma, staging / "storage" / "chroma")
    pyq = ROOT / "storage" / "pyq_urls.json"
    if pyq.exists():
        shutil.copy2(pyq, staging / "storage" / "pyq_urls.json")

    (staging / ".gitignore").write_text(
        "**/node_modules/\n**/__pycache__/\n*.pyc\nfrontend/dist/\n", "utf-8")


def _read_openai_key() -> str | None:
    env = ROOT / ".env"
    if not env.exists():
        return None
    for line in env.read_text("utf-8", "ignore").splitlines():
        line = line.strip()
        if line.startswith("OPENAI_API_KEY"):
            return line.split("=", 1)[1].strip().strip('"').strip("'") or None
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--space", required=True,
                    help="Target Space id, e.g. yourname/gateoverflow-chatbot")
    ap.add_argument("--private", action="store_true",
                    help="Create the Space as private (default: public).")
    ap.add_argument("--set-openai-key", action="store_true",
                    help="Store OPENAI_API_KEY from .env as an encrypted Space secret.")
    ap.add_argument("--chat-model", default=None,
                    help="Optionally set the CHAT_MODEL Space variable (e.g. gpt-4o-mini).")
    args = ap.parse_args()

    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    if not token:
        sys.exit("❌ Set HF_TOKEN (a write token) in your environment first.")

    from huggingface_hub import HfApi
    api = HfApi(token=token)

    print(f"🔧 Ensuring Space exists: {args.space} "
          f"({'private' if args.private else 'public'}, Docker SDK)")
    api.create_repo(repo_id=args.space, repo_type="space", space_sdk="docker",
                    private=args.private, exist_ok=True)

    if args.set_openai_key:
        key = _read_openai_key()
        if not key:
            sys.exit("❌ --set-openai-key given but OPENAI_API_KEY not found in .env")
        api.add_space_secret(repo_id=args.space, key="OPENAI_API_KEY", value=key)
        print("🔑 Stored OPENAI_API_KEY as an encrypted Space secret.")
    if args.chat_model:
        api.add_space_variable(repo_id=args.space, key="CHAT_MODEL", value=args.chat_model)
        print(f"⚙️  Set CHAT_MODEL = {args.chat_model}")

    with tempfile.TemporaryDirectory() as tmp:
        staging = Path(tmp) / "space"
        staging.mkdir()
        print("📂 Staging files …")
        _stage(staging)
        size_mb = sum(f.stat().st_size for f in staging.rglob("*") if f.is_file()) / 1e6
        print(f"⬆️  Uploading ~{size_mb:.0f} MB to {args.space} (large files via LFS) …")
        api.upload_folder(repo_id=args.space, repo_type="space",
                          folder_path=str(staging),
                          commit_message="Deploy GateOverflow Chatbot (expanded textbook index)")

    print(f"\n✅ Pushed. The Space will build automatically.")
    print(f"   URL: https://huggingface.co/spaces/{args.space}")
    print(f"   App: https://{args.space.replace('/', '-')}.hf.space")
    if not args.set_openai_key:
        print("\n⚠️  Set OPENAI_API_KEY in Space → Settings → Variables and secrets "
              "(or re-run with --set-openai-key).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
