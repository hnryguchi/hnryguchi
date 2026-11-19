"""Generate the profile's project cards and the animated terminal (SVG, light + dark).

    python scripts/cards.py
"""

from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets"

THEMES = {
    "dark": dict(bg="#0d1117", border="#30363d", fg="#e6edf3", muted="#9198a1", chip="#161b22", chipfg="#c9d1d9"),
    "light": dict(bg="#ffffff", border="#d1d9e0", fg="#1f2328", muted="#59636e", chip="#f6f8fa", chipfg="#31373d"),
}

# (file, title, two description lines, stack chips, status, accent colour)
CARDS = [
    ("portal", "Portal de gestão ambiental",
     ["A equipe revisa e publica programas e indicadores;", "cada cliente vê só o que foi aprovado."],
     ["Next.js", "TypeScript", "PostgreSQL", "Azure"], "em produção", "#2da44e"),
    ("mapa", "Mapa de operações marítimas",
     ["Relatórios por e-mail viram um mapa público,", "validados por regras e revisados por IA."],
     ["MapLibre", "WebGL2", "Logic Apps", "Claude"], "em produção", "#0969da"),
    ("agentes", "Agentes de e-mail",
     ["Anexos conferidos por um motor de regras e uma IA;", "o resultado vira rascunho para uma pessoa aprovar."],
     ["Python", "PowerShell", "Outlook", "Claude"], "uso diário", "#8250df"),
    ("coralguard", "CoralGuard",
     ["Estresse térmico nos recifes de coral do Brasil", "desde 1985, atualizado todo dia (NOAA)."],
     ["Python", "pandas", "Plotly", "Actions"], "ao vivo", "#e4572e"),
    ("metocean", "metocean-qc",
     ["Controle de qualidade de dados de boias, testado", "com dados reais e rodando todo dia."],
     ["Python", "pytest", "Docker", "Actions"], "código aberto", "#1f6feb"),
    ("aerys", "Aerys",
     ["Estação ambiental de baixo custo: protótipo físico", "com ESP32 e painel web. Jovens Cientistas Cariocas."],
     ["ESP32", "Arduino", "Next.js", "Supabase"], "protótipo", "#bf8700"),
    ("qrcode", "Ficha por QR Code",
     ["Fichas de papel viram formulário no celular, PDF fiel", "ao modelo e envio automático ao SharePoint."],
     ["Flask", "MS Graph", "Azure", "pytest"], "em produção", "#2da44e"),
    ("prompts", "Prompts de engenharia",
     ["Prompts para trabalhar com agentes de código:", "auditoria antes de mudar, aprovação, sem dado inventado."],
     ["Markdown"], "mantido", "#57606a"),
]

W, H = 400, 150


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def card(theme: str, title, lines, chips, status, accent) -> str:
    t = THEMES[theme]
    font = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f"<style>text{{font-family:{font}}}"
        ".bar{transform-origin:left;animation:g 1.2s ease-out both}@keyframes g{from{transform:scaleX(0)}}"
        "@media (prefers-reduced-motion:reduce){.bar{animation:none}}</style>",
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{t["bg"]}" stroke="{t["border"]}"/>',
        f'<rect class="bar" x="1" y="1" width="{W - 2}" height="4" rx="2" fill="{accent}"/>',
        f'<text x="18" y="39" font-size="16" font-weight="600" fill="{t["fg"]}">{esc(title)}</text>',
    ]
    sw = 12 + 6.4 * len(status)
    parts.append(f'<rect x="{W - 16 - sw:.0f}" y="22" width="{sw:.0f}" height="22" rx="11" fill="{accent}" '
                 'fill-opacity=".15"/>')
    parts.append(f'<text x="{W - 16 - sw / 2:.0f}" y="37" font-size="11" text-anchor="middle" fill="{accent}" '
                 f'font-weight="600">{esc(status)}</text>')
    for i, ln in enumerate(lines):
        parts.append(f'<text x="18" y="{70 + i * 18}" font-size="12.5" fill="{t["muted"]}">{esc(ln)}</text>')
    x = 18
    for c in chips:
        cw = 14 + 6.6 * len(c)
        parts.append(f'<rect x="{x}" y="112" width="{cw:.0f}" height="22" rx="6" fill="{t["chip"]}" '
                     f'stroke="{t["border"]}"/>')
        parts.append(f'<text x="{x + cw / 2:.0f}" y="127" font-size="11" text-anchor="middle" '
                     f'fill="{t["chipfg"]}">{esc(c)}</text>')
        x += cw + 6
    parts.append("</svg>")
    return "".join(parts)


# ---- animated terminal: each line appears in turn, like typing; real output from metocean-qc ----
TERM = [
    ("$ ", "whoami"),
    ("", "henry · biologia (UERJ) + ADS (UVA) · IC no NAPROA · equipe ambiental offshore"),
    ("$ ", "ls projetos/"),
    ("", "portal-ambiental/  mapa-maritimo/  agentes-email/  coralguard/  metocean-qc/  aerys/"),
    ("$ ", "metqc fetch 41010 && metqc check data/41010.txt"),
    ("", "41010: 6347 registros, 12 achados, 2 eventos  ✓ relatório gerado"),
]


def terminal(theme: str) -> str:
    dark = theme == "dark"
    bg, bar, fg = ("#0b0f14", "#161b22", "#c9d1d9") if dark else ("#1f2328", "#2d333b", "#e6edf3")
    prompt, out = ("#2dd4bf", "#8b949e") if dark else ("#5eead4", "#adbac7")
    w, lh, top = 840, 22, 52
    h = top + lh * len(TERM) + 20
    font = "ui-monospace,SFMono-Regular,Consolas,'Liberation Mono',monospace"
    css = [f"text{{font-family:{font};font-size:13.5px}}", ".l{opacity:0;animation:s .01s forwards}",
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
              f'<rect width="{w}" height="{h}" rx="10" fill="{bg}"/>',
              f'<rect width="{w}" height="30" rx="10" fill="{bar}"/><rect y="20" width="{w}" height="10" fill="{bar}"/>',
              '<circle cx="20" cy="15" r="5.5" fill="#ff5f57"/><circle cx="38" cy="15" r="5.5" fill="#febc2e"/>'
              '<circle cx="56" cy="15" r="5.5" fill="#28c840"/>',
              f'<text x="{w / 2}" y="20" text-anchor="middle" fill="{out}" style="font-size:12px">henry@hnryguchi: ~</text>',
              *body, "</svg>"]
    return "".join(parts)


if __name__ == "__main__":
    (OUT / "cards").mkdir(parents=True, exist_ok=True)
    for name, *spec in CARDS:
        for theme in THEMES:
            (OUT / "cards" / f"{name}-{theme}.svg").write_text(card(theme, *spec), encoding="utf-8")
    for theme in THEMES:
        (OUT / f"terminal-{theme}.svg").write_text(terminal(theme), encoding="utf-8")
    print(f"{len(CARDS)} cards x 2 themes + terminal written to {OUT}")
