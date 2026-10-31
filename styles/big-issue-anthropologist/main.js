const art = document.querySelector("[data-art]");
const by = document.querySelector("[data-by]");
const text = document.querySelector("[data-text]");
const whos = [...document.querySelectorAll("[data-who]")];
const intro = [by.textContent, text.textContent];

// The vector art is inlined so it takes the page's ink colour.
fetch("assets/art.svg")
  .then((r) => r.text())
  .then((svg) => { document.querySelector("[data-ink]").innerHTML = svg; });

// Reverse fieldwork: each animal's notes on the human.
const notes = {
  bird: ["鳥的筆記", "巢的材質：毛，偏硬，很保暖。屋主似乎不知道我住在這裡。"],
  bear: ["熊的筆記", "他每隔一會兒就低頭在紙上刮東西，刮完又抬頭看我們一眼。推測是在數我們。"],
  monkey: ["猴子的筆記", "臉上的毛只長下半部。眼睛前面有兩個圈圈，拿下來的時候會瞇眼。"],
  dog: ["狗的筆記", "筆的味道：木頭和墨水。手的味道：咖啡。結論：可以信任。"],
  cat: ["貓的筆記", "紙很溫暖，適合躺。他不讓我躺。觀察結束。"],
  man: ["他的筆記", "田野調查第一天。我總覺得，被觀察的好像是我。"],
};

let pinned = null;
function show(btn) {
  const key = btn ? btn.dataset.who : null;
  whos.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
  if (btn) {
    art.style.setProperty("--sx", btn.style.getPropertyValue("--x"));
    art.style.setProperty("--sy", btn.style.getPropertyValue("--y"));
    art.style.setProperty("--sr", btn.style.getPropertyValue("--r"));
    art.dataset.focus = key;
  } else {
    delete art.dataset.focus;
  }
  [by.textContent, text.textContent] = key ? notes[key] : intro;
}

whos.forEach((btn) => {
  btn.setAttribute("aria-pressed", "false");
  btn.addEventListener("mouseenter", () => !pinned && show(btn));
  btn.addEventListener("mouseleave", () => !pinned && show(null));
  btn.addEventListener("click", () => {
    pinned = pinned === btn ? null : btn;
    show(pinned);
  });
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") { pinned = null; show(null); }
});
