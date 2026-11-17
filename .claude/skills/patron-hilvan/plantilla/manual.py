"""Manual de la camiseta H-031 en el estilo de la web Hilván (blanco, grises y negro)."""
import os
from geo import SIZES, body, sleeve
from render2 import COL, DASH, FONTS, path, REF, canvas_size, CW, CH, TW, TH, COLS, ROWS, a4_page_ranges, SCISSORS
from shapely.geometry import LineString

OUT = os.path.join(os.path.dirname(__file__), 'build')
TOTAL = 17


def badges():
    return ''.join(f'<span class="sz" style="background:{COL[s]}">{s}</span>' for s in SIZES)


def table(rows, head=True, first='', cls=''):
    h = f'<thead><tr><th>{first}</th>' + ''.join(f'<th><span class="sz" style="background:{COL[s]}">{s}</span></th>' for s in SIZES) + '</tr></thead>' if head else ''
    b = ''.join('<tr>' + f'<td>{r[0]}</td>' + ''.join(f'<td style="color:{COL[SIZES[i]]}">{v}</td>' for i, v in enumerate(r[1:])) + '</tr>' for r in rows)
    return f'<table class="t {cls}">{h}<tbody>{b}</tbody></table>'


def page(n, eyebrow, title, content, cls=''):
    return f'''<section class="page {cls}">
  <header><span class="eb">{eyebrow}</span><h2>{title}</h2></header>
  <div class="content">{content}</div>
  <footer><span>HILVÁN · Camiseta básica de hombre · Ref. {REF} · XS–XL</span><span>{n} / {TOTAL}</span></footer>
</section>'''


def tip(label, text):
    return f'<div class="tip"><b>{label}</b><p>{text}</p></div>'


def steps_list(items):
    return '<ol class="num">' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'


# ---------- Dibujos ----------
def mirror(pts):
    return [(-x, y) for x, y in pts]


def full_body_seam(size, back=False):
    half = body(size, back)['seam']
    pts = [p for p in half if p[0] > 1e-6]
    return mirror(pts[::-1]) + pts


def piece_thumb(kind):
    if kind == 'sleeve':
        g = ''.join(f'<path d="{path(sleeve(s)["cut"])}" fill="none" stroke="{COL[s]}" stroke-width=".3"/>' for s in SIZES)
        return f'<svg viewBox="-26 -3 52 30" class="th">{g}<path d="M0 2 L0 22" stroke="#111" stroke-width=".2"/></svg>'
    back = kind == 'back'
    g = ''.join(f'<path d="{path(body(s, back)["cut"])}" fill="none" stroke="{COL[s]}" stroke-width=".5"/>' for s in SIZES)
    return f'<svg viewBox="-3 -3 40 84" class="th tall">{g}<path d="M0 {1 if back else 7} L0 78.5" stroke="#111" stroke-width="1"/></svg>'


TEE = ('M70 22 Q100 44 130 22 L170 36 L197 92 L164 106 L156 88 L156 208 L44 208 L44 88 L36 106 L3 92 L30 36 Z')
NECK = 'M70 22 Q100 44 130 22 Q100 52 70 22'


def tee_svg(extra='', fill='#e9e9e7'):
    return (f'<svg viewBox="-6 6 212 212" class="tee"><path d="{TEE}" fill="{fill}" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<path d="{NECK}" fill="#111"/><path d="M50 200 L150 200" stroke="#888" stroke-width="1" stroke-dasharray="4 3"/>{extra}</svg>')


def measure_tee():
    def lab(x, y, t):
        return f'<circle cx="{x}" cy="{y}" r="7" fill="#fff" stroke="#111" stroke-width="1.2"/><text x="{x}" y="{y+3.6}" text-anchor="middle" font-size="9.5" font-weight="600">{t}</text>'
    ln = 'stroke="#111" stroke-width="1"'
    extra = (f'<path d="M44 112 L156 112" {ln}/>' + lab(100, 112, 'A') +
             f'<path d="M168 36 L168 208" {ln}/>' + lab(168, 150, 'B') +
             f'<path d="M30 14 L170 14" {ln}/>' + lab(150, 14, 'C') +
             f'<path d="M174 30 L203 90" {ln}/>' + lab(190, 58, 'D') +
             f'<path d="M70 4 L130 4" {ln}/>' + lab(100, 4, 'E') +
             lab(180, 100, 'F') + lab(100, 34, 'H') +
             f'<path d="M44 222 L156 222" {ln}/>' + lab(100, 222, 'G'))
    return (f'<svg viewBox="-6 -8 220 240" class="tee"><path d="{TEE}" fill="#ececea" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<path d="{NECK}" fill="#111"/>{extra}</svg>')


def figure():
    return '''<svg viewBox="0 0 220 300" class="fig">
  <circle cx="80" cy="42" r="26" fill="#e6e6e4"/>
  <path d="M40 80 Q80 66 120 80 L136 96 L146 190 L132 192 L126 120 L124 290 L36 290 L34 120 L28 192 L14 190 L24 96 Z" fill="#e6e6e4"/>
  <g stroke="#111" stroke-width="1.4"><path d="M22 118 L150 118"/><path d="M30 168 L150 168"/><path d="M28 222 L150 222"/></g>
  <g font-size="11" font-weight="600"><circle cx="160" cy="118" r="8" fill="#111"/><text x="160" y="122" fill="#fff" text-anchor="middle">1</text><text x="174" y="122">Pecho</text>
  <circle cx="160" cy="168" r="8" fill="#111"/><text x="160" y="172" fill="#fff" text-anchor="middle">2</text><text x="174" y="172">Cintura</text>
  <circle cx="160" cy="222" r="8" fill="#111"/><text x="160" y="226" fill="#fff" text-anchor="middle">3</text><text x="174" y="226">Cadera</text></g></svg>'''


def cutting_layout():
    f = body('M')['cut']; b = body('M', True)['cut']; m = sleeve('M')['cut']
    W, H = 75, 170
    def tr(pts, dx, dy): return [(x + dx, y + dy) for x, y in pts]
    g = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="#f4f4f2" stroke="#bbb" stroke-width=".3"/>',
         f'<path d="M0 0 L0 {H}" stroke="#111" stroke-width="1.2"/>']
    for pts, lab, (lx, ly) in [(tr(f, 0, 2.5), 'DELANTERO', (12, 42)), (tr(b, 0, 82), 'ESPALDA', (12, 120)),
                               (tr(m, 53, 2.5), 'MANGA ×2', (53, 15))]:
        g.append(f'<path d="{path(pts)}" fill="#d9d9d6" stroke="#111" stroke-width=".35"/>')
        g.append(f'<text x="{lx}" y="{ly}" font-size="3.2" font-weight="600" text-anchor="{"middle" if lab.startswith("MANGA") else "start"}" letter-spacing=".3">{lab}</text>')
    g.append('<rect x="32" y="84" width="42" height="6" fill="#bdbdba" stroke="#111" stroke-width=".35"/>')
    g.append('<text x="53" y="88.1" font-size="2.6" font-weight="600" text-anchor="middle">TIRA DEL CUELLO</text>')
    g.append('<path d="M33 93 L73 93" stroke="#111" stroke-width=".3"/><path d="M34.5 92 L33 93 L34.5 94 M71.5 92 L73 93 L71.5 94" stroke="#111" stroke-width=".3" fill="none"/>')
    g.append('<text x="53" y="97" font-size="2.4" text-anchor="middle" fill="#555">sentido en que más estira</text>')
    g.append(f'<text x="1.6" y="{H-3}" font-size="2.6" font-weight="600" letter-spacing=".2">DOBLEZ</text>')
    return (f'<svg viewBox="-2 -8 79 185" class="lay"><text x="37.5" y="-3" font-size="2.8" text-anchor="middle" fill="#555">75 cm (tela de 150 cm doblada)</text>'
            + ''.join(g) + f'<text x="37.5" y="{H+6}" font-size="2.8" text-anchor="middle" font-weight="600">Largo de tela para la talla M: 1,7 m</text></svg>')


def tee_pieces_flat():
    fr = full_body_seam('M'); bk = full_body_seam('M', True)
    return fr, bk


