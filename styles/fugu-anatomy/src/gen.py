"""Draw the three ink plates of an original fugu anatomy chart as SVG.

Each plate is solid black on transparent; the page fills it with its ink colour
through a CSS mask. Composition is drawn from scratch (not traced).
Writes plate-teal.svg, plate-cyan.svg, plate-coral.svg and tags.json.
"""
import json
import math
import random

W, H = 1120, 800
BX, BY, RX, RY = 540, 380, 290, 210          # body
CX, CY, CRX, CRY = 575, 470, 190, 85         # opened belly
LX, LY, LR = 950, 140, 85                    # magnifier
TAG = 35                                     # label glyph size in chart units


def ell(t, cx=BX, cy=BY, rx=RX, ry=RY, k=1.0):
    return cx + rx * k * math.cos(t), cy + ry * k * math.sin(t)


def svg(body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}"><defs>{defs}</defs>{body}</svg>')


rnd = random.Random(7)

# ---------- shared shapes ----------
tail = "M815 345 C 870 300 920 260 970 232 C 952 300 948 340 950 380 C 948 420 952 460 970 528 C 920 500 870 460 815 415 Z"
dorsal = "M560 182 C 590 140 625 112 655 98 C 662 130 680 160 705 196 Z"
pectoral = "M318 420 C 290 440 268 470 262 500 C 296 492 330 470 350 445 Z"
lips = "M262 362 C 238 360 226 374 236 388 C 226 402 240 414 262 408 Z"

spikes = []
for i in range(44):
    t = 2 * math.pi * i / 44 + 0.03
    deg = math.degrees(t) % 360
    if 340 < deg or deg < 20:        # tail
        continue
    if 165 < deg < 195:              # mouth
        continue
    if 245 < deg < 295:              # dorsal fin
        continue
    a = ell(t - 0.035)
    b = ell(t + 0.035)
    tip = ell(t, k=1.085)
    spikes.append(f"M{a[0]:.1f} {a[1]:.1f} L{tip[0]:.1f} {tip[1]:.1f} L{b[0]:.1f} {b[1]:.1f} Z")

spots = []
while len(spots) < 22:
    x, y = rnd.uniform(400, 790), rnd.uniform(205, 330)
    if ((x - BX) / (RX - 30)) ** 2 + ((y - BY) / (RY - 30)) ** 2 > 1:
        continue
    if any(math.hypot(x - sx, y - sy) < 34 for sx, sy, _ in spots):
        continue
    spots.append((x, y, rnd.uniform(6, 11)))

ribs = [f"M{x0} 405 C {x0 - 14} 360 {x0 - 6} 318 {x0 + 18} 288"
        for x0 in (455, 505, 555, 605, 655)]
gill = "M405 300 C 385 340 385 400 410 440"
cavity = f"M{CX - CRX} {CY} A {CRX} {CRY} 0 0 0 {CX + CRX} {CY} A {CRX} {CRY} 0 0 0 {CX - CRX} {CY} Z"
cavity_in = f"M{CX - CRX + 10} {CY} A {CRX - 10} {CRY - 9} 0 0 0 {CX + CRX - 10} {CY} A {CRX - 10} {CRY - 9} 0 0 0 {CX - CRX + 10} {CY} Z"

# dissection pins around the cut
pins = []
for t in (200, 235, 270, 305, 340, 30, 90, 150):
    r = math.radians(t)
    px, py = CX + (CRX + 6) * math.cos(r), CY + (CRY + 6) * math.sin(r)
    hx, hy = CX + (CRX + 30) * math.cos(r), CY + (CRY + 26) * math.sin(r)
    pins.append(((px, py), (hx, hy)))

# organs
ink = (428, 458)
skull = (498, 478)
spike_ball = (628, 510)
jar = (708, 452)

intestine = ("M540 432 C 600 420 610 455 572 462 C 534 470 540 500 585 494 "
             "C 630 488 660 470 650 445 C 642 425 612 432 620 455")

