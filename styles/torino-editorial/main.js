// Theme toggle: follows the system until the viewer picks one.
(() => {
  const root = document.documentElement;
  const button = document.querySelector("[data-theme-toggle]");
  const icon = button.querySelector("i");
  const media = window.matchMedia("(prefers-color-scheme: dark)");

  let saved = null;
  try { saved = localStorage.getItem("torino-theme"); } catch {}
  if (saved) root.dataset.theme = saved;

  const isDark = () => (root.dataset.theme ? root.dataset.theme === "dark" : media.matches);
  const sync = () => {
    icon.className = isDark() ? "ph ph-sun" : "ph ph-moon";
    button.setAttribute("aria-pressed", String(isDark()));
  };

  button.addEventListener("click", () => {
    root.dataset.theme = isDark() ? "light" : "dark";
    try { localStorage.setItem("torino-theme", root.dataset.theme); } catch {}
    sync();
  });
  media.addEventListener("change", sync);
  sync();
})();

// Postcard: live preview, character count, inline validation.
(() => {
  const form = document.querySelector("[data-postcard-form]");
  const to = form.querySelector("#pc-to");
  const msg = form.querySelector("#pc-msg");
  const count = form.querySelector("[data-count]");
  const error = form.querySelector(".field__error");
  const success = form.querySelector(".field__success");
  const previewTo = document.querySelector("[data-preview-to]");
  const previewMsg = document.querySelector("[data-preview-msg]");

  const render = () => {
    previewTo.textContent = to.value.trim() || to.placeholder;
    previewMsg.textContent = msg.value.trim() || "Wish you were here.";
    count.textContent = msg.value.length;
    success.hidden = true;
  };

  to.addEventListener("input", () => {
    if (to.value.trim()) {
      to.removeAttribute("aria-invalid");
      error.hidden = true;
    }
    render();
  });
  msg.addEventListener("input", render);

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const valid = to.value.trim().length > 0;
    to.setAttribute("aria-invalid", String(!valid));
    error.hidden = valid;
    success.hidden = !valid;
    if (!valid) to.focus();
  });
})();
