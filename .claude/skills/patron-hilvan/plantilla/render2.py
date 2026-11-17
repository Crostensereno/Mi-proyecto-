"""Patrones A4, A0 y proyector pensados para principiantes:
cada talla en su color y en sus propias páginas, una sola línea gruesa para recortar."""
import os
from shapely.geometry import LineString, Polygon
from geo import SIZES, body, sleeve, E, SLEEVE_CUFF

OUT = os.path.join(os.path.dirname(__file__), 'build')
os.makedirs(OUT, exist_ok=True)

REF = 'H-031'
CW, CH = 83.1, 114.0
TW, TH = 27.7, 19.0
COLS, ROWS = 3, 6
FRONT_O = (2.0, 2.6)
BACK_O = (40.5, 2.6)
SLEEVE_O = (27.0, 86.5)
TIRA_O = (76.4, 4.0)
TIRA = {'XS': 39, 'S': 41, 'M': 42, 'L': 43, 'XL': 44}
COL = {'XS': '#7c3aed', 'S': '#2563eb', 'M': '#16a34a', 'L': '#ea7a0c', 'XL': '#e11d48'}
COL_DARK = {'XS': '#b794f6', 'S': '#6ea8ff', 'M': '#4ade80', 'L': '#fdba5c', 'XL': '#fb7190'}
DASH = {'XS': '0.06 0.22', 'S': '0.55 0.3', 'M': '1.1 0.3 0.12 0.3', 'L': '1.7 0.45', 'XL': ''}
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..700&family=Inter:wght@400;500;600;700&display=swap">'

SCISSORS = ('<symbol id="sc" viewBox="-1.1 -1.1 2.2 2.2" overflow="visible"><g fill="none" stroke="currentColor" stroke-width=".13" stroke-linecap="round">'
            '<circle cx="-.62" cy="-.42" r=".3"/><circle cx="-.62" cy=".42" r=".3"/>'
            '<path d="M-.36 -.27 L.95 .22 M-.36 .27 L.95 -.22"/></g></symbol>')


def path(pts, close=True):
    d = 'M' + ' L'.join(f'{x:.3f} {y:.3f}' for x, y in pts)
    return d + (' Z' if close else '')


def T(x, y, s, size=.55, weight=400, anchor='start', fam='Inter', fill='var(--ink)', extra=''):
    stretch = ' font-stretch="125%"' if fam == 'Archivo' else ''
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{fam}, Arial, sans-serif"{stretch} font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>')


def badge(x, y, s, color, size=.9):
    label = f'TALLA {s}'
    w = size * (.6 * len(label) + 1.4)
    h = size * 1.55
    return (f'<rect x="{x}" y="{y}" width="{w:.2f}" height="{h:.2f}" rx="{h/2:.2f}" fill="{color}"/>'
            + T(x + w / 2, y + h * .7, label, size * .78, 700, 'middle', fill='#fff', extra='letter-spacing=".04"'))


def scissors_on(seg, poly, color, frac=.5, off=1.15, size=1.6):
    ln = LineString(seg)
    if ln.length < 4:
        return ''
    p = ln.interpolate(frac, normalized=True)
    q = ln.interpolate(min(ln.length, ln.project(p) + .3))
    r = ln.interpolate(max(0, ln.project(p) - .3))
    dx, dy = q.x - r.x, q.y - r.y
    d = (dx * dx + dy * dy) ** .5 or 1
    nx, ny = -dy / d, dx / d
    if poly.contains(LineString([(p.x, p.y), (p.x + nx * off, p.y + ny * off)]).interpolate(1)):
        nx, ny = -nx, -ny
    cx, cy = p.x + nx * off, p.y + ny * off
    import math
    ang = math.degrees(math.atan2(dy, dx))
    return (f'<use href="#sc" x="{cx-size/2:.2f}" y="{cy-size/2:.2f}" width="{size}" height="{size}" '
            f'style="color:{color}" transform="rotate({ang:.1f} {cx:.2f} {cy:.2f})"/>')


