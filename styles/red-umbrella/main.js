const win = document.querySelector("[data-window]");
const fogCanvas = document.querySelector("[data-fog]");
const rainCanvas = document.querySelector("[data-rain]");
const fogCtx = fogCanvas.getContext("2d");
const rainCtx = rainCanvas.getContext("2d");
const rainLevel = document.querySelector("[data-rain-level]");
const fogSpeed = document.querySelector("[data-fog-speed]");
const reduce = window.matchMedia("(prefers-reduced-motion: reduce)");

const fogImg = new Image();
fogImg.src = "assets/fog.jpg";

let w = 0, h = 0, dpr = 1;
function size() {
  const r = win.getBoundingClientRect();
  dpr = Math.min(window.devicePixelRatio || 1, 2);
  w = Math.round(r.width * dpr);
  h = Math.round(r.height * dpr);
  // keep what was wiped across resizes by redrawing full fog (simplest, and it fogs back anyway)
  for (const c of [fogCanvas, rainCanvas]) { c.width = w; c.height = h; }
  if (fogImg.complete) fogCtx.drawImage(fogImg, 0, 0, w, h);
}
new ResizeObserver(size).observe(win);
fogImg.addEventListener("load", size);

// Wiping: erase fog along the pointer path with a soft round brush.
let last = null;
function wipe(x, y) {
  const r = Math.max(w, h) * 0.045;
  fogCtx.save();
  fogCtx.globalCompositeOperation = "destination-out";
  fogCtx.lineCap = "round";
  fogCtx.lineJoin = "round";
  fogCtx.lineWidth = r * 2;
  fogCtx.shadowColor = "#000";
  fogCtx.shadowBlur = r * 0.6;
  fogCtx.beginPath();
  fogCtx.moveTo(last ? last.x : x, last ? last.y : y);
  fogCtx.lineTo(x, y);
  fogCtx.stroke();
  fogCtx.restore();
  last = { x, y };
}
const point = (e) => {
  const r = fogCanvas.getBoundingClientRect();
  return [(e.clientX - r.left) * dpr, (e.clientY - r.top) * dpr];
};
let down = false;
win.addEventListener("pointerdown", (e) => { down = true; last = null; win.setPointerCapture(e.pointerId); wipe(...point(e)); });
// a mouse wipes just by moving over the glass; touch and pen wipe while pressed
win.addEventListener("pointermove", (e) => { if (down || e.pointerType === "mouse") wipe(...point(e)); });
win.addEventListener("pointerup", () => { down = false; last = null; });
win.addEventListener("pointerleave", () => { last = null; });

document.querySelector("[data-clear]").addEventListener("click", () => fogCtx.clearRect(0, 0, w, h));

// Fog creeps back: repaint the fog image at a low alpha each frame.
// Rain: thin falling streaks on the glass.
const drops = [];
function spawn(n) {
  for (let i = 0; i < n; i++) {
    drops.push({ x: Math.random() * w, y: -Math.random() * h, v: (0.9 + Math.random() * 0.8) * h * 0.012, l: (0.4 + Math.random()) * h * 0.03 });
  }
}
let prev = performance.now();
function frame(now) {
  const dt = Math.min(50, now - prev) / 16.7;
  prev = now;

  if (fogImg.complete && w) {
    const k = Number(fogSpeed.value) / 100;
    if (k > 0) {
      fogCtx.globalAlpha = 0.004 * k * dt;
      fogCtx.drawImage(fogImg, 0, 0, w, h);
      fogCtx.globalAlpha = 1;
    }
  }

  rainCtx.clearRect(0, 0, w, h);
  if (!reduce.matches) {
    const target = Math.round((Number(rainLevel.value) / 100) * 220);
    if (drops.length < target) spawn(Math.min(6, target - drops.length));
    if (drops.length > target) drops.length = target;
    rainCtx.strokeStyle = "rgba(255,255,255,0.55)";
    rainCtx.lineWidth = Math.max(1, dpr);
    rainCtx.beginPath();
    for (const d of drops) {
      d.y += d.v * dt;
      if (d.y - d.l > h) { d.y = -Math.random() * h * 0.2; d.x = Math.random() * w; }
      rainCtx.moveTo(d.x, d.y);
      rainCtx.lineTo(d.x - d.l * 0.06, d.y - d.l);
    }
    rainCtx.stroke();
  }
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
