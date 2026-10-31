const stage = document.querySelector("[data-stage]");
const lineup = stage.parentElement;
const bodies = [...stage.querySelectorAll(".body")];
const loupe = document.querySelector("[data-loupe]");
const index = document.querySelector(".index");
const out = {
  no: document.querySelector("[data-out-no]"),
  spec: document.querySelector("[data-out-spec]"),
  hint: document.querySelector("[data-out-hint]"),
  head: document.querySelector("[data-out-head]"),
  shell: document.querySelector("[data-out-shell]"),
  core: document.querySelector("[data-out-core]"),
};
const ZOOM = 2.6;

function activate(body) {
  bodies.forEach((b) => b.classList.toggle("is-active", b === body));
  if (body) {
    stage.dataset.active = body.dataset.no;
    index.dataset.on = "";
    out.no.textContent = body.dataset.no;
    out.head.textContent = body.dataset.head;
    out.shell.textContent = body.dataset.shell;
    out.core.textContent = body.dataset.core;
  } else {
    delete stage.dataset.active;
    delete index.dataset.on;
    out.no.textContent = String(bodies.length);
  }
  out.spec.hidden = !body;
  out.hint.hidden = Boolean(body);
}

// Loupe: magnify the specimen under the pointer.
function moveLoupe(body, event) {
  const img = body.querySelector("img");
  const r = img.getBoundingClientRect();
  const box = lineup.getBoundingClientRect();
  const size = loupe.offsetWidth;
  const px = event.clientX - r.left;
  const py = event.clientY - r.top;
  loupe.style.setProperty("--src", `url("${img.currentSrc || img.src}")`);
  loupe.style.setProperty("--bw", `${r.width * ZOOM}px`);
  loupe.style.setProperty("--bh", `${r.height * ZOOM}px`);
  loupe.style.setProperty("--bx", `${size / 2 - px * ZOOM}px`);
  loupe.style.setProperty("--by", `${size / 2 - py * ZOOM}px`);
  loupe.style.setProperty("--lx", `${event.clientX - box.left - size / 2}px`);
  loupe.style.setProperty("--ly", `${event.clientY - box.top - size - 18}px`);
}

bodies.forEach((body, i) => {
  body.addEventListener("pointerenter", (event) => {
    if (event.pointerType !== "mouse") return;
    activate(body);
    loupe.classList.add("is-on");
    moveLoupe(body, event);
  });
  body.addEventListener("pointermove", (event) => {
    if (event.pointerType === "mouse") moveLoupe(body, event);
  });
  body.addEventListener("click", () => {
    activate(body.classList.contains("is-active") && !loupe.classList.contains("is-on") ? null : body);
  });
  body.addEventListener("focus", () => activate(body));
  body.addEventListener("keydown", (event) => {
    const step = event.key === "ArrowRight" ? 1 : event.key === "ArrowLeft" ? -1 : 0;
    if (!step) return;
    event.preventDefault();
    bodies[(i + step + bodies.length) % bodies.length].focus();
  });
});

stage.addEventListener("pointerleave", (event) => {
  if (event.pointerType !== "mouse") return;
  loupe.classList.remove("is-on");
  if (!stage.contains(document.activeElement)) activate(null);
});
stage.addEventListener("focusout", (event) => {
  if (!stage.contains(event.relatedTarget)) activate(null);
});