def grain(x, y1, y2, lw, label='HILO · paralela al doblez'):
    h = .5
    return (f'<g stroke="var(--ink)" stroke-width="{lw}" fill="none" stroke-linecap="round">'
            f'<path d="M{x} {y1} L{x} {y2}"/><path d="M{x-h/1.5} {y1+h} L{x} {y1} L{x+h/1.5} {y1+h}"/>'
            f'<path d="M{x-h/1.5} {y2-h} L{x} {y2} L{x+h/1.5} {y2-h}"/></g>'
            + T(x - .4, (y1 + y2) / 2, label, .5, 600, 'middle', extra=f'transform="rotate(-90 {x-.4} {(y1+y2)/2})" letter-spacing=".06"'))


# ---------------- Piezas de una talla ----------------
def body_piece(size, back, lw, colors):
    c = colors[size]
    ox, oy = BACK_O if back else FRONT_O
    d = body(size, back)
    cut, segs = d['cut'], d['segs']
    poly = Polygon(cut)
    g = [f'<g transform="translate({ox} {oy})">',
         f'<path d="{path(cut)}" fill="{c}" fill-opacity=".09"/>',
         f'<path d="{path(d["seam"], close=False)}" fill="none" stroke="var(--grey)" stroke-width="{lw*.6}" stroke-dasharray=".3 .25"/>']
    for k in ['neck', 'shoulder', 'armhole', 'side', 'hem']:
        g.append(f'<path d="{path(segs[k], False)}" fill="none" stroke="{c}" stroke-width="{lw*3.4}" stroke-linejoin="round" stroke-linecap="round"/>')
    fold = segs['fold']
    g.append(f'<path d="{path(fold, False)}" stroke="var(--ink)" stroke-width="{lw*3.4}"/>')
    for k, f in [('hem', .5), ('side', .55), ('shoulder', .5), ('armhole', .55), ('neck', .5)]:
        g.append(scissors_on(segs[k], poly, c, f))
    # Doblez
    y0, y1 = fold[-1][1], fold[0][1]
    ym = (y0 + y1) / 2
    g.append(f'<g stroke="var(--ink)" stroke-width="{lw}" fill="none"><path d="M.2 {ym-14} L2.4 {ym-14} L2.4 {ym+14} L.2 {ym+14}"/>'
             f'<path d="M.8 {ym-14.45} L.2 {ym-14} L.8 {ym-13.55}"/><path d="M.8 {ym+13.55} L.2 {ym+14} L.8 {ym+14.45}"/></g>')
    g.append(T(3.1, ym, 'DOBLEZ DE LA TELA · NO CORTAR ESTE BORDE', .55, 700, 'middle', extra=f'transform="rotate(-90 3.1 {ym})" letter-spacing=".08"'))
    g.append(grain(16.5, 34, 66, lw))
    name = 'ESPALDA' if back else 'DELANTERO'
    x, y = 5, 18 if not back else 14
    g.append(T(x, y, name, 1.7, 700, fam='Archivo', extra='letter-spacing=".06"'))
    g.append(badge(x, y + .9, size, c, 1.0))
    lines = ['Corta 1 pieza', 'Pon el borde negro', 'en el doblez de la tela', '', 'Recorta por la línea', 'gruesa de color',
             '', 'Puntos grises = costura', '(el margen ya está incluido)', '', f'Camiseta básica · Ref. {REF}']
    for i, t in enumerate(lines):
        if t:
            g.append(T(x, y + 3.9 + i * .78, t, .55, 700 if i in (0, 4, 5) else 400))
    g.append('</g>')
    return '\n'.join(g)


def sleeve_piece(size, lw, colors):
    c = colors[size]
    ox, oy = SLEEVE_O
    d = sleeve(size)
    cut, segs = d['cut'], d['segs']
    poly = Polygon(cut)
    g = [f'<g transform="translate({ox} {oy})">',
         f'<path d="{path(cut)}" fill="{c}" fill-opacity=".09"/>',
         f'<path d="{path(d["seam"])}" fill="none" stroke="var(--grey)" stroke-width="{lw*.6}" stroke-dasharray=".3 .25"/>',
         f'<path d="{path(cut)}" fill="none" stroke="{c}" stroke-width="{lw*3.4}" stroke-linejoin="round"/>']
    for k, f in [('cap', .25), ('cap', .75), ('cuff', .5), ('right', .5), ('left', .5)]:
        g.append(scissors_on(segs[k], poly, c, f))
    g.append(f'<path d="M0 -1.5 L0 .2" stroke="var(--ink)" stroke-width="{lw*3}"/>')
    g.append(T(.6, .5, 'piquete: se une con el hombro', .5, 600))
    g.append(f'<path d="M0 1.6 L0 {d["cuffy"]-1}" stroke="var(--ink)" stroke-width="{lw*.7}" stroke-dasharray=".35 .3"/>')
    g.append(grain(-7, 7, 19, lw, 'HILO'))
    x, y = 1.4, 5.6
    g.append(T(x, y, 'MANGA', 1.7, 700, fam='Archivo', extra='letter-spacing=".06"'))
    g.append(badge(x, y + .9, size, c, 1.0))
    for i, t in enumerate(['Corta 2 piezas: dobla la tela', 'y corta las dos capas a la vez', 'Recorta por la línea gruesa de color']):
        g.append(T(x, y + 3.9 + i * .78, t, .55, 700 if i == 2 else 400))
    g.append('</g>')
    return '\n'.join(g)


