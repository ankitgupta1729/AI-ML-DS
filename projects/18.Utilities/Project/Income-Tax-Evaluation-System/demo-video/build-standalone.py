#!/usr/bin/env python3
"""Inline css+js into one self-contained, CSP-safe index.html for static hosts."""
import re, pathlib
base = pathlib.Path(__file__).resolve().parent.parent / "webapp"
out  = pathlib.Path(__file__).resolve().parent.parent / "dist" / "index.html"
out.parent.mkdir(parents=True, exist_ok=True)

html = (base/"index.html").read_text()
css  = (base/"css/styles.css").read_text()
js   = "\n".join((base/f"js/{f}").read_text() for f in ["tax.js","db.js","app.js"])

html = html.replace('<link rel="stylesheet" href="css/styles.css">', "<style>\n"+css+"\n</style>")
html = re.sub(r'\s*<!-- tax engine.*?<script src="js/app\.js"></script>',
              lambda m: "\n<script>\n"+js+"\n</script>", html, flags=re.S)
out.write_text(html)
ext = [u for u in re.findall(r'(?:src|href)="([^"]+)"', html) if not u.startswith(("data:", "#"))]
print(f"built {out} ({out.stat().st_size/1024:.0f} KB)")
print("external refs:", ext or "none (CSP-safe)")
