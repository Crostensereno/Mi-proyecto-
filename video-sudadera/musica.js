// Genera una música de fondo original y ligera (musica.wav), sin derechos de terceros.
const fs = require('fs');
const path = require('path');

const sr = 44100, dur = Number(process.argv[2] || 57.5), N = Math.floor(sr * dur);
const L = new Float32Array(N), R = new Float32Array(N);
const mf = m => 440 * Math.pow(2, (m - 69) / 12);

function add(start, len, fn, pan = 0) {
  const s0 = Math.floor(start * sr), n = Math.floor(len * sr);
  const gl = Math.cos((pan + 1) * Math.PI / 4), gr = Math.sin((pan + 1) * Math.PI / 4);
  for (let i = 0; i < n && s0 + i < N; i++) {
    const v = fn(i / sr);
    L[s0 + i] += v * gl; R[s0 + i] += v * gr;
  }
}
const pluck = (f, a) => t => a * Math.min(1, t / 0.004) * Math.exp(-t * 5) *
  (Math.sin(2 * Math.PI * f * t) + 0.35 * Math.sin(4 * Math.PI * f * t) * Math.exp(-t * 8) + 0.12 * Math.sin(6 * Math.PI * f * t) * Math.exp(-t * 12));
const pad = (f, a, len) => t => a * Math.min(1, t / 0.6) * Math.min(1, (len - t) / 0.5) * (Math.sin(2 * Math.PI * f * t) + 0.2 * Math.sin(2 * Math.PI * f * 2.003 * t));
const bass = (f, a) => t => a * Math.min(1, t / 0.01) * Math.exp(-t * 2.2) * Math.sin(2 * Math.PI * f * t);
const kick = a => t => a * Math.exp(-t * 16) * Math.sin(2 * Math.PI * (45 * t + 60 * (1 - Math.exp(-t * 30)) / 30));
let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647 * 2 - 1;
const shaker = a => { let prev = 0; return t => { const n = rnd(); const v = n - prev; prev = n; return a * v * Math.exp(-t * 55); }; };

const beat = Number(process.argv[3] || 0.6), bar = beat * 4;
const chords = [
  { arp: [60, 64, 67, 72], bass: 36 }, // C
  { arp: [59, 62, 67, 71], bass: 43 }, // G
  { arp: [60, 64, 69, 72], bass: 45 }, // Am
  { arp: [60, 65, 69, 72], bass: 41 }, // F
];
const pattern = [0, 1, 2, 3, 2, 1, 2, 3];
const bars = Math.ceil(dur / bar);
for (let b = 0; b < bars; b++) {
  const c = chords[b % 4], t0 = b * bar;
  pattern.forEach((k, i) => add(t0 + i * beat / 2, 1.2, pluck(mf(c.arp[k] + 12), 0.16), i % 2 ? 0.35 : -0.35));
  c.arp.slice(0, 3).forEach(m => add(t0, bar, pad(mf(m), 0.035, bar)));
  add(t0, bar, bass(mf(c.bass), 0.32));
  add(t0 + beat * 2.5, bar, bass(mf(c.bass + 7), 0.18));
  if (b >= 1) {
    for (let q = 0; q < 4; q++) {
      if (q % 2 === 0) add(t0 + q * beat, 0.4, kick(0.55));
      add(t0 + q * beat + beat / 2, 0.12, shaker(0.07), 0.2);
    }
  }
}
// final: acorde de Do
add(dur - 3.2, 3.2, pad(mf(48), 0.06, 3.2));

let peak = 0;
for (let i = 0; i < N; i++) peak = Math.max(peak, Math.abs(L[i]), Math.abs(R[i]));
const g = 0.8 / peak;
const buf = Buffer.alloc(44 + N * 4);
buf.write('RIFF', 0); buf.writeUInt32LE(36 + N * 4, 4); buf.write('WAVE', 8);
buf.write('fmt ', 12); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(2, 22);
buf.writeUInt32LE(sr, 24); buf.writeUInt32LE(sr * 4, 28); buf.writeUInt16LE(4, 32); buf.writeUInt16LE(16, 34);
buf.write('data', 36); buf.writeUInt32LE(N * 4, 40);
for (let i = 0; i < N; i++) {
  const t = i / sr;
  const fade = Math.min(1, t / 0.3) * Math.min(1, (dur - t) / 2.5);
  buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, L[i] * g * fade)) * 32767), 44 + i * 4);
  buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, R[i] * g * fade)) * 32767), 46 + i * 4);
}
fs.writeFileSync(path.join(__dirname, process.argv[4] || 'musica.wav'), buf);
console.log('musica.wav generada');
