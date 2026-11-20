"""Plancha de la bermuda H-032 con el formato Hilván (reutiliza la maquetación de render2)."""
import os
from shapely.geometry import LineString, Polygon
import render2 as R
from render2 import T, badge, scissors_on, path, SCISSORS, COL, COL_DARK, DASH, grid_lines, CW, CH
from geo_b import SIZES, piece, pocket, measures, POCKET_OPEN, front_seam, back_seam

R.REF = 'H-032'
REF = R.REF
NAME = 'Bermuda de hombre'
LEG = {False: {'ox': 1.5, 'oy': 1.0, 'x1': 42.4}, True: {'ox': 1.5, 'oy': 47.0, 'x1': 50.2}}
Y0 = -3.6
POCKET_O = (66.4, 3.0)
BAND_O = (2.0, 101.5)


def tr(pts, back):
    c = LEG[back]
    return [(c['ox'] + (y - Y0), c['oy'] + (c['x1'] - x)) for x, y in pts]


def tp(x, y, back):
    return tr([(x, y)], back)[0]


def side_x_at(seg, y):
    ln = LineString(seg)
    hit = ln.intersection(LineString([(-100, y), (200, y)]))
    return hit.x if hit.geom_type == 'Point' else list(hit.geoms)[0].x


def leg_piece(s, back, lw, colors, solo=True):
    c = colors[s]
    d = piece(s, back)
    cut = tr(d['cut'], back)
    poly = Polygon(cut)
    g = []
    if solo:
        g.append(f'<path d="{path(cut)}" fill="{c}" fill-opacity=".09"/>')
        g.append(f'<path d="{path(tr(d["seam"], back))}" fill="none" stroke="var(--grey)" stroke-width="{lw*.6}" stroke-dasharray=".3 .25"/>')
        g.append(f'<path d="{path(cut)}" fill="none" stroke="{c}" stroke-width="{lw*3.4}" stroke-linejoin="round"/>')
        for k, f in [('top', .5), ('side', .7), ('hem', .5), ('inseam', .5), ('crotch', .35)]:
            g.append(scissors_on(tr(d['segs'][k], back), poly, c, f))
    else:
        da = f' stroke-dasharray="{DASH[s]}"' if DASH[s] else ''
        g.append(f'<path d="{path(cut)}" fill="none" stroke="{c}" stroke-width="{lw*1.8}"{da}/>')
    # Piquetes del bolsillo (boca) y de casar delantero/trasero
    side = d['segs']['side']
    ticks = [POCKET_OPEN[0], POCKET_OPEN[1]] + ([30 - .45, 30 + .45] if back else [30])
    for y in ticks:
        x = side_x_at(side, y)
        a, b = tp(x, y, back), tp(x - 1.1, y, back)
        g.append(f'<path d="M{a[0]:.2f} {a[1]:.2f} L{b[0]:.2f} {b[1]:.2f}" stroke="var(--ink)" stroke-width="{lw*2.6}"/>')
    if solo:
        a = tp(side_x_at(side, (POCKET_OPEN[0] + POCKET_OPEN[1]) / 2) - 1.8, (POCKET_OPEN[0] + POCKET_OPEN[1]) / 2, back)
        g.append(T(a[0], a[1] + .2, 'boca del bolsillo', .45, 600, 'middle'))
        e = d['edges']
        xi, xo = e['hem'][1][0], e['hem'][0][0]
        L = e['hem'][0][1]
        xc = (xi + xo) / 2
        p0, p1 = tp(xc, 27, back), tp(xc, L - 7, back)
        h = .5
        g.append(f'<g stroke="var(--ink)" stroke-width="{lw}" fill="none" stroke-linecap="round"><path d="M{p0[0]} {p0[1]} L{p1[0]} {p1[1]}"/>'
                 f'<path d="M{p0[0]+h} {p0[1]-h/1.5} L{p0[0]} {p0[1]} L{p0[0]+h} {p0[1]+h/1.5}"/><path d="M{p1[0]-h} {p1[1]-h/1.5} L{p1[0]} {p1[1]} L{p1[0]-h} {p1[1]+h/1.5}"/></g>')
        g.append(T((p0[0] + p1[0]) / 2, p0[1] - .45, 'HILO · paralela al orillo de la tela', .5, 600, 'middle', extra='letter-spacing=".06"'))
        fe = e['top'][0][0] if not back else e['top'][0][0]
        W = e['side'][0][0]
        lab = tp((fe + W) / 2, 6.5, back)
        x, y = lab[0], lab[1] - 6.2
        g.append(T(x, y, 'TRASERO' if back else 'DELANTERO', 1.7, 700, fam='Archivo', extra='letter-spacing=".06"'))
        g.append(badge(x, y + .9, s, c, 1.0))
        lines = ['Corta 2 piezas: dobla la tela', 'y corta las dos capas a la vez', 'Recorta por la línea gruesa de color', '',
                 'Rayitas del costado: boca del bolsillo', ('Dos rayitas: trasero' if back else 'Una rayita: delantero') + ' (casan al coser)',
                 'Puntos grises = costura (margen incluido)', f'{NAME} · Ref. {REF}']
        for i, t in enumerate(lines):
            if t:
                g.append(T(x, y + 3.9 + i * .78, t, .55, 700 if i == 2 else 400))
        # Indicación de dónde va la cintura y el bajo
        top_mid = tp((fe + W) / 2, -.2, back)
        g.append(T(top_mid[0] + .9, top_mid[1] + 6, 'CINTURA', .5, 700, 'middle', extra=f'transform="rotate(-90 {top_mid[0]+.9} {top_mid[1]+6})" letter-spacing=".1"'))
        hm = tp(xc, L - 1.4, back)
        g.append(T(hm[0], hm[1], 'BAJO · dobla 1 cm y luego 2,5 cm', .45, 700, 'middle', extra=f'transform="rotate(-90 {hm[0]} {hm[1]})"'))
    return '\n'.join(g)


