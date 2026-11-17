// Renderiza animacion.html a MP4 (1080x1920, 30 fps) con música.
// Uso: node render.js [--preview t1,t2,...]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const FPS = 30;
const dir = __dirname;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.join(dir, 'animacion.html'));
  await page.evaluate(async () => {
    for (const w of [600, 700, 800, 900]) await document.fonts.load(`${w} 40px Inter`);
  });
  const total = await page.evaluate(() => window.TOTAL);

  const prevIdx = process.argv.indexOf('--preview');
  if (prevIdx > -1) {
    const outDir = process.argv[prevIdx + 2] || dir;
    for (const t of process.argv[prevIdx + 1].split(',').map(Number)) {
      const url = await page.evaluate(t => { renderFrame(t); return document.getElementById('c').toDataURL('image/jpeg', .85); }, t);
      fs.writeFileSync(path.join(outDir, `prev_${t}.jpg`), Buffer.from(url.split(',')[1], 'base64'));
    }
    await browser.close();
    return;
  }

  const out = path.join(dir, 'sudadera-capucha-tutorial.mp4');
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error',
    '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-i', path.join(dir, 'musica.wav'),
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });

  const frames = Math.round(total * FPS);
  for (let f = 0; f < frames; f++) {
    const url = await page.evaluate(t => { renderFrame(t); return document.getElementById('c').toDataURL('image/jpeg', 0.95); }, f / FPS);
    const buf = Buffer.from(url.split(',')[1], 'base64');
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 150 === 0) console.log(`frame ${f}/${frames}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log('Listo:', out);
})();
