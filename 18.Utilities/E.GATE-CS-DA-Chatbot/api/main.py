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
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from fastapi.responses import PlainTextResponse, StreamingResponse  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

from gate_chatbot import __version__  # noqa: E402
from gate_chatbot import db  # noqa: E402
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


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        db.init_db(get_settings())
    except Exception as exc:  # noqa: BLE001 - chat still works without a DB
        logger.warning("Database init failed (continuing without persistence): %s", exc)
    yield


app = FastAPI(
    title=f"{APP_NAME} API",
    version=__version__,
    description="RAG assistant for GATE Computer Science (CS) and "
    "Data Science & AI (DA), powered by GateOverflow.",
    lifespan=lifespan,
)

# Lock this down to your front-end origin(s) in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


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


def _history_dicts(req: ChatRequest) -> list[dict]:
    return [{"role": m.role, "content": m.content} for m in req.history]


# --------------------------------------------------------------------------- #
# Info endpoints                                                              #
# --------------------------------------------------------------------------- #
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
    result: ChatResult = engine.chat(req.question, _history_dicts(req), attachments)
    sources = [s.__dict__ for s in result.sources]

    conv_id, msg_id = _persist_turn(
        req.conversation_id, req.question, result.answer, result.in_scope, sources
    )
    return {
        "conversation_id": conv_id,
        "message_id": msg_id,
        "answer": result.answer,
        "in_scope": result.in_scope,
        "sources": sources,
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
        for item in engine.stream(req.question, history, attachments=attachments):
            if isinstance(item, ChatResult):
                final = item
            else:
                parts.append(item)
                yield f"data: {json.dumps({'type': 'token', 'content': item})}\n\n"

        answer = "".join(parts).strip()
        sources = [s.__dict__ for s in final.sources] if final else []
        in_scope = final.in_scope if final else True
        conv_id, msg_id = _persist_turn(
            req.conversation_id, req.question, answer, in_scope, sources,
            model=settings.chat_model,
        )
        done = {
            "type": "done",
            "conversation_id": conv_id,
            "message_id": msg_id,
            "in_scope": in_scope,
            "sources": sources,
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
        for item in engine.stream(question, history, feedback_hint=feedback_hint):
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