def pocket_piece(s, lw, colors, solo=True):
    c = colors[s]
    d = pocket()
    ox, oy = POCKET_O
    g = [f'<g transform="translate({ox} {oy})">']
    if solo:
        poly = Polygon(d['cut'])
        g.append(f'<path d="{path(d["cut"])}" fill="{c}" fill-opacity=".09"/>')
        g.append(f'<path d="{path(d["seam"])}" fill="none" stroke="var(--grey)" stroke-width="{lw*.6}" stroke-dasharray=".3 .25"/>')
        g.append(f'<path d="{path(d["cut"])}" fill="none" stroke="{c}" stroke-width="{lw*3.4}" stroke-linejoin="round"/>')
        for f in (.3, .7):
            g.append(scissors_on(d['segs']['curve'], poly, c, f))
        g.append(scissors_on(d['segs']['straight'], poly, c, .5))
    else:
        g.append(f'<path d="{path(d["cut"])}" fill="none" stroke="var(--ink)" stroke-width="{lw*1.8}"/>')
    for y in POCKET_OPEN:
        g.append(f'<path d="M-1.5 {y} L-.4 {y}" stroke="var(--ink)" stroke-width="{lw*2.6}"/>')
    g.append(f'<g stroke="var(--ink)" stroke-width="{lw}" fill="none" stroke-linecap="round"><path d="M12 6 L12 21"/><path d="M11.65 6.5 L12 6 L12.35 6.5"/><path d="M11.65 20.5 L12 21 L12.35 20.5"/></g>')
    if solo:
        g.append(T(1.4, 4.4, 'BOLSILLO', 1.25, 700, fam='Archivo'))
        g.append(badge(1.4, 5.2, s, c, .8))
        for i, t in enumerate(['Corta 4 piezas', '(2 por cada lado)', 'Borde recto: va', 'en el costado', 'Rayitas = boca', 'del bolsillo']):
            g.append(T(1.4, 8.6 + i * .72, t, .5, 700 if i == 0 else 400))
    else:
        g.append(T(1.4, 4.4, 'BOLSILLO', 1.25, 700, fam='Archivo'))
        g.append(T(1.4, 5.6, 'Talla única · corta 4', .5, 600))
    g.append('</g>')
    return '\n'.join(g)


