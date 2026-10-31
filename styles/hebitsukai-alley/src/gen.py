"""Original one-point-perspective alley for this page, in five flat colours.

Draws scene.svg (986x1200) using exactly the five palette colours, renders it
at 2x, then splits it into four alpha layers (navy, orange, peach, mint) by
nearest colour; paper is the background. Layers are written to ../assets.
All sign names are invented for this page.

  uv run python gen.py        (needs node + Playwright for the render step)
"""
import math
import random
import subprocess

from PIL import Image

W, H = 986, 1200
VP = (493, 420)
PAPER, NAVY, ORANGE, PEACH, MINT = "#F2FCF8", "#023D5C", "#F86C42", "#FCCC9A", "#A8EAE0"
rnd = random.Random(8)
o = []
FONT = 'font-family="IPAGothic, IPAPGothic, sans-serif" font-weight="700"'


def ytop(x):        # roofline: from (0,130) towards the vanishing point
    return 130 + (VP[1] - 30 - 130) * x / VP[0]


def ybot(x):        # where the wall meets the street
    return 1200 + (x - 250) * (452 - 1200) / (468 - 250)


def P(x, v, side):
    """Point on a wall at screen x (left-wall coordinates) and height v (0 top, 1 street)."""
    y = ytop(x) + (ybot(x) - ytop(x)) * v
    return (x if side < 0 else W - x, y)


def quad(x0, x1, v0, v1, side, fill, stroke=NAVY, sw=3):
    pts = [P(x0, v0, side), P(x1, v0, side), P(x1, v1, side), P(x0, v1, side)]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'


def blade(x, v0, v1, side, w, fill, text, ink, size):
    """A vertical sign sticking out of the wall, seen face-on, with vertical text."""
    (px, py0), (_, py1) = P(x, v0, side), P(x, v1, side)
    h = py1 - py0
    bx = px if side < 0 else px - w
    s = [f'<rect x="{bx:.1f}" y="{py0:.1f}" width="{w}" height="{h:.1f}" rx="3" fill="{fill}" stroke="{NAVY}" stroke-width="3"/>']
    arm = (px, py0 + 6)
    s.append(f'<path d="M{arm[0]:.1f} {arm[1]:.1f} h{(w if side < 0 else -w) * 0.2:.1f}" stroke="{NAVY}" stroke-width="3"/>')
    n = len(text)
    step = min(size * 1.05, (h - 10) / max(n, 1))
    for i, ch in enumerate(text):
        s.append(f'<text x="{bx + w / 2:.1f}" y="{py0 + 8 + step * (i + 0.82):.1f}" font-size="{min(size, step):.1f}" {FONT} '
                 f'fill="{ink}" text-anchor="middle">{ch}</text>')
    return "".join(s)


# ---------- sky, wires ----------
o.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
o.append(f'<path d="M0 0 H{W} V130 L{W - VP[0] + 40} {ytop(VP[0] - 40):.0f} L{VP[0] - 40} {ytop(VP[0] - 40):.0f} L0 130 Z" fill="{NAVY}"/>')
for _ in range(30):
    x = rnd.uniform(60, 920); y = rnd.uniform(10, 120)
    if y < ytop(min(x, W - x)) - 10:
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(1.2, 2.6):.1f}" fill="{PAPER}"/>')
o.append(f'<circle cx="760" cy="62" r="22" fill="{PEACH}"/>')

