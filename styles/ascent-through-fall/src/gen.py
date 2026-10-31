"""Illustration layer for this page, drawn from scratch as SVG.

A thin vertical axis with a black star at the top; a winged figure falls
headfirst beside it, rendered as photocopy halftone; a target circle, a
crescent, loose feathers and small stars scattered around. Greyscale on white
(the page multiplies it onto grey paper). Writes ../assets/art.png.
"""
import math
import random
import subprocess

from PIL import Image, ImageChops, ImageFilter

W, H = 1080, 1350
AX = 540
rnd = random.Random(12)
o = [f'<rect width="{W}" height="{H}" fill="#fff"/>']
o.append('<pattern id="dots" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(30)">'
         '<circle cx="3.5" cy="3.5" r="2.2" fill="#2a2a2a"/></pattern>')
o.append('<pattern id="dots2" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(30)">'
         '<circle cx="3" cy="3" r="1.3" fill="#2a2a2a"/></pattern>')
o.append('<linearGradient id="wing" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>')

# axis and star
o.append(f'<path d="M{AX} 150 V 1120" stroke="#2a2a2a" stroke-width="1.6"/>')
sx, sy = AX, 130
for k in range(16):
    a = math.radians(k * 22.5)
    L = 70 if k % 4 == 0 else (40 if k % 2 == 0 else 22)
    w = 7 if k % 4 == 0 else 4
    nx, ny = -math.sin(a) * w, math.cos(a) * w
    o.append(f'<path d="M{sx + nx:.1f} {sy + ny:.1f} L{sx + L * math.cos(a):.1f} {sy + L * math.sin(a):.1f} L{sx - nx:.1f} {sy - ny:.1f} Z" fill="#2a2a2a"/>')
o.append(f'<circle cx="{sx}" cy="{sy}" r="12" fill="#2a2a2a"/>')
# a fan of thin rays on the right of the axis (the light he fell from)
for k in range(22):
    a = math.radians(-70 + k * 6.5)
    r0, r1 = 120, 120 + rnd.uniform(40, 120)
    o.append(f'<path d="M{AX + 20 + r0 * math.cos(a):.1f} {330 + r0 * math.sin(a):.1f} L{AX + 20 + r1 * math.cos(a):.1f} {330 + r1 * math.sin(a):.1f}" stroke="#2a2a2a" stroke-width="1.1"/>')
    if k % 3 == 0:
        o.append(f'<circle cx="{AX + 20 + (r1 + 8) * math.cos(a):.1f}" cy="{330 + (r1 + 8) * math.sin(a):.1f}" r="2" fill="#2a2a2a"/>')

# ---------- the falling figure: headfirst, tilted, wings trailing upward ----------
fx, fy, tilt = 500, 660, 18       # body centre and rotation (head points down-left)
fig = []
# wings: two full wing shapes rooted at the shoulders, trailing up behind the fall
for side in (-1, 1):
    rx = side * 22
    edge = [(side * 120, 0), (side * 210, -110), (side * 230, -230), (side * 170, -360)]   # leading edge to tip
    trail = [(side * 120, -330), (side * 90, -250), (side * 60, -150), (side * 30, -60)]   # scalloped trailing edge
    d = f"M{rx} 50 C {side * 80} 50 {edge[0][0]} 20 {edge[0][0]} 0 C {edge[1][0]} -40 {edge[2][0]} -150 {edge[3][0]} {edge[3][1]}"
    prev = edge[3]
    for t in trail:
        mx, my = (prev[0] + t[0]) / 2 - side * 26, (prev[1] + t[1]) / 2
        d += f" Q {mx:.0f} {my:.0f} {t[0]} {t[1]}"
        prev = t
    d += f" L {side * 8} 20 Z"
    fig.append(f'<path d="{d}" fill="url(#dots)" stroke="#2a2a2a" stroke-width="2"/>')
    # covert feathers near the root, long primaries towards the tip
    for k in range(12):
        t = k / 11
        ex = edge[0][0] + (edge[3][0] - edge[0][0]) * t
        ey = edge[0][1] + (edge[3][1] - edge[0][1]) * t
        tx = side * (30 + 90 * t)
        ty = -60 - 270 * t
        fig.append(f'<path d="M{ex:.0f} {ey:.0f} Q {(ex + tx) / 2 + side * 10:.0f} {(ey + ty) / 2:.0f} {tx:.0f} {ty:.0f}" stroke="#2a2a2a" stroke-width="1.3" fill="none"/>')
    fig.append(f'<path d="M{rx} 40 C {side * 70} 20 {side * 90} -20 {side * 70} -60" fill="url(#dots2)" stroke="#2a2a2a" stroke-width="1.4"/>')
