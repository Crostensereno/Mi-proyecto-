# Genera voz/NN.wav con Piper y la voz "davefx" (castellano de España, CC0). Gratis y local.
# Uso: python3 generar_voz.py <modelo.onnx> [velocidad]
# 00.wav = gancho (dos frases unidas); 01..11 = resto de escenas.
import sys, json, os, wave, io
import numpy as np
from piper import PiperVoice, SynthesisConfig
here = os.path.dirname(os.path.abspath(__file__))
voice = PiperVoice.load(sys.argv[1])
speed = float(sys.argv[2]) if len(sys.argv) > 2 else 1.12
cfg = SynthesisConfig(length_scale=1 / speed, noise_scale=0.75, noise_w_scale=0.9)
sr = voice.config.sample_rate

def synth(text):
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as w: voice.synthesize_wav(text, w, syn_config=cfg)
    buf.seek(0)
    with wave.open(buf) as w: a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    nz = np.nonzero(np.abs(a) > 300)[0]  # recorta silencios
    return a[max(0, nz[0] - int(.03 * sr)): nz[-1] + int(.08 * sr)] if len(nz) else a

def save(i, a):
    with wave.open(os.path.join(here, f'{i:02d}.wav'), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(a.tobytes())
    return round(len(a) / sr, 2)

F = json.load(open(os.path.join(here, 'frases.json')))
a, b = synth(F['gancho'][0]), synth(F['gancho'][1])
gap = np.zeros(int(.18 * sr), dtype=np.int16)
dur = [save(0, np.concatenate([a, gap, b]))]
split = round((len(a) + len(gap)) / sr, 2)
for i, t in enumerate(F['voz'], start=1): dur.append(save(i, synth(t)))
json.dump({'duraciones': dur, 'gancho_corte': split}, open(os.path.join(here, 'duraciones.json'), 'w'))
print(dur, split)
