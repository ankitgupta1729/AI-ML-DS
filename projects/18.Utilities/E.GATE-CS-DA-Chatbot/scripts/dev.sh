#!/usr/bin/env bash
# Run the whole app with one command: FastAPI backend (:8000) + React dev (:5173).
# Stop everything with Ctrl+C.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Prefer the project venv's uvicorn if present, else whatever is on PATH.
if [ -x ".venv/bin/uvicorn" ]; then
  UVICORN=".venv/bin/uvicorn"
else
  UVICORN="uvicorn"
fi

if [ ! -f ".env" ]; then
  echo "⚠️  No .env found. Copy .env.example to .env and set OPENAI_API_KEY first."
fi

echo "▶  Starting API on http://localhost:8000 ..."
"$UVICORN" api.main:app --host 0.0.0.0 --port 8000 --reload &
API_PID=$!

# Make sure the API is stopped when this script exits.
cleanup() { echo; echo "⏹  Stopping..."; kill "$API_PID" 2>/dev/null || true; }
trap cleanup EXIT INT TERM

cd frontend
if [ ! -d node_modules ]; then
  echo "📦  Installing frontend dependencies (first run)..."
  npm install
fi

echo "▶  Starting frontend on http://localhost:5173 ..."
echo "   → Open http://localhost:5173 in your browser."
npm run dev
