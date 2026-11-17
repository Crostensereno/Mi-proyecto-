# Project: sewing patterns and manuals (PDF for sale) + promo videos

## Who I am and how I want things done
- I sell **PDF manuals with sewing patterns** for men's garments. Each garment is a separate product.
- Always talk to me in **Spanish from Spain (Castilian)**, in a casual, close tone. Every text meant for my customers is also in Castilian Spanish (use "vosotros", never Latin American expressions).
- The target reader of each manual is someone who **knows nothing about sewing** and only has **a sewing machine, paper and fabric**. It has to be "the easiest manual ever": everything in **centimetres**, numbered steps, a drawing for every step, and nothing assumed as known.
- I don't have a background in pattern-making: if a measurement is an estimate, say so and recommend a test garment.

## Garment manuals (the most important thing)
- The format is fixed: the one in the **hoodie manual** (`sudadera_capucha_patron_1-5_XS-XL.pdf`, 25 pages). The **shirt manual** follows it exactly and is the code reference.
- To make a new garment, **use the `manual-patron` skill** (`.claude/skills/manual-patron/SKILL.md`). It covers the structure, the rules and the code.
- Code: `manuales/plantilla.py` (shared style and components: DO NOT change the look), `manuales/<garment>_geo.py` (measurements and geometry), `manuales/<garment>.py` (pages). Output in `manuales/salida/`.
- Garments done: hoodie (made in an earlier session, PDF only), shirt (`manuales/camiseta*.py`).

## Promo videos
- `video-sudadera/`: 2D animated videos (canvas + Playwright + ffmpeg), vertical 1080x1920. See its README.
- Every sales video starts with a **hook in the first second** (e.g. "¿Harto de pagar 40 € por una sudadera? ¡Hazte la tuya!").
- Voice: ideally mine (I send it and you clean it up and sync it); the free alternative is Piper `davefx` (Spain Spanish). Runway costs money: don't use it without asking.
