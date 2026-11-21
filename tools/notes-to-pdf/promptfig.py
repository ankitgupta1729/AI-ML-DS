#!/usr/bin/env python3
"""Draw the "prompt builder" figures of the prompt-engineering notes as SVG.

    python tools/notes-to-pdf/promptfig.py OUT.svg "Chip A,Chip B,…" [existing-layers]

The prompt box holds `existing-layers` filled bars (already added parts) plus a
dashed slot that the chips feed into; a response box sits on the right.
"""
from __future__ import annotations

import html
import sys

A = "#7c3aed"


def main() -> None:
    out, chips = sys.argv[1], [c.strip() for c in sys.argv[2].split(",")]
    layers = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    o = []
    ph = 60 + 22 * layers
    o.append(f'<rect x="20" y="10" width="200" height="{ph}" rx="6" fill="#fff" stroke="#0f172a"/>')
    o.append('<text x="120" y="28" text-anchor="middle" font-size="12" font-weight="600">Prompt</text>')
    for i in range(layers):
        o.append(f'<rect x="35" y="{36 + 22 * i}" width="170" height="16" rx="3" fill="#ede9fe" stroke="{A}"/>')
    sy = 36 + 22 * layers
    o.append(f'<rect x="35" y="{sy}" width="170" height="18" rx="3" fill="none" stroke="{A}" stroke-dasharray="4 3"/>')
    o.append(f'<text x="120" y="{sy + 13}" text-anchor="middle" font-size="10" fill="{A}">+ add</text>')
    o.append('<rect x="300" y="10" width="170" height="70" rx="6" fill="#fff" stroke="#0f172a"/>'
             '<text x="385" y="28" text-anchor="middle" font-size="12" font-weight="600">Response</text>')
    for i in range(3):
        o.append(f'<line x1="318" y1="{44 + 11 * i}" x2="452" y2="{44 + 11 * i}" stroke="#94a3b8"/>')
    o.append('<line x1="228" y1="45" x2="292" y2="45" stroke="#475569" marker-end="url(#m)"/>')
    cy = ph + 40
    o.append(f'<line x1="120" y1="{cy - 6}" x2="120" y2="{sy + 20}" stroke="#475569" marker-end="url(#m)"/>')
    x, y = 20, cy
    for c in chips:
        w = 14 + 7.2 * len(c)
        if x + w > 470:
            x, y = 20, y + 30
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="22" rx="4" fill="#f8fafc" stroke="#0f172a"/>'
                 f'<text x="{x + w / 2}" y="{y + 15}" text-anchor="middle" font-size="11">{html.escape(c)}</text>')
        x += w + 8
    h = y + 34
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 490 {h}" font-family="Inter, Arial, sans-serif">'
           '<defs><marker id="m" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
           'orient="auto"><path d="M0 0L10 5L0 10z" fill="#475569"/></marker></defs>'
           f'<rect width="100%" height="100%" fill="#fff"/>{"".join(o)}</svg>')
    with open(out, "w") as f:
        f.write(svg)


if __name__ == "__main__":
    main()
