// Spelling toggle: the 1918 reform, applied to the re-set text.
const roots = document.querySelectorAll("[data-ortho-text]");
const nodes = [];
roots.forEach((root) => {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) nodes.push({ node: walker.currentNode, old: walker.currentNode.data });
});

const LETTER = "[А-Яа-яЁёЀ-ӿ]";
const rules = [
  [/ѣ/g, "е"], [/Ѣ/g, "Е"], [/і/g, "и"], [/І/g, "И"], [/ѳ/g, "ф"], [/Ѳ/g, "Ф"],
  // hard sign is dropped at the end of a word
  [new RegExp(`ъ(?!${LETTER})`, "g"), ""],
  // adjective endings -аго / -яго become -ого / -его
  [new RegExp(`аго(?!${LETTER})`, "g"), "ого"],
  [new RegExp(`яго(?!${LETTER})`, "g"), "его"],
  // prefixes без- / из- before a voiceless consonant
  [/(^|[^А-Яа-я])([Бб])езп/g, "$1$2есп"],
  [/(^|[^А-Яа-я])([Ии])зс/g, "$1$2сс"],
  // feminine and neuter plural adjectives
  [/ловчия/g, "ловчие"], [/царския/g, "царские"],
];
const modern = (text) => rules.reduce((t, [re, to]) => t.replace(re, to), text);

const orthoButtons = document.querySelectorAll("[data-ortho]");
orthoButtons.forEach((button) =>
  button.addEventListener("click", () => {
    const toNew = button.dataset.ortho === "new";
    nodes.forEach((n) => { n.node.data = toNew ? modern(n.old) : n.old; });
    orthoButtons.forEach((b) => b.setAttribute("aria-pressed", String(b === button)));
  })
);

// Scan overlay for comparison
const spread = document.querySelector(".spread");
const scan = document.querySelector("[data-scan]");
scan.addEventListener("click", () => {
  const on = spread.classList.toggle("is-scan");
  scan.setAttribute("aria-pressed", String(on));
});
