#!/usr/bin/env python3
"""Build a DETAILED, narrated feature-guide video for the GateOverflow Chatbot.

For every feature it explains: Purpose · Example · Benefit & why it's better than
ChatGPT/Claude/DeepSeek · How to use it. Fully offline (Chrome + ffmpeg + `say`).

Run:  python demo/build_detailed_video.py
Output: demo/GateOverflow-Chatbot-Feature-Guide.mp4
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FRAMES = ROOT / "frames_detailed"
OUT = ROOT / "GateOverflow-Chatbot-Feature-Guide.mp4"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
VOICE = "Samantha"
W, H = 1280, 720

GO_LOGO = """
<svg viewBox="0 0 100 100" width="{s}" height="{s}" style="display:block">
  <text x="60" y="50" text-anchor="middle" font-family="Georgia,serif" font-size="74"
        font-weight="700" fill="#dc2626" transform="rotate(9 60 44)">?</text>
  <text x="49" y="86" text-anchor="middle" font-family="Arial,sans-serif" font-size="50"
        font-weight="900" fill="{go}" letter-spacing="-2">GO</text>
</svg>
"""

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',system-ui,-apple-system,sans-serif;background:#020617}
.app{position:relative;width:1280px;height:720px;overflow:hidden;background:linear-gradient(180deg,#020617,#0b1220)}
.glow{position:absolute;border-radius:9999px;filter:blur(80px)}
.glow.a{top:-120px;left:50%;transform:translateX(-50%);width:640px;height:240px;background:rgba(220,38,38,.16)}
.glow.b{bottom:40px;right:-40px;width:280px;height:280px;background:rgba(225,29,72,.12)}
.watermark{position:absolute;top:12px;right:24px;font-size:11px;color:#475569}
.kicker{position:absolute;top:14px;left:26px;font-size:12px;font-weight:700;letter-spacing:.5px;
  text-transform:uppercase;color:#f87171}
/* feature layout */
.wrap{display:flex;gap:22px;height:556px;padding:44px 30px 0}
.illus{flex:0 0 360px;border:1px solid rgba(255,255,255,.1);border-radius:18px;
  background:rgba(15,23,42,.55);padding:22px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:12px}
.bigicon{font-size:60px;line-height:1}
.iname{font-size:22px;font-weight:800;color:#fff}
.mock{width:100%;margin-top:4px}
.facets{flex:1;display:flex;flex-direction:column;gap:11px}
.facet{border:1px solid rgba(255,255,255,.1);border-radius:14px;background:rgba(15,23,42,.5);padding:11px 14px}
.facet .h{font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.4px;color:#f87171;margin-bottom:3px}
.facet .b{font-size:13.5px;color:#dbeafe;line-height:1.5}
.facet.better .h{color:#4ade80}
.facet ol{margin:2px 0 0 16px}.facet li{font-size:13px;color:#cbd5e1;margin:2px 0}
/* mock bits */
.bub{background:rgba(2,6,23,.6);border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:9px 12px;font-size:12.5px;color:#dbeafe;text-align:left}
.ubub{background:linear-gradient(135deg,#dc2626,#b91c1c);color:#fff;border-radius:12px;padding:7px 11px;font-size:12.5px;display:inline-block}
.math{font-family:Georgia,serif;font-style:italic;background:rgba(220,38,38,.14);padding:1px 6px;border-radius:5px;color:#fecaca}
.src{margin-top:7px;border:1px solid rgba(255,255,255,.12);border-radius:9px;padding:6px 8px;font-size:10.5px;color:#94a3b8}
.src .nm{color:#fff}
.pill{font-size:9px;border-radius:9999px;padding:1px 6px;background:rgba(34,197,94,.15);color:#4ade80}
.chips{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin-top:4px}
.chip{font-size:11px;border:1px solid rgba(255,255,255,.14);border-radius:9999px;padding:4px 10px;color:#cbd5e1}
.chip.red{border-color:rgba(220,38,38,.4);color:#fca5a5}
.opt{border:1px solid rgba(255,255,255,.14);border-radius:8px;padding:6px 9px;font-size:12px;color:#cbd5e1;margin-top:5px;text-align:left}
.opt.ok{border-color:#22c55e;background:rgba(34,197,94,.12);color:#bbf7d0}
.meter{height:8px;border-radius:9999px;background:rgba(255,255,255,.1);overflow:hidden;margin-top:6px}
.meter span{display:block;height:100%;background:linear-gradient(90deg,#dc2626,#e11d48)}
.bar{height:7px;border-radius:9999px;background:rgba(255,255,255,.1);overflow:hidden;margin:5px 0}
.bar span{display:block;height:100%}
.grades{display:flex;gap:5px;justify-content:center;margin-top:6px}
.g{font-size:10px;border:1px solid rgba(255,255,255,.2);border-radius:7px;padding:3px 9px;color:#cbd5e1}
/* center scenes */
.center{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:14px;padding:0 64px}
.big-title{font-size:42px;font-weight:900;background:linear-gradient(90deg,#f87171,#e11d48);-webkit-background-clip:text;background-clip:text;color:transparent}
.subtitle{font-size:18px;color:#94a3b8;max-width:720px}
.badge{display:grid;place-items:center;width:104px;height:104px;border-radius:28px;background:#1e293b;border:1px solid rgba(255,255,255,.1)}
.steps2{display:grid;grid-template-columns:1fr 1fr;gap:10px 22px;text-align:left;margin-top:6px}
.step{display:flex;gap:9px;font-size:14px;color:#e2e8f0}
.step .nx{color:#f87171;font-weight:800}
.caption{position:absolute;left:0;right:0;bottom:0;height:84px;background:linear-gradient(180deg,rgba(2,6,23,0),rgba(2,6,23,.92));display:flex;align-items:center;gap:14px;padding:0 30px 12px}
.cbar{width:5px;height:44px;border-radius:9999px;background:linear-gradient(#dc2626,#e11d48)}
.ctitle{font-size:19px;font-weight:800;color:#fff}.csub{font-size:12.5px;color:#cbd5e1;margin-top:2px}
.counter{margin-left:auto;font-size:12px;color:#64748b}
"""