# ---------- walls ----------
for side in (-1, 1):
    wall = [P(0, 0, side), P(VP[0] - 40, 0, side), P(VP[0] - 40, 1, side), P(250, 1, side), (0 if side < 0 else W, H)]
    o.append(f'<path d="M{" L".join(f"{x:.1f} {y:.1f}" for x, y in wall)} Z" fill="{PAPER}" stroke="{NAVY}" stroke-width="4"/>')
    # buildings: alternating facade colours with dark windows
    edges = [0, 150, 270, 350, 405, 440, 453]
    for k, (x0, x1) in enumerate(zip(edges, edges[1:])):
        face = [MINT, PEACH, PAPER][(k + (side > 0)) % 3]
        o.append(quad(x0, x1, 0.0, 0.62, side, face))
        # windows on the upper floors
        for v0 in (0.08, 0.3):
            o.append(quad(x0 + (x1 - x0) * 0.2, x0 + (x1 - x0) * 0.75, v0, v0 + 0.12, side, NAVY, sw=2))
            o.append(quad(x0 + (x1 - x0) * 0.2, x0 + (x1 - x0) * 0.75, v0 + 0.085, v0 + 0.12, side, ORANGE if (k + side) % 2 else MINT, sw=2))
        # ground floor: shutter or doorway in shadow, striped awning above
        o.append(quad(x0, x1, 0.62, 1.0, side, NAVY, sw=2))
        o.append(quad(x0 + (x1 - x0) * 0.15, x0 + (x1 - x0) * 0.85, 0.7, 1.0, side, PEACH if k % 2 else MINT, sw=2))
        stripes = 6
        for i in range(stripes):
            a = x0 + (x1 - x0) * i / stripes
            b = x0 + (x1 - x0) * (i + 1) / stripes
            o.append(quad(a, b, 0.56, 0.66, side, ORANGE if i % 2 == 0 else PAPER, sw=1.5))
    # air-conditioner boxes
    for x, v in [(60, 0.46), (300, 0.5), (420, 0.48)]:
        o.append(quad(x, x + (24 if x < 300 else 8), v, v + 0.07, side, PAPER, sw=2))
    # pipes running along the wall
    for x in (140, 345):
        a, b = P(x, 0.02, side), P(x, 0.62, side)
        o.append(f'<path d="M{a[0]:.1f} {a[1]:.1f} L{b[0]:.1f} {b[1]:.1f}" stroke="{NAVY}" stroke-width="5"/>')

# ---------- blade signs (invented names) ----------
left = [(110, 0.04, 0.42, 66, ORANGE, "喫茶灯台", PAPER, 42), (215, 0.1, 0.44, 48, MINT, "麺処七福", NAVY, 30),
        (318, 0.08, 0.4, 32, PEACH, "酒の店", NAVY, 20), (380, 0.12, 0.42, 22, ORANGE, "たばこ", PAPER, 14),
        (424, 0.14, 0.44, 14, MINT, "質", NAVY, 10)]
right = [(90, 0.06, 0.44, 70, MINT, "焼鳥とり吉", NAVY, 40), (200, 0.08, 0.42, 50, ORANGE, "スナック千鶴", PAPER, 21),
         (305, 0.1, 0.42, 34, PEACH, "湯", NAVY, 26), (372, 0.12, 0.42, 22, ORANGE, "古本", PAPER, 14),
         (420, 0.14, 0.44, 14, MINT, "宿", NAVY, 10)]
for x, v0, v1, w, f, t, ink, sz in left:
    o.append(blade(x, v0, v1, -1, w, f, t, ink, sz))
for x, v0, v1, w, f, t, ink, sz in right:
    o.append(blade(x, v0, v1, 1, w, f, t, ink, sz))

# flat signs over the awnings, with English to mix scripts like a real side street
for side, x0, x1, txt, f, ink in [(-1, 0, 150, "BAR NAMI", PEACH, NAVY), (1, 0, 150, "COFFEE", ORANGE, PAPER), (-1, 150, 270, "KOMA", MINT, NAVY), (1, 150, 270, "GYOZA", PEACH, NAVY)]:
    o.append(quad(x0 + 8, x1 - 8, 0.49, 0.555, side, f))
    (ax, ay), (bx, by) = P(x0 + 8, 0.522, side), P(x1 - 8, 0.522, side)
    ang = math.degrees(math.atan2(by - ay, bx - ax))
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    cx, cy = (ax + bx) / 2, (ay + by) / 2
    size = abs(bx - ax) / (len(txt) * 0.75)
    o.append(f'<text x="0" y="0" transform="translate({cx:.1f} {cy:.1f}) rotate({ang:.1f})" font-size="{min(size, 30):.1f}" '
             f'{FONT} fill="{ink}" text-anchor="middle" dominant-baseline="central" letter-spacing="1">{txt}</text>')

