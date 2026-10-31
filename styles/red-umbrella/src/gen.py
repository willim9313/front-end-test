"""Draw the rainy-window scene for this page from scratch, as SVG.

Bird's-eye view straight down onto a street through a sash window: grey
pavements, cars, trees and umbrellas, one red umbrella on the crossing, a
potted plant on the sill. Writes scene.svg (736x1308).
Then: node render.js && uv run python post.py  -> scene.jpg, fog.jpg
"""
import math
import random

W, H = 736, 1308
rnd = random.Random(11)
out = []
add = out.append

ROAD = (232, 548)          # road edges (x)
CROSS = (770, 870)         # zebra crossing (y)

# ---------- street ----------
add(f'<rect width="{W}" height="{H}" fill="#9a9c9e"/>')                       # pavement
add(f'<rect x="{ROAD[0]}" width="{ROAD[1] - ROAD[0]}" height="{H}" fill="#6f7275"/>')  # asphalt
# paving joints
for y in range(0, H, 46):
    add(f'<line x1="0" y1="{y}" x2="{ROAD[0] - 14}" y2="{y}" stroke="#8c8e90" stroke-width="2"/>')
    add(f'<line x1="{ROAD[1] + 14}" y1="{y + 23}" x2="{W}" y2="{y + 23}" stroke="#8c8e90" stroke-width="2"/>')
# kerbs
for x in (ROAD[0] - 14, ROAD[1]):
    add(f'<rect x="{x}" width="14" height="{H}" fill="#b6b8ba"/>')
# centre dashes
mid = sum(ROAD) / 2
for y in range(-20, H, 110):
    if CROSS[0] - 90 < y < CROSS[1] + 20:
        continue
    add(f'<rect x="{mid - 4}" y="{y}" width="8" height="58" fill="#c9cacb"/>')
# stop lines and zebra
add(f'<rect x="{ROAD[0]}" y="{CROSS[0] - 34}" width="{mid - ROAD[0]}" height="9" fill="#c9cacb"/>')
add(f'<rect x="{mid}" y="{CROSS[1] + 25}" width="{ROAD[1] - mid}" height="9" fill="#c9cacb"/>')
for x in range(ROAD[0] + 12, ROAD[1] - 20, 44):
    add(f'<rect x="{x}" y="{CROSS[0]}" width="26" height="{CROSS[1] - CROSS[0]}" fill="#cfd0d1"/>')

# wet sheen: soft light streaks along the road
for _ in range(40):
    x = rnd.uniform(ROAD[0] + 10, ROAD[1] - 10)
    y = rnd.uniform(0, H)
    add(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(3, 9):.0f}" ry="{rnd.uniform(30, 90):.0f}" fill="#8d9093" opacity="0.6"/>')
# puddles on the pavements
for cx, cy, rx, ry in [(120, 470, 70, 26), (640, 690, 52, 20), (90, 1010, 48, 18), (660, 210, 60, 22)]:
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#b3b5b7"/>')
    add(f'<ellipse cx="{cx - rx * 0.2:.0f}" cy="{cy - ry * 0.2:.0f}" rx="{rx * 0.5:.0f}" ry="{ry * 0.35:.0f}" fill="#c4c6c8"/>')


def car(x, y, w, h, body, heading_up=True):
    g = [f'<g transform="translate({x} {y})">',
         f'<rect x="4" y="6" width="{w}" height="{h}" rx="22" fill="#4a4c4f" opacity="0.5"/>',  # shadow
         f'<rect width="{w}" height="{h}" rx="22" fill="{body}"/>']
    fy = 26 if heading_up else h - 26 - 34
    ry = h - 26 - 26 if heading_up else 26
    g.append(f'<rect x="10" y="{fy}" width="{w - 20}" height="34" rx="10" fill="#b9bbbd"/>')      # windscreen
    g.append(f'<rect x="12" y="{ry}" width="{w - 24}" height="26" rx="8" fill="#a5a7a9"/>')        # rear window
    g.append(f'<rect x="10" y="{min(fy, ry) + 40}" width="{w - 20}" height="{abs(fy - ry) - 46}" rx="6" fill="{body}" stroke="#2f3133" stroke-width="2" opacity="0.8"/>')
    g.append("</g>")
    add("".join(g))


car(266, 210, 96, 188, "#3b3d40")
car(422, 960, 96, 196, "#5d6064", heading_up=False)
car(270, 1120, 92, 180, "#26282a")