def band_piece(s, lw, colors, solo=True):
    c = colors[s]
    m = measures(s)
    x, y = BAND_O
    L, Hh = m['band_cut_half'], m['band_cut_h']
    if not solo:
        da = f' stroke-dasharray="{DASH[s]}"' if DASH[s] else ''
        return f'<rect x="{x}" y="{y}" width="{L}" height="{Hh}" fill="none" stroke="{c}" stroke-width="{lw*1.8}"{da}/>'
    g = [f'<rect x="{x}" y="{y}" width="{L}" height="{Hh}" fill="{c}" fill-opacity=".09"/>',
         f'<path d="M{x} {y} L{x+L} {y} L{x+L} {y+Hh} L{x} {y+Hh}" fill="none" stroke="{c}" stroke-width="{lw*3.4}" stroke-linejoin="round"/>',
         f'<path d="M{x} {y} L{x} {y+Hh}" stroke="var(--ink)" stroke-width="{lw*3.4}"/>',
         f'<path d="M{x+.2} {y+1} L{x+L-1} {y+1} L{x+L-1} {y+Hh-1} L{x+.2} {y+Hh-1}" fill="none" stroke="var(--grey)" stroke-width="{lw*.6}" stroke-dasharray=".3 .25"/>',
         f'<path d="M{x+.2} {y+Hh/2} L{x+L-.2} {y+Hh/2}" stroke="var(--ink)" stroke-width="{lw*.8}" stroke-dasharray="1 .5"/>',
         f'<use href="#sc" x="{x+L/2-.8:.2f}" y="{y-1.9:.2f}" width="1.6" height="1.6" style="color:{c}"/>',
         f'<use href="#sc" x="{x+L+.3:.2f}" y="{y+Hh/2-.8:.2f}" width="1.6" height="1.6" style="color:{c}" transform="rotate(90 {x+L+1.1:.2f} {y+Hh/2:.2f})"/>']
    g.append(T(x + .9, y + Hh / 2, 'DOBLEZ · NO CORTAR', .42, 700, 'middle', extra=f'transform="rotate(-90 {x+.9} {y+Hh/2})"'))
    g.append(T(x + 2.4, y + 2.4, 'CINTURILLA', .9, 700, fam='Archivo'))
    g.append(badge(x + 11.5, y + 1.35, s, c, .7))
    g.append(T(x + 2.4, y + 3.6, f'Corta 2 piezas con el borde negro en el doblez de la tela · cada pieza abierta mide {2*L:.1f} × {Hh:.0f} cm'.replace('.', ','), .45))
    g.append(T(x + 2.4, y + Hh / 2 - .3, 'línea de doblado: se dobla a lo largo por aquí', .42, 600))
    return '\n'.join(g)


def elastic_note(s, lw, colors):
    m = measures(s)
    x, y = 41.5, 102.3
    g = [T(x, y, 'ELÁSTICO', .6, 700, extra='letter-spacing=".1"'),
         T(x, y + 1.1, f'3,5 cm de ancho · corta {m["elastic"]} cm', .55, 700, fill=colors[s]),
         T(x, y + 2.0, '(2 cm se solapan al cerrarlo)', .45),
         T(x, y + 3.4, 'Va dentro de la cinturilla.', .45),
         T(x, y + 4.2, 'Se mete al final con un imperdible.', .45)]
    return '\n'.join(g)


