document.documentElement.classList.add("js");

// Theme toggle: follows the system until the viewer picks one.
(() => {
  const root = document.documentElement;
  const button = document.querySelector("[data-theme-toggle]");
  const icon = button.querySelector("i");
  const media = window.matchMedia("(prefers-color-scheme: dark)");

  let saved = null;
  try { saved = localStorage.getItem("manga-poster-theme"); } catch {}
  if (saved) root.dataset.theme = saved;

  const isDark = () => (root.dataset.theme ? root.dataset.theme === "dark" : media.matches);
  const sync = () => {
    icon.className = isDark() ? "ph ph-sun" : "ph ph-moon";
    button.setAttribute("aria-pressed", String(isDark()));
  };

  button.addEventListener("click", () => {
    root.dataset.theme = isDark() ? "light" : "dark";
    try { localStorage.setItem("manga-poster-theme", root.dataset.theme); } catch {}
    sync();
  });
  media.addEventListener("change", sync);
  sync();
})();

// Scroll reveal.
(() => {
  const items = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window)) {
    items.forEach((el) => el.classList.add("is-in"));
    return;
  }
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        io.unobserve(entry.target);
      });
    },
    { threshold: 0.2 }
  );
  items.forEach((el) => io.observe(el));
})();

// Demo form: inline error and success states.
(() => {
  const form = document.querySelector("[data-demo-form]");
  const input = form.querySelector("input");
  const error = form.querySelector(".field__error");
  const success = form.querySelector(".field__success");

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const valid = input.value.includes("@");
    input.setAttribute("aria-invalid", String(!valid));
    error.hidden = valid;
    success.hidden = !valid;
    if (!valid) input.focus();
  });
})();
