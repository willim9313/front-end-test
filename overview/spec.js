// Spec card: the same nine fields for every style, read from catalog.js.
// On a style page (styles/<slug>/) it adds a small "← 目錄 / 規格" bar; on the
// overview page cards call StyleSpec.open(slug). Everything lives in a shadow
// root so the page's own CSS never reaches it.
// Field guide: docs/style-spec.md

(() => {
  const root = new URL("../", document.currentScript.src); // repo root
  const styles = window.STYLES || [];
  const bySlug = Object.fromEntries(styles.map((s) => [s.slug, s]));
  const pageSlug = (location.pathname.match(/\/styles\/([^/]+)\//) || [])[1];

  // ---------- colour maths ----------
  const lum = (hex) => {
    const c = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255)
      .map((v) => (v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4));
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
  };
  const contrast = (a, b) => {
    const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p);
    return (x + 0.05) / (y + 0.05);
  };
  const grade = (r) =>
    r >= 4.5 ? ["ok", "文字可用"] : r >= 3 ? ["mid", "只能大字"] : ["no", "只當色塊"];

  const cssVars = (s) => {
    const seen = {};
    return ":root {\n" + s.colors.map((c) => {
      seen[c.role] = (seen[c.role] || 0) + 1;
      const name = seen[c.role] > 1 ? `${c.role}-${seen[c.role]}` : c.role;
      return `  --${name}: ${c.hex}; /* ${c.name}：${c.use} */`;
    }).join("\n") + "\n}";
  };

  const missing = (s) => (window.SPEC_FIELDS || []).filter((f) => {
    const v = s[f];
    return v == null || v === "" || (Array.isArray(v) && v.length === 0);
  });

  // ---------- DOM helpers ----------
  const h = (tag, props = {}, ...kids) => {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(props)) {
      if (k === "class") node.className = v;
      else if (k.startsWith("on")) node.addEventListener(k.slice(2), v);
      else if (v != null) node.setAttribute(k, v);
    }
    node.append(...kids.flat().filter((k) => k != null));
    return node;
  };
  const list = (items, cls) => h("ul", { class: cls }, (items || []).map((t) => h("li", {}, t)));
  const section = (n, title, ...body) =>
    h("section", { class: "sec" }, h("h3", {}, h("span", { class: "n" }, n), title), ...body);

  async function copy(text, btn) {
    try { await navigator.clipboard.writeText(text); }
    catch {
      const t = h("textarea", {}, text);
      shadow.append(t); t.select(); document.execCommand("copy"); t.remove();
    }
    const old = btn.dataset.label || btn.textContent;
    btn.dataset.label = old;
    btn.textContent = "已複製";
    setTimeout(() => (btn.textContent = old), 1200);
  }

  // ---------- card ----------
  function render(s) {
    const paper = (s.colors.find((c) => c.role === "paper") || s.colors[0]).hex;
    const gaps = missing(s);
    const dark = s.technique.includes("深色模式");

    const colorRows = s.colors.map((c) => {
      const isPaper = c.hex === paper && c.role === "paper";
      const r = contrast(c.hex, paper);
      const [cls, label] = isPaper ? ["base", "底色"] : grade(r);
      const hexBtn = h("button", { type: "button", class: "hex", title: "複製色碼" }, c.hex.toUpperCase());
      hexBtn.addEventListener("click", () => copy(c.hex.toUpperCase(), hexBtn));
      return h("li", { class: "color" },
        h("span", { class: "chip", style: `background:${c.hex}` }),
        h("span", { class: "color__text" },
          h("strong", {}, c.name), h("span", { class: "muted" }, c.use)),
        h("span", { class: "color__meta" },
          hexBtn,
          h("span", { class: "tags" },
            h("span", { class: "area" }, c.area),
            h("span", { class: `grade grade--${cls}`, title: isPaper ? "" : `對比 ${r.toFixed(2)} : 1（對 ${paper}）` },
              isPaper ? label : `${label} ${r.toFixed(1)}`))));
    });

    const varsBtn = h("button", { type: "button", class: "btn" }, "複製 CSS 變數");
    varsBtn.addEventListener("click", () => copy(cssVars(s), varsBtn));

    const typeRows = (s.typeRoles || []).map((t) =>
      h("li", { class: "type" },
        h("span", { class: "type__role" }, t.role),
        h("span", { class: "type__sample", style: `font-family:"${t.family.split("／")[0]}",var(--font);font-weight:${parseInt(t.weight) || 400}` },
          t.sample || (/[぀-ヿ一-鿿]/.test(s.name) ? "Aa Bb Cc 0123" : s.name)),
        h("span", { class: "muted" }, [t.family, t.weight, t.note].filter(Boolean).join(" · "))));

    const pageLink = pageSlug ? null : h("a", { href: new URL(`styles/${s.slug}/`, root) }, "開啟頁面");

    return [
      h("header", { class: "head" },
        h("div", {},
          h("p", { class: "eyebrow" }, s.zh),
          h("h2", { id: "spec-title" }, s.name),
          h("p", { class: "links" },
            h("span", { class: `status status--${s.status}` }, s.statusLabel),
            dark ? h("span", { class: "status" }, "有深色版") : h("span", { class: "status status--none" }, "無深色版"),
            s.source ? h("a", { href: s.source.url, target: "_blank", rel: "noopener" }, `出處：${s.source.by}`) : null,
            h("a", { href: new URL(`styles/${s.slug}/NOTES.md`, root), target: "_blank" }, "NOTES.md"),
            pageLink)),
        h("button", { type: "button", class: "close", "aria-label": "關閉", onclick: () => dialog.close() }, "✕")),
      gaps.length ? h("p", { class: "warn" }, `規格不完整：缺 ${gaps.join("、")}`) : null,
      section(1, "身分與授權", h("p", {}, s.summary)),
      section(2, "適用場景",
        h("div", { class: "two" },
          h("div", {}, h("h4", { class: "yes" }, "適合"), list(s.fit, "ticks")),
          h("div", {}, h("h4", { class: "no" }, "避免"), list(s.avoid, "crosses")))),
      section("3·4", "色彩角色與可讀性",
        h("p", { class: "muted small" }, `對比是每個顏色對底色 ${paper.toUpperCase()} 量的；4.5 以上可排內文，3 以上只能排大字。`),
        h("ul", { class: "colors" }, colorRows), varsBtn),
      section(5, "字體角色", h("ul", { class: "types" }, typeRows)),
      section(6, "版面與構圖", list(s.layout, "dots")),
      section(7, "質感與線條", list(s.texture, "dots")),
      section(8, "動態與互動", list(s.motion, "dots"),
        h("p", { class: "reduced" }, h("strong", {}, "減少動態時："), s.reducedMotion || "—")),
      section(9, "Do / Don't",
        h("div", { class: "two" },
          h("div", {}, h("h4", { class: "yes" }, "Do"), list(s.do, "ticks")),
          h("div", {}, h("h4", { class: "no" }, "Don't"), list(s.dont, "crosses")))),
    ];
  }

  // ---------- shell ----------
  const host = document.createElement("style-spec");
  const shadow = host.attachShadow({ mode: "open" });
  shadow.innerHTML = `<style>${CSS()}</style>`;
  const dialog = h("dialog", { "aria-labelledby": "spec-title" });
  const body = h("div", { class: "body" });
  dialog.append(body);
  dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close(); });
  shadow.append(dialog);

  // Outside its own page a style's fonts aren't loaded, so the type samples would
  // fall back to a default face. Borrow the @font-face rules from its stylesheet.
  const fontsLoaded = new Set();
  async function loadFonts(slug) {
    if (slug === pageSlug || fontsLoaded.has(slug)) return;
    fontsLoaded.add(slug);
    try {
      const sheet = new URL(`styles/${slug}/styles.css`, root);
      const css = await (await fetch(sheet)).text();
      const faces = (css.match(/@font-face\s*{[^}]*}/g) || [])
        .map((rule) => rule.replace(/url\((["']?)([^"')]+)\1\)/g, (_, q, u) => `url("${new URL(u, sheet)}")`));
      if (faces.length) document.head.append(Object.assign(document.createElement("style"), { textContent: faces.join("\n") }));
    } catch { /* samples fall back to a default face */ }
  }

  function open(slug) {
    const s = bySlug[slug];
    if (!s) return;
    loadFonts(slug);
    body.replaceChildren(...render(s).filter(Boolean));
    dialog.showModal();
    body.scrollTop = 0;
  }

  // ?thumb keeps the bar out of thumbnail screenshots (tools/thumbs.ps1)
  if (pageSlug && bySlug[pageSlug] && !new URLSearchParams(location.search).has("thumb")) {
    const bar = h("nav", { class: "bar", "aria-label": "風格目錄" },
      h("a", { href: root.href }, "← 目錄"),
      h("button", { type: "button", "aria-haspopup": "dialog", onclick: () => open(pageSlug) }, "規格"));
    shadow.append(bar);

    // On phones the bar can sit on top of the page's own controls: tuck it away
    // while scrolling down, bring it back on the way up or when focused.
    const narrow = matchMedia("(max-width: 640px)");
    let lastY = scrollY;
    addEventListener("scroll", () => {
      const y = scrollY;
      if (Math.abs(y - lastY) < 8) return;
      bar.classList.toggle("is-tucked", narrow.matches && y > lastY && y > 40);
      lastY = y;
    }, { passive: true });
    bar.addEventListener("focusin", () => bar.classList.remove("is-tucked"));

    // Local-only original art (see overview/local-original.js): offered only when this
    // checkout has styles/<slug>/local-original/manifest.json, which git never tracks.
    const key = `local-original:${pageSlug}`;
    fetch("local-original/manifest.json", { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : null))
      .then((files) => {
        if (!Array.isArray(files) || !files.length) return;
        let on = false;
        try { on = !!localStorage.getItem(key); } catch {}
        const toggle = h("button", {
          type: "button", class: "orig", "aria-pressed": String(on),
          title: on ? "目前顯示從原圖做的本機版本；點一下換回公開版" : "換成從原圖做的本機版本（只在這台電腦上，不會公開）",
        }, on ? "原圖版" : "公開版");
        toggle.addEventListener("click", () => {
          try { on ? localStorage.removeItem(key) : localStorage.setItem(key, JSON.stringify(files)); } catch {}
          location.reload();
        });
        bar.insertBefore(toggle, bar.lastChild);
      })
      .catch(() => {});
  }
  document.body.append(host);

  window.StyleSpec = { open, missing, contrast };

  function CSS() {
    return `
:host { all: initial; }
* { box-sizing: border-box; }
:host {
  --bg: #ffffff; --fg: #1d1d1f; --mute: #5f6368; --line: #e3e3e6; --soft: #f4f4f6;
  --ok: #1e7a46; --ok-bg: #e3f4ea; --mid: #8a5a00; --mid-bg: #fbf0d9; --no: #b3261e; --no-bg: #fbe6e4;
  --font: system-ui, -apple-system, "Segoe UI", "Noto Sans TC", "PingFang TC", sans-serif;
}
@media (prefers-color-scheme: dark) {
  :host {
    --bg: #1c1c1e; --fg: #f2f2f4; --mute: #a5a5ab; --line: #333336; --soft: #2a2a2d;
    --ok: #7fd3a0; --ok-bg: #173826; --mid: #f0c36b; --mid-bg: #3a2e14; --no: #ff8a80; --no-bg: #3f1c1a;
  }
}
.bar {
  position: fixed; right: 16px; bottom: 16px; z-index: 2147483000;
  display: flex; gap: 2px; padding: 3px; border-radius: 999px;
  background: color-mix(in srgb, var(--bg) 88%, transparent); color: var(--fg);
  border: 1px solid var(--line); box-shadow: 0 4px 16px rgb(0 0 0 / 0.12);
  backdrop-filter: blur(8px); font: 500 13px/1 var(--font);
}
.bar a, .bar button {
  font: inherit; color: inherit; text-decoration: none; background: none; border: 0;
  padding: 8px 12px; border-radius: 999px; cursor: pointer;
}
.bar { transition: transform 0.2s ease, opacity 0.2s ease; }
.bar.is-tucked { transform: translateY(calc(100% + 24px)); opacity: 0; pointer-events: none; }
@media (prefers-reduced-motion: reduce) { .bar { transition: none; } }
@media (max-width: 640px) { .bar { right: 12px; bottom: 12px; font-size: 12px; } .bar a, .bar button { padding: 7px 10px; } }
.bar a:hover, .bar button:hover { background: var(--soft); }
.bar .orig, .bar .orig:hover { background: none; color: var(--mute); opacity: 1; }
.bar .orig:hover { background: var(--soft); }
.bar .orig[aria-pressed="true"] { color: #b3261e; }
@media (prefers-color-scheme: dark) { .bar .orig[aria-pressed="true"] { color: #ff8a80; } }
.bar button { background: var(--fg); color: var(--bg); }
.bar button:hover { background: var(--fg); opacity: 0.85; }
:focus-visible { outline: 2px solid #3b82f6; outline-offset: 2px; }

dialog {
  margin: 0 0 0 auto; height: 100dvh; max-height: 100dvh; width: min(480px, 100vw); max-width: 100vw;
  padding: 0; border: 0; border-left: 1px solid var(--line);
  background: var(--bg); color: var(--fg); font: 14px/1.6 var(--font);
}
dialog::backdrop { background: rgb(0 0 0 / 0.35); }
dialog[open] { animation: slide 0.22s cubic-bezier(0.2, 0.8, 0.2, 1); }
@keyframes slide { from { transform: translateX(24px); opacity: 0; } }
@media (prefers-reduced-motion: reduce) { dialog[open] { animation: none; } }
.body { height: 100%; overflow-y: auto; padding: 0 20px 32px; }

.head {
  position: sticky; top: 0; z-index: 1; display: flex; gap: 12px; align-items: flex-start;
  justify-content: space-between; padding: 18px 0 14px; background: var(--bg); border-bottom: 1px solid var(--line);
}
.eyebrow { margin: 0; color: var(--mute); font-size: 12px; }
h2 { margin: 2px 0 8px; font-size: 20px; line-height: 1.25; }
.links { display: flex; flex-wrap: wrap; gap: 6px 10px; align-items: center; margin: 0; font-size: 12px; }
.links a { color: inherit; text-underline-offset: 2px; }
.status { padding: 2px 8px; border-radius: 999px; background: var(--soft); }
.status--original { background: var(--ok-bg); color: var(--ok); }
.status--public-domain { background: #e5edfb; color: #1f4fa8; }
.status--derived { background: var(--mid-bg); color: var(--mid); }
.status--none { color: var(--mute); }
@media (prefers-color-scheme: dark) { .status--public-domain { background: #1b2a45; color: #9fbefa; } }
.close {
  flex: none; width: 32px; height: 32px; border: 0; border-radius: 8px; background: var(--soft);
  color: var(--fg); font: 16px/1 var(--font); cursor: pointer;
}
.warn { margin: 12px 0 0; padding: 8px 10px; border-radius: 8px; background: var(--mid-bg); color: var(--mid); font-size: 13px; }

.sec { padding: 18px 0 4px; border-bottom: 1px solid var(--line); }
.sec:last-child { border-bottom: 0; }
h3 { display: flex; gap: 8px; align-items: center; margin: 0 0 10px; font-size: 14px; }
.n {
  display: inline-grid; place-items: center; min-width: 20px; height: 20px; padding: 0 6px; border-radius: 10px;
  background: var(--fg); color: var(--bg); font-size: 11px;
}
h4 { margin: 0 0 6px; font-size: 12px; letter-spacing: 0.04em; }
h4.yes { color: var(--ok); } h4.no { color: var(--no); }
p { margin: 0 0 12px; }
.muted { color: var(--mute); }
.small { font-size: 12px; }
ul { margin: 0 0 12px; padding: 0; list-style: none; }
.dots li, .ticks li, .crosses li { position: relative; padding-left: 16px; margin-bottom: 4px; }
.dots li::before { content: "•"; position: absolute; left: 2px; color: var(--mute); }
.ticks li::before { content: "✓"; position: absolute; left: 0; color: var(--ok); }
.crosses li::before { content: "✕"; position: absolute; left: 0; color: var(--no); }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
@media (max-width: 420px) { .two { grid-template-columns: 1fr; gap: 4px; } }

.color { display: grid; grid-template-columns: 36px 1fr auto; gap: 10px; align-items: center; padding: 6px 0; }
.chip { width: 36px; height: 36px; border-radius: 8px; box-shadow: inset 0 0 0 1px rgb(0 0 0 / 0.12); }
.color__text { display: grid; line-height: 1.35; min-width: 0; }
.color__text .muted { font-size: 12px; }
.color__meta { display: grid; justify-items: end; gap: 3px; }
.hex {
  border: 0; background: none; color: var(--fg); padding: 0; cursor: pointer;
  font: 600 12px/1.2 ui-monospace, "Cascadia Mono", Consolas, monospace;
}
.hex:hover { text-decoration: underline; }
.tags { display: flex; gap: 4px; }
.area, .grade { font-size: 11px; padding: 1px 6px; border-radius: 4px; white-space: nowrap; }
.area { background: var(--soft); color: var(--mute); }
.grade--ok { background: var(--ok-bg); color: var(--ok); }
.grade--mid { background: var(--mid-bg); color: var(--mid); }
.grade--no { background: var(--no-bg); color: var(--no); }
.grade--base { background: var(--soft); color: var(--mute); }
.btn {
  margin: 4px 0 14px; padding: 8px 12px; border: 1px solid var(--line); border-radius: 8px;
  background: var(--soft); color: var(--fg); font: 500 13px/1 var(--font); cursor: pointer;
}
.btn:hover { border-color: var(--mute); }

.type { display: grid; gap: 2px; padding: 8px 0; border-bottom: 1px dashed var(--line); }
.type:last-child { border-bottom: 0; }
.type__role { font-size: 12px; color: var(--mute); }
.type__sample { font-size: 22px; line-height: 1.25; overflow-wrap: anywhere; }
.type .muted { font-size: 12px; }
.reduced { padding: 8px 10px; border-radius: 8px; background: var(--soft); font-size: 13px; }
`;
  }
})();
