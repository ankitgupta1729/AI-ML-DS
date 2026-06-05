#!/usr/bin/env python3
"""Build the CONCISE demo video from REAL screenshots of the running app.

A ~3-minute highlight reel: intro, "why it's different" comparison, the key
features shown live, architecture, and outro. Reuses the helpers from
build_live_video.py. Output: demo/GateOverflow-Chatbot-Demo.mp4

Run (with the app running and demo/live/ captured):
    python demo/build_live_demo.py
"""

from __future__ import annotations

import shutil
from pathlib import Path

# Reuse the rendering helpers + styling from the detailed-guide builder.
from build_live_video import (  # noqa: E402  (demo/ is on sys.path at runtime)
    CHROME, LOGO_BIG, VOICE, W, H, _img, duration, page, sh, shot_scene,
)

ROOT = Path(__file__).resolve().parent
LIVE = ROOT / "live"
FRAMES = ROOT / "frames_demo"
OUT = ROOT / "GateOverflow-Chatbot-Demo.mp4"

CARD = "border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:16px;background:rgba(15,23,42,.5)"
GO_CARD = "border:1px solid rgba(220,38,38,.45);border-radius:16px;padding:16px;background:rgba(220,38,38,.06)"
NODE = "border:1px solid rgba(255,255,255,.14);background:rgba(15,23,42,.6);border-radius:14px;padding:13px 16px;min-width:150px;text-align:center"


def _row(mark, color, text):
    return f'<div style="font-size:13px;color:#cbd5e1;margin:7px 0"><span style="color:{color}">{mark}</span> {text}</div>'


