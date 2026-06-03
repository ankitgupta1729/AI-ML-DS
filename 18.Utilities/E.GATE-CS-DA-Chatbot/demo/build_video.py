#!/usr/bin/env python3
"""Build a narrated demo video for the GateOverflow Chatbot — fully offline.

Pipeline (macOS):
  1. Render each "scene" (HTML mock of the real UI) to a PNG with headless Chrome.
  2. Generate narration for each scene with the `say` command.
  3. Assemble per-scene clips (image + narration, padded to the audio length)
     and concatenate them into demo/GateOverflow-Chatbot-Demo.mp4 with ffmpeg.

Run:  python demo/build_video.py
Requires: Google Chrome, ffmpeg, ffprobe, `say` (all standard on macOS).
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FRAMES = ROOT / "frames"
OUT = ROOT / "GateOverflow-Chatbot-Demo.mp4"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
VOICE = "Samantha"
W, H = 1280, 720

# --------------------------------------------------------------------------- #
# Shared styling + components                                                 #
# --------------------------------------------------------------------------- #
GO_LOGO = """
<svg viewBox="0 0 100 100" width="{s}" height="{s}" style="display:block">
  <text x="60" y="50" text-anchor="middle" font-family="Georgia,serif"
        font-size="74" font-weight="700" fill="#dc2626"
        transform="rotate(9 60 44)">?</text>
  <text x="49" y="86" text-anchor="middle" font-family="Arial,sans-serif"
        font-size="50" font-weight="900" fill="{go}" letter-spacing="-2">GO</text>
