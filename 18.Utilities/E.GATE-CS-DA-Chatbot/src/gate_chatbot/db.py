"""Persistence layer: conversations, messages, feedback and the RLHF
preference dataset.

Uses SQLAlchemy 2.0 with SQLite by default (``storage/app.db``) and switches to
any URL via ``DATABASE_URL`` (e.g. Postgres in production). All writes are
best-effort from the API's point of view — a DB hiccup must never break a chat.
"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
    create_engine,
    func,
    select,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    sessionmaker,
)

from .config import Settings, get_settings

logger = logging.getLogger(__name__)


def _uuid() -> str:
    return uuid.uuid4().hex


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    title: Mapped[Optional[str]] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    conversation_id: Mapped[str] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"), index=True
    )
    role: Mapped[str] = mapped_column(String(16))  # 'user' | 'assistant'
    content: Mapped[str] = mapped_column(Text)
    model: Mapped[Optional[str]] = mapped_column(String(64))
    in_scope: Mapped[Optional[bool]] = mapped_column(Boolean)
    sources_json: Mapped[Optional[str]] = mapped_column(Text)
    # For regenerated answers: points at the assistant message this one replaces.
    parent_id: Mapped[Optional[str]] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    conversation: Mapped[Conversation] = relationship(back_populates="messages")
    feedback: Mapped[list["Feedback"]] = relationship(
        back_populates="message", cascade="all, delete-orphan"
    )


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    message_id: Mapped[str] = mapped_column(
        ForeignKey("messages.id", ondelete="CASCADE"), index=True
    )
    rating: Mapped[str] = mapped_column(String(8))  # 'up' | 'down'
    reason: Mapped[Optional[str]] = mapped_column(String(64))
    comment: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    message: Mapped[Message] = relationship(back_populates="feedback")


class PreferencePair(Base):
    """A (prompt, chosen, rejected) triple — the unit of RLHF/DPO training data.

    Populated when a user supplies a correction to a disliked answer, or when a
    regenerated answer replaces one that was thumbed-down. Export it as JSONL to
    train a reward model / run DPO offline, then redeploy an improved model.
    """

    __tablename__ = "preference_pairs"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    prompt: Mapped[str] = mapped_column(Text)
    chosen: Mapped[str] = mapped_column(Text)
    rejected: Mapped[str] = mapped_column(Text)
    kind: Mapped[str] = mapped_column(String(32))  # 'human_correction'|'regeneration'
    message_id: Mapped[Optional[str]] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


# --------------------------------------------------------------------------- #
# Engine / session management                                                 #
# --------------------------------------------------------------------------- #
_engine = None
_SessionLocal: Optional[sessionmaker[Session]] = None


def init_db(settings: Settings | None = None) -> None:
    """Create the engine and tables (idempotent)."""
    global _engine, _SessionLocal
    if _engine is not None:
        return
    settings = settings or get_settings()
    url = settings.database_url
    if url.startswith("sqlite:///"):
        # Ensure the parent dir exists for file-based SQLite.
        db_path = Path(url.replace("sqlite:///", "", 1))
        db_path.parent.mkdir(parents=True, exist_ok=True)
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    _engine = create_engine(url, connect_args=connect_args, future=True)
    _SessionLocal = sessionmaker(bind=_engine, expire_on_commit=False, future=True)
    Base.metadata.create_all(_engine)
    logger.info("Database ready at %s", url)


def session() -> Session:
    if _SessionLocal is None:
        init_db()
    assert _SessionLocal is not None
    return _SessionLocal()


# --------------------------------------------------------------------------- #
# Repository helpers (all defensive — return None on failure, never raise up)  #
# --------------------------------------------------------------------------- #
def get_or_create_conversation(db: Session, conversation_id: str | None, title: str) -> Conversation:
    if conversation_id:
        conv = db.get(Conversation, conversation_id)
        if conv:
            return conv
    conv = Conversation(id=conversation_id or _uuid(), title=title[:200])
    db.add(conv)
    db.flush()
    return conv


def add_message(
    db: Session,
    *,
    conversation_id: str,
    role: str,
    content: str,
    model: str | None = None,
    in_scope: bool | None = None,
    sources: list[dict] | None = None,
    parent_id: str | None = None,
) -> Message:
    msg = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        model=model,
        in_scope=in_scope,
        sources_json=json.dumps(sources) if sources is not None else None,
        parent_id=parent_id,
    )
    db.add(msg)
    db.flush()
    return msg


def record_feedback(
    db: Session,
    *,
    message_id: str,
    rating: str,
    reason: str | None = None,
    comment: str | None = None,
) -> Feedback | None:
    msg = db.get(Message, message_id)
    if not msg:
        return None
    # One feedback row per message: update if it already exists.
    existing = db.scalars(
        select(Feedback).where(Feedback.message_id == message_id)
    ).first()
    if existing:
        existing.rating = rating
        existing.reason = reason
        existing.comment = comment
        db.flush()
        return existing
    fb = Feedback(message_id=message_id, rating=rating, reason=reason, comment=comment)
    db.add(fb)
    db.flush()
    return fb


def message_was_disliked(db: Session, message_id: str) -> bool:
    fb = db.scalars(
        select(Feedback).where(Feedback.message_id == message_id)
    ).first()
    return bool(fb and fb.rating == "down")


def preceding_user_question(db: Session, assistant_message_id: str) -> tuple[str, list[dict]] | None:
    """Return (question, history-before-it) for an assistant message, so we can
    regenerate the answer with the same context."""
    msg = db.get(Message, assistant_message_id)
    if not msg:
        return None
    msgs = list(
        db.scalars(
            select(Message)
            .where(Message.conversation_id == msg.conversation_id)
            .order_by(Message.created_at)
        )
    )
    # Find the assistant message, then the most recent user turn before it.
    idx = next((i for i, m in enumerate(msgs) if m.id == assistant_message_id), None)
    if idx is None:
        return None
    question = None
    for j in range(idx - 1, -1, -1):
        if msgs[j].role == "user":
            question = msgs[j].content
            history = [
                {"role": m.role, "content": m.content} for m in msgs[:j]
            ]
            return question, history
    return None


def add_preference_pair(
    db: Session,
    *,
    prompt: str,
    chosen: str,
    rejected: str,
    kind: str,
    message_id: str | None = None,
) -> PreferencePair:
    pair = PreferencePair(
        prompt=prompt,
        chosen=chosen,
        rejected=rejected,
        kind=kind,
        message_id=message_id,
    )
    db.add(pair)
    db.flush()
    return pair


def export_preferences(db: Session) -> list[dict]:
    rows = db.scalars(select(PreferencePair).order_by(PreferencePair.created_at)).all()
    return [
        {
            "prompt": r.prompt,
            "chosen": r.chosen,
            "rejected": r.rejected,
            "kind": r.kind,
            "created_at": r.created_at.isoformat(),
        }
        for r in rows
    ]


def stats(db: Session) -> dict:
    def _count(model) -> int:
        return db.scalar(select(func.count()).select_from(model)) or 0

    ups = db.scalar(
        select(func.count()).select_from(Feedback).where(Feedback.rating == "up")
    ) or 0
    downs = db.scalar(
        select(func.count()).select_from(Feedback).where(Feedback.rating == "down")
    ) or 0
    return {
        "conversations": _count(Conversation),
        "messages": _count(Message),
        "likes": ups,
        "dislikes": downs,
        "preference_pairs": _count(PreferencePair),
    }
