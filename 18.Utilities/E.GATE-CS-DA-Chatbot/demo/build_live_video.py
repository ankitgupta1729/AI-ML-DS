#!/usr/bin/env python3
"""Build the DETAILED feature-guide video from REAL screenshots of the running
app (captured in demo/live/). Each scene shows the live UI in a browser frame
with a caption, while the narration explains the feature's purpose, an example,
its benefit vs ChatGPT/Claude/DeepSeek, and how to use it.

Output: demo/GateOverflow-Chatbot-Feature-Guide.mp4
Requires: Google Chrome, ffmpeg, ffprobe, `say` (macOS).
"""

from __future__ import annotations

import base64
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIVE = ROOT / "live"
FRAMES = ROOT / "frames_live"
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
body{font-family:'Inter',system-ui,-apple-system,sans-serif}
.app{position:relative;width:1280px;height:720px;overflow:hidden;background:linear-gradient(180deg,#020617,#0b1220)}
.glow{position:absolute;border-radius:9999px;filter:blur(80px)}
.glow.a{top:-130px;left:50%;transform:translateX(-50%);width:680px;height:240px;background:rgba(220,38,38,.16)}
.glow.b{bottom:30px;right:-40px;width:280px;height:280px;background:rgba(225,29,72,.12)}
.watermark{position:absolute;top:13px;right:24px;font-size:11px;color:#475569}
.kicker{position:absolute;top:14px;left:28px;font-size:12px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;color:#f87171}
/* browser frame holding the real screenshot */
.stage{position:absolute;top:46px;left:0;right:0;display:flex;justify-content:center}
.win{width:1008px;border-radius:14px;overflow:hidden;border:1px solid rgba(255,255,255,.14);
  box-shadow:0 30px 70px rgba(0,0,0,.55);background:#0b1220}
.bar{height:26px;background:#0f172a;display:flex;align-items:center;gap:6px;padding:0 12px;border-bottom:1px solid rgba(255,255,255,.08)}
.bar i{width:9px;height:9px;border-radius:50%;background:#334155;display:block}
.bar .url{margin-left:10px;font-size:10px;color:#64748b}
.win img{display:block;width:100%}
/* how-to chip */
.howto{position:absolute;left:28px;bottom:104px;max-width:560px;background:rgba(2,6,23,.7);
  border:1px solid rgba(220,38,38,.35);border-radius:12px;padding:8px 13px;font-size:13px;color:#fecaca;backdrop-filter:blur(4px)}
.howto b{color:#fff}
/* center scenes */
.center{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:14px;padding:0 70px}
.badge{display:grid;place-items:center;width:104px;height:104px;border-radius:28px;background:#1e293b;border:1px solid rgba(255,255,255,.1)}
.big{font-size:42px;font-weight:900;background:linear-gradient(90deg,#f87171,#e11d48);-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{font-size:18px;color:#94a3b8;max-width:760px}
.chips{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:4px}
.chip{font-size:12px;border:1px solid rgba(220,38,38,.4);color:#fca5a5;border-radius:9999px;padding:5px 12px}
.steps{display:grid;grid-template-columns:1fr 1fr;gap:10px 24px;text-align:left;margin-top:6px}
.st{display:flex;gap:9px;font-size:15px;color:#e2e8f0}.st .n{color:#f87171;font-weight:800}
/* caption */
.caption{position:absolute;left:0;right:0;bottom:0;height:92px;background:linear-gradient(180deg,rgba(2,6,23,0),rgba(2,6,23,.94));display:flex;align-items:center;gap:14px;padding:0 28px 14px}
.cbar{width:5px;height:46px;border-radius:9999px;background:linear-gradient(#dc2626,#e11d48)}
.ctitle{font-size:20px;font-weight:800;color:#fff}.csub{font-size:13px;color:#cbd5e1;margin-top:2px}
.counter{margin-left:auto;font-size:12px;color:#64748b}
"""


def _img(name: str) -> str:
    data = base64.b64encode((LIVE / name).read_bytes()).decode()
    return f"data:image/png;base64,{data}"


def page(inner, title, sub, n, total, kicker=""):
    k = f'<div class="kicker">{kicker}</div>' if kicker else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div class="app"><div class="glow a"></div><div class="glow b"></div>
<div class="watermark">gateoverflow.in · live app</div>{k}{inner}
<div class="caption"><div class="cbar"></div><div><div class="ctitle">{title}</div>
<div class="csub">{sub}</div></div><div class="counter">{n} / {total}</div></div>
</div></body></html>"""


def shot_scene(n, total, *, img, kicker, title, sub, howto):
    inner = (f'<div class="stage"><div class="win"><div class="bar"><i></i><i></i><i></i>'
             f'<span class="url">localhost:5173 — GateOverflow Chatbot</span></div>'
             f'<img src="{_img(img)}"></div></div>'
             f'<div class="howto"><b>How to use:</b> {howto}</div>')
    return page(inner, title, sub, n, total, kicker)


LOGO_BIG = f'<div class="badge">{GO_LOGO.format(s=78, go="#fff")}</div>'

# (kind, ...) scene definitions
RAW = [
    dict(kind="center", title="GateOverflow Chatbot — Feature Guide", sub="A detailed tour of the live app",
         narration="Welcome to the detailed feature guide for the GateOverflow Chatbot. Everything you'll see here is the real, running application. For each feature we'll explain its purpose, show an example, why it's better than a general chatbot like ChatGPT or Claude, and exactly how to use it.",
         body=lambda n, t: page(f'<div class="center">{LOGO_BIG}<div class="big">Feature Guide</div>'
                                '<div class="sub">Real screenshots of the running app — purpose, examples, benefits and how to use every feature.</div>'
                                '<div class="chips"><span class="chip">Grounded answers</span><span class="chip">Mock tests</span>'
                                '<span class="chip">Spaced repetition</span><span class="chip">Planner &amp; analytics</span></div></div>',
                                "GateOverflow Chatbot — Feature Guide", "Everything shown is the live app", n, t)),

    dict(kind="shot", img="01_guide.png", kicker="Onboarding",
         title="Built-in guide", sub="Never get lost — guidance lives in the app",
         howto="It opens on first visit; reopen anytime via the “?” in the header.",
         narration="The very first thing a new user sees is a built-in guide. It explains every feature — what it's for and how to use it — and it opens automatically on the first visit. You can reopen it any time from the question-mark button in the header. Unlike a blank chat box, the app teaches you how to use it from the start."),

    dict(kind="shot", img="02_welcome.png", kicker="Workspace",
         title="One focused study workspace", sub="Sidebar: Chat · Mock Test · Flashcards · Planner · Dashboard · Daily",
         howto="Use the left sidebar to switch modules; click an example prompt to begin.",
         narration="This is the workspace. A sidebar on the left gives you six purpose-built modules — chat, mock tests, flashcards, a planner, a dashboard and a daily question. The composer at the bottom has a language selector, a Socratic toggle, and buttons to attach files, sketch, or speak. Just click an example prompt to start, or type your own question."),

    dict(kind="shot", img="03_chat.png", kicker="Feature · Chat",
         title="Grounded answers, LaTeX & confidence", sub="Streamed, formatted, with a grounding meter and quick actions",
         howto="Type a question and press Enter; rate, regenerate or read aloud the answer.",
         narration="The heart of the app is grounded chat. Here we asked about the time complexity of merge sort. The answer streams in with properly rendered mathematics and a clear conclusion. Below it, a grounding-confidence meter shows how strongly the answer is backed by your indexed material — a transparency feature ChatGPT and Claude don't offer. Each answer has copy, like, dislike, regenerate and read-aloud actions, plus one-click follow-up suggestions. To use it, just type a question and press Enter."),

    dict(kind="shot", img="04_sources.png", kicker="Feature · Trust",
         title="Citations you can verify", sub="Real source files, pages and match scores",
         howto="Click “sources” under any answer to see the exact files and pages used.",
         narration="Expand the sources panel and you see exactly where the answer came from — real previous-year-question PDFs, with page references and a match score for each. This is the biggest difference from general chatbots: instead of an unverifiable claim, every answer is traceable to your material, so you can trust it for the exam."),

    dict(kind="shot", img="18_pyq_links.png", kicker="Feature · GateOverflow",
         title="Direct GateOverflow question links", sub="For PYQ answers — open the exact thread & community answers",
         howto="On a previous-year-question answer, click a link under “See this question on GateOverflow”.",
         narration="When the answer is a previous-year question, you get something unique: a direct link to that exact question on GateOverflow — extracted from the URLs embedded in the question PDFs. One click opens the official thread with the community's discussion and answers. These links appear only for previous-year questions, never for general ones."),

    dict(kind="shot", img="21_site_aware.png", kicker="Feature · GateOverflow",
         title="Knows the GateOverflow platform", sub="Ask how to use the site itself — not just the syllabus",
         howto="Ask things like “How do I find PYQs / use search / read the PDFs on GateOverflow?”",
         narration="The assistant also knows the GateOverflow website itself. Ask how to use the platform and it explains where to find previous-year questions, how to browse by subject or exam, the advanced search syntax, the online PDF Book Viewer, the rank predictor, badges and how to ask a question. So while you study, you also learn to get the most out of GateOverflow — something a general chatbot has no idea about."),

    dict(kind="shot", img="05_mock_config.png", kicker="Feature · Practice",
         title="Mock Test & Practice", sub="Choose exam, subject, difficulty and length",
         howto="Open Mock Test, pick your settings, and click Start.",
         narration="The Mock Test module turns study into measurable practice. You choose the exam, a subject, the difficulty and how many questions, and whether it's a quick quiz or a full mock. No general chatbot offers structured, exam-style testing like this. Open Mock Test, pick your settings, and click Start."),

    dict(kind="shot", img="06_mock_questions.png", kicker="Feature · Practice",
         title="Exam-style questions", sub="MCQ, MSQ and NAT — generated live, with a timer",
         howto="Answer each question; the timer runs; click Submit when done.",
         narration="It then generates real exam-style questions — multiple choice, multiple-select, and numerical-answer types — grounded in actual previous-year questions, with a timer running just like the real exam. You answer each one and submit when ready."),

    dict(kind="shot", img="07_mock_result.png", kicker="Feature · Practice",
         title="Scored with GATE rules", sub="Negative marking · percentile · per-question explanations",
         howto="Review your score, percentile and the explanation for every question.",
         narration="When you submit, it's scored on the server with real GATE negative marking and gives you an estimated percentile — here, a perfect seven out of seven at the ninety-ninth percentile. Every question comes with an explanation, and any you got wrong automatically become flashcards. This measurable feedback loop is something a general chatbot simply can't provide."),

    dict(kind="shot", img="17_flashcard_review.png", kicker="Feature · Revision",
         title="Flashcards & SM-2 scheduling", sub="Grade your recall; the algorithm picks the next review date",
         howto="Flip a card, then grade it: Again · Hard · Good · Easy.",
         narration="Flashcards use the proven SM-2 spaced-repetition algorithm. Flip a card and grade your recall with one of four buttons. SM-2 then schedules the next review: tap “Again” and the card comes back tomorrow; tap “Good” or “Easy” and it pushes the next review further out — a few days, then weeks — as an ease factor grows. So material you know well appears rarely, while what you struggle with returns soon. Wrong quiz answers land here automatically, and you can generate a deck on any topic."),

    dict(kind="shot", img="10_planner.png", kicker="Feature · Planning",
         title="Study planner", sub="Day-by-day plan to your exam date · export to calendar",
         howto="Set your exam date and hours/day, click Build plan, then export the .ics.",
         narration="The planner builds a concrete, day-by-day schedule to your exam date, prioritising high-weight subjects with previous-year practice and revision built in. You can export the whole plan to your calendar as an ICS file. It turns a vague intention to study into an actionable schedule."),

    dict(kind="shot", img="08_dashboard.png", kicker="Feature · Insight",
         title="Performance dashboard", sub="Readiness score · accuracy by subject · weak areas",
         howto="Take a few quizzes, then open Dashboard to see where to focus.",
         narration="The dashboard turns your attempts into insight: an exam-readiness score, accuracy broken down by subject, your streak, and automatic weak-area detection. Because general chatbots keep no history, they can't tell you where you stand — this does, so you always know what to study next."),

    dict(kind="shot", img="11_daily.png", kicker="Feature · Habit",
         title="Daily question & streaks", sub="One question a day keeps the momentum",
         howto="Open Daily, try the question, reveal the hint, or solve it in chat.",
         narration="A daily question, with a hint, builds the consistent habit that ultimately cracks GATE, and a streak keeps you coming back. Open it each day, attempt the question, and click Solve with GO Buddy to work through it in chat."),

    dict(kind="shot", img="02_welcome.png", kicker="Feature · Multimodal",
         title="Voice & attachments", sub="Speak, listen, or attach images and PDFs",
         howto="Use 🎙️ to speak, 🔊 to listen, and 📎 to attach images/PDFs.",
         narration="Look at the composer. The microphone lets you ask by speaking and have answers read aloud — perfect for revision on the go. The paperclip attaches images and PDFs, which the vision model reads. These input options go far beyond a plain text box."),

    dict(kind="shot", img="12_sketch.png", kicker="Feature · Multimodal",
         title="Sketch a question or your working", sub="Draw a diagram; the vision model reads it",
         howto="Click the ✏️ pen, draw on the canvas, then “Attach sketch” and ask.",
         narration="When typing maths or a diagram is awkward, just draw it. The sketch pad lets you draw a figure or your working — here, a triangle — choose a pen colour, and attach it as an image the model can read. It bridges pen-and-paper study with the AI, something a plain chat box can't do."),

    dict(kind="shot", img="13_hindi.png", kicker="Feature · Multilingual",
         title="Explanations in your language", sub="Hindi & more — terms and formulas stay standard",
         howto="Pick a language from the dropdown above the chat, then ask normally.",
         narration="Choose your language from the dropdown and the explanation comes back in it — here, a full answer on dynamic programming in Hindi, while technical terms, code and formulas stay in their standard form. It's tailored for Indian students, and no global chatbot setting blends your language with this GATE-grounded material the same way."),

    dict(kind="shot", img="16_socratic.png", kicker="Feature · Tutoring",
         title="Socratic tutor mode (on / off)", sub="Hints first — builds real understanding",
         howto="Toggle “Socratic” above the chat; ask, attempt the hint, then ask for the full solution.",
         narration="Toggle Socratic mode on, above the chat, and the tutor changes how it answers. Instead of dumping the solution, it gives you guiding hints and a leading question — here, nudging you to think about how many times binary search halves the array — and waits for you to attempt the next step. Ask again, or say you're stuck, and it reveals the full worked solution. Turn it off for direct answers. It's the difference between being handed an answer and actually learning."),

    dict(kind="shot", img="14_feedback.png", kicker="Feature · Improvement",
         title="Feedback that trains the assistant", sub="Dislike → reason → optional correction (RLHF)",
         howto="👎 an answer, pick a reason, optionally suggest a better answer, and submit.",
         narration="Now the feedback loop. Dislike an answer and a quick form opens — pick a reason like incomplete or incorrect, add a comment, even suggest a better answer. Each correction is stored as a preference pair that can be exported to fine-tune an improved model with reinforcement learning from human feedback."),

    dict(kind="shot", img="15_regenerate.png", kicker="Feature · Improvement",
         title="Regenerated — steered by your feedback", sub="A better, more complete answer",
         howto="Click ↻ regenerate; the new answer addresses your feedback.",
         narration="Click regenerate and the assistant rewrites the answer, steered by your feedback — here it returns a more complete explanation with the base case, tabulation and time complexity. Unlike ChatGPT, which forgets your corrections, this system actually improves from them."),

    dict(kind="shot", img="20_history.png", kicker="Feature · Productivity",
         title="Bookmarks & chat history", sub="Save answers; revisit past conversations",
         howto="Tap ★ on any answer to save it; open the 🕑 history panel to revisit.",
         narration="Found a great explanation? Tap the star to save it. The history panel in the header keeps all your past conversations and saved answers in one place — open any one to pick up exactly where you left off. Nothing you learn gets lost."),

    dict(kind="shot", img="19_cheatsheet.png", kicker="Feature · Productivity",
         title="Cheat-sheet & PDF export", sub="Turn a chat into a revision sheet — then print or save as PDF",
         howto="Click “Cheat sheet” to build one, or “Export PDF” for the whole chat.",
         narration="With one click, turn a whole conversation into a concise revision cheat-sheet — the key formulas, definitions and pitfalls, with proper maths. Print it or save it as a PDF for last-minute revision, or export the entire conversation. Your study sessions become take-away study material."),

    dict(kind="center", title="Getting started — in 4 steps", sub="Tap the “?” in the header for this guide anytime",
         narration="To get started: first, open the app and read the welcome guide. Second, ask a question or click an example prompt. Third, take a quick quiz to seed your dashboard. And fourth, review your flashcards and follow your planner every day. The in-app guide is always a tap away on the question-mark button.",
         body=lambda n, t: page('<div class="center"><div class="big" style="font-size:34px">Getting started</div>'
                                '<div class="steps">'
                                '<div class="st"><span class="n">1</span> Open the app — read the welcome guide.</div>'
                                '<div class="st"><span class="n">2</span> Ask a question or click an example.</div>'
                                '<div class="st"><span class="n">3</span> Take a quick quiz to seed your dashboard.</div>'
                                '<div class="st"><span class="n">4</span> Review flashcards &amp; follow your planner daily.</div>'
                                '</div><div class="sub" style="margin-top:12px">Help is always one tap away — the “?” in the header.</div></div>',
                                "Getting started — in 4 steps", "In-app guide: tap “?” anytime", n, t)),

    dict(kind="center", title="Thank you", sub="GateOverflow Chatbot · gateoverflow.in",
         narration="That's the complete feature guide, shown entirely in the live application. Every capability is built to make GATE preparation more effective, measurable and trustworthy than a general chatbot. Thanks for watching, and happy studying!",
         body=lambda n, t: page(f'<div class="center">{LOGO_BIG}<div class="big" style="font-size:34px">Now you know every feature</div>'
                                '<div class="sub">Grounded answers · PYQs &amp; mock tests · spaced repetition · planner · dashboard · voice, sketch &amp; multilingual · feedback that learns.</div>'
                                '<div class="chips"><span class="chip">Built for GateOverflow · gateoverflow.in</span></div></div>',
                                "Thank you", "GateOverflow Chatbot · gateoverflow.in", n, t)),
]


def sh(cmd): return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
def duration(p): return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).strip())


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
            html_str = sc["body"](i, total)
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