def legend(s, lw, colors, title=None):
    x, y = 65.0, 34.0
    c = colors[s] if s else 'var(--ink)'
    g = [f'<g transform="translate({x} {y})">',
         T(0, 1.3, 'HILVÁN', 1.3, 600, fam='Archivo', extra='letter-spacing=".4"'),
         T(0, 2.6, f'{NAME} · Ref. {REF}', .55, 700)]
    if s:
        g.append(badge(0, 3.4, s, c, 1.1))
        g.append(T(0, 6.4, 'Escala real 1:1 · margen incluido', .48))
    else:
        g.append(T(0, 4.3, title or '', .6, 700))
    g.append(f'<path d="M0 7.3 L17.5 7.3" stroke="var(--line)" stroke-width="{lw}"/>')
    g.append(T(0, 8.5, 'CÓMO SE USA', .45, 700, extra='letter-spacing=".12"'))
    if s:
        rows = [(f'<path d="M0 0 L3 0" stroke="{c}" stroke-width="{lw*3.4}" stroke-linecap="round"/>', 'Color: recorta por aquí'),
                (f'<use href="#sc" x=".8" y="-.8" width="1.6" height="1.6" style="color:{c}"/>', 'Tijeras: este lado se corta'),
                (f'<path d="M0 0 L3 0" stroke="var(--ink)" stroke-width="{lw*3.4}"/>', 'Negro: doblez, no cortar'),
                (f'<path d="M0 0 L3 0" stroke="var(--grey)" stroke-width="{lw*.8}" stroke-dasharray=".3 .25"/>', 'Puntos grises: costura'),
                (f'<path d="M1.5 -.55 L1.5 .55" stroke="var(--ink)" stroke-width="{lw*2.6}"/>', 'Rayita: marca para casar')]
    else:
        rows = []
        for z in SIZES:
            da = f' stroke-dasharray="{DASH[z]}"' if DASH[z] else ''
            rows.append((f'<path d="M0 0 L3 0" stroke="{colors[z]}" stroke-width="{lw*2}"{da}/>', f'Talla {z}'))
    for i, (sym, txt) in enumerate(rows):
        yy = 9.7 + i * 1.0
        g.append(f'<g transform="translate(0 {yy-.18})">{sym}</g>')
        g.append(T(3.8, yy, txt, .5))
    sy = 15.6
    g.append(f'<rect x="0" y="{sy}" width="5" height="5" fill="none" stroke="var(--ink)" stroke-width="{lw*1.4}"/>')
    g.append(T(2.5, sy + 2.75, '5 × 5 cm', .5, 700, 'middle'))
    for i, t in enumerate(['Cuadrado de prueba', 'Mídelo antes de cortar:', 'si no mide 5 cm, imprime', 'otra vez al 100 %.']):
        g.append(T(5.8, sy + .9 + i * .78, t, .48, 700 if i == 0 else 400))
    ry = 23.2
    g.append(f'<path d="M0 {ry} L10 {ry}" stroke="var(--ink)" stroke-width="{lw*1.2}"/>')
    for k in range(11):
        h = .6 if k % 5 == 0 else .3
        g.append(f'<path d="M{k} {ry} L{k} {ry+h}" stroke="var(--ink)" stroke-width="{lw*.8}"/>')
        if k % 5 == 0:
            g.append(T(k, ry + 1.25, f'{k} cm' if k == 10 else str(k), .42, 400, 'middle'))
    g.append(f'<path d="M0 26 L17.5 26" stroke="var(--line)" stroke-width="{lw}"/>')
    g.append(T(0, 27.2, 'PIEZAS', .45, 700, extra='letter-spacing=".12"'))
    for i, (a, b) in enumerate([('Delantero', 'corta 2'), ('Trasero', 'corta 2'), ('Bolsillo', 'corta 4'), ('Cinturilla', 'corta 2 al doblez'), ('Elástico', '3,5 cm de ancho')]):
        g.append(T(0, 28.4 + i * .85, a, .5, 700))
        g.append(T(6.5, 28.4 + i * .85, b, .5))
    g.append('</g>')
    return '\n'.join(g)


def canvas_size(s, lw=.045, grid=False, colors=COL):
    parts = [f'<defs>{SCISSORS}</defs>']
    if grid:
        parts.append(grid_lines(lw))
    parts += [leg_piece(s, False, lw, colors), leg_piece(s, True, lw, colors), pocket_piece(s, lw, colors),
              band_piece(s, lw, colors), elastic_note(s, lw, colors), legend(s, lw, colors)]
    return '\n'.join(parts)


def canvas_all(lw=.045, grid=False, colors=COL):
    parts = [f'<defs>{SCISSORS}</defs>']
    if grid:
        parts.append(grid_lines(lw))
    for back in (False, True):
        for z in SIZES[::-1]:
            parts.append(leg_piece(z, back, lw, colors, solo=False))
        d = piece('M', back)
        e = d['edges']
        lab = tp((e['top'][0][0] + e['side'][0][0]) / 2, 6.5, back)
        parts.append(T(lab[0], lab[1] - 2, 'TRASERO' if back else 'DELANTERO', 1.7, 700, fam='Archivo'))
        parts.append(T(lab[0], lab[1] - .6, 'Todas las tallas · corta 2', .6, 600))
    parts.append(pocket_piece('M', lw, colors, solo=False))
    for z in SIZES[::-1]:
        parts.append(band_piece(z, lw, colors, solo=False))
    parts.append(T(BAND_O[0] + 1.5, BAND_O[1] + 2.4, 'CINTURILLA · todas las tallas · corta 2 al doblez', .6, 700))
    parts.append(legend(None, lw, colors, 'Todas las tallas juntas (para calcar)'))
    return '\n'.join(parts)


R.canvas_size = canvas_size
R.canvas_all = canvas_all

if __name__ == '__main__':
    os.makedirs('build', exist_ok=True)
    for name, fn in [('a4', R.a4), ('a0', R.a0), ('proyector', R.projector)]:
        h = fn().replace('Camiseta básica de hombre', NAME).replace('Camiseta básica', NAME)
        with open(os.path.join('build', f'{name}.html'), 'w') as f:
            f.write(h)
    print('ok')
