"""Moon-window poster for this page, drawn from scratch as SVG.

A round window onto a night landscape (moon, ridges, pine, cliff); a waterfall
leaves the cliff, crosses the window's edge and drops into a koi pond. A crane
and a stone lantern stand on the bank. The top right stays empty for the
page's own vertical caption.
Constraints from the page: pond surface at y = 77.6% (758 of 977); the fall
lands at x = 46% (339). Writes poster.svg and fall.svg (the waterfall mask).
"""
import math
import random

W, H = 736, 977
CX, CY, R = 360, 330, 248
POND = 758
PAPER, INK, GREEN, BLUE, RED = "#E8DDB0", "#243A3A", "#35514d", "#608080", "#C8462F"
rnd = random.Random(5)
o = []
o.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
o.append('<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3"/>'
         '<feColorMatrix values="0 0 0 0 0.25  0 0 0 0 0.22  0 0 0 0 0.12  0 0 0 0.10 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>')
o.append(f'<clipPath id="win"><circle cx="{CX}" cy="{CY}" r="{R}"/></clipPath>')
o.append('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c2f2f"/><stop offset="1" stop-color="#3c5a56"/></linearGradient>')
o.append('<linearGradient id="mist" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E8DDB0" stop-opacity="0"/><stop offset="1" stop-color="#E8DDB0" stop-opacity="0.45"/></linearGradient>')

# ---------- inside the window ----------
g = [f'<rect x="{CX - R}" y="{CY - R}" width="{2 * R}" height="{2 * R}" fill="url(#sky)"/>']
g.append(f'<circle cx="450" cy="170" r="34" fill="{PAPER}"/><circle cx="450" cy="170" r="48" fill="{PAPER}" opacity="0.12"/>')
for (y0, amp, col, op) in [(330, 50, BLUE, 0.55), (380, 60, "#4d6b68", 0.8), (430, 46, GREEN, 1)]:
    pts = [f"M{CX - R} {CY + R}"]
    x = CX - R
    pts.append(f"L{x} {y0}")
    while x < CX + R:
        nx = x + rnd.uniform(40, 80)
        pts.append(f"Q {(x + nx) / 2:.0f} {y0 - amp * rnd.uniform(0.4, 1.2):.0f} {nx:.0f} {y0 + rnd.uniform(-10, 10):.0f}")
        x = nx
    pts.append(f"L{CX + R} {CY + R} Z")
    g.append(f'<path d="{" ".join(pts)}" fill="{col}" opacity="{op}"/>')
    g.append(f'<rect x="{CX - R}" y="{y0 - 40}" width="{2 * R}" height="80" fill="url(#mist)"/>')
# cliff the water leaves from
g.append(f'<path d="M230 600 L250 470 L290 420 L330 400 L352 392 L360 420 L372 440 L420 470 L470 520 L500 600 Z" fill="{INK}"/>')
g.append(f'<path d="M262 470 l20 -24 M300 430 l14 -8 M398 460 l24 20 M440 500 l18 24" stroke="#4d6b68" stroke-width="3" fill="none"/>')
# pine branch reaching in from the left
br = "M110 230 C 170 220 220 236 270 214 C 300 200 330 206 350 196"
g.append(f'<path d="{br}" stroke="#5d7a74" stroke-width="9" fill="none" stroke-linecap="round"/>')
for x, y in [(150, 222), (200, 230), (240, 222), (280, 210), (320, 202), (346, 196)]:
    for k in range(7):
        a = math.radians(-160 + k * 24)
        g.append(f'<path d="M{x} {y} l{26 * math.cos(a):.1f} {16 * math.sin(a):.1f}" stroke="#7b968e" stroke-width="2.4" stroke-linecap="round"/>')
o.append(f'<g clip-path="url(#win)">{"".join(g)}</g>')
o.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{INK}" stroke-width="6"/>')
o.append(f'<circle cx="{CX}" cy="{CY}" r="{R + 14}" fill="none" stroke="{INK}" stroke-width="1.5"/>')

# ---------- the waterfall: from the cliff lip, over the window edge, into the pond ----------
fall = (f"M346 396 C 344 450 334 520 330 600 C 328 660 326 720 318 {POND + 6} "
        f"L 362 {POND + 6} C 356 720 358 660 360 600 C 364 520 368 450 368 396 Z")
o.append(f'<path d="{fall}" fill="#9fb7b2"/>')
o.append(f'<path d="{fall}" fill="none" stroke="{BLUE}" stroke-width="2"/>')
for _ in range(26):
    x = rnd.uniform(332, 360); y0 = rnd.uniform(400, 700)
    o.append(f'<path d="M{x:.0f} {y0:.0f} v{rnd.uniform(30, 70):.0f}" stroke="#d6e0d8" stroke-width="1.6" opacity="0.8"/>')
