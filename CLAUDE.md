# Hilván · tienda de patrones de costura

Proyecto de una tienda online de patrones de costura en PDF ("Hilván"). La web es sencilla, de estilo tienda de moda, en blanco, grises y negro. Las fotos de producto son mitad prenda real y mitad su patrón.

- **Patrones:** cuando la usuaria pida un patrón, su manual o los PDF de una prenda, usa siempre la skill `patron-hilvan` (`.claude/skills/patron-hilvan/SKILL.md`). Define el formato fijo de 4 PDF (manual, A4, A0 y proyector) y trae la plantilla de código.
- **Resultados:** los patrones terminados van en `patrones/<prenda>-<REF>/`. El de referencia es `patrones/camiseta-H-031/`.
- **Clientas:** son principiantes. Todo tiene que ser muy fácil de recortar y de entender.
- **Idioma:** responde a la usuaria en español y con lenguaje sencillo.
