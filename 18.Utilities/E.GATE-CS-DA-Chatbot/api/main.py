"""Production FastAPI backend exposing the chat engine.

Endpoints
---------
GET  /health             liveness + index size
GET  /meta               branding + capability info
POST /chat               synchronous JSON answer with sources (persisted)
POST /chat/stream        token-by-token Server-Sent Events stream (persisted)
POST /feedback           record like / dislike (+ reason, comment, correction)
POST /regenerate/stream  regenerate an answer, steered by prior feedback (RLHF)
GET  /export/preferences  export the RLHF preference dataset as JSONL
GET  /admin/stats        usage + feedback counters
"""

from __future__ import annotations

import base64
import io
import json
import logging
import sys
from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from fastapi.responses import (  # noqa: E402
    FileResponse,
    HTMLResponse,
    PlainTextResponse,
    StreamingResponse,
)
from fastapi.staticfiles import StaticFiles  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

from gate_chatbot import __version__  # noqa: E402
from gate_chatbot import db  # noqa: E402
from gate_chatbot import study  # noqa: E402
from gate_chatbot.config import get_settings  # noqa: E402
from gate_chatbot.engine import ChatResult, get_engine  # noqa: E402
from gate_chatbot.prompts import (  # noqa: E402
    ALLOWED_SCOPE,
    APP_NAME,
    ASSISTANT_NAME,
    TAGLINE,
)
from gate_chatbot.vectorstore import collection_size  # noqa: E402

logger = logging.getLogger(__name__)


UI_URL = "http://localhost:5173"


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        db.init_db(get_settings())
    except Exception as exc:  # noqa: BLE001 - chat still works without a DB
        logger.warning("Database init failed (continuing without persistence): %s", exc)

    # Make it obvious where the *app* lives — uvicorn only prints the API port.
    banner = (
        "\n"
        "┌───────────────────────────────────────────────────────────────┐\n"
        f"│  {APP_NAME} — backend ready                          \n"
        "│                                                               \n"
        f"│   👉  Open the APP in your browser:   {UI_URL}      \n"
        "│                                                               \n"
        "│   This terminal runs the API only:                            \n"
        "│     • API base : http://localhost:8000                        \n"
        "│     • API docs : http://localhost:8000/docs                   \n"
        "│                                                               \n"
        "│   If the page doesn't load, start the frontend in another     \n"
        "│   terminal:   cd frontend && npm run dev                      \n"
        "│   (or run both at once from the project root:  make dev)      \n"
        "└───────────────────────────────────────────────────────────────┘\n"
    )
    print(banner, flush=True)
    yield


app = FastAPI(
    title=f"{APP_NAME} API",
    version=__version__,
    description="RAG assistant for GATE Computer Science (CS) and "
    "Data Science & AI (DA), powered by GateOverflow.",
    lifespan=lifespan,
)

# CORS origins from env (CORS_ORIGINS, comma-separated). Default "*". In the
# single-container deploy the UI is same-origin, so CORS isn't even needed.
_origins = [o.strip() for o in get_settings().cors_origins.split(",") if o.strip()] or ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single-origin production: if a built frontend exists, the API also serves it.
_DIST = Path(get_settings().frontend_dist)
_SPA = _DIST / "index.html"
_SERVE_SPA = _SPA.exists()


# --------------------------------------------------------------------------- #
# Schemas                                                                     #
# --------------------------------------------------------------------------- #
class Message(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str


class Attachment(BaseModel):
    name: str = Field(..., max_length=256)
    mime: str = Field(default="", max_length=128)
    # A data URL ("data:<mime>;base64,<...>") or raw base64.
    data: str = Field(..., max_length=20_000_000)


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=4000)
    history: list[Message] = Field(default_factory=list)
    conversation_id: str | None = None
    attachments: list[Attachment] = Field(default_factory=list)
    tutor_mode: bool = False
    language: str | None = Field(default=None, max_length=40)


# Max characters of extracted document text injected per file (token control).
_MAX_DOC_CHARS = 6000


