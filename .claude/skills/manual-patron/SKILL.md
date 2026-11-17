---
name: manual-patron
description: Creates the PDF sewing manual + 1:5 pattern for a new men's garment (t-shirt, trousers, shirt...) in the exact format of the hoodie and shirt manuals. Use it whenever the user asks for "the manual/pattern for <garment>", or to change an existing manual.
---

# Pattern manual in the house format

The user sells these PDFs. The format is **fixed**: copy `manuales/camiseta.py` as the base and reuse
`manuales/plantilla.py` without touching its style. Language: **Spanish from Spain**. Reader: someone who has
never sewn and only has a machine, paper and fabric.

## How to work
1. Create `manuales/<garment>_geo.py` with the geometry (copy `camiseta_geo.py`):
   - Sizes **XS–XL**, same body measurements as the hoodie (chest 84–88 / 92–96 / 100–104 / 108–112 / 116–120,
     waist, hip, height). Ease above the upper limit of the chest (shirt 8 cm, hoodie 12 cm).
   - Coordinates in cm **without seam allowance**, origin (0,0) top left, x to the right, y downwards,
     the x=0 edge is the **fold**. Named points: corners with letters (A, B, C…), curves sampled as c1…c7
     (neck), s1…s8 (armhole and cap).
   - **Matching seams must measure the same**: sleeve cap = armhole (solve it numerically, as `resolver_manga`
     does), neck band = % of the neckline, etc. Print a check table (`python3 <garment>_geo.py`) and look at
     whether the measurements are realistic before drawing (e.g. sleeve width at the armpit for size M ≈ 38–42 cm on a tee).
2. Create `manuales/<garment>.py` copying the page structure of `camiseta.py` and changing texts and drawings.
3. Generate: `cd manuales && python3 <garment>.py` → `manuales/salida/<garment>_patron_1-5_XS-XL.pdf`.
4. **Check visually**: `pdftoppm -r 75 -png` and look at EVERY page (overlaps, text running off the page,
   drawings out of scale, legend over the boxes). Fix and regenerate.
5. Give the user the PDF and list which measurements are estimates (recommend a test garment).

## Page order (always the same)
1. **Cover** (navy background, decorative circles, garment drawing in orange tones, size pills,
   orange band with 3 figures: "1:5 patterns with grid", "N illustrated steps", "5 sizes, XS to XL").
2. **Bienvenida** (welcome): intro paragraph in bold, 3 cards (Level / Time / Sizes), "The pieces of your
   <garment>" with icons and quantity, "What you'll find in this PDF" contents with page numbers
   (`doc.num('anchor')`), tip box.
3. **Materiales y herramientas** (materials and tools): numbered list of things to buy, tools with ticks,
   table "How much you need by size" (metres of 150 cm fabric folded = 75 cm), notes (pre-wash…).
4. **Guía de tallas** (size guide): silhouette with chest/waist/hip, how to measure yourself, body-measurement
   table, 3 cards (Fit / If in doubt / Lengths), how each size is calculated.
5. **Medidas de la prenda terminada** (finished garment measurements): drawing with letters A, B, C… +
   table; "Length of each seam (cm, without allowance)"; rectangles (bands, cuffs…).
6. **Cómo pasar el patrón a tu papel** (how to transfer the pattern to your paper): method A coordinates /
   method B grid + grid example.
7. **Cómo leer los dibujos** (how to read the drawings): line symbols per size, fold, grain, letter, box;
   seam allowance table; pieces and quantity table.
8. **Cómo cortar la tela** (how to cut the fabric): cutting layout for size M to scale on 75 cm + steps + tip.
9. **Antes de coser: lo esencial** (before sewing: the basics): right sides together / backstitch / seam
   allowance, glossary, machine settings, five golden rules.
10. **Step-by-step assembly**: 2 steps per page (number in an orange circle, "PASO n", title, cream box with
    a drawing on the left, numbered list on the right, TIP box underneath).
11. **Remate y revisión** (finishing and check): "Your <garment> is ready!", checklist, "If something goes
    wrong" table, garment care.
12. For each piece: **1:5 pattern page** (`pagina_patron`: grid 2/10 cm, 5 sizes with colour and line type,
    measurement boxes with a leader line, legend, scale bar of 5 cm = 25 cm, piece sizes, "Cómo copiarlo"
    (how to copy it)) + **coordinates page** (`pagina_coordenadas`).
13. Rectangular pieces (bands, cuffs): measurements per size table, drawing with fold and stretch direction,
    1:1 ruler at the end.

## Style rules (already in plantilla.py)
- A4, **Poppins** font (`manuales/fuentes`, OFL licence). Colours: navy `#1F2430`, orange `#F2542D`,
  dark orange `#C63F1B`, cream `#F7F1E8`, grey text `#6F7585`.
- Sizes: XS `#7E3FF2` dotted, S `#1E88E5` dashed, M `#16A34A` dash-dot,
  L `#E08A00` long dash, XL `#E11D48` solid. Always in that order.
- Header: navy band with an orange block on the left, small upper-case pre-title + title.
  Footer: "<Garment> de hombre · Patrón y manual · XS–XL" and "n / total".
- Numbers in Spanish format (comma): use `fmt()`.
- Poppins does NOT have "→": write "a" ("escala 1:5 a 1:1").
- Seam allowances: 1.5 cm general; 1 cm on necklines and narrow bands; 2.5 cm on hems.
  Knit fabrics: narrow zigzag (width 1–1.5, length 2.5–3), ballpoint needle.
- Clear instructions: every action with its measurement in cm, bold on the key thing, "derecho con derecho"
  (right sides together), "con retroceso" (with backstitch), where to press the seam allowances.
