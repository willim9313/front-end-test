"""Thirteen specimen figures for this page, drawn from scratch as SVG.

Each figure follows the head / shell / core described in its button's data
attributes in index.html, at the same pixel size as before so the lineup's arc
keeps working. Charcoal shells, one warm colour for the opened core.
Writes ../assets/fig-NN.jpg via tools/render-svg.js.
"""
import math
import random
import subprocess

FIGS = [
    ("01", "chrome", "scales", "coil", 217, 456),
    ("02", "hood", "plates", "heart", 153, 416),
    ("03", "chrome", "plates", "skeleton", 145, 368),
    ("04", "hood", "drape", "ribs_coil", 127, 318),
    ("05", "hood", "folds", "stomach", 114, 273),
    ("06", "hood", "collar", "organ", 97, 236),
    ("07", "hood", "drape", "pelvis", 109, 218),
    ("08", "hood", "scales", "spine", 106, 239),
    ("09", "hood", "cloak", "ribs_hang", 115, 274),
    ("10", "chrome", "cloak", "ribs_heart", 117, 326),
    ("11", "hood", "folds", "ribs_spine", 149, 377),
    ("12", "chrome", "cloak", "ribs_coil", 149, 410),
    ("13", "hood", "cocoon", "opening", 185, 451),
]
SHELL, SHELL2, LINE = "#2a2a2c", "#3a3a3d", "#4a4a4e"
FLESH, FLESH2, DEEP, BONE = "#d99a8f", "#c26b62", "#8f2f2a", "#efe4dc"


