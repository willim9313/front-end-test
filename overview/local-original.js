// Local-only "original art" mode.
// Each style can keep the earlier art cut from its reference in styles/<slug>/local-original/
// (gitignored, so it never reaches the public repo) with a manifest.json listing the files.
// spec.js shows a 原圖版 toggle when that manifest exists; turning it on stores the list in
// localStorage, and this script then points every matching assets/<file> at local-original/<file>:
// <img> tags, CSS url()s, new Image() and fetch(). It runs in <head>, before the page's main.js.
// Without the manifest or the stored list it does nothing.

(() => {
  const slug = (location.pathname.match(/\/styles\/([^/]+)\//) || [])[1];
  if (!slug) return;
  let files = null;
  try { files = JSON.parse(localStorage.getItem(`local-original:${slug}`)); } catch {}
  if (!Array.isArray(files) || !files.length) return;

  const names = new Set(files);
  const pattern = /(^|[^\w-])assets\/([\w.-]+)/g;
  const swap = (url) =>
    String(url).replace(pattern, (m, pre, name) => (names.has(name) ? `${pre}local-original/${name}` : m));

  // Images and fetches the page's own scripts start later
  const src = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, "src");
  Object.defineProperty(HTMLImageElement.prototype, "src", {
    ...src,
    set(value) { src.set.call(this, swap(value)); },
  });
  const fetch0 = window.fetch;
  window.fetch = (input, init) => fetch0(typeof input === "string" ? swap(input) : input, init);

  // <img> tags in the markup, and url()s in the stylesheets (re-declared in a later <style>)
  document.addEventListener("DOMContentLoaded", () => {
    for (const img of document.querySelectorAll("img[src]")) {
      const next = swap(img.getAttribute("src"));
      if (next !== img.getAttribute("src")) img.setAttribute("src", next);
    }
    const out = [];
    const walk = (rules, wrap) => {
      for (const rule of rules) {
        if (rule.cssRules && rule.conditionText !== undefined) {
          walk(rule.cssRules, (t) => wrap(`@media ${rule.conditionText} { ${t} }`));
        } else if (rule.style && rule.cssText.includes("assets/")) {
          const next = swap(rule.cssText);
          if (next !== rule.cssText) out.push(wrap(next));
        }
      }
    };
    for (const sheet of document.styleSheets) {
      try { walk(sheet.cssRules, (t) => t); } catch { /* cross-origin sheet */ }
    }
    if (out.length) document.head.append(Object.assign(document.createElement("style"), { textContent: out.join("\n") }));
    document.documentElement.dataset.localOriginal = "";
  });
})();
