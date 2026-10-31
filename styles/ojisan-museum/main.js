const exhibit = document.querySelector(".exhibit");
const spots = [...exhibit.querySelectorAll(".spot")];
const guide = document.querySelector("[data-guide]");

spots.forEach((spot, i) => spot.style.setProperty("--i", i));

function open(spot) {
  spots.forEach((s) => {
    const on = s === spot;
    s.setAttribute("aria-expanded", String(on));
    document.getElementById(s.getAttribute("aria-controls")).classList.toggle("is-open", on);
  });
}

// Hover previews a label on pointer devices; click (or tap) pins it.
spots.forEach((spot) => {
  spot.addEventListener("click", (event) => {
    event.stopPropagation();
    open(spot.getAttribute("aria-expanded") === "true" ? null : spot);
  });
  spot.addEventListener("mouseenter", () => {
    document.getElementById(spot.getAttribute("aria-controls")).classList.add("is-lit");
    if (!spots.some((s) => s.getAttribute("aria-expanded") === "true")) {
      document.getElementById(spot.getAttribute("aria-controls")).classList.add("is-open");
    }
  });
  spot.addEventListener("mouseleave", () => {
    document.getElementById(spot.getAttribute("aria-controls")).classList.remove("is-lit");
    if (spot.getAttribute("aria-expanded") !== "true") {
      document.getElementById(spot.getAttribute("aria-controls")).classList.remove("is-open");
    }
  });
});

document.addEventListener("click", () => open(null));
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") open(null);
});

// Guide mode: every label at once, like walking the room with the audio guide on.
guide.addEventListener("click", () => {
  const on = exhibit.classList.toggle("is-guide");
  guide.setAttribute("aria-pressed", String(on));
  if (on) open(null);
});
