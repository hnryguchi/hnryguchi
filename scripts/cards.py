"""Generate the profile's project cards, the animated terminal and the banner (SVG, one brand palette).

Fonts are embedded (see fonts.py), so the images look the same in GitHub's light and dark themes.

    python scripts/cards.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fonts import DISPLAY, MONO, SANS, embed  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "assets"

# Brand palette, matching the banner: deep navy with teal/sky accents.
BRAND = dict(bg="#081a2e", border="#16324f", fg="#f0f9ff", muted="#9cc3dc", chip="#0d2540", chipfg="#bae6fd")

# (file, title, two description lines, stack chips, status, accent colour)
CARDS = [
    ("portal", "Portal de gestão ambiental",
     ["Plataforma multi-tenant com RBAC por projeto,", "workflow de revisão/publicação e trilha de auditoria."],
     ["Next.js", "TypeScript", "Prisma", "PostgreSQL", "Azure"], "produção", "#3fb950"),
    ("mapa", "Mapa de operações marítimas",
     ["Ingestão por e-mail (Logic Apps), validação por regras,", "revisão por LLM e mapa WebGL2 sem redeploy."],
     ["MapLibre", "WebGL2", "Logic Apps", "Claude API"], "produção", "#58a6ff"),
    ("agentes", "Agentes LLM de e-mail",
     ["Motor de regras determinístico + segunda opinião", "do modelo; saída em rascunho com aprovação humana."],
     ["Python", "PowerShell", "Outlook COM", "Claude API"], "uso diário", "#bc8cff"),
    ("coralguard", "CoralGuard",
     ["Pipeline diário NOAA CRW: DHW, eventos de alerta e", "tendência de TSM em 7 recifes desde 1985."],
     ["Python", "pandas", "Plotly", "GitHub Actions"], "ao vivo", "#ff7b54"),
    ("metocean", "metocean-qc",
     ["QC de séries de boias no padrão QARTOD: range,", "spike, flat line e gaps. CI em 4 versões do Python."],
     ["Python", "pytest", "Docker", "GitHub Actions"], "open source", "#2dd4bf"),
    ("aerys", "Aerys",
     ["Estação IoT de baixo custo: firmware ESP32, ingestão", "autenticada e dashboard. Jovens Cientistas Cariocas."],
     ["ESP32", "C++", "Next.js", "Supabase"], "protótipo", "#e3b341"),
    ("qrcode", "Formulário por QR Code",
     ["Formulário mobile, PDF fiel ao template e upload", "automático via Microsoft Graph para o SharePoint."],
     ["Flask", "MS Graph", "Azure", "pytest"], "produção", "#3fb950"),
    ("prompts", "Engineering prompts",
     ["Templates para agentes de código: auditoria read-only,", "gates de aprovação e dados verificáveis."],
     ["Markdown", "Claude Code"], "mantido", "#8b949e"),
]

W, H = 400, 150


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def card(title, lines, chips, status, accent) -> str:
    t = BRAND
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f"<style>text{{font-family:{SANS}}}.d{{font-family:{DISPLAY}}}"
        ".bar{transform-origin:left;animation:g 1.2s ease-out both}@keyframes g{from{transform:scaleX(0)}}"
        "@media (prefers-reduced-motion:reduce){.bar{animation:none}}</style>",
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{t["bg"]}" stroke="{t["border"]}"/>',
        f'<rect class="bar" x="1" y="1" width="{W - 2}" height="3" rx="1.5" fill="{accent}"/>',
        f'<text class="d" x="18" y="39" font-size="17" font-weight="600" fill="{t["fg"]}">{esc(title)}</text>',
    ]
    sw = 14 + 6.2 * len(status)
    parts.append(f'<rect x="{W - 16 - sw:.0f}" y="22" width="{sw:.0f}" height="22" rx="11" fill="{accent}" '
                 'fill-opacity=".14"/>')
    parts.append(f'<text x="{W - 16 - sw / 2:.0f}" y="37" font-size="11" text-anchor="middle" fill="{accent}" '
                 f'font-weight="600">{esc(status)}</text>')
    for i, ln in enumerate(lines):
        parts.append(f'<text x="18" y="{70 + i * 18}" font-size="12" fill="{t["muted"]}">{esc(ln)}</text>')
    x = 18
    for c in chips:
        cw = 14 + 6.3 * len(c)
        parts.append(f'<rect x="{x}" y="112" width="{cw:.0f}" height="22" rx="6" fill="{t["chip"]}" '
                     f'stroke="{t["border"]}"/>')
        parts.append(f'<text x="{x + cw / 2:.0f}" y="127" font-size="11" text-anchor="middle" '
                     f'fill="{t["chipfg"]}">{esc(c)}</text>')
        x += cw + 6
    parts.append("</svg>")
    return embed("".join(parts))


# ---- animated terminal: each line appears in turn, like typing; real output from metocean-qc ----
TERM = [
    ("$ ", "whoami"),
    ("", "henry · engenharia de software e IA · biologia (UERJ) + ADS (UVA) · IC NAPROA"),
    ("$ ", "ls projetos/"),
    ("", "portal-ambiental/  mapa-maritimo/  agentes-email/  coralguard/  metocean-qc/  aerys/"),
    ("$ ", "metqc fetch 41010 && metqc check data/41010.txt"),
    ("", "41010: 6347 registros · 12 flags · 2 eventos  ✓ report.json report.md"),
]


def terminal() -> str:
    bg, bar, fg = "#06121f", "#0b1e33", "#e0f2fe"
    prompt, out = "#2dd4bf", "#8fb3cc"
    w, lh, top = 840, 22, 52
    h = top + lh * len(TERM) + 20
    css = [f"text{{font-family:{MONO};font-size:13px}}", ".l{opacity:0;animation:s .01s forwards}",
           "@keyframes s{to{opacity:1}}", ".cur{animation:b 1s steps(1) infinite}@keyframes b{50%{opacity:0}}",
           "@media (prefers-reduced-motion:reduce){.l{animation:none;opacity:1}.cur{animation:none}}"]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
             'aria-label="Terminal: whoami, lista de projetos e execução do metocean-qc">']
    body = []
    t = 0.3
    for i, (p, txt) in enumerate(TERM):
        y = top + i * lh
        color = fg if p else out
        delay = t
        t += 0.9 if p else 0.5
        body.append(f'<text class="l" style="animation-delay:{delay:.1f}s" x="20" y="{y}">'
                    f'<tspan fill="{prompt}">{esc(p)}</tspan><tspan fill="{color}">{esc(txt)}</tspan></text>')
    cy = top + lh * len(TERM)
    body.append(f'<text class="l" style="animation-delay:{t:.1f}s" x="20" y="{cy}"><tspan fill="{prompt}">$ </tspan>'
                f'<tspan class="cur" fill="{fg}">▍</tspan></text>')
    parts += ["<style>" + "".join(css) + "</style>",
              f'<rect width="{w}" height="{h}" rx="10" fill="{bg}" stroke="#16324f"/>',
              f'<rect width="{w}" height="30" rx="10" fill="{bar}"/><rect y="20" width="{w}" height="10" fill="{bar}"/>',
              '<circle cx="20" cy="15" r="5.5" fill="#ff5f57"/><circle cx="38" cy="15" r="5.5" fill="#febc2e"/>'
              '<circle cx="56" cy="15" r="5.5" fill="#28c840"/>',
              f'<text x="{w / 2}" y="20" text-anchor="middle" fill="{out}" style="font-size:12px">'
              "henry@hnryguchi: ~</text>",
              *body, "</svg>"]
    return embed("".join(parts))


def banner() -> str:
    """Brand banner from assets/src/banner-pt.svg, with the embedded fonts."""
    s = (OUT / "src" / "banner-pt.svg").read_text(encoding="utf-8")
    s = s.replace('font-family="Segoe UI,Helvetica,Arial,sans-serif"', f'font-family="{SANS}"')
    s = s.replace('font-family="ui-monospace,SFMono-Regular,Consolas,monospace"', f'font-family="{MONO}"')
    s = s.replace(f'font-family="{SANS}" font-size="54" font-weight="700"',
                  f'font-family="{DISPLAY}" font-size="58" font-weight="700"')
    return embed(s)


if __name__ == "__main__":
    (OUT / "cards").mkdir(parents=True, exist_ok=True)
    for name, *spec in CARDS:
        (OUT / "cards" / f"{name}.svg").write_text(card(*spec), encoding="utf-8")
    (OUT / "terminal.svg").write_text(terminal(), encoding="utf-8")
    (OUT / "banner.svg").write_text(banner(), encoding="utf-8")
    print(f"{len(CARDS)} cards + terminal + banner written to {OUT}")