# rocks where the water leaves the window and lands
o.append(f'<path d="M270 600 C 290 586 312 590 330 604 L 330 640 C 300 640 280 632 270 600 Z M360 604 C 380 590 410 594 424 612 C 410 630 380 636 360 636 Z" fill="{INK}"/>')
o.append(f'<path d="M210 {POND} C 220 726 260 716 300 730 L 318 {POND} Z M362 {POND} L 372 728 C 410 712 470 716 520 {POND} Z" fill="{INK}"/>')
o.append(f'<ellipse cx="340" cy="{POND + 4}" rx="70" ry="10" fill="{PAPER}" opacity="0.55"/>')

# ---------- the pond ----------
o.append(f'<rect x="0" y="{POND}" width="{W}" height="{H - POND}" fill="{INK}"/>')
for _ in range(40):
    y = rnd.uniform(POND + 8, H - 6); x = rnd.uniform(0, W)
    o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(14, 40):.0f}" ry="1.6" fill="{BLUE}" opacity="0.5"/>')
for x, y, r in [(90, 800, 26), (130, 830, 18), (600, 820, 30), (660, 860, 20), (520, 930, 24), (40, 920, 22)]:
    o.append(f'<path d="M{x} {y} m{-r} 0 a {r} {r * 0.42:.1f} 0 1 0 {2 * r} 0 a {r} {r * 0.42:.1f} 0 0 0 {-r * 0.9:.1f} {-r * 0.4:.1f} L {x} {y} Z" fill="#4f6f5f"/>')


def koi(x, y, ang, s=1.0, col=RED):
    return (f'<g transform="translate({x} {y}) rotate({ang}) scale({s})">'
            f'<path d="M-26 0 C -18 -9 8 -9 20 0 C 8 9 -18 9 -26 0 Z" fill="{col}"/>'
            f'<path d="M-24 0 L -40 -9 L -36 0 L -40 9 Z" fill="{col}" opacity="0.85"/>'
            f'<path d="M-4 -6 l -8 -6 M-4 6 l -8 6" stroke="{col}" stroke-width="3" stroke-linecap="round"/>'
            f'<circle cx="-4" cy="-2" r="3" fill="{PAPER}" opacity="0.8"/></g>')


for x, y, a, s in [(200, 820, 20, 1.1), (260, 860, -10, 0.9), (420, 830, 200, 1.0), (470, 880, 160, 1.2), (330, 920, 10, 1.0),
                   (150, 900, -30, 0.8), (580, 905, 190, 0.9), (690, 940, 170, 0.7), (380, 790, 180, 0.8)]:
    o.append(koi(x, y, a, s, RED if rnd.random() > 0.25 else PAPER))

# ---------- bank: stone lantern (left) and crane (right) ----------
o.append(f'<path d="M80 {POND} L 96 690 L 132 690 L 148 {POND} Z" fill="{INK}"/>')
o.append(f'<path d="M84 690 h60 l -8 -22 h -44 Z M100 668 h28 v-34 h-28 Z M90 634 h48 l -24 -26 Z" fill="{INK}"/>')
o.append(f'<rect x="106" y="642" width="16" height="18" fill="{RED}" opacity="0.85"/>')
o.append(f'<path d="M560 {POND} C 580 728 640 722 690 {POND} Z" fill="{INK}"/>')
cx, cy = 618, 650
o.append(f'<path d="M{cx - 4} {cy + 44} L {cx - 10} {POND - 26} M{cx + 6} {cy + 44} L {cx + 10} {POND - 26}" stroke="{INK}" stroke-width="2.4"/>')
o.append(f'<path d="M{cx - 30} {cy + 30} C {cx - 24} {cy + 4} {cx + 20} {cy} {cx + 34} {cy + 22} C {cx + 22} {cy + 46} {cx - 14} {cy + 50} {cx - 30} {cy + 30} Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>')
o.append(f'<path d="M{cx - 30} {cy + 30} l -20 6 l 22 6 Z" fill="{INK}"/>')
o.append(f'<path d="M{cx + 28} {cy + 18} C {cx + 34} {cy - 10} {cx + 22} {cy - 40} {cx + 32} {cy - 58}" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/>')
o.append(f'<circle cx="{cx + 33}" cy="{cy - 60}" r="7" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>')
o.append(f'<circle cx="{cx + 33}" cy="{cy - 64}" r="3" fill="{RED}"/>')
o.append(f'<path d="M{cx + 39} {cy - 60} l 22 4" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')

# swallows over the window
for x, y, s in [(560, 120, 1.0), (600, 170, 0.8), (520, 210, 0.7), (640, 230, 0.6)]:
    o.append(f'<path d="M{x} {y} q {8 * s:.1f} {-6 * s:.1f} {16 * s:.1f} 0 q {8 * s:.1f} {-6 * s:.1f} {16 * s:.1f} 0" stroke="{INK}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
# seal stamp, top left
o.append(f'<g transform="translate(56 64)"><rect width="46" height="46" rx="4" fill="{RED}"/>'
         f'<path d="M12 12 h22 M12 23 h22 M12 34 h22 M23 12 v22" stroke="{PAPER}" stroke-width="3"/></g>')
o.append(f'<rect width="{W}" height="{H}" filter="url(#grain)"/>')

open("poster.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(o)}</svg>')
open("fall.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><path d="{fall}" fill="#000"/></svg>')
print("ok")
