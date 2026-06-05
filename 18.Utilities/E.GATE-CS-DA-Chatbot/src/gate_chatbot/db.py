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
from datetime import date, datetime, timedelta, timezone
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


class Bookmark(Base):
    """A saved assistant answer the user wants to revisit."""

    __tablename__ = "bookmarks"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    message_id: Mapped[str] = mapped_column(
        ForeignKey("messages.id", ondelete="CASCADE"), unique=True, index=True
    )
    note: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class GeneratedQuiz(Base):
    """A generated quiz held server-side (with answers) until it is submitted."""

    __tablename__ = "generated_quizzes"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    exam: Mapped[str] = mapped_column(String(8))
    subject: Mapped[str] = mapped_column(String(80))
    difficulty: Mapped[str] = mapped_column(String(16))
    payload_json: Mapped[str] = mapped_column(Text)  # full questions incl answers
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    kind: Mapped[str] = mapped_column(String(16), default="quiz")  # quiz | mock
    exam: Mapped[str] = mapped_column(String(8), default="CS")
    subject: Mapped[str] = mapped_column(String(80), default="mixed")
    score: Mapped[float] = mapped_column(default=0.0)
    max_score: Mapped[float] = mapped_column(default=0.0)
    correct: Mapped[int] = mapped_column(default=0)
    total: Mapped[int] = mapped_column(default=0)
    accuracy: Mapped[float] = mapped_column(default=0.0)
    percentile: Mapped[float] = mapped_column(default=0.0)
    duration_sec: Mapped[int] = mapped_column(default=0)
    subject_breakdown_json: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class ReviewItem(Base):
    """A spaced-repetition card (SM-2 scheduled)."""

    __tablename__ = "review_items"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    front: Mapped[str] = mapped_column(Text)
    back: Mapped[str] = mapped_column(Text)
    subject: Mapped[str] = mapped_column(String(80), default="general")
    source: Mapped[str] = mapped_column(String(24), default="manual")  # manual|quiz|flashcard
    ease: Mapped[float] = mapped_column(default=2.5)
    interval: Mapped[int] = mapped_column(default=0)
    repetitions: Mapped[int] = mapped_column(default=0)
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    last_reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class StudyPlan(Base):
    __tablename__ = "study_plans"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    exam: Mapped[str] = mapped_column(String(8), default="CS")
    exam_date: Mapped[Optional[str]] = mapped_column(String(20))
    content_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class ActivityLog(Base):
    """One row per day the user was active — powers streaks."""

    __tablename__ = "activity_log"

    day: Mapped[str] = mapped_column(String(10), primary_key=True)  # YYYY-MM-DD
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
        "quiz_attempts": _count(QuizAttempt),
        "review_items": _count(ReviewItem),
    }


# --------------------------------------------------------------------------- #
# History & bookmarks                                                          #
# --------------------------------------------------------------------------- #
def list_conversations(db, limit: int = 50) -> list[dict]:
    convs = db.scalars(
        select(Conversation).order_by(Conversation.updated_at.desc()).limit(limit)
    ).all()
    out = []
    for c in convs:
        n = db.scalar(
            select(func.count()).select_from(Message).where(Message.conversation_id == c.id)
        ) or 0
        if n == 0:
            continue
        out.append({
            "id": c.id, "title": c.title or "Untitled",
            "messages": int(n), "updated_at": c.updated_at.isoformat(),
        })
    return out


def conversation_messages(db, conversation_id: str) -> list[dict] | None:
    conv = db.get(Conversation, conversation_id)
    if not conv:
        return None
    msgs = db.scalars(
        select(Message).where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    ).all()
    bookmarked = {
        b.message_id for b in db.scalars(select(Bookmark)).all()
    }
    out = []
    for m in msgs:
        try:
            sources = json.loads(m.sources_json) if m.sources_json else []
        except Exception:  # noqa: BLE001
            sources = []
        out.append({
            "id": m.id, "role": m.role, "content": m.content,
            "sources": sources, "in_scope": m.in_scope,
            "bookmarked": m.id in bookmarked,
        })
    return out


def toggle_bookmark(db, message_id: str, note: str | None = None) -> bool:
    """Add or remove a bookmark. Returns True if now bookmarked."""
    existing = db.scalars(
        select(Bookmark).where(Bookmark.message_id == message_id)
    ).first()
    if existing:
        db.delete(existing)
        db.flush()
        return False
    if not db.get(Message, message_id):
        return False
    db.add(Bookmark(message_id=message_id, note=note))
    db.flush()
    return True


def list_bookmarks(db, limit: int = 100) -> list[dict]:
    rows = db.scalars(
        select(Bookmark).order_by(Bookmark.created_at.desc()).limit(limit)
    ).all()
    out = []
    for b in rows:
        m = db.get(Message, b.message_id)
        if not m:
            continue
        out.append({
            "message_id": b.message_id,
            "conversation_id": m.conversation_id,
            "content": m.content,
            "note": b.note,
            "created_at": b.created_at.isoformat(),
        })
    return out


