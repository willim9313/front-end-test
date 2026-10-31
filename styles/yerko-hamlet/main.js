const spread = document.querySelector(".spread");
const lines = [...spread.querySelectorAll(".lines span")];
const labels = [...spread.querySelectorAll(".who")];

// Keep the English text so the toggle can switch back.
[...lines, ...labels].forEach((el, i) => {
  el.dataset.en = el.textContent;
  el.style.setProperty("--i", i);
});

// Shared verse lines: the second half starts where the first half ended.
function alignHalfLines() {
  spread.querySelectorAll("[data-half-end]").forEach((end) => {
    const start = spread.querySelector(`[data-half-start="${end.dataset.halfEnd}"]`);
    end.style.paddingLeft = "";
    if (getComputedStyle(end.closest(".col")).position !== "absolute") return;
    const range = document.createRange();
    range.selectNodeContents(start);
    const width = range.getBoundingClientRect().width;
    const em = parseFloat(getComputedStyle(end).fontSize);
    end.style.paddingLeft = `${width + em * 0.4}px`;
  });
}

// Language
const langButtons = document.querySelectorAll("[data-lang]");
function setLang(lang) {
  spread.lang = lang === "zh" ? "zh-Hant" : "en";
  [...lines, ...labels].forEach((el) => {
    el.textContent = el.dataset[lang];
  });
  langButtons.forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.lang === lang)));
  alignHalfLines();
}
langButtons.forEach((b) => b.addEventListener("click", () => setLang(b.dataset.lang)));

// Original spread for comparison. The reference image is kept out of git
// (see CREDITS.md), so the button only appears when a local copy exists.
const origButton = document.querySelector("[data-original]");
const origImage = document.querySelector(".spread__orig");
const showOrigButton = () => { if (origImage.naturalWidth) origButton.hidden = false; };
if (origImage.complete) showOrigButton();
else origImage.addEventListener("load", showOrigButton);
origButton.addEventListener("click", () => {
  const on = spread.classList.toggle("is-original");
  origButton.setAttribute("aria-pressed", String(on));
});

// Speaker focus: hover previews, click locks.
let locked = null;
const focus = (who) => {
  if (who) spread.dataset.focus = who;
  else delete spread.dataset.focus;
};
labels.forEach((label) => {
  const who = label.closest(".speech").dataset.speaker;
  label.addEventListener("mouseenter", () => !locked && focus(who));
  label.addEventListener("mouseleave", () => !locked && focus(null));
  label.addEventListener("click", () => {
    locked = locked === who ? null : who;
    focus(locked);
    labels.forEach((l) =>
      l.setAttribute("aria-pressed", String(locked === l.closest(".speech").dataset.speaker))
    );
  });
});

new ResizeObserver(alignHalfLines).observe(spread);
document.fonts.ready.then(alignHalfLines);
