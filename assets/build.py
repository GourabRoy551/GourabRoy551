"""Generates the animated SVGs used by the profile README.

    python assets/build.py

Writes assets/header-{dark,light}.svg and assets/cards/<slug>-{dark,light}.svg.
Edit HEADER / PROJECTS below and re-run to update the profile.
Pillow (optional) is used to measure text so lines wrap neatly.
"""

import math
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent

SANS = "Inter, 'Segoe UI', system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'SF Mono', Consolas, 'Liberation Mono', Menlo, monospace"

THEMES = {
    "dark": dict(
        bg="#0B0D12", card="#0F1218", border="#1E2330", grid="#1A1F2B",
        text="#E7E9EE", muted="#8A92A6", faint="#5A6275", pill="#121620",
        orb=0.38, cell="#161A24",
    ),
    "light": dict(
        bg="#FFFFFF", card="#FAFAFB", border="#E5E7EB", grid="#EEF0F3",
        text="#0B1220", muted="#5B6476", faint="#8A92A3", pill="#F4F5F7",
        orb=0.22, cell="#EEF0F4",
    ),
}
A1, A2 = "#8B5CF6", "#22D3EE"  # violet -> cyan accent
GREEN = "#22C55E"

# ---------------------------------------------------------------- content
HEADER = dict(
    status="Open to research internships · from Feb 2027",
    name="Gourab Roy",
    subtitle="ML researcher · Erasmus Mundus MSc in AI & Computer Vision",
    focus_prefix="Focused on",
    focus=[
        "explainable AI for vision–language models",
        "medical image analysis (CT / MRI)",
        "vision transformers & CLIP",
        "trustworthy, reproducible deep learning",
    ],
    metrics=[
        ("12", "peer-reviewed papers"),
        ("2 yrs", "research assistant"),
        ("4", "universities"),
        ("350+", "problems solved"),
    ],
)

PROJECTS = [
    dict(
        slug="banglacaption40k", title="BanglaCaption40K",
        kind="Vision–language · XAI", year="2026",
        desc="Bengali image–text retrieval benchmark on a multilingual CLIP-style "
             "model, with token-ablation and patch-perturbation explanations.",
        metrics=[("217K", "captions"), ("43.8K", "images"), ("6.2→17.6", "I→T R@1")],
        tags=["PyTorch", "CLIP", "XAI"],
    ),
    dict(
        slug="clip-soft-prefix", title="CLIP Soft-Prefix Attribution",
        kind="Prompt learning · Attribution", year="2026",
        desc="Learns a continuous soft prefix on frozen CLIP encoders for "
             "retrieval, then measures which caption tokens the prefix makes "
             "CLIP rely on.",
        metrics=[("0", "encoder weights tuned"), ("Token", "level attribution")],
        tags=["PyTorch", "CLIP", "Prompt learning"],
    ),
    dict(
        slug="siteguard-ai", title="SiteGuard AI",
        kind="Detection · ML lead", year="2026 — now",
        desc="Five-class PPE detection for construction sites with "
             "worker-to-PPE matching. YOLO26n/s vs YOLOv8n, served with "
             "FastAPI and Docker.",
        metrics=[("5", "PPE classes"), ("3", "detectors compared")],
        tags=["YOLO", "FastAPI", "Docker"],
    ),
    dict(
        slug="multiview-3d", title="Multi-View 3D Reconstruction",
        kind="3D vision", year="2026",
        desc="Calibration, RANSAC matching, epipolar geometry, pose "
             "estimation, sparse reconstruction and bundle adjustment.",
        metrics=[("4.47 px", "reprojection error"), ("672", "multi-view tracks")],
        tags=["MATLAB", "SfM", "Bundle adjustment"],
    ),
    dict(
        slug="ppg-hrv", title="Cardiac Autonomic Assessment",
        kind="Biomedical signals", year="2025",
        desc="Raw PPG to time- and frequency-domain HRV, testing how "
             "self-selected music shifts each subject's autonomic response.",
        metrics=[("10", "participants"), ("3", "sound conditions")],
        tags=["Python", "SciPy", "Statistics"],
    ),
    dict(
        slug="cerebralnet", title="CerebralNet",
        kind="Medical imaging · B.Sc. thesis", year="2023",
        desc="Deep-learning system that detects major abnormalities in brain "
             "CT and MRI scans by combining segmentation and classification.",
        metrics=[("CT + MRI", "modalities"), ("Seg + Cls", "two-stage")],
        tags=["Segmentation", "Classification", "Medical AI"],
    ),
]

