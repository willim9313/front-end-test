"""Original isometric-cube comic for this page, plus its reading-order map.

One big cube seen from above; each visible face is split into 2x2 rhombus
panels, so 12 panels in all. Every panel is drawn as a flat 100x100 scene and
mapped onto its rhombus with an affine transform, so the drawings follow the
faces and the reader has to turn the page to read them.

Writes comic.svg (800x928) and map.json (hexagon, panel centres, arrows).
Render: node ../../../tools/render-svg.js comic.svg ../assets/comic.png --opaque
"""
import base64
import json
import math

W, H = 800, 928
A = 200                                   # panel edge
C30, S30 = math.cos(math.pi / 6), 0.5
ER = (C30 * A, S30 * A)                   # one panel step towards the lower right
EL = (-C30 * A, S30 * A)                  # ... towards the lower left
ED = (0, A)                               # ... straight down
T = (400, 64)                             # top vertex of the hexagon


def add(*ps):
    return (sum(p[0] for p in ps), sum(p[1] for p in ps))


def mul(p, k):
    return (p[0] * k, p[1] * k)


UL = add(T, mul(EL, 2))
UR = add(T, mul(ER, 2))
O = add(T, mul(ER, 2), mul(EL, 2))       # the near corner, centre of the hexagon
hexagon = [T, UR, add(UR, mul(ED, 2)), add(O, mul(ED, 2)), add(UL, mul(ED, 2)), UL]

# faces: origin, u step, v step, panel order as (i, j)
faces = [
    (T, ER, EL, [(0, 0), (1, 0), (1, 1), (0, 1)]),           # top: read 1-4
    (O, mul(EL, -1), ED, [(0, 0), (1, 0), (1, 1), (0, 1)]),  # right: 5-8
    (UL, ER, ED, [(0, 0), (1, 0), (1, 1), (0, 1)]),          # left: 9-12
]

# ---------- drawing kit (local 0..100 coordinates) ----------
INK, PAPER = "#141414", "#fcfcfa"
SW = 'stroke-width="3" vector-effect="non-scaling-stroke"'


def figure(x, y, ink, s=1.0, flip=False, ladder=False):
    """A small figure in a striped scarf, feet at (x, y)."""
    d = -1 if flip else 1
    g = [f'<g transform="translate({x} {y}) scale({d * s} {s})" stroke="{ink}" fill="none" stroke-linecap="round" {SW}>',
         '<circle cx="0" cy="-30" r="6" fill="{0}"/>'.format(PAPER if ink == INK else INK),
         '<path d="M0 -24 L0 -10 M0 -10 L-5 0 M0 -10 L6 0 M0 -20 L-6 -13 M0 -20 L7 -15"/>',
         '<path d="M-3 -24 L6 -27 L9 -20" stroke-width="5"/>']
    if ladder:
        g.append('<path d="M-16 -22 L22 -26 M-15 -16 L23 -20 M-10 -22 l1 6 M0 -23 l1 6 M10 -24 l1 6 M18 -25 l1 6"/>')
    g.append("</g>")
    return "".join(g)


def bubble(x, y, text, ink, w=None):
    w = w or 7 * len(text) + 12
    bg = PAPER if ink == INK else INK
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="15" rx="7" fill="{bg}" stroke="{ink}" {SW}/>'
            f'<path d="M{x + 10} {y + 15} l3 6 l4 -6" fill="{bg}" stroke="{ink}" {SW}/>'
            f'<text x="{x + w / 2}" y="{y + 11}" fill="{ink}" font-family="Comic Neue" font-weight="700" '
            f'font-size="9.5" text-anchor="middle">{text}</text></g>')


def hatch(x0, y0, x1, y1, ink, gap=5):
    return "".join(f'<line x1="{x}" y1="{y0}" x2="{x - (y1 - y0) * 0.4}" y2="{y1}" stroke="{ink}" stroke-width="1.2" vector-effect="non-scaling-stroke"/>'
                   for x in range(int(x0), int(x1) + 30, gap))


