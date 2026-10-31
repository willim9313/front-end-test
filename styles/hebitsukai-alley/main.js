const body = document.body;
const alley = document.querySelector("[data-alley]");
const presets = document.querySelectorAll("[data-set]");
const hexes = document.querySelectorAll("[data-hex]");

function showHex() {
  const css = getComputedStyle(body);
  hexes.forEach((el) => { el.textContent = css.getPropertyValue(`--${el.dataset.hex}`).trim(); });
}

presets.forEach((btn) =>
  btn.addEventListener("click", () => {
    body.dataset.preset = btn.dataset.set;
    presets.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
    showHex();
  })
);

// Point at a swatch to see only that colour's share of the drawing.
document.querySelectorAll("[data-isolate]").forEach((sw) => {
  const on = () => { if (sw.dataset.isolate !== "paper") alley.dataset.isolate = sw.dataset.isolate; else alley.dataset.isolate = "none"; };
  const off = () => { delete alley.dataset.isolate; };
  sw.addEventListener("mouseenter", on);
  sw.addEventListener("focus", on);
  sw.addEventListener("mouseleave", off);
  sw.addEventListener("blur", off);
});

// Follow the system theme on arrival: a dark system starts in the night palette.
if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
  document.querySelector('[data-set="night"]').click();
} else {
  showHex();
}
