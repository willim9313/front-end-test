"""Engraving-style ornaments for this page, drawn from scratch as SVG.

Writes ink-bat.svg, ink-corner.svg, ink-dropcap-t.svg (black on transparent;
the page uses them as alpha masks filled with the theme ink). Render each with
  node ../../../tools/render-svg.js ink-bat.svg ../assets/ink-bat.png
"""
import math
import random

rnd = random.Random(3)
K = 'fill="none" stroke="#000" stroke-linecap="round" stroke-linejoin="round"'


def svg(w, h, body, scale=2):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w * scale}" height="{h * scale}" viewBox="0 0 {w} {h}">'
            + body + "</svg>")


def hatch_clip(cid, path, angle, gap, x0, y0, x1, y1, sw=0.6):
    """Parallel engraving lines clipped to a path."""
    lines = []
    a = math.radians(angle)
    dx, dy = math.cos(a), math.sin(a)
    span = max(x1 - x0, y1 - y0) * 1.6
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    k = -span
    while k < span:
        px, py = cx - dy * k, cy + dx * k
        lines.append(f"M{px - dx * span:.1f} {py - dy * span:.1f} L{px + dx * span:.1f} {py + dy * span:.1f}")
        k += gap
    return (f'<clipPath id="{cid}"><path d="{path}"/></clipPath>'
            f'<path d="{" ".join(lines)}" {K} stroke-width="{sw}" clip-path="url(#{cid})"/>')


# ---------------- bat (324 x 138) ----------------
def wing(side):
    s = side
    cx = 162
    pts = [(cx + s * 14, 50), (cx + s * 60, 22), (cx + s * 110, 12), (cx + s * 150, 30), (cx + s * 158, 70)]
    # finger tips along the trailing edge, scalloped membrane between them
    tips = [(cx + s * 158, 70), (cx + s * 130, 92), (cx + s * 96, 100), (cx + s * 60, 94), (cx + s * 22, 80)]
    d = f"M{cx + s * 12} 46 C {cx + s * 50} 18 {cx + s * 100} 6 {cx + s * 150} 28 L {tips[0][0]} {tips[0][1]}"
    for (x0, y0), (x1, y1) in zip(tips, tips[1:]):
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - 14
        d += f" Q {mx} {my} {x1} {y1}"
    d += f" L {cx + s * 12} 66 Z"
    bones = "".join(f'<path d="M{cx + s * 40} 30 Q {(cx + s * 40 + x) / 2} {(30 + y) / 2 - 6} {x} {y}" {K} stroke-width="1.6"/>' for x, y in tips[:4])
    return d, bones


body = []
for side, cid in ((-1, "wl"), (1, "wr")):
    d, bones = wing(side)
    body.append(f'<path d="{d}" fill="#000" fill-opacity="0.08" stroke="#000" stroke-width="2"/>')
    body.append(hatch_clip(cid, d, 20 if side < 0 else 160, 2.6, 0, 0, 324, 138, 0.7))
    body.append(bones)
    body.append(f'<path d="M{162 + side * 40} 30 L{162 + side * 50} 20" {K} stroke-width="1.8"/>')  # thumb claw
# body, head, ears, feet
body.append('<path d="M150 44 C 148 70 152 96 162 112 C 172 96 176 70 174 44 C 170 36 154 36 150 44 Z" fill="#000"/>')
body.append('<path d="M150 42 C 150 28 156 22 162 22 C 168 22 174 28 174 42 Z" fill="#000"/>')
body.append('<path d="M152 30 L 146 8 L 158 24 M172 30 L 178 8 L 166 24" fill="#000" stroke="#000" stroke-width="1.5"/>')
body.append('<circle cx="157" cy="32" r="1.8" fill="#fff"/><circle cx="167" cy="32" r="1.8" fill="#fff"/>')
body.append(f'<path d="M156 112 l-4 10 M162 114 v10 M168 112 l4 10" {K} stroke-width="1.6"/>')
# fur strokes on the body
for _ in range(40):
    x = rnd.uniform(152, 172); y = rnd.uniform(46, 104)
    body.append(f'<path d="M{x:.1f} {y:.1f} l{rnd.uniform(-1.5, 1.5):.1f} 3" stroke="#fff" stroke-width="0.6"/>')
open("ink-bat.svg", "w").write(svg(324, 138, "".join(body)))

# ---------------- corner vine (320 x 290) ----------------
out = []
stem = "M14 284 C 10 220 22 150 18 96 C 16 56 30 24 70 16 C 130 6 200 22 300 14"
out.append(f'<path d="{stem}" {K} stroke-width="3"/>')
out.append(f'<path d="M18 120 C 40 110 52 92 50 70 M60 18 C 70 40 92 46 110 40 M200 20 C 214 36 236 40 252 32" {K} stroke-width="1.8"/>')