def _decode_b64(data: str) -> bytes:
    """Decode a data URL or raw base64 string to bytes."""
    if "," in data and data.strip().startswith("data:"):
        data = data.split(",", 1)[1]
    return base64.b64decode(data)


def _extract_text(name: str, mime: str, raw: bytes) -> str:
    """Best-effort text extraction from an uploaded document."""
    lower = name.lower()
    try:
        if "pdf" in mime or lower.endswith(".pdf"):
            from pypdf import PdfReader

            reader = PdfReader(io.BytesIO(raw))
            pages = [(p.extract_text() or "") for p in reader.pages]
            return "\n".join(pages)
        # Plain text / markdown / csv / code → decode directly.
        return raw.decode("utf-8", errors="ignore")
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not extract text from %s: %s", name, exc)
        return ""


def _process_attachments(attachments: list[Attachment]) -> dict:
    """Split attachments into vision image data-URLs and extracted doc text."""
    images: list[str] = []
    docs: list[dict] = []
    for a in attachments:
        is_image = a.mime.startswith("image/") or a.name.lower().endswith(
            (".png", ".jpg", ".jpeg", ".webp", ".gif")
        )
        if is_image:
            url = a.data if a.data.startswith("data:") else f"data:{a.mime};base64,{a.data}"
            images.append(url)
            continue
        try:
            text = _extract_text(a.name, a.mime, _decode_b64(a.data))
        except Exception:  # noqa: BLE001
            text = ""
        if text.strip():
            docs.append({"name": a.name, "text": text[:_MAX_DOC_CHARS]})
    return {"images": images, "docs": docs}


class FeedbackRequest(BaseModel):
    message_id: str
    rating: str = Field(..., pattern="^(up|down)$")
    reason: str | None = Field(default=None, max_length=64)
    comment: str | None = Field(default=None, max_length=4000)
    corrected_answer: str | None = Field(default=None, max_length=8000)


class RegenerateRequest(BaseModel):
    message_id: str
    guidance: str | None = Field(default=None, max_length=2000)
    tutor_mode: bool = False
    language: str | None = Field(default=None, max_length=40)


def _history_dicts(req: ChatRequest) -> list[dict]:
    return [{"role": m.role, "content": m.content} for m in req.history]


# --------------------------------------------------------------------------- #
# Info endpoints                                                              #
# --------------------------------------------------------------------------- #
@app.get("/")
def root():
    """Serve the built React app if present, else a friendly API landing page."""
    if _SERVE_SPA:
        return FileResponse(str(_SPA))
    return HTMLResponse(f"""<!doctype html><html><head><meta charset="utf-8">
<title>{APP_NAME} API</title>
<style>body{{font-family:system-ui,-apple-system,Segoe UI,sans-serif;background:#0b1220;
color:#e2e8f0;display:grid;place-items:center;height:100vh;margin:0;text-align:center}}
a{{color:#f87171;font-weight:700}}.c{{max-width:520px;padding:32px;border:1px solid #1e293b;
border-radius:18px;background:#0f172a}}.b{{display:inline-block;margin-top:14px;padding:10px 18px;
border-radius:12px;background:linear-gradient(135deg,#dc2626,#e11d48);color:#fff;text-decoration:none;
font-weight:700}}.m{{color:#94a3b8;font-size:14px}}</style></head>
<body><div class="c">
<h1>{APP_NAME} — API</h1>
<p class="m">You're looking at the <b>backend API</b>. The actual app UI runs on a
different port.</p>
<a class="b" href="{UI_URL}">👉 Open the app at {UI_URL}</a>
<p class="m" style="margin-top:18px">API docs: <a href="/docs">/docs</a> ·
health: <a href="/health">/health</a><br>
If the app doesn't load, start the frontend:
<code>cd frontend &amp;&amp; npm run dev</code></p>
</div></body></html>""")


@app.get("/health")
def health() -> dict:
    settings = get_settings()
    return {
        "status": "ok",
        "version": __version__,
        "model": settings.chat_model,
        "indexed_chunks": collection_size(settings),
        "key_configured": bool(settings.openai_api_key),
    }


