"""Manual de la bermuda H-032 (mismo estilo y orden que el de la camiseta)."""
import os
import manual as Mn
import render_b as RB
from manual import badges, table, page, tip, steps_list, figure, fmt, CSS, FONTS
from render2 import COL, path, CW, CH, TW, TH, COLS, ROWS, a4_page_ranges, SCISSORS
from geo_b import SIZES, piece, pocket, measures, front_seam, back_seam, POCKET_OPEN, WAIST_BODY
from shapely.geometry import LineString

REF = 'H-032'
NAME = 'Bermuda de hombre'
Mn.REF = REF
Mn.TOTAL = 17
TOTAL = 17
OUT = 'build'
M = {s: measures(s) for s in SIZES}


def f1(v):
    return fmt(v)


def row(label, key=None, fn=None):
    return (label,) + tuple(f1(fn(M[s]) if fn else M[s][key]) for s in SIZES)


# ---------- Dibujos ----------
def thumb(kind):
    if kind == 'pocket':
        return f'<svg viewBox="-3 -3 22 34" class="th"><path d="{path(pocket()["cut"])}" fill="none" stroke="#111" stroke-width=".4"/></svg>'
    if kind == 'band':
        g = ''.join(f'<rect x="1" y="{12-M[s]["band_cut_h"]/2}" width="{M[s]["band_cut_half"]}" height="{M[s]["band_cut_h"]}" fill="none" stroke="{COL[s]}" stroke-width=".35"/>' for s in SIZES)
        return f'<svg viewBox="-1 0 38 24" class="th">{g}<path d="M1 7 L1 17" stroke="#111" stroke-width="1"/></svg>'
    back = kind == 'back'
    g = ''.join(f'<path d="{path(piece(s, back)["cut"])}" fill="none" stroke="{COL[s]}" stroke-width=".5"/>' for s in SIZES)
    return f'<svg viewBox="-4 -5 57 66" class="th">{g}</svg>'


def shorts_flat(letters=True):
    """Dibujo plano de la bermuda vista de frente (esquemático)."""
    body = 'M40 40 L160 40 L172 196 L108 204 L100 110 L92 204 L28 196 Z'
    band = '<rect x="40" y="18" width="120" height="22" fill="#d9d9d6" stroke="#111" stroke-width="1.2"/>'
    gath = ''.join(f'<path d="M{x} 20 L{x} 38" stroke="#888" stroke-width=".8"/>' for x in range(48, 160, 8))
    pk = '<path d="M150 46 Q158 70 163 92" fill="none" stroke="#111" stroke-width="1"/><path d="M50 46 Q42 70 37 92" fill="none" stroke="#111" stroke-width="1"/>'
    hem = '<path d="M30 186 L98 193 M170 186 L102 193" stroke="#888" stroke-width="1" stroke-dasharray="4 3"/>'
    lab = ''
    if letters:
        def L(x, y, t):
            return f'<circle cx="{x}" cy="{y}" r="7" fill="#fff" stroke="#111" stroke-width="1.2"/><text x="{x}" y="{y+3.6}" text-anchor="middle" font-size="9.5" font-weight="600">{t}</text>'
        ln = 'stroke="#111" stroke-width="1"'
        lab = (f'<path d="M40 8 L160 8" {ln}/>' + L(70, 8, 'A') + L(130, 8, 'B') +
               f'<path d="M34 70 L166 70" {ln}/>' + L(100, 70, 'C') +
               f'<path d="M182 18 L190 196" {ln}/>' + L(186, 110, 'D') +
               L(100, 90, 'E') + L(118, 150, 'G') + L(14, 29, 'I') +
               f'<path d="M28 214 L92 214" {ln}/>' + L(60, 214, 'H'))
    return (f'<svg viewBox="0 -2 200 226" class="tee"><path d="{body}" fill="#ececea" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/>'
            f'{band}{gath}{pk}{hem}<path d="M100 40 L100 110" stroke="#111" stroke-width="1"/>{lab}</svg>')


def cutting_layout():
    W, H = 75, 130
    f, b, pk = piece('M')['cut'], piece('M', True)['cut'], pocket()['cut']
    def trn(pts, dx, dy):
        return [(x + dx, y + dy) for x, y in pts]
    fx = W - 37.6
    g = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="#f4f4f2" stroke="#bbb" stroke-width=".3"/>',
         f'<path d="M0 0 L0 {H}" stroke="#111" stroke-width="1.2"/>']
    g.append(f'<path d="{path(trn(f, fx, 1.5))}" fill="#d9d9d6" stroke="#111" stroke-width=".35"/>')
    g.append(f'<text x="{fx+18}" y="30" font-size="3.2" font-weight="600" text-anchor="middle">DELANTERO</text>')
    g.append(f'<path d="{path(trn(b, 2.5, 62))}" fill="#d9d9d6" stroke="#111" stroke-width=".35"/>')
    g.append('<text x="24" y="92" font-size="3.2" font-weight="600" text-anchor="middle">TRASERO</text>')
    L = M['M']['band_cut_half']
    for i in range(2):
        g.append(f'<rect x="0" y="{1.5+i*11}" width="{L}" height="10" fill="#bdbdba" stroke="#111" stroke-width=".35"/>')
        g.append(f'<text x="{L/2}" y="{7.4+i*11}" font-size="2.6" font-weight="600" text-anchor="middle">CINTURILLA</text>')
    g.append(f'<path d="{path(trn(pk, 2.0, 25.5))}" fill="#bdbdba" stroke="#111" stroke-width=".35"/>')
    g.append(f'<path d="{path(trn(pk, 53.5, 64))}" fill="#bdbdba" stroke="#111" stroke-width=".35"/>')
    g.append('<text x="10" y="41" font-size="2.6" font-weight="600" text-anchor="middle">BOLSILLO</text><text x="61.5" y="79" font-size="2.6" font-weight="600" text-anchor="middle">BOLSILLO</text>')
    g.append(f'<text x="1.6" y="{H-3}" font-size="2.6" font-weight="600" letter-spacing=".2">DOBLEZ</text>')
    return (f'<svg viewBox="-2 -8 79 {H+15}" class="lay"><text x="37.5" y="-3" font-size="2.8" text-anchor="middle" fill="#555">75 cm (tela de 150 cm doblada)</text>'
            + ''.join(g) + f'<text x="37.5" y="{H+6}" font-size="2.8" text-anchor="middle" font-weight="600">Largo de tela para la talla M: 1,3 m</text></svg>')