def panel(n):
    """Return (background, body) for panel n (1-based)."""
    dark = n % 2 == 0
    ink = PAPER if dark else INK
    bg = INK if dark else PAPER
    s = []
    if n == 1:   # walking across a roof with a ladder
        s += [f'<path d="M0 80 H100" stroke="{ink}" {SW}/>', figure(34, 80, ink, ladder=True), bubble(40, 18, "Encore !", ink)]
    elif n == 2:  # finds a hatch
        s += [f'<path d="M0 80 H100" stroke="{ink}" {SW}/>', f'<rect x="58" y="80" width="26" height="6" fill="none" stroke="{ink}" {SW}/>',
              figure(40, 80, ink, flip=True), bubble(14, 22, "Tiens !", ink)]
    elif n == 3:  # opens it: black hole
        s += [hatch(0, 70, 100, 100, ink), f'<rect x="30" y="58" width="44" height="22" fill="{INK}" stroke="{ink}" {SW}/>',
              f'<path d="M30 58 L22 30 L66 30 L74 58" fill="{PAPER}" stroke="{INK}" {SW}/>', figure(84, 82, ink, s=0.9, flip=True)]
    elif n == 4:  # jumps in, only legs left
        s += [f'<rect x="28" y="62" width="44" height="18" fill="{PAPER}"/>', f'<rect x="28" y="62" width="44" height="18" fill="none" stroke="{ink}" {SW}/>',
              f'<path d="M46 62 L42 40 M54 62 L60 42" stroke="{ink}" {SW} stroke-linecap="round"/>', bubble(56, 16, "Hop !", ink)]
    elif n == 5:  # falling
        s += ["".join(f'<line x1="{x}" y1="{10 + (x * 7) % 30}" x2="{x}" y2="{60 + (x * 3) % 30}" stroke="{ink}" stroke-width="1.2" vector-effect="non-scaling-stroke"/>'
                      for x in range(8, 100, 9)),
              f'<g transform="rotate(180 50 50)">{figure(50, 78, ink, s=1.2)}</g>']
    elif n == 6:  # a room full of doors
        s += [f'<path d="M0 84 H100" stroke="{ink}" {SW}/>'] + \
             [f'<rect x="{x}" y="44" width="18" height="40" fill="none" stroke="{ink}" {SW}/><circle cx="{x + 14}" cy="66" r="1.6" fill="{ink}"/>' for x in (10, 41, 72)] + \
             [figure(54, 96, ink, s=0.8), bubble(30, 14, "Laquelle ?", ink)]
    elif n == 7:  # behind a door: stairs going up
        s += [f'<rect x="20" y="20" width="48" height="70" fill="none" stroke="{ink}" {SW}/>',
              f'<path d="M24 86 h10 v-10 h10 v-10 h10 v-10 h10 v-10" fill="none" stroke="{ink}" {SW}/>',
              hatch(22, 22, 66, 40, ink, 6), figure(84, 90, ink, flip=True)]
    elif n == 8:  # climbing
        s += [f'<path d="M0 96 h16 v-14 h16 v-14 h16 v-14 h16 v-14 h16 v-14 h20" fill="none" stroke="{ink}" {SW}/>',
              figure(56, 54, ink), bubble(8, 12, "Plus haut.", ink)]
    elif n == 9:  # out on another roof, under the stars
        s += ["".join(f'<circle cx="{x}" cy="{y}" r="1.2" fill="{ink}"/>' for x, y in [(12, 14), (30, 26), (64, 10), (86, 30), (48, 36), (78, 52), (20, 44)]),
              f'<path d="M0 90 L100 70" stroke="{ink}" {SW}/>', f'<rect x="40" y="73" width="20" height="5" fill="{ink}" transform="rotate(-11 50 76)"/>',
              figure(50, 76, ink, s=0.9)]
    elif n == 10:  # sets the ladder against the sky
        s += [f'<path d="M0 86 H100" stroke="{ink}" {SW}/>',
              f'<path d="M50 86 L62 8 M64 86 L76 8" stroke="{ink}" {SW}/>' +
              "".join(f'<path d="M{50 + k * 1.54} {86 - k * 10} h14" stroke="{ink}" {SW}/>' for k in range(1, 8)),
              figure(30, 86, ink), bubble(8, 16, "Bon.", ink)]
    elif n == 11:  # climbs out of the top of the panel
        s += [f'<path d="M40 100 L46 -4 M58 100 L64 -4" stroke="{ink}" {SW}/>' +
              "".join(f'<path d="M{40 + k * 0.58} {100 - k * 10} h18" stroke="{ink}" {SW}/>' for k in range(1, 10)),
              f'<path d="M48 18 L46 4 M56 18 L60 6" stroke="{ink}" {SW} stroke-linecap="round"/>']
    elif n == 12:  # ...and finds himself back on top of the cube
        c = (50, 58)
        s += [f'<path d="M{c[0]} {c[1] - 24} l21 12 v24 l-21 12 l-21 -12 v-24 Z M{c[0]} {c[1]} l21 -12 M{c[0]} {c[1]} l-21 -12 M{c[0]} {c[1]} v24" fill="none" stroke="{ink}" {SW}/>',
              figure(50, 40, ink, s=0.35, ladder=True), bubble(26, 10, "…encore ?", ink)]
    return bg, "".join(s)


# ---------- assemble ----------
font = base64.b64encode(open("../fonts/comic-neue-700-latin.woff2", "rb").read()).decode()
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       f'<style>@font-face{{font-family:"Comic Neue";font-weight:700;src:url(data:font/woff2;base64,{font})}}</style>',
       f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
centres = []
n = 0
for origin, u, v, order in faces:
    for i, j in order:
        n += 1
        p = add(origin, mul(u, i), mul(v, j))
        centres.append(add(p, mul(u, 0.5), mul(v, 0.5)))
        m = f"matrix({u[0] / 100:.4f} {u[1] / 100:.4f} {v[0] / 100:.4f} {v[1] / 100:.4f} {p[0]:.2f} {p[1]:.2f})"
        bg, body = panel(n)
        out.append(f'<clipPath id="c{n}"><rect width="100" height="100" transform="{m}"/></clipPath>')
        out.append(f'<g clip-path="url(#c{n})"><g transform="{m}"><rect width="100" height="100" fill="{bg}"/>{body}</g></g>')
        out.append(f'<rect width="100" height="100" transform="{m}" fill="none" stroke="{INK}" stroke-width="5" vector-effect="non-scaling-stroke"/>')
out.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in hexagon)}" fill="none" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>')
out.append("</svg>")
open("comic.svg", "w").write("".join(out))

# reading map: same geometry as the comic, arrows turning clockwise
cx, cy = O[0], O[1]
arcs = []
for a0, a1 in [(-70, -25), (50, 95), (170, 215)]:
    r = 450
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    arcs.append(f"M {p0[0]:.0f} {p0[1]:.0f} A {r} {r} 0 0 1 {p1[0]:.0f} {p1[1]:.0f}")
json.dump({"hexagon": [[round(x), round(y)] for x, y in hexagon],
           "centres": [[round(x), round(y)] for x, y in centres],
           "arcs": arcs}, open("map.json", "w"), indent=1)
print("ok", n, "panels")
