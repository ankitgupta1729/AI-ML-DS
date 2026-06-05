# 🎯 GateOverflow Chatbot

> **Your AI study buddy for GATE CS & DA — grounded in real previous-year questions.**

A production-ready **Retrieval-Augmented Generation (RAG)** assistant for
**GateOverflow** ([gateoverflow.in](https://gateoverflow.in)) that helps you
prepare for:

- **GATE CS** — Computer Science & Information Technology
- **GATE DA** — Data Science & Artificial Intelligence
- …and allied exams (ISRO, NIELIT, UGC-NET CS, TIFR)

Drop study material and previous-year-question (PYQ) PDFs into `data/`, the app
indexes it, and the bot answers grounded in that material — with **streaming
responses**, **source citations**, **conversation memory**, **LaTeX & code
rendering**, and a beautiful **React + Tailwind** interface.

```
┌──────────────┐   ingest    ┌────────────────┐  retrieve  ┌───────────────┐
│  data/*.pdf  │ ──────────▶ │  Chroma vector  │ ─────────▶ │   RAG engine   │
│  *.docx/*.md │  (OpenAI    │  store          │  top-k      │  + OpenAI LLM  │
└──────────────┘  embeddings)└────────────────┘  chunks     └───────┬───────┘
                                                                     │ SSE stream
                                          ┌──────────────────────────┴───────────┐
                                          │  FastAPI  ⇄  React + TS + Vite + TW   │
                                          └───────────────────────────────────────┘
```

---

## ✨ Features

- **RAG over your documents** — PDF, DOCX, PPTX, TXT, Markdown; recursive scan.
- **Rich knowledge base** — ships dense seed notes across the full CS & DA
  syllabus, plus a one-command fetcher for free/open textbooks, and ingests your
  own PYQ PDFs (CS, DA, ISRO, NIELIT, UGC-NET, TIFR).
- **Grounded answers with citations** — every answer can show source file,
  page/slide, similarity score and a snippet.
- **Broad, helpful scope** — answers across Computer Science, Data Science, ML
  and AI; politely declines only clearly-unrelated topics.
- **Conversation memory** — history-aware follow-ups (rewrites "what about its
  complexity?" into a standalone query).
- **Per-answer actions** — like 👍 / dislike 👎 / **copy** / **regenerate** on
  every turn, plus contextual **follow-up suggestion chips** — exactly like
  ChatGPT / Claude / DeepSeek.
- **Attachments** — 📎 attach **images** (a snapshot of a question is read by the
  vision model) or **PDF / text files** (extracted and used as context); paste
  images straight into the box.
- **Math & code rendering** — full **LaTeX** via KaTeX (auto-normalises
  `\(…\)` / `\[…\]` to `$…$`) and syntax-highlighted code blocks.
- **Natural small talk** — greetings like "hi" get a friendly welcome instead
  of a wrong retrieval-driven answer; clearly off-topic questions are politely
  declined.
- **GateOverflow look** — the familiar "GO + red ?" wordmark and brand colours.

### 🧪 Study suite (beyond chat)

A full GATE preparation workspace, navigable from the sidebar:

- **Mock Test & Practice** — LLM-generated MCQ/MSQ/NAT, **server-scored with GATE
  negative marking**, estimated percentile, per-question explanations. Wrong
  answers auto-become flashcards.
- **Flashcards & Spaced Repetition** — **SM-2** scheduling; generate cards on any
  topic or review the ones created from your mistakes.
- **Study Planner** — a day-by-day plan to your exam date; **export to calendar
  (.ics)**.
- **Performance Dashboard** — readiness score, accuracy by subject, weak-area
  detection, percentile and streak.
- **Daily question + streaks** — a question of the day with a hint and a habit streak.
- **Socratic tutor mode**, **multilingual answers** (Hindi & more), **voice in/out**
  (Web Speech), **draw/sketch a question**, and a **confidence (grounding) meter**
  on every answer.
- **Local/offline model** support via `OPENAI_BASE_URL` (Ollama/LM Studio/vLLM).
- **Built-in guide** — an in-app "How to use" walkthrough (auto-opens on first
  visit; reopen via the **?** button in the header) explains every feature and
  how to use it effectively.
- **GateOverflow PYQ links** — for previous-year-question answers (and *only*
  those), the exact GateOverflow question thread(s) are shown at the end of the
  answer, extracted from the URLs embedded in the PYQ PDFs
  (`python scripts/build_pyq_index.py` builds the lookup — no re-embedding).
- **Bookmarks & chat history** — ★ any answer to save it; revisit past
  conversations and saved answers from the **🕑 history** panel in the header.
- **Cheat-sheet & PDF export** — build a revision cheat-sheet from a chat, or
  export the whole conversation, to **PDF** (one click → print/save).
- **Optional reranking** — set `RERANK=true` (with `flashrank`) for cross-encoder
  reranking of citations.
- **PYQ practice mode** — ask for previous-year questions by exam (GATE CS / DA,
  ISRO, NIELIT, UGC-NET, TIFR), get step-by-step solutions, and ask follow-ups.
- **Feedback → RLHF loop** — every turn and rating is persisted; a disliked
  answer can be **regenerated steered by your feedback**, and corrections build
  a **preference dataset** you can export as JSONL for offline reward-model /
  DPO training. (See *Feedback & RLHF* below.)
- **Streaming UX** — tokens appear as they're generated (Server-Sent Events).
- **Modern frontend** — React 19 + TypeScript + Vite + Tailwind v4, dark/light
  mode, Markdown + KaTeX math + syntax-highlighted code, example prompts,
  expandable source cards. Fast, responsive, mobile-friendly.
- **Persistence** — SQLAlchemy (SQLite by default, Postgres-ready) stores
  conversations, messages, feedback and preference pairs.
- **Production API** — FastAPI with `/chat`, `/chat/stream` (SSE), `/feedback`,
  `/regenerate/stream`, `/export/preferences`, `/admin/stats`, `/health`, `/meta`.
- **Incremental, resilient ingestion** — content-hash chunk IDs (no duplicates),
  a manifest that skips unchanged files (only re-embeds what changed), per-file
  error isolation, progress logging — built for large multi-hundred-page PDFs.
- **Config via `.env`** — swap models, chunking, retrieval depth without code.
- **Docker & docker-compose** — one command to run frontend + API.

---

## 📁 Project structure

```
E.GATE-CS-DA-Chatbot/
├── api/main.py                 # FastAPI backend (/chat, /chat/stream, /meta, /health)
├── scripts/
│   ├── ingest.py               # Build / refresh the vector index (CLI)
│   └── fetch_open_resources.py  # Download free/open textbooks into data/
├── src/gate_chatbot/
│   ├── config.py               # Settings (env-driven)
│   ├── prompts.py              # Branding, system prompt, guardrail, templates
│   ├── ingestion.py            # Loaders, chunking, incremental indexing
│   ├── vectorstore.py          # Chroma + OpenAI embeddings
│   └── engine.py               # RAG orchestration (retrieve→guardrail→stream)
├── frontend/                   # React + TS + Vite + Tailwind UI
│   ├── src/                    # components, hooks, lib (SSE client)
│   ├── Dockerfile / nginx.conf # production build served by nginx
│   └── package.json
├── data/                       # ← your study material + PYQ PDFs (see data/README.md)
│   ├── seed/                   # dense starter notes (shipped with the repo)
│   └── GATA-Data/              # your attached PYQ PDFs (CS, DA, ISRO, NIELIT, …)
├── tests/test_smoke.py
├── requirements.txt
├── .env.example
├── Dockerfile / docker-compose.yml / Makefile
└── README.md
```

---

## 🚀 Quick start

### 1. Prerequisites
- **Python 3.10 – 3.12** (3.13+ may lack prebuilt `chromadb` wheels).
- **Node.js 18+** (for the frontend).
- An **OpenAI API key**.

### 2. Backend — install & configure

```bash
cd 18.Utilities/E.GATE-CS-DA-Chatbot

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # then set OPENAI_API_KEY=sk-...
```

### 3. Add knowledge & build the index

Your PYQ PDFs already live in `data/GATA-Data/`. Optionally pull free/open
textbooks too, then build the index:

```bash
python scripts/fetch_open_resources.py            # list open resources
python scripts/fetch_open_resources.py --download # (optional) download them

python scripts/ingest.py            # incremental — only embeds new/changed files
python scripts/ingest.py --reset    # clean rebuild
python scripts/ingest.py --stats    # how many chunks are indexed?
```

> First ingestion of the large PYQ PDFs (~137 MB) embeds many chunks and will
> take a few minutes and consume OpenAI credits. Subsequent runs skip unchanged
> files automatically (manifest-based incremental indexing).

### 4. Run the app

The app has **two parts** that must BOTH be running: the **API** (port 8000) and
the **frontend** (port 5173). You open the **frontend** in the browser.

#### Option A — one command (recommended)

```bash
make dev          # or:  bash scripts/dev.sh
```

This starts the API **and** the frontend together (installing frontend deps on
first run). Then open **<http://localhost:5173>**. Press `Ctrl+C` to stop both.

#### Option B — two terminals (manual)

```bash
# Terminal 1 — backend API (keep it running)
source .venv/bin/activate
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 — frontend (keep it running)
cd frontend
npm install        # first time only
npm run dev
```

Now open **<http://localhost:5173>** — the dev server proxies `/api` → the API on
port 8000. Start asking GATE questions. 🎉

> ⚠️ **Seeing nothing at http://localhost:5173?**
> That URL is the **frontend** — it only works while `npm run dev` (Terminal 2 /
> `make dev`) is running. Running only `uvicorn` starts just the API; the API
> itself lives at <http://localhost:8000/docs>, **not** 5173.

---

## 🔌 API reference

| Method | Endpoint               | Description                                          |
|--------|------------------------|------------------------------------------------------|
| GET    | `/health`              | Liveness, model, indexed-chunk count                 |
| GET    | `/meta`                | Branding (name, tagline, scope) + status             |
| POST   | `/chat`                | JSON answer + sources (synchronous, persisted)       |
| POST   | `/chat/stream`         | SSE token stream; `done` event returns `conversation_id` + `message_id` |
| POST   | `/feedback`            | Record like/dislike (+ reason, comment, correction)  |
| POST   | `/regenerate/stream`   | Regenerate an answer, steered by prior feedback      |
| GET    | `/export/preferences`  | Download the RLHF preference dataset as JSONL        |
| GET    | `/admin/stats`         | Conversation / message / feedback counters           |
| POST   | `/quiz/generate`       | Generate a quiz/mock test (questions sent without answers) |
| POST   | `/quiz/submit`         | Score with GATE negative marking; returns explanations + analytics |
| POST   | `/flashcards/generate` | Generate spaced-repetition cards on a topic          |
| GET    | `/review/due`          | Cards due for review (SM-2)                          |
| POST   | `/review/grade`        | Grade a card (0–5) → reschedule with SM-2            |
| POST   | `/plan/generate`       | Generate a day-by-day study plan                     |
| GET    | `/plan` · `/plan/calendar.ics` | Latest plan (JSON) / calendar export         |
| GET    | `/daily`               | Question of the day + streak                         |
| GET    | `/analytics`           | Readiness score, accuracy by subject, weak areas     |

```bash
curl -s http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"Explain dynamic programming with an example.","history":[]}' | jq
```

Interactive docs at <http://localhost:8000/docs>.

---

## 🐳 Docker

```bash
docker compose up --build
# Frontend → http://localhost:8080   (nginx serves the built React app)
# API      → http://localhost:8000
```

nginx proxies the frontend's `/api/*` calls to the `api` service, so the browser
talks to one origin. `data/` and `storage/` are mounted as volumes on the API so
your documents and index persist. Ingest inside the container with:

```bash
docker compose run --rm api python scripts/ingest.py
```

---

## ⚙️ Configuration reference (`.env`)

| Variable | Default | Meaning |
|---|---|---|
| `OPENAI_API_KEY` | — | **Required.** Your OpenAI key. |
| `CHAT_MODEL` | `gpt-4o-mini` | Answer model (`gpt-4o`/`gpt-4.1` for best quality). |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model for retrieval. |
| `TEMPERATURE` | `0.2` | Lower = more deterministic. |
| `MAX_TOKENS` | `1024` | Max answer length. |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | `1000` / `150` | Chunking for indexing. |
| `RETRIEVER_K` | `5` | Chunks retrieved per question. |
| `RELEVANCE_THRESHOLD` | `0.25` | Min similarity to treat a question as grounded (controls the "answered from general knowledge" note). |
| `COLLECTION_NAME` | `gate_cs_da` | Chroma collection name. |
| `API_HOST` / `API_PORT` | `0.0.0.0` / `8000` | API bind address. |

Frontend build-time var (`frontend/.env`): `VITE_API_BASE` (production API URL).

> **Changed the embedding model or chunk size?** Re-index with
> `python scripts/ingest.py --reset`.

---

## 🧠 How it works

1. **Ingestion** (`ingestion.py`) — each file is parsed to text, split into
   overlapping chunks, tagged with provenance (`source`, `subject`, page/slide),
   embedded with OpenAI and stored in **Chroma** with content-hash IDs. A JSON
   manifest records each file's size+mtime so unchanged files are skipped.
2. **Query reformulation** (`engine.py`) — a follow-up is rewritten into a
   standalone query using recent chat history.
3. **Retrieval** — top-`k` chunks by cosine similarity; the best score informs
   whether the answer is grounded in indexed material.
4. **Generation** — the system prompt keeps the assistant focused on CS / DS /
   ML / AI and GATE prep, injects retrieved context, and streams a grounded,
   exam-oriented answer.
5. **Citations** — de-duplicated sources are returned alongside the answer.

### Why RAG and not fine-tuning?
RAG keeps answers **current and source-grounded**, lets you **add/update
material instantly** (just re-ingest), avoids costly retraining, and reduces
hallucination by anchoring responses to your documents. Fine-tuning would lock
knowledge into weights and need retraining on every syllabus update.

---

## 🔁 Feedback & RLHF

Every question, answer and rating is stored (SQLAlchemy). The app implements the
practical, industry-standard **RLHF** workflow used by production assistants —
collect human preferences, then improve the model — split into an *online* and
an *offline* half:

**Online (immediate):**
- 👎 on an answer opens a quick feedback form (reason + comment + an optional
  "better answer"). Hitting **Regenerate** then calls `/regenerate/stream`,
  which feeds your dislike reason/comment back into the prompt so the model
  produces an improved, feedback-conditioned answer.

**Offline (training data → model update):**
- A **correction** to a disliked answer, or a regeneration that replaces a
  disliked one, is stored as a **preference pair** `(prompt, chosen, rejected)`
  in the `preference_pairs` table.
- Export them anytime as JSONL:
  ```bash
  curl -s http://localhost:8000/export/preferences -o preferences.jsonl
  ```
  This is exactly the format consumed by a **reward model** or **DPO** fine-tune
  ([TRL](https://huggingface.co/docs/trl) `DPOTrainer` / `RewardTrainer`,
  or OpenAI preference fine-tuning). Train offline, then point `CHAT_MODEL` at
  the improved model and redeploy.

> Full reward-model + PPO training is an offline process — this app provides the
> complete human-feedback **data collection + online steering** loop and the
> export pipeline that feeds it, which is the realistic RLHF phenomenon for a
> deployed RAG product.

**Data model** (`src/gate_chatbot/db.py`): `conversations` → `messages` →
`feedback`, plus `preference_pairs`.

---

## 🧪 Tests

```bash
pytest -q                      # offline backend smoke tests (no API key needed)
cd frontend && npm run build   # type-checks + builds the frontend
```

---

## 🛡️ Notes for production

- **Secrets:** keep `OPENAI_API_KEY` in `.env`/a secret manager — `.env` is git-ignored.
- **CORS:** `api/main.py` allows all origins for convenience — restrict to your
  front-end domain before deploying (or rely on the nginx same-origin proxy).
- **Auth & rate limiting:** add an API gateway / auth layer in front of FastAPI.
- **Persistent vector store:** for multi-instance deployments, point Chroma at a
  shared volume or migrate to a hosted vector DB.
- **Cost control:** `gpt-4o-mini` + `text-embedding-3-small` is the cheap
  default; monitor usage on the OpenAI dashboard.
- **Copyright:** only ingest material you're licensed to use (see `data/README.md`).

---

## 🗺️ Roadmap ideas

- Per-subject / per-exam filtering in the UI
- Reranking (cross-encoder) for sharper retrieval
- Citation click-through to the source page/PDF
- Evaluation harness with PYQ benchmark questions
- User accounts, saved chats, and shareable answers

---

Built for **GateOverflow** · part of the **AI-ML-DS** workspace ·
`18.Utilities/E.GATE-CS-DA-Chatbot`
