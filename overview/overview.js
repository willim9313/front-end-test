// Overview: render cards from catalog.js and filter them.
// Within a facet, selected values are OR'd; across facets they are AND'd.
// Filter state lives in the URL hash so a filtered view can be bookmarked.

const FACETS = window.FACETS;
const STYLES = window.STYLES;
const grid = document.querySelector("[data-grid]");
const facetsBox = document.querySelector("[data-facets]");
const search = document.querySelector("[data-search]");
const count = document.querySelector("[data-count]");
const empty = document.querySelector("[data-empty]");
const clear = document.querySelector("[data-clear]");

const selected = Object.fromEntries(Object.keys(FACETS).map((k) => [k, new Set()]));

const valuesOf = (style, key) => {
  if (key === "status") return [style.statusLabel];
  const v = style[key];
  return Array.isArray(v) ? v : [v];
};

const el = (tag, props = {}, children = []) => {
  const node = Object.assign(document.createElement(tag), props);
  node.append(...children);
  return node;
};

// ---------- cards ----------
const cards = STYLES.map((s) => {
  const href = `styles/${s.slug}/`;
  const tags = [...s.type, ...s.technique, ...s.mood];
  // text-only variants (role "*-text") stay in the spec card, not on the card strip
  const swatches = s.colors.filter((c) => !c.role.endsWith("-text"));
  const card = el("li", { className: "card" }, [
    el("img", {
      className: "card__thumb",
      src: `styles/${s.slug}/thumb.jpg`,
      alt: "",
      loading: "lazy",
      width: 640,
      height: 400,
    }),
    el("span", { className: `status status--${s.status}`, textContent: s.statusLabel }),
    el("div", { className: "card__body" }, [
      el("h2", { className: "card__name" }, [el("a", { href, textContent: s.name })]),
      el("p", { className: "card__zh", textContent: s.zh }),
      el("div", { className: "swatches", role: "img", ariaLabel: `配色：${swatches.map((c) => c.hex).join("、")}` },
        swatches.map((c) => el("span", { className: "swatch", title: `${c.name} ${c.hex}`, style: `background:${c.hex}` }))),
      el("p", { className: "card__summary", textContent: s.summary }),
      el("p", { className: "card__fonts", textContent: s.fonts.join(" · ") }),
      el("ul", { className: "tags" }, tags.map((t) => el("li", { className: "tag", textContent: t }))),
    ]),
    el("button", {
      type: "button",
      className: "card__spec",
      textContent: "規格",
      ariaLabel: `${s.name} 的規格卡`,
      onclick: () => window.StyleSpec.open(s.slug),
    }),
  ]);
  card.querySelector("img").addEventListener("error", (e) => e.target.removeAttribute("src"));
  const haystack = [s.slug, s.name, s.zh, s.summary, s.palette, s.statusLabel, ...s.fonts, ...tags, ...s.type_style, ...s.colors.map((c) => c.hex), ...(s.fit || [])]
    .join(" ")
    .toLowerCase();
  return { style: s, card, haystack };
});
grid.append(...cards.map((c) => c.card));

// Spec fields still empty, so gaps show up while editing catalog.js
for (const s of STYLES) {
  const gaps = window.StyleSpec.missing(s);
  if (gaps.length) console.warn(`[spec] ${s.slug} 缺：${gaps.join("、")}`);
}

// ---------- facets ----------
const chips = [];
for (const [key, facet] of Object.entries(FACETS)) {
  const row = el("div", { className: "facet", role: "group", ariaLabel: facet.label }, [
    el("span", { className: "facet__label", textContent: facet.label }),
  ]);
  const box = el("div", { className: "facet__chips" });
  for (const value of facet.values) {
    const n = el("span", { className: "chip__n" });
    const chip = el("button", { type: "button", className: "chip" }, [value, n]);
    chip.setAttribute("aria-pressed", "false");
    chip.addEventListener("click", () => {
      const set = selected[key];
      set.has(value) ? set.delete(value) : set.add(value);
      update();
    });
    chips.push({ key, value, chip, n });
    box.append(chip);
  }
  row.append(box);
  facetsBox.append(row);
}

// ---------- filtering ----------
function matches(item, skipKey) {
  const q = search.value.trim().toLowerCase();
  if (q && !q.split(/\s+/).every((w) => item.haystack.includes(w))) return false;
  for (const [key, set] of Object.entries(selected)) {
    if (key === skipKey || set.size === 0) continue;
    if (!valuesOf(item.style, key).some((v) => set.has(v))) return false;
  }
  return true;
}

function update() {
  let shown = 0;
  for (const item of cards) {
    const ok = matches(item);
    item.card.hidden = !ok;
    if (ok) shown++;
  }
  // counts show how many you would get by adding each value to the current filters
  for (const { key, value, chip, n } of chips) {
    const on = selected[key].has(value);
    const would = cards.filter((item) => matches(item, key) && valuesOf(item.style, key).includes(value)).length;
    chip.setAttribute("aria-pressed", String(on));
    n.textContent = would;
    chip.disabled = !on && would === 0;
  }
  const any = search.value.trim() || Object.values(selected).some((s) => s.size);
  count.textContent = any ? `${shown} / ${cards.length} 個風格` : `${cards.length} 個風格`;
  empty.hidden = shown > 0;
  clear.hidden = !any;
  writeHash();
}

// ---------- URL hash ----------
function writeHash() {
  const params = new URLSearchParams();
  for (const [key, set] of Object.entries(selected)) if (set.size) params.set(key, [...set].join(","));
  if (search.value.trim()) params.set("q", search.value.trim());
  const hash = params.toString();
  history.replaceState(null, "", hash ? `#${hash}` : location.pathname + location.search);
}
function readHash() {
  const params = new URLSearchParams(location.hash.slice(1));
  for (const [key, set] of Object.entries(selected)) {
    set.clear();
    for (const v of (params.get(key) || "").split(",")) if (FACETS[key].values.includes(v)) set.add(v);
  }
  search.value = params.get("q") || "";
}

search.addEventListener("input", update);
clear.addEventListener("click", () => {
  Object.values(selected).forEach((s) => s.clear());
  search.value = "";
  update();
});
window.addEventListener("hashchange", () => { readHash(); update(); });

readHash();
update();
