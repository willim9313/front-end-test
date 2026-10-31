const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1120, height: 800 } });
  for (const n of ['teal', 'cyan', 'coral']) {
    await p.setContent(`<style>html,body{margin:0;background:transparent}</style>${fs.readFileSync(`plate-${n}.svg`, 'utf8')}`);
    await p.locator('svg').screenshot({ path: `raw-${n}.png`, omitBackground: true });
  }
  await b.close();
})();
