"""Graphite plate for this page, drawn from scratch as SVG.

The end of Act V without figures: a bier borne on four halberds, a dark cloak
draped over it with a crown and a sword laid on top, two banners hanging at
the sides; a graphite smear runs down the gutter between the two columns of
verse. Pencil hatching, rough edges dissolving into the paper, then grain.
Writes ../assets/plate.jpg (2296x1768, white ground; the page multiplies it).
"""
import math
import random
import subprocess

from PIL import Image, ImageChops, ImageFilter

W, H = 2296, 1768
CX = 1148
rnd = random.Random(21)
o = [f'<rect width="{W}" height="{H}" fill="#fff"/>']
o.append('<filter id="rough" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="3" seed="7"/>'
         '<feDisplacementMap in="SourceGraphic" scale="10"/></filter>')
o.append('<filter id="soft"><feGaussianBlur stdDeviation="6"/></filter>')
o.append('<filter id="tooth"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="2" result="n"/>'
         '<feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 -3 1.2" result="holes"/>'
         '<feComposite in="SourceGraphic" in2="holes" operator="out"/></filter>')
o.append('<linearGradient id="fade" gradientUnits="userSpaceOnUse" x1="0" y1="560" x2="0" y2="900"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>'
         '<filter id="ragged"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="5" result="n"/>'
         '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 4 -1.6" result="a"/>'
         '<feComposite in="SourceGraphic" in2="a" operator="arithmetic" k1="0" k2="1" k3="-0.9" k4="0"/></filter>'
         f'<mask id="dissolve"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>'
         '<linearGradient id="shade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#141414"/><stop offset=".6" stop-color="#3a3a3a"/><stop offset="1" stop-color="#6a6a6a"/></linearGradient>')


def hatch(clip_id, x0, y0, x1, y1, angle, gap, op, sw=2.2, jitter=0.4):
    a = math.radians(angle)
    dx, dy = math.cos(a), math.sin(a)
    L = max(x1 - x0, y1 - y0) * 1.5
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    lines = []
    k = -L
    while k < L:
        px, py = cx - dy * k, cy + dx * k
        s = rnd.uniform(-L, -L * jitter)
        e = rnd.uniform(L * jitter, L)
        lines.append(f"M{px + dx * s:.0f} {py + dy * s:.0f} L{px + dx * e:.0f} {py + dy * e:.0f}")
        k += gap * rnd.uniform(0.7, 1.3)
    return f'<path d="{" ".join(lines)}" stroke="#1e1e1e" stroke-width="{sw}" opacity="{op}" clip-path="url(#{clip_id})" fill="none"/>'


art = []
# halberds: four poles with axe heads, held upright
for i, x in enumerate((430, 830, 1466, 1866)):
    art.append(f'<path d="M{x} 70 L{x + rnd.uniform(-8, 8):.0f} 980" stroke="#2a2a2a" stroke-width="18" stroke-linecap="round"/>')
    s = -1 if i < 2 else 1
    art.append(f'<path d="M{x} 70 l 0 -46 M{x} 110 c {s * 70} -40 {s * 110} 0 {s * 96} 60 c {-s * 30} -20 {-s * 70} -20 {-s * 96} 0 Z" fill="#3a3a3a" stroke="#1e1e1e" stroke-width="6"/>')
    art.append(f'<path d="M{x} 110 l {-s * 40} -30 l 0 50 Z" fill="#2a2a2a"/>')
# banners hanging from the outer halberds
for x, s in ((430, -1), (1866, 1)):
    d = f"M{x} 150 L{x + s * 210} 170 L{x + s * 200} 560 L{x + s * 110} 500 L{x + s * 20} 590 Z"
    cid = f"bn{x}"
    art.append(f'<clipPath id="{cid}"><path d="{d}"/></clipPath><path d="{d}" fill="#6a6a6a" stroke="#1e1e1e" stroke-width="5"/>')
    art.append(hatch(cid, x - 220, 150, x + 220, 600, 80, 9, .45))
    art.append(f'<path d="M{x + s * 70} 260 l {s * 60} 0 l {-s * 30} 70 Z" fill="none" stroke="#1e1e1e" stroke-width="6"/>')