def figure(head, shell, core, w, h, seed):
    rnd = random.Random(seed)
    X = lambda u: u * w
    Y = lambda v: v * h
    o = [f'<rect width="{w}" height="{h}" fill="#ffffff"/>']
    o.append(f'<ellipse cx="{X(.5)}" cy="{Y(.985)}" rx="{X(.42)}" ry="{Y(.012)}" fill="#e7e5e2"/>')
    # legs and feet under the hem
    o.append(f'<path d="M{X(.4)} {Y(.9)} L{X(.38)} {Y(.975)} M{X(.6)} {Y(.9)} L{X(.62)} {Y(.975)}" stroke="{SHELL}" stroke-width="{X(.07)}" stroke-linecap="round"/>')
    # ---------- shell ----------
    hem = .93 if shell != "cocoon" else .95
    if shell == "cocoon":
        body = f"M{X(.5)} {Y(.1)} C {X(1.02)} {Y(.2)} {X(1.0)} {Y(.8)} {X(.5)} {Y(hem)} C {X(0)} {Y(.8)} {X(-.02)} {Y(.2)} {X(.5)} {Y(.1)} Z"
    else:
        flare = {"drape": .02, "cloak": .04, "folds": .08, "plates": .1, "scales": .1, "collar": .12}[shell]
        body = (f"M{X(.3)} {Y(.15)} C {X(.16)} {Y(.17)} {X(.12)} {Y(.25)} {X(.13)} {Y(.4)} "
                f"L {X(flare)} {Y(hem)} Q {X(.5)} {Y(hem + .02)} {X(1 - flare)} {Y(hem)} "
                f"L {X(.87)} {Y(.4)} C {X(.88)} {Y(.25)} {X(.84)} {Y(.17)} {X(.7)} {Y(.15)} Z")
    o.append(f'<clipPath id="b{seed}"><path d="{body}"/></clipPath>')
    o.append(f'<path d="{body}" fill="{SHELL}"/>')
    tex = []
    if shell in ("scales", "cocoon"):
        r = w * .06
        for row in range(int(h / (r * .9)) + 1):
            for col in range(-1, int(w / r) + 2):
                cx = col * r * 1.6 + (r * .8 if row % 2 else 0)
                cy = row * r * .9
                tex.append(f'<path d="M{cx - r * .8:.1f} {cy:.1f} a {r * .8:.1f} {r * .8:.1f} 0 0 0 {r * 1.6:.1f} 0" fill="none" stroke="{LINE}" stroke-width="1.2"/>')
    elif shell in ("plates", "folds"):
        step = h * (.035 if shell == "plates" else .05)
        y = h * .2
        while y < h:
            if shell == "plates":
                tex.append(f'<path d="M0 {y:.1f} Q {w / 2:.1f} {y + step * .8:.1f} {w} {y:.1f}" fill="none" stroke="{LINE}" stroke-width="1.6"/>')
            else:
                tex.append(f'<path d="M0 {y:.1f} C {w * .3:.1f} {y - step * .4:.1f} {w * .7:.1f} {y + step * .7:.1f} {w} {y:.1f}" fill="none" stroke="{SHELL2}" stroke-width="{step * .35:.1f}"/>')
            y += step
    else:   # drape, cloak, collar: long vertical folds
        for k in range(9):
            u = .08 + k * .105
            tex.append(f'<path d="M{X(u)} {Y(.2)} C {X(u - .03)} {Y(.5)} {X(u + .03)} {Y(.7)} {X(u - .02)} {Y(.95)}" fill="none" stroke="{SHELL2 if k % 2 else LINE}" stroke-width="{w * .02:.1f}"/>')
    o.append(f'<g clip-path="url(#b{seed})">{"".join(tex)}</g>')
    if shell == "collar":
        o.append(f'<path d="M{X(.2)} {Y(.2)} L{X(.32)} {Y(.07)} L{X(.5)} {Y(.17)} L{X(.68)} {Y(.07)} L{X(.8)} {Y(.2)} Z" fill="{SHELL}" stroke="{LINE}" stroke-width="1.5"/>')
    # ---------- the opened core ----------
    cy, ry = .4, .15 if core != "pelvis" else .12
    if core == "pelvis":
        cy = .55
    rx = .24 if shell != "cocoon" else .2
    open_ = f"M{X(.5)} {Y(cy - ry)} C {X(.5 + rx)} {Y(cy - ry)} {X(.5 + rx)} {Y(cy + ry)} {X(.5)} {Y(cy + ry)} C {X(.5 - rx)} {Y(cy + ry)} {X(.5 - rx)} {Y(cy - ry)} {X(.5)} {Y(cy - ry)} Z"
    o.append(f'<clipPath id="c{seed}"><path d="{open_}"/></clipPath>')
    o.append(f'<path d="{open_}" fill="{FLESH}"/>')
    g = []
    sw = w * .028
    L, R, T, B = X(.5 - rx), X(.5 + rx), Y(cy - ry), Y(cy + ry)
    mx, my = X(.5), Y(cy)

    def coil(y0, y1):
        d, x, y, k = f"M{L + (R - L) * .2:.1f} {y0:.1f}", 0, y0, 0
        n = 5
        for i in range(n):
            ya = y0 + (y1 - y0) * (i + 1) / n
            xa = L + (R - L) * (.8 if i % 2 == 0 else .2)
            d += f" C {xa:.1f} {ya - (y1 - y0) / n * .9:.1f} {xa:.1f} {ya:.1f} {(L + R) / 2:.1f} {ya:.1f}"
        return f'<path d="{d}" fill="none" stroke="{FLESH2}" stroke-width="{sw * 1.8:.1f}" stroke-linecap="round"/><path d="{d}" fill="none" stroke="{DEEP}" stroke-width="{sw * .5:.1f}" opacity=".5"/>'

    def ribs(n=4):
        s = ""
        for i in range(n):
            y = T + (B - T) * (.18 + i * .16)
            s += f'<path d="M{mx:.1f} {y:.1f} Q {L:.1f} {y + (B - T) * .05:.1f} {L + (R - L) * .1:.1f} {y + (B - T) * .14:.1f} M{mx:.1f} {y:.1f} Q {R:.1f} {y + (B - T) * .05:.1f} {R - (R - L) * .1:.1f} {y + (B - T) * .14:.1f}" fill="none" stroke="{BONE}" stroke-width="{sw:.1f}" stroke-linecap="round"/>'
        return s

    def spine():
        s = ""
        for i in range(8):
            y = T + (B - T) * (.06 + i * .12)
            s += f'<rect x="{mx - sw * 1.4:.1f}" y="{y:.1f}" width="{sw * 2.8:.1f}" height="{(B - T) * .085:.1f}" rx="{sw * .6:.1f}" fill="{BONE}"/>'
        return s

    def heart(cx, cy_, s):
        return (f'<path d="M{cx:.1f} {cy_ + s:.1f} C {cx - s * 1.4:.1f} {cy_:.1f} {cx - s:.1f} {cy_ - s * 1.1:.1f} {cx:.1f} {cy_ - s * .4:.1f} '
                f'C {cx + s:.1f} {cy_ - s * 1.1:.1f} {cx + s * 1.4:.1f} {cy_:.1f} {cx:.1f} {cy_ + s:.1f} Z" fill="{DEEP}"/>'
                f'<path d="M{cx - s * .2:.1f} {cy_ - s * .6:.1f} q {s * .1:.1f} {-s * .5:.1f} {s * .4:.1f} {-s * .6:.1f}" stroke="{FLESH2}" stroke-width="{sw:.1f}" fill="none"/>')

    if core == "coil":
        g.append(coil(T + (B - T) * .1, B - (B - T) * .05))
    elif core == "heart":
        g.append(f'<rect x="{L}" y="{T}" width="{R - L}" height="{B - T}" fill="{FLESH2}"/>')
        g.append(heart(mx, my, (R - L) * .32))
    elif core == "skeleton":
        g.append(spine() + ribs(3))
        g.append(coil(my + (B - T) * .1, B))
    elif core == "ribs_coil":
        g.append(coil(my, B))
        g.append(ribs(3))
    elif core == "stomach":
        g.append(f'<path d="M{L + (R - L) * .3:.1f} {T + (B - T) * .2:.1f} C {R:.1f} {T:.1f} {R:.1f} {my + (B - T) * .2:.1f} {mx:.1f} {my + (B - T) * .1:.1f} C {L:.1f} {my:.1f} {L + (R - L) * .1:.1f} {T + (B - T) * .3:.1f} {L + (R - L) * .3:.1f} {T + (B - T) * .2:.1f} Z" fill="{FLESH2}"/>')
        g.append(coil(my + (B - T) * .15, B))
    elif core == "organ":
        g.append(f'<ellipse cx="{mx:.1f}" cy="{my:.1f}" rx="{(R - L) * .26:.1f}" ry="{(B - T) * .3:.1f}" fill="{DEEP}"/>')
        g.append(f'<path d="M{mx:.1f} {T:.1f} V {my - (B - T) * .3:.1f}" stroke="{FLESH2}" stroke-width="{sw * 1.4:.1f}"/>')
    elif core == "pelvis":
        g.append(f'<path d="M{mx:.1f} {my + (B - T) * .3:.1f} C {L:.1f} {my + (B - T) * .4:.1f} {L:.1f} {T:.1f} {mx - (R - L) * .1:.1f} {my - (B - T) * .1:.1f} L {mx:.1f} {my:.1f} L {mx + (R - L) * .1:.1f} {my - (B - T) * .1:.1f} C {R:.1f} {T:.1f} {R:.1f} {my + (B - T) * .4:.1f} {mx:.1f} {my + (B - T) * .3:.1f} Z" fill="{BONE}"/>')
        g.append(f'<circle cx="{mx - (R - L) * .2:.1f}" cy="{my + (B - T) * .05:.1f}" r="{(R - L) * .07:.1f}" fill="{FLESH2}"/><circle cx="{mx + (R - L) * .2:.1f}" cy="{my + (B - T) * .05:.1f}" r="{(R - L) * .07:.1f}" fill="{FLESH2}"/>')
    elif core == "spine":
        g.append(f'<rect x="{L}" y="{T}" width="{R - L}" height="{B - T}" fill="{FLESH2}" opacity=".5"/>' + spine())
    elif core == "ribs_hang":
        g.append(ribs(4))
        d = f"M{mx:.1f} {my:.1f} C {mx - (R - L) * .3:.1f} {B:.1f} {mx + (R - L) * .2:.1f} {B + (B - T) * .5:.1f} {mx - (R - L) * .05:.1f} {B + (B - T) * .9:.1f}"
        o.append(f'<path d="{d}" fill="none" stroke="{FLESH2}" stroke-width="{sw * 1.8:.1f}" stroke-linecap="round"/>')
    elif core == "ribs_heart":
        g.append(heart(mx, my + (B - T) * .05, (R - L) * .22))
        g.append(ribs(4))
    elif core == "ribs_spine":
        g.append(spine() + ribs(4))
    elif core == "opening":
        g.append(f'<rect x="{L}" y="{T}" width="{R - L}" height="{B - T}" fill="{DEEP}"/>')
        g.append(f'<ellipse cx="{mx:.1f}" cy="{my:.1f}" rx="{(R - L) * .3:.1f}" ry="{(B - T) * .36:.1f}" fill="#4b1714"/>')
    o.append(f'<g clip-path="url(#c{seed})">{"".join(g)}</g>')
    o.append(f'<path d="{open_}" fill="none" stroke="{LINE}" stroke-width="{w * .02:.1f}"/>')
    # ---------- head ----------
    hy = .07 if shell != "cocoon" else .12
    if head == "chrome":
        o.append(f'<defs><linearGradient id="g{seed}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#eef3f7"/><stop offset=".5" stop-color="#9eacb8"/><stop offset="1" stop-color="#55606b"/></linearGradient></defs>')
        o.append(f'<ellipse cx="{X(.5)}" cy="{Y(hy)}" rx="{X(.13)}" ry="{Y(.06)}" fill="url(#g{seed})"/>')
        o.append(f'<rect x="{X(.36)}" y="{Y(hy - .01)}" width="{X(.05)}" height="{Y(.03)}" rx="2" fill="#b0342d"/>')
        o.append(f'<path d="M{X(.42)} {Y(hy)} h{X(.16)}" stroke="#2a2a2c" stroke-width="{w * .02:.1f}"/>')
    else:
        o.append(f'<path d="M{X(.3)} {Y(hy + .08)} C {X(.26)} {Y(hy - .04)} {X(.38)} {Y(hy - .07)} {X(.5)} {Y(hy - .07)} C {X(.62)} {Y(hy - .07)} {X(.74)} {Y(hy - .04)} {X(.7)} {Y(hy + .08)} Z" fill="#1b1b1d"/>')
        o.append(f'<ellipse cx="{X(.5)}" cy="{Y(hy + .01)}" rx="{X(.07)}" ry="{Y(.03)}" fill="#0b0b0c"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{"".join(o)}</svg>'


for i, (no, head, shell, core, w, h) in enumerate(FIGS):
    open("fig.svg", "w").write(figure(head, shell, core, w, h, i))
    subprocess.run(["node", "../../../tools/render-svg.js", "fig.svg", f"../assets/fig-{no}.jpg"], check=True, stdout=subprocess.DEVNULL)
print("ok")
