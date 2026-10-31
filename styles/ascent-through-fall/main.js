// Fit each title line to the width it has on the poster (data-fit, in % of the sheet width).
const poster = document.querySelector(".poster");
const lines = [...poster.querySelectorAll("[data-fit]")];

function fit() {
  const sheet = poster.clientWidth;
  lines.forEach((line) => {
    line.style.fontSize = `${sheet * 0.1}px`;
    const width = line.getBoundingClientRect().width;
    const target = (parseFloat(line.dataset.fit) / 100) * sheet;
    line.style.fontSize = `${sheet * 0.1 * (target / width)}px`;
  });
}

new ResizeObserver(fit).observe(poster);
document.fonts.ready.then(fit);