def tree(cx, cy, r):
    blobs = []
    for i in range(9):
        t = 2 * math.pi * i / 9 + rnd.uniform(-0.2, 0.2)
        rr = r * rnd.uniform(0.45, 0.62)
        blobs.append(f'<circle cx="{cx + r * 0.55 * math.cos(t):.0f}" cy="{cy + r * 0.55 * math.sin(t):.0f}" r="{rr:.0f}"/>')
    add(f'<g fill="#4a4d50" opacity="0.45" transform="translate(10 12)">{"".join(blobs)}<circle cx="{cx}" cy="{cy}" r="{r * 0.6:.0f}"/></g>')
    add(f'<g fill="#3a3c3f">{"".join(blobs)}<circle cx="{cx}" cy="{cy}" r="{r * 0.6:.0f}"/></g>')
    for i in range(14):
        t = rnd.uniform(0, 2 * math.pi)
        d = rnd.uniform(0, r * 0.8)
        add(f'<circle cx="{cx + d * math.cos(t):.0f}" cy="{cy + d * math.sin(t):.0f}" r="{rnd.uniform(6, 14):.0f}" fill="#55585b"/>')


tree(108, 300, 96)
tree(640, 1060, 88)
tree(118, 1180, 80)


def umbrella(cx, cy, r, fill, rib="#1f2022", rot=0.0):
    pts = []
    for i in range(16):
        t = rot + 2 * math.pi * i / 16
        rr = r if i % 2 == 0 else r * 0.9
        pts.append(f"{cx + rr * math.cos(t):.1f},{cy + rr * math.sin(t):.1f}")
    add(f'<ellipse cx="{cx + 7}" cy="{cy + 9}" rx="{r}" ry="{r * 0.92:.0f}" fill="#4a4c4f" opacity="0.45"/>')
    add(f'<polygon points="{" ".join(pts)}" fill="{fill}"/>')
    for i in range(0, 16, 2):
        t = rot + 2 * math.pi * i / 16
        add(f'<line x1="{cx}" y1="{cy}" x2="{cx + r * math.cos(t):.1f}" y2="{cy + r * math.sin(t):.1f}" stroke="{rib}" stroke-width="1.6" opacity="0.5"/>')
    add(f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{rib}"/>')


for cx, cy, r, f in [(170, 640, 31, "#2d2f32"), (196, 702, 28, "#505357"), (618, 470, 30, "#3c3e41"),
                     (660, 560, 27, "#26282a"), (606, 900, 30, "#46494c"), (150, 880, 29, "#323437"),
                     (680, 300, 26, "#55585c"), (300, 640, 27, "#2a2c2e")]:
    umbrella(cx, cy, r, f, rot=rnd.uniform(0, 1))
# the one colour in the picture
umbrella(452, 818, 33, "#E4342A", rib="#7c1712", rot=0.3)

# ---------- the window ----------
FR = "#1b1c1e"
frame = (f'<path fill-rule="evenodd" fill="{FR}" d="M0 0H{W}V{H}H0Z '
         f'M40 40H357V560H40Z M379 40H696V560H379Z M40 582H357V1150H40Z M379 582H696V1150H379Z"/>')
add(frame)
# glazing bars catch a little light on their inner edges
for x, y, w, h in [(357, 40, 3, 1110), (40, 560, 656, 3)]:
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#3a3c3f"/>')
# sill
add(f'<rect y="1150" width="{W}" height="{H - 1150}" fill="#141516"/>')
add(f'<rect y="1150" width="{W}" height="10" fill="#2c2e30"/>')
# potted plant: pot on the sill, leaves silhouetted against the glass
leaves = []
for (a, l, w) in [(-1.2, 210, 26), (-0.85, 250, 30), (-0.5, 190, 24), (-1.6, 170, 22), (-2.1, 200, 26), (-2.5, 150, 20), (-1.9, 260, 28)]:
    bx, by = 560, 1170
    tx, ty = bx + l * math.cos(a), by + l * math.sin(a)
    nx, ny = -math.sin(a) * w, math.cos(a) * w
    leaves.append(f'<path d="M{bx} {by} Q {bx + (tx - bx) * 0.5 + nx:.0f} {by + (ty - by) * 0.5 + ny:.0f} {tx:.0f} {ty:.0f} '
                  f'Q {bx + (tx - bx) * 0.5 - nx:.0f} {by + (ty - by) * 0.5 - ny:.0f} {bx} {by} Z"/>')
add(f'<g fill="#101112">{"".join(leaves)}</g>')
add('<path d="M500 1160 H620 L606 1262 H514 Z" fill="#0d0e0f"/>')
add('<rect x="494" y="1150" width="132" height="18" rx="3" fill="#0d0e0f"/>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
       + "".join(out) + "</svg>")
open("scene.svg", "w").write(svg)
print("ok")
