# Estado del proyecto Hilván (actualizado el 18-11-2026)

## Hecho
- **Web de la tienda** (`web/`, y en ZIP `hilvan_web.zip`). Diseño de tienda de moda en blanco, grises y negro, con fotos mitad prenda real y mitad patrón.
  - Vista previa: https://claude.ai/artifact/QeihCxazz8HYBbnduVEf5D
  - Solo la **Camiseta básica** se puede comprar: el botón "Comprar · 9,00 €" lleva a Payhip, https://payhip.com/b/HFg5q
  - El resto de prendas son de ejemplo y aparecen como **"Próximamente"**.
  - Se quitó la cesta de demostración, porque el pago lo hace Payhip.
- **Patrón camiseta H-031** (`patrones/camiseta-H-031/`): 4 PDF (manual, A4, A0, proyector), fotos de producto y `patrones/Hilvan_H-031_Camiseta_basica.zip`. Ese ZIP ya está subido a Payhip.
- **Patrón bermuda H-032** (`patrones/bermuda-H-032/`): 4 PDF, fotos y `patrones/Hilvan_H-032_Bermuda.zip`, listo para subir a Payhip. Trazado desde cero; precio y nivel por definir. Aún no está en la web.
- **Skill `patron-hilvan`** (`.claude/skills/patron-hilvan/`): el formato fijo y la plantilla para hacer patrones nuevos.
- **Idea de anuncio** en stop-motion para la Henley (`anuncios/henley/README.md`). Está guardada y falta el vídeo real de la usuaria.

## Decisiones tomadas
- **Sin Shopify:** dominio en **Dinahosting**, alojamiento gratis en **Netlify** (recomendado: Netlify Drop, arrastrando la carpeta `web/`) o en GitHub Pages, y cobros con **Payhip**.
- **Formato de los patrones:** el producto que se vende es un ZIP con los 4 PDF.

## Siguiente paso (para mañana)
1. **Precio:** confirmar que el precio de Payhip es 9 €. Si no, cambiarlo en `web/index.html` (`price:9` de la camiseta).
2. **Publicar la web:** en Netlify Drop, con la carpeta `web/`, y comprobar que el botón de compra funciona.
3. **Dominio:** elegir y comprar el dominio en Dinahosting y conectarlo a Netlify (DNS).
4. **Web real:**
   - Revisar los textos.
   - Quitar o mantener las prendas "Próximamente".
   - Añadir páginas legales: aviso legal, privacidad, cookies y condiciones de venta (consultar con su gestor).
   - Opcional: un formulario para dejar el email.
5. **Más adelante:**
   - Siguientes patrones con la skill.
   - La Henley: patrón, ficha en la web y anuncio.
   - Redes: Instagram, TikTok y Pinterest.

## Nota
Todo está en la rama `claude/blissful-shannon-4r6dk2`. Pendiente: proponer una pull request para pasarlo a la rama principal, para que las sesiones nuevas lo vean aunque empiecen desde `main`.