def step_svg(n):
    leg = 'M20 10 L70 10 L76 84 L44 88 L40 46 L22 40 Z'
    if n == 1:
        return ('<svg viewBox="0 0 120 92" class="stp"><path d="M30 6 L80 6 L86 86 L48 88 L44 44 L26 38 Z" fill="#c9c9c6" stroke="#111" stroke-width=".5"/>'
                '<path d="M80 8 Q100 10 102 22 Q103 38 92 42 L82 40" fill="#e9e9e7" stroke="#111" stroke-width=".5"/>'
                '<path d="M79 8 L81 40" stroke="#111" stroke-width="1.1" stroke-dasharray="1.6 1"/>'
                '<path d="M76 11 L82 11 M76 30 L82 30" stroke="#111" stroke-width="1"/>'
                '<text x="54" y="56" font-size="4" text-anchor="middle" font-weight="600">DELANTERO</text><text x="54" y="61" font-size="3.2" text-anchor="middle" fill="#555">(derecho arriba)</text>'
                '<text x="96" y="28" font-size="3.6" text-anchor="middle" font-weight="600">BOLSILLO</text><text x="100" y="52" font-size="3.2" text-anchor="middle">rayitas juntas</text></svg>')
    if n == 2:
        return ('<svg viewBox="0 0 120 92" class="stp"><path d="M30 6 L80 6 L86 86 L48 88 L44 44 L26 38 Z" fill="#c9c9c6" stroke="#111" stroke-width=".5"/>'
                '<path d="M80 9 Q99 11 101 23 Q102 38 91 42 L82 41" fill="#e9e9e7" stroke="#111" stroke-width=".5"/>'
                '<path d="M78.5 6 L79.2 11 Q97 13 98 24 Q99 36 89 39 L80.6 39 L85 86" fill="none" stroke="#111" stroke-width="1.1" stroke-dasharray="1.6 1"/>'
                '<text x="56" y="56" font-size="4" text-anchor="middle" font-weight="600">DELANTERO + TRASERO</text><text x="56" y="61" font-size="3.2" text-anchor="middle" fill="#555">(derecho con derecho)</text>'
                '<text x="104" y="60" font-size="3.2" text-anchor="middle">costura</text><text x="104" y="64" font-size="3.2" text-anchor="middle">alrededor</text><text x="104" y="68" font-size="3.2" text-anchor="middle">del bolsillo</text></svg>')
    if n == 3:
        return ('<svg viewBox="0 0 120 92" class="stp"><path d="M36 6 L84 6 L82 86 L40 86 Z" fill="#c9c9c6" stroke="#111" stroke-width=".5"/>'
                '<path d="M40 40 L42 86" stroke="#111" stroke-width="1.1" stroke-dasharray="1.6 1"/><path d="M36 6 Q38 30 40 40" fill="none" stroke="#111" stroke-width=".6"/>'
                '<text x="62" y="46" font-size="4" text-anchor="middle" font-weight="600">PERNERA</text><text x="62" y="51" font-size="3.2" text-anchor="middle" fill="#555">(doblada, revés fuera)</text>'
                '<text x="28" y="66" font-size="3.4" text-anchor="middle">entrepierna</text></svg>')
    if n == 4:
        return ('<svg viewBox="0 0 120 92" class="stp"><path d="M22 10 L62 10 L60 86 L26 86 Z" fill="#c9c9c6" stroke="#111" stroke-width=".5"/>'
                '<path d="M58 10 L98 10 L94 86 L60 86 Z" fill="#e2e2df" stroke="#111" stroke-width=".5"/>'
                '<path d="M60 10 Q60 40 60 46" fill="none" stroke="#111" stroke-width="1.2" stroke-dasharray="1.6 1"/>'
                '<text x="40" y="52" font-size="3.6" text-anchor="middle" font-weight="600">pernera</text><text x="40" y="57" font-size="3.2" text-anchor="middle">(revés fuera)</text>'
                '<text x="78" y="52" font-size="3.6" text-anchor="middle" font-weight="600">pernera</text><text x="78" y="57" font-size="3.2" text-anchor="middle">(metida dentro)</text>'
                '<text x="60" y="6" font-size="3.4" text-anchor="middle">tiro: una sola costura curva</text></svg>')
    if n == 5:
        return ('<svg viewBox="0 0 120 92" class="stp"><rect x="14" y="10" width="92" height="12" fill="#c9c9c6" stroke="#111" stroke-width=".6"/>'
                '<path d="M14 16 L106 16" stroke="#111" stroke-width=".5" stroke-dasharray="2 1.2"/><path d="M60 10 L60 22" stroke="#111" stroke-width="1"/>'
                '<path d="M60 16 L60 22" stroke="#fff" stroke-width="1.6"/>'
                '<text x="60" y="30" font-size="3.6" text-anchor="middle">abertura de 4 cm en una costura (por dentro)</text>'
                '<path d="M20 44 L100 44 L104 86 L16 86 Z" fill="#e2e2df" stroke="#111" stroke-width=".5"/><rect x="20" y="38" width="80" height="8" fill="#c9c9c6" stroke="#111" stroke-width=".5"/>'
                '<path d="M20 45 L100 45" stroke="#111" stroke-width="1.1" stroke-dasharray="1.6 1"/><text x="60" y="66" font-size="4" text-anchor="middle" font-weight="600">PANTALÓN</text></svg>')
    if n == 6:
        return ('<svg viewBox="0 0 120 92" class="stp"><rect x="10" y="30" width="100" height="16" fill="#c9c9c6" stroke="#111" stroke-width=".6"/>'
                '<path d="M10 38 L74 38" stroke="#fff" stroke-width="5"/><path d="M10 38 L74 38" stroke="#111" stroke-width=".5" stroke-dasharray="2 1"/>'
                '<path d="M74 35 L84 38 L74 41" fill="none" stroke="#111" stroke-width=".9"/><ellipse cx="80" cy="38" rx="6" ry="2.4" fill="none" stroke="#111" stroke-width=".8"/>'
                '<text x="60" y="24" font-size="3.8" text-anchor="middle" font-weight="600">CINTURILLA</text>'
                '<text x="60" y="58" font-size="3.4" text-anchor="middle">el imperdible lleva el elástico por dentro</text>'
                '<rect x="36" y="66" width="48" height="10" fill="#fff" stroke="#111" stroke-width=".6"/><rect x="56" y="66" width="8" height="10" fill="#d9d9d6"/>'
                '<path d="M57 67 L63 75 M63 67 L57 75" stroke="#111" stroke-width=".7"/><text x="60" y="84" font-size="3.4" text-anchor="middle">solapa 2 cm y cose con zigzag</text></svg>')
    if n == 7:
        return ('<svg viewBox="0 0 120 92" class="stp"><rect x="16" y="6" width="88" height="62" fill="#c9c9c6" stroke="#111" stroke-width=".5"/>'
                '<rect x="16" y="68" width="88" height="10" fill="#e2e2df" stroke="#111" stroke-width=".5"/>'
                '<path d="M17 72 L103 72" stroke="#111" stroke-width=".5" stroke-dasharray="1.5 1"/>'
                '<text x="60" y="38" font-size="4" text-anchor="middle" font-weight="600">PERNERA (del revés)</text>'
                '<text x="60" y="87" font-size="3.4" text-anchor="middle">dobla 1 cm, luego 2,5 cm · cose a 2,3 cm del borde</text></svg>')


