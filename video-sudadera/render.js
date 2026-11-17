// Renderiza animacion.html a MP4 (1080x1920, 30 fps) con música.
// Uso: node render.js [archivo.html] [--preview t1,t2,... [carpeta]]
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const FPS = 30;
const dir = __dirname;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  const html = process.argv[2] && !process.argv[2].startsWith('--') ? process.argv[2] : 'animacion.html';
  await page.goto('file://' + path.join(dir, html));
  await page.evaluate(async () => {
    for (const w of [600, 700, 800, 900]) await document.fonts.load(`${w} 40px Inter`);
  });
  const total = await page.evaluate(() => window.TOTAL);
  const speed = await page.evaluate(() => window.SPEED || 1);

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

  const base = html === 'animacion.html' ? 'sudadera-capucha-tutorial' : 'sudadera-capucha-' + html.replace('animacion-', '').replace('.html', '');
  const out = path.join(dir, base + '.mp4');
  const wav = base + '.wav';
  execFileSync('node', [path.join(dir, 'musica.js'), String(total / speed + 1), String(speed > 1 ? 0.42 : 0.6), wav], { stdio: 'inherit' });
  // Voz (opcional): voz/NN.wav colocadas en VOZ_STARTS; la música baja cuando habla.
  const starts = await page.evaluate(() => window.VOZ_STARTS || []);
  const voces = starts.map((st, i) => ({ st, f: path.join(dir, 'voz', String(i).padStart(2, '0') + '.wav') }))
    .filter(v => v.st !== null && fs.existsSync(v.f));
  const audioIn = [], filt = [];
  voces.forEach((v, i) => { audioIn.push('-i', v.f); filt.push(`[${i + 2}:a]aresample=44100,aformat=channel_layouts=stereo,volume=1.6,adelay=${Math.round(v.st * 1000)}|${Math.round(v.st * 1000)}[v${i}]`); });
  // Efectos de sonido (opcional): window.SFX -> sfx.js
  const sfxEv = await page.evaluate(() => window.SFX || null);
  const sfxWav = base + '-sfx.wav', sfxJson = path.join(dir, base + '-sfx.json');
  if (sfxEv) {
    fs.writeFileSync(sfxJson, JSON.stringify(sfxEv));
    execFileSync('node', [path.join(dir, 'sfx.js'), sfxJson, String(total / speed + 1), path.join(dir, sfxWav)], { stdio: 'inherit' });
    audioIn.push('-i', path.join(dir, sfxWav));
    filt.push(`[${voces.length + 2}:a]volume=0.9[sfx]`);
  }
  let audioMap = ['-map', '1:a'];
  if (voces.length) {
    filt.push(`${voces.map((_, i) => `[v${i}]`).join('')}amix=inputs=${voces.length}:normalize=0[voz]`,
      '[voz]apad[vozp]', '[vozp]asplit[voz1][voz2]', '[1:a]volume=0.8[mus]',
      '[mus][voz1]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[musd]',
      `[musd][voz2]${sfxEv ? '[sfx]' : ''}amix=inputs=${sfxEv ? 3 : 2}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[aout]`);
    audioMap = ['-filter_complex', filt.join(';'), '-map', '[aout]'];
  }
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error',
    '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-i', path.join(dir, wav), ...audioIn,
    '-map', '0:v', ...audioMap,
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });

  const frames = Math.round(total / speed * FPS);
  for (let f = 0; f < frames; f++) {
    const url = await page.evaluate(t => { renderFrame(t); return document.getElementById('c').toDataURL('image/jpeg', 0.95); }, f / FPS * speed);
    const buf = Buffer.from(url.split(',')[1], 'base64');
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 150 === 0) console.log(`frame ${f}/${frames}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  fs.unlinkSync(path.join(dir, wav));
  if (sfxEv) { fs.unlinkSync(path.join(dir, sfxWav)); fs.unlinkSync(sfxJson); }
  console.log('Listo:', out);
})();