# ---------- lantern string and wires across the alley ----------
for k, (xl, vl, sag) in enumerate([(200, 0.18, 70), (330, 0.2, 40), (410, 0.24, 18)]):
    a, b = P(xl, vl, -1), P(xl, vl, 1)
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + sag
    o.append(f'<path d="M{a[0]:.1f} {a[1]:.1f} Q {mx:.1f} {my + sag:.1f} {b[0]:.1f} {b[1]:.1f}" stroke="{NAVY}" stroke-width="{3 - k * 0.6:.1f}" fill="none"/>')
    if k < 2:
        n = 7 if k == 0 else 5
        for i in range(1, n):
            t = i / n
            x = (1 - t) ** 2 * a[0] + 2 * (1 - t) * t * mx + t * t * b[0]
            y = (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * (my + sag) + t * t * b[1]
            r = 13 if k == 0 else 8
            o.append(f'<ellipse cx="{x:.1f}" cy="{y + r:.1f}" rx="{r * 0.8:.1f}" ry="{r:.1f}" fill="{ORANGE if i % 2 else PEACH}" stroke="{NAVY}" stroke-width="2"/>')

# ---------- street ----------
for x in (300, 400, 586, 686):
    o.append(f'<path d="M{x} {H} L{VP[0] + (x - 493) * 0.05:.1f} 470" stroke="{MINT}" stroke-width="3"/>')
o.append(f'<ellipse cx="560" cy="1110" rx="46" ry="14" fill="{NAVY}"/><ellipse cx="560" cy="1108" rx="36" ry="9" fill="{MINT}"/>')
for x, y in [(380, 1000), (620, 880), (430, 760)]:
    o.append(f'<rect x="{x}" y="{y}" width="26" height="18" fill="{PEACH}" stroke="{NAVY}" stroke-width="2"/>')
# a cat by a doorway
o.append(f'<path d="M318 1060 c 0 -26 34 -26 34 0 Z" fill="{NAVY}"/><path d="M322 1040 l 4 -10 l 6 8 Z M342 1040 l 4 -10 l 4 10 Z" fill="{NAVY}"/>')
o.append(f'<path d="M352 1056 q 20 -2 18 -20" stroke="{NAVY}" stroke-width="3" fill="none"/>')

# the one person: a small kid in a mint coat with an orange bag, looking up
fx, fy = 493, 900
o.append(f'<ellipse cx="{fx}" cy="{fy + 2}" rx="20" ry="5" fill="{MINT}"/>')
o.append(f'<path d="M{fx - 12} {fy - 48} L{fx + 12} {fy - 48} L{fx + 16} {fy - 12} L{fx - 16} {fy - 12} Z" fill="{MINT}" stroke="{NAVY}" stroke-width="2.5"/>')
o.append(f'<path d="M{fx - 7} {fy - 12} v12 M{fx + 7} {fy - 12} v12" stroke="{NAVY}" stroke-width="4"/>')
o.append(f'<circle cx="{fx}" cy="{fy - 60}" r="12" fill="{PEACH}" stroke="{NAVY}" stroke-width="2.5"/>')
o.append(f'<path d="M{fx - 12} {fy - 60} c 0 -18 24 -18 24 0 c -6 -6 -18 -6 -24 0 Z" fill="{NAVY}"/>')
o.append(f'<rect x="{fx + 12}" y="{fy - 36}" width="12" height="14" rx="3" fill="{ORANGE}" stroke="{NAVY}" stroke-width="2"/>')

svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W * 2}" height="{H * 2}" viewBox="0 0 {W} {H}" shape-rendering="geometricPrecision">{"".join(o)}</svg>'
open("scene.svg", "w").write(svg)
subprocess.run(["node", "../../../tools/render-svg.js", "scene.svg", "scene.png", "--opaque"], check=True)

# ---------- split into layers ----------
img = Image.open("scene.png").convert("RGB")
pal = {"paper": PAPER, "navy": NAVY, "orange": ORANGE, "peach": PEACH, "mint": MINT}
rgb = {k: tuple(int(v[i:i + 2], 16) for i in (1, 3, 5)) for k, v in pal.items()}
px = img.load()
masks = {k: Image.new("L", img.size, 0) for k in pal}
mp = {k: m.load() for k, m in masks.items()}
for y in range(img.height):
    for x in range(img.width):
        c = px[x, y]
        best = min(rgb, key=lambda k: (c[0] - rgb[k][0]) ** 2 + (c[1] - rgb[k][1]) ** 2 + (c[2] - rgb[k][2]) ** 2)
        mp[best][x, y] = 255
for k in ("navy", "orange", "peach", "mint"):
    a = masks[k].resize((W, H), Image.LANCZOS)
    Image.merge("LA", (Image.new("L", (W, H), 0), a)).save(f"../assets/layer-{k}.png", optimize=True)
print("ok")
