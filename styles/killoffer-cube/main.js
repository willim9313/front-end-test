// Reading-order player: walk the route panel by panel.
const map = document.querySelector("[data-map]");
const steps = [...map.querySelectorAll(".step")];
const cursor = map.querySelector(".map__cursor");
const scrub = document.querySelector("[data-scrub]");
const out = document.querySelector("[data-out]");
const play = document.querySelector("[data-play]");
const reduce = window.matchMedia("(prefers-reduced-motion: reduce)");

function go(n) {
  steps.forEach((s, i) => s.classList.toggle("is-done", i < n));
  const dot = steps[n - 1].querySelector("circle");
  cursor.setAttribute("cx", dot.getAttribute("cx"));
  cursor.setAttribute("cy", dot.getAttribute("cy"));
  map.style.setProperty("--done", n - 1);
  scrub.value = n;
  out.textContent = `第 ${n} 格`;
}

let timer = null;
function stop() {
  clearInterval(timer);
  timer = null;
  play.setAttribute("aria-pressed", "false");
  play.textContent = "播放";
}
play.addEventListener("click", () => {
  if (timer) return stop();
  let n = Number(scrub.value) >= steps.length ? 0 : Number(scrub.value);
  play.setAttribute("aria-pressed", "true");
  play.textContent = "暫停";
  const tick = () => {
    n += 1;
    go(n);
    if (n >= steps.length) stop();
  };
  tick();
  timer = setInterval(tick, reduce.matches ? 400 : 700);
});
scrub.addEventListener("input", () => {
  stop();
  go(Number(scrub.value));
});
steps.forEach((s, i) => s.addEventListener("click", () => { stop(); go(i + 1); }));

go(1);