def step(n, title, items, tipt):
    return f'''<div class="step"><div class="sh"><span class="sn">{n}</span><div><span class="eb">Paso {n}</span><h3>{title}</h3></div></div>
      <div class="sg"><div class="art">{step_svg(n)}</div>{steps_list(items)}</div>{tip("Consejo", tipt)}</div>'''


# ---------- Puntos para dibujar a mano ----------
def at(seg, d):
    ln = LineString(seg)
    p = ln.interpolate(d)
    return (p.x, p.y)


def leg_points(s, back):
    d = piece(s, back)
    sg = d['segs']
    side = sg['side']
    kink = min(side, key=lambda p: abs(p[1] - .55 * {'XS': 23, 'S': 23.5, 'M': 24, 'L': 24.5, 'XL': 25}[s]))
    cr = sg['crotch']
    curve_len = LineString(d['edges']['crotch'][:-1]).length
    pts = [('A', 'Cintura, en el tiro', sg['top'][0]), ('B', 'Cintura, en el costado', sg['top'][-1]),
           ('K', 'Costado: aquí empieza a estrecharse', kink), ('E', 'Bajo, en el costado', side[-1]),
           ('F', 'Bajo, en la entrepierna', sg['hem'][-1]), ('C', 'Punta de la entrepierna', sg['inseam'][-1])]
    for i in range(1, 5):
        pts.append((f't{i}', 'curva del tiro', at(cr, curve_len * i / 5)))
    pts.append(('P', 'Fin de la curva: de aquí a A, recto', at(cr, curve_len)))
    return pts


def shift(pts_by_size):
    xs = [p[2][0] for v in pts_by_size.values() for p in v]
    ys = [p[2][1] for v in pts_by_size.values() for p in v]
    x0, y0 = min(xs), min(ys)
    return {k: [(a, b, (x - x0, y - y0)) for a, b, (x, y) in v] for k, v in pts_by_size.items()}, (x0, y0)


def pts_diagram(pts, cut, origin, box):
    c = COL['M']
    x0, y0 = origin
    outline = f'<path d="{path([(x - x0, y - y0) for x, y in cut])}" fill="{c}" fill-opacity=".08" stroke="{c}" stroke-width=".6"/>'
    dots = ''
    for a, _, (x, y) in pts:
        big = a[0] not in 'tc' or a == 'C'
        dots += f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{.6 if big else .45}" fill="{"#111" if big else c}"/>'
        dots += f'<text x="{x+1:.2f}" y="{y+.7:.2f}" font-size="{1.9 if big else 1.5}" font-weight="{700 if big else 500}">{a}</text>'
    axes = ('<path d="M0 0 L9 0 M0 0 L0 9" stroke="#111" stroke-width=".3"/><path d="M8 -.6 L9 0 L8 .6 M-.6 8 L0 9 L.6 8" stroke="#111" stroke-width=".3" fill="none"/>'
            '<text x="9.6" y=".5" font-size="1.4">x</text><text x=".6" y="10.4" font-size="1.4">y</text><text x="-.6" y="-.9" font-size="1.3" text-anchor="end">(0, 0)</text>')
    return f'<svg viewBox="{box}" class="pd">{outline}{axes}{dots}</svg>'


def annex(P):
    howto = steps_list(['Pega folios o usa papel de patronaje o de estraza: necesitas unos <b>45 × 62 cm</b> para cada pieza (un poco más en las tallas grandes).',
                        'Dibuja con regla una <b>esquina</b>: una línea horizontal arriba y otra vertical a la izquierda. La esquina es el <b>(0, 0)</b>.',
                        'Para cada punto de tu talla, mide <b>x hacia la derecha</b> e <b>y hacia abajo</b> desde la esquina y marca un punto con el boli.',
                        'Une con regla: <b>A–B</b> (cintura), <b>B–K–E</b> (costado), <b>E–F</b> (bajo), <b>F–C</b> (entrepierna) y <b>P–A</b>. De C a P, pasando por t1…t4, traza una <b>curva suave</b> a mano: es el tiro.',
                        'Copia también las rayitas del costado (boca del bolsillo, a 2 y a 18 cm de la cintura) y recorta. <b>El margen ya está incluido.</b>'])
    for n, back, title in [(15, False, 'Delantero'), (16, True, 'Trasero')]:
        raw = {s: leg_points(s, back) for s in SIZES}
        pts, origin = shift(raw)
        tab = Mn.coord_table(pts)
        diag = pts_diagram(pts['M'], piece('M', back)['cut'], origin, '-4 -3 58 66')
        side = howto if not back else '<p class="note">Igual que el delantero. El trasero es más ancho y su curva del tiro es más larga y más alta: así no lo confundirás. Marca <b>dos rayitas</b> en el costado, a 30 cm de la cintura, y una en el delantero.</p>'
        top = f'<div class="two fx ann"><div>{diag}<p class="note c">Ejemplo: talla M</p></div><div>' + (f'<h4>Cómo dibujarlo</h4>{side}' if not back else side) + '</div></div>'
        P.append(page(n, 'Sin impresora · dibújalo con regla', f'{title}: puntos para dibujar', top + '<h4>Coordenadas en cm (margen incluido)</h4>' + tab))
    # Bolsillo y cinturilla
    d = pocket()
    cv = d['segs']['curve']
    L = LineString(cv).length
    pk = [('A', 'Arriba, en el borde recto', cv[0])] + [(f'c{i}', 'curva del bolsillo', at(cv, L * i / 8)) for i in range(1, 8)] + [('B', 'Abajo, en el borde recto', cv[-1])]
    x0 = min(p[0] for p in d['cut']); y0 = min(p[1] for p in d['cut'])
    pk = [(a, b, (x - x0, y - y0)) for a, b, (x, y) in pk]
    rows = ''.join(f'<tr><td><b>{a}</b></td><td class="w">{b}</td><td>{fmt(x)}</td><td>{fmt(y)}</td></tr>' for a, b, (x, y) in pk)
    ptab = f'<table class="t coord pk"><thead><tr><th>Punto</th><th style="text-align:left">Dónde está</th><th>x</th><th>y</th></tr></thead><tbody>{rows}</tbody></table>'
    diag = pts_diagram(pk, d['cut'], (x0, y0), '-3 -3 26 36')
    band = table([('Cinturilla: corta 2 (abierta, largo × alto)',) + tuple(f'{fmt(2*M[s]["band_cut_half"])} × 10' for s in SIZES),
                  ('Elástico de 3,5 cm: largo de corte',) + tuple(f'{M[s]["elastic"]}' for s in SIZES)])
    P.append(page(17, 'Sin impresora · dibújalo con regla', 'Bolsillo y cinturilla', f'''
  <div class="two fx ann sl"><div>{diag}<p class="note c">Bolsillo: talla única</p></div><div>
  <p class="note">El bolsillo es igual en todas las tallas. Dibuja la línea vertical del borde recto a la izquierda: va de <b>A</b> a <b>B</b>. Une A con los puntos c1…c7 y B con una <b>curva suave</b>. Marca las rayitas de la boca en el borde recto, a 3,3 y a 19,3 cm de arriba.</p>
  {ptab}</div></div>
  <h4>Cinturilla</h4>
  <p class="note">Es un rectángulo: dibújalo con regla directamente en la tela. Las medidas incluyen 1 cm de margen en todos los bordes. Si la cortas al doblez, dibuja solo la mitad del largo con el borde corto sobre el doblez de la tela.</p>
  {band}'''))


