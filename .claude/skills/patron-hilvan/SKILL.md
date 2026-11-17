---
name: patron-hilvan
description: Crear un patrón de costura completo para la tienda Hilván con su formato fijo de 4 PDF (manual, patrón A4, patrón A0 y patrón para proyector), tallas en color, una talla por página, margen incluido y foto de portada mitad prenda real y mitad patrón. Úsala siempre que la usuaria pida un patrón, un manual de patrón, pasar un patrón a escala real, rehacer o ampliar los PDF de un patrón, o añadir una prenda nueva a la tienda.
---

# Patrón Hilván: formato fijo

La usuaria vende patrones de costura en PDF en su tienda **Hilván** (web en blanco, grises y negro). Sus clientas **no saben nada de patronaje**: todo tiene que poder recortarse con tijeras y entenderse sin explicaciones. Este formato está aprobado por ella ("10 de 10"): **no lo cambies sin que lo pida**.

La implementación de referencia es la **camiseta básica H-031** (`plantilla/`) y su resultado final está en `patrones/camiseta-H-031/`. Para un patrón nuevo, copia `plantilla/` a una carpeta de trabajo y cambia solo la geometría y los textos de la prenda.

## Qué se entrega (siempre 4 PDF)

Carpeta `patrones/<prenda>-<REF>/` con estos nombres:

| Archivo | Contenido |
|---|---|
| `Hilvan_<REF>_<Prenda>_1_Manual.pdf` | Manual A4 vertical (~17 págs.) |
| `Hilvan_<REF>_<Prenda>_2_Patron_A4.pdf` | Hoja de instrucciones + 18 hojas A4 apaisadas **por talla** |
| `Hilvan_<REF>_<Prenda>_3_Patron_A0.pdf` | 1 página A0 por talla + 1 página con todas las tallas (para calcar) |
| `Hilvan_<REF>_<Prenda>_4_Patron_Proyector.pdf` | 1 página por talla clara + 1 por talla oscura + 1 con todas las tallas |

Al terminar: copiar los PDF a esa carpeta, enviarlos con SendUserFile y hacer commit y push en la rama de trabajo.

## Reglas del patrón (A4, A0 y proyector)

- **Escala real 1:1** y **margen de costura incluido** en la línea de corte. Por defecto: 1 cm escote, 1,5 cm hombros/sisas/costados/copa/bajomanga, 2,5 cm bajos y bocas, 0 en el doblez.
- **Una talla por página**: nunca tallas anidadas, salvo en la página final "todas las tallas, para calcar" del A0 y del proyector.
- **Colores por talla**: XS `#7c3aed` (morado), S `#2563eb` (azul), M `#16a34a` (verde), L `#ea7a0c` (naranja), XL `#e11d48` (rojo). En la versión oscura del proyector se usan los tonos claros de `COL_DARK`.
- **Cada pieza** se dibuja así:
  - Relleno muy suave del color de la talla.
  - **Línea gruesa del color de la talla** = recortar.
  - **Iconos de tijeras** a lo largo de los bordes que se cortan.
  - **Borde negro grueso** con el texto "DOBLEZ DE LA TELA · NO CORTAR ESTE BORDE" en las piezas al doblez.
  - **Puntos grises** = línea de costura.
  - Flecha de hilo y piquetes.
  - Cartel grande con el nombre de la pieza, una pastilla "TALLA X" de color, "Corta 1 pieza / Corta 2 piezas" e instrucciones en frases cortas.
- **Las piezas rectangulares** (tiras, vistas…) también se dibujan para recortarlas, con sus medidas escritas.
- **Bloque de leyenda** en cada plancha:
  - Logo HILVÁN y referencia.
  - Talla.
  - "Cómo se usa" con las 4 líneas: color, tijeras, negro y gris.
  - **Cuadrado de prueba de 5 × 5 cm**.
  - Regla de 10 cm.
  - Lista de piezas.
- **Plancha**: 83,1 × 114 cm, el área de 3 × 6 hojas A4 apaisadas. Las piezas se reparten para que quepa en A0 (84,1 × 118,9 cm).

