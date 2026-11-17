// Sintetiza los efectos de sonido (pop, whoosh, máquina de coser, tijeras, tachán, ding).
// Uso: node sfx.js eventos.json duracion salida.wav
const fs = require('fs');
const [, , evFile, durArg, out] = process.argv;
const ev = JSON.parse(fs.readFileSync(evFile, 'utf8'));
const sr = 44100, dur = Number(durArg), N = Math.floor(sr * dur);
const L = new Float32Array(N), R = new Float32Array(N);
let seed = 11; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647 * 2 - 1;
const TAU = Math.PI * 2;

function add(start, len, fn, pan = 0) {
  const s0 = Math.floor(start * sr), n = Math.floor(len * sr);
  const gl = Math.cos((pan + 1) * Math.PI / 4), gr = Math.sin((pan + 1) * Math.PI / 4);
  for (let i = 0; i < n && s0 + i < N; i++) { if (s0 + i < 0) continue; const v = fn(i / sr, i); L[s0 + i] += v * gl; R[s0 + i] += v * gr; }
}
const SFX = {
  // burbuja que aparece: barrido rápido hacia arriba
  pop: t => { let ph = 0; return (tt) => { const f = 500 + 1400 * Math.min(1, tt / 0.06); return 0.35 * Math.exp(-tt * 28) * Math.sin(TAU * f * tt); }; },
  // transición: ruido filtrado que sube y baja
  whoosh: () => { let lp = 0; return tt => { const env = Math.sin(Math.PI * Math.min(1, tt / 0.35)); const k = 0.04 + 0.25 * env; lp += k * (rnd() - lp); return 0.5 * env * lp; }; },
  // máquina de coser: golpecitos rápidos + zumbido grave
  machine: (d) => { let lp = 0; return tt => { const env = Math.min(1, tt / 0.05) * Math.min(1, (d - tt) / 0.08); const ph = (tt * 18) % 1; const tick = Math.exp(-ph * 30); lp += 0.3 * (rnd() - lp); return env * (0.16 * tick * lp * 4 + 0.05 * Math.sin(TAU * 110 * tt) * (0.6 + 0.4 * Math.sin(TAU * 18 * tt))); }; },
  // tijeras: dos chasquidos metálicos
  snip: () => tt => { const c = (x, f) => (tt > x ? Math.exp(-(tt - x) * 90) * (Math.sin(TAU * f * (tt - x)) * 0.6 + rnd() * 0.5) : 0); return 0.45 * (c(0, 3200) + c(0.07, 2600)); },
  // tachán: acorde mayor en arpegio con brillo
  tada: () => tt => { let v = 0; [[0, 523.25], [0.09, 659.25], [0.18, 783.99], [0.27, 1046.5]].forEach(([x, f]) => { if (tt > x) { const u = tt - x; v += Math.exp(-u * 2.5) * (Math.sin(TAU * f * u) + 0.4 * Math.sin(TAU * 2 * f * u) + 0.2 * Math.sin(TAU * 3 * f * u)); } }); return 0.16 * v; },
  // ding del botón
  ding: () => tt => 0.3 * Math.exp(-tt * 4) * (Math.sin(TAU * 1318.5 * tt) + 0.5 * Math.sin(TAU * 2637 * tt) * Math.exp(-tt * 6)),
};
const LEN = { pop: 0.25, whoosh: 0.4, snip: 0.25, tada: 2.2, ding: 1.5 };
for (const e of ev) {
  const len = e.type === 'machine' ? e.d : LEN[e.type];
  add(e.t, len, SFX[e.type](e.d), e.type === 'snip' ? 0.2 : 0);
}
const buf = Buffer.alloc(44 + N * 4);
buf.write('RIFF', 0); buf.writeUInt32LE(36 + N * 4, 4); buf.write('WAVE', 8);
buf.write('fmt ', 12); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(2, 22);
buf.writeUInt32LE(sr, 24); buf.writeUInt32LE(sr * 4, 28); buf.writeUInt16LE(4, 32); buf.writeUInt16LE(16, 34);
buf.write('data', 36); buf.writeUInt32LE(N * 4, 40);
for (let i = 0; i < N; i++) {
  buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, L[i])) * 32767), 44 + i * 4);
  buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, R[i])) * 32767), 46 + i * 4);
}
fs.writeFileSync(out, buf);
console.log('efectos generados:', ev.length);
