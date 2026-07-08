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


def test_extract_json_handles_fences_and_noise():
    from gate_chatbot.study import extract_json

    assert extract_json('```json\n{"a": 1}\n```') == {"a": 1}
    assert extract_json('Here you go: [1, 2, 3] cheers') == [1, 2, 3]
    assert extract_json("not json at all") is None


def test_sm2_progression():
    from gate_chatbot.study import sm2

    # A failed recall resets repetitions and schedules tomorrow.
    bad = sm2(quality=1, repetitions=4, ease=2.5, interval=30)
    assert bad["repetitions"] == 0 and bad["interval"] == 1

    # Successful recalls grow the interval and keep ease >= 1.3.
    s1 = sm2(quality=5, repetitions=0, ease=2.5, interval=0)
    assert s1["interval"] == 1 and s1["repetitions"] == 1
    s2 = sm2(quality=5, repetitions=s1["repetitions"], ease=s1["ease"], interval=s1["interval"])
    assert s2["interval"] == 6
    s3 = sm2(quality=4, repetitions=s2["repetitions"], ease=s2["ease"], interval=s2["interval"])
    assert s3["interval"] > 6 and s3["ease"] >= 1.3


def test_score_quiz_gate_negative_marking():
    from gate_chatbot.study import score_quiz

    questions = [
        {"id": "0", "type": "MCQ", "options": ["a", "b", "c", "d"], "answer": 1,
         "marks": 1, "subject": "algorithms"},
        {"id": "1", "type": "MCQ", "options": ["a", "b", "c", "d"], "answer": 2,
         "marks": 2, "subject": "os"},
        {"id": "2", "type": "MSQ", "options": ["a", "b", "c", "d"], "answer": [0, 2],
         "marks": 2, "subject": "dbms"},
        {"id": "3", "type": "NAT", "options": [], "answer": "3.14",
         "marks": 1, "subject": "maths"},
    ]
    answers = {"0": 1, "1": 0, "2": [0, 2], "3": "3.14"}  # q1 wrong MCQ (2 mark)
    r = score_quiz(questions, answers)
    # +1 (q0) -2/3 (q1) +2 (q2) +1 (q3) = 3.333…
    assert r["correct"] == 3
    assert abs(r["score"] - (1 - 2 / 3 + 2 + 1)) < 0.01
    assert r["max_score"] == 6
    assert 0 <= r["percentile"] <= 100
    assert "os" in r["subject_breakdown"]


def test_score_quiz_no_negative_for_msq_nat():
    from gate_chatbot.study import score_quiz

    questions = [
        {"id": "0", "type": "MSQ", "options": ["a", "b"], "answer": [0], "marks": 2, "subject": "x"},
        {"id": "1", "type": "NAT", "options": [], "answer": "5", "marks": 1, "subject": "y"},
    ]
    r = score_quiz(questions, {"0": [0, 1], "1": "9"})  # both wrong
    assert r["score"] == 0.0  # no negative marking on MSQ/NAT


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


def test_db_study_flow():
    pytest.importorskip("sqlalchemy")
    from gate_chatbot import db
    from gate_chatbot.study import score_quiz

    db._engine = None
    db._SessionLocal = None
    db.init_db(Settings(OPENAI_API_KEY="test", DATABASE_URL="sqlite:///:memory:"))

    questions = [
        {"id": "0", "type": "MCQ", "options": ["a", "b"], "answer": 0, "marks": 1,
         "subject": "algorithms", "explanation": "because a"},
        {"id": "1", "type": "MCQ", "options": ["a", "b"], "answer": 1, "marks": 1,
         "subject": "os", "explanation": "because b"},
    ]
    scored = score_quiz(questions, {"0": 0, "1": 0})  # q1 wrong

    with db.session() as sess:
        qid = db.save_generated_quiz(sess, exam="CS", subject="mixed",
                                     difficulty="medium", questions=questions)
        assert db.load_generated_quiz(sess, qid)
        db.save_attempt(sess, kind="quiz", exam="CS", subject="mixed",
                        scored=scored, duration_sec=42)
        db.add_review_item(sess, front="q", back="a", subject="os", source="quiz")
        db.log_activity(sess)
        sess.commit()

    with db.session() as sess:
        assert db.current_streak(sess) >= 1
        assert len(db.due_review_items(sess)) == 1
        a = db.analytics(sess)
        assert a["attempts"] == 1 and a["review_items"] == 1
        assert "os" in a["by_subject"]