def tira_piece(size, lw, colors):
    c = colors[size]
    x, y = TIRA_O
    L = TIRA[size]
    g = [f'<rect x="{x}" y="{y}" width="6" height="{L}" fill="{c}" fill-opacity=".09" stroke="{c}" stroke-width="{lw*3.4}"/>',
         f'<path d="M{x+3} {y+.4} L{x+3} {y+L-.4}" stroke="var(--grey)" stroke-width="{lw*.6}" stroke-dasharray=".3 .25"/>',
         f'<use href="#sc" x="{x-1.5:.2f}" y="{y+L/2-.6:.2f}" width="1.2" height="1.2" style="color:{c}" transform="rotate(90 {x-.9:.2f} {y+L/2:.2f})"/>']
    cx = x + 1.45
    g.append(T(cx, y + L / 2, f'TIRA DEL CUELLO · TALLA {size} · corta 1', .55, 700, 'middle', extra=f'transform="rotate(-90 {cx} {y+L/2})"'))
    cx2 = x + 4.6
    g.append(T(cx2, y + L / 2, f'{L} × 6 cm · el largo en el sentido que más estira', .45, 400, 'middle', extra=f'transform="rotate(-90 {cx2} {y+L/2})"'))
    return '\n'.join(g)


def legend_block(size, lw, colors, title=None):
    x, y = 55.5, 86.0
    c = colors[size] if size else 'var(--ink)'
    g = [f'<g transform="translate({x} {y})">']
    g.append(T(0, 1.4, 'HILVÁN', 1.4, 600, fam='Archivo', extra='letter-spacing=".45"'))
    g.append(T(0, 2.8, f'Camiseta básica de hombre · Ref. {REF}', .6, 700))
    if size:
        g.append(badge(0, 3.6, size, c, 1.15))
        g.append(T(8.2, 4.95, 'Escala real 1:1 · margen incluido', .5))
    else:
        g.append(T(0, 4.6, title or '', .7, 700))
    g.append(f'<path d="M0 6.4 L25.5 6.4" stroke="var(--line)" stroke-width="{lw}"/>')
    g.append(T(0, 7.6, 'CÓMO SE USA', .45, 700, extra='letter-spacing=".12"'))
    rows = []
    if size:
        rows = [(f'<path d="M0 0 L3.4 0" stroke="{c}" stroke-width="{lw*3.4}" stroke-linecap="round"/>', 'Línea de color: recorta por aquí'),
                (f'<use href="#sc" x=".9" y="-.8" width="1.6" height="1.6" style="color:{c}"/>', 'Tijeras: lado por el que se corta'),
                (f'<path d="M0 0 L3.4 0" stroke="var(--ink)" stroke-width="{lw*3.4}"/>', 'Borde negro: va en el doblez, no cortar'),
                (f'<path d="M0 0 L3.4 0" stroke="var(--grey)" stroke-width="{lw*.8}" stroke-dasharray=".3 .25"/>', 'Puntos grises: por donde se cose')]
    else:
        for i, s in enumerate(SIZES):
            da = f' stroke-dasharray="{DASH[s]}"' if DASH[s] else ''
            rows.append((f'<path d="M0 0 L3.4 0" stroke="{colors[s]}" stroke-width="{lw*2}"{da}/>', f'Talla {s}'))
    for i, (sym, txt) in enumerate(rows):
        yy = 8.7 + i * 1.0
        g.append(f'<g transform="translate(0 {yy-.18})">{sym}</g>')
        g.append(T(4.2, yy, txt, .5, 600 if i == 0 else 400))
    sx, sy = 0, 13.6
    g.append(f'<rect x="{sx}" y="{sy}" width="5" height="5" fill="none" stroke="var(--ink)" stroke-width="{lw*1.4}"/>')
    g.append(T(sx + 2.5, sy + 2.75, '5 × 5 cm', .5, 700, 'middle'))
    for i, t in enumerate(['Cuadrado de prueba', 'Mídelo con una regla antes de', 'cortar. Si no mide 5 cm, imprime', 'otra vez al 100 % (tamaño real).']):
        g.append(T(sx + 5.8, sy + .9 + i * .78, t, .5, 700 if i == 0 else 400))
    ry = 20.6
    g.append(f'<path d="M0 {ry} L10 {ry}" stroke="var(--ink)" stroke-width="{lw*1.2}"/>')
    for k in range(11):
        h = .6 if k % 5 == 0 else .3
        g.append(f'<path d="M{k} {ry} L{k} {ry+h}" stroke="var(--ink)" stroke-width="{lw*.8}"/>')
        if k % 5 == 0:
            g.append(T(k, ry + 1.25, f'{k} cm' if k == 10 else str(k), .42, 400, 'middle'))
    g.append(T(12, ry + .4, 'Piezas: delantero (1), espalda (1),', .45))
    g.append(T(12, ry + 1.15, 'manga (2) y tira del cuello (1)', .45))
    g.append('</g>')
    return '\n'.join(g)