ball_spikes = []
for i in range(12):
    t = 2 * math.pi * i / 12
    a = (spike_ball[0] + 21 * math.cos(t - 0.2), spike_ball[1] + 21 * math.sin(t - 0.2))
    b = (spike_ball[0] + 21 * math.cos(t + 0.2), spike_ball[1] + 21 * math.sin(t + 0.2))
    c = (spike_ball[0] + 36 * math.cos(t), spike_ball[1] + 36 * math.sin(t))
    ball_spikes.append(f"M{a[0]:.1f} {a[1]:.1f} L{c[0]:.1f} {c[1]:.1f} L{b[0]:.1f} {b[1]:.1f} Z")

# chopsticks: tapered, lying across the bottom
def stick(x0, y0, x1, y1, w0, w1):
    ang = math.atan2(y1 - y0, x1 - x0) + math.pi / 2
    dx, dy = math.cos(ang), math.sin(ang)
    return (f"M{x0 + dx * w0:.1f} {y0 + dy * w0:.1f} L{x1 + dx * w1:.1f} {y1 + dy * w1:.1f} "
            f"L{x1 - dx * w1:.1f} {y1 - dy * w1:.1f} L{x0 - dx * w0:.1f} {y0 - dy * w0:.1f} Z")

stick_a = stick(170, 728, 930, 690, 11, 4)
stick_b = stick(190, 762, 950, 735, 11, 4)

# scales inside the lens
scales = []
for row in range(-4, 5):
    for col in range(-4, 5):
        sx = LX + col * 30 + (15 if row % 2 else 0)
        sy = LY + row * 20
        if math.hypot(sx - LX, sy - LY) > LR - 18:
            continue
        scales.append(f"M{sx - 15} {sy} A 15 15 0 0 0 {sx + 15} {sy}")

# ---------- labels (live text on the page) and their leader lines ----------
tags = [
    # key, text, x, y (left edge, vertical centre), organ point
    ("ink", "インク", 150, 650, (ink[0] - 4, ink[1] + 20)),
    ("poison", "毒物", 330, 650, (skull[0] - 6, skull[1] + 30)),
    ("ribs", "リブ", 330, 130, (480, 300)),
    ("spark", "電気", 840, 650, (jar[0] + 6, jar[1] + 40)),
    ("spike", "とがったボール", 525, 650, (spike_ball[0], spike_ball[1] + 34)),
]
leaders = []
for key, text, x, y, (ox, oy) in tags:
    w = len(text) * TAG
    ex, ey = x + w / 2, (y + 26 if oy < y else y + 30) if False else (y - 26 if oy < y else y + 26)
    leaders.append(f"M{ox} {oy} L{ex:.1f} {ey}")
lens_from = (705, 222)
ang = math.atan2(LY - lens_from[1], LX - lens_from[0])
lens_to = (LX - (LR + 8) * math.cos(ang), LY - (LR + 8) * math.sin(ang))

# ---------- plates ----------
knock = (f'<mask id="k"><rect width="{W}" height="{H}" fill="#fff"/>'
         f'<path d="{cavity}" fill="#000"/>'
         f'<circle cx="345" cy="328" r="27" fill="#000"/>'
         + "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#000"/>' for x, y, r in spots)
         + "".join(f'<path d="{d}" stroke="#000" stroke-width="9" stroke-linecap="round" fill="none"/>' for d in ribs)
         + f'<path d="{gill}" stroke="#000" stroke-width="7" stroke-linecap="round" fill="none"/>'
         + "</mask>")