@app.get("/meta")
def meta() -> dict:
    settings = get_settings()
    return {
        "app_name": APP_NAME,
        "assistant_name": ASSISTANT_NAME,
        "tagline": TAGLINE,
        "scope": ALLOWED_SCOPE,
        "model": settings.chat_model,
        "indexed_chunks": collection_size(settings),
        "key_configured": bool(settings.openai_api_key),
    }


# --------------------------------------------------------------------------- #
# Chat                                                                        #
# --------------------------------------------------------------------------- #
@app.post("/chat")
def chat(req: ChatRequest) -> dict:
    engine = get_engine()
    attachments = _process_attachments(req.attachments)
    result: ChatResult = engine.chat(
        req.question, _history_dicts(req), attachments,
        tutor_mode=req.tutor_mode, language=req.language,
    )
    sources = [s.__dict__ for s in result.sources]

    conv_id, msg_id = _persist_turn(
        req.conversation_id, req.question, result.answer, result.in_scope, sources
    )
    return {
        "conversation_id": conv_id,
        "message_id": msg_id,
        "answer": result.answer,
        "in_scope": result.in_scope,
        "confidence": result.confidence,
        "sources": sources,
        "pyq_links": result.pyq_links,
    }


@app.post("/chat/stream")
def chat_stream(req: ChatRequest) -> StreamingResponse:
    engine = get_engine()
    history = _history_dicts(req)
    settings = get_settings()
    attachments = _process_attachments(req.attachments)

    def event_gen():
        parts: list[str] = []
        final: ChatResult | None = None
        for item in engine.stream(
            req.question, history, attachments=attachments,
            tutor_mode=req.tutor_mode, language=req.language,
        ):
            if isinstance(item, ChatResult):
                final = item
            else:
                parts.append(item)
                yield f"data: {json.dumps({'type': 'token', 'content': item})}\n\n"

        answer = "".join(parts).strip()
        sources = [s.__dict__ for s in final.sources] if final else []
        in_scope = final.in_scope if final else True
        confidence = final.confidence if final else 0.0
        pyq_links = final.pyq_links if final else []
        conv_id, msg_id = _persist_turn(
            req.conversation_id, req.question, answer, in_scope, sources,
            model=settings.chat_model,
        )
        done = {
            "type": "done",
            "conversation_id": conv_id,
            "message_id": msg_id,
            "in_scope": in_scope,
            "confidence": confidence,
            "sources": sources,
            "pyq_links": pyq_links,
        }
        yield f"data: {json.dumps(done)}\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream")