RAW = [
    dict(kind="center", title="GateOverflow Chatbot", sub="Product demo",
         narration="This is the GateOverflow Chatbot — a complete AI study companion for the GATE Computer Science and Data Science and AI exams, grounded in real previous-year questions. Everything you'll see is the live application.",
         inner=f'<div class="center">{LOGO_BIG}<div class="big">GateOverflow Chatbot</div>'
               '<div class="sub">Your AI study buddy for GATE CS &amp; DA — grounded in real previous-year questions.</div>'
               '<div class="chips"><span class="chip">Grounded RAG</span><span class="chip">Mock tests</span>'
               '<span class="chip">Spaced repetition</span><span class="chip">Analytics &amp; RLHF</span></div></div>'),

    dict(kind="center", title="Why not just use ChatGPT or Claude?", sub="A GATE specialist vs. a general chatbot",
         narration="Why not just use ChatGPT, Claude or DeepSeek? Because exam prep needs trust and structure. General chatbots are brilliant generalists that can hallucinate. This is a GATE specialist: it cites real previous-year questions, scores mock tests, schedules revision, and learns from your feedback.",
         inner='<div class="center"><div class="big" style="font-size:30px">A specialist, not a generalist</div>'
               '<div style="display:flex;gap:18px;width:100%;margin-top:8px">'
               f'<div style="flex:1;{CARD}"><h3 style="font-size:15px;color:#fff;margin-bottom:8px">🌐 ChatGPT / Claude / DeepSeek</h3>'
               + _row("✗", "#f87171", "Generic web knowledge")
               + _row("✗", "#f87171", "Can invent fake “GATE questions”")
               + _row("✗", "#f87171", "No citations to your material")
               + _row("✗", "#f87171", "No scoring, mock tests or revision")
               + _row("✗", "#f87171", "Forgets your corrections")
               + '</div>'
               f'<div style="flex:1;{GO_CARD}"><h3 style="font-size:15px;color:#fff;margin-bottom:8px">🎯 GateOverflow Chatbot</h3>'
               + _row("✓", "#4ade80", "Grounded in real PYQs &amp; your notes")
               + _row("✓", "#4ade80", "Cites source file, page &amp; match score")
               + _row("✓", "#4ade80", "Mock tests with GATE negative marking")
               + _row("✓", "#4ade80", "Spaced repetition + analytics")
               + _row("✓", "#4ade80", "Learns from feedback (RLHF)")
               + '</div></div></div>'),

    dict(kind="shot", img="02_welcome.png", kicker="Workspace",
         title="One focused study workspace", sub="Chat · Mock Test · Flashcards · Planner · Dashboard · Daily",
         howto="Use the sidebar to switch modules; click an example to begin.",
         narration="It opens to a clean workspace. A sidebar gives you chat, mock tests, flashcards, a planner, a dashboard and a daily question — all tuned for GATE — with example prompts to get started instantly."),

    dict(kind="shot", img="03_chat.png", kicker="Chat",
         title="Ask anything — grounded answers", sub="LaTeX, a grounding meter and quick actions, streamed live",
         howto="Type a question and press Enter.",
         narration="Ask any question. Answers stream in with proper mathematics, a grounding-confidence meter that shows how well the answer is backed by your material, and quick actions to copy, rate, regenerate or read it aloud."),

    dict(kind="shot", img="04_sources.png", kicker="Trust",
         title="Every answer cites its sources", sub="Real PYQ files, pages and match scores",
         howto="Expand “sources” under any answer.",
         narration="And every answer can show exactly where it came from — real previous-year-question PDFs with page references and match scores. That verifiability is the biggest difference from a general chatbot."),

    dict(kind="shot", img="18_pyq_links.png", kicker="GateOverflow",
         title="Direct GateOverflow question links", sub="PYQ answers link to the exact thread",
         howto="Click a link under “See this question on GateOverflow”.",
         narration="And for previous-year questions, the answer links straight to that exact question on GateOverflow — pulled from the URLs in the question PDFs — so you can read the official discussion and community answers. These links appear only for previous-year questions."),

    dict(kind="shot", img="07_mock_result.png", kicker="Practice",
         title="Mock tests, scored like GATE", sub="Negative marking · percentile · explanations",
         howto="Open Mock Test, answer, and submit.",
         narration="The mock-test module generates exam-style questions and scores them with real GATE negative marking and an estimated percentile, with an explanation for every question — turning study into measurable practice."),

    dict(kind="shot", img="09_flashcards.png", kicker="Revision",
         title="Flashcards & spaced repetition", sub="SM-2 schedule · wrong answers become cards",
         howto="Generate a deck or review what's due.",
         narration="Missed questions automatically become flashcards, reviewed on a spaced-repetition schedule so you remember them for the exam."),

    dict(kind="shot", img="10_planner.png", kicker="Planning",
         title="Day-by-day study planner", sub="Prioritised plan → export to calendar",
         howto="Set your exam date, build the plan, export the .ics.",
         narration="The planner builds a day-by-day schedule to your exam date, prioritising high-weight subjects, and exports straight to your calendar."),

    dict(kind="shot", img="08_dashboard.png", kicker="Insight",
         title="Performance dashboard", sub="Readiness · accuracy by subject · weak areas",
         howto="Take a few quizzes, then open Dashboard.",
         narration="A dashboard turns your attempts into insight: an exam-readiness score, accuracy by subject, your streak, and the weak areas to prioritise next."),

    dict(kind="shot", img="13_hindi.png", kicker="Multimodal",
         title="Multilingual, voice, sketch & more", sub="Study the way that suits you",
         howto="Pick a language, use 🎙️ voice, ✏️ sketch, 📎 attach.",
         narration="You can get explanations in Hindi and other languages, ask by voice and listen to answers, sketch a diagram, attach images or PDFs, and switch on Socratic mode for hints before solutions."),

    dict(kind="shot", img="14_feedback.png", kicker="Improvement",
         title="Feedback → RLHF", sub="Dislike → reason → regenerate → preference data",
         howto="👎 an answer, give a reason, then ↻ regenerate.",
         narration="And it learns from you. Dislike an answer with a reason and it regenerates a better one, while your corrections build a preference dataset you can export to fine-tune an improved model. Unlike general chatbots, it gets better from your feedback."),

    dict(kind="shot", img="19_cheatsheet.png", kicker="Productivity",
         title="Save, revisit & export", sub="Bookmarks · history · cheat-sheet · PDF export",
         howto="★ save answers · 🕑 history · “Cheat sheet” / “Export PDF”.",
         narration="Everything you learn stays with you: star answers to save them, revisit any past conversation from the history panel, and with one click turn a chat into a revision cheat-sheet or export it to PDF for last-minute study."),

    dict(kind="center", title="Architecture", sub="React + TypeScript + Tailwind ⇄ FastAPI ⇄ Chroma RAG + OpenAI",
         narration="Under the hood, a React, TypeScript and Tailwind front-end talks to a FastAPI backend running retrieval-augmented generation over a Chroma vector store with OpenAI, and persists everything in a database.",
         inner='<div class="center"><div class="big" style="font-size:30px">How it fits together</div>'
               '<div style="display:flex;align-items:center;justify-content:center;gap:16px;margin-top:14px;flex-wrap:wrap">'
               f'<div style="{NODE}"><div style="font-weight:800;color:#fff;font-size:14px">React + TS</div><div style="font-size:11px;color:#94a3b8">Vite · Tailwind · SSE</div></div>'
               '<span style="color:#f87171;font-size:22px;font-weight:800">⇄</span>'
               f'<div style="{NODE};border-color:rgba(220,38,38,.45)"><div style="font-weight:800;color:#fff;font-size:14px">FastAPI</div><div style="font-size:11px;color:#94a3b8">chat · quiz · review · plan</div></div>'
               '<span style="color:#f87171;font-size:22px;font-weight:800">⇄</span>'
               f'<div style="{NODE}"><div style="font-weight:800;color:#fff;font-size:14px">RAG engine</div><div style="font-size:11px;color:#94a3b8">Chroma + OpenAI</div></div>'
               '</div>'
               '<div style="display:flex;align-items:center;justify-content:center;gap:16px;margin-top:14px;flex-wrap:wrap">'
               f'<div style="{NODE}"><div style="font-weight:800;color:#fff;font-size:14px">data/ PDFs + notes</div><div style="font-size:11px;color:#94a3b8">ingested &amp; chunked</div></div>'
               f'<div style="{NODE}"><div style="font-weight:800;color:#fff;font-size:14px">SQLite / Postgres</div><div style="font-size:11px;color:#94a3b8">chats · feedback · progress</div></div>'
               f'<div style="{NODE};border-color:rgba(220,38,38,.45)"><div style="font-weight:800;color:#fff;font-size:14px">gpt-4o-mini</div><div style="font-size:11px;color:#94a3b8">answers + vision</div></div>'
               '</div></div>'),

    dict(kind="center", title="Thank you", sub="GateOverflow Chatbot · gateoverflow.in",
         narration="That's the GateOverflow Chatbot — rich in knowledge, grounded in real questions, with mock tests, spaced repetition, analytics and a feedback loop, built to production standards. Thanks for watching!",
         inner=f'<div class="center">{LOGO_BIG}<div class="big" style="font-size:34px">Rich. Grounded. Production-ready.</div>'
               '<div class="sub">Grounded answers · PYQs &amp; mock tests · spaced repetition · planner · dashboard · voice &amp; multilingual · feedback that learns.</div>'
               '<div class="chips"><span class="chip">Built for GateOverflow · gateoverflow.in</span></div></div>'),
]