# the bier: a board across the poles, the cloak draped over it in heavy folds
art.append(f'<path d="M330 420 L1966 420 L1966 470 L330 470 Z" fill="#2a2a2a"/>')
cloak = ("M360 400 C 600 330 900 350 1148 360 C 1400 350 1700 330 1936 400 "
         "C 1960 520 1900 640 1820 700 C 1700 620 1560 760 1400 700 C 1300 820 1200 720 1148 860 "
         "C 1090 720 990 820 896 700 C 740 760 600 620 476 700 C 400 640 340 520 360 400 Z")
art.append('<clipPath id="ck"><path d="' + cloak + '"/></clipPath>')
art.append(f'<path d="{cloak}" fill="url(#shade)"/>')
art.append(hatch("ck", 300, 300, 2000, 900, 70, 7, .5, 2.6))
art.append(hatch("ck", 300, 300, 2000, 900, 110, 11, .35, 2))
for x in range(440, 1900, 90):          # fold highlights
    art.append(f'<path d="M{x} {420 + rnd.uniform(-10, 10):.0f} C {x + rnd.uniform(-30, 30):.0f} 540 {x + rnd.uniform(-40, 40):.0f} 620 {x + rnd.uniform(-20, 20):.0f} {rnd.uniform(650, 760):.0f}" '
               f'stroke="#b0b0b0" stroke-width="{rnd.uniform(8, 22):.0f}" fill="none" opacity=".45" filter="url(#soft)" clip-path="url(#ck)" stroke-linecap="round"/>')
# crown and sword laid on top
art.append(f'<path d="M{CX - 70} 360 L{CX - 80} 290 L{CX - 40} 320 L{CX} 270 L{CX + 40} 320 L{CX + 80} 290 L{CX + 70} 360 Z" fill="#b8b8b8" stroke="#1e1e1e" stroke-width="6"/>')
for x in (CX - 80, CX, CX + 80):
    art.append(f'<circle cx="{x}" cy="{290 if x != CX else 270}" r="10" fill="#1e1e1e"/>')
art.append(f'<path d="M{CX - 520} 380 L{CX + 380} 372" stroke="#d0d0d0" stroke-width="14" stroke-linecap="round"/>')
art.append(f'<path d="M{CX - 520} 380 L{CX + 380} 372" stroke="#1e1e1e" stroke-width="3"/>')
art.append(f'<path d="M{CX + 380} 340 L{CX + 390} 410 M{CX + 390} 376 L{CX + 470} 374" stroke="#1e1e1e" stroke-width="14" stroke-linecap="round"/>')
o.append(f'<g filter="url(#rough)" mask="url(#dissolve)">{"".join(art)}</g>')

# the graphite smear down the gutter
smear = []
for k in range(70):
    x = CX + rnd.gauss(0, 26 + k * 0.4)
    y0 = rnd.uniform(700, 900)
    y1 = y0 + rnd.uniform(200, 820) * (1 - k / 140)
    smear.append(f'<path d="M{x:.0f} {y0:.0f} C {x + rnd.uniform(-30, 30):.0f} {y0 + 200:.0f} {x + rnd.uniform(-20, 20):.0f} {y1 - 200:.0f} {x + rnd.uniform(-10, 10):.0f} {y1:.0f}" '
                 f'stroke="#2a2a2a" stroke-width="{rnd.uniform(2, 14):.0f}" opacity="{rnd.uniform(.15, .55):.2f}" fill="none" stroke-linecap="round"/>')
o.append(f'<g filter="url(#rough)">{"".join(smear)}</g>')

open("plate.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(o)}</svg>')
subprocess.run(["node", "../../../tools/render-svg.js", "plate.svg", "plate-raw.png", "--opaque"], check=True)
img = Image.open("plate-raw.png").convert("L")
# paper tooth: graphite catches only on the high points, so lift the darks at random
tooth = Image.effect_noise((W, H), 70).point(lambda v: 0 if v < 150 else min(255, (v - 150) * 3))
dark = ImageChops.invert(img)
dark = ImageChops.subtract(dark, ImageChops.multiply(dark, tooth))
img = ImageChops.invert(dark)
grain = Image.effect_noise((W, H), 14).point(lambda v: max(0, v - 136))
img = ImageChops.subtract(img, grain).filter(ImageFilter.GaussianBlur(0.7))
img.convert("RGB").save("../assets/plate.jpg", quality=84, optimize=True, progressive=True)
print("ok")