@app.post("/regenerate/stream")
def regenerate_stream(req: RegenerateRequest) -> StreamingResponse:
    """Regenerate the answer for an existing assistant message, steered by any
    feedback it received — the online half of the RLHF loop."""
    engine = get_engine()
    settings = get_settings()

    question = ""
    history: list[dict] = []
    old_content = ""
    feedback_hint = req.guidance or None
    conv_id: str | None = None
    disliked = False

    try:
        with db.session() as s:
            ctx = db.preceding_user_question(s, req.message_id)
            old = s.get(db.Message, req.message_id)
            if old:
                old_content = old.content
                conv_id = old.conversation_id
                fb = next(iter(old.feedback), None)
                if fb and fb.rating == "down":
                    disliked = True
                    bits = []
                    if fb.reason:
                        bits.append(f"reason: {fb.reason}")
                    if fb.comment:
                        bits.append(f"the user said: \"{fb.comment}\"")
                    if bits:
                        prefix = "The user disliked the previous answer (" + "; ".join(bits) + ")."
                        feedback_hint = (prefix + " " + (req.guidance or "")).strip()
            if ctx:
                question, history = ctx
    except Exception as exc:  # noqa: BLE001
        logger.warning("Regenerate context lookup failed: %s", exc)

    if not question:
        # Fall back: nothing to regenerate from.
        def err():
            yield f"data: {json.dumps({'type': 'token', 'content': '⚠️ Could not find the original question to regenerate.'})}\n\n"
            yield f"data: {json.dumps({'type': 'done', 'sources': [], 'in_scope': True})}\n\n"
        return StreamingResponse(err(), media_type="text/event-stream")

    def event_gen():
        parts: list[str] = []
        final: ChatResult | None = None
        for item in engine.stream(
            question, history, feedback_hint=feedback_hint,
            tutor_mode=req.tutor_mode, language=req.language,
        ):
            if isinstance(item, ChatResult):
                final = item
            else:
                parts.append(item)
                yield f"data: {json.dumps({'type': 'token', 'content': item})}\n\n"

        answer = "".join(parts).strip()
        sources = [s.__dict__ for s in final.sources] if final else []
        in_scope = final.in_scope if final else True

        new_msg_id = None
        try:
            with db.session() as s:
                if conv_id:
                    m = db.add_message(
                        s,
                        conversation_id=conv_id,
                        role="assistant",
                        content=answer,
                        model=settings.chat_model,
                        in_scope=in_scope,
                        sources=sources,
                        parent_id=req.message_id,
                    )
                    new_msg_id = m.id
                    # RLHF: record the preference (old rejected, new chosen).
                    if disliked and old_content and answer:
                        db.add_preference_pair(
                            s,
                            prompt=question,
                            chosen=answer,
                            rejected=old_content,
                            kind="regeneration",
                            message_id=new_msg_id,
                        )
                    s.commit()
        except Exception as exc:  # noqa: BLE001
            logger.warning("Persisting regeneration failed: %s", exc)

        done = {
            "type": "done",
            "conversation_id": conv_id,
            "message_id": new_msg_id,
            "in_scope": in_scope,
            "sources": sources,
            "pyq_links": [pl.__dict__ if hasattr(pl, "__dict__") else pl
                          for pl in (final.pyq_links if final else [])],
        }
        yield f"data: {json.dumps(done)}\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream")


# --------------------------------------------------------------------------- #
# Feedback + RLHF dataset                                                     #
# --------------------------------------------------------------------------- #
@app.post("/feedback")
def feedback(req: FeedbackRequest) -> dict:
    try:
        with db.session() as s:
            fb = db.record_feedback(
                s,
                message_id=req.message_id,
                rating=req.rating,
                reason=req.reason,
                comment=req.comment,
            )
            if fb is None:
                return {"ok": False, "error": "message not found"}

            # A human correction to a disliked answer is gold-standard RLHF data.
            if req.rating == "down" and req.corrected_answer:
                ctx = db.preceding_user_question(s, req.message_id)
                old = s.get(db.Message, req.message_id)
                if ctx and old:
                    question, _ = ctx
                    db.add_preference_pair(
                        s,
                        prompt=question,
                        chosen=req.corrected_answer,
                        rejected=old.content,
                        kind="human_correction",
                        message_id=req.message_id,
                    )
            s.commit()
        return {"ok": True}
    except Exception as exc:  # noqa: BLE001
        logger.warning("Feedback persist failed: %s", exc)
        return {"ok": False, "error": "persistence unavailable"}


@app.get("/export/preferences")
def export_preferences() -> PlainTextResponse:
    """Download the RLHF preference dataset as JSONL (one record per line),
    ready for offline reward-model training or DPO fine-tuning."""
    try:
        with db.session() as s:
            rows = db.export_preferences(s)
    except Exception as exc:  # noqa: BLE001
        return PlainTextResponse(f"export failed: {exc}", status_code=500)
    body = "\n".join(json.dumps(r, ensure_ascii=False) for r in rows)
    return PlainTextResponse(
        body,
        media_type="application/x-ndjson",
        headers={"Content-Disposition": "attachment; filename=preferences.jsonl"},
    )


@app.get("/admin/stats")
def admin_stats() -> dict:
    try:
        with db.session() as s:
            return db.stats(s)
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


# --------------------------------------------------------------------------- #
# History & bookmarks                                                         #
# --------------------------------------------------------------------------- #
class BookmarkRequest(BaseModel):
    message_id: str
    note: str | None = Field(default=None, max_length=500)


