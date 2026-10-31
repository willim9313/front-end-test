// Render SVG files to PNG or JPEG with headless Chromium (Playwright).
//   node tools/render-svg.js in.svg out.png [--opaque]
//   node tools/render-svg.js in.svg out.jpg            (JPEG is always opaque)
// The output size is the SVG's width/height attributes. PNG keeps transparency
// unless --opaque is given.
const { chromium } = require("playwright");
const fs = require("fs");

(async () => {
  const [input, output, flag] = process.argv.slice(2);
  const svg = fs.readFileSync(input, "utf8");
  const w = Number(/<svg[^>]*\swidth="([\d.]+)"/.exec(svg)[1]);
  const h = Number(/<svg[^>]*\sheight="([\d.]+)"/.exec(svg)[1]);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: Math.ceil(w), height: Math.ceil(h) } });
  await page.setContent(`<style>html,body{margin:0;background:transparent}svg{display:block}</style>${svg}`);
  await page.evaluate(() => document.fonts.ready);
  const jpeg = /\.jpe?g$/i.test(output);
  await page.locator("svg").first().screenshot({
    path: output,
    type: jpeg ? "jpeg" : "png",
    quality: jpeg ? 86 : undefined,
    omitBackground: !jpeg && flag !== "--opaque",
  });
  await browser.close();
  console.log("rendered", output, `${w}x${h}`);
})();
