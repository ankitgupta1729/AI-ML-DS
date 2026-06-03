"""Lightweight tests that don't require network or an API key."""

import sys
from pathlib import Path

import pytest  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gate_chatbot.config import Settings  # noqa: E402
from gate_chatbot.ingestion import (  # noqa: E402
    SUPPORTED_EXTENSIONS,
    _chunk,
    _dedupe_by_id,
    discover_files,
)
from langchain_core.documents import Document  # noqa: E402


def test_settings_defaults():
    s = Settings(OPENAI_API_KEY="test")
    assert s.chat_model
    assert s.chunk_size > s.chunk_overlap
    assert 0 <= s.relevance_threshold <= 1


def test_supported_extensions():
    for ext in (".pdf", ".docx", ".pptx", ".txt", ".md", ".markdown"):
        assert ext in SUPPORTED_EXTENSIONS


def test_chunking_assigns_ids():
    s = Settings(OPENAI_API_KEY="test", CHUNK_SIZE=50, CHUNK_OVERLAP=10)
    # Distinct words per chunk -> distinct content -> distinct hash IDs.
    text = " ".join(f"token{i}" for i in range(400))
    docs = [Document(page_content=text, metadata={"path": "x.txt"})]
    chunks = _chunk(docs, s)
    assert len(chunks) > 1
    assert all("chunk_id" in c.metadata for c in chunks)
    # Unique content yields unique IDs (identical content would dedup by design).
    assert len({c.metadata["chunk_id"] for c in chunks}) == len(chunks)


def test_discover_finds_seed_doc():
    repo = Path(__file__).resolve().parents[1]
    files = discover_files(repo / "data")
    assert any(f.name.endswith(".md") for f in files)


def test_dedupe_by_id_collapses_identical_chunks():
    # Identical content within a file → identical chunk_id → must collapse to
    # one (Chroma rejects duplicate IDs inside a single upsert request).
    docs = [
        Document(page_content="repeated header", metadata={"chunk_id": "a"}),
        Document(page_content="repeated header", metadata={"chunk_id": "a"}),
        Document(page_content="unique body", metadata={"chunk_id": "b"}),
    ]
    unique = _dedupe_by_id(docs)
    assert [d.metadata["chunk_id"] for d in unique] == ["a", "b"]


def test_db_feedback_and_preference_flow(tmp_path):
    pytest.importorskip("sqlalchemy")
    from gate_chatbot import db

    db._engine = None  # force a fresh in-memory engine for the test
    db._SessionLocal = None
    s = Settings(OPENAI_API_KEY="test", DATABASE_URL="sqlite:///:memory:")
    db.init_db(s)

    with db.session() as sess:
        conv = db.get_or_create_conversation(sess, None, "What is a B+ tree?")
        db.add_message(sess, conversation_id=conv.id, role="user", content="What is a B+ tree?")
        a = db.add_message(sess, conversation_id=conv.id, role="assistant", content="wrong")
        sess.commit()
        aid = a.id

    with db.session() as sess:
        db.record_feedback(sess, message_id=aid, rating="down", reason="incorrect")
        assert db.message_was_disliked(sess, aid)
        q, _ = db.preceding_user_question(sess, aid)
        assert q == "What is a B+ tree?"
        db.add_preference_pair(
            sess, prompt=q, chosen="right", rejected="wrong", kind="human_correction"
        )
        sess.commit()

    with db.session() as sess:
        prefs = db.export_preferences(sess)
        assert len(prefs) == 1 and prefs[0]["chosen"] == "right"
        assert db.stats(sess)["dislikes"] == 1