def step_svg(n):
    fr, bk = tee_pieces_flat()
    if n == 1:
        bpath = path([(x + 4, y + 3) for x, y in bk])
        return (f'<svg viewBox="-34 -6 76 86" class="stp"><path d="{bpath}" fill="#e2e2df" stroke="#111" stroke-width=".4"/>'
                f'<path d="{path(fr)}" fill="#c9c9c6" stroke="#111" stroke-width=".4"/>'
                '<path d="M9 0 L23 4 M-9 0 L-23 4" stroke="#111" stroke-width="1.1" stroke-dasharray="1.2 .8"/>'
                '<text x="0" y="40" font-size="3.4" text-anchor="middle" font-weight="600">delantero</text>'
                '<text x="0" y="45" font-size="2.8" text-anchor="middle" fill="#555">(derecho arriba)</text>'
                '<text x="16" y="-2" font-size="2.6" text-anchor="middle">hombros</text></svg>')
    if n == 2:
        return ('<svg viewBox="0 0 120 92" class="stp"><rect x="14" y="8" width="92" height="12" fill="#c9c9c6" stroke="#111" stroke-width=".6"/>'
                '<text x="60" y="16.2" font-size="5" text-anchor="middle" font-weight="600">tira (talla M: 42 × 6 cm)</text>'
                '<path d="M14 26 L106 26 M17 24 L14 26 L17 28 M103 24 L106 26 L103 28" stroke="#111" stroke-width=".6" fill="none"/>'
                '<text x="60" y="32" font-size="4" text-anchor="middle" fill="#555">largo = sentido que más estira</text>'
                '<ellipse cx="60" cy="62" rx="34" ry="18" fill="none" stroke="#111" stroke-width="5"/>'
                '<ellipse cx="60" cy="62" rx="34" ry="18" fill="none" stroke="#fff" stroke-width=".6" stroke-dasharray="1.5 1.5"/>'
                + ''.join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="#fff" stroke="#111" stroke-width=".8"/>' for x, y in [(60, 44), (60, 80), (26, 62), (94, 62)])
                + '<text x="60" y="40" font-size="3.8" text-anchor="middle">costura (centro espalda)</text>'
                '<text x="60" y="88" font-size="3.8" text-anchor="middle">centro delantero</text></svg>')
    if n == 3:
        return ('<svg viewBox="0 0 120 92" class="stp"><ellipse cx="60" cy="46" rx="50" ry="34" fill="#d9d9d6"/>'
                '<ellipse cx="60" cy="46" rx="30" ry="19" fill="#fff" stroke="#111" stroke-width="4.5"/>'
                '<ellipse cx="60" cy="46" rx="30" ry="19" fill="none" stroke="#fff" stroke-width=".5" stroke-dasharray="1.5 1.5"/>'
                + ''.join(f'<g><circle cx="{x}" cy="{y}" r="3" fill="#111"/><text x="{x}" y="{y+1.3}" font-size="3.6" fill="#fff" text-anchor="middle" font-weight="600">{t}</text></g>' for x, y, t in [(60, 27, 1), (60, 65, 2), (30, 46, 3), (90, 46, 4)])
                + '<text x="60" y="44" font-size="4" text-anchor="middle" font-weight="600">tira por fuera</text>'
                '<text x="60" y="50" font-size="3.4" text-anchor="middle" fill="#555">(se estira entre marcas)</text>'
                '<text x="60" y="8" font-size="3.6" text-anchor="middle">centro espalda</text><text x="60" y="88" font-size="3.6" text-anchor="middle">centro delantero</text></svg>')
    if n == 4:
        return ('<svg viewBox="0 0 120 92" class="stp"><rect x="44" y="4" width="32" height="84" fill="#c9c9c6" stroke="#111" stroke-width=".5"/>'
                '<path d="M44 34 L14 38 L14 58 L44 62 Z M76 34 L106 38 L106 58 L76 62 Z" fill="#e2e2df" stroke="#111" stroke-width=".5"/>'
                '<path d="M44 46 L76 46" stroke="#111" stroke-width=".5" stroke-dasharray="1.5 1.2"/>'
                '<path d="M44 34 L44 62 M76 34 L76 62" stroke="#111" stroke-width="1.1" stroke-dasharray="1.4 .9"/>'
                '<circle cx="44" cy="46" r="1.6" fill="#fff" stroke="#111" stroke-width=".6"/><circle cx="76" cy="46" r="1.6" fill="#fff" stroke="#111" stroke-width=".6"/>'
                '<text x="60" y="22" font-size="4" text-anchor="middle" font-weight="600">DELANTERO</text><text x="60" y="76" font-size="4" text-anchor="middle" font-weight="600">ESPALDA</text>'
                '<text x="27" y="50" font-size="3.8" text-anchor="middle" font-weight="600">MANGA</text><text x="93" y="50" font-size="3.8" text-anchor="middle" font-weight="600">MANGA</text>'
                '<text x="88" y="28" font-size="3.2">centro de la copa</text><text x="88" y="32" font-size="3.2">= hombro</text></svg>')
    if n == 5:
        return ('<svg viewBox="0 0 120 92" class="stp"><path d="M10 8 L110 8 L110 24 L82 30 L82 84 L38 84 L38 30 L10 24 Z" fill="#c9c9c6" stroke="#111" stroke-width=".5"/>'
                '<path d="M10 8 L110 8" stroke="#111" stroke-width="1.4"/>'
                '<path d="M110 21.5 L80 27.5 L80 84 M10 21.5 L40 27.5 L40 84" fill="none" stroke="#111" stroke-width="1" stroke-dasharray="1.6 1"/>'
                '<text x="60" y="5" font-size="3.6" text-anchor="middle" font-weight="600">doblez = línea de los hombros</text>'
                '<text x="60" y="50" font-size="4" text-anchor="middle" font-weight="600">DELANTERO</text>'
                + ''.join(f'<g><circle cx="{x}" cy="{y}" r="3" fill="#fff" stroke="#111" stroke-width=".6"/><text x="{x}" y="{y+1.3}" font-size="3.4" text-anchor="middle" font-weight="600">{t}</text></g>' for x, y, t in [(112, 28, 'A'), (84, 89, 'B')])
                + '</svg>')
    if n == 6:
        return ('<svg viewBox="0 0 120 92" class="stp"><path d="M26 10 L94 10 L104 72 L16 72 Z" fill="#c9c9c6" stroke="#111" stroke-width=".5"/>'
                '<rect x="16" y="72" width="88" height="10" fill="#e2e2df" stroke="#111" stroke-width=".5"/>'
                '<path d="M17 75 L103 75 M17 78 L103 78" stroke="#111" stroke-width=".5" stroke-dasharray="1.5 1"/>'
                '<text x="60" y="40" font-size="4" text-anchor="middle" font-weight="600">MANGA (del revés)</text>'
                '<text x="60" y="90" font-size="3.4" text-anchor="middle">dobla 2,5 cm hacia dentro · cose a 2 cm del doblez</text></svg>')
    if n == 7:
        return ('<svg viewBox="0 0 120 92" class="stp"><rect x="16" y="6" width="88" height="62" fill="#c9c9c6" stroke="#111" stroke-width=".5"/>'
                '<rect x="16" y="68" width="88" height="10" fill="#e2e2df" stroke="#111" stroke-width=".5"/>'
                '<path d="M17 71 L103 71 M17 74 L103 74" stroke="#111" stroke-width=".5" stroke-dasharray="1.5 1"/>'
                '<text x="60" y="38" font-size="4" text-anchor="middle" font-weight="600">CUERPO (del revés)</text>'
                '<text x="60" y="87" font-size="3.4" text-anchor="middle">dobla 2,5 cm hacia dentro · cose a 2 cm del doblez</text></svg>')


def step(n, title, items, tipt):
    return f'''<div class="step"><div class="sh"><span class="sn">{n}</span><div><span class="eb">Paso {n}</span><h3>{title}</h3></div></div>
      <div class="sg"><div class="art">{step_svg(n)}</div>{steps_list(items)}</div>{tip("Consejo", tipt)}</div>'''


def legend_line(s, w=60):
    da = f' stroke-dasharray="{DASH[s]}"' if DASH[s] else ''
    return f'<svg viewBox="0 0 6 .6" width="{w}" height="8"><path d="M0 .3 L6 .3" stroke="#111" stroke-width=".09"{da} stroke-linecap="{"round" if s=="XS" else "butt"}"/></svg>'



