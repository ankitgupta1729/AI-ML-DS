#!/usr/bin/env bash
# Populate a cloned Hugging Face Space repo with the GateOverflow Chatbot.
#
# Usage — run this from INSIDE your cloned Space directory:
#   cd gateoverflow-chatbot                      # the folder you `git clone`d from HF
#   bash /path/to/E.GATE-CS-DA-Chatbot/deploy/setup_hf_space.sh /path/to/E.GATE-CS-DA-Chatbot
#   git commit -m "Deploy GateOverflow Chatbot" && git push
#
set -euo pipefail

APP="${1:?Pass the path to the chatbot project dir (E.GATE-CS-DA-Chatbot)}"
APP="$(cd "$APP" && pwd)"

# Safety: make sure we're inside a Hugging Face Space git repo, not the app repo.
if [ ! -d .git ]; then
  echo "❌ Run this from inside your cloned Space folder (it must contain .git)."; exit 1
fi
if [ "$APP" = "$(pwd)" ]; then
  echo "❌ Don't run this inside the app project itself — run it in the cloned Space."; exit 1
fi

command -v git-lfs >/dev/null 2>&1 || { echo "❌ Install git-lfs first:  brew install git-lfs"; exit 1; }
[ -d "$APP/storage/chroma" ] || { echo "❌ $APP/storage/chroma not found. Run: python scripts/ingest.py"; exit 1; }

echo "📦  git-lfs init + track large files"
git lfs install
git lfs track "storage/**" "*.sqlite3" "*.bin" >/dev/null

echo "📂  Copying application files from $APP"
cp -R "$APP"/api "$APP"/src "$APP"/scripts ./
cp "$APP"/requirements.txt "$APP"/.dockerignore ./
cp "$APP"/Dockerfile.prod ./Dockerfile                      # HF builds a file named "Dockerfile"
cp "$APP"/deploy/huggingface-space-README.md ./README.md     # Space metadata (app_port: 8000)

# Frontend source (built inside the image) — without node_modules/dist
rm -rf frontend && mkdir -p frontend
rsync -a --exclude node_modules --exclude dist "$APP"/frontend/ ./frontend/

# Prebuilt retrieval assets (the only large files; tracked by LFS)
rm -rf storage && mkdir -p storage
cp -R "$APP"/storage/chroma ./storage/chroma
[ -f "$APP/storage/pyq_urls.json" ] && cp "$APP"/storage/pyq_urls.json ./storage/

# Keep the Space repo clean
cat > .gitignore <<'EOF'
**/node_modules/
**/__pycache__/
*.pyc
frontend/dist/
EOF

git add -A
echo
echo "✅ Staged. Files in the Space:"
git -c core.quotepath=false status --short | sed 's/^/   /' | head -40
echo
echo "👉 Next:"
echo "   git commit -m 'Deploy GateOverflow Chatbot'"
echo "   git push           # use your HF access token (write) as the password"
echo
echo "Then in the Space → Settings → Variables and secrets → add secret:"
echo "   OPENAI_API_KEY = sk-...   (and optionally Variable CHAT_MODEL = gpt-4o-mini)"