@app.get("/conversations")
def conversations(limit: int = 50) -> dict:
    try:
        with db.session() as s:
            return {"ok": True, "conversations": db.list_conversations(s, limit=limit)}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc), "conversations": []}


@app.get("/conversations/{conversation_id}")
def conversation(conversation_id: str) -> dict:
    try:
        with db.session() as s:
            msgs = db.conversation_messages(s, conversation_id)
        if msgs is None:
            return {"ok": False, "error": "not found"}
        return {"ok": True, "conversation_id": conversation_id, "messages": msgs}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}


@app.post("/bookmark")
def bookmark(req: BookmarkRequest) -> dict:
    try:
        with db.session() as s:
            now = db.toggle_bookmark(s, req.message_id, req.note)
            s.commit()
        return {"ok": True, "bookmarked": now}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}


@app.get("/bookmarks")
def bookmarks(limit: int = 100) -> dict:
    try:
        with db.session() as s:
            return {"ok": True, "bookmarks": db.list_bookmarks(s, limit=limit)}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc), "bookmarks": []}


# --------------------------------------------------------------------------- #
# Study suite: quizzes / mock tests, flashcards, spaced repetition,           #
# study planner, daily question, analytics                                    #
# --------------------------------------------------------------------------- #
class QuizGenerateRequest(BaseModel):
    exam: str = Field(default="CS", pattern="^(CS|DA)$")
    subject: str = Field(default="mixed topics", max_length=80)
    num: int = Field(default=5, ge=1, le=20)
    difficulty: str = Field(default="medium", pattern="^(easy|medium|hard)$")
    kind: str = Field(default="quiz", pattern="^(quiz|mock)$")


class QuizSubmitRequest(BaseModel):
    quiz_id: str
    answers: dict[str, object] = Field(default_factory=dict)
    duration_sec: int = Field(default=0, ge=0)


class FlashcardRequest(BaseModel):
    exam: str = Field(default="CS", pattern="^(CS|DA)$")
    topic: str = Field(..., min_length=2, max_length=80)
    num: int = Field(default=8, ge=1, le=20)


class ReviewGradeRequest(BaseModel):
    item_id: str
    quality: int = Field(..., ge=0, le=5)


class PlanRequest(BaseModel):
    exam: str = Field(default="CS", pattern="^(CS|DA)$")
    exam_date: str | None = Field(default=None, max_length=20)
    days: int = Field(default=30, ge=1, le=180)
    hours: float = Field(default=4.0, ge=0.5, le=16)


def _log_activity() -> None:
    try:
        with db.session() as s:
            db.log_activity(s)
            s.commit()
    except Exception as exc:  # noqa: BLE001
        logger.warning("activity log failed: %s", exc)


@app.post("/quiz/generate")
def quiz_generate(req: QuizGenerateRequest) -> dict:
    engine = get_engine()
    n = req.num if req.kind == "quiz" else max(req.num, 10)
    questions = study.generate_quiz(
        engine, exam=req.exam, subject=req.subject, n=n, difficulty=req.difficulty
    )
    if not questions:
        return {"ok": False, "error": "Could not generate questions. Try again."}
    try:
        with db.session() as s:
            quiz_id = db.save_generated_quiz(
                s, exam=req.exam, subject=req.subject,
                difficulty=req.difficulty, questions=questions,
            )
            s.commit()
    except Exception as exc:  # noqa: BLE001
        logger.warning("save quiz failed: %s", exc)
        quiz_id = ""
    # Send questions WITHOUT answers/explanations (scored server-side).
    public = [
        {"id": q["id"], "type": q["type"], "question": q["question"],
         "options": q["options"], "marks": q["marks"], "subject": q["subject"]}
        for q in questions
    ]
    return {"ok": True, "quiz_id": quiz_id, "kind": req.kind, "exam": req.exam,
            "subject": req.subject, "questions": public}


