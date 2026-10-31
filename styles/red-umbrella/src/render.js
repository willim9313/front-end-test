// Render scene.svg to scene-raw.png with headless Chromium (Playwright).
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 736, height: 1308 } });
  await p.setContent(`<style>html,body{margin:0}</style>${fs.readFileSync('scene.svg', 'utf8')}`);
  await p.locator('svg').screenshot({ path: 'scene-raw.png' });
  await b.close();
})();