</svg>
"""

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;
  background:#020617}
.app{position:relative;width:1280px;height:720px;overflow:hidden;
  background:linear-gradient(180deg,#020617,#0b1220)}
.glow{position:absolute;border-radius:9999px;filter:blur(80px);pointer-events:none}
.glow.a{top:-120px;left:50%;transform:translateX(-50%);width:640px;height:240px;
  background:rgba(220,38,38,.18)}
.glow.b{bottom:60px;right:-40px;width:280px;height:280px;background:rgba(225,29,72,.14)}
.header{position:relative;display:flex;align-items:center;gap:12px;
  padding:12px 24px;border-bottom:1px solid rgba(255,255,255,.08);
  background:rgba(2,6,23,.6)}
.badge{display:grid;place-items:center;width:42px;height:42px;border-radius:14px;
  background:#1e293b;border:1px solid rgba(255,255,255,.1)}
.h-title{font-size:18px;font-weight:800;color:#fff;display:flex;align-items:center;gap:8px}
.tag{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;
  color:#f87171;background:rgba(220,38,38,.15);padding:2px 8px;border-radius:9999px}
.h-sub{font-size:12px;color:#94a3b8}
.status{margin-left:auto;display:flex;align-items:center;gap:6px;font-size:12px;
  color:#cbd5e1;border:1px solid rgba(255,255,255,.1);padding:5px 10px;border-radius:9999px}
.dot{width:8px;height:8px;border-radius:9999px;background:#22c55e}
.main{position:relative;height:578px;padding:22px 26px 0;overflow:hidden}
.row{display:flex;gap:12px;margin-bottom:18px;animation:up .5s ease both}
.row.user{justify-content:flex-end}
.ubub{max-width:74%;background:linear-gradient(135deg,#dc2626,#b91c1c);color:#fff;
  padding:11px 15px;border-radius:18px 18px 4px 18px;font-size:15px;line-height:1.5;
  box-shadow:0 8px 24px rgba(220,38,38,.25)}
.avatar{flex:0 0 auto;width:34px;height:34px;border-radius:11px;background:#1e293b;
  border:1px solid rgba(255,255,255,.1);display:grid;place-items:center}
.bbub{max-width:80%;background:rgba(15,23,42,.7);border:1px solid rgba(255,255,255,.1);
  color:#e2e8f0;padding:13px 17px;border-radius:18px 18px 18px 4px;font-size:14.5px;
  line-height:1.62}
.bbub h4{color:#fff;font-size:15px;margin:2px 0 6px}
.bbub p{margin:6px 0}
.bbub b{color:#fff}
.math{font-family:'Times New Roman',Georgia,serif;font-style:italic;
  background:rgba(220,38,38,.14);padding:1px 7px;border-radius:6px;color:#fecaca}
.li{margin:4px 0 4px 4px;display:flex;gap:8px}.li::before{content:'•';color:#f87171}
.src{margin-top:10px;border:1px solid rgba(255,255,255,.1);border-radius:12px;
  background:rgba(2,6,23,.5);padding:8px 11px;font-size:12px;color:#cbd5e1}
.src .name{color:#fff;font-weight:600}
.pill{display:inline-block;font-size:10px;font-weight:600;padding:2px 8px;border-radius:9999px}
.pill.subj{background:rgba(220,38,38,.15);color:#f87171}
.pill.match{background:rgba(34,197,94,.15);color:#4ade80;margin-left:6px}
.actions{display:flex;gap:6px;margin-top:10px}
.act{width:30px;height:30px;border-radius:9px;display:grid;place-items:center;
  color:#94a3b8;border:1px solid rgba(255,255,255,.08)}
.act.on{color:#f87171;background:rgba(220,38,38,.15);border-color:rgba(220,38,38,.3)}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.chip{font-size:12px;color:#cbd5e1;border:1px solid rgba(255,255,255,.12);
  background:rgba(15,23,42,.6);padding:6px 12px;border-radius:9999px}
.chip.red{border-color:rgba(220,38,38,.4);color:#fca5a5}
.composer{position:absolute;left:26px;right:26px;bottom:104px;display:flex;
  align-items:center;gap:10px;border:1px solid rgba(255,255,255,.12);
  background:rgba(15,23,42,.85);border-radius:16px;padding:10px 12px}
.composer .ph{flex:1;color:#64748b;font-size:14px}
.send{width:38px;height:38px;border-radius:11px;display:grid;place-items:center;
  background:linear-gradient(135deg,#dc2626,#e11d48);color:#fff;font-weight:700}
.clip{width:30px;height:30px;border-radius:9px;display:grid;place-items:center;color:#94a3b8}
.thumb{width:120px;height:84px;border-radius:12px;border:1px solid rgba(255,255,255,.15);
  background:linear-gradient(135deg,#334155,#1e293b);display:grid;place-items:center;
  color:#cbd5e1;font-size:11px;text-align:center;padding:6px}
.feedback{margin-top:10px;border:1px solid rgba(255,255,255,.1);border-radius:12px;
  background:rgba(2,6,23,.5);padding:11px}
.feedback .q{font-size:12px;color:#cbd5e1;font-weight:600;margin-bottom:8px}
.rchip{display:inline-block;font-size:11px;color:#cbd5e1;border:1px solid rgba(255,255,255,.15);
  padding:4px 10px;border-radius:9999px;margin:0 6px 6px 0}
.rchip.on{border-color:#dc2626;background:rgba(220,38,38,.12);color:#fca5a5}

/* welcome / center scenes */
.center{height:100%;display:flex;flex-direction:column;align-items:center;
  justify-content:center;text-align:center;gap:14px;padding:0 60px}
.big-title{font-size:46px;font-weight:900;
  background:linear-gradient(90deg,#f87171,#e11d48);-webkit-background-clip:text;
  background-clip:text;color:transparent}
.subtitle{font-size:18px;color:#94a3b8;max-width:640px}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;width:100%;margin-top:8px}
.card{border:1px solid rgba(255,255,255,.1);background:rgba(15,23,42,.55);
  border-radius:16px;padding:16px;text-align:left}
.card .k{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;
  color:#f87171;margin-bottom:6px}
.card .v{font-size:13.5px;color:#cbd5e1;line-height:1.5}
.checklist{display:grid;grid-template-columns:1fr 1fr;gap:10px 26px;text-align:left;
  margin-top:8px}
.check{font-size:15px;color:#e2e8f0;display:flex;gap:10px;align-items:center}
.check .tick{color:#4ade80;font-weight:800}

/* architecture */
.arch{display:flex;align-items:center;justify-content:center;gap:18px;margin-top:18px;flex-wrap:wrap}
.node{border:1px solid rgba(255,255,255,.14);background:rgba(15,23,42,.6);border-radius:14px;
  padding:14px 16px;min-width:150px;text-align:center}
.node .t{font-weight:800;color:#fff;font-size:14px}
.node .d{font-size:11.5px;color:#94a3b8;margin-top:4px}
.node.red{border-color:rgba(220,38,38,.45)}
.arrow{color:#f87171;font-size:24px;font-weight:800}

/* caption lower-third */
.caption{position:absolute;left:0;right:0;bottom:0;height:92px;
  background:linear-gradient(180deg,rgba(2,6,23,0),rgba(2,6,23,.92));
  display:flex;align-items:center;gap:14px;padding:0 26px 14px}
.cbar{width:5px;height:48px;border-radius:9999px;background:linear-gradient(#dc2626,#e11d48)}
.ctitle{font-size:20px;font-weight:800;color:#fff}
.csub{font-size:13px;color:#cbd5e1;margin-top:2px}
.counter{margin-left:auto;font-size:12px;color:#64748b}
.watermark{position:absolute;top:12px;right:24px;font-size:11px;color:#475569}
@keyframes up{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
"""