def main() -> int:
    if not Path(CHROME).exists():
        print("❌ Chrome not found"); return 1
    for t in ("ffmpeg", "say", "ffprobe"):
        if shutil.which(t) is None:
            print(f"❌ {t} not found"); return 1
    missing = [s["img"] for s in RAW if s["kind"] == "shot" and not (LIVE / s["img"]).exists()]
    if missing:
        print("❌ missing screenshots:", missing); return 1

    if FRAMES.exists():
        shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True)

    total = len(RAW)
    segments = []
    for i, sc in enumerate(RAW, 1):
        if sc["kind"] == "center":
            html_str = page(sc["inner"], sc["title"], sc["sub"], i, total)
        else:
            html_str = shot_scene(i, total, img=sc["img"], kicker=sc["kicker"],
                                  title=sc["title"], sub=sc["sub"], howto=sc["howto"])
        html, png = FRAMES / f"{i:02d}.html", FRAMES / f"{i:02d}.png"
        aiff, seg = FRAMES / f"{i:02d}.aiff", FRAMES / f"{i:02d}.mp4"
        html.write_text(html_str, encoding="utf-8")
        print(f"🎬 {i}/{total} rendering")
        sh([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=2", f"--window-size={W},{H}",
            f"--screenshot={png}", f"file://{html}", "--virtual-time-budget=2500"])
        sh(["say", "-v", VOICE, "-o", str(aiff), sc["narration"]])
        dur = max(duration(aiff) + 0.9, 4.5)
        vf = (f"scale=1920:1080:force_original_aspect_ratio=decrease,"
              f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x020617,fps=30,"
              f"fade=t=in:st=0:d=0.3,fade=t=out:st={dur-0.35:.2f}:d=0.35")
        sh(["ffmpeg", "-y", "-loop", "1", "-t", f"{dur:.2f}", "-i", str(png), "-i", str(aiff),
            "-filter_complex", f"[0:v]{vf}[v];[1:a]apad[a]", "-map", "[v]", "-map", "[a]",
            "-t", f"{dur:.2f}", "-c:v", "libx264", "-preset", "medium", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "160k", "-ar", "44100", str(seg)])
        segments.append(seg)
        print(f"   ✓ {dur:.1f}s")

    listfile = FRAMES / "concat.txt"
    listfile.write_text("".join(f"file '{s}'\n" for s in segments), encoding="utf-8")
    print("🎞️  concatenating →", OUT.name)
    sh(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile), "-c", "copy", str(OUT)])
    print(f"\n✅ Done: {OUT}  ({duration(OUT):.1f}s, {total} scenes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
