"""Embed subsetted web fonts in an SVG, so it renders the same inside <img> on GitHub (no network access there).

Fonts (SIL Open Font License): Inter, Space Grotesk, JetBrains Mono, from @fontsource on jsdelivr.
They are cached in .fontcache/ (git-ignored); only the glyphs each SVG uses are embedded.
"""

from __future__ import annotations

import base64
import html
import io
import re
import urllib.request
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

CACHE = Path(__file__).resolve().parents[1] / ".fontcache"
CDN = "https://cdn.jsdelivr.net/npm/@fontsource/{pkg}@5.0.18/files/{pkg}-latin-{w}-normal.woff2"
FAMILIES = {  # css family -> (fontsource package, weights)
    "Inter": ("inter", (400, 600)),
    "Space Grotesk": ("space-grotesk", (600, 700)),
    "JetBrains Mono": ("jetbrains-mono", (400, 700)),
}
SANS = "'Inter',-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
DISPLAY = "'Space Grotesk','Inter',-apple-system,'Segoe UI',sans-serif"
MONO = "'JetBrains Mono',ui-monospace,SFMono-Regular,Consolas,monospace"


def _font_file(pkg: str, weight: int) -> Path:
    f = CACHE / f"{pkg}-latin-{weight}-normal.woff2"
    if not f.exists():
        CACHE.mkdir(exist_ok=True)
        with urllib.request.urlopen(CDN.format(pkg=pkg, w=weight), timeout=30) as r:
            f.write_bytes(r.read())
    return f


def _subset_b64(path: Path, chars: str) -> str:
    font = TTFont(path)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt"]
    sub = subset.Subsetter(opts)
    sub.populate(text=chars)
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def embed(svg: str) -> str:
    """Add @font-face rules (subset to the SVG's text) for the families referenced in it."""
    text = "".join(html.unescape(t) for t in re.findall(r">([^<]+)<", svg)) + " 0123456789"
    rules = []
    for family, (pkg, weights) in FAMILIES.items():
        if f"'{family}'" not in svg:
            continue
        for w in weights:
            data = _subset_b64(_font_file(pkg, w), text)
            rules.append(f"@font-face{{font-family:'{family}';font-weight:{w};"
                         f"src:url(data:font/woff2;base64,{data}) format('woff2')}}")
    if not rules:
        return svg
    css = "<style>" + "".join(rules) + "</style>"
    i = svg.index(">", svg.index("<svg")) + 1
    return svg[:i] + css + svg[i:]