HEADER = """
<div class="header">
  <div class="badge">{logo}</div>
  <div>
    <div class="h-title">GateOverflow Chatbot <span class="tag">GATE CS · DA</span></div>
    <div class="h-sub">Your AI study buddy for GATE CS &amp; DA — grounded in real PYQs.</div>
  </div>
  <div class="status"><span class="dot"></span> 18,420 chunks · gpt-4o-mini</div>
</div>
""".format(logo=GO_LOGO.format(s=30, go="#fff"))


def page(body: str, title: str, sub: str, n: int, total: int, center: bool = False) -> str:
    inner = body if center else (HEADER + f'<div class="main">{body}</div>')
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head>
<body><div class="app">
  <div class="glow a"></div><div class="glow b"></div>
  <div class="watermark">gateoverflow.in</div>
  {inner}
  <div class="caption"><div class="cbar"></div>
    <div><div class="ctitle">{title}</div><div class="csub">{sub}</div></div>
    <div class="counter">{n} / {total}</div>
  </div>
</div></body></html>"""


def bot(inner: str) -> str:
    return f'<div class="row bot"><div class="avatar">{GO_LOGO.format(s=24, go="#fff")}</div><div class="bbub">{inner}</div></div>'


def user(text: str, extra: str = "") -> str:
    return f'<div class="row user">{extra}<div class="ubub">{text}</div></div>'


# --------------------------------------------------------------------------- #
# Scenes                                                                      #
# --------------------------------------------------------------------------- #
LOGO_BIG = f'<div class="badge" style="width:104px;height:104px;border-radius:28px">{GO_LOGO.format(s=78, go="#fff")}</div>'

SCENES = [
    dict(
        key="intro", center=True, min=4.5,
        title="GateOverflow Chatbot", sub="Product demo",
        narration="Meet the GateOverflow Chatbot — an AI study buddy for the GATE Computer Science and Data Science and AI exams, grounded in real previous-year questions.",
        body=f'<div class="center">{LOGO_BIG}<div class="big-title">GateOverflow Chatbot</div>'
             f'<div class="subtitle">Your AI study buddy for GATE CS &amp; DA — grounded in real previous-year questions.</div>'
             f'<div class="chips" style="justify-content:center"><span class="chip red">RAG over your material</span>'
             f'<span class="chip red">Streaming answers</span><span class="chip red">PYQ practice</span>'
             f'<span class="chip red">Feedback &amp; RLHF</span></div></div>',
    ),
    dict(
        key="welcome", min=4.0,
        title="A clean, focused workspace", sub="Example prompts get you started instantly",
        narration="It opens to a clean welcome screen with one-click example prompts — explain a concept, practise a previous-year question, quiz yourself, or plan your strategy.",
        body='<div class="grid">'
             '<div class="card"><div class="k">📝 PYQ practice</div><div class="v">Give me a GATE CS PYQ on operating systems and explain it step by step.</div></div>'
             '<div class="card"><div class="k">📝 PYQ — DA</div><div class="v">Ask me a GATE DA question on probability and wait for my answer.</div></div>'
             '<div class="card"><div class="k">🧠 Quiz me</div><div class="v">Quiz me with 5 mixed GATE CS MCQs, one at a time, then score me.</div></div>'
             '<div class="card"><div class="k">Explain a concept</div><div class="v">Explain conflict serializability with a precedence-graph example.</div></div>'
             '<div class="card"><div class="k">ML / AI</div><div class="v">Derive the bias–variance trade-off and how regularisation helps.</div></div>'
             '<div class="card"><div class="k">Strategy</div><div class="v">How should I plan my last 30 days of GATE DA prep?</div></div>'
             '</div>'
             '<div class="composer"><span class="clip">📎</span><span class="ph">Ask anything about GATE CS / DA — or attach a question image / PDF…</span><span class="send">➤</span></div>',
    ),
    dict(
        key="answer", min=5.5,
        title="Ask anything — grounded answers", sub="Markdown, LaTeX maths and citations, streamed token-by-token",
        narration="Ask any question across the syllabus. Answers stream in live, formatted with proper maths and code, and grounded in your study material.",
        body=user("Explain the time complexity of merge sort and why.")
             + bot('<h4>Merge sort — <span class="math">O(n&nbsp;log&nbsp;n)</span></h4>'
                   '<p>Merge sort splits the array in half each time and merges the sorted halves:</p>'
                   '<div class="li">Recurrence: <span class="math">T(n) = 2T(n/2) + O(n)</span></div>'
                   '<div class="li">By the Master Theorem this solves to <span class="math">Θ(n&nbsp;log&nbsp;n)</span></div>'
                   '<div class="li">The <span class="math">log&nbsp;n</span> levels each do <span class="math">O(n)</span> merge work.</div>'
                   '<p>It is stable and <b>worst-case</b> <span class="math">O(n&nbsp;log&nbsp;n)</span>, unlike quicksort.</p>'
                   '<div class="src">📄 <span class="name">cs_core_concepts.md</span> '
                   '<span class="pill subj">computer_science</span><span class="pill match">91% match</span></div>'),
    ),
    dict(
        key="sources", min=4.5,
        title="Every answer cites its sources", sub="Expandable source cards with file, location and match score",
        narration="Each answer can show exactly where it came from — the source file, the page, and a relevance score — so you can trust and verify it.",
        body=bot('<h4>Sources used for this answer</h4>'
                 '<div class="src">📄 <span class="name">dive_into_deep_learning.pdf</span> · p. 142 '
                 '<span class="pill subj">data_science_ai</span><span class="pill match">88% match</span><br>'
                 '<span style="color:#94a3b8">…the convolution operation slides a kernel across the input, sharing weights to detect local patterns…</span></div>'
                 '<div class="src">📄 <span class="name">filter1_volume2.pdf</span> · p. 57 '
                 '<span class="pill subj">GATA-Data</span><span class="pill match">84% match</span><br>'
                 '<span style="color:#94a3b8">GATE 2021 CS: A 3×3 kernel with stride 1 and no padding applied to a 7×7 image…</span></div>')
             + '<div class="chips"><span class="chip">Explain step by step</span><span class="chip">Give a similar PYQ</span><span class="chip">Why is this correct?</span></div>',
    ),
    dict(
        key="pyq", min=5.0,
        title="Previous-year question (PYQ) practice", sub="Ingested CS, DA, ISRO, NIELIT, UGC-NET & TIFR papers",
        narration="It has ingested thousands of real previous-year questions. Ask for one and it presents the question, then walks through the full solution.",
        body=user("Give me a GATE CS PYQ on TLB effective access time.")
             + bot('<p><b>GATE PYQ.</b> A paged system has a TLB hit ratio of 0.9, TLB access 10&nbsp;ns, '
                   'and memory access 100&nbsp;ns. Find the effective access time.</p>'
                   '<div class="li"><b>Hit:</b> <span class="math">10 + 100 = 110</span> ns</div>'
                   '<div class="li"><b>Miss:</b> <span class="math">10 + 100 + 100 = 210</span> ns</div>'
                   '<div class="li"><b>EAT</b> = <span class="math">0.9·110 + 0.1·210 = 120</span> ns ✅</div>'),
    ),
    dict(
        key="attach", min=5.5,
        title="Attach images or PDFs", sub="Vision reads a snapshot of a question; PDFs/text become context",
        narration="Stuck on a question in a screenshot or a PDF? Just attach it. The vision model reads the image, or text is extracted from documents, and the bot answers from it.",
        body=user("Solve the question in this image.",
                  extra='<div class="thumb">🖼️ photo of a<br>GATE question</div>')
             + bot('<p>From your image — finding the number of spanning trees of <span class="math">K₄</span>:</p>'
                   '<div class="li">Cayley\'s formula: <span class="math">n^(n−2)</span></div>'
                   '<div class="li">For <span class="math">n = 4</span>: <span class="math">4² = 16</span> spanning trees ✅</div>'
                   '<p>So the correct option is <b>16</b>.</p>'),
    ),
    dict(
        key="feedback", min=5.0,
        title="Like · dislike · copy · regenerate", sub="Familiar per-answer controls on every turn",
        narration="Every answer has copy, like, dislike and regenerate controls. Dislike opens a quick form so you can say exactly what was wrong.",
        body=bot('<p>…the worst-case complexity of quicksort is <span class="math">O(n&nbsp;log&nbsp;n)</span>.</p>'
                 '<div class="actions"><span class="act">⧉</span><span class="act">👍</span>'
                 '<span class="act on">👎</span><span class="act">↻</span></div>'
                 '<div class="feedback"><div class="q">What went wrong? Your feedback trains the assistant.</div>'
                 '<span class="rchip on">Incorrect</span><span class="rchip">Incomplete</span>'
                 '<span class="rchip">Not helpful</span><span class="rchip">Too verbose</span>'
                 '<div style="font-size:12px;color:#64748b;margin-top:6px">+ Suggest a better answer (helps RLHF training)</div></div>'),
    ),
    dict(
        key="rlhf", center=True, min=6.0,
        title="Human feedback → RLHF", sub="Feedback steers regeneration & builds a preference dataset",
        narration="This powers a human-feedback loop. A disliked answer is regenerated using your feedback, and the correction is saved as a preference pair you can export as J-S-O-N-L to fine-tune the model with D-P-O.",
        body='<div class="center"><div class="big-title" style="font-size:34px">Feedback &amp; RLHF loop</div>'
             '<div class="arch">'
             '<div class="node red"><div class="t">👎 Dislike + reason</div><div class="d">captured per answer</div></div>'
             '<span class="arrow">→</span>'
             '<div class="node"><div class="t">↻ Regenerate</div><div class="d">prompt steered by feedback</div></div>'
             '<span class="arrow">→</span>'
             '<div class="node red"><div class="t">preference_pairs</div><div class="d">(prompt, chosen, rejected)</div></div>'
             '<span class="arrow">→</span>'
             '<div class="node"><div class="t">export JSONL</div><div class="d">reward model / DPO</div></div>'
             '</div>'
             '<div class="subtitle" style="font-size:14px;margin-top:14px">GET /export/preferences → train offline → redeploy an improved model</div></div>',
    ),
    dict(
        key="arch", center=True, min=6.0,
        title="Architecture", sub="React + TypeScript + Tailwind ⇄ FastAPI ⇄ Chroma RAG + OpenAI",
        narration="Under the hood: a React, TypeScript and Tailwind front-end talks to a FastAPI backend, which runs retrieval-augmented generation over a Chroma vector store with OpenAI, and persists everything in a database.",
        body='<div class="center"><div class="big-title" style="font-size:34px">How it fits together</div>'
             '<div class="arch">'
             '<div class="node"><div class="t">React + TS</div><div class="d">Vite · Tailwind · SSE</div></div>'
             '<span class="arrow">⇄</span>'
             '<div class="node red"><div class="t">FastAPI</div><div class="d">/chat · /feedback · /regenerate</div></div>'
             '<span class="arrow">⇄</span>'
             '<div class="node"><div class="t">RAG engine</div><div class="d">Chroma + OpenAI embeddings</div></div>'
             '</div>'
             '<div class="arch">'
             '<div class="node"><div class="t">data/ PDFs + notes</div><div class="d">ingested &amp; chunked</div></div>'
             '<div class="node"><div class="t">SQLite / Postgres</div><div class="d">chats · feedback · RLHF</div></div>'
             '<div class="node red"><div class="t">gpt-4o-mini</div><div class="d">answers + vision</div></div>'
             '</div></div>',
    ),
    dict(
        key="outro", center=True, min=5.5,
        title="Thank you", sub="GateOverflow Chatbot · gateoverflow.in",
        narration="That's the GateOverflow Chatbot — rich in knowledge, grounded in real questions, and built to standards you can ship. Thanks for watching!",
        body=f'<div class="center">{LOGO_BIG}<div class="big-title" style="font-size:38px">Rich. Grounded. Production-ready.</div>'
             '<div class="checklist">'
             '<div class="check"><span class="tick">✓</span> RAG over CS / DS / ML / AI material</div>'
             '<div class="check"><span class="tick">✓</span> Previous-year question practice</div>'
             '<div class="check"><span class="tick">✓</span> Streaming, citations &amp; LaTeX</div>'
             '<div class="check"><span class="tick">✓</span> Image &amp; PDF attachments</div>'
             '<div class="check"><span class="tick">✓</span> Feedback + RLHF export</div>'
             '<div class="check"><span class="tick">✓</span> Dockerised, tested, documented</div>'
             '</div>'
             '<div class="subtitle" style="margin-top:10px">Built for GateOverflow · gateoverflow.in</div></div>',
    ),
]


# --------------------------------------------------------------------------- #
# Build                                                                       #
# --------------------------------------------------------------------------- #
def sh(cmd: list[str]) -> str:
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def duration(path: Path) -> float:
    out = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
              "-of", "csv=p=0", str(path)])
    return float(out.strip())


def main() -> int:
    for tool, hint in [(CHROME, "Google Chrome"), ("ffmpeg", "ffmpeg"), ("say", "say")]:
        if "/" in tool and not Path(tool).exists():
            print(f"❌ {hint} not found at {tool}")
            return 1
        if "/" not in tool and shutil.which(tool) is None:
            print(f"❌ {hint} not found on PATH")
            return 1

    if FRAMES.exists():
        shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True)

    total = len(SCENES)
    segments: list[Path] = []

    for i, sc in enumerate(SCENES, 1):
        stem = f"{i:02d}_{sc['key']}"
        html = FRAMES / f"{stem}.html"
        png = FRAMES / f"{stem}.png"
        aiff = FRAMES / f"{stem}.aiff"
        seg = FRAMES / f"{stem}.mp4"

        html.write_text(
            page(sc["body"], sc["title"], sc["sub"], i, total, sc.get("center", False)),
            encoding="utf-8",
        )

        print(f"🎬 scene {i}/{total}: {sc['key']} — rendering")
        sh([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=2", f"--window-size={W},{H}",
            f"--screenshot={png}", f"file://{html}", "--virtual-time-budget=2500"])

        sh(["say", "-v", VOICE, "-o", str(aiff), sc["narration"]])
        dur = max(duration(aiff) + 1.1, sc.get("min", 3.5))

        # One clip: still image for `dur` s, with gentle fade in/out, narration
        # padded with trailing silence so audio and video lengths match exactly.
        vf = (f"scale=1920:1080:force_original_aspect_ratio=decrease,"
              f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x020617,fps=30,"
              f"fade=t=in:st=0:d=0.3,fade=t=out:st={dur-0.35:.2f}:d=0.35")
        sh(["ffmpeg", "-y", "-loop", "1", "-t", f"{dur:.2f}", "-i", str(png),
            "-i", str(aiff),
            "-filter_complex", f"[0:v]{vf}[v];[1:a]apad[a]",
            "-map", "[v]", "-map", "[a]", "-t", f"{dur:.2f}",
            "-c:v", "libx264", "-preset", "medium", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "160k", "-ar", "44100", str(seg)])
        segments.append(seg)
        print(f"   ✓ {dur:.1f}s")

    listfile = FRAMES / "concat.txt"
    listfile.write_text("".join(f"file '{s}'\n" for s in segments), encoding="utf-8")
    print("🎞️  concatenating →", OUT.name)
    sh(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile),
        "-c", "copy", str(OUT)])

    print(f"\n✅ Done: {OUT}  ({duration(OUT):.1f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