def grid_lines(lw):
    gl = [f'<path d="M{x} 0 L{x} {CH}"/>' for x in range(0, int(CW) + 1, 10)]
    gl += [f'<path d="M0 {y} L{CW} {y}"/>' for y in range(0, int(CH) + 1, 10)]
    out = [f'<g stroke="var(--gridc)" stroke-width="{lw*.7}">' + ''.join(gl) + '</g>']
    out += [T(x + .2, .7, f'{x}', .45, 400, extra='fill-opacity=".6"') for x in range(10, int(CW), 10)]
    out += [T(.2, y - .25, f'{y}', .45, 400, extra='fill-opacity=".6"') for y in range(10, int(CH), 10)]
    return ''.join(out)


def canvas_size(size, lw=.045, grid=False, colors=COL):
    parts = [f'<defs>{SCISSORS}</defs>']
    if grid:
        parts.append(grid_lines(lw))
    parts += [body_piece(size, False, lw, colors), body_piece(size, True, lw, colors), sleeve_piece(size, lw, colors),
              tira_piece(size, lw, colors), legend_block(size, lw, colors)]
    return '\n'.join(parts)


def canvas_all(lw=.045, grid=False, colors=COL):
    """Todas las tallas juntas, cada una en su color (para calcar)."""
    parts = [f'<defs>{SCISSORS}</defs>']
    if grid:
        parts.append(grid_lines(lw))
    for (o, back) in [(FRONT_O, False), (BACK_O, True)]:
        g = [f'<g transform="translate({o[0]} {o[1]})">']
        for s in SIZES[::-1]:
            d = body(s, back)
            da = f' stroke-dasharray="{DASH[s]}"' if DASH[s] else ''
            g.append(f'<path d="{path(d["cut"])}" fill="none" stroke="{colors[s]}" stroke-width="{lw*1.8}"{da}/>')
            g.append(T(E[s][0] + .9, E[s][1] + 1.6, s, .65, 700, 'start', fill=colors[s]))
        g.append(f'<path d="M0 {1 if back else 7} L0 78.5" stroke="var(--ink)" stroke-width="{lw*3.4}"/>')
        g.append(T(5, 18 if not back else 14, 'ESPALDA' if back else 'DELANTERO', 1.7, 700, fam='Archivo'))
        g.append(T(5, (18 if not back else 14) + 1.4, 'Todas las tallas · corta 1 al doblez', .6, 600))
        g.append(grain(16.5, 34, 66, lw))
        g.append('</g>')
        parts.append(''.join(g))
    g = [f'<g transform="translate({SLEEVE_O[0]} {SLEEVE_O[1]})">']
    for s in SIZES[::-1]:
        da = f' stroke-dasharray="{DASH[s]}"' if DASH[s] else ''
        g.append(f'<path d="{path(sleeve(s)["cut"])}" fill="none" stroke="{colors[s]}" stroke-width="{lw*1.8}"{da}/>')
        cx, cy = SLEEVE_CUFF[s]
        g.append(T(cx + 1.2, cy + 1.6, s, .65, 700, fill=colors[s]))
    g.append(f'<path d="M0 -1.5 L0 .2" stroke="var(--ink)" stroke-width="{lw*3}"/>')
    g.append(T(1.4, 5.6, 'MANGA', 1.7, 700, fam='Archivo'))
    g.append(T(1.4, 7.0, 'Todas las tallas · corta 2', .6, 600))
    g.append(grain(-7, 7, 19, lw, 'HILO'))
    g.append('</g>')
    parts.append(''.join(g))
    x, y = TIRA_O
    for s in SIZES[::-1]:
        da = f' stroke-dasharray="{DASH[s]}"' if DASH[s] else ''
        parts.append(f'<rect x="{x}" y="{y}" width="6" height="{TIRA[s]}" fill="none" stroke="{colors[s]}" stroke-width="{lw*1.8}"{da}/>')
    parts.append(T(x + 3, y + 20, 'TIRA DEL CUELLO', .55, 700, 'middle', extra=f'transform="rotate(-90 {x+3} {y+20})"'))
    parts.append(legend_block(None, lw, colors, 'Todas las tallas juntas (para calcar)'))
    return '\n'.join(parts)