@app.get("/quiz/adaptive")
def quiz_adaptive(exam: str = "CS", num: int = 5) -> dict:
    """Generate a quiz targeting the student's weakest subjects (from analytics)."""
    exam = exam if exam in ("CS", "DA") else "CS"
    num = max(3, min(15, num))
    try:
        with db.session() as s:
            data = db.analytics(s)
    except Exception:  # noqa: BLE001
        data = {}
    weak = (data.get("weak_areas") or [])[:2]
    subject = " and ".join(weak) if weak else "your most exam-relevant topics"
    questions = study.generate_quiz(
        get_engine(), exam=exam, subject=subject, n=num, difficulty="medium"
    )
    if not questions:
        return {"ok": False, "error": "Could not generate questions. Try again."}
    try:
        with db.session() as s:
            quiz_id = db.save_generated_quiz(
                s, exam=exam, subject=subject, difficulty="medium", questions=questions
            )
            s.commit()
    except Exception as exc:  # noqa: BLE001
        logger.warning("save adaptive quiz failed: %s", exc)
        quiz_id = ""
    public = [
        {"id": q["id"], "type": q["type"], "question": q["question"],
         "options": q["options"], "marks": q["marks"], "subject": q["subject"]}
        for q in questions
    ]
    return {"ok": True, "quiz_id": quiz_id, "kind": "quiz", "exam": exam,
            "subject": subject, "adaptive": True,
            "targeted": weak, "questions": public}


@app.post("/quiz/submit")
def quiz_submit(req: QuizSubmitRequest) -> dict:
    with db.session() as s:
        questions = db.load_generated_quiz(s, req.quiz_id)
        if questions is None:
            return {"ok": False, "error": "Quiz not found or expired."}
        gq = s.get(db.GeneratedQuiz, req.quiz_id)
        exam = gq.exam if gq else "CS"
        subject = gq.subject if gq else "mixed"

        scored = study.score_quiz(questions, req.answers)
        attempt = db.save_attempt(
            s, kind="quiz", exam=exam, subject=subject,
            scored=scored, duration_sec=req.duration_sec,
        )
        # Auto-create spaced-repetition cards for wrong answers.
        created = 0
        for r in scored["results"]:
            if not r["is_correct"] and r.get("explanation"):
                db.add_review_item(
                    s, front=r["question"],
                    back=r["explanation"], subject=r["subject"], source="quiz",
                )
                created += 1
        db.log_activity(s)
        s.commit()
        attempt_id = attempt.id

    scored["ok"] = True
    scored["attempt_id"] = attempt_id
    scored["weak_areas"] = study.weak_areas(scored["subject_breakdown"])
    scored["review_cards_created"] = created
    return scored


@app.post("/flashcards/generate")
def flashcards_generate(req: FlashcardRequest) -> dict:
    engine = get_engine()
    cards = study.generate_flashcards(engine, exam=req.exam, topic=req.topic, n=req.num)
    if not cards:
        return {"ok": False, "error": "Could not generate flashcards. Try again."}
    saved = []
    try:
        with db.session() as s:
            for c in cards:
                item = db.add_review_item(
                    s, front=c["front"], back=c["back"],
                    subject=c.get("subject", req.topic), source="flashcard",
                )
                saved.append({"id": item.id, "front": c["front"], "back": c["back"],
                              "subject": c.get("subject", req.topic)})
            db.log_activity(s)
            s.commit()
    except Exception as exc:  # noqa: BLE001
        logger.warning("save flashcards failed: %s", exc)
        saved = [{"id": None, **c} for c in cards]
    return {"ok": True, "cards": saved}


@app.get("/review/due")
def review_due(limit: int = 20) -> dict:
    try:
        with db.session() as s:
            items = db.due_review_items(s, limit=limit)
            return {"ok": True, "items": [
                {"id": i.id, "front": i.front, "back": i.back, "subject": i.subject,
                 "repetitions": i.repetitions}
                for i in items
            ]}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc), "items": []}


@app.post("/review/grade")
def review_grade(req: ReviewGradeRequest) -> dict:
    try:
        with db.session() as s:
            item = s.get(db.ReviewItem, req.item_id)
            if not item:
                return {"ok": False, "error": "Item not found."}
            upd = study.sm2(req.quality, item.repetitions, item.ease, item.interval)
            db.apply_sm2_update(
                s, item, ease=upd["ease"], interval=upd["interval"],
                repetitions=upd["repetitions"], due_in_days=upd["due_in_days"],
            )
            db.log_activity(s)
            s.commit()
            return {"ok": True, **upd}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}