### A4 (imprimir en casa)
- **Página 1:**
  - Tabla "imprime solo tu talla" con el rango de páginas de cada talla, en color.
  - Cuadrado de prueba.
  - Pasos para unir las hojas.
  - Mapa de montaje con el código y el número de cada hoja.
- **Hojas:** apaisadas, con márgenes de 1 cm y ventana de 27,7 × 19 cm. Cada una lleva:
  - Una cabecera con la pastilla de la talla en color, el código (A1…) y "hoja k de 18 de tu talla · página n de N".
  - El código grande y tenue de fondo.
  - Marco y **medios rombos negros** en los bordes interiores, para unir.
  - "une con B1 →" y "↓ une con A2" en los márgenes.
- **Orden de las hojas por columnas**: A1, A2… A6, luego B1… B6 y C1… C6, para que cada hoja se pegue debajo de la anterior. Lo pidió la usuaria expresamente.
- **Instrucciones de unión:** recortar el margen derecho y el de abajo, y unir las hojas a tope haciendo coincidir los rombos.

### A0 y proyector
- **A0:** una página por talla con la cabecera "TALLA X · imprime solo la página de tu talla al 100 %", y al final una página con todas las tallas.
- **Proyector:** cuadrícula de 10 cm con números, líneas más gruesas (`lw=.085`), versión clara y versión oscura (fondo negro) de cada talla, y al final una página con todas las tallas.

## Manual (estilo de la web)

- **Estilo:** blanco, grises y negro con tipografías **Archivo** (títulos, `font-stretch` ancho) e **Inter** (texto). **El único color son los de las tallas**: pastillas de talla en su color y, en las tablas, los números de cada columna en el color de su talla. Cabecera con antetítulo y título sobre una línea negra, y pie con "HILVÁN · <prenda> · Ref. · tallas" y "n / total".
- **Portada:** foto de la prenda **mitad real, mitad patrón** (ver más abajo), logo, título, entradilla, fila con nivel, tiempo, tallas y tela, y pastillas de las tallas.
- **Páginas, en este orden:**
  1. Portada.
  2. Bienvenida: piezas en miniatura de color, archivos que incluye e índice.
  3. Materiales y herramientas, y tela por talla.
  4. Guía de tallas: figura, cómo medirse y tabla del cuerpo.
  5. Medidas de la prenda terminada (dibujo con letras), longitud de cada costura y piezas rectangulares.
  6. Cómo imprimir: tabla de páginas por talla de A4, A0 y proyector, pasos del A4, proyector, cuadrado de prueba y mapa.
  7. Cómo leer el patrón: pieza de ejemplo, significado de cada línea, márgenes y piezas con su cantidad.
  8. Cómo cortar la tela: plano de corte a escala con la talla M.
  9. Antes de coser: lo esencial, diccionario, ajustes de la máquina y reglas de oro.
  10. Montaje paso a paso, dos pasos por página, cada uno con dibujo, lista numerada y consejo.
  11. (Continúa el montaje.)
  12. (Continúa el montaje.)
  13. Último paso y resumen de costuras.
  14. Remate y revisión: lista de comprobación, "si algo sale mal" y cuidado de la prenda.
  15. **Sin impresora: dibújalo con regla.** Una página por pieza con diagrama de puntos y **tabla de coordenadas x/y de la línea de corte (margen incluido) para cada talla**, con el (0, 0) arriba del doblez y las curvas marcadas con c/s. En la manga, se dibuja la mitad sobre el papel doblado.
- Añade o quita páginas según la prenda, pero mantén el orden y el estilo, y actualiza `TOTAL` y el índice.

## Foto de portada (Runway)

Genera con `mcp__RunwayApp__generate_image` usando `model: nano-banana-2.1` y `ratio: 3:4`, unos 4 créditos. Usa esta plantilla de prompt cambiando solo la prenda:

