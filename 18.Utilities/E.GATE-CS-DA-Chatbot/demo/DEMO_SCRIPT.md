# 🎬 GateOverflow Chatbot — Demo Kit

Everything you need to present the app: a **ready-made narrated video**, an
**editable wireframe**, a **storyboard/narration script**, and a set of
**sample Q&A** to type live.

## What's in `demo/`

| File | What it is | How to use |
|---|---|---|
| `GateOverflow-Chatbot-Demo.mp4` | ~3:25 narrated demo, 16 scenes (1080p, voiced) from **real app footage** — every feature + differentiation + GateOverflow PYQ links + site awareness + save/export | Play it directly in the meeting / embed in slides |
| `GateOverflow-Chatbot-Feature-Guide.mp4` | ~7:45 **detailed** guide (24 scenes) from **real screenshots of the running app** — incl. GateOverflow PYQ links, **GateOverflow platform awareness**, bookmarks & history, cheat-sheet & PDF export, sketch, multilingual (Hindi), Socratic, dislike→regenerate — per feature: purpose, example, benefit vs ChatGPT/Claude, how to use | Train the team / onboarding deep-dive |
| `live/` | Real screenshots captured from the running app (source stills for the guide video) | Reuse in slides/docs |
| `build_live_video.py` | Rebuilds the detailed guide from `live/` screenshots (run the app first, recapture, then this) | Regenerate the real-footage video |
| `GateOverflow-Chatbot-Demo.docx` | **Full documentation**: features, workflow, architecture, differentiation, sample Q&A, roadmap | Hand to the team / present alongside the video |
| `Why-GateOverflow-Chatbot.docx` | Shorter positioning doc (why it beats general chatbots) | Quick read / leave-behind |
| `wireframe.html` | Annotated wireframe + UX spec (screens, flow, components) | Open in a browser; Print → Save as PDF; or import to Figma |
| `build_video.py` / `build_demo_doc.py` | Regenerate the video / docx from scratch (offline) | `python demo/build_video.py` · edit `SCENES`/sections to customise |
| `frames/` | Per-scene PNGs + clips (build artifacts) | Reuse stills in slides |

> **Regenerate the video** anytime: `python demo/build_video.py`
> (needs Google Chrome + ffmpeg + macOS `say` — all already on this machine).
> Swap the voice via the `VOICE` constant, or edit any scene's `narration`/`body`.

---

## A. Live-demo storyboard (≈ 5 min)

Run the real app first:

```bash
# terminal 1 — backend (needs OPENAI_API_KEY in .env, index built)
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
# terminal 2 — frontend
cd frontend && npm install && npm run dev      # → http://localhost:5173
```

| # | Scene | Do this | Say this (narration) |
|---|---|---|---|
| 1 | **Intro** | Show the welcome screen | "This is the GateOverflow Chatbot — an AI tutor for GATE CS and DA, grounded in real previous-year questions." |
| 2 | **Greeting** | Type `Hi` | "It handles small talk naturally — a greeting gets a friendly welcome, not a wrong answer." |
| 3 | **Concept Q&A** | Ask *“Explain conflict serializability with an example.”* | "Ask anything in the syllabus. Answers stream live with proper maths, and cite the source material." |
| 4 | **Citations** | Expand the source card | "Every answer shows where it came from — file, page and a match score." |
| 5 | **Follow-up** | Click a follow-up chip (e.g. *Give me a similar PYQ*) | "Follow-up chips keep the conversation going with one click." |
| 6 | **PYQ practice** | Ask *“Give me a GATE CS PYQ on TLB effective access time and solve it.”* | "It has ingested thousands of PYQs — it poses the question and walks through the solution." |
| 7 | **Quiz** | Click **🧠 Quiz me** | "It can run an interactive quiz, one question at a time, and score you." |
| 8 | **Attachment** | 📎 attach a screenshot of a question (or paste an image) | "Stuck on a question in an image or PDF? Attach it — the vision model reads it and solves it." |
| 9 | **Feedback** | 👎 a reply, pick a reason, add a correction | "Rate any answer. A dislike opens a quick form and feeds the learning loop." |
| 10 | **Regenerate (RLHF)** | Click ↻ regenerate | "Regenerate re-answers, steered by your feedback — and stores a preference pair for offline RLHF training." |
| 11 | **Export** | Open `http://localhost:8000/export/preferences` | "All feedback exports as JSONL, ready for reward-model or DPO fine-tuning." |
| 12 | **Theme** | Toggle dark/light | "Polished, responsive UI in light and dark — built to production standards." |

---

## B. Sample questions to type (copy-paste)

These showcase breadth + the grounded/citation behaviour:

1. `Hi` — *(greeting handling)*
2. `Explain conflict serializability with a precedence-graph example.`
3. `Solve: a paged system has TLB hit ratio 0.9, TLB access 10 ns, memory access 100 ns. Find the effective access time.`
4. `Derive the time complexity of merge sort using the Master Theorem.`
5. `What is the bias–variance trade-off and how does regularisation help?` *(LaTeX-heavy)*
6. `Give me a GATE DA previous-year question on probability, then explain it step by step.`
7. `Quiz me with 5 mixed GATE CS MCQs, one at a time, and score me at the end.`
8. `What can you do?` — *(capabilities)*
9. `Tell me a joke about cricket.` — *(out-of-scope → polite decline)*

### Example interaction (what the bot returns)

> **You:** Solve: TLB hit ratio 0.9, TLB access 10 ns, memory access 100 ns — effective access time?
>
> **GO Buddy:**
> - **TLB hit** (prob 0.9): 10 + 100 = **110 ns**
> - **TLB miss** (prob 0.1): 10 + 100 + 100 = **210 ns**
> - **EAT** = 0.9·110 + 0.1·210 = **120 ns** ✅
>
> *Sources: filter1_volume2.pdf · p. 57 · GATA-Data · 88% match*

---

## C. Feature checklist (mention these)

- ✅ **RAG** over your PDFs / notes (CS · DS · ML · AI) with citations
- ✅ **Previous-year questions** ingested (GATE CS/DA, ISRO, NIELIT, UGC-NET, TIFR)
- ✅ **Streaming** answers · **LaTeX** maths · syntax-highlighted code
- ✅ **Per-answer actions**: copy · like · dislike · regenerate
- ✅ **Follow-up suggestions** + **interactive quiz**
- ✅ **Attachments**: image (vision) + PDF/text (extracted to context)
- ✅ **Greeting / out-of-scope** handling
- ✅ **Feedback → RLHF**: preference pairs + JSONL export for DPO/reward-model
- ✅ **Persistence**: SQLite (Postgres-ready) — conversations, messages, feedback
- ✅ **Stack**: React + TS + Vite + Tailwind ⇄ FastAPI ⇄ Chroma + OpenAI
- ✅ **Production-ready**: Docker, tests, configurable via `.env`, GateOverflow branding

---

## D. Turn the wireframe into a Figma file

1. Open `wireframe.html` in Chrome.
2. In Figma, install the **“html.to.design”** plugin.
3. Plugin → *Import* → paste the local file (or a hosted URL) → it imports
   editable layers matching these screens.

(Alternatively: Print the page to PDF and drop it into any slide deck.)