@app.post("/plan/generate")
def plan_generate(req: PlanRequest) -> dict:
    engine = get_engine()
    days = req.days
    if req.exam_date:
        try:
            target = date.fromisoformat(req.exam_date)
            days = max(1, min(180, (target - date.today()).days))
        except ValueError:
            pass
    plan = study.generate_plan(engine, exam=req.exam, days=days, hours=req.hours)
    if not plan.get("days"):
        return {"ok": False, "error": "Could not generate a plan. Try again."}
    try:
        with db.session() as s:
            db.save_plan(s, exam=req.exam, exam_date=req.exam_date, content=plan)
            db.log_activity(s)
            s.commit()
    except Exception as exc:  # noqa: BLE001
        logger.warning("save plan failed: %s", exc)
    return {"ok": True, "exam": req.exam, "exam_date": req.exam_date, **plan}


@app.get("/plan")
def plan_latest() -> dict:
    try:
        with db.session() as s:
            plan = db.latest_plan(s)
            adherence = None
            if plan and plan.get("created_at"):
                created_day = plan["created_at"][:10]
                days_since = max(0, (date.today() - date.fromisoformat(created_day)).days) + 1
                active = db.activity_since(s, created_day)
                total = len(plan.get("days", []) or []) or days_since
                expected = min(days_since, total)
                on_track = active >= max(1, expected - 1)
                if on_track:
                    msg = f"On track 🎯 — active {active} of {expected} planned day(s)."
                else:
                    behind = expected - active
                    msg = (f"You're ~{behind} day(s) behind — active {active} of "
                           f"{expected}. Do a focused session today to catch up.")
                adherence = {
                    "days_since": days_since, "active_days": active,
                    "expected": expected, "total_days": total,
                    "on_track": on_track, "message": msg,
                }
        return {"ok": bool(plan), "plan": plan, "adherence": adherence}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}


@app.get("/plan/calendar.ics")
def plan_ics() -> PlainTextResponse:
    """Export the latest study plan as an .ics calendar (offline, no email needed)."""
    with db.session() as s:
        plan = db.latest_plan(s)
    if not plan:
        return PlainTextResponse("no plan", status_code=404)
    start = date.today()
    try:
        if plan.get("exam_date"):
            start = date.fromisoformat(plan["exam_date"]) - timedelta(days=len(plan["days"]))
            if start < date.today():
                start = date.today()
    except ValueError:
        pass
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//GateOverflow Chatbot//EN"]
    for d in plan.get("days", []):
        day = start + timedelta(days=int(d.get("day", 1)) - 1)
        ymd = day.strftime("%Y%m%d")
        summary = f"GATE {plan.get('exam','')} — {d.get('focus','study')}"
        desc = " \\n ".join(d.get("tasks", []))
        lines += ["BEGIN:VEVENT", f"DTSTART;VALUE=DATE:{ymd}", f"DTEND;VALUE=DATE:{ymd}",
                  f"SUMMARY:{summary}", f"DESCRIPTION:{desc}", "END:VEVENT"]
    lines.append("END:VCALENDAR")
    return PlainTextResponse(
        "\r\n".join(lines), media_type="text/calendar",
        headers={"Content-Disposition": "attachment; filename=gate-study-plan.ics"},
    )


@app.get("/daily")
def daily() -> dict:
    """A deterministic 'question of the day' prompt + streak info."""
    engine = get_engine()
    topics = [
        "dynamic programming", "TCP congestion control", "Bayes' theorem",
        "normalization (BCNF)", "process scheduling", "eigenvalues & PCA",
        "pumping lemma", "pipelining hazards", "gradient descent",
        "B+ tree indexing", "deadlock avoidance", "logistic regression",
        "minimum spanning trees", "virtual memory & TLB",
    ]
    topic = topics[date.today().toordinal() % len(topics)]
    prompt = (
        f"Create ONE crisp GATE-style question on '{topic}'. "
        'Return ONLY JSON: {"question":"...","hint":"...","topic":"' + topic + '"}'
    )
    data = study.extract_json(engine.generate_json(prompt)) or {}
    streak = 0
    try:
        with db.session() as s:
            streak = db.current_streak(s)
    except Exception:  # noqa: BLE001
        pass
    return {
        "ok": True,
        "date": date.today().isoformat(),
        "topic": data.get("topic", topic),
        "question": data.get("question", f"Explain a key idea in {topic}."),
        "hint": data.get("hint", ""),
        "streak": streak,
    }