def fmt(v):
    v = round(v, 1) + 0.0
    if v == 0:
        v = 0.0
    t = f'{abs(v):.1f}' if v == 0 else f'{v:.1f}'
    if t.endswith('.0'):
        t = t[:-2]
    return t.replace('.', ',')


def sample(seg, fr):
    ln = LineString(seg)
    p = ln.interpolate(fr, normalized=True)
    return (p.x, p.y)


def body_points(size, back):
    sg = body(size, back)['segs']
    pts = [('A', 'Centro del cuello (en el doblez)', sg['neck'][0])]
    for i in range(1, 5):
        pts.append((f'c{i}', 'curva del cuello', sample(sg['neck'], i / 5)))
    pts.append(('B', 'Cuello con hombro', sg['neck'][-1]))
    pts.append(('C', 'Punta del hombro', sg['shoulder'][-1]))
    for i in range(1, 7):
        pts.append((f's{i}', 'curva de la sisa', sample(sg['armhole'], i / 7)))
    pts.append(('D', 'Axila', sg['armhole'][-1]))
    pts.append(('E', 'Esquina del bajo', sg['side'][-1]))
    pts.append(('F', 'Bajo en el doblez', sg['hem'][-1]))
    return [(a, b, (x, y + 2)) for a, b, (x, y) in pts]


def sleeve_points(size):
    sg = sleeve(size)['segs']
    cap = LineString(sg['cap'])
    L = cap.length
    pts = [('A', 'Centro de la copa (en el doblez del papel)', (0.0, cap.interpolate(.5, normalized=True).y))]
    for i in range(1, 7):
        p = cap.interpolate(L / 2 + L / 2 * i / 7)
        pts.append((f's{i}', 'curva de la copa', (p.x, p.y)))
    pts.append(('B', 'Axila de la manga', sg['cap'][-1]))
    pts.append(('C', 'Boca de la manga (lado)', sg['right'][-1]))
    pts.append(('D', 'Centro de la boca (en el doblez)', (0.0, sg['right'][-1][1])))
    return [(a, b, (x, y + 1.5)) for a, b, (x, y) in pts]


def coord_table(pts_by_size):
    names = pts_by_size[SIZES[0]]
    head = ('<thead><tr><th rowspan="2">Punto</th><th rowspan="2" style="text-align:left">Dónde está</th>'
            + ''.join(f'<th colspan="2"><span class="sz" style="background:{COL[z]}">{z}</span></th>' for z in SIZES)
            + '</tr><tr>' + ''.join('<th class="xy">x</th><th class="xy">y</th>' for _ in SIZES) + '</tr></thead>')
    rows = ''
    for i, (a, b, _) in enumerate(names):
        cur = a[0] in 'cs'
        rows += f'<tr class="{"cv" if cur else ""}"><td><b>{a}</b></td><td class="w">{b}</td>'
        for z in SIZES:
            x, y = pts_by_size[z][i][2]
            rows += f'<td style="color:{COL[z]}">{fmt(x)}</td><td style="color:{COL[z]}">{fmt(y)}</td>'
        rows += '</tr>'
    return f'<table class="t coord">{head}<tbody>{rows}</tbody></table>'


def point_diagram(kind):
    c = COL['M']
    if kind == 'sleeve':
        d = sleeve('M')
        pts = sleeve_points('M')
        cut = [(x, y + 1.5) for x, y in d['cut'] if x >= -0.01]
        half = [p for p in [(x, y + 1.5) for x, y in d['cut']] if p[0] >= -1e-6]
        g = (f'<path d="M0 {pts[0][2][1]} ' + ' '.join(f'L{x:.2f} {y:.2f}' for x, y in sorted(half, key=lambda p: 0)) + '" fill="none"/>')
        outline = f'<path d="{path([(x, y + 1.5) for x, y in d["cut"]])}" fill="{c}" fill-opacity=".08" stroke="{c}" stroke-width=".35" stroke-dasharray="1 .7"/>'
        box = '-3 -3 32 32'
        fold = f'<path d="M0 0 L0 {pts[-1][2][1]}" stroke="#111" stroke-width=".7"/>'
        right = f'<path d="M{pts[-3][2][0]} {pts[-3][2][1]} L{pts[-2][2][0]} {pts[-2][2][1]} L0 {pts[-1][2][1]}" fill="none" stroke="{c}" stroke-width=".6"/>'
        curve = ''
    else:
        back = kind == 'back'
        d = body('M', back)
        pts = body_points('M', back)
        outline = f'<path d="{path([(x, y + 2) for x, y in d["cut"]])}" fill="{c}" fill-opacity=".08" stroke="{c}" stroke-width=".6"/>'
        box = '-4 -3 42 86'
        fold = f'<path d="M0 {pts[0][2][1]} L0 {pts[-1][2][1]}" stroke="#111" stroke-width="1.2"/>'
        right = curve = ''
    dots = ''
    for a, _, (x, y) in pts:
        big = a[0] not in 'cs'
        dots += f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{.55 if big else .4}" fill="{"#111" if big else c}"/>'
        dx = -1.1 if x < 1 else 1.0
        anchor = 'end' if x < 1 else 'start'
        dots += f'<text x="{x+dx:.2f}" y="{y+.6:.2f}" font-size="{1.7 if big else 1.3}" font-weight="{700 if big else 500}" text-anchor="{anchor}">{a}</text>'
    axes = ('<path d="M0 0 L8 0 M0 0 L0 8" stroke="#111" stroke-width=".3"/><path d="M7 -.6 L8 0 L7 .6 M-.6 7 L0 8 L.6 7" stroke="#111" stroke-width=".3" fill="none"/>'
            '<text x="8.6" y=".5" font-size="1.3">x</text><text x=".5" y="9.4" font-size="1.3">y</text><text x="-.6" y="-.8" font-size="1.2" text-anchor="end">(0, 0)</text>')
    return f'<svg viewBox="{box}" class="pd">{outline}{fold}{right}{axes}{dots}</svg>'


def annex_pages(P):
    howto = steps_list(['Pega folios o usa papel de patronaje o de estraza: necesitas unos <b>40 × 85 cm</b> para el delantero y la espalda, y <b>30 × 30 cm</b> para media manga.',
                        'Dibuja con regla una <b>línea vertical a la izquierda</b>: es el borde que irá en el doblez. Su punto de arriba es el <b>(0, 0)</b>.',
                        'Para cada punto de tu talla, mide <b>x hacia la derecha</b> e <b>y hacia abajo</b> desde el (0, 0) y marca un punto con el boli.',
                        'Une con regla los puntos de letra mayúscula seguidos (B–C, D–E, E–F). Los puntos <b>c</b> (cuello) y <b>s</b> (sisa) van en curva: únelos a mano con un trazo suave.',
                        'Recorta por la línea. <b>El margen de costura ya está incluido</b>: no añadas nada.'])
    for n, kind, title, extra in [(15, 'front', 'Delantero', ''), (16, 'back', 'Espalda', ''), (17, 'sleeve', 'Manga', '')]:
        if kind == 'sleeve':
            tab = coord_table({z: sleeve_points(z) for z in SIZES})
            intro = ('<p class="note"><b>Dobla el papel por la mitad</b> y dibuja la media manga con el doblez a la izquierda (x = 0). '
                     'El (0, 0) es el punto A, arriba del doblez. Une A con los puntos s1…s6 y B en curva suave, y luego B–C y C–D con regla. '
                     'Recorta con el papel doblado: al abrirlo tienes la manga entera. Marca el piquete en A.</p>')
            after = ('<h4>Tira del cuello</h4><p class="note">Es un rectángulo: dibújalo con regla directamente en la tela. '
                     'Largo × alto: <b style="color:' + COL['XS'] + '">XS 39 × 6</b> · <b style="color:' + COL['S'] + '">S 41 × 6</b> · '
                     '<b style="color:' + COL['M'] + '">M 42 × 6</b> · <b style="color:' + COL['L'] + '">L 43 × 6</b> · <b style="color:' + COL['XL'] + '">XL 44 × 6 cm</b>. '
                     'El largo va en el sentido en que más estira la tela.</p>')
        else:
            tab = coord_table({z: body_points(z, kind == 'back') for z in SIZES})
            intro = '' if kind == 'front' else '<p class="note">Igual que el delantero: solo cambia el cuello, que en la espalda es casi recto.</p>'
            after = ''
        top = (f'<div class="two fx ann"><div>{point_diagram(kind)}<p class="note c">Ejemplo: talla M</p></div><div>'
               + (f'<h4>Cómo dibujarlo</h4>{howto}' if kind == 'front' else intro) + '</div></div>')
        if kind == 'sleeve':
            top = (f'<div class="two fx ann sl"><div>{point_diagram(kind)}<p class="note c">Ejemplo: talla M (media manga)</p></div><div>{intro}</div></div>')
        P.append(page(n, 'Sin impresora · dibújalo con regla', f'{title}: puntos para dibujar', top + '<h4>Coordenadas en cm (margen incluido)</h4>' + tab + after))


