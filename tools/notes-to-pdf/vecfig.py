#!/usr/bin/env python3
"""Draw small 2-D "vectors in a plane" figures as SVG for the digital notes.

    python tools/notes-to-pdf/vecfig.py OUT.svg 'title' 'label:x,y[:v]' ... [--panels N]

Each item is a point with a label; ':v' also draws the ray from the origin.
Several panels are separated by '|' items and drawn side by side.
"""
from __future__ import annotations

import html
import re
import sys

W, H, PAD = 220, 170, 26
ACC, INK, MUT = "#7c3aed", "#0f172a", "#64748b"


def panel(items, ox, title):
    pts = [(lbl, float(x), float(y), v) for lbl, x, y, v in items]
    mx = max([p[1] for p in pts] + [1]) * 1.15
    my = max([p[2] for p in pts] + [1]) * 1.15
    sx = lambda x: ox + PAD + x / mx * (W - 2 * PAD)
    sy = lambda y: H - PAD - y / my * (H - 2 * PAD - 10)
    o = [f'<line x1="{ox+PAD}" y1="{H-PAD}" x2="{ox+W-8}" y2="{H-PAD}" stroke="{MUT}" marker-end="url(#a)"/>',
         f'<line x1="{ox+PAD}" y1="{H-PAD}" x2="{ox+PAD}" y2="14" stroke="{MUT}" marker-end="url(#a)"/>']
    if title:
        o.append(f'<text x="{ox+W/2}" y="{H-6}" text-anchor="middle" fill="{MUT}" font-size="11">'
                 f'{html.escape(title)}</text>')
    for lbl, x, y, v in pts:
        if v:
            o.append(f'<line x1="{sx(0)}" y1="{sy(0)}" x2="{sx(x)}" y2="{sy(y)}" stroke="{ACC}" stroke-width="1.6"/>')
        o.append(f'<circle cx="{sx(x)}" cy="{sy(y)}" r="3.5" fill="{ACC}"/>')
        o.append(f'<text x="{sx(x)+6}" y="{sy(y)-6}" fill="{INK}" font-size="12">{html.escape(lbl)}</text>')
    return o


def main():
    out, *args = sys.argv[1:]
    panels, cur, title = [], [], ""
    for a in args:
        if a.startswith("|"):
            panels.append((cur, title))
            cur, title = [], a[1:]
            continue
        m = re.fullmatch(r"(.+):(-?[\d.]+),(-?[\d.]+)(:v)?", a)
        if not m:
            title = a
            continue
        cur.append((m.group(1), m.group(2), m.group(3), bool(m.group(4))))
    panels.append((cur, title))
    body = []
    for i, (items, t) in enumerate(panels):
        body += panel(items, i * W, t)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W*len(panels)} {H}" '
           f'font-family="Inter, Arial, sans-serif"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" '
           f'markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{MUT}"/></marker></defs>'
           f'<rect width="100%" height="100%" fill="#fff"/>{"".join(body)}</svg>')
    open(out, "w").write(svg)


if __name__ == "__main__":
    main()
