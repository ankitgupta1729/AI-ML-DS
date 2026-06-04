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
body{font-family:'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;background:#020617}
.app{position:relative;width:1280px;height:720px;overflow:hidden;
  background:linear-gradient(180deg,#020617,#0b1220)}
.glow{position:absolute;border-radius:9999px;filter:blur(80px);pointer-events:none}
.glow.a{top:-120px;left:50%;transform:translateX(-50%);width:640px;height:240px;background:rgba(220,38,38,.18)}
.glow.b{bottom:60px;right:-40px;width:280px;height:280px;background:rgba(225,29,72,.14)}
.header{position:relative;display:flex;align-items:center;gap:12px;padding:12px 24px;
  border-bottom:1px solid rgba(255,255,255,.08);background:rgba(2,6,23,.6)}
.badge{display:grid;place-items:center;width:42px;height:42px;border-radius:14px;
  background:#1e293b;border:1px solid rgba(255,255,255,.1)}
.h-title{font-size:18px;font-weight:800;color:#fff;display:flex;align-items:center;gap:8px}
.tag{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:#f87171;
  background:rgba(220,38,38,.15);padding:2px 8px;border-radius:9999px}
.h-sub{font-size:12px;color:#94a3b8}
.status{margin-left:auto;display:flex;align-items:center;gap:6px;font-size:12px;color:#cbd5e1;
  border:1px solid rgba(255,255,255,.1);padding:5px 10px;border-radius:9999px}
.dot{width:8px;height:8px;border-radius:9999px;background:#22c55e}
.shell{display:flex;height:578px}
.rail{width:172px;flex:0 0 auto;border-right:1px solid rgba(255,255,255,.08);background:rgba(2,6,23,.4);padding:10px 8px}
.nav{display:flex;align-items:center;gap:10px;padding:9px 11px;border-radius:11px;font-size:13px;color:#94a3b8;margin-bottom:3px}
.nav.on{background:linear-gradient(90deg,rgba(220,38,38,.18),rgba(225,29,72,.08));color:#fca5a5;font-weight:600}
.nav .ic{width:18px;text-align:center}
.main{position:relative;flex:1;padding:20px 26px 0;overflow:hidden}
.row{display:flex;gap:12px;margin-bottom:16px;animation:up .5s ease both}
.row.user{justify-content:flex-end}
.ubub{max-width:74%;background:linear-gradient(135deg,#dc2626,#b91c1c);color:#fff;padding:11px 15px;
  border-radius:18px 18px 4px 18px;font-size:15px;line-height:1.5;box-shadow:0 8px 24px rgba(220,38,38,.25)}
.avatar{flex:0 0 auto;width:34px;height:34px;border-radius:11px;background:#1e293b;border:1px solid rgba(255,255,255,.1);display:grid;place-items:center}
.bbub{max-width:82%;background:rgba(15,23,42,.7);border:1px solid rgba(255,255,255,.1);color:#e2e8f0;
  padding:13px 17px;border-radius:18px 18px 18px 4px;font-size:14px;line-height:1.6}
.bbub h4{color:#fff;font-size:15px;margin:2px 0 6px}
.bbub p{margin:5px 0}.bbub b{color:#fff}
.math{font-family:'Times New Roman',Georgia,serif;font-style:italic;background:rgba(220,38,38,.14);
  padding:1px 7px;border-radius:6px;color:#fecaca}
.li{margin:4px 0;display:flex;gap:8px}.li::before{content:'•';color:#f87171}
.src{margin-top:10px;border:1px solid rgba(255,255,255,.1);border-radius:12px;background:rgba(2,6,23,.5);padding:8px 11px;font-size:12px;color:#cbd5e1}
.src .name{color:#fff;font-weight:600}
.pill{display:inline-block;font-size:10px;font-weight:600;padding:2px 8px;border-radius:9999px}
.pill.subj{background:rgba(220,38,38,.15);color:#f87171}
.pill.match{background:rgba(34,197,94,.15);color:#4ade80;margin-left:6px}
.actions{display:flex;gap:6px;margin-top:10px}
.act{width:30px;height:30px;border-radius:9px;display:grid;place-items:center;color:#94a3b8;border:1px solid rgba(255,255,255,.08);font-size:13px}
.act.on{color:#f87171;background:rgba(220,38,38,.15);border-color:rgba(220,38,38,.3)}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.chip{font-size:12px;color:#cbd5e1;border:1px solid rgba(255,255,255,.12);background:rgba(15,23,42,.6);padding:6px 12px;border-radius:9999px}
.chip.red{border-color:rgba(220,38,38,.4);color:#fca5a5}
.thumb{width:120px;height:84px;border-radius:12px;border:1px solid rgba(255,255,255,.15);
  background:linear-gradient(135deg,#334155,#1e293b);display:grid;place-items:center;color:#cbd5e1;font-size:11px;text-align:center;padding:6px}
.feedback{margin-top:10px;border:1px solid rgba(255,255,255,.1);border-radius:12px;background:rgba(2,6,23,.5);padding:11px}
.feedback .q{font-size:12px;color:#cbd5e1;font-weight:600;margin-bottom:8px}
.rchip{display:inline-block;font-size:11px;color:#cbd5e1;border:1px solid rgba(255,255,255,.15);padding:4px 10px;border-radius:9999px;margin:0 6px 6px 0}
.rchip.on{border-color:#dc2626;background:rgba(220,38,38,.12);color:#fca5a5}

.center{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:14px;padding:0 60px}
.big-title{font-size:44px;font-weight:900;background:linear-gradient(90deg,#f87171,#e11d48);-webkit-background-clip:text;background-clip:text;color:transparent}
.subtitle{font-size:18px;color:#94a3b8;max-width:680px}
.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;width:100%;margin-top:8px}
.card{border:1px solid rgba(255,255,255,.1);background:rgba(15,23,42,.55);border-radius:16px;padding:15px;text-align:left}
.card .k{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;color:#f87171;margin-bottom:5px}
.card .v{font-size:13px;color:#cbd5e1;line-height:1.45}
.checklist{display:grid;grid-template-columns:1fr 1fr;gap:9px 26px;text-align:left;margin-top:8px}
.check{font-size:15px;color:#e2e8f0;display:flex;gap:10px;align-items:center}
.check .tick{color:#4ade80;font-weight:800}

/* comparison */
.cmp{display:flex;gap:18px;width:100%;margin-top:10px}
.col{flex:1;border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:16px;background:rgba(15,23,42,.5)}
.col.go{border-color:rgba(220,38,38,.45);background:rgba(220,38,38,.06)}
.col h3{font-size:15px;color:#fff;margin-bottom:10px}
.cmp .r{display:flex;gap:8px;font-size:13px;color:#cbd5e1;margin:7px 0;text-align:left}
.cmp .x{color:#f87171}.cmp .ok{color:#4ade80}

/* quiz */
.opt{border:1px solid rgba(255,255,255,.12);border-radius:10px;padding:9px 12px;font-size:13.5px;color:#cbd5e1;margin:6px 0;display:flex;gap:8px;align-items:center}
.opt .b{width:22px;height:22px;border-radius:50%;border:1px solid rgba(255,255,255,.25);display:grid;place-items:center;font-size:11px}
.opt.correct{border-color:#22c55e;background:rgba(34,197,94,.12);color:#bbf7d0}
.opt.correct .b{background:#22c55e;border-color:#22c55e;color:#022}
.scorebar{display:flex;gap:10px;flex-wrap:wrap;margin-top:6px}
.stat{border:1px solid rgba(255,255,255,.12);border-radius:9999px;padding:5px 13px;font-size:13px;color:#cbd5e1}
.stat b{color:#fff}

/* flashcard */
.flash{border:1px solid rgba(255,255,255,.12);border-radius:16px;background:rgba(15,23,42,.6);padding:18px;max-width:560px;margin:0 auto}
.flash .lbl{font-size:10px;text-transform:uppercase;letter-spacing:.5px;color:#64748b;margin-bottom:4px}
.flash .f{font-size:16px;color:#fff;font-weight:600}
.flash hr{border:none;border-top:1px dashed rgba(255,255,255,.15);margin:12px 0}
.flash .bk{font-size:13.5px;color:#cbd5e1}
.grades{display:flex;gap:8px;justify-content:center;margin-top:12px}
.g{border:1px solid rgba(255,255,255,.18);border-radius:10px;padding:6px 16px;font-size:13px;font-weight:600}

/* timeline */
.tl{display:flex;flex-direction:column;gap:9px;margin-top:6px}
.day{display:flex;gap:12px;border:1px solid rgba(255,255,255,.1);border-radius:12px;background:rgba(15,23,42,.5);padding:10px 12px}
.dnum{width:34px;height:34px;flex:0 0 auto;border-radius:10px;background:linear-gradient(135deg,#dc2626,#e11d48);display:grid;place-items:center;color:#fff;font-weight:800;font-size:13px}
.day .f{font-weight:700;color:#fff;font-size:13.5px}.day .t{font-size:12px;color:#94a3b8}

/* dashboard */
.dash{display:flex;gap:18px;align-items:center;margin-top:6px}
.kpis{display:grid;grid-template-columns:1fr 1fr;gap:10px;flex:0 0 300px}
.kpi{border:1px solid rgba(255,255,255,.1);border-radius:14px;background:rgba(15,23,42,.55);padding:12px}
.kpi.acc{border-color:transparent;background:linear-gradient(135deg,#dc2626,#e11d48)}
.kpi .n{font-size:26px;font-weight:900;color:#fff}.kpi .l{font-size:11px;color:#94a3b8}
.kpi.acc .l{color:rgba(255,255,255,.85)}
.bars{flex:1}
.barrow{margin:8px 0}
.barrow .h{display:flex;justify-content:space-between;font-size:12px;color:#cbd5e1;margin-bottom:3px}
.track{height:9px;border-radius:9999px;background:rgba(255,255,255,.08);overflow:hidden}
.fill{height:100%;border-radius:9999px}

/* feature grid */
.feat{display:grid;grid-template-columns:1fr 1fr;gap:12px;width:100%;margin-top:6px;text-align:left}
.fitem{display:flex;gap:11px;border:1px solid rgba(255,255,255,.1);border-radius:14px;background:rgba(15,23,42,.5);padding:12px 14px}
.fitem .e{font-size:22px}.fitem .t{font-weight:700;color:#fff;font-size:13.5px}.fitem .d{font-size:12px;color:#94a3b8}

/* architecture */
.arch{display:flex;align-items:center;justify-content:center;gap:16px;margin-top:14px;flex-wrap:wrap}
.node{border:1px solid rgba(255,255,255,.14);background:rgba(15,23,42,.6);border-radius:14px;padding:13px 15px;min-width:140px;text-align:center}
.node .t{font-weight:800;color:#fff;font-size:13.5px}.node .d{font-size:11px;color:#94a3b8;margin-top:3px}
.node.red{border-color:rgba(220,38,38,.45)}
.arrow{color:#f87171;font-size:22px;font-weight:800}

.caption{position:absolute;left:0;right:0;bottom:0;height:92px;background:linear-gradient(180deg,rgba(2,6,23,0),rgba(2,6,23,.92));display:flex;align-items:center;gap:14px;padding:0 26px 14px}
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


def _rail(active: str) -> str:
    items = [("💬", "Chat", "chat"), ("📝", "Mock Test", "mock"), ("🃏", "Flashcards", "review"),
             ("🗓️", "Planner", "planner"), ("📊", "Dashboard", "dashboard"), ("🔥", "Daily", "daily")]
    rows = "".join(
        f'<div class="nav {"on" if k == active else ""}"><span class="ic">{e}</span>{lbl}</div>'
        for e, lbl, k in items
    )
    return f'<div class="rail">{rows}</div>'


def page(body: str, title: str, sub: str, n: int, total: int,
         center: bool = False, rail: str | None = None) -> str:
    if center:
        inner = body
    else:
        side = _rail(rail) if rail else ""
        inner = HEADER + f'<div class="shell">{side}<div class="main">{body}</div></div>'
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


LOGO_BIG = f'<div class="badge" style="width:104px;height:104px;border-radius:28px">{GO_LOGO.format(s=78, go="#fff")}</div>'

# --------------------------------------------------------------------------- #
# Scenes                                                                      #
# --------------------------------------------------------------------------- #
SCENES = [
    dict(key="intro", center=True, min=5.0,
         title="GateOverflow Chatbot", sub="Product demo",
         narration="Meet the GateOverflow Chatbot — a complete AI study companion for the GATE Computer Science and Data Science and AI exams, grounded in real previous-year questions.",
         body=f'<div class="center">{LOGO_BIG}<div class="big-title">GateOverflow Chatbot</div>'
              f'<div class="subtitle">Your AI study buddy for GATE CS &amp; DA — grounded in real previous-year questions.</div>'
              f'<div class="chips" style="justify-content:center"><span class="chip red">Grounded RAG</span>'
              f'<span class="chip red">PYQ practice &amp; mock tests</span><span class="chip red">Spaced repetition</span>'
              f'<span class="chip red">Analytics &amp; RLHF</span></div></div>'),

    dict(key="why", center=True, min=8.5,
         title="Why not just use ChatGPT or Claude?", sub="A GATE specialist vs. a general chatbot",
         narration="You might ask: why not just use ChatGPT, Claude or DeepSeek? Because exam prep needs trust and structure. General chatbots are brilliant generalists that can hallucinate. This is a GATE specialist — it cites real previous-year questions, scores mock tests, schedules revision, and learns from your feedback.",
         body='<div class="center"><div class="big-title" style="font-size:32px">A specialist, not a generalist</div>'
              '<div class="cmp">'
              '<div class="col"><h3>🌐 ChatGPT / Claude / DeepSeek</h3>'
              '<div class="r"><span class="x">✗</span> Answers from generic web knowledge</div>'
              '<div class="r"><span class="x">✗</span> Can invent fake "GATE questions"</div>'
              '<div class="r"><span class="x">✗</span> No citations to your material</div>'
              '<div class="r"><span class="x">✗</span> No scoring, mock tests or revision</div>'
              '<div class="r"><span class="x">✗</span> Forgets your corrections</div></div>'
              '<div class="col go"><h3>🎯 GateOverflow Chatbot</h3>'
              '<div class="r"><span class="ok">✓</span> Grounded in real PYQs &amp; your notes</div>'
              '<div class="r"><span class="ok">✓</span> Cites source file, page &amp; match score</div>'
              '<div class="r"><span class="ok">✓</span> Mock tests with GATE negative marking</div>'
              '<div class="r"><span class="ok">✓</span> Spaced repetition + analytics</div>'
              '<div class="r"><span class="ok">✓</span> Learns from feedback (RLHF)</div></div>'
              '</div></div>'),

    dict(key="workspace", rail="chat", min=6.0,
         title="One focused workspace", sub="Chat · Mock Test · Flashcards · Planner · Dashboard · Daily",
         narration="Everything lives in one focused workspace. A sidebar gives you chat, mock tests, flashcards, a study planner, a performance dashboard, and a daily question — all tuned for GATE.",
         body='<div class="grid3">'
              '<div class="card"><div class="k">💬 Chat</div><div class="v">Ask anything — grounded, cited answers.</div></div>'
              '<div class="card"><div class="k">📝 Mock Test</div><div class="v">MCQ/MSQ/NAT, scored with negative marking.</div></div>'
              '<div class="card"><div class="k">🃏 Flashcards</div><div class="v">Spaced repetition (SM-2).</div></div>'
              '<div class="card"><div class="k">🗓️ Planner</div><div class="v">Day-by-day plan to exam date.</div></div>'
              '<div class="card"><div class="k">📊 Dashboard</div><div class="v">Readiness, weak areas, percentile.</div></div>'
              '<div class="card"><div class="k">🔥 Daily</div><div class="v">Question of the day + streaks.</div></div>'
              '</div>'),

    dict(key="answer", rail="chat", min=6.0,
         title="Ask anything — grounded answers", sub="Markdown, LaTeX maths and citations, streamed live",
         narration="In chat, ask any question. Here: explain the complexity of merge sort. The answer streams in with proper maths, and a citation to the source material.",
         body=user("Explain the time complexity of merge sort and why.")
              + bot('<h4>Merge sort — <span class="math">O(n&nbsp;log&nbsp;n)</span></h4>'
                    '<p>It splits the array in half each time and merges sorted halves:</p>'
                    '<div class="li">Recurrence <span class="math">T(n)=2T(n/2)+O(n)</span></div>'
                    '<div class="li">By the Master Theorem → <span class="math">Θ(n&nbsp;log&nbsp;n)</span></div>'
                    '<div class="li">Stable, with <b>worst-case</b> <span class="math">O(n&nbsp;log&nbsp;n)</span> (unlike quicksort).</div>'
                    '<div class="src">📄 <span class="name">cs_core_concepts.md</span> '
                    '<span class="pill subj">computer_science</span><span class="pill match">91% match</span></div>')),

    dict(key="pyq", rail="chat", min=6.5,
         title="PYQ practice — solved step by step", sub="CS, DA, ISRO, NIELIT, UGC-NET & TIFR papers ingested",
         narration="Ask for a previous-year question and it solves it step by step. Here, a classic numerical on TLB effective access time, worked through to the final answer.",
         body=user("Solve a GATE PYQ on TLB effective access time.")
              + bot('<p><b>PYQ.</b> TLB hit ratio 0.9, TLB access 10&nbsp;ns, memory access 100&nbsp;ns. Find EAT.</p>'
                    '<div class="li"><b>Hit:</b> <span class="math">10+100 = 110</span> ns</div>'
                    '<div class="li"><b>Miss:</b> <span class="math">10+100+100 = 210</span> ns</div>'
                    '<div class="li"><b>EAT</b> = <span class="math">0.9·110 + 0.1·210 = 120</span> ns ✅</div>'
                    '<div class="actions"><span class="act">⧉</span><span class="act">👍</span><span class="act">👎</span><span class="act">↻</span><span class="act">🔊</span></div>')),

    dict(key="sources", rail="chat", min=5.0,
         title="Every answer cites its sources", sub="File, page, subject and a similarity score",
         narration="Trust matters in exam prep. Every answer can show exactly where it came from — the source file, the page, and a relevance score — and offers one-click follow-ups.",
         body=bot('<h4>Sources used</h4>'
                  '<div class="src">📄 <span class="name">dive_into_deep_learning.pdf</span> · p. 142 '
                  '<span class="pill subj">data_science_ai</span><span class="pill match">88% match</span></div>'
                  '<div class="src">📄 <span class="name">filter1_volume2.pdf</span> · p. 57 '
                  '<span class="pill subj">GATA-Data</span><span class="pill match">84% match</span></div>')
              + '<div class="chips"><span class="chip">Explain step by step</span><span class="chip">Similar PYQ</span><span class="chip">Why correct?</span></div>'),

    dict(key="attach", rail="chat", min=6.0,
         title="Attach images, PDFs — or sketch", sub="Vision reads a question; PDFs become context",
         narration="Stuck on a question in a screenshot, a PDF, or even your own sketch? Attach it. The vision model reads the image and solves it.",
         body=user("Solve the question in this image.", extra='<div class="thumb">🖼️ photo of a<br>GATE question</div>')
              + bot('<p>From your image — spanning trees of <span class="math">K₄</span>:</p>'
                    '<div class="li">Cayley\'s formula <span class="math">n^(n−2)</span></div>'
                    '<div class="li">For <span class="math">n=4</span>: <span class="math">4²=16</span> ✅</div>')),

    dict(key="power", center=True, min=7.0,
         title="Power features", sub="Voice · sketch · multilingual · Socratic · confidence",
         narration="The chat is packed with features: speak your question and hear answers read aloud, draw a diagram, get answers in Hindi and other languages, switch on Socratic mode for hints before solutions, and see a grounding-confidence meter on every reply.",
         body='<div class="center"><div class="big-title" style="font-size:30px">Built for how students study</div>'
              '<div class="feat">'
              '<div class="fitem"><span class="e">🎙️</span><div><div class="t">Voice in &amp; out</div><div class="d">Ask by speaking; listen to answers.</div></div></div>'
              '<div class="fitem"><span class="e">✏️</span><div><div class="t">Sketch a question</div><div class="d">Draw it; vision reads your sketch.</div></div></div>'
              '<div class="fitem"><span class="e">🌐</span><div><div class="t">Multilingual</div><div class="d">Explanations in Hindi &amp; more.</div></div></div>'
              '<div class="fitem"><span class="e">💡</span><div><div class="t">Socratic mode</div><div class="d">Hints first, solution when ready.</div></div></div>'
              '<div class="fitem"><span class="e">📈</span><div><div class="t">Confidence meter</div><div class="d">Shows how grounded each answer is.</div></div></div>'
              '<div class="fitem"><span class="e">📎</span><div><div class="t">Attachments</div><div class="d">Images &amp; PDFs as context.</div></div></div>'
              '</div></div>'),

    dict(key="feedback", rail="chat", min=5.5,
         title="Like · dislike · copy · regenerate", sub="Familiar controls on every answer",
         narration="Every answer has copy, like, dislike, regenerate and read-aloud. A dislike opens a quick form so you can say exactly what was wrong.",
         body=bot('<p>…the worst-case complexity of quicksort is <span class="math">O(n&nbsp;log&nbsp;n)</span>.</p>'
                  '<div class="actions"><span class="act">⧉</span><span class="act">👍</span><span class="act on">👎</span><span class="act">↻</span><span class="act">🔊</span></div>'
                  '<div class="feedback"><div class="q">What went wrong? Your feedback trains the assistant.</div>'
                  '<span class="rchip on">Incorrect</span><span class="rchip">Incomplete</span><span class="rchip">Too verbose</span>'
                  '<div style="font-size:12px;color:#64748b;margin-top:6px">+ Suggest a better answer (helps RLHF)</div></div>')),

    dict(key="rlhf", center=True, min=6.5,
         title="Human feedback → RLHF", sub="Feedback steers regeneration & builds a preference dataset",
         narration="This powers a real human-feedback loop. A disliked answer is regenerated using your feedback, and the correction becomes a preference pair you can export as J-S-O-N-L to fine-tune the model with D-P-O.",
         body='<div class="center"><div class="big-title" style="font-size:32px">Feedback &amp; RLHF loop</div>'
              '<div class="arch">'
              '<div class="node red"><div class="t">👎 Dislike + reason</div><div class="d">captured per answer</div></div>'
              '<span class="arrow">→</span>'
              '<div class="node"><div class="t">↻ Regenerate</div><div class="d">steered by feedback</div></div>'
              '<span class="arrow">→</span>'
              '<div class="node red"><div class="t">preference_pairs</div><div class="d">(prompt, chosen, rejected)</div></div>'
              '<span class="arrow">→</span>'
              '<div class="node"><div class="t">export JSONL</div><div class="d">reward model / DPO</div></div>'
              '</div><div class="subtitle" style="font-size:14px;margin-top:12px">Collect → export → train offline → redeploy a better model</div></div>'),

    dict(key="mock", rail="mock", min=7.0,
         title="Mock tests & scoring", sub="MCQ / MSQ / NAT with GATE negative marking + percentile",
         narration="The mock-test module generates exam-style questions, then scores them server-side with GATE negative marking, and estimates your percentile.",
         body='<div style="font-size:13px;color:#94a3b8;margin-bottom:4px">Q3 · MCQ · 2 marks · Algorithms</div>'
              '<div style="font-size:15px;color:#e2e8f0;margin-bottom:8px">The recurrence <span class="math">T(n)=2T(n/2)+n</span> solves to:</div>'
              '<div class="opt"><span class="b">A</span> Θ(n)</div>'
              '<div class="opt correct"><span class="b">✓</span> Θ(n log n)</div>'
              '<div class="opt"><span class="b">C</span> Θ(n²)</div>'
              '<div class="opt"><span class="b">D</span> Θ(log n)</div>'
              '<div class="scorebar"><span class="stat"><b>Score</b> 7.3 / 10</span><span class="stat"><b>Accuracy</b> 80%</span>'
              '<span class="stat"><b>Est. percentile</b> 96.4</span><span class="stat"><b>−1/3</b> per wrong MCQ</span></div>'),

    dict(key="flash", rail="review", min=6.0,
         title="Flashcards & spaced repetition", sub="SM-2 schedule · wrong answers become cards",
         narration="Missed questions automatically become flashcards, reviewed on a spaced-repetition schedule so you remember them for the exam.",
         body='<div class="flash"><div class="lbl">Question — tap to flip</div>'
              '<div class="f">State the Master Theorem case for T(n)=2T(n/2)+n.</div><hr>'
              '<div class="lbl">Answer</div>'
              '<div class="bk">a=2, b=2, f(n)=n. Since n^(log_b a)=n, it is Case 2 → <b>Θ(n log n)</b>.</div>'
              '<div class="grades"><span class="g" style="color:#f87171;border-color:rgba(248,113,113,.5)">Again</span>'
              '<span class="g" style="color:#fbbf24;border-color:rgba(251,191,36,.5)">Hard</span>'
              '<span class="g" style="color:#38bdf8;border-color:rgba(56,189,248,.5)">Good</span>'
              '<span class="g" style="color:#4ade80;border-color:rgba(74,222,128,.5)">Easy</span></div></div>'),

    dict(key="planner", rail="planner", min=6.0,
         title="Study planner", sub="Day-by-day plan → export to your calendar (.ics)",
         narration="The planner builds a day-by-day schedule to your exam date, prioritising high-weight subjects, and exports straight to your calendar.",
         body='<div style="font-size:13px;color:#cbd5e1;margin-bottom:6px">30-day plan · ~4 h/day · high-weight first, PYQs &amp; revision built in</div>'
              '<div class="tl">'
              '<div class="day"><div class="dnum">1</div><div><div class="f">Operating Systems — scheduling</div><div class="t">Learn concepts · 10 PYQs · short notes</div></div></div>'
              '<div class="day"><div class="dnum">2</div><div><div class="f">DBMS — normalization &amp; transactions</div><div class="t">Concepts · BCNF drills · 12 PYQs</div></div></div>'
              '<div class="day"><div class="dnum">3</div><div><div class="f">Algorithms — DP &amp; greedy</div><div class="t">Patterns · mock set · revise Day 1</div></div></div>'
              '</div>'
              '<div class="chips" style="margin-top:12px"><span class="chip red">⬇ Export to calendar (.ics)</span></div>'),

    dict(key="dashboard", rail="dashboard", min=6.5,
         title="Performance dashboard", sub="Readiness score · accuracy by subject · weak areas",
         narration="A dashboard turns your attempts into insight: an exam-readiness score, accuracy by subject, your streak, and the weak areas to prioritise next.",
         body='<div class="dash">'
              '<div class="kpis">'
              '<div class="kpi acc"><div class="n">78</div><div class="l">Readiness / 100</div></div>'
              '<div class="kpi"><div class="n">82%</div><div class="l">Avg accuracy</div></div>'
              '<div class="kpi"><div class="n">94.1</div><div class="l">Avg percentile</div></div>'
              '<div class="kpi"><div class="n">12🔥</div><div class="l">Day streak</div></div>'
              '</div>'
              '<div class="bars">'
              '<div class="barrow"><div class="h"><span>Algorithms</span><span>88%</span></div><div class="track"><div class="fill" style="width:88%;background:#22c55e"></div></div></div>'
              '<div class="barrow"><div class="h"><span>Operating Systems</span><span>72%</span></div><div class="track"><div class="fill" style="width:72%;background:#f59e0b"></div></div></div>'
              '<div class="barrow"><div class="h"><span>Computer Networks</span><span>46%</span></div><div class="track"><div class="fill" style="width:46%;background:#ef4444"></div></div></div>'
              '<div class="barrow"><div class="h"><span>Probability</span><span>61%</span></div><div class="track"><div class="fill" style="width:61%;background:#f59e0b"></div></div></div>'
              '<div style="font-size:12px;color:#fbbf24;margin-top:8px">⚠ Prioritise: Computer Networks, Probability</div>'
              '</div></div>'),

    dict(key="daily", rail="daily", min=5.5,
         title="Daily question & streaks", sub="Habit-forming, one question a day",
         narration="A daily question with a hint keeps the habit going and your streak alive — small, consistent practice that compounds.",
         body='<div style="max-width:560px;margin:6px auto 0;border:1px solid rgba(255,255,255,.1);border-radius:16px;background:rgba(15,23,42,.6);padding:18px">'
              '<div style="display:flex;justify-content:space-between"><span class="pill subj">Question of the day · 2026-06-04</span><span style="color:#fbbf24;font-weight:700">12🔥 streak</span></div>'
              '<div style="font-size:11px;text-transform:uppercase;color:#64748b;margin-top:10px">dynamic programming</div>'
              '<div style="font-size:17px;color:#fff;font-weight:600;margin-top:3px">What is the time complexity of the 0/1 knapsack DP, and why isn\'t it polynomial in the input size?</div>'
              '<div style="margin-top:10px;background:rgba(245,158,11,.12);color:#fcd34d;border-radius:10px;padding:9px;font-size:13px">💡 Hint: think pseudo-polynomial — O(nW).</div>'
              '<div class="chips" style="margin-top:12px"><span class="chip red">Solve with GO Buddy →</span></div></div>'),

    dict(key="arch", center=True, min=6.0,
         title="Architecture", sub="React + TypeScript + Tailwind ⇄ FastAPI ⇄ Chroma RAG + OpenAI",
         narration="Under the hood: a React, TypeScript and Tailwind front-end talks to a FastAPI backend, which runs retrieval-augmented generation over a Chroma vector store with OpenAI, and persists chats, feedback and progress in a database.",
         body='<div class="center"><div class="big-title" style="font-size:30px">How it fits together</div>'
              '<div class="arch">'
              '<div class="node"><div class="t">React + TS</div><div class="d">Vite · Tailwind · SSE</div></div>'
              '<span class="arrow">⇄</span>'
              '<div class="node red"><div class="t">FastAPI</div><div class="d">chat · quiz · review · plan</div></div>'
              '<span class="arrow">⇄</span>'
              '<div class="node"><div class="t">RAG engine</div><div class="d">Chroma + OpenAI</div></div>'
              '</div>'
              '<div class="arch">'
              '<div class="node"><div class="t">data/ PDFs + notes</div><div class="d">ingested &amp; chunked</div></div>'
              '<div class="node"><div class="t">SQLite / Postgres</div><div class="d">chats · feedback · progress</div></div>'
              '<div class="node red"><div class="t">gpt-4o-mini</div><div class="d">answers + vision</div></div>'
              '</div></div>'),

    dict(key="outro", center=True, min=6.0,
         title="Thank you", sub="GateOverflow Chatbot · gateoverflow.in",
         narration="That's the GateOverflow Chatbot — rich in knowledge, grounded in real questions, with mock tests, spaced repetition, analytics and a feedback loop, built to production standards. Thanks for watching!",
         body=f'<div class="center">{LOGO_BIG}<div class="big-title" style="font-size:34px">Rich. Grounded. Production-ready.</div>'
              '<div class="checklist">'
              '<div class="check"><span class="tick">✓</span> Grounded RAG with citations</div>'
              '<div class="check"><span class="tick">✓</span> PYQ practice &amp; mock tests</div>'
              '<div class="check"><span class="tick">✓</span> Spaced repetition &amp; flashcards</div>'
              '<div class="check"><span class="tick">✓</span> Planner, dashboard &amp; daily streaks</div>'
              '<div class="check"><span class="tick">✓</span> Voice, sketch, multilingual, Socratic</div>'
              '<div class="check"><span class="tick">✓</span> Feedback + RLHF export</div>'
              '</div>'
              '<div class="subtitle" style="margin-top:10px">Built for GateOverflow · gateoverflow.in</div></div>'),
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
    for tool, hint, is_path in [(CHROME, "Google Chrome", True), ("ffmpeg", "ffmpeg", False),
                                ("say", "say", False)]:
        if is_path and not Path(tool).exists():
            print(f"❌ {hint} not found at {tool}")
            return 1
        if not is_path and shutil.which(tool) is None:
            print(f"❌ {hint} not found on PATH")
            return 1

    if FRAMES.exists():
        shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True)

    total = len(SCENES)
    segments: list[Path] = []

    for i, sc in enumerate(SCENES, 1):
        stem = f"{i:02d}_{sc['key']}"
        html, png = FRAMES / f"{stem}.html", FRAMES / f"{stem}.png"
        aiff, seg = FRAMES / f"{stem}.aiff", FRAMES / f"{stem}.mp4"

        html.write_text(
            page(sc["body"], sc["title"], sc["sub"], i, total,
                 sc.get("center", False), sc.get("rail")),
            encoding="utf-8",
        )

        print(f"🎬 scene {i}/{total}: {sc['key']} — rendering")
        sh([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=2", f"--window-size={W},{H}",
            f"--screenshot={png}", f"file://{html}", "--virtual-time-budget=2500"])

        sh(["say", "-v", VOICE, "-o", str(aiff), sc["narration"]])
        dur = max(duration(aiff) + 1.1, sc.get("min", 3.5))

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

    print(f"\n✅ Done: {OUT}  ({duration(OUT):.1f}s, {total} scenes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
