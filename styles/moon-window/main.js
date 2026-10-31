const poster = document.querySelector("[data-poster]");
const pond = document.querySelector("[data-pond]");
const ctx = pond.getContext("2d");
const flow = document.querySelector("[data-flow]");
const reduce = window.matchMedia("(prefers-reduced-motion: reduce)");

// Flow toggle (a pause control for the looping waterfall)
function setFlow(on) {
  poster.classList.toggle("is-flowing", on);
  flow.setAttribute("aria-pressed", String(on));
  flow.textContent = on ? "水在流動" : "水靜止了";
}
flow.addEventListener("click", () => setFlow(!poster.classList.contains("is-flowing")));
setFlow(!reduce.matches);

// Pond ripples: rings flattened for the low viewing angle, widening as they fade.
let dpr = 1;
function size() {
  dpr = Math.min(window.devicePixelRatio || 1, 2);
  pond.width = Math.round(pond.clientWidth * dpr);
  pond.height = Math.round(pond.clientHeight * dpr);
}
new ResizeObserver(size).observe(pond);

const rings = [];
function drop(x, y) {
  for (let i = 0; i < 3; i++) rings.push({ x, y, t: -i * 9 });
}
pond.addEventListener("pointerdown", (e) => {
  const r = pond.getBoundingClientRect();
  drop((e.clientX - r.left) * dpr, (e.clientY - r.top) * dpr);
});
// The fall feeds the pond: a ring now and then where the water lands.
setInterval(() => {
  if (poster.classList.contains("is-flowing") && !reduce.matches) drop(pond.width * 0.46, pond.height * 0.04);
}, 1400);

function frame() {
  ctx.clearRect(0, 0, pond.width, pond.height);
  const max = pond.width * 0.16;
  for (let i = rings.length - 1; i >= 0; i--) {
    const ring = rings[i];
    ring.t += reduce.matches ? 3 : 1;
    if (ring.t < 0) continue;
    const k = ring.t / 70;
    if (k >= 1) { rings.splice(i, 1); continue; }
    const rx = max * k * (0.35 + 0.65 * (ring.y / pond.height + 0.3));
    ctx.beginPath();
    ctx.ellipse(ring.x, ring.y, rx, rx * 0.24, 0, 0, Math.PI * 2);
    ctx.strokeStyle = `rgba(232, 221, 176, ${0.75 * (1 - k)})`;
    ctx.lineWidth = Math.max(1, 2 * dpr * (1 - k));
    ctx.stroke();
  }
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