# ---------- Páginas ----------
def build():
    P = []
    P.append(f'''<section class="page cover">
  <div class="cv-img"><img src="portada.jpg" alt=""></div>
  <div class="cv-txt">
    <div class="cv-top"><span class="logo">HILVÁN</span><span class="eb">Patrón PDF · Ref. {REF}</span></div>
    <h1>Bermuda<br>de hombre</h1>
    <p class="lead">Pantalón corto con cintura elástica, bolsillos en el costado y largo a 1 cm de la rodilla. Patrón a escala real con manual paso a paso, pensado para quien empieza a coser.</p>
    <div class="cv-row"><div><b>Principiante</b><span>Nivel</span></div><div><b>3–4 h</b><span>Tiempo</span></div><div><b>XS–XL</b><span>Tallas</span></div><div><b>Tela plana</b><span>Tela</span></div></div>
    <div class="cv-sizes">{badges()}</div>
  </div></section>''')

    idx = [('Materiales y herramientas', 3), ('Guía de tallas', 4), ('Medidas de la prenda terminada', 5), ('Cómo imprimir el patrón', 6),
           ('Cómo leer el patrón', 7), ('Cómo cortar la tela', 8), ('Antes de coser: lo esencial', 9), ('Montaje paso a paso (7 pasos)', 10),
           ('Remate y revisión', 14), ('Sin impresora: dibújalo con regla', 15)]
    P.append(page(2, 'Antes de empezar', 'Bienvenida', f'''
  <p class="intro">Con este patrón vas a coser una <b>bermuda de hombre con cintura elástica, bolsillos en el costado y largo a 1 cm de la rodilla</b>, desde cero. No lleva cremallera ni botones: solo necesitas <b>una máquina de coser con puntada recta y zigzag, la tela, un elástico y el patrón impreso</b>. Cada talla tiene <b>su color y sus propias páginas</b>, a tamaño real y con el <b>margen de costura ya incluido</b>. ¿No tienes impresora? Al final del manual tienes las medidas para dibujarlo con papel, boli y regla.</p>
  <div class="cards3"><div class="card"><span class="eb">Nivel</span><b>Principiante</b><small>sin conocimientos previos</small></div>
  <div class="card"><span class="eb">Tiempo</span><b>3–4 horas</b><small>la primera vez</small></div>
  <div class="card"><span class="eb">Tallas</span><b>XS · S · M · L · XL</b><small>de hombre</small></div></div>
  <h4>Las piezas de tu bermuda</h4>
  <div class="pieces">
    <div><div class="pv">{thumb('front')}</div><b>Delantero</b><small>corta 2</small></div>
    <div><div class="pv">{thumb('back')}</div><b>Trasero</b><small>corta 2</small></div>
    <div><div class="pv">{thumb('pocket')}</div><b>Bolsillo</b><small>corta 4</small></div>
    <div><div class="pv">{thumb('band')}</div><b>Cinturilla</b><small>corta 2 al doblez</small></div>
  </div>
  <div class="two">
    <div><h4>Archivos que incluye</h4>
      <div class="files"><div><b>Manual</b><span>este documento · 17 páginas</span></div><div><b>Patrón A4</b><span>18 hojas por talla · imprime solo la tuya</span></div><div><b>Patrón A0</b><span>1 hoja por talla, para copistería</span></div><div><b>Patrón proyector</b><span>1 página por talla, clara y oscura</span></div></div></div>
    <div><h4>En este manual</h4><div class="toc">{''.join(f'<div><span>{a}</span><i></i><b>{b}</b></div>' for a, b in idx)}</div></div>
  </div>
  {tip('Antes de cortar la tela buena', 'Si es la primera vez que usas este patrón, haz una prueba con una tela barata y de tu talla. Así compruebas el ajuste y el largo y practicas cada paso sin miedo a equivocarte.')}'''))

    mats = [('Tela plana de algodón o lino', 'Chino, sarga, gabardina ligera o lino, de 150 a 250 g/m². Ancho: 140–150 cm. Evita las telas elásticas la primera vez.'),
            ('Elástico de 3,5 cm de ancho', 'Elástico plano para cinturillas. Mira en la tabla de abajo cuánto necesitas según tu talla.'),
            ('Hilo de poliéster', '1 bobina del color de la tela. Es más resistente que el de algodón.'),
            ('Aguja universal', 'Del 80/12; del 90/14 si la tela es gruesa.'),
            ('Imperdible grande', 'Sirve para meter el elástico por dentro de la cinturilla.')]
    tools = ['Máquina de coser con puntada recta y zigzag', 'Tijeras de costura o cortador rotativo con base', 'Clips de costura o alfileres',
             'Cinta métrica y regla larga (60 cm o más)', 'Patrón impreso, celo y tijeras de papel', 'Sin impresora: papel grande y regla',
             'Tiza de sastre o lápiz de tela', 'Plancha y tabla de planchar', 'Descosedor (por si te equivocas)']
    P.append(page(3, 'Prepárate', 'Materiales y herramientas', f'''
  <h4>Lo que necesitas comprar</h4>
  <div class="mats">{''.join(f'<div><span class="n">{i+1}</span><div><b>{a}</b><p>{b}</p></div></div>' for i, (a, b) in enumerate(mats))}</div>
  <h4>Herramientas</h4>
  <ul class="checks">{''.join(f'<li>{t}</li>' for t in tools)}</ul>
  <h4>Cuánto necesitas según tu talla</h4>
  {table([('Tela de 140–150 cm de ancho (m)', '1,2', '1,2', '1,3', '1,4', '1,5'), ('Elástico de 3,5 cm (cm)',) + tuple(str(M[s]['elastic']) for s in SIZES), ('Hilo (bobinas)', '1', '1', '1', '1', '1')])}
  <ul class="dots"><li><b>Prelava y seca la tela</b> igual que lavarás la bermuda: así no encoge después de coserla.</li>
  <li>Calculado para tela sin dirección en el dibujo. Si tiene dibujo o pelo, añade 20 cm.</li>
  <li>El elástico ya incluye 2 cm para solaparlo al cerrarlo.</li></ul>'''))

    P.append(page(4, 'Elige tu talla', 'Guía de tallas', f'''
  <div class="two fx"><div>{figure()}</div><div><h4>Cómo medirte</h4>
    {steps_list(['<b>Cintura:</b> rodea la parte más estrecha del torso, a la altura del ombligo, sin apretar.', '<b>Cadera:</b> rodea la parte más ancha de la cadera y el culo, con los pies juntos.', '<b>Largo:</b> mide de la cintura hasta 1 cm por encima de la rodilla y compáralo con el largo total (D) de la página siguiente.'])}
    {tip('Importante', 'Mídete con ropa fina, de pie y relajado. <b>Elige la talla por la medida de la cadera.</b> La cintura la ajusta el elástico.')}</div></div>
  <h4>Medidas del cuerpo (cm)</h4>
  {table([('Contorno de cintura', '72–76', '80–84', '88–92', '96–100', '104–108'), ('Contorno de cadera', '88–92', '96–100', '104–108', '112–116', '120–124'), ('Altura aproximada', '164–170', '170–175', '175–180', '180–185', '185–190')])}
  <div class="cards3"><div class="card"><span class="eb">Ajuste</span><b>Relajado</b><small>10 cm de holgura en la cadera: cómoda y con caída recta.</small></div>
  <div class="card"><span class="eb">Si dudas</span><b>Entre dos tallas</b><small>Elige la de tu cadera. ¿Más ajustada? Baja una. ¿Más holgada? Sube una.</small></div>
  <div class="card"><span class="eb">Largo</span><b>A la rodilla</b><small>Queda a 1 cm de la rodilla con la altura de la tabla. Alarga o acorta en el bajo.</small></div></div>
  {tip('Cómo se calcula cada talla', 'Con el límite alto de cada rango de cadera (por ejemplo, la M con 108 cm) más 10 cm de holgura. El largo crece 1,5 cm por talla.')}'''))

    P.append(page(5, 'Tabla de medidas', 'Medidas de la prenda terminada', f'''
  <div class="two fx mtg"><div class="mt">{shorts_flat()}</div><div>
  <table class="t sm"><thead><tr><th></th><th style="text-align:left">Medida (cm)</th>{''.join(f'<th><span class="sz" style="background:{COL[s]}">{s}</span></th>' for s in SIZES)}</tr></thead><tbody>
  {''.join(f'<tr><td><b>{a}</b></td><td>{b}</td>' + ''.join(f'<td style="color:{COL[s]}">{fmt(fn(M[s]))}</td>' for s in SIZES) + '</tr>' for a, b, fn in [
      ('A', 'Cintura sin estirar (plano)', lambda m: m['waist_relaxed'] / 2), ('B', 'Cintura con el elástico (plano)', lambda m: (m['elastic'] - 2) / 2),
      ('C', 'Cadera (plano)', lambda m: m['hip'] / 2), ('D', 'Largo total, con cinturilla', lambda m: m['side_f'] + 4),
      ('E', 'Tiro delantero, con cinturilla', lambda m: m['rise_f'] + 4), ('F', 'Tiro trasero, con cinturilla', lambda m: m['rise_b'] + 4),
      ('G', 'Entrepierna', lambda m: m['ins_f']), ('H', 'Ancho del bajo (plano)', lambda m: m['opening'] / 2), ('I', 'Alto de la cinturilla', lambda m: 4)])}
  </tbody></table></div></div>
  <h4>Longitud de cada costura (cm, sin margen)</h4>
  <p class="note">Úsala para comprobar tu patrón recortado: mide por la línea de costura, a 1,5 cm del borde.</p>
  {table([row('Costado (delantero y trasero)', fn=lambda m: m['side_f']), row('Entrepierna (delantero y trasero)', fn=lambda m: m['ins_f']),
          row('Tiro delantero (sin cinturilla)', fn=lambda m: m['rise_f']), row('Tiro trasero (sin cinturilla)', fn=lambda m: m['rise_b']),
          row('Contorno de la cintura del pantalón', fn=lambda m: m['waist_relaxed']), row('Contorno del bajo de cada pierna', fn=lambda m: m['opening']),
          ('Boca del bolsillo', '16', '16', '16', '16', '16')], cls='sm')}
  <h4>Piezas rectangulares (medidas de corte, margen incluido)</h4>
  {table([('Cinturilla: corta 2 (largo × alto)',) + tuple(f'{fmt(2*M[s]["band_cut_half"])} × 10' for s in SIZES), ('Elástico de 3,5 cm (largo)',) + tuple(str(M[s]['elastic']) for s in SIZES)])}
  <p class="note">La cintura del pantalón es más ancha que tu cadera para que la bermuda entre sin cremallera; el elástico la recoge hasta tu cintura. Si quieres la cintura más justa o más suelta, acorta o alarga el elástico 2–3 cm.</p>'''))

    grid = ''.join(f'<rect x="{c*TW}" y="{r*TH}" width="{TW}" height="{TH}" fill="none" stroke="#111" stroke-width=".3"/>'
                   f'<text x="{c*TW+TW/2}" y="{r*TH+TH/2+1.8}" font-size="5" font-weight="700" text-anchor="middle" fill="#111" fill-opacity=".45">{"ABC"[c]}{r+1}</text>'
                   f'<text x="{c*TW+TW/2}" y="{r*TH+TH/2+5.6}" font-size="2.4" font-weight="600" text-anchor="middle" fill="#111" fill-opacity=".5">hoja {c*ROWS+r+1}</text>'
                   for r in range(ROWS) for c in range(COLS))
    mapsvg = f'<svg viewBox="0 0 {CW} {CH}" class="map">{RB.canvas_size("M", lw=.2)}{grid}</svg>'
    rng = a4_page_ranges()
    rows6 = ''.join(f'<tr><td><span class="sz" style="background:{COL[z]}">{z}</span></td><td>págs. {a1}–{b1}</td><td>pág. {i+1}</td><td>págs. {i+1} y {i+6}</td></tr>' for i, (z, (a1, b1)) in enumerate(rng.items()))
    P.append(page(6, 'Escala real 1:1', 'Cómo imprimir el patrón', f"""
  <p class="intro">El patrón viene en <b>tres formatos</b>. En los tres, <b>cada talla tiene sus propias páginas y su color</b>: solo imprimes o proyectas la tuya, así que solo verás una línea para recortar.</p>
  <h4>Qué páginas son las de tu talla</h4>
  <table class="t plain pr6"><thead><tr><th>Talla</th><th>A4 · en casa</th><th>A0 · copistería</th><th>Proyector (clara y oscura)</th></tr></thead><tbody>{rows6}</tbody></table>
  <p class="note">En la ventana de imprimir, elige “Páginas” y escribe las de tu talla. Imprime siempre al <b>100 %</b> (“tamaño real”), sin “ajustar a página”. El A0 y el proyector tienen además una página final con todas las tallas juntas, para calcar.</p>
  <div class="two fx"><div>
    <h4>A4: une las hojas como un puzle</h4>
    {steps_list(['Imprime primero la página 1 y <b>mide el cuadrado de prueba</b>: tiene que medir 5 × 5 cm.', 'Imprime las 18 hojas de tu talla. Cada una lleva arriba su <b>talla en color</b> y su código. Salen <b>por columnas</b>: A1 a A6, luego B1 a B6 y C1 a C6.', 'Recorta el margen blanco <b>a la derecha y abajo</b> de cada hoja.', 'Colócalas como en el mapa y júntalas a tope: los <b>medios rombos negros</b> forman un rombo completo. Pega con celo.', 'Recorta cada pieza <b>por la línea gruesa de color</b>.'])}
    <h4>Proyector</h4>
    <p class="note">Ajusta el proyector hasta que los cuadros de la cuadrícula midan <b>10 × 10 cm</b> sobre la mesa y comprueba el cuadrado de 5 cm. Corta la tela siguiendo la línea de color.</p>
    <div class="test"><svg width="5.2cm" height="5.2cm" viewBox="-.1 -.1 5.2 5.2"><rect x="0" y="0" width="5" height="5" fill="none" stroke="#111" stroke-width=".05"/><text x="2.5" y="2.7" font-size=".5" font-weight="700" text-anchor="middle">5 × 5 cm</text></svg><p><b>Cuadrado de prueba a tamaño real.</b> Si imprimes este manual al 100 %, también te sirve para comprobar tu impresora.</p></div>
  </div><div><h4>Mapa del A4 (3 × 6 hojas)</h4>{mapsvg}<p class="note">Ejemplo con la talla M. Las perneras están tumbadas: la cintura a la izquierda y el bajo a la derecha.</p></div></div>"""))

    c = COL['M']
    def symrow(svg, txt):
        return f'<div class="sym"><svg viewBox="0 0 60 16" width="64" height="17">{svg}</svg><span>{txt}</span></div>'
    syms = (symrow(f'<path d="M3 8 L57 8" stroke="{c}" stroke-width="3.2" stroke-linecap="round"/>', '<b>Línea gruesa de color: recorta por aquí.</b> Es la línea de corte de tu talla.') +
            symrow(f'<defs>{SCISSORS}</defs><use href="#sc" x="20" y="0" width="16" height="16" style="color:{c}"/>', '<b>Tijeras:</b> te recuerdan que ese borde se corta.') +
            symrow('<path d="M3 8 L57 8" stroke="#111" stroke-width="4"/>', '<b>Borde negro: NO se corta.</b> Solo en la cinturilla: va justo en el doblez de la tela.') +
            symrow('<path d="M3 8 L57 8" stroke="#888" stroke-width="1" stroke-dasharray="3 2.5"/>', '<b>Puntos grises: línea de costura.</b> Te enseña por dónde coserás. No se corta.') +
            symrow('<path d="M6 8 L54 8 M10 5 L6 8 L10 11 M50 5 L54 8 L50 11" stroke="#111" stroke-width="1.1" fill="none"/>', '<b>Flecha de hilo:</b> colócala paralela al orillo (el borde de la tela).') +
            symrow('<path d="M10 13 L50 13" stroke="#888" stroke-width="1" stroke-dasharray="3 2"/><path d="M24 13 L24 3" stroke="#111" stroke-width="2.6"/><path d="M36 13 L36 3" stroke="#111" stroke-width="2.6"/>', '<b>Rayitas del costado:</b> marcan la boca del bolsillo. Una rayita más abajo = delantero; dos = trasero.'))
    d = piece('M')
    sg = d['segs']
    dpath = ''.join(f'<path d="{path(sg[k], False)}" fill="none" stroke="{c}" stroke-width="1.1" stroke-linecap="round"/>' for k in sg)
    demo = (f'<svg viewBox="-4 -5 50 66" class="demo"><path d="{path(d["cut"])}" fill="{c}" fill-opacity=".1"/>'
            f'<path d="{path(d["seam"])}" fill="none" stroke="#888" stroke-width=".35" stroke-dasharray="1 .8"/>{dpath}'
            + ''.join(f'<path d="M{sg["side"][0][0]} {y} L{sg["side"][0][0]-1.6} {y}" stroke="#111" stroke-width=".7"/>' for y in (2, 18, 30)) +
            f'<text x="6" y="12" font-size="3.4" font-weight="700" font-family="Archivo" font-stretch="125%">DELANTERO</text>'
            f'<rect x="6" y="14" width="12" height="3.4" rx="1.7" fill="{c}"/><text x="12" y="16.4" font-size="1.9" font-weight="700" fill="#fff" text-anchor="middle">TALLA M</text>'
            f'<text x="20" y="-1.8" font-size="2" font-weight="700" text-anchor="middle">CINTURA</text><text x="20" y="59.5" font-size="2" font-weight="700" text-anchor="middle">BAJO</text>'
            f'<text x="44" y="10" font-size="1.8" font-weight="700" transform="rotate(90 44 10)">BOCA DEL BOLSILLO</text></svg>')
    P.append(page(7, 'Símbolos', 'Cómo leer el patrón', f"""
  <div class="two fx sy7"><div><h4>Así es una pieza de tu patrón</h4>{demo}</div>
  <div><h4>Qué significa cada línea</h4><div class="syms">{syms}</div></div></div>
  <h4>El margen de costura ya está incluido</h4>
  <table class="t plain"><thead><tr><th>Pieza</th><th>Cose a</th><th>Dónde</th></tr></thead><tbody>
  <tr><td><b>Delantero y trasero</b></td><td>1,5 cm</td><td>costados, entrepierna y tiro</td></tr><tr><td></td><td>1 cm</td><td>cintura: se une a la cinturilla</td></tr>
  <tr><td></td><td>3,5 cm</td><td>bajo: se dobla 1 cm y luego 2,5 cm</td></tr><tr><td><b>Bolsillo</b></td><td>1 cm</td><td>curva del bolsillo y unión al costado</td></tr>
  <tr><td><b>Cinturilla</b></td><td>1 cm</td><td>extremos y borde que se une a la cintura</td></tr></tbody></table>
  <h4>Piezas y cantidad</h4>
  <table class="t plain"><thead><tr><th>Pieza</th><th>N.º</th><th>Cómo cortarla</th></tr></thead><tbody>
  <tr><td><b>Delantero</b></td><td>2</td><td>con la tela doblada: cortas las dos capas a la vez</td></tr><tr><td><b>Trasero</b></td><td>2</td><td>con la tela doblada: cortas las dos capas a la vez</td></tr>
  <tr><td><b>Bolsillo</b></td><td>4</td><td>con la tela doblada, dos veces</td></tr><tr><td><b>Cinturilla</b></td><td>2</td><td>borde negro en el doblez de la tela, dos veces</td></tr></tbody></table>"""))

    P.append(page(8, 'Corte', 'Cómo cortar la tela', f'''
  <div class="two fx"><div>{cutting_layout()}<p class="note c">Dibujo para la talla M. En la L y la XL coloca las cinturillas debajo del trasero si no caben junto al delantero.</p></div><div>
  <h4>Prepara la tela</h4>
  <ul class="dots"><li>Plancha la tela y dóblala por la mitad a lo largo, <b>derecho con derecho</b> y con los orillos juntos.</li><li>Recorta el patrón por la <b>línea gruesa de color</b>. <b>No añadas margen</b>: ya está incluido.</li></ul>
  <h4>Corta las piezas</h4>
  {steps_list(['<b>Delantero y trasero:</b> la flecha de hilo paralela al orillo. Corta las dos capas: te salen la pierna derecha y la izquierda.', '<b>Bolsillo:</b> colócalo y córtalo <b>dos veces</b> sobre la tela doblada: salen 4 bolsillos.', '<b>Cinturilla:</b> el borde negro justo sobre el doblez de la tela. Córtala <b>dos veces</b>.', '<b>Marca las rayitas</b> del costado en todas las piezas con un corte pequeño de 3 mm o con tiza.'])}
  {tip('Para no confundir las piezas', 'El <b>trasero</b> es más ancho y tiene la curva del tiro más larga y más alta. Además lleva <b>dos rayitas</b> en el costado; el delantero, una.')}</div></div>'''))

    P.append(page(9, 'Si nunca has cosido', 'Antes de coser: lo esencial', f'''
  <div class="cards3 ess">
   <div class="card"><svg viewBox="0 0 100 40"><rect x="5" y="4" width="70" height="7" fill="#e6e6e4" stroke="#999" stroke-width=".5"/><rect x="5" y="12" width="70" height="7" fill="#b9b9b6"/><rect x="5" y="20" width="70" height="7" fill="#b9b9b6"/><rect x="5" y="28" width="70" height="7" fill="#e6e6e4" stroke="#999" stroke-width=".5"/><g font-size="5"><text x="78" y="9">revés</text><text x="78" y="17">derecho</text><text x="78" y="25">derecho</text><text x="78" y="33">revés</text></g></svg><b>Derecho con derecho</b><small>Las caras bonitas de la tela se miran: la costura queda por dentro.</small></div>
   <div class="card"><svg viewBox="0 0 100 40"><path d="M10 14 L40 14 M40 20 L18 20 M18 26 L90 26" stroke="#111" stroke-width="1.2" stroke-dasharray="3 2"/><path d="M36 11 L40 14 L36 17 M22 17 L18 20 L22 23 M86 23 L90 26 L86 29" stroke="#111" stroke-width="1" fill="none"/></svg><b>Retroceso</b><small>Cose 3 puntadas, vuelve atrás y avanza otra vez: la costura no se deshace.</small></div>
   <div class="card"><svg viewBox="0 0 100 40"><rect x="10" y="4" width="80" height="32" fill="#d9d9d6" stroke="#111" stroke-width=".6"/><path d="M10 4 L13 7 L10 10 L13 13 L10 16 L13 19 L10 22 L13 25 L10 28 L13 31 L10 34" fill="none" stroke="#111" stroke-width=".8"/><path d="M22 4 L22 36" stroke="#111" stroke-width="1" stroke-dasharray="2.5 1.5"/><text x="26" y="12" font-size="4.2" font-weight="600">1,5 cm</text></svg><b>Margen y zigzag</b><small>Cose a la distancia indicada del borde. En tela plana, remata los bordes con zigzag para que no se deshilachen.</small></div></div>
  <h4>Pequeño diccionario</h4>
  <div class="dict">{''.join(f'<div><b>{a}</b><p>{b}</p></div>' for a, b in [('Derecho y revés', 'El derecho es la cara bonita de la tela; el revés, la de dentro.'), ('Orillo', 'El borde de la tela que no se deshilacha. La flecha de hilo va paralela a él.'), ('Tiro', 'La costura curva que va de la cintura, por debajo, hasta la cintura de atrás.'), ('Entrepierna', 'La costura de dentro de cada pierna.'), ('Pernera', 'Cada pierna del pantalón, ya cerrada.'), ('Cinturilla', 'La tira de la cintura por donde pasa el elástico.')])}</div>
  <h4>Ajustes de la máquina para tela plana</h4>
  <table class="t plain kv"><tbody><tr><td><b>Aguja</b></td><td>Universal 80/12 (90/14 si la tela es gruesa)</td></tr><tr><td><b>Hilo</b></td><td>Poliéster</td></tr><tr><td><b>Puntada para coser</b></td><td>Recta, largo 2,5 (2 en la curva del tiro)</td></tr><tr><td><b>Puntada para rematar bordes</b></td><td>Zigzag, ancho 4–5 y largo 1,5–2, justo en el borde</td></tr><tr><td><b>Antes de empezar</b></td><td>Prueba siempre en un retal doble de la misma tela</td></tr></tbody></table>
  <h4>Cinco reglas de oro</h4>
  <ul class="dots"><li><b>Lee cada paso entero</b> antes de coser.</li><li><b>Plancha</b> las costuras en cada paso: la prenda quedará mucho más profesional.</li><li><b>Remata los bordes con zigzag</b> antes de unir las piezas.</li><li><b>Mide dos veces, corta una.</b> Comprueba la talla y el largo antes de cortar.</li><li>Si te equivocas, <b>descose y repite</b>. A todos nos pasa, sobre todo al principio.</li></ul>'''))

    S = [
        (1, 'Cose los bolsillos', ['Remata con zigzag los costados, la entrepierna y el tiro de las 4 piezas, y la curva de los 4 bolsillos.', 'Pon un <b>bolsillo</b> sobre el costado de un <b>delantero</b>, <b>derecho con derecho</b>: borde recto con borde recto y las rayitas juntas.', 'Cose a <b>1 cm</b> del borde todo el borde recto del bolsillo.', 'Abre el bolsillo hacia fuera y plancha la costura hacia el bolsillo.', 'Repite con el otro delantero y con los dos traseros.'], 'Si el bolsillo asoma por fuera al terminar, haz un pespunte a 0,5 cm por encima de la costura, sobre el bolsillo.'),
        (2, 'Cierra los costados', ['Pon un delantero y un trasero <b>derecho con derecho</b>, costado con costado y los bolsillos juntos hacia fuera.', 'Casa las rayitas: la del delantero con las dos del trasero, y las de la boca del bolsillo.', 'Cose a <b>1,5 cm</b> desde la cintura hasta la primera rayita de la boca, <b>gira y sigue por la curva del bolsillo</b> a 1 cm hasta la segunda rayita, y vuelve al costado hasta el bajo.', 'Haz retroceso en las dos rayitas de la boca: ahí se hace fuerza al meter la mano.', 'Plancha el costado abierto y el bolsillo hacia el delantero. Repite en la otra pierna.'], 'Mide el costado y compáralo con la tabla (pág. 5): debe coincidir con tu talla.'),
        (3, 'Cierra la entrepierna', ['Dobla cada pierna por la mitad, <b>derecho con derecho</b>, con la entrepierna del delantero sobre la del trasero.', 'Casa primero el bajo y la punta de la entrepierna y sujeta con clips.', 'Cose a <b>1,5 cm</b> del bajo hasta la punta de la entrepierna.', 'Plancha la costura abierta.', 'Ahora tienes <b>dos perneras</b>.'], 'Si una capa sobra un poco al llegar arriba, estírala con suavidad: la diferencia es pequeña y se reparte.'),
        (4, 'Une las dos perneras (tiro)', ['Da la vuelta a una pernera, con el <b>derecho por fuera</b>.', 'Métela <b>dentro</b> de la otra pernera, que sigue con el revés por fuera: así quedan <b>derecho con derecho</b>.', 'Casa las costuras de la entrepierna y la cintura de delante y de atrás.', 'Cose el tiro a <b>1,5 cm</b> en <b>una sola costura curva</b>, de la cintura delantera a la trasera, con puntada de largo 2.', 'Cose una segunda vez sobre la parte curva de abajo para reforzarla. Saca la pernera de dentro.'], 'Recorta el margen de la curva de abajo a 0,7 cm: así no tira ni hace bulto al sentarte.'),
        (5, 'Prepara y cose la cinturilla', ['Une las 2 cinturillas por los extremos cortos, <b>derecho con derecho</b>, a 1 cm. En una de las costuras deja <b>4 cm sin coser</b> en una de las dos mitades a lo largo: por ahí meterás el elástico.', 'Abre las costuras con la plancha y dobla la cinturilla a lo largo, <b>revés con revés</b>: queda de 4 cm. Plancha.', 'Pon la cinturilla sobre la cintura del pantalón, por el derecho, con los bordes juntos, las costuras en los costados y <b>la abertura hacia dentro</b>.', 'Cose a <b>1 cm</b> todo alrededor, sin estirar.', 'Remata con zigzag y plancha la cinturilla hacia arriba.'], 'La cintura del pantalón y la cinturilla miden lo mismo: si sobra o falta, revisa que las costuras de la cinturilla estén en los costados.'),
        (6, 'Mete el elástico', ['Engancha un <b>imperdible</b> en un extremo del elástico.', 'Mételo por la abertura y llévalo por dentro de la cinturilla hasta que salga por el mismo sitio. Sujeta el otro extremo con un alfiler para que no se escape.', 'Comprueba que el elástico <b>no está retorcido</b>.', 'Solapa los extremos <b>2 cm</b> y cóselos con zigzag, yendo y viniendo varias veces.', 'Cierra la abertura a máquina o a mano y reparte el frunce por toda la cintura.'], 'Para que el elástico no gire al lavar, cose una línea vertical en cada costado, atravesando la cinturilla y el elástico.'),
        (7, 'Dobladillo del bajo', ['Con la bermuda del revés, dobla <b>1 cm</b> hacia dentro el bajo de cada pierna y plancha.', 'Dobla otra vez <b>2,5 cm</b>, plancha y sujeta con clips.', 'Cose a <b>2,3 cm</b> del borde, cerca del primer doblez, dando la vuelta completa a la pierna.', 'Acaba cosiendo 2 cm encima del inicio para rematar.', 'Plancha todo el bajo con vapor.'], 'Mide los 2,5 cm en varios puntos antes de planchar: así el bajo queda recto y las dos piernas iguales.'),
    ]
    for n, ss in [(10, S[0:2]), (11, S[2:4]), (12, S[4:6])]:
        P.append(page(n, f'Pasos {ss[0][0]} y {ss[1][0]}', 'Montaje paso a paso', ''.join(step(*s) for s in ss)))
    P.append(page(13, 'Paso 7', 'Montaje paso a paso', step(*S[6]) + '''<h4>Resumen de la costura</h4>
  <table class="t plain"><thead><tr><th>Paso</th><th>Costura</th><th>Margen</th><th>Puntada</th></tr></thead><tbody>''' + ''.join(
        f'<tr><td>{a}</td><td>{b}</td><td>{c_}</td><td>{d_}</td></tr>' for a, b, c_, d_ in [
            (1, 'Bolsillos al costado', '1 cm', 'recta'), (2, 'Costados y bolsillos', '1,5 cm (1 cm en la curva)', 'recta'),
            (3, 'Entrepierna', '1,5 cm', 'recta'), (4, 'Tiro', '1,5 cm, dos veces', 'recta, largo 2'),
            (5, 'Cinturilla', '1 cm', 'recta + zigzag'), (6, 'Elástico', 'solapa 2 cm', 'zigzag'),
            (7, 'Bajo', 'doblar 1 + 2,5 · coser a 2,3', 'recta')]) + '</tbody></table>'))

    P.append(page(14, 'Última página del manual', 'Remate y revisión', f'''
  <div class="two fx"><div class="done"><img src="portada.jpg" alt=""></div><div><h4>Tu bermuda está lista</h4>
  {steps_list(['Recorta los hilos sueltos de todas las costuras.', 'Plancha toda la prenda con vapor; la cinturilla, sin aplastar el frunce.', 'Compara las medidas con la tabla (pág. 5).', 'Pruébatela y revisa la lista de abajo.'])}</div></div>
  <h4>Lista de comprobación</h4>
  <ul class="boxes">{''.join(f'<li>{t}</li>' for t in ['Los bolsillos quedan por dentro y no asoman', 'El elástico no está retorcido', 'El frunce está repartido por igual', 'Las dos piernas miden lo mismo', 'El tiro no tira al sentarte', 'Los bajos quedan rectos'])}</ul>
  <h4>Si algo sale mal</h4>
  <table class="t plain kv"><tbody>{''.join(f'<tr><td><b>{a}</b></td><td>{b}</td></tr>' for a, b in [('El bolsillo asoma por fuera', 'Plánchalo hacia el delantero y haz un pespunte a 0,5 cm sobre la costura del bolsillo.'), ('El elástico se retuerce', 'Cose una línea vertical en cada costado atravesando la cinturilla y el elástico.'), ('La cintura queda ancha o justa', 'Saca el elástico por la abertura y acórtalo o alárgalo 2–3 cm.'), ('El tiro se descose al sentarte', 'Cose la curva otra vez con puntada más corta (2) y recorta el margen a 0,7 cm.'), ('El bajo queda torcido', 'Descose, mide los 2,5 cm en varios puntos, plancha y vuelve a coser.'), ('La tela se deshilacha', 'Remata todos los bordes con zigzag antes de coser.')])}</tbody></table>
  {tip('Cuidado de la prenda', 'Lávala del revés a 30–40 °C y sécala tendida. Plancha a temperatura media; el lino, a temperatura alta y algo húmedo.')}
  <p class="sign">¿La has cosido? Nos encantará verla. HILVÁN · patrones para coser tu propia ropa.</p>'''))
    annex(P)
    return P


EXTRA = """
:root{--photo:#e7e7e7}
.coord.pk{max-width:110mm}
.ann{grid-template-columns:74mm 1fr}
.ann.sl{grid-template-columns:62mm 1fr}
.pd{max-height:100mm}
"""

if __name__ == '__main__':
    html = f'<!doctype html><html lang="es"><head><meta charset="utf-8">{FONTS}<style>{CSS}{EXTRA}</style></head><body>' + ''.join(build()) + '</body></html>'
    html = html.replace('Camiseta básica de hombre', NAME)
    with open(os.path.join(OUT, 'manual.html'), 'w') as f:
        f.write(html)
    print('ok')