# ---------------------------------------------------------------- text metrics
try:
    from PIL import ImageFont

    _FONTS = {}

    def text_w(s, size, bold=False, mono=False):
        name = ("consolab.ttf" if bold else "consola.ttf") if mono else \
               ("segoeuib.ttf" if bold else "segoeui.ttf")
        key = (name, size)
        if key not in _FONTS:
            try:
                _FONTS[key] = ImageFont.truetype(name, size)
            except OSError:
                _FONTS[key] = None
        f = _FONTS[key]
        if f is None:
            return len(s) * size * (0.6 if mono else 0.52)
        return f.getlength(s) * 1.06  # slack for wider fallback fonts
except ImportError:
    def text_w(s, size, bold=False, mono=False):
        return len(s) * size * (0.6 if mono else 0.52)


def wrap(s, size, width):
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if text_w(trial, size) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def t(x, y, s, size, fill, weight=400, family=SANS, anchor="start", extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>'
            f"{escape(s)}</text>")


# ---------------------------------------------------------------- header
def header(theme):
    c = THEMES[theme]
    W, H = 1200, 420
    p = []
    p.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(HEADER['name'])}, {escape(HEADER['subtitle'])}">
<defs>
  <linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{A1}"/><stop offset="1" stop-color="{A2}"/></linearGradient>
  <linearGradient id="accD" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{A1}"/><stop offset="1" stop-color="{A2}"/></linearGradient>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{A2}" stop-opacity="0"/><stop offset=".5" stop-color="{A2}" stop-opacity=".28"/><stop offset="1" stop-color="{A2}" stop-opacity="0"/></linearGradient>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{c['grid']}" stroke-width="1"/></pattern>
  <radialGradient id="fade" cx=".78" cy=".45" r=".7"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
  <mask id="gridMask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
  <filter id="blur" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="70"/></filter>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="20"/></clipPath>
  <clipPath id="hm"><rect x="876" y="76" width="268" height="268" rx="10"/></clipPath>
</defs>
<style>
  .rot {{ opacity: 0; }}
  .rot0 {{ opacity: 1; }}
  @media (prefers-reduced-motion: no-preference) {{
    .orb1 {{ animation: drift1 16s ease-in-out infinite; }}
    .orb2 {{ animation: drift2 19s ease-in-out infinite; }}
    .ring {{ transform-box: fill-box; transform-origin: center; animation: ping 2s cubic-bezier(0,0,.2,1) infinite; }}
    .rot {{ opacity: 0; animation: rot 14s ease-in-out infinite both; }}
    .cell {{ animation: pulse 3.2s ease-in-out infinite; }}
    .scan {{ animation: scan 4.5s linear infinite; }}
    .in {{ animation: up .9s cubic-bezier(.2,.7,.2,1) both; }}
  }}
  @keyframes drift1 {{ 50% {{ transform: translate(-60px, 40px); }} }}
  @keyframes drift2 {{ 50% {{ transform: translate(50px, -30px); }} }}
  @keyframes ping {{ 0% {{ transform: scale(1); opacity: .7; }} 80%,100% {{ transform: scale(3); opacity: 0; }} }}
  @keyframes rot {{ 0% {{ opacity: 0; transform: translateY(10px); }} 4%,21% {{ opacity: 1; transform: translateY(0); }} 25%,100% {{ opacity: 0; transform: translateY(-10px); }} }}
  @keyframes pulse {{ 50% {{ opacity: .3; }} }}
  @keyframes scan {{ from {{ transform: translateY(-60px); }} to {{ transform: translateY(330px); }} }}
  @keyframes up {{ from {{ opacity: 0; transform: translateY(14px); }} }}
