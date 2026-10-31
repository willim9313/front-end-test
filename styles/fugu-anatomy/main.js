// Fit the header lines to the widths they have on the print (% of the poster width).
const poster = document.querySelector(".poster");
const fits = [
  [".kicker", 47.6],
  [".title", 71.6],
  [".subtitle", 38],
];
function fit() {
  const width = poster.clientWidth;
  fits.forEach(([selector, pct]) => {
    const el = poster.querySelector(selector);
    el.style.fontSize = "100px";
    el.style.fontSize = `${(100 * (pct / 100) * width) / el.scrollWidth}px`;
  });
}
new ResizeObserver(fit).observe(poster);
document.fonts.ready.then(fit);

// Organ notes
const notes = {
  ink: ["非常墨", "備用墨水。萬一哪天決定改當章魚，至少先準備好了。"],
  poison: ["ダメ", "真正不能吃的地方。在日本要有執照的師傅才能處理，畫成骷髏是怕你看不懂。"],
  ribs: ["ほね", "骨頭，暫定。河豚其實沒有這樣的肋骨，畫的人說先放著。"],
  spark: ["根性", "一瓶幹勁。把自己鼓成一顆球很費力，力氣都存在這裡。"],
  spike: ["ふくらむ練習", "鼓起來的練習版。先在肚子裡練，失敗了也沒有人看到。"],
  scale: ["うろこ", "鱗片放大。每一片都在看你。"],
};
const ja = document.querySelector("[data-note-ja]");
const text = document.querySelector("[data-note-text]");
const intro = [ja.textContent, text.textContent];
const tags = document.querySelectorAll("[data-note]");
tags.forEach((tag) =>
  tag.addEventListener("click", () => {
    const on = tag.getAttribute("aria-pressed") !== "true";
    tags.forEach((t) => t.setAttribute("aria-pressed", String(on && t === tag)));
    [ja.textContent, text.textContent] = on ? notes[tag.dataset.note] : intro;
  })
);
tags.forEach((t) => t.setAttribute("aria-pressed", "false"));

// Plates: pull an ink off the print to see what it carried
const chart = document.querySelector("[data-chart]");
const boxes = document.querySelectorAll("[data-plate]");
boxes.forEach((box) =>
  box.addEventListener("change", () => {
    chart.dataset.off = [...boxes].filter((b) => !b.checked).map((b) => b.dataset.plate).join(" ");
  })
);