# --------------------------------------------------------------------------- #
# Study-suite repository                                                       #
# --------------------------------------------------------------------------- #
def save_generated_quiz(db, *, exam, subject, difficulty, questions: list[dict]) -> str:
    q = GeneratedQuiz(
        exam=exam, subject=subject, difficulty=difficulty,
        payload_json=json.dumps(questions),
    )
    db.add(q)
    db.flush()
    return q.id


def load_generated_quiz(db, quiz_id: str) -> list[dict] | None:
    q = db.get(GeneratedQuiz, quiz_id)
    if not q:
        return None
    try:
        return json.loads(q.payload_json)
    except Exception:  # noqa: BLE001
        return None


def save_attempt(db, *, kind, exam, subject, scored: dict, duration_sec: int) -> QuizAttempt:
    a = QuizAttempt(
        kind=kind, exam=exam, subject=subject,
        score=scored["score"], max_score=scored["max_score"],
        correct=scored["correct"], total=scored["total"],
        accuracy=scored["accuracy"], percentile=scored["percentile"],
        duration_sec=duration_sec,
        subject_breakdown_json=json.dumps(scored.get("subject_breakdown", {})),
    )
    db.add(a)
    db.flush()
    return a


def add_review_item(db, *, front, back, subject="general", source="manual",
                    due_at: datetime | None = None) -> ReviewItem:
    item = ReviewItem(front=front, back=back, subject=subject, source=source,
                      due_at=due_at or _now())
    db.add(item)
    db.flush()
    return item


def due_review_items(db, limit: int = 20) -> list[ReviewItem]:
    return list(db.scalars(
        select(ReviewItem).where(ReviewItem.due_at <= _now())
        .order_by(ReviewItem.due_at).limit(limit)
    ))


def apply_sm2_update(db, item: ReviewItem, *, ease, interval, repetitions, due_in_days) -> None:
    item.ease = ease
    item.interval = interval
    item.repetitions = repetitions
    item.due_at = _now() + timedelta(days=int(due_in_days))
    item.last_reviewed_at = _now()
    db.flush()


def save_plan(db, *, exam, exam_date, content: dict) -> StudyPlan:
    p = StudyPlan(exam=exam, exam_date=exam_date, content_json=json.dumps(content))
    db.add(p)
    db.flush()
    return p


def latest_plan(db) -> dict | None:
    p = db.scalars(select(StudyPlan).order_by(StudyPlan.created_at.desc()).limit(1)).first()
    if not p:
        return None
    try:
        content = json.loads(p.content_json)
    except Exception:  # noqa: BLE001
        content = {}
    return {"exam": p.exam, "exam_date": p.exam_date, "created_at": p.created_at.isoformat(), **content}


def log_activity(db, day: str | None = None) -> None:
    day = day or date.today().isoformat()
    if not db.get(ActivityLog, day):
        db.add(ActivityLog(day=day))
        db.flush()


def current_streak(db) -> int:
    days = set(db.scalars(select(ActivityLog.day)).all())
    if not days:
        return 0
    streak = 0
    cur = date.today()
    # Allow the streak to count from today or yesterday (today not yet active).
    if cur.isoformat() not in days:
        cur = cur - timedelta(days=1)
        if cur.isoformat() not in days:
            return 0
    while cur.isoformat() in days:
        streak += 1
        cur -= timedelta(days=1)
    return streak


def analytics(db) -> dict:
    attempts = list(db.scalars(select(QuizAttempt).order_by(QuizAttempt.created_at.desc())))
    n = len(attempts)
    avg_acc = round(sum(a.accuracy for a in attempts) / n, 3) if n else 0.0
    avg_pct = round(sum(a.percentile for a in attempts) / n, 1) if n else 0.0

    # Aggregate subject accuracy across all attempts.
    agg: dict[str, dict] = {}
    for a in attempts:
        try:
            sb = json.loads(a.subject_breakdown_json or "{}")
        except Exception:  # noqa: BLE001
            sb = {}
        for s, b in sb.items():
            bucket = agg.setdefault(s, {"correct": 0, "total": 0})
            bucket["correct"] += int(b.get("correct", 0))
            bucket["total"] += int(b.get("total", 0))
    by_subject = {
        s: {**b, "accuracy": round(b["correct"] / b["total"], 3) if b["total"] else 0.0}
        for s, b in agg.items()
    }
    streak = current_streak(db)
    due = db.scalar(
        select(func.count()).select_from(ReviewItem).where(ReviewItem.due_at <= _now())
    ) or 0
    weak = sorted(
        [(s, b["accuracy"]) for s, b in by_subject.items() if b["total"] and b["accuracy"] < 0.6],
        key=lambda x: x[1],
    )
    return {
        "attempts": n,
        "avg_accuracy": avg_acc,
        "avg_percentile": avg_pct,
        "streak": streak,
        "due_reviews": int(due),
        "review_items": db.scalar(select(func.count()).select_from(ReviewItem)) or 0,
        "by_subject": by_subject,
        "weak_areas": [s for s, _ in weak],
        "recent": [
            {
                "kind": a.kind, "subject": a.subject, "score": a.score,
                "max_score": a.max_score, "accuracy": a.accuracy,
                "percentile": a.percentile, "at": a.created_at.isoformat(),
            }
            for a in attempts[:8]
        ],
    }