def leaf(x, y, ang, L=26, w=9):
    a = math.radians(ang)
    tx, ty = x + L * math.cos(a), y + L * math.sin(a)
    nx, ny = -math.sin(a) * w, math.cos(a) * w
    mx, my = (x + tx) / 2, (y + ty) / 2
    d = f"M{x:.1f} {y:.1f} Q {mx + nx:.1f} {my + ny:.1f} {tx:.1f} {ty:.1f} Q {mx - nx:.1f} {my - ny:.1f} {x:.1f} {y:.1f} Z"
    vein = f"M{x:.1f} {y:.1f} L{tx:.1f} {ty:.1f}"
    side = "".join(f"M{x + (tx - x) * t:.1f} {y + (ty - y) * t:.1f} l{nx * 0.6 + (tx - x) * 0.12:.1f} {ny * 0.6 + (ty - y) * 0.12:.1f}" for t in (0.3, 0.5, 0.7))
    return (f'<path d="{d}" fill="#000" fill-opacity="0.12" stroke="#000" stroke-width="1.4"/>'
            f'<path d="{vein} {side}" {K} stroke-width="0.8"/>')


for x, y, a in [(16, 250, 200), (16, 226, -20), (20, 190, 195), (18, 160, -25), (18, 130, 205), (22, 84, -40),
                (36, 30, 250), (92, 12, -80), (120, 10, 70), (160, 14, -70), (196, 18, 80), (236, 18, -75), (276, 16, 60),
                (50, 70, 10), (110, 40, 40), (252, 32, 30)]:
    out.append(leaf(x, y, a))
# berries
for x, y in [(52, 96), (58, 102), (48, 104), (150, 34), (156, 40), (146, 42), (290, 30), (284, 36)]:
    out.append(f'<circle cx="{x}" cy="{y}" r="3.6" fill="#000"/><circle cx="{x - 1}" cy="{y - 1}" r="1" fill="#fff"/>')
# a moth resting on the vine
mx, my = 96, 70
for s in (-1, 1):
    wd = f"M{mx} {my} C {mx + s * 18} {my - 22} {mx + s * 34} {my - 10} {mx + s * 30} {my + 4} C {mx + s * 24} {my + 14} {mx + s * 8} {my + 10} {mx} {my} Z"
    out.append(f'<path d="{wd}" fill="#000" fill-opacity="0.1" stroke="#000" stroke-width="1.4"/>')
    out.append(hatch_clip(f"m{s + 1}", wd, 60 if s < 0 else 120, 2.2, mx - 40, my - 30, mx + 40, my + 20, 0.6))
    out.append(f'<circle cx="{mx + s * 20}" cy="{my - 4}" r="3" fill="none" stroke="#000" stroke-width="1"/>')
out.append(f'<path d="M{mx} {my - 6} v18" stroke="#000" stroke-width="3.4" stroke-linecap="round"/>')
out.append(f'<path d="M{mx - 1} {my - 6} q -6 -10 -12 -12 M{mx + 1} {my - 6} q 6 -10 12 -12" {K} stroke-width="0.9"/>')
open("ink-corner.svg", "w").write(svg(320, 290, '<g transform="translate(12 14) scale(0.95)">' + "".join(out) + "</g>"))

# ---------------- drop cap T (130 x 132) ----------------
d = []
frame = "M6 6 H124 V126 H6 Z"
d.append(f'<path d="{frame}" {K} stroke-width="3"/>')
d.append(f'<path d="M12 12 H118 V120 H12 Z" {K} stroke-width="1"/>')
d.append(hatch_clip("bg", "M12 12 H118 V120 H12 Z", 45, 3.2, 0, 0, 130, 132, 0.7))
# leaf sprigs in the field
for x, y, a in [(24, 96, -60), (30, 70, -30), (100, 96, 240), (96, 70, 210), (40, 108, -10), (88, 108, 190)]:
    d.append(leaf(x, y, a, L=18, w=6))
# the letter, knocked out of the hatching with a white halo
T = "M22 24 H108 V44 H100 C 98 36 92 33 82 33 H72 V100 C 72 106 76 108 84 108 V114 H46 V108 C 54 108 58 106 58 100 V33 H48 C 38 33 32 36 30 44 H22 Z"
d.append(f'<path d="{T}" fill="none" stroke="#fff" stroke-width="7" stroke-linejoin="round"/>')
d.append(f'<path d="{T}" fill="#000"/>')
d.append(f'<path d="M62 40 V100 M68 40 V100" stroke="#fff" stroke-width="0.8"/>')
open("ink-dropcap-t.svg", "w").write(svg(130, 132, "".join(d)))
print("ok")
