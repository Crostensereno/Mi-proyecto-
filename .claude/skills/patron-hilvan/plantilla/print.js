// Imprime los HTML de build/ a PDF con Chromium, respetando el tamaño de página CSS (escala exacta).
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const jobs = process.argv.slice(2); // pares html:pdf
  const b = await chromium.launch();
  for (const job of jobs) {
    const [src, dst] = job.split(':');
    const p = await b.newPage();
    await p.goto('file://' + path.resolve(src), { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: dst, preferCSSPageSize: true, printBackground: true, scale: 1 });
    await p.close();
    console.log('pdf', dst);
  }
  await b.close();
})();
