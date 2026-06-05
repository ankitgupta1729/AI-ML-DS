"""Study-suite logic: quiz generation & scoring (GATE rules), spaced
repetition (SM-2), flashcards, study plans, and analytics helpers.

The deterministic parts (scoring, SM-2, JSON extraction, percentile) are pure
functions with no external dependencies, so they're fully unit-testable offline.
"""

from __future__ import annotations

import json
import re
from typing import Any

from .prompts import CHEATSHEET_PROMPT, FLASHCARD_PROMPT, PLAN_PROMPT, QUIZ_PROMPT

# --------------------------------------------------------------------------- #
# Robust JSON extraction from an LLM response                                 #
# --------------------------------------------------------------------------- #
def extract_json(text: str) -> Any | None:
    """Parse the first JSON object/array in ``text`` (tolerates ``` fences)."""
    if not text:
        return None
    t = text.strip()
    # Strip ```json … ``` fences if present.
    fence = re.search(r"```(?:json)?\s*(.*?)```", t, re.DOTALL)
    if fence:
        t = fence.group(1).strip()
    try:
        return json.loads(t)
    except Exception:  # noqa: BLE001
        pass
    # Fall back to scanning for the first balanced { } or [ ].
    for open_ch, close_ch in (("{", "}"), ("[", "]")):
        start = t.find(open_ch)
        if start == -1:
            continue
        depth = 0
        for i in range(start, len(t)):
            if t[i] == open_ch:
                depth += 1
            elif t[i] == close_ch:
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(t[start : i + 1])
                    except Exception:  # noqa: BLE001
                        break
    return None


# --------------------------------------------------------------------------- #
# Spaced repetition — SM-2                                                     #
# --------------------------------------------------------------------------- #
def sm2(quality: int, repetitions: int, ease: float, interval: int) -> dict:
    """SuperMemo-2 update. ``quality`` is 0–5 (>=3 == correct recall).

    Returns the new repetitions, ease factor, interval (days) and due-in days.
    """
    quality = max(0, min(5, int(quality)))
    if quality < 3:
        repetitions = 0
        interval = 1
    else:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = round(interval * ease)
        repetitions += 1

    ease = ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ease = max(1.3, round(ease, 2))
    return {"repetitions": repetitions, "ease": ease, "interval": interval, "due_in_days": interval}


# --------------------------------------------------------------------------- #
# Quiz scoring with GATE negative marking                                     #
# --------------------------------------------------------------------------- #
def _nat_correct(user: Any, answer: Any) -> bool:
    try:
        u, a = float(str(user).strip()), float(str(answer).strip())
    except (TypeError, ValueError):
        return False
    return abs(u - a) <= max(0.01, abs(a) * 0.01)


def _is_correct(q: dict, user: Any) -> bool:
    qtype = (q.get("type") or "MCQ").upper()
    answer = q.get("answer")
    if user is None or user == "" or user == []:
        return False
    if qtype == "NAT":
        return _nat_correct(user, answer)
    if qtype == "MSQ":
        want = {int(x) for x in answer} if isinstance(answer, list) else {int(answer)}
        try:
            got = {int(x) for x in (user if isinstance(user, list) else [user])}
        except (TypeError, ValueError):
            return False
        return got == want
    # MCQ
    try:
        return int(user) == int(answer)
    except (TypeError, ValueError):
        return str(user).strip() == str(answer).strip()


def score_quiz(questions: list[dict], answers: dict[str, Any]) -> dict:
    """Score a quiz with GATE rules. ``answers`` maps str(question-id) → choice.

    Negative marking: wrong MCQ loses 1/3 (1-mark) or 2/3 (2-mark). MSQ and NAT
    have no negative marking. Unanswered = 0.
    """
    total_marks = 0.0
    max_marks = 0.0
    correct = 0
    answered = 0
    results: list[dict] = []
    subj: dict[str, dict] = {}

    for idx, q in enumerate(questions):
        qid = str(q.get("id", idx))
        marks = float(q.get("marks", 1) or 1)
        qtype = (q.get("type") or "MCQ").upper()
        max_marks += marks
        user = answers.get(qid, answers.get(str(idx)))
        has_answer = not (user is None or user == "" or user == [])
        ok = _is_correct(q, user) if has_answer else False

        if has_answer:
            answered += 1
        if ok:
            awarded = marks
            correct += 1
        elif has_answer and qtype == "MCQ":
            awarded = -(1 / 3 if marks == 1 else 2 / 3 if marks == 2 else marks / 3)
        else:
            awarded = 0.0
        total_marks += awarded

        s = q.get("subject", "general")
        bucket = subj.setdefault(s, {"correct": 0, "total": 0})
        bucket["total"] += 1
        if ok:
            bucket["correct"] += 1

        results.append({
            "id": qid,
            "type": qtype,
            "question": q.get("question", ""),
            "options": q.get("options", []),
            "your_answer": user,
            "correct_answer": q.get("answer"),
            "is_correct": ok,
            "awarded": round(awarded, 3),
            "marks": marks,
            "explanation": q.get("explanation", ""),
            "subject": s,
        })

    total_marks = round(max(total_marks, 0.0), 2)  # GATE never goes below 0 overall
    ratio = total_marks / max_marks if max_marks else 0.0
    return {
        "score": total_marks,
        "max_score": round(max_marks, 2),
        "correct": correct,
        "answered": answered,
        "total": len(questions),
        "accuracy": round(correct / len(questions), 3) if questions else 0.0,
        "percentile": estimate_percentile(ratio),
        "subject_breakdown": {
            k: {**v, "accuracy": round(v["correct"] / v["total"], 3) if v["total"] else 0.0}
            for k, v in subj.items()
        },
        "results": results,
    }


