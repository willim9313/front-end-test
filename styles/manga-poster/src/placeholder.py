"""Placeholders for this page's three illustrations.

The page used to ship a from-scratch redraw (src/gen.py, removed): it did not
carry the reference's style, so the public page now shows an empty mist field
with the credit instead. The real art stays local only (local-original/, see
overview/local-original.js).

Writes ../assets/hero-figures.jpg, still-horse.jpg, still-knight.jpg at the
sizes index.html expects. Run from this folder:  uv run python placeholder.py
(renders with headless Edge through tools/render_svg.py, or Node + tools/render-svg.js)
"""
import subprocess
import sys
from pathlib import Path

MIST, MIST_HI, SKY, INK = "#d4dee1", "#e3eaec", "#6e8c94", "#1c1c1e"
HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[2] / "tools"


def page(w, h, label):
    """mist field, a dashed frame inside the radial fade, the credit in the middle"""
    m = round(min(w, h) * 0.2)
    cx, cy = w / 2, h / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<rect width="{w}" height="{h}" fill="{MIST}"/>'
            f'<rect x="{m}" y="{m}" width="{w - 2 * m}" height="{h - 2 * m}" fill="{MIST_HI}" '
            f'stroke="{SKY}" stroke-width="2" stroke-dasharray="8 6"/>'
            f'<g font-family="Arial, Helvetica, sans-serif" text-anchor="middle" fill="{INK}">'
            f'<text x="{cx}" y="{cy - 6}" font-size="{max(13, w // 40)}" font-weight="700" '
            f'letter-spacing="2">{label}</text>'
            f'<text x="{cx}" y="{cy + 18}" font-size="{max(11, w // 60)}" fill="{SKY}">'
            f'illustration not included · original by DeadKatBarks</text>'
            f'</g></svg>')


def render(svg, out):
    tmp = HERE / "tmp.svg"
    tmp.write_text(svg, encoding="utf-8")
    try:
        sys.path.insert(0, str(TOOLS))
        from render_svg import render as edge_render
        edge_render(tmp, HERE / out)
    except ImportError:
        subprocess.run(["node", str(TOOLS / "render-svg.js"), str(tmp), str(HERE / out)], check=True, stdout=subprocess.DEVNULL)
    tmp.unlink()


render(page(848, 818, "HORSE AND KNIGHT, FROM ABOVE"), "../assets/hero-figures.jpg")
render(page(360, 380, "THE HORSE"), "../assets/still-horse.jpg")
render(page(380, 340, "THE KNIGHT"), "../assets/still-knight.jpg")
print("ok")