def shell(inner, title, sub, n, total, kicker=""):
    k = f'<div class="kicker">{kicker}</div>' if kicker else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div class="app"><div class="glow a"></div><div class="glow b"></div>
<div class="watermark">gateoverflow.in</div>{k}{inner}
<div class="caption"><div class="cbar"></div><div><div class="ctitle">{title}</div>
<div class="csub">{sub}</div></div><div class="counter">{n} / {total}</div></div>
</div></body></html>"""


def feature(num, total, *, icon, name, mock, purpose, example, benefit, how, narration,
            title, sub):
    steps = "".join(f"<li>{s}</li>" for s in how)
    body = f"""<div class="wrap">
      <div class="illus"><div class="bigicon">{icon}</div><div class="iname">{name}</div>
        <div class="mock">{mock}</div></div>
      <div class="facets">
        <div class="facet"><div class="h">🎯 Purpose — why it exists</div><div class="b">{purpose}</div></div>
        <div class="facet"><div class="h">💡 Example</div><div class="b">{example}</div></div>
        <div class="facet better"><div class="h">✅ Benefit &amp; why it beats ChatGPT / Claude</div><div class="b">{benefit}</div></div>
        <div class="facet"><div class="h">🛠 How to use it</div><ol>{steps}</ol></div>
      </div></div>"""
    return dict(body=shell(body, title, sub, num, total, kicker=f"Feature {num-1} of {total-3}"),
                narration=narration)


# --------------------------------------------------------------------------- #
LOGO_BIG = f'<div class="badge">{GO_LOGO.format(s=78, go="#fff")}</div>'

# Scenes are built below with the running index so the counter is correct.
_RAW = [
    # intro
    dict(kind="center", title="GateOverflow Chatbot", sub="Detailed feature guide",
         narration="Welcome to the detailed feature guide for the GateOverflow Chatbot. For every feature we'll cover what it's for, a quick example, why it's better than a general chatbot, and exactly how to use it.",
         body=lambda n, t: shell(f'<div class="center">{LOGO_BIG}<div class="big-title">Feature Guide</div>'
                                 f'<div class="subtitle">For each feature: its purpose, an example, the benefit, and how to use it effectively — so the whole team understands the value.</div></div>',
                                 "GateOverflow Chatbot — Feature Guide", "What each feature does & how to use it", n, t)),

    dict(kind="feature", icon="💬", name="Grounded answers",
         mock='<div class="bub">Merge sort is <b style="color:#fff">O(n&nbsp;log&nbsp;n)</b> — splits &amp; merges.'
              '<div class="src">📄 <span class="nm">cs_core_concepts.md</span> · <span class="pill">91% match</span></div></div>',
         purpose="Answer questions using YOUR study material and real previous-year questions (RAG), not just generic web knowledge.",
         example="Ask “Explain conflict serializability” → you get an exam-style answer that cites the exact source file and page.",
         benefit="ChatGPT/Claude can’t see your material and give no citations; here every answer is grounded and verifiable — critical when a wrong fact costs marks.",
         how=["Type a question, press Enter.", "Read the streamed answer.", "Expand “Sources” to verify file, page & match score."],
         narration="The core feature: grounded answers. It retrieves from your own material and real previous-year questions, then answers with citations. Unlike ChatGPT or Claude, which can't see your notes and don't cite sources, every answer here is verifiable — which matters when one wrong fact costs you marks. Just type a question, read the streamed answer, and expand Sources to check exactly where it came from.",
         title="Grounded answers with citations", sub="RAG over your material & real PYQs"),

    dict(kind="feature", icon="📈", name="Confidence meter",
         mock='<div class="bub">…the answer is well supported.<div class="meter"><span style="width:88%"></span></div>'
              '<div style="font-size:10px;color:#94a3b8;margin-top:3px">Grounding 88%</div></div>',
         purpose="Show, transparently, how strongly each answer is backed by your indexed material.",
         example="A question covered by your PDFs shows ~90% grounding; an off-topic one drops low with an “answered from general knowledge” note.",
         benefit="General chatbots give the same confident tone whether right or guessing. The meter tells you when to trust and when to double-check.",
         how=["Look at the bar under each answer.", "High % = grounded in sources.", "Low % → verify before relying on it."],
         narration="Every answer carries a grounding-confidence meter. It shows how strongly the response is backed by your indexed material. A topic covered by your PDFs scores high; something outside it drops low and is clearly flagged. General chatbots sound equally confident whether they're right or guessing — this meter tells you when to trust an answer and when to double-check it.",
         title="Grounding-confidence meter", sub="Transparency on every answer"),

    dict(kind="feature", icon="🔁", name="Actions & follow-ups",
         mock='<div class="bub">Quicksort worst case is <span class="math">O(n²)</span>.'
              '<div style="margin-top:6px">⧉ &nbsp; 👍 &nbsp; 👎 &nbsp; ↻ &nbsp; 🔊</div></div>'
              '<div class="chips"><span class="chip">Explain step by step</span><span class="chip">Similar PYQ</span></div>',
         purpose="Make every answer actionable and keep a topic moving with one click.",
         example="After an answer, click “Give a similar PYQ”, or 🔊 to hear it read aloud, or ↻ to regenerate.",
         benefit="Curated, GATE-specific follow-ups keep you on-syllabus — instead of typing prompts from scratch as in a blank chat box.",
         how=["Use copy / 👍 / 👎 / regenerate / read-aloud under any answer.", "Click a follow-up chip to continue."],
         narration="Under every answer you get familiar controls — copy, like, dislike, regenerate and read-aloud — plus contextual follow-up chips. One click asks for a similar previous-year question or a step-by-step breakdown, keeping you on-syllabus instead of typing prompts from scratch.",
         title="Per-answer actions & follow-ups", sub="Copy · rate · regenerate · speak · follow-up"),

    dict(kind="feature", icon="📝", name="PYQ practice",
         mock='<div class="ubub">Solve a PYQ on TLB EAT</div>'
              '<div class="bub" style="margin-top:6px">Hit: <span class="math">110</span> · Miss: <span class="math">210</span><br>'
              'EAT = <span class="math">0.9·110+0.1·210 = 120 ns</span> ✅</div>',
         purpose="Practise with REAL previous-year questions and see them solved step by step.",
         example="“Give me a GATE PYQ on TLB effective access time” → the question, then the full worked solution.",
         benefit="General chatbots often invent fake ‘GATE questions’. Here the bank is real (CS, DA, ISRO, NIELIT, UGC-NET, TIFR) and ingested.",
         how=["Ask for a PYQ on any subject.", "Try it yourself, then read the step-by-step solution.", "Ask a follow-up to go deeper."],
         narration="It has ingested thousands of real previous-year questions across CS, DA, ISRO, NIELIT, UGC-NET and TIFR. Ask for one and it presents the question, then walks through the full solution. General chatbots tend to invent plausible-but-fake GATE questions — here the bank is real, so your practice reflects the actual exam.",
         title="Previous-year question practice", sub="Real PYQs, solved step by step"),

    dict(kind="feature", icon="🧪", name="Mock tests",
         mock='<div style="font-size:11px;color:#94a3b8;text-align:left">Q · MCQ · 2 marks</div>'
              '<div class="opt">A. Θ(n)</div><div class="opt ok">✓ Θ(n log n)</div>'
              '<div class="chips" style="margin-top:6px"><span class="chip red">7.3/10</span><span class="chip">96.4 pc</span></div>',
         purpose="Simulate the exam with MCQ/MSQ/NAT, scored exactly like GATE.",
         example="A 10-question mock returns 7.3/10 with −1/3 applied to wrong MCQs and an estimated 96th percentile.",
         benefit="No general chatbot scores you with GATE negative marking or estimates percentile — this turns study into measurable practice.",
         how=["Open Mock Test → choose exam, subject, difficulty, count.", "Answer against the timer; Submit.", "Review score, percentile, explanations & weak areas."],
         narration="The mock-test module generates exam-style questions, then scores them on the server with real GATE negative marking — minus one-third for a wrong one-mark question — and estimates your percentile. No general chatbot does this. It turns open-ended study into measurable practice. Pick your exam, subject and difficulty, answer against the timer, and review your score, explanations and weak areas.",
         title="Mock tests & GATE scoring", sub="MCQ/MSQ/NAT · negative marking · percentile"),

    dict(kind="feature", icon="🃏", name="Spaced repetition",
         mock='<div class="bub">Master Theorem case for T(n)=2T(n/2)+n?<hr style="border-color:rgba(255,255,255,.15);margin:6px 0">'
              'Case 2 → <b style="color:#fff">Θ(n log n)</b></div>'
              '<div class="grades"><span class="g">Again</span><span class="g">Hard</span><span class="g">Good</span><span class="g">Easy</span></div>',
         purpose="Make concepts stick using the SM-2 spaced-repetition algorithm.",
         example="Miss a question in a quiz → it becomes a flashcard, resurfacing just before you’d forget it.",
         benefit="ChatGPT has no memory of what you got wrong; this schedules YOUR weak cards at the optimal time to remember them.",
         how=["Open Flashcards → review due cards.", "Flip, then grade Again / Hard / Good / Easy.", "Generate a deck on any topic on demand."],
         narration="Missed questions automatically become flashcards, reviewed on an SM-2 spaced-repetition schedule so they resurface right before you'd forget them. A general chatbot has no memory of what you got wrong — this remembers your weak cards and schedules them at the optimal moment. Just review the due cards, grade your recall, and generate new decks on any topic.",
         title="Flashcards & spaced repetition", sub="SM-2 · wrong answers become cards"),

    dict(kind="feature", icon="🗓️", name="Study planner",
         mock='<div class="bub" style="text-align:left">Day 1 — Operating Systems<br>Day 2 — DBMS &amp; transactions<br>Day 3 — Algorithms (DP)</div>'
              '<div class="chips"><span class="chip red">⬇ Export .ics</span></div>',
         purpose="Turn a vague ‘I’ll study’ into a concrete, day-by-day plan to your exam date.",
         example="“30 days, 4 hours a day” → a schedule prioritising high-weight subjects with PYQs and revision built in.",
         benefit="A general chatbot can draft a plan once; here it’s saved, structured, and exportable straight to your calendar.",
         how=["Open Planner → set exam, date/days and hours/day.", "Click Build plan.", "Export to your calendar with one click (.ics)."],
         narration="The planner converts a vague intention into a concrete day-by-day schedule to your exam date, prioritising high-weight subjects with practice and revision built in. Unlike a one-off chatbot plan, this one is saved, structured, and exportable straight to your calendar as an ICS file.",
         title="Study planner", sub="Day-by-day plan → calendar export"),

    dict(kind="feature", icon="📊", name="Dashboard",
         mock='<div style="text-align:left;font-size:11px;color:#cbd5e1">Algorithms 88%<div class="bar"><span style="width:88%;background:#22c55e"></span></div>'
              'Networks 46%<div class="bar"><span style="width:46%;background:#ef4444"></span></div>'
              '<span style="color:#fbbf24">⚠ Readiness 78/100</span></div>',
         purpose="Show where you actually stand and what to fix next.",
         example="The dashboard reveals 88% in Algorithms but 46% in Networks → it tells you to prioritise Networks.",
         benefit="General chatbots keep no history; this aggregates every attempt into a readiness score, subject accuracy and weak-area alerts.",
         how=["Take a few quizzes first.", "Open Dashboard.", "Act on the readiness score and flagged weak areas."],
         narration="The dashboard turns your attempts into insight: an exam-readiness score, accuracy by subject, your streak, and automatic weak-area detection. Because general chatbots keep no history, they can't tell you where you stand — this does, so you always know exactly what to study next.",
         title="Performance dashboard", sub="Readiness · accuracy by subject · weak areas"),

    dict(kind="feature", icon="🔥", name="Daily question",
         mock='<div class="bub" style="text-align:left">Q of the day · dynamic programming<br><span style="color:#fbbf24">12🔥 streak</span></div>',
         purpose="Build a daily study habit — the real differentiator in long exam prep.",
         example="Each day a fresh question with a hint; solving it keeps your streak alive.",
         benefit="A streak and daily nudge create consistency that a general chatbot simply doesn’t encourage.",
         how=["Open Daily each day.", "Reveal the hint if stuck.", "Click “Solve with GO Buddy” to work it in chat."],
         narration="A question of the day, with a hint, builds the daily habit that ultimately cracks GATE. Solving it keeps your streak alive. It's a small nudge toward consistency that a general chatbot doesn't provide.",
         title="Daily question & streaks", sub="Habit-forming, one question a day"),

    dict(kind="feature", icon="📎", name="Attachments",
         mock='<div class="ubub">Solve the question in this image 🖼️</div>'
              '<div class="bub" style="margin-top:6px">K₄ has <span class="math">4² = 16</span> spanning trees ✅</div>',
         purpose="Answer from a screenshot, photo or PDF — no retyping.",
         example="Snap a photo of a tricky question; the vision model reads and solves it. Attach a PDF and ask about its contents.",
         benefit="It uses YOUR uploaded document as grounding context — a free chatbot can’t pull from your files natively.",
         how=["Click 📎 (or paste an image).", "Attach up to 4 files (≤ 8 MB).", "Ask your question about them."],
         narration="Stuck on a question in a screenshot or PDF? Attach it. The vision model reads images, and text is extracted from documents to use as context. You can even paste an image directly. It answers from your uploaded material — something a general chatbot can't do with your files natively.",
         title="Image & PDF attachments", sub="Vision + document understanding"),

    dict(kind="feature", icon="✏️", name="Sketch input",
         mock='<div class="bub" style="text-align:center">✏️ draw your diagram / working<br><span style="font-size:11px;color:#94a3b8">→ sent as an image</span></div>',
         purpose="Let you draw a diagram or working when typing maths is awkward.",
         example="Sketch a circuit or a tree and ask “is this correct?” — the model reads your drawing.",
         benefit="Bridges pen-and-paper study with the AI; general chat boxes have no canvas.",
         how=["Click the ✏️ pen icon in the composer.", "Draw, pick a colour.", "Click “Attach sketch” and ask."],
         narration="When typing maths or a diagram is awkward, just draw it. The sketch pad lets you draw your working or a diagram and sends it as an image the model can read — bridging pen-and-paper study with the AI. Click the pen icon, draw, and attach.",
         title="Sketch a question", sub="Draw diagrams & working"),

    dict(kind="feature", icon="🎙️", name="Voice in & out",
         mock='<div class="bub" style="text-align:center">🎙️ “Explain virtual memory”<br><span style="font-size:11px;color:#94a3b8">🔊 answer read aloud</span></div>',
         purpose="Study hands-free — ask by speaking and listen to answers.",
         example="Walking to class? Speak your question and have the explanation read back to you.",
         benefit="Accessibility and on-the-go revision that a text-only workflow can’t match.",
         how=["Click 🎙️ and speak your question.", "Click 🔊 on any answer to hear it.", "(Chrome, Edge, Safari.)"],
         narration="Study hands-free: click the microphone to ask by speaking, and the speaker icon to have any answer read aloud. It's great for revision on the go and for accessibility — and it works right in the browser.",
         title="Voice input & output", sub="Speak questions · listen to answers"),

    dict(kind="feature", icon="🌐", name="Multilingual",
         mock='<div class="bub" style="text-align:left">प्रश्न को हिंदी में समझाया गया<br><span style="font-size:11px;color:#94a3b8">terms/formulas stay standard</span></div>',
         purpose="Explain concepts in the language you think in.",
         example="Choose Hindi → explanations come in Hindi while formulas and code stay in standard form.",
         benefit="Tailored for Indian students; a single global model setting can’t mix language with GATE grounding like this.",
         how=["Pick a language from the dropdown above the chat.", "Ask normally — the explanation adapts."],
         narration="Choose your language — Hindi and other Indian languages are supported — and explanations come back in that language, while technical terms, formulas and code stay in their standard form. It's tailored for Indian students preparing for GATE.",
         title="Multilingual explanations", sub="Hindi & more, GATE-grounded"),

    dict(kind="feature", icon="💡", name="Socratic mode",
         mock='<div class="bub" style="text-align:left">Hint: what does the recurrence’s f(n) compare to?<br>'
              '<span style="font-size:11px;color:#94a3b8">full solution when you’re ready</span></div>',
         purpose="Build real understanding by giving hints before the full answer.",
         example="Ask a problem with Socratic mode on → you get a leading hint first, then the solution when you ask.",
         benefit="Default chatbots dump the answer; this trains you to think — the way a good mentor teaches.",
         how=["Toggle “Socratic” on above the chat.", "Try the hint first.", "Ask again to reveal the full solution."],
         narration="Socratic mode flips the usual behaviour: instead of dumping the answer, it gives a hint or a leading question first, and reveals the full solution only when you're ready. It trains you to think — the way a good mentor teaches — rather than handing you the answer every time.",
         title="Socratic tutor mode", sub="Hints first, solution when ready"),

    dict(kind="feature", icon="🛠️", name="Feedback → RLHF",
         mock='<div class="bub" style="text-align:left">👎 Incorrect → ↻ regenerated, improved<br>'
              '<span style="font-size:11px;color:#94a3b8">saved as a preference pair</span></div>',
         purpose="Let the assistant learn from your corrections over time.",
         example="Dislike a weak answer with a reason → regenerate gives a better one, and the pair is stored for training.",
         benefit="ChatGPT forgets your corrections; here they build an exportable dataset to fine-tune a better model (DPO/RLHF).",
         how=["👎 an answer and pick a reason / suggest a better answer.", "Click ↻ to regenerate, steered by feedback.", "Admins export the dataset as JSONL."],
         narration="This powers a real human-feedback loop. Dislike a weak answer with a reason, and regeneration produces a better one steered by your feedback. The correction is stored as a preference pair that can be exported to fine-tune an improved model with DPO. Unlike ChatGPT, which forgets your corrections, this system gets better from them.",
         title="Feedback & RLHF", sub="It learns from your corrections"),

    dict(kind="feature", icon="🛡️", name="Smart scope",
         mock='<div class="ubub">Hi</div><div class="bub" style="margin-top:6px">Hi! I\'m GO Buddy 👋 What shall we study?</div>',
         purpose="Handle greetings and off-topic asks gracefully — no junk answers.",
         example="“Hi” gets a friendly welcome; “tell me a joke” is politely declined and redirected to GATE.",
         benefit="Keeps the tool focused on the exam, instead of wandering off-syllabus like an open chatbot.",
         how=["Just chat naturally.", "Greetings get a warm reply; clearly off-topic asks are declined."],
         narration="Small touches matter. A greeting like 'hi' gets a friendly welcome instead of a junk retrieval-driven answer, and clearly off-topic questions are politely declined and redirected to GATE topics — keeping the tool focused on what helps you pass the exam.",
         title="Greeting & scope handling", sub="Focused, friendly, on-syllabus"),

    # getting started
    dict(kind="center", title="Getting started — in 4 steps", sub="There's an in-app guide too: tap the ? in the header anytime",
         narration="Getting started is easy, and there's an in-app guide built right in — tap the question-mark in the header anytime. First, open the app and read the welcome guide. Second, ask a question or try an example prompt. Third, take a quick quiz to seed your dashboard. Fourth, review your flashcards and follow the planner each day.",
         body=lambda n, t: shell('<div class="center"><div class="big-title" style="font-size:34px">Getting started</div>'
                                 '<div class="steps2">'
                                 '<div class="step"><span class="nx">1</span> Open the app — the in-app guide pops up (or tap “?”).</div>'
                                 '<div class="step"><span class="nx">2</span> Ask a question or click an example prompt.</div>'
                                 '<div class="step"><span class="nx">3</span> Take a quick quiz to seed your dashboard.</div>'
                                 '<div class="step"><span class="nx">4</span> Review flashcards &amp; follow your planner daily.</div>'
                                 '</div><div class="subtitle" style="margin-top:14px">Every screen has a help “?” — you’re never lost.</div></div>',
                                 "Getting started — in 4 steps", "In-app guide: tap “?” in the header", n, t)),

    # outro
    dict(kind="center", title="Thank you", sub="GateOverflow Chatbot · gateoverflow.in",
         narration="That's the complete feature guide. Every capability is built to make GATE preparation more effective, measurable and trustworthy than a general chatbot. Thanks for watching — and happy studying!",
         body=lambda n, t: shell(f'<div class="center">{LOGO_BIG}<div class="big-title" style="font-size:34px">Now you know every feature</div>'
                                 '<div class="subtitle">Grounded answers · PYQs &amp; mock tests · spaced repetition · planner · dashboard · voice, sketch &amp; multilingual · feedback that learns.</div>'
                                 '<div class="chips"><span class="chip red">Tap “?” in-app for this guide anytime</span></div></div>',
                                 "Thank you", "GateOverflow Chatbot · gateoverflow.in", n, t)),
]


def build_scenes():
    total = len(_RAW)
    scenes = []
    for i, raw in enumerate(_RAW, 1):
        if raw["kind"] == "center":
            body = raw["body"](i, total)
        else:
            f = feature(i, total, icon=raw["icon"], name=raw["name"], mock=raw["mock"],
                        purpose=raw["purpose"], example=raw["example"], benefit=raw["benefit"],
                        how=raw["how"], narration=raw["narration"], title=raw["title"], sub=raw["sub"])
            body = f["body"]
        scenes.append(dict(key=f"{i:02d}", body=body, narration=raw["narration"]))
    return scenes


# --------------------------------------------------------------------------- #
def sh(cmd): return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
def duration(p): return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).strip())


def main() -> int:
    if not Path(CHROME).exists():
        print("❌ Chrome not found"); return 1
    for t in ("ffmpeg", "say", "ffprobe"):
        if shutil.which(t) is None:
            print(f"❌ {t} not found"); return 1

    if FRAMES.exists():
        shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True)

    scenes = build_scenes()
    total = len(scenes)
    segments = []
    for i, sc in enumerate(scenes, 1):
        stem = f"{sc['key']}"
        html, png = FRAMES / f"{stem}.html", FRAMES / f"{stem}.png"
        aiff, seg = FRAMES / f"{stem}.aiff", FRAMES / f"{stem}.mp4"
        html.write_text(sc["body"], encoding="utf-8")
        print(f"🎬 {i}/{total} rendering")
        sh([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=2", f"--window-size={W},{H}",
            f"--screenshot={png}", f"file://{html}", "--virtual-time-budget=2500"])
        sh(["say", "-v", VOICE, "-o", str(aiff), sc["narration"]])
        dur = max(duration(aiff) + 1.0, 5.0)
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
