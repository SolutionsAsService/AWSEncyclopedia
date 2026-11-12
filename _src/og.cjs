// Usage: node _src/og.cjs <base-url>   Writes site/og.png (1200x630) from the home page's first screen.
const { chromium } = require('playwright');
const path = require('path');
(async () => { const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 }, colorScheme: 'light' });
  await p.goto(process.argv[2] + 'index.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(__dirname, '..', 'site', 'og.png') }); await b.close(); })();