class CheatSheetRequest(BaseModel):
    history: list[Message] = Field(default_factory=list)


@app.post("/cheatsheet")
def cheatsheet(req: CheatSheetRequest) -> dict:
    if not req.history:
        return {"ok": False, "error": "Nothing to summarise yet — chat first."}
    transcript = "\n\n".join(
        f"{'Q' if m.role == 'user' else 'A'}: {m.content}" for m in req.history
    )
    md = study.generate_cheatsheet(get_engine(), transcript=transcript)
    if not md:
        return {"ok": False, "error": "Could not build a cheat-sheet. Try again."}
    return {"ok": True, "markdown": md}


@app.get("/analytics")
def analytics() -> dict:
    try:
        with db.session() as s:
            data = db.analytics(s)
        data["readiness"] = study.readiness_score(
            data["avg_accuracy"], data["attempts"], data["streak"]
        )
        data["rank_band"] = (
            study.rank_band(data["avg_percentile"]) if data["attempts"] else ""
        )
        data["ok"] = True
        return data
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}


@app.get("/coach")
def coach(exam: str = "CS") -> dict:
    """AI Coach: personalized, rank-focused feedback from the student's own
    quiz/mock performance, weak areas, streak and study plan."""
    try:
        with db.session() as s:
            data = db.analytics(s)
            plan = db.latest_plan(s)
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}

    if not data.get("attempts"):
        return {
            "ok": False,
            "reason": "no_data",
            "message": "Take a quiz or mock test first — then your AI coach can "
            "analyse your performance and tell you exactly how to improve.",
        }

    data["readiness"] = study.readiness_score(
        data["avg_accuracy"], data["attempts"], data["streak"]
    )
    exam = exam if exam in ("CS", "DA") else "CS"
    report = study.generate_coach(get_engine(), exam=exam, analytics=data, plan=plan)
    if not report.get("headline") and not report.get("focus_areas"):
        return {"ok": False, "error": "Could not generate coaching. Try again."}
    return {"ok": True, "readiness": data["readiness"], **report}


# --------------------------------------------------------------------------- #
# Persistence helper                                                          #
# --------------------------------------------------------------------------- #
def _persist_turn(
    conversation_id: str | None,
    question: str,
    answer: str,
    in_scope: bool,
    sources: list[dict],
    model: str | None = None,
) -> tuple[str | None, str | None]:
    """Persist a user→assistant turn. Returns (conversation_id, assistant_message_id).

    Best-effort: if the DB is unavailable the chat still succeeds (returns Nones).
    """
    try:
        with db.session() as s:
            conv = db.get_or_create_conversation(s, conversation_id, title=question)
            db.add_message(s, conversation_id=conv.id, role="user", content=question)
            assistant = db.add_message(
                s,
                conversation_id=conv.id,
                role="assistant",
                content=answer,
                model=model,
                in_scope=in_scope,
                sources=sources,
            )
            s.commit()
            return conv.id, assistant.id
    except Exception as exc:  # noqa: BLE001
        logger.warning("Persisting chat turn failed: %s", exc)
        return conversation_id, None


# --------------------------------------------------------------------------- #
# Static frontend (single-origin production). Mounted LAST so all API routes  #
# above take precedence; serves /assets, /favicon.svg, etc.                   #
# --------------------------------------------------------------------------- #
if _SERVE_SPA:
    app.mount("/", StaticFiles(directory=str(_DIST), html=True), name="spa")
    logger.info("Serving built frontend from %s", _DIST)