CSS = """
:root{--ink:#111;--grey:#8a8a88;--line:#cfcfcd;--gridc:#d7d7d4;--bg:#fff}
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:var(--bg)}
body{font-family:Inter,Arial,sans-serif;color:var(--ink);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{position:relative;overflow:hidden;page-break-after:always;break-after:page;background:var(--bg)}
.page:last-child{page-break-after:auto;break-after:auto}
svg{display:block}
.dark{--ink:#f4f4f2;--grey:#9a9a98;--line:#555;--gridc:#3a3a3a;--bg:#000;background:#000}
"""


def html(pages, w, h, extra_css=''):
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8">{FONTS}<style>@page{{size:{w} {h};margin:0}}'
            f'{CSS}.page{{width:{w};height:{h}}}{extra_css}</style></head><body>' + ''.join(pages) + '</body></html>')


def tile_id(c, r):
    return f'{"ABC"[c]}{r+1}'


TILES = [(c, r) for c in range(COLS) for r in range(ROWS)]  # por columnas: A1…A6, B1…B6, C1…C6


def a4_page_ranges():
    start = 2
    rng = {}
    for s in SIZES:
        rng[s] = (start, start + len(TILES) - 1)
        start += len(TILES)
    return rng


def a4():
    rng = a4_page_ranges()
    total = 1 + len(SIZES) * len(TILES)
    pages = []
    scale = 15.5 / CH
    grid = ''.join(f'<rect x="{c*TW}" y="{r*TH}" width="{TW}" height="{TH}" fill="none" stroke="#111" stroke-width=".25"/>'
                   f'<text x="{c*TW+TW/2}" y="{r*TH+TH/2+1.6}" font-family="Inter" font-size="4.2" font-weight="700" text-anchor="middle" fill="#111" fill-opacity=".45">{tile_id(c,r)}</text>'
                   f'<text x="{c*TW+TW/2}" y="{r*TH+TH/2+5.4}" font-family="Inter" font-size="2.2" font-weight="600" text-anchor="middle" fill="#111" fill-opacity=".5">hoja {k+1}</text>'
                   for k, (c, r) in enumerate(TILES))
    mapsvg = f'<svg width="{CW*scale}cm" height="{CH*scale}cm" viewBox="0 0 {CW} {CH}">{canvas_size("M", lw=.16)}{grid}</svg>'
    size_rows = ''.join(f'<tr><td><span class="sz" style="background:{COL[s]}">{s}</span></td><td><b>páginas {a}–{b}</b></td></tr>' for s, (a, b) in rng.items())
    pages.append(f'''<section class="page"><div class="intro">
      <div>
        <div class="logo">HILVÁN</div>
        <div class="eyebrow">Patrón A4 · imprimir en casa</div>
        <h1>Camiseta básica de hombre</h1>
        <p class="ref">Ref. {REF} · escala real 1:1 · margen de costura incluido</p>
        <h3>1 · Imprime solo tu talla</h3>
        <table class="pr">{size_rows}</table>
        <p class="small">En la ventana de imprimir, elige “Páginas” y escribe el rango de tu talla. Imprime al <b>100 %</b> (“tamaño real”), sin “ajustar a página”.</p>
        <h3>2 · Comprueba la escala</h3>
        <div class="test"><svg width="5.2cm" height="5.2cm" viewBox="-.1 -.1 5.2 5.2"><rect x="0" y="0" width="5" height="5" fill="none" stroke="#111" stroke-width=".05"/><text x="2.5" y="2.7" font-family="Inter" font-size=".5" font-weight="700" text-anchor="middle">5 × 5 cm</text></svg>
        <p class="small">Mide este cuadrado con una regla. Si mide 5 cm, todo está bien.</p></div>
      </div>
      <div>
        <h3>3 · Une las hojas como un puzle</h3>
        <ol>
          <li>Las hojas salen <b>por columnas</b>: primero <b>A1 a A6</b> (columna de la izquierda, de arriba abajo), después <b>B1 a B6</b> y por último <b>C1 a C6</b>. Ve pegando cada hoja debajo de la anterior.</li>
          <li>Recorta el margen blanco del lado <b>derecho</b> y de <b>abajo</b> de cada hoja.</li>
          <li>Junta las hojas a tope: los <b>medios rombos negros</b> de los bordes se unen y forman un rombo completo. Pega con celo.</li>
          <li>Recorta cada pieza <b>por la línea gruesa de color</b>. El borde negro no se corta: va en el doblez de la tela.</li>
        </ol>
        <div class="map">{mapsvg}</div>
      </div>
    </div></section>''')
    n = 1
    for s in SIZES:
        body_svg = canvas_size(s)
        for k, (c, r) in enumerate(TILES):
            n += 1
            tid = tile_id(c, r)
            x0, y0 = c * TW, r * TH
            d = .9
            marks = []
            if c < COLS - 1: marks.append(f'<path d="M{TW} {TH/2-d} L{TW-d} {TH/2} L{TW} {TH/2+d} Z"/>')
            if c > 0: marks.append(f'<path d="M0 {TH/2-d} L{d} {TH/2} L0 {TH/2+d} Z"/>')
            if r < ROWS - 1: marks.append(f'<path d="M{TW/2-d} {TH} L{TW/2} {TH-d} L{TW/2+d} {TH} Z"/>')
            if r > 0: marks.append(f'<path d="M{TW/2-d} 0 L{TW/2} {d} L{TW/2+d} 0 Z"/>')
            right = f'une con {tile_id(c+1, r)} →' if c < COLS - 1 else ''
            below = f'↓ une con {tile_id(c, r+1)}' if r < ROWS - 1 else ''
            pages.append(f'''<section class="page tile">
              <div class="hdr"><span class="sz big" style="background:{COL[s]}">TALLA {s}</span><span class="tid">{tid}</span><span>hoja {k+1} de 18 de tu talla · página {n} de {total} · Camiseta básica · {REF} · imprime al 100 %</span><span class="sp"></span><span>HILVÁN</span></div>
              <div class="win"><svg width="{TW}cm" height="{TH}cm" viewBox="{x0} {y0} {TW} {TH}">
                <text x="{x0+TW/2}" y="{y0+TH/2+2.2}" font-family="Inter" font-size="6" font-weight="700" text-anchor="middle" fill="{COL[s]}" fill-opacity=".08">{tid}</text>
                {body_svg}</svg>
                <svg class="ov" width="{TW}cm" height="{TH}cm" viewBox="0 0 {TW} {TH}"><rect x="0" y="0" width="{TW}" height="{TH}" fill="none" stroke="#111" stroke-width=".02"/><g fill="#111">{''.join(marks)}</g></svg>
              </div>
              <div class="side r">{right}</div><div class="side b">{below}</div>
            </section>''')
    css = """
    .intro{display:grid;grid-template-columns:1fr 1fr;gap:1.1cm;padding:1cm 1.3cm;height:100%}
    .logo{font-family:Archivo;font-stretch:125%;font-weight:600;letter-spacing:.32em;font-size:12pt}
    .eyebrow{font-size:7pt;letter-spacing:.14em;text-transform:uppercase;color:#666;margin-top:.35cm}
    h1{font-family:Archivo;font-stretch:112%;font-weight:400;font-size:20pt;line-height:1.05;margin-top:.1cm}
    h3{font-family:Archivo;font-stretch:110%;font-weight:600;font-size:10.5pt;margin:.4cm 0 .15cm}
    .ref{font-size:8pt;color:#666;margin-top:.1cm}
    .pr{border-collapse:collapse;font-size:9pt}
    .pr td{padding:.05cm .3cm .05cm 0}
    .sz{display:inline-block;min-width:1cm;padding:.05cm .2cm;border-radius:99px;color:#fff;font-size:7.5pt;font-weight:700;text-align:center}
    .small{font-size:8pt;color:#444;line-height:1.4;margin-top:.12cm;max-width:12cm}
    ol{margin-left:.45cm;font-size:8.4pt;line-height:1.4;display:grid;gap:.1cm}
    .test{display:flex;gap:.4cm;align-items:center}
    .test svg{flex:none}
    .map{margin-top:.25cm}
    .tile .hdr{position:absolute;left:1cm;right:1cm;top:.22cm;display:flex;gap:.35cm;align-items:center;font-size:7pt;color:#444}
    .tile .hdr .sp{flex:1}
    .sz.big{font-size:9pt;padding:.06cm .3cm}
    .tid{font-size:11pt;font-weight:700;color:#111}
    .tile .win{position:absolute;left:1cm;top:1cm;width:27.7cm;height:19cm}
    .tile .win svg{position:absolute;left:0;top:0}
    .tile .side{position:absolute;font-size:7.5pt;font-weight:600;color:#444}
    .side.r{right:.12cm;top:8.8cm;writing-mode:vertical-rl}
    .side.b{left:13.6cm;bottom:.22cm}
    """
    return html(pages, '297mm', '210mm', css)


