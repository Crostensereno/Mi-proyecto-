# Genera voz/NN.wav a partir de frases.json con Kokoro (gratis, local).
# Uso: python3 generar_voz.py <carpeta_modelo_kokoro> [velocidad]
import sys, json, os, soundfile as sf
from kokoro_onnx import Kokoro
here = os.path.dirname(os.path.abspath(__file__))
k = Kokoro(os.path.join(sys.argv[1], 'kokoro-v1.0.onnx'), os.path.join(sys.argv[1], 'voices-v1.0.bin'))
speed = float(sys.argv[2]) if len(sys.argv) > 2 else 1.12
voz = k.get_voice_style('em_alex') * 0.7 + k.get_voice_style('em_santa') * 0.3  # mezcla: más cálida
dur = []
for i, t in enumerate(json.load(open(os.path.join(here, 'frases.json')))):
    a, sr = k.create(t, voice=voz, speed=speed, lang='es')
    sf.write(os.path.join(here, f'{i:02d}.wav'), a, sr)
    dur.append(round(len(a) / sr, 2))
json.dump(dur, open(os.path.join(here, 'duraciones.json'), 'w'))
print(dur)