</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="{c['bg']}"/>
  <rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gridMask)"/>
  <g filter="url(#blur)" opacity="{c['orb']}">
    <circle class="orb1" cx="980" cy="90" r="170" fill="{A1}"/>
    <circle class="orb2" cx="1080" cy="360" r="150" fill="{A2}"/>
  </g>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="19.5" fill="none" stroke="{c['border']}"/>''')

    # status pill
    st = HEADER["status"]
    pw = text_w(st, 14) + 52
    p.append(f'''<g class="in">
  <rect x="56" y="48" width="{pw:.0f}" height="34" rx="17" fill="{c['pill']}" stroke="{c['border']}"/>
  <circle class="ring" cx="77" cy="65" r="4" fill="{GREEN}"/>
  <circle cx="77" cy="65" r="4" fill="{GREEN}"/>
  {t(92, 70, st, 14, c['text'], 500)}
</g>''')

    # name + subtitle
    p.append(f'<g class="in" style="animation-delay:.08s">{t(52, 172, HEADER["name"], 78, c["text"], 700, extra=' letter-spacing=\"-2.5\"')}</g>')
    p.append(f'<g class="in" style="animation-delay:.16s">{t(56, 214, HEADER["subtitle"], 20, c["muted"])}</g>')

    # rotating focus line
    pre = HEADER["focus_prefix"]
    px = 56 + text_w(pre, 19, mono=True) + 12
    p.append(f'<g class="in" style="animation-delay:.24s">{t(56, 262, pre, 19, c["faint"], family=MONO)}')
    slot = 14 / len(HEADER["focus"])
    for i, s in enumerate(HEADER["focus"]):
        p.append(f'  <g class="rot{" rot0" if i == 0 else ""}" style="animation-delay:{i*slot:.2f}s">'
                 f'{t(px, 262, s, 19, "url(#acc)", 600, family=MONO)}</g>')
    p.append("</g>")

    # divider + metrics
    p.append(f'<line x1="56" y1="306" x2="820" y2="306" stroke="{c["border"]}"/>')
    for i, (num, label) in enumerate(HEADER["metrics"]):
        x = 56 + i * 192
        p.append(f'<g class="in" style="animation-delay:{.32 + i*.07:.2f}s">'
                 f'{t(x, 352, num, 30, c["text"], 700, extra=' letter-spacing=\"-0.5\"')}'
                 f'{t(x, 378, label.upper(), 11.5, c["muted"], 500, extra=' letter-spacing=\"1.4\"')}</g>')

    # attention-map heatmap: a saliency blob over an 8x8 patch grid
    n, size, gap, x0, y0 = 8, 28, 6, 878, 78
    cx, cy = 4.6, 3.2
    p.append('<g class="in" style="animation-delay:.4s">')
    for r in range(n):
        for col in range(n):
            x, y = x0 + col * (size + gap), y0 + r * (size + gap)
            d2 = (col - cx) ** 2 + (r - cy) ** 2
            v = math.exp(-d2 / 6.5) + 0.55 * math.exp(-((col - 1.8) ** 2 + (r - 5.6) ** 2) / 3.2)
            v = min(v, 1)
            p.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="6" fill="{c["cell"]}"/>')
            if v > 0.06:
                delay = math.sqrt(d2) * 0.18
                p.append(f'<g opacity="{0.15 + 0.85*v:.2f}"><rect class="cell" style="animation-delay:{delay:.2f}s" '
                         f'x="{x}" y="{y}" width="{size}" height="{size}" rx="6" fill="url(#accD)"/></g>')
    p.append(f'<g clip-path="url(#hm)"><rect class="scan" x="876" y="76" width="268" height="60" fill="url(#scan)"/></g>')
    p.append(t(1144, 372, "attention rollout · 8×8 patches", 11.5, c["faint"], family=MONO, anchor="end"))
    p.append("</g>")

    p.append("</svg>")
    return "\n".join(p)


# ---------------------------------------------------------------- project cards
def card(proj, idx, theme):
    c = THEMES[theme]
    W, H, P = 560, 300, 30
    uid = f"{proj['slug']}{theme}"
    p = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(proj['title'])}: {escape(proj['desc'])}">
<defs>
  <linearGradient id="a{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{A1}"/><stop offset="1" stop-color="{A2}"/></linearGradient>
  <linearGradient id="s{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{A2}" stop-opacity="0"/><stop offset=".5" stop-color="{A2}"/><stop offset="1" stop-color="{A1}" stop-opacity="0"/></linearGradient>
  <clipPath id="c{uid}"><rect width="{W}" height="{H}" rx="16"/></clipPath>
</defs>
<style>
  @media (prefers-reduced-motion: no-preference) {{
    .sh{uid} {{ animation: sh{uid} 7s ease-in-out {idx*1.1:.1f}s infinite; }}
    .in{uid} {{ animation: in{uid} .8s cubic-bezier(.2,.7,.2,1) {idx*.08:.2f}s both; }}
  }}
  @keyframes sh{uid} {{ 0% {{ transform: translateX(-200px); }} 60%,100% {{ transform: translateX({W}px); }} }}
  @keyframes in{uid} {{ from {{ opacity: 0; transform: translateY(10px); }} }}
</style>
<g clip-path="url(#c{uid})">
  <rect width="{W}" height="{H}" fill="{c['card']}"/>
  <rect width="{W}" height="2" fill="url(#a{uid})" opacity=".55"/>
  <rect class="sh{uid}" width="200" height="2" fill="url(#s{uid})"/>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="15.5" fill="none" stroke="{c['border']}"/>
<g class="in{uid}">''']

    p.append(t(P, 46, f"{idx+1:02d}", 13, c["faint"], 500, MONO))
    p.append(t(P + 30, 46, proj["kind"].upper(), 11.5, f"url(#a{uid})", 600,
               extra=' letter-spacing="1.5"'))
    p.append(t(W - P, 46, proj["year"], 13, c["faint"], 400, MONO, anchor="end"))
    p.append(t(P, 92, proj["title"], 27, c["text"], 700, extra=' letter-spacing="-0.6"'))

    lines = wrap(proj["desc"], 17, W - 2 * P)[:3]
    for i, line in enumerate(lines):
        p.append(t(P, 128 + i * 25, line, 17, c["muted"]))

    mx = P
    for num, label in proj["metrics"]:
        p.append(t(mx, 226, num, 21, c["text"], 700, extra=' letter-spacing="-0.3"'))
        p.append(t(mx, 246, label, 13, c["faint"]))
        mx += max(text_w(num, 21, bold=True), text_w(label, 13)) + 32

    tx = P
    for tag in proj["tags"]:
        tw = text_w(tag, 12, mono=True) + 20
        p.append(f'<rect x="{tx:.1f}" y="260" width="{tw:.1f}" height="24" rx="12" fill="none" stroke="{c["border"]}"/>')
        p.append(t(tx + tw / 2, 276, tag, 12, c["muted"], 400, MONO, anchor="middle"))
        tx += tw + 8

    p.append("</g></svg>")
    return "\n".join(p)


def main():
    (OUT / "cards").mkdir(exist_ok=True)
    for theme in THEMES:
        (OUT / f"header-{theme}.svg").write_text(header(theme), encoding="utf-8")
        for i, proj in enumerate(PROJECTS):
            (OUT / "cards" / f"{proj['slug']}-{theme}.svg").write_text(card(proj, i, theme), encoding="utf-8")
    print(f"wrote header + {len(PROJECTS)} cards x {len(THEMES)} themes")


if __name__ == "__main__":
    main()