# body: torso, head, arms reaching down, legs bent up
body = ("M-34 -60 C -40 -10 -30 40 -14 70 L 14 70 C 30 40 40 -10 34 -60 C 20 -74 -20 -74 -34 -60 Z")
fig.append(f'<path d="{body}" fill="url(#dots)" stroke="#2a2a2a" stroke-width="2"/>')
fig.append('<circle cx="0" cy="96" r="26" fill="url(#dots)" stroke="#2a2a2a" stroke-width="2"/>')
fig.append('<path d="M-26 88 C -20 70 20 70 26 88" fill="#2a2a2a"/>')                      # hair
fig.append('<path d="M-30 -30 C -64 10 -70 70 -54 120 M30 -30 C 64 10 74 70 60 118" stroke="#2a2a2a" stroke-width="13" stroke-linecap="round" fill="none"/>')
fig.append('<path d="M-14 -66 C -30 -120 -10 -170 -40 -210 M14 -66 C 40 -110 70 -120 80 -170" stroke="#2a2a2a" stroke-width="17" stroke-linecap="round" fill="none"/>')
fig.append('<path d="M-14 -66 C -30 -120 -10 -170 -40 -210 M14 -66 C 40 -110 70 -120 80 -170" stroke="#fff" stroke-width="9" stroke-linecap="round" fill="none" opacity=".6"/>')
o.append(f'<g transform="translate({fx} {fy}) rotate({tilt}) scale(0.82)">{"".join(fig)}</g>')

# target circle low on the axis, crescent to the left, small marks
o.append(f'<circle cx="{AX}" cy="980" r="46" fill="none" stroke="#2a2a2a" stroke-width="1.6"/>')
o.append(f'<circle cx="{AX}" cy="980" r="20" fill="none" stroke="#2a2a2a" stroke-width="1.2"/>')
o.append(f'<path d="M{AX - 70} 980 H{AX + 70}" stroke="#2a2a2a" stroke-width="1.2"/>')
o.append('<path d="M800 860 a 46 46 0 1 0 40 72 a 36 36 0 1 1 -40 -72 Z" fill="#2a2a2a"/>')
for x, y, s in [(250, 900, 7), (900, 1110, 9), (170, 1020, 6), (880, 1050, 5), (420, 220, 4), (700, 1180, 6)]:
    o.append(f'<path d="M{x} {y - s * 2} L{x + s * .4} {y - s * .4} L{x + s * 2} {y} L{x + s * .4} {y + s * .4} L{x} {y + s * 2} L{x - s * .4} {y + s * .4} L{x - s * 2} {y} L{x - s * .4} {y - s * .4} Z" fill="#2a2a2a"/>')
# loose feathers drifting down
for x, y, a in [(400, 830, 30), (690, 1040, -20), (330, 1080, 60), (820, 1210, 10)]:
    o.append(f'<g transform="translate({x} {y}) rotate({a})"><path d="M0 -38 C 14 -20 12 20 0 38 C -12 20 -14 -20 0 -38 Z" fill="url(#dots2)" stroke="#2a2a2a" stroke-width="1.2"/><path d="M0 -38 V 46" stroke="#2a2a2a" stroke-width="1.2"/></g>')
# dotted orbit around the figure
o.append(f'<ellipse cx="{AX}" cy="700" rx="300" ry="90" fill="none" stroke="#2a2a2a" stroke-width="1.4" stroke-dasharray="1 9" stroke-linecap="round" transform="rotate(-24 {AX} 700)"/>')

open("art.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(o)}</svg>')
subprocess.run(["node", "../../../tools/render-svg.js", "art.svg", "art-raw.png", "--opaque"], check=True)

# photocopy: slight blur, toner noise, contrast crush
img = Image.open("art-raw.png").convert("L").filter(ImageFilter.GaussianBlur(0.7))
noise = Image.effect_noise((W, H), 30)
img = ImageChops.add(img, noise, scale=1, offset=-128)
img = img.point(lambda v: 0 if v < 70 else (255 if v > 200 else int((v - 70) * 255 / 130)))
img.save("../assets/art.png", optimize=True)
print("ok")