> Fashion e-commerce product image, pure light grey studio background, a single <PRENDA en inglés, color y tejido> shown front-facing … perfectly centered. The image is split exactly down the vertical center line of the garment: the LEFT half is a realistic photograph of the real garment (…); the RIGHT half shows the same garment's matching half drawn as a sewing pattern / technical flat: thin black ink lines on white pattern paper, with seam lines, dashed stitch lines, a grainline arrow and notches, lining up seamlessly with the photo at the center so the silhouette continues. Minimalist, monochrome, black white and grey only, no text, no logos.

- **Descarga:** las imágenes están en `dnznrvs05pmza.cloudfront.net`. El entorno "Mi-proyecto-" ya permite ese host. Si la descarga da 403, revisa el entorno con `get_environment`.
- **Destino:** convierte la imagen a JPG y guárdala como `build/portada.jpg`.
- **Fondo de la portada:** en el CSS del manual, `--photo` es el gris del fondo de la foto (#e3e3e3) y la imagen va con `object-fit:contain`, para que no se corte.
- **Web:** usa la misma foto para el producto en el catálogo de la tienda.

## Flujo de trabajo

1. **Lee el patrón de origen** que te dé la usuaria (PDF con tablas de coordenadas, medidas o tallas). Con el Read de PDF por rangos de páginas y `pdftotext -layout` sacas todas las tablas.
2. **Copia `plantilla/` a una carpeta de trabajo** en el scratchpad.
3. **Prepara las herramientas:** `pip install shapely numpy` si falta. Playwright y Chromium ya están instalados.
4. **En `geo.py`**, pon los puntos de costura por talla y los márgenes:
   - `catmull()` suaviza las curvas.
   - `cut_outline()` añade el margen con un valor por borde y devuelve también cada borde (`segs`), que sirve para marcar el doblez y las tijeras y para sacar las coordenadas.
   - **Comprueba que las longitudes coinciden** con la tabla de costuras del original antes de seguir.
5. **En `render2.py`**, ajusta las piezas, las posiciones (`*_O`), los textos de cada pieza y las piezas rectangulares para que todo quepa en la plancha y en A0.
6. **En `manual.py`**, cambia los textos y datos de la prenda: materiales, tallas, medidas, pasos de montaje y sus dibujos, plano de corte y puntos del anexo.
7. **Genera los HTML** con `python3 render2.py && python3 manual.py` y después los PDF con `node print.js build/manual.html:out/manual.pdf build/a4.html:out/a4.pdf build/a0.html:out/a0.pdf build/proyector.html:out/proyector.pdf`. Chromium respeta el tamaño de página CSS, así que la escala es exacta.
8. **Verifica antes de entregar:**
   - Tamaño de página y número de páginas con pdfplumber.
   - **Que el cuadrado de prueba mida 5,0 × 5,0 cm** en la página 1 del A4, en una hoja del A4 que lo contenga, en el A0, en el proyector y en la página 6 del manual.
   - Vistas previas con `pdftoppm` y `montage` para revisar que no haya textos montados ni páginas desbordadas.
9. **Entrega:** copia los 4 PDF a `patrones/<prenda>-<REF>/`, envíalos y haz commit y push. Opcionalmente, añade la prenda al catálogo de la web.

## Problemas ya resueltos

- **Cuadrado de prueba:** un `<svg>` dentro de un contenedor flex se encoge (salía de 4,58 cm). Pon `flex:none` en el svg del cuadrado de prueba.
- **Fuentes:** se cargan de Google Fonts en Chromium. Espera a `document.fonts.ready`, que ya lo hace `print.js`.
- **Borrar archivos:** no uses `rm` con comodines relativos tras un `cd`, porque lo bloquea una comprobación de seguridad. Crea carpetas de vista previa nuevas en lugar de vaciar las viejas.
- **Etiqueta de talla en las piezas:** su ancho se calcula a partir del texto "TALLA X" en `badge()`.
- **Datos inventados:** las referencias (H-0xx), los precios y los niveles son inventados mientras la usuaria no dé los suyos. Díselo y mantén coherentes el nivel de la web y el del manual.