def a0():
    ox, oy = (84.1 - CW) / 2, (118.9 - CH) / 2
    pages = []
    for s in SIZES:
        pages.append(f'''<section class="page"><div class="hd"><span class="sz" style="background:{COL[s]}">TALLA {s}</span> HILVÁN · Camiseta básica · {REF} · Patrón A0 · imprime solo la página de tu talla, al 100 % (tamaño real)</div>
          <svg style="position:absolute;left:{ox}cm;top:{oy}cm" width="{CW}cm" height="{CH}cm" viewBox="0 0 {CW} {CH}">{canvas_size(s)}</svg>
          <div class="ft">Página {SIZES.index(s)+1}: talla {s} · comprueba el cuadrado de prueba (abajo a la derecha): debe medir 5 × 5 cm</div></section>''')
    pages.append(f'''<section class="page"><div class="hd">HILVÁN · Camiseta básica · {REF} · Página 6: todas las tallas juntas, para calcar en papel</div>
      <svg style="position:absolute;left:{ox}cm;top:{oy}cm" width="{CW}cm" height="{CH}cm" viewBox="0 0 {CW} {CH}">{canvas_all()}</svg>
      <div class="ft">Calca tu talla en papel de seda o de patronaje y recórtala. Así conservas todas las tallas.</div></section>''')
    css = ('.hd,.ft{position:absolute;left:2cm;font-size:13pt;color:#333;display:flex;gap:.4cm;align-items:center}.hd{top:.6cm}.ft{bottom:.7cm}'
           '.sz{display:inline-block;padding:.08cm .35cm;border-radius:99px;color:#fff;font-weight:700}')
    return html(pages, '841mm', '1189mm', css)


def projector():
    pages = []
    for s in SIZES:
        pages.append(f'<section class="page"><svg width="{CW}cm" height="{CH}cm" viewBox="0 0 {CW} {CH}">{canvas_size(s, lw=.085, grid=True)}</svg></section>')
    for s in SIZES:
        pages.append(f'<section class="page dark"><svg width="{CW}cm" height="{CH}cm" viewBox="0 0 {CW} {CH}">{canvas_size(s, lw=.085, grid=True, colors=COL_DARK)}</svg></section>')
    pages.append(f'<section class="page"><svg width="{CW}cm" height="{CH}cm" viewBox="0 0 {CW} {CH}">{canvas_all(lw=.085, grid=True)}</svg></section>')
    return html(pages, f'{CW}cm', f'{CH}cm')


if __name__ == '__main__':
    for name, fn in [('a4', a4), ('a0', a0), ('proyector', projector)]:
        with open(os.path.join(OUT, f'{name}.html'), 'w') as f:
            f.write(fn())
    print('ok')