# ---------- Páginas ----------
def build():
    P = []
    P.append(f'''<section class="page cover">
  <div class="cv-img"><img src="portada.jpg" alt=""></div>
  <div class="cv-txt">
    <div class="cv-top"><span class="logo">HILVÁN</span><span class="eb">Patrón PDF · Ref. {REF}</span></div>
    <h1>Camiseta básica<br>de hombre</h1>
    <p class="lead">Cuello redondo con tira y manga corta. Patrón a escala real con manual paso a paso, pensado para quien empieza a coser.</p>
    <div class="cv-row"><div><b>Principiante</b><span>Nivel</span></div><div><b>3–4 h</b><span>Tiempo</span></div><div><b>XS–XL</b><span>Tallas</span></div><div><b>Punto</b><span>Tela</span></div></div>
    <div class="cv-sizes">{badges()}</div>
  </div></section>''')

    idx = [('Materiales y herramientas', 3), ('Guía de tallas', 4), ('Medidas de la prenda terminada', 5),
           ('Cómo imprimir el patrón', 6), ('Cómo leer el patrón', 7), ('Cómo cortar la tela', 8),
           ('Antes de coser: lo esencial', 9), ('Montaje paso a paso (7 pasos)', 10), ('Remate y revisión', 14),
           ('Sin impresora: dibújalo con regla', 15)]
    P.append(page(2, 'Antes de empezar', 'Bienvenida', f'''
  <p class="intro">Con este patrón vas a coser una <b>camiseta básica de hombre con cuello redondo y manga corta</b>, desde cero. Solo necesitas <b>una máquina de coser con zigzag, la tela y el patrón impreso</b>. Cada talla tiene <b>su color y sus propias páginas</b>, a tamaño real y con el <b>margen de costura ya incluido</b>: imprimes solo tu talla, recortas por la línea de color y cortas la tela. ¿No tienes impresora? Al final del manual tienes las medidas para dibujarlo con papel, boli y regla.</p>
  <div class="cards3"><div class="card"><span class="eb">Nivel</span><b>Principiante</b><small>sin conocimientos previos</small></div>
  <div class="card"><span class="eb">Tiempo</span><b>3–4 horas</b><small>la primera vez</small></div>
  <div class="card"><span class="eb">Tallas</span><b>XS · S · M · L · XL</b><small>de hombre</small></div></div>
  <h4>Las piezas de tu camiseta</h4>
  <div class="pieces">
    <div><div class="pv">{piece_thumb('front')}</div><b>Delantero</b><small>cortar 1 al doblez</small></div>
    <div><div class="pv">{piece_thumb('back')}</div><b>Espalda</b><small>cortar 1 al doblez</small></div>
    <div><div class="pv">{piece_thumb('sleeve')}</div><b>Manga</b><small>cortar 2</small></div>
    <div><div class="pv"><svg viewBox="0 0 50 30" class="th"><rect x="3" y="12" width="44" height="6" fill="#d9d9d6" stroke="#111" stroke-width=".4"/></svg></div><b>Tira del cuello</b><small>cortar 1 · rectángulo</small></div>
  </div>
  <div class="two">
    <div><h4>Archivos que incluye</h4>
      <div class="files"><div><b>Manual</b><span>este documento · 17 páginas</span></div><div><b>Patrón A4</b><span>18 hojas por talla · imprime solo la tuya</span></div><div><b>Patrón A0</b><span>1 hoja por talla, para copistería</span></div><div><b>Patrón proyector</b><span>1 página por talla, clara y oscura</span></div></div></div>
    <div><h4>En este manual</h4><div class="toc">{''.join(f'<div><span>{a}</span><i></i><b>{b}</b></div>' for a, b in idx)}</div></div>
  </div>
  {tip('Antes de cortar la tela buena', 'Si es la primera vez que usas este patrón, haz una prueba con una tela barata y de tu talla. Así compruebas el ajuste y practicas cada paso sin miedo a equivocarte.')}'''))

    mats = [('Tela de punto para camiseta', 'Punto liso (<i>jersey</i>) de algodón con un 5 % de elastano, de 160 a 200 g/m². Ancho mínimo: 150 cm.'),
            ('Hilo de poliéster', '1 bobina del color de la tela. El poliéster aguanta mejor que el algodón cuando la costura estira.'),
            ('Agujas de punta redonda', '<i>Ballpoint</i> / jersey 80/12 (o 75/11 si la tela es muy fina). Con aguja normal se saltan puntadas.'),
            ('Aguja doble (opcional)', 'Aguja doble <i>stretch</i> de 4 mm para que los dobladillos queden como los de tienda. Sin ella, se hacen con zigzag.'),
            ('La tira del cuello', 'Sale de la <b>misma tela</b>: no hay que comprar nada más. Si prefieres canalé (<i>rib</i>), compra 0,2 m.')]
    tools = ['Máquina de coser con zigzag (no hace falta overlock)', 'Tijeras de costura o cortador rotativo con base', 'Clips de costura o alfileres',
             'Cinta métrica y regla larga (60 cm o más)', 'Patrón impreso, celo y tijeras de papel', 'Sin impresora: papel grande y regla',
             'Tiza de sastre o lápiz de tela', 'Plancha y tabla de planchar', 'Descosedor (por si te equivocas)']
    P.append(page(3, 'Prepárate', 'Materiales y herramientas', f'''
  <h4>Lo que necesitas comprar</h4>
  <div class="mats">{''.join(f'<div><span class="n">{i+1}</span><div><b>{a}</b><p>{b}</p></div></div>' for i, (a, b) in enumerate(mats))}</div>
  <h4>Herramientas</h4>
  <ul class="checks">{''.join(f'<li>{t}</li>' for t in tools)}</ul>
  <h4>Cuánta tela necesitas según tu talla</h4>
  {table([('Tela de 150 cm de ancho (m)', '1,6', '1,6', '1,7', '2', '2,1'), ('Tira del cuello: corte (largo × alto, cm)', '39 × 6', '41 × 6', '42 × 6', '43 × 6', '44 × 6'), ('Hilo (bobinas)', '1', '1', '1', '1', '1')])}
  <ul class="dots"><li><b>Prelava y seca la tela</b> igual que lavarás la camiseta: así no encoge después de coserla.</li>
  <li>Calculado para tela de 150 cm de ancho, sin dirección en el dibujo. Si tiene dibujo o pelo, añade 20 cm.</li>
  <li>La tira del cuello sale de un trozo que sobra al cortar: ya está incluida en los metros de tela.</li></ul>'''))

    P.append(page(4, 'Elige tu talla', 'Guía de tallas', f'''
  <div class="two fx"><div>{figure()}</div><div><h4>Cómo medirte</h4>
    {steps_list(['<b>Pecho:</b> rodea la parte más ancha del pecho, por debajo de las axilas, con la cinta horizontal y sin apretar.', '<b>Cintura:</b> rodea la parte más estrecha del torso, a la altura del ombligo.', '<b>Cadera:</b> rodea la parte más ancha de la cadera, con los pies juntos.'])}
    {tip('Importante', 'Mídete con ropa fina o sin ropa, de pie y relajado. Si puedes, que te ayude otra persona. <b>Elige la talla por la medida del pecho.</b>')}</div></div>
  <h4>Medidas del cuerpo (cm)</h4>
  {table([('Contorno de pecho', '84–88', '92–96', '100–104', '108–112', '116–120'), ('Contorno de cintura', '72–76', '80–84', '88–92', '96–100', '104–108'), ('Contorno de cadera', '88–92', '96–100', '104–108', '112–116', '120–124'), ('Altura aproximada', '164–170', '170–175', '175–180', '180–185', '185–190')])}
  <div class="cards3"><div class="card"><span class="eb">Ajuste</span><b>Regular</b><small>8 cm de holgura sobre el pecho: cómoda, ni ceñida ni oversize.</small></div>
  <div class="card"><span class="eb">Si dudas</span><b>Entre dos tallas</b><small>Elige la de tu pecho. ¿Más ajustada? Baja una. ¿Más holgada? Sube una.</small></div>
  <div class="card"><span class="eb">Largos</span><b>Largo y manga</b><small>El largo crece 2 cm y la manga 1 cm por talla. Alarga o acorta al cortar.</small></div></div>
  {tip('Cómo se calcula cada talla', 'Con el límite alto de cada rango de pecho (por ejemplo, la M con 104 cm) más 8 cm de holgura. Las medidas de la prenda terminada están en la página siguiente.')}'''))

    P.append(page(5, 'Tabla de medidas', 'Medidas de la prenda terminada', f'''
  <div class="two fx mtg"><div class="mt">{measure_tee()}</div><div>
  <table class="t sm"><thead><tr><th></th><th style="text-align:left">Medida (cm)</th>{''.join(f'<th><span class="sz" style="background:{COL[s]}">{s}</span></th>' for s in SIZES)}</tr></thead><tbody>
  {''.join(f'<tr><td><b>{a}</b></td><td>{b}</td>' + ''.join(f'<td>{v}</td>' for v in vals) + '</tr>' for a, b, vals in [
      ('A', 'Ancho de pecho (plano)', ['48', '52', '56', '60', '64']), ('B', 'Largo total desde el hombro', ['68', '70', '72', '74', '76']),
      ('C', 'Ancho de hombros', ['42', '44', '46', '48', '50']), ('D', 'Largo de manga', ['19', '20', '21', '22', '23']),
      ('E', 'Ancho del cuello', ['17', '17,5', '18', '18,5', '19']), ('F', 'Contorno de la boca de manga', ['31,2', '34', '36,8', '39,8', '42,8']),
      ('G', 'Ancho del bajo (plano)', ['48', '52', '56', '60', '64']), ('H', 'Alto de la tira del cuello', ['2', '2', '2', '2', '2'])])}
  </tbody></table></div></div>
  <h4>Longitud de cada costura (cm, sin margen)</h4>
  <p class="note">Úsala para comprobar tu patrón recortado: mide por la línea de costura, a 1–1,5 cm del borde.</p>
  {table([('Hombro (×2)', '13,1', '13,8', '14,6', '15,3', '16'), ('Sisa del delantero y de la espalda (cada una)', '19,2', '20,8', '22,3', '23,9', '25,5'),
          ('Copa de la manga (mitad) = igual que la sisa', '19,3', '20,8', '22,3', '23,9', '25,5'), ('Profundidad de la sisa (desde el cuello)', '22', '23', '24', '25', '26'),
          ('Altura de la copa de la manga', '7,5', '8', '8,5', '9', '9,5'), ('Ancho de la manga en la axila', '34,2', '37', '39,8', '42,8', '45,8'),
          ('Costado: de la axila al bajo', '46', '47', '48', '49', '50'), ('Bajomanga: de la boca a la axila', '11,6', '12,1', '12,6', '13,1', '13,6'),
          ('Cuello delantero / espalda (mitad)', '13 / 9,1', '13,4 / 9,3', '13,7 / 9,5', '14,1 / 9,8', '14,5 / 10'), ('Escote completo (contorno)', '44', '45,3', '46,6', '47,8', '49,1'),
          ('Bajo del cuerpo (contorno)', '96', '104', '112', '120', '128')], cls='sm')}
  <h4>Tira del cuello: rectángulo de corte (largo × alto, cm)</h4>
  {table([('Tira del cuello (cortar 1)', '39 × 6', '41 × 6', '42 × 6', '43 × 6', '44 × 6')])}
  <p class="note">El <b>largo</b> es el 85 % del escote (así el cuello queda plano y no se da de sí) e incluye 1 cm de margen en cada extremo. El alto es el doble de la tira terminada (2 cm) más los márgenes. El largo va en el sentido en que más estira la tela. Con canalé, corta al 80 % del escote; con telas que estiran poco, al 90 %.</p>'''))

    grid = ''.join(f'<rect x="{c*TW}" y="{r*TH}" width="{TW}" height="{TH}" fill="none" stroke="#111" stroke-width=".3"/>'
                   f'<text x="{c*TW+TW/2}" y="{r*TH+TH/2+1.8}" font-size="5" font-weight="700" text-anchor="middle" fill="#111" fill-opacity=".45">{"ABC"[c]}{r+1}</text>'
                   f'<text x="{c*TW+TW/2}" y="{r*TH+TH/2+5.6}" font-size="2.4" font-weight="600" text-anchor="middle" fill="#111" fill-opacity=".5">hoja {c*ROWS+r+1}</text>'
                   for r in range(ROWS) for c in range(COLS))
    mapsvg = f'<svg viewBox="0 0 {CW} {CH}" class="map">{canvas_size("M", lw=.2)}{grid}</svg>'
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
  </div><div><h4>Mapa del A4 (3 × 6 hojas)</h4>{mapsvg}<p class="note">Ejemplo con la talla M. Todas las tallas usan el mismo mapa.</p></div></div>"""))

    def symrow(svg, txt):
        return f'<div class="sym"><svg viewBox="0 0 60 16" width="64" height="17">{svg}</svg><span>{txt}</span></div>'
    c = COL['M']
    syms = (symrow(f'<path d="M3 8 L57 8" stroke="{c}" stroke-width="3.2" stroke-linecap="round"/>', '<b>Línea gruesa de color: recorta por aquí.</b> Es la línea de corte de tu talla.') +
            symrow(f'<defs>{SCISSORS}</defs><use href="#sc" x="20" y="0" width="16" height="16" style="color:{c}"/>', '<b>Tijeras:</b> te recuerdan que ese borde se corta.') +
            symrow('<path d="M3 8 L57 8" stroke="#111" stroke-width="4"/>', '<b>Borde negro: NO se corta.</b> Se coloca justo en el doblez de la tela. Al abrir la tela, la pieza sale entera.') +
            symrow('<path d="M3 8 L57 8" stroke="#888" stroke-width="1" stroke-dasharray="3 2.5"/>', '<b>Puntos grises: línea de costura.</b> Te enseña por dónde coserás. No se corta.') +
            symrow('<path d="M6 8 L54 8 M10 5 L6 8 L10 11 M50 5 L54 8 L50 11" stroke="#111" stroke-width="1.1" fill="none"/>', '<b>Flecha de hilo:</b> colócala paralela al doblez de la tela.') +
            symrow('<path d="M10 13 L50 13" stroke="#888" stroke-width="1" stroke-dasharray="3 2"/><path d="M30 13 L30 3" stroke="#111" stroke-width="2.6"/>', '<b>Piquete:</b> marca de encaje. En la manga señala el centro, que se une con el hombro.'))
    demo = body('M')
    segs = demo['segs']
    dpath = ''.join(f'<path d="{path(segs[k], False)}" fill="none" stroke="{c}" stroke-width="1.1" stroke-linecap="round"/>' for k in ['neck', 'shoulder', 'armhole', 'side', 'hem'])
    demo_svg = (f'<svg viewBox="-6 -4 44 84" class="demo"><path d="{path(demo["cut"])}" fill="{c}" fill-opacity=".1"/>'
                f'<path d="{path(demo["seam"], False)}" fill="none" stroke="#888" stroke-width=".35" stroke-dasharray="1 .8"/>{dpath}'
                f'<path d="{path(segs["fold"], False)}" stroke="#111" stroke-width="1.6"/>'
                f'<text x="-1.6" y="40" font-size="2.4" font-weight="700" text-anchor="middle" transform="rotate(-90 -1.6 40)">DOBLEZ · NO CORTAR</text>'
                f'<text x="5" y="22" font-size="3.6" font-weight="700" font-family="Archivo" font-stretch="125%">DELANTERO</text>'
                f'<rect x="5" y="24" width="12" height="3.4" rx="1.7" fill="{c}"/><text x="11" y="26.4" font-size="1.9" font-weight="700" fill="#fff" text-anchor="middle">TALLA M</text>'
                f'<text x="33" y="50" font-size="2.2" font-weight="700" fill="{c}" transform="rotate(90 33 50)">✂ RECORTA POR LA LÍNEA</text></svg>')
    P.append(page(7, 'Símbolos', 'Cómo leer el patrón', f"""
  <div class="two fx sy7"><div><h4>Así es una pieza de tu patrón</h4>{demo_svg}</div>
  <div><h4>Qué significa cada línea</h4><div class="syms">{syms}</div></div></div>
  <h4>El margen de costura ya está incluido</h4>
  <table class="t plain"><thead><tr><th>Pieza</th><th>Cose a</th><th>Dónde</th></tr></thead><tbody>
  <tr><td><b>Delantero y espalda</b></td><td>1,5 cm</td><td>hombros, sisas y costados</td></tr><tr><td></td><td>1 cm</td><td>escote (cuello)</td></tr>
  <tr><td></td><td>2,5 cm</td><td>bajo: se dobla para hacer el dobladillo</td></tr><tr><td><b>Manga</b></td><td>1,5 cm</td><td>copa y bajomanga</td></tr>
  <tr><td></td><td>2,5 cm</td><td>boca de la manga: se dobla para el dobladillo</td></tr><tr><td><b>Tira del cuello</b></td><td>1 cm</td><td>extremos y borde que se une al escote</td></tr></tbody></table>
  <h4>Piezas y cantidad</h4>
  <table class="t plain"><thead><tr><th>Pieza</th><th>N.º</th><th>Cómo cortarla</th></tr></thead><tbody>
  <tr><td><b>Delantero</b></td><td>1</td><td>borde negro sobre el doblez de la tela</td></tr><tr><td><b>Espalda</b></td><td>1</td><td>borde negro sobre el doblez de la tela</td></tr>
  <tr><td><b>Manga</b></td><td>2</td><td>con la tela doblada: cortas las dos capas a la vez</td></tr><tr><td><b>Tira del cuello</b></td><td>1</td><td>rectángulo · el largo en el sentido que más estira</td></tr></tbody></table>"""))

    P.append(page(8, 'Corte', 'Cómo cortar la tela', f'''
  <div class="two fx"><div>{cutting_layout()}<p class="note c">Dibujo para la talla M. En las tallas L y XL coloca las mangas debajo de la espalda si no caben junto al delantero.</p></div><div>
  <h4>Prepara la tela</h4>
  <ul class="dots"><li>Plancha la tela y dóblala por la mitad a lo largo, <b>derecho con derecho</b> y con los orillos juntos.</li><li>Recorta el patrón por la <b>línea gruesa de color</b>. <b>No añadas margen</b>: ya está incluido.</li></ul>
  <h4>Corta las piezas</h4>
  {steps_list(['<b>Delantero y espalda:</b> el <b>borde negro</b> del patrón justo sobre el doblez de la tela; la flecha de hilo, paralela al doblez.', '<b>Mangas:</b> la pieza entera sobre las dos capas: salen las dos mangas.', '<b>Tira del cuello:</b> coloca el rectángulo del patrón con el largo en el sentido en que más estira la tela y córtalo.', '<b>Marca con tiza</b> el piquete del centro de la copa de cada manga y el centro del delantero y de la espalda en el escote.'])}
  {tip('Truco', 'Fija cada pieza con pesas o clips y corta con tijeras bien afiladas, <b>sin levantar ni estirar la tela</b>: el punto se deforma con facilidad.')}</div></div>'''))

    P.append(page(9, 'Si nunca has cosido', 'Antes de coser: lo esencial', f'''
  <div class="cards3 ess">
   <div class="card"><svg viewBox="0 0 100 40"><rect x="5" y="4" width="70" height="7" fill="#e6e6e4" stroke="#999" stroke-width=".5"/><rect x="5" y="12" width="70" height="7" fill="#b9b9b6"/><rect x="5" y="20" width="70" height="7" fill="#b9b9b6"/><rect x="5" y="28" width="70" height="7" fill="#e6e6e4" stroke="#999" stroke-width=".5"/><g font-size="5"><text x="78" y="9">revés</text><text x="78" y="17">derecho</text><text x="78" y="25">derecho</text><text x="78" y="33">revés</text></g></svg><b>Derecho con derecho</b><small>Las caras bonitas de la tela se miran: la costura queda por dentro.</small></div>
   <div class="card"><svg viewBox="0 0 100 40"><path d="M10 14 L40 14 M40 20 L18 20 M18 26 L90 26" stroke="#111" stroke-width="1.2" stroke-dasharray="3 2"/><path d="M36 11 L40 14 L36 17 M22 17 L18 20 L22 23 M86 23 L90 26 L86 29" stroke="#111" stroke-width="1" fill="none"/></svg><b>Retroceso</b><small>Cose 3 puntadas, vuelve atrás y avanza otra vez: la costura no se deshace.</small></div>
   <div class="card"><svg viewBox="0 0 100 40"><rect x="10" y="4" width="80" height="32" fill="#d9d9d6" stroke="#111" stroke-width=".6"/><path d="M22 4 L22 36" stroke="#111" stroke-width="1" stroke-dasharray="2.5 1.5"/><path d="M10 10 L22 10" stroke="#111" stroke-width=".6"/><text x="12" y="8.5" font-size="4.2" font-weight="600">1,5</text></svg><b>Margen de costura</b><small>Cose siempre a la distancia indicada del borde. Usa las guías de la placa de tu máquina.</small></div></div>
  <h4>Pequeño diccionario</h4>
  <div class="dict">{''.join(f'<div><b>{a}</b><p>{b}</p></div>' for a, b in [('Derecho', 'La cara bonita de la tela, la que se ve por fuera.'), ('Revés', 'La cara de dentro de la tela.'), ('Hilo de la tela', 'Dirección de los hilos. Las flechas del patrón van paralelas al doblez.'), ('Punto (jersey)', 'La tela de las camisetas: estira mucho de lado a lado y poco de arriba abajo.'), ('Clips', 'Sujetan las capas antes de coser; en tela de punto son mejores que los alfileres.'), ('Dobladillo', 'Borde doblado hacia dentro y cosido: el bajo de la camiseta y de las mangas.')])}</div>
  <h4>Ajustes de la máquina para tela de punto</h4>
  <table class="t plain kv"><tbody><tr><td><b>Aguja</b></td><td>Punta redonda (ballpoint) 80/12</td></tr><tr><td><b>Hilo</b></td><td>Poliéster</td></tr><tr><td><b>Puntada</b></td><td>Zigzag estrecho: ancho 1–1,5 y largo 2,5–3 (o puntada elástica)</td></tr><tr><td><b>Presión del prensatelas</b></td><td>Ligera, si tu máquina lo permite</td></tr><tr><td><b>Antes de empezar</b></td><td>Prueba siempre en un retal doble de la misma tela</td></tr></tbody></table>
  <h4>Cinco reglas de oro</h4>
  <ul class="dots"><li><b>Lee cada paso entero</b> antes de coser.</li><li><b>Plancha</b> las costuras en cada paso: la prenda quedará mucho más profesional.</li><li><b>No tires de la tela</b> mientras coses: deja que la máquina la lleve.</li><li><b>Mide dos veces, corta una.</b> Comprueba la talla en la tabla antes de cortar.</li><li>Si te equivocas, <b>descose y repite</b>. A todos nos pasa, sobre todo al principio.</li></ul>'''))

    S = [
        (1, 'Une los hombros', ['Pon el <b>delantero</b> sobre la mesa con el derecho hacia arriba.', 'Coloca la <b>espalda</b> encima, con el derecho hacia abajo (<b>derecho con derecho</b>). Alinea hombros y cuello.', 'Sujeta cada hombro con clips.', 'Cose los dos hombros a <b>1,5 cm</b> del borde, del cuello hacia la manga, con retroceso al empezar y al acabar.', 'Plancha los márgenes hacia la espalda.'], 'Usa zigzag estrecho (ancho 1, largo 2,5) en todas las costuras: así estiran con la tela y no se rompen.'),
        (2, 'Prepara la tira del cuello', ['Corta la tira con la medida de tu talla (pág. 5). El <b>largo</b> va en el sentido en que más estira la tela.', 'Dobla la tira por la mitad uniendo los <b>extremos cortos</b>, derecho con derecho, y cose a <b>1 cm</b>: queda un aro.', 'Abre esa costura con los dedos y dobla el aro por la mitad a lo largo, <b>con el revés dentro</b>: queda una tira de 3 cm con los dos bordes juntos.', 'Marca <b>4 puntos iguales</b> con clips: la costura (será el centro de la espalda), el lado contrario y los dos puntos de en medio.'], 'La tira es más corta que el escote a propósito: así el cuello queda plano, pegado al cuerpo, y no se da de sí.'),
        (3, 'Cose la tira al cuello', ['Marca también <b>4 puntos</b> en el escote: dobla el cuello por el centro del delantero y de la espalda, y luego otra vez por la mitad.', 'Con la camiseta del derecho, pon la tira por fuera, con los bordes juntos sobre el borde del escote y su costura en el <b>centro de la espalda</b>.', 'Casa las 4 marcas de la tira con las 4 del escote y sujeta con clips.', 'Cose a <b>1 cm</b> con zigzag <b>estirando solo la tira</b> (no el escote) para que llegue de marca a marca.', 'Dobla el margen hacia el cuerpo y plancha con vapor. Si quieres, pespuntea a 0,5 cm por fuera.'], 'Cose con la tira hacia arriba para ver cuánto la estiras. Ve despacio y para con la aguja abajo en cada marca.'),
        (4, 'Cose las mangas', ['Extiende el cuerpo plano, con el derecho hacia arriba: delantero arriba y espalda abajo, unidos por los hombros.', 'Coloca una manga encima, <b>derecho con derecho</b>, con su copa curva sobre la sisa curva.', 'Casa el <b>piquete del centro de la copa</b> con la costura del hombro y fija con clips hacia los extremos.', 'Cose a <b>1,5 cm</b> con retroceso. No hace falta estirar: copa y sisa miden lo mismo.', 'Repite con la otra manga y plancha los márgenes hacia la manga.'], 'Si al llegar al final sobra tela en un lado, la manga no está centrada: suelta los clips y vuelve a casar el centro con el hombro.'),
        (5, 'Cierra costados y mangas', ['Dobla la camiseta por la línea de los hombros, <b>derecho con derecho</b>, con las mangas extendidas.', 'Casa las costuras de las axilas y sujétalas con un clip. Luego casa el borde de la manga y el bajo.', 'Cose en <b>una sola costura</b> a 1,5 cm: del borde de la manga (A), pasando por debajo del brazo, hasta el bajo del cuerpo (B).', 'Cruza la axila despacio. Puedes reforzarla con una segunda pasada.', 'Repite en el otro lado y plancha los márgenes hacia la espalda.'], 'Mide la costura de la manga y la del costado y compáralas con la tabla (pág. 5): deben coincidir con tu talla.'),
        (6, 'Dobladillo de las mangas', ['Con la camiseta del revés, dobla <b>2,5 cm</b> hacia dentro el borde de cada manga.', 'Plancha el doblez y sujétalo con clips.', 'Da la vuelta a la camiseta (del derecho) y cose a <b>2 cm</b> del borde doblado, dando la vuelta completa a la manga.', '<b>Con aguja doble</b> salen dos líneas rectas por fuera; <b>sin aguja doble</b>, usa zigzag estrecho.', 'Acaba cosiendo 2 cm encima del inicio para rematar.'], 'Mete la manga en el brazo libre de la máquina (quita la mesita de la base) para coserla en redondo más fácil.'),
        (7, 'Dobladillo del bajo', ['Con la camiseta del revés, dobla <b>2,5 cm</b> hacia dentro todo el bajo y plancha.', 'Sujeta con clips cada 10 cm, empezando por las costuras de los costados.', 'Del derecho, cose a <b>2 cm</b> del borde doblado, empezando en un costado y dando la vuelta completa.', 'Acaba cosiendo 2 cm encima del inicio para rematar.', 'Plancha todo el bajo con vapor.'], 'Si el bajo ondula, sube el largo de puntada a 3 y baja la presión del prensatelas. No tires de la tela.'),
    ]
    for i, pg in enumerate([(10, S[0:2]), (11, S[2:4]), (12, S[4:6])]):
        n, ss = pg
        P.append(page(n, f'Pasos {ss[0][0]} y {ss[1][0]}', 'Montaje paso a paso', ''.join(step(*s) for s in ss)))
    P.append(page(13, 'Paso 7', 'Montaje paso a paso', step(*S[6]) + '''<h4>Resumen de la costura</h4>
  <table class="t plain"><thead><tr><th>Paso</th><th>Costura</th><th>Margen</th><th>Puntada</th></tr></thead><tbody>''' + ''.join(
        f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in [
            (1, 'Hombros', '1,5 cm', 'zigzag estrecho'), (2, 'Aro de la tira', '1 cm', 'recta o zigzag'), (3, 'Tira al escote', '1 cm', 'zigzag, estirando la tira'),
            (4, 'Mangas a la sisa', '1,5 cm', 'zigzag estrecho'), (5, 'Costados y bajomangas', '1,5 cm', 'zigzag estrecho'),
            (6, 'Dobladillo de mangas', 'doblar 2,5 · coser a 2', 'aguja doble o zigzag'), (7, 'Dobladillo del bajo', 'doblar 2,5 · coser a 2', 'aguja doble o zigzag')]) + '</tbody></table>'))

    P.append(page(14, 'Última página del manual', 'Remate y revisión', f'''
  <div class="two fx"><div class="done"><img src="portada.jpg" alt=""></div><div><h4>Tu camiseta está lista</h4>
  {steps_list(['Recorta los hilos sueltos de todas las costuras.', 'Plancha toda la prenda con vapor, sin aplastar el cuello.', 'Compara las medidas con la tabla (pág. 5).', 'Pruébatela y revisa la lista de abajo.'])}</div></div>
  <h4>Lista de comprobación</h4>
  <ul class="boxes">{''.join(f'<li>{t}</li>' for t in ['El cuello queda plano y no hace ondas', 'Los costados caen rectos', 'Los hombros quedan planos y sin arrugas', 'Los dobladillos no ondulan', 'Las dos mangas miden lo mismo', 'Ninguna costura cruje al estirar'])}</ul>
  <h4>Si algo sale mal</h4>
  <table class="t plain kv"><tbody>{''.join(f'<tr><td><b>{a}</b></td><td>{b}</td></tr>' for a, b in [('El cuello hace ondas', 'La tira quedó larga o no la estiraste: descose, acorta la tira 2 cm y vuelve a coserla.'), ('El cuello se da de sí', 'Estiraste también el escote: estira solo la tira y cose con ella hacia arriba.'), ('Se saltan puntadas', 'Cambia la aguja por una nueva de punta redonda 80/12.'), ('Las costuras se rompen al estirar', 'Usa zigzag estrecho o puntada elástica, nunca recta sola.'), ('El dobladillo hace un túnel', 'Con aguja doble, baja un poco la tensión del hilo de arriba o usa zigzag.'), ('No me encaja la manga', 'Compara sisa y copa con la tabla y revisa que el piquete de la manga coincida con el hombro.')])}</tbody></table>
  {tip('Cuidado de la prenda', 'Lávala del revés a 30 °C, sin lejía, y sécala en plano o a baja temperatura. Plancha a temperatura media.')}
  <p class="sign">¿La has cosido? Nos encantará verla. HILVÁN · patrones para coser tu propia ropa.</p>'''))
    annex_pages(P)
    return P


CSS = """
@page{size:210mm 297mm;margin:0}
:root{--photo:#e3e3e3}
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#fff}
body{font-family:Inter,Arial,sans-serif;color:#111;font-size:8.6pt;line-height:1.45;-webkit-print-color-adjust:exact;print-color-adjust:exact}
b{font-weight:600}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;padding:15mm 15mm 16mm}
.page:last-child{page-break-after:auto}
header{border-bottom:1px solid #111;padding-bottom:3.2mm;margin-bottom:5mm}
.eb{display:block;font-size:6.6pt;letter-spacing:.14em;text-transform:uppercase;color:#6a6a68}
h2{font-family:Archivo;font-stretch:112%;font-weight:500;font-size:19pt;letter-spacing:-.015em;margin-top:1mm}
h3{font-family:Archivo;font-stretch:108%;font-weight:500;font-size:13pt}
h4{font-family:Archivo;font-stretch:110%;font-weight:600;font-size:9.6pt;margin:5mm 0 2.4mm;letter-spacing:.01em}
.content > h4:first-child{margin-top:0}
footer{position:absolute;left:15mm;right:15mm;bottom:8mm;display:flex;justify-content:space-between;font-size:6.6pt;color:#777;border-top:1px solid #e2e2e0;padding-top:2mm}
.intro{font-size:9.6pt;line-height:1.55;max-width:170mm}
.note{color:#555;font-size:8pt;margin:1.6mm 0}
.note.c{text-align:center}
.sz{display:inline-block;min-width:9mm;padding:.6mm 1.6mm;border-radius:99px;background:#111;color:#fff;font-size:6.6pt;font-weight:600;text-align:center;letter-spacing:.04em}
.t{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums;margin-top:1mm}
.t th{background:#f1f1ef;padding:1.8mm 2mm;font-weight:600;font-size:7.4pt;text-align:center;border-bottom:1px solid #111}
.t th:first-child{text-align:left}
.t td{padding:1.7mm 2mm;border-bottom:1px solid #e3e3e1;text-align:center}
.t td:first-child{text-align:left}
.t.sm td{padding:1.25mm 2mm;font-size:7.9pt}
.t.plain td,.t.plain th{text-align:left}
.t.kv td:first-child{width:52mm}
.tip{border:1px solid #111;padding:3mm 4mm;margin-top:4.5mm}
.tip > b{display:block;font-size:6.6pt;letter-spacing:.14em;text-transform:uppercase;margin-bottom:1mm}
.tip p{font-size:8.4pt}
.cards3{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin-top:4.5mm}
.card{background:#f4f4f2;padding:3.6mm 4mm;display:grid;gap:.8mm;align-content:start}
.card b{font-family:Archivo;font-stretch:110%;font-weight:500;font-size:12pt}
.card small{font-size:7.6pt;color:#555}
.cards3.ess .card svg{width:100%;height:16mm;margin-bottom:1.5mm}
.pieces{display:grid;grid-template-columns:repeat(4,1fr);gap:4mm}
.pieces > div{display:grid;justify-items:center;text-align:center;gap:.5mm}
.pv{background:#f4f4f2;width:100%;height:38mm;display:grid;place-items:center;padding:3mm;margin-bottom:1.5mm}
.th{width:100%;height:100%}
.pieces small{color:#666;font-size:7.2pt}
.two{display:grid;grid-template-columns:1fr 1fr;gap:8mm;margin-top:1mm}
.two.fx{align-items:start}
.files{display:grid;gap:0;border-top:1px solid #111}
.files div{display:flex;justify-content:space-between;gap:3mm;padding:1.8mm 0;border-bottom:1px solid #e3e3e1}
.files span{color:#666}
.toc div{display:flex;align-items:baseline;gap:2mm;padding:1.05mm 0}
.toc i{flex:1;border-bottom:1px dotted #aaa}
.mats{display:grid;gap:2.2mm}
.mats > div{display:grid;grid-template-columns:7mm 1fr;gap:2mm;align-items:start;background:#f4f4f2;padding:2.6mm 3.4mm}
.n{width:5.4mm;height:5.4mm;border-radius:50%;background:#111;color:#fff;font-size:7pt;font-weight:600;display:grid;place-items:center}
.mats p{color:#555;font-size:8pt}
.checks{list-style:none;columns:2;column-gap:8mm}
.checks li{padding:1mm 0 1mm 5mm;position:relative;break-inside:avoid}
.checks li::before{content:"";position:absolute;left:0;top:2.2mm;width:2.4mm;height:1.2mm;border-left:1.3px solid #111;border-bottom:1.3px solid #111;transform:rotate(-45deg)}
.dots{list-style:none;margin-top:2.5mm;display:grid;gap:1.4mm}
.dots li{padding-left:4.4mm;position:relative}
.dots li::before{content:"";position:absolute;left:.4mm;top:1.8mm;width:1.5mm;height:1.5mm;background:#111;border-radius:50%}
ol.num{list-style:none;counter-reset:n;display:grid;gap:2mm}
ol.num li{counter-increment:n;position:relative;padding-left:7.5mm}
ol.num li::before{content:counter(n);position:absolute;left:0;top:-.2mm;width:5mm;height:5mm;border-radius:50%;background:#111;color:#fff;font-size:6.8pt;font-weight:600;display:grid;place-items:center}
.fig{width:100%;max-height:70mm}
.tee{width:100%;max-height:72mm}
.mt .tee{max-height:62mm}
.mtg{grid-template-columns:52mm 1fr;gap:6mm}
.mtg .t td:nth-child(2){text-align:left;white-space:nowrap}
.mt text{font-family:Inter}
.map{width:100%;max-height:118mm;display:block}
.test{display:flex;align-items:center;gap:4mm;margin-top:3mm}
.test svg{flex:none}
.test p{font-size:7.8pt;color:#444}
.syms{display:grid;gap:2mm}
.sym{display:grid;grid-template-columns:20mm 1fr;align-items:center;gap:3mm}
.lay{width:100%;max-height:205mm}
.dict{display:grid;grid-template-columns:1fr 1fr;gap:2.4mm}
.dict div{border:1px solid #deded c;padding:2.4mm 3.2mm;border:1px solid #dcdcda}
.dict p{color:#555;font-size:8pt}
.step{margin-bottom:6mm}
.sh{display:flex;gap:3.6mm;align-items:center;margin-bottom:3mm}
.sn{width:9mm;height:9mm;border-radius:50%;background:#111;color:#fff;font-family:Archivo;font-weight:600;font-size:12pt;display:grid;place-items:center}
.sg{display:grid;grid-template-columns:80mm 1fr;gap:7mm;align-items:start}
.art{background:#f4f4f2;padding:4mm;height:64mm;display:grid;place-items:center}
.stp{width:100%;height:100%}
.stp text{font-family:Inter}
.boxes{list-style:none;columns:2;column-gap:8mm}
.boxes li{padding:1.2mm 0 1.2mm 6mm;position:relative;break-inside:avoid}
.boxes li::before{content:"";position:absolute;left:0;top:1.5mm;width:3.2mm;height:3.2mm;border:1.2px solid #111;border-radius:.6mm}
.done{background:var(--photo);height:62mm;display:grid;place-items:center;overflow:hidden}
.done img{height:100%;width:100%;object-fit:contain}
.sign{margin-top:6mm;font-size:8pt;color:#666;text-align:center}
.fmt .card b{font-size:15pt}
.pr6 td,.pr6 th{text-align:left}
.sy7{grid-template-columns:62mm 1fr}
.demo{width:100%;max-height:92mm}
.sym{grid-template-columns:24mm 1fr}
.coord{font-size:7.2pt}
.coord th{padding:1.2mm .8mm;font-size:6.6pt}
.coord th.xy{background:#fafaf9;font-weight:500;color:#666;border-bottom:1px solid #ccc}
.coord td{padding:1.05mm .8mm}
.coord td.w{text-align:left;color:#666;font-size:6.8pt}
.coord tr.cv td:first-child{color:#666}
.ann{grid-template-columns:52mm 1fr;margin-bottom:1mm}
.ann.sl{grid-template-columns:62mm 1fr}
.pd{width:100%;max-height:92mm}
.ann ol.num{gap:1.4mm;font-size:8.2pt}

/* portada */
.cover{padding:0}
.cv-img{height:190mm;background:var(--photo);overflow:hidden;display:grid;place-items:center}
.cv-img img{width:100%;height:100%;object-fit:contain}
.cv-txt{padding:10mm 15mm 0}
.cv-top{display:flex;justify-content:space-between;align-items:baseline}
.logo{font-family:Archivo;font-stretch:125%;font-weight:600;font-size:13pt;letter-spacing:.34em}
.cover h1{font-family:Archivo;font-stretch:112%;font-weight:400;font-size:30pt;line-height:1.02;letter-spacing:-.02em;margin-top:6mm}
.lead{font-size:10pt;color:#444;max-width:140mm;margin-top:3.5mm}
.cv-row{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid #111;margin-top:6mm}
.cv-row div{padding:2.6mm 0;display:grid}
.cv-row b{font-family:Archivo;font-stretch:110%;font-weight:500;font-size:12pt}
.cv-row span{font-size:6.8pt;letter-spacing:.12em;text-transform:uppercase;color:#777}
.cv-sizes{display:flex;gap:2mm;margin-top:3mm}
"""

if __name__ == '__main__':
    html = f'<!doctype html><html lang="es"><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head><body>' + ''.join(build()) + '</body></html>'
    with open(os.path.join(OUT, 'manual.html'), 'w') as f:
        f.write(html)
    print('ok')
