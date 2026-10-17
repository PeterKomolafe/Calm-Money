// Prints each guide HTML to an A4 PDF and saves page screenshots for review
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = path.join(__dirname, 'out');
  const b = await chromium.launch();
  for (const f of fs.readdirSync(dir).filter((x) => x.endsWith('.html'))) {
    const p = await b.newPage();
    await p.goto('file://' + path.join(dir, f));
    await p.evaluate(() => document.fonts.ready);
    // flag any page whose content overflows its A4 box
    const over = await p.evaluate(() => [...document.querySelectorAll('.page')].map((pg, i) => {
      const foot = pg.querySelector('.foot, .bottom'); const last = [...pg.children].filter(c => c !== foot && !c.classList.contains('letter') && !c.classList.contains('photo')).pop();
      return foot && last && last.getBoundingClientRect().bottom > foot.getBoundingClientRect().top + 1 ? i + 1 : null;
    }).filter(Boolean));
    await p.pdf({ path: path.join(dir, f.replace('.html', '.pdf')), format: 'A4', printBackground: true, preferCSSPageSize: true });
    console.log(f, over.length ? 'OVERFLOW on pages ' + over : 'ok');
    await p.close();
  }
  await b.close();
})();
