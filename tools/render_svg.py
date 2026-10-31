"""Render an SVG file to PNG or JPEG with headless Edge (Windows), for machines
without Node/Playwright. Same contract as tools/render-svg.js:

    python tools/render_svg.py in.svg out.png [--opaque]
    python tools/render_svg.py in.svg out.jpg            (JPEG is always opaque)

Output size is the SVG's width/height attributes. PNG keeps transparency unless
--opaque is given. Generators can also `from render_svg import render`.
Needs Pillow.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from PIL import Image

EDGE = next((p for p in (
    os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
    os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
) if os.path.exists(p)), "msedge")


def render(svg_path, out_path, opaque=False):
    svg = Path(svg_path).read_text(encoding="utf-8")
    w = float(re.search(r'<svg[^>]*\swidth="([\d.]+)(?:px)?"', svg).group(1))
    h = float(re.search(r'<svg[^>]*\sheight="([\d.]+)(?:px)?"', svg).group(1))
    W, H = int(-(-w // 1)), int(-(-h // 1))
    tmp = Path(tempfile.mkdtemp(prefix="render-svg-"))
    try:
        page = tmp / "page.html"
        page.write_text(
            "<!doctype html><meta charset=utf-8>"
            "<style>html,body{margin:0;background:transparent;overflow:hidden}svg{display:block}</style>"
            + re.sub(r"^<\?xml[^>]*\?>", "", svg), encoding="utf-8")  # an XML declaration is invalid inside HTML
        shot = tmp / "shot.png"
        subprocess.run([
            EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            f"--user-data-dir={tmp / 'profile'}", "--force-device-scale-factor=1",
            "--default-background-color=00000000", f"--window-size={W},{H}",
            "--virtual-time-budget=3000", f"--screenshot={shot}", page.as_uri(),
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # msedge.exe can return before its headless child has written the file
        for _ in range(150):
            if shot.exists() and shot.stat().st_size:
                time.sleep(0.2)
                break
            time.sleep(0.1)
        else:
            raise RuntimeError(f"Edge wrote no screenshot for {svg_path}")
        img = Image.open(shot).convert("RGBA").crop((0, 0, W, H))
        out = Path(out_path)
        if out.suffix.lower() in (".jpg", ".jpeg"):
            bg = Image.new("RGB", img.size, "white")
            bg.paste(img, mask=img.getchannel("A"))
            bg.save(out, quality=86)
        else:
            if opaque:
                bg = Image.new("RGBA", img.size, "white")
                img = Image.alpha_composite(bg, img)
            img.save(out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("rendered", out_path, f"{W}x{H}")


if __name__ == "__main__":
    args = sys.argv[1:]
    render(args[0], args[1], opaque="--opaque" in args)
