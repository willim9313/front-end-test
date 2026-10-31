// Screenshot every style page into styles/<slug>/thumb.jpg (640x400) for the overview.
// Run from the repo root with a static server on :8000:
//   python3 -m http.server 8000 &   then   node overview/tools/thumbs.js [slug ...]
const { chromium } = require("playwright");
const fs = require("fs");
const vm = require("vm");

const ctx = { window: {} };
vm.runInNewContext(fs.readFileSync("overview/catalog.js", "utf8"), ctx);
const only = process.argv.slice(2);
const slugs = ctx.window.STYLES.map((s) => s.slug).filter((s) => !only.length || only.includes(s));

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1280, height: 800 },
    deviceScaleFactor: 0.5,
    reducedMotion: "reduce",
    colorScheme: "light",
  });
  for (const slug of slugs) {
    await page.goto(`http://localhost:8000/styles/${slug}/`, { waitUntil: "networkidle" });
    await page.evaluate(() => document.fonts.ready);
    // keep the shared "← 目錄 / 規格" bar out of the thumbnail
    await page.addStyleTag({ content: "style-spec { display: none !important; }" });
    await page.waitForTimeout(600);
    await page.screenshot({ path: `styles/${slug}/thumb.jpg`, type: "jpeg", quality: 78 });
    console.log("thumb", slug);
  }
  await browser.close();
})();
