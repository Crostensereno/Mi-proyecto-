# Anuncio Henley (Reels / TikTok) · idea guardada para retomar

Estado: **prueba aprobada como idea** (v1). Falta el vídeo real y la Henley en la tienda.

## La idea
Anuncio vertical 9:16 (1080×1920), unos 15 s, sin pagar vídeo con IA: **stop-motion con imágenes fijas** generadas en Runway (unos 4 créditos cada una) y montaje gratis con ffmpeg.

| Tiempo | Plano | Origen |
|---|---|---|
| 0–5 s | Persona real con camiseta Henley (cuello panadero) | **Vídeo de la usuaria**, grabado con el móvil en vertical, luz natural y fondo liso blanco o gris |
| 5–9 s | El patrón de la Henley dibujándose: papel → líneas → patrón completo → tijeras | Imágenes IA `fuentes/f1–f4.jpg` con zoom continuo |
| 9–12 s | Tienda Hilván en el móvil (scroll por el catálogo) | Grabación con Playwright (`fuentes/rec.js`) |
| Final | HILVÁN · "Cose tu propia camiseta Henley" · Patrón en PDF · tallas XS–XL · Enlace en la bio | `fuentes/card.html` → `card.png` |

Sin música: la usuaria la pone en Instagram o TikTok, con audio de tendencia.

## Cómo se generaron las imágenes (Runway, `nano-banana-2.1`, ratio 9:16)
Cada fotograma se genera **a partir del anterior** (`referenceImages` con el taskId previo, etiqueta `frame`) para que la mesa, el papel y los objetos no cambien.
1. **f1:** vista cenital, papel de patronaje blanco sobre mesa gris claro, regla transparente, lápiz, alfileres y cinta métrica. Solo las primeras líneas a lápiz. Monocromo, sin manos, sin texto.
2. **f2:** "@frame exactly the same scene… more pencil lines: shoulder, armhole, rounded neckline with a button placket…".
3. **f3:** el patrón delantero de la Henley terminado: contorno marcado, tapeta con botones, margen discontinuo, flecha de hilo y piquetes.
4. **f4:** tijeras negras abiertas recortando por el costado, con recortes de papel en la mesa.

## Montaje
`bash montar.sh <carpeta>`. La carpeta tiene que contener `f1–f4.jpg`, `web.mp4` y `card.png`.
- **Fotogramas:** 0,8 / 0,8 / 1,3 / 1,4 s, con zoom de 1,00 a 1,16 repartido entre ellos.
- **Transición a la tienda:** destello blanco.
- **Tienda:** se usan 3,2 s a partir del segundo 0,9, porque al principio las fotos aún no han cargado.
- **Cierre:** 2,2 s.

`web.mp4` se obtiene con `node fuentes/rec.js <carpeta> <ruta a la web index.html>`, que también genera `card.png`. Después se convierte a 1080×1920 con `ffmpeg -vf scale=1080:1920,fps=30`.

## Pendiente para la versión final
- [ ] Recibir el vídeo real de la usuaria y ponerlo al principio. Enlazarlo usando su último fotograma (por ejemplo, un primer plano del cuello) como referencia para f1.
- [ ] Añadir la Henley a la tienda: foto mitad prenda y mitad patrón, y su ficha. Si se vende, hacer su patrón con la skill `patron-hilvan`. Grabar la tienda mostrando la Henley y su ficha.
- [ ] Opcional: 2–4 imágenes intermedias para que el dibujo avance más suave (unos 4 créditos cada una).
- [ ] Cuando la web esté publicada, poner la dirección real en el cierre en lugar de "Enlace en la bio", si se quiere.
