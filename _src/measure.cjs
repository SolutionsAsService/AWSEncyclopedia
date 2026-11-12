// Usage: node _src/measure.cjs <base-url> <outdir>
// Enumerates every page in site/ (never a typed list), screenshots key pages, and measures
// overflow, the smallest text, the hero's bottom edge and targets under 44px.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [base, outdir] = process.argv.slice(2);
const root = path.join(__dirname, '..', 'site');
const walk = d => fs.readdirSync(path.join(root, d), { withFileTypes: true }).flatMap(e =>
  e.isDirectory() ? (e.name === 'fonts' ? [] : walk(path.join(d, e.name))) : e.name.endsWith('.html') ? [path.join(d, e.name)] : []);
const pages = walk('').sort((a, b) => (a === 'index.html' ? -1 : b === 'index.html' ? 1 : a.localeCompare(b)));
const shots = new Set(['index.html', 'services.html', 'why.html', 's3.html', 'shadw.html', 'start.html']);
(async () => {
  const b = await chromium.launch(); const report = [];
  for (const scheme of ['light', 'dark']) for (const [w, h] of [[1280, 800], [375, 812], [390, 844], [320, 640]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, colorScheme: scheme, hasTouch: w < 500 });
    const p = await ctx.newPage();
    for (const pg of pages) {
      await p.goto(base + pg, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
      const m = await p.evaluate(() => {
        let minFont = 99, minEl = '';
        for (const el of document.querySelectorAll('body *')) {
          if (el.closest('[aria-hidden="true"]')) continue;
          if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
          const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden') continue;
          const r = el.getBoundingClientRect(); if (!r.width) continue;
          const fs = parseFloat(cs.fontSize); if (fs < minFont) { minFont = fs; minEl = el.tagName + '.' + el.className + ' "' + el.textContent.trim().slice(0, 24) + '"'; }
        }
        const small = [...document.querySelectorAll('a:not(.wall a), button, summary')].filter(a => { const r = a.getBoundingClientRect(); if (!r.width) return false;
          const inline = getComputedStyle(a).display === 'inline' && a.closest('p, li, figcaption') && !a.closest('nav, .legend, .strip, .chips, .lessons, .pager'); return !inline && (r.height < 44 || r.width < 24); }).map(a => a.textContent.trim().slice(0, 20));
        const hero = document.querySelector('.hero'); let heroBottom = null, parts = {};
        if (hero) { for (const s of ['.hero h1', '.ctas', '.hero-fig']) { const e = document.querySelector(s); if (e && e.getBoundingClientRect().height) parts[s] = Math.round(e.getBoundingClientRect().bottom); } heroBottom = Math.max(...Object.values(parts)); }
        const selfcheck = document.documentElement.dataset.selfcheck || null; const figBad = []; for (const sv of document.querySelectorAll('svg.fig-svg, svg.mini, svg.hero-svg')) { const r = sv.getBoundingClientRect(); if (!r.width) continue; const vb = sv.viewBox.baseVal; const k = r.width / vb.width; for (const t of sv.querySelectorAll('text')) { if (t.closest('[aria-hidden="true"]') || t.hasAttribute('transform')) continue; const b = t.getBBox(); const px = parseFloat(getComputedStyle(t).fontSize) * k; if (b.x < -1 || b.x + b.width > vb.width + 1) figBad.push('clipped:' + t.textContent.slice(0, 20)); if (px < 12 && b.width) figBad.push(px.toFixed(1) + 'px:' + t.textContent.slice(0, 20)); if (sv.classList.contains('fig-svg')) for (const r2 of sv.querySelectorAll('rect')) { const c = r2.getBBox(); const ov = b.x < c.x + c.width && b.x + b.width > c.x && b.y < c.y + c.height && b.y + b.height > c.y; const inside = b.x >= c.x - 1 && b.x + b.width <= c.x + c.width + 1 && b.y >= c.y - 1 && b.y + b.height <= c.y + c.height + 1; if (ov && !inside) figBad.push('overlap:' + t.textContent.slice(0, 20)); } } } return { figBad: figBad.slice(0, 4), selfcheck, scrollW: document.documentElement.scrollWidth, minFont, minEl, small: small.slice(0, 5), nSmall: small.length, heroBottom, parts };
      });
      report.push({ scheme, w, h, page: pg, ...m, overflow: m.scrollW > w });
      if (shots.has(pg) && (scheme === 'light' || pg === 'index.html')) await p.screenshot({ path: `${outdir}/${pg.replace(/\//g, '_')}-${w}-${scheme}.png`, fullPage: pg !== 'index.html' });
    }
    await ctx.close();
  }
  await b.close();
  console.log(JSON.stringify(report).replace(/},{/g, '},\n{'));
})();