teal = svg(
    f'<g mask="url(#k)"><ellipse cx="{BX}" cy="{BY}" rx="{RX}" ry="{RY}"/>'
    f'<path d="{tail}"/><path d="{dorsal}"/>' + "".join(f'<path d="{d}"/>' for d in spikes) + "</g>"
    f'<path d="{pectoral}" fill="none" stroke="#000" stroke-width="7"/>'
    f'<path d="{lips}"/>'
    f'<circle cx="345" cy="328" r="13"/>'
    # organs drawn in the open belly
    f'<path d="M{ink[0]} {ink[1] - 34} C {ink[0] + 28} {ink[1] - 4} {ink[0] + 26} {ink[1] + 26} {ink[0]} {ink[1] + 26} '
    f'C {ink[0] - 26} {ink[1] + 26} {ink[0] - 28} {ink[1] - 4} {ink[0]} {ink[1] - 34} Z"/>'
    f'<circle cx="{skull[0]}" cy="{skull[1] - 6}" r="30"/>'
    f'<rect x="{skull[0] - 17}" y="{skull[1] + 12}" width="34" height="22" rx="4"/>'
    f'<circle cx="{spike_ball[0]}" cy="{spike_ball[1]}" r="22"/>' + "".join(f'<path d="{d}"/>' for d in ball_spikes)
    + f'<path d="M{jar[0] - 18} {jar[1] - 22} h36 v52 a8 8 0 0 1 -8 8 h-20 a8 8 0 0 1 -8 -8 Z M{jar[0] - 12} {jar[1] - 34} h24 v12 h-24 Z" '
    f'fill="none" stroke="#000" stroke-width="6" stroke-linejoin="round"/>'
    + "".join(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{h[0]:.1f}" y2="{h[1]:.1f}" stroke="#000" stroke-width="3"/>' for p, h in pins)
    + f'<path d="{stick_a}"/><path d="{stick_b}"/>'
    + f'<g clip-path="url(#lens)">' + "".join(f'<path d="{d}" fill="none" stroke="#000" stroke-width="4"/>' for d in scales) + "</g>",
    defs=knock + f'<clipPath id="lens"><circle cx="{LX}" cy="{LY}" r="{LR - 6}"/></clipPath>',
)

cyan = svg(
    f'<path d="{cavity_in}"/>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#000" stroke-width="4"/>'
              for x, y, r in [(205, 330, 9), (180, 296, 13), (196, 252, 7), (162, 220, 10)])
    + f'<path d="{stick(260, 718, 900, 686, 3, 1.5)}"/><path d="{stick(280, 752, 920, 731, 3, 1.5)}"/>'
    + f'<circle cx="{LX}" cy="{LY}" r="{LR - 6}" opacity="0.35"/>'
    + f'<path d="M{jar[0] - 12} {jar[1] - 16} h24 v44 a5 5 0 0 1 -5 5 h-14 a5 5 0 0 1 -5 -5 Z" opacity="0.6"/>'
)

skull_eyes = (f'<circle cx="{skull[0] - 9}" cy="{skull[1] - 8}" r="7"/>'
              f'<circle cx="{skull[0] + 9}" cy="{skull[1] - 8}" r="6"/>')
coral = svg(
    f'<path d="{intestine}" fill="none" stroke="#000" stroke-width="17" stroke-linecap="round"/>'
    + f'<path d="M{jar[0] + 4} {jar[1] - 14} l-12 22 h10 l-8 22 l18 -28 h-10 l8 -16 Z"/>'
    + skull_eyes
    + "".join(f'<circle cx="{h[0]:.1f}" cy="{h[1]:.1f}" r="6"/>' for _, h in pins)
    + "".join(f'<path d="{d}" fill="none" stroke="#000" stroke-width="3"/>' for d in leaders)
    + "".join(f'<circle cx="{o[0]}" cy="{o[1]}" r="5"/>' for *_, o in tags)
    + f'<path d="M{lens_from[0]} {lens_from[1]} L{lens_to[0]:.1f} {lens_to[1]:.1f}" stroke="#000" stroke-width="3" stroke-dasharray="10 7"/>'
    + f'<circle cx="{lens_from[0]}" cy="{lens_from[1]}" r="5"/>'
    + f'<circle cx="{LX}" cy="{LY}" r="{LR}" fill="none" stroke="#000" stroke-width="14"/>'
    + f'<path d="M{LX + 64} {LY + 64} L{LX + 120} {LY + 120}" stroke="#000" stroke-width="22" stroke-linecap="round"/>'
    + f'<rect x="300" y="752" width="70" height="26" rx="13"/>'
)

for name, s in (("teal", teal), ("cyan", cyan), ("coral", coral)):
    open(f"plate-{name}.svg", "w").write(s)

json.dump({k: {"x": round(100 * x / W, 2), "y": round(100 * y / H, 2), "text": t}
           for k, t, x, y, _ in tags} | {"scale": {"x": round(100 * LX / W, 2), "y": round(100 * LY / H, 2)}},
          open("tags.json", "w"), ensure_ascii=False, indent=1)
print("ok", len(spikes), "spikes", len(spots), "spots")