def estimate_percentile(ratio: float) -> float:
    """Rough GATE percentile estimate from a score ratio (0–1). Heuristic only."""
    ratio = max(0.0, min(1.0, ratio))
    # Logistic-ish mapping: ~40% score ≈ 85th percentile (GATE is competitive).
    import math

    pct = 100 / (1 + math.exp(-9 * (ratio - 0.32)))
    return round(min(99.9, pct), 1)


def weak_areas(subject_breakdown: dict[str, dict], threshold: float = 0.6) -> list[str]:
    """Subjects whose accuracy is below ``threshold`` (worst first)."""
    weak = [
        (s, b.get("accuracy", 0.0))
        for s, b in subject_breakdown.items()
        if b.get("total", 0) and b.get("accuracy", 0.0) < threshold
    ]
    return [s for s, _ in sorted(weak, key=lambda x: x[1])]


def readiness_score(avg_accuracy: float, attempts: int, streak: int) -> int:
    """A 0–100 'exam readiness' score blending accuracy, practice volume & habit."""
    acc = max(0.0, min(1.0, avg_accuracy))
    volume = min(1.0, attempts / 20)      # ~20 quizzes ≈ full marks for practice
    habit = min(1.0, streak / 14)         # a 2-week streak ≈ full marks for habit
    score = 100 * (0.6 * acc + 0.25 * volume + 0.15 * habit)
    return int(round(score))


# --------------------------------------------------------------------------- #
# LLM-backed generation (uses the chat engine)                                #
# --------------------------------------------------------------------------- #
def _normalise_questions(raw: list[dict]) -> list[dict]:
    """Coerce model output into a consistent quiz schema with indexed answers."""
    out: list[dict] = []
    letters = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}
    for i, q in enumerate(raw):
        qtype = str(q.get("type", "MCQ")).upper()
        if qtype not in ("MCQ", "MSQ", "NAT"):
            qtype = "MCQ"
        options = q.get("options") or []
        if qtype == "NAT":
            options = []
        ans = q.get("answer")

        def to_index(v):
            if isinstance(v, int):
                return v
            v = str(v).strip()
            if v.upper() in letters:
                return letters[v.upper()]
            # match against option text
            for j, opt in enumerate(options):
                if str(opt).strip().lower() == v.lower():
                    return j
            try:
                return int(v)
            except ValueError:
                return 0

        if qtype == "MCQ":
            answer: Any = to_index(ans)
        elif qtype == "MSQ":
            lst = ans if isinstance(ans, list) else [ans]
            answer = sorted({to_index(x) for x in lst})
        else:  # NAT
            answer = str(ans).strip()

        try:
            marks = int(q.get("marks", 1))
            marks = 2 if marks == 2 else 1
        except (TypeError, ValueError):
            marks = 1

        out.append({
            "id": str(i),
            "type": qtype,
            "question": str(q.get("question", "")).strip(),
            "options": [str(o) for o in options],
            "answer": answer,
            "explanation": str(q.get("explanation", "")).strip(),
            "subject": str(q.get("subject", "general")).strip() or "general",
            "difficulty": str(q.get("difficulty", "medium")).strip() or "medium",
            "marks": marks,
        })
    return [q for q in out if q["question"]]


def generate_quiz(engine, *, exam: str, subject: str, n: int, difficulty: str) -> list[dict]:
    context = engine.retrieve_context(f"{subject} GATE {exam} previous year questions", k=5)
    prompt = QUIZ_PROMPT.format(
        exam=exam, subject=subject, n=n, difficulty=difficulty,
        context=context or "(no extra material — use your expert knowledge)",
    )
    data = extract_json(engine.generate_json(prompt)) or {}
    questions = data.get("questions") if isinstance(data, dict) else data
    return _normalise_questions(questions or [])[:n]


def generate_flashcards(engine, *, exam: str, topic: str, n: int) -> list[dict]:
    prompt = FLASHCARD_PROMPT.format(exam=exam, topic=topic, n=n)
    data = extract_json(engine.generate_json(prompt)) or {}
    cards = data.get("cards") if isinstance(data, dict) else data
    out = []
    for c in (cards or []):
        front, back = str(c.get("front", "")).strip(), str(c.get("back", "")).strip()
        if front and back:
            out.append({"front": front, "back": back, "subject": str(c.get("subject", topic))})
    return out[:n]


def generate_cheatsheet(engine, *, transcript: str) -> str:
    """Build a Markdown revision cheat-sheet from a conversation transcript."""
    prompt = CHEATSHEET_PROMPT.format(transcript=transcript[:12000])
    text = (engine.generate_json(prompt) or "").strip()
    # Strip stray ``` fences if the model wrapped the whole thing.
    if text.startswith("```"):
        text = re.sub(r"^```[a-z]*\n|\n```$", "", text)
    return text


def generate_plan(engine, *, exam: str, days: int, hours: float) -> dict:
    prompt = PLAN_PROMPT.format(exam=exam, days=days, hours=hours)
    data = extract_json(engine.generate_json(prompt)) or {}
    if not isinstance(data, dict):
        data = {}
    plan_days = data.get("days") or []
    clean = []
    for d in plan_days:
        clean.append({
            "day": int(d.get("day", len(clean) + 1)),
            "focus": str(d.get("focus", "")).strip(),
            "tasks": [str(t) for t in (d.get("tasks") or [])],
            "hours": float(d.get("hours", hours) or hours),
        })
    return {"summary": str(data.get("summary", "")).strip(), "days": clean}
