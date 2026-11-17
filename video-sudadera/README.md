# Promotional video: men's hoodie with a hood

- `sudadera-capucha-tutorial.mp4`: final video (1080x1920, 30 fps, 56 s, with music).
- `animacion.html`: the 2D animation. The texts for the final screen (call to action, benefits, button, link) are in `CONFIG` at the top of the file. Open it in a browser to see a preview.
- `musica.js`: generates original background music (`musica.wav`).

Re-render the video:

```
node musica.js
node render.js
```

## Stick-figure version (1.5x speed)

- `sudadera-capucha-muneco.mp4`: video with a stick figure narrating (41.6 s).
- `animacion-muneco.html`: what the stick figure says is in `DIALOGO`; the speed is in `SPEED`.
- `guion-voz.md`: the script with timestamps, for recording the voiceover.

```
node render.js animacion-muneco.html
```
- `sfx.js`: comedy sound effects (pop, whoosh, sewing machine, scissors, ta-da, ding), placed using `SFX` in `animacion-muneco.html`.
- `voz/`: voiceover lines (`frases.json`) and the script that generates them for free (`generar_voz.py`, Kokoro).
