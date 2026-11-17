"""
Manual + patrón de la CAMISETA básica de hombre (cuello redondo, manga corta), XS–XL.
Mismo formato que la sudadera con capucha. Uso:  python3 camiseta.py
"""
import math, os
from plantilla import *
from camiseta_geo import *

R = todo()
M = 'M'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'salida', 'camiseta_patron_1-5_XS-XL.pdf')
os.makedirs(os.path.dirname(OUT), exist_ok=True)
PIE = 'Camiseta de hombre · Patrón y manual · XS–XL'
doc = Manual(OUT, 'Camiseta básica de hombre · Patrón 1:5 y manual de costura (XS–XL)',
             'Patrón PDF a escala 1:5 con cuadrícula, coordenadas y manual de costura paso a paso',
             PIE, 'Patrón de camiseta básica')
V = lambda f: [f(t) for t in TALLAS]          # valores por talla
med = lambda pieza, k: V(lambda t: R[t][pieza][2][k])

# ---------------------------------------------------------------- tela necesaria (tela de 150 cm doblada = 75 cm)
def tela_m(t):
    q, W = CUARTO[t], R[t]['man'][2]['ancho']
    largo_cuerpo = LARGO[t] + MARGEN_CUELLO + DOBLADILLO
    cabe_manga = (q + MARGEN) + (2 * W + 2 * MARGEN) + 2 <= 75
    total = 2 * largo_cuerpo + (0 if cabe_manga else LARGO_MANGA[t] + MARGEN + DOBLADILLO + 2) + 8 + 5
    return math.ceil(total / 10) / 10

TELA = V(tela_m)

# ---------------------------------------------------------------- dibujos de la camiseta
def camiseta_dibujo(c, cx, cy, s, cuerpo=ACC, manga=ACC_D, tira=RIB, costuras=white, sombra=None):
    """Camiseta de frente. Unidades locales: hombros en y=0, ancho de pecho 256."""
    P = lambda pts: [(cx + x * s, cy + y * s) for x, y in pts]
    for k in (1, -1):
        sl = [(k * 116, 16), (k * 205, 92), (k * 168, 140), (k * 128, 112)]
        poligono(c, P(sl), fill=manga)
        poligono(c, P([(k * 205, 92), (k * 212, 100), (k * 175, 148), (k * 168, 140)]), fill=tira if tira else manga)
    body = [(-40, -6)] + [(-40 + 80 * i / 20, -6 + 30 * math.sin(math.pi * i / 20)) for i in range(21)] + \
           [(40, -6), (116, 16), (128, 112), (128, 330), (-128, 330), (-128, 112), (-116, 16)]
    poligono(c, P(body), fill=cuerpo)
    neck = [(-40 + 80 * i / 20, -6 + 30 * math.sin(math.pi * i / 20)) for i in range(21)]
    c.setLineWidth(9 * s); c.setStrokeColor(tira); c.setLineCap(1)
    p = c.beginPath(); pts = P(neck); p.moveTo(pts[0][0], Y(pts[0][1]))
    for x, y in pts[1:]: p.lineTo(x, Y(y))
    c.drawPath(p, stroke=1, fill=0)
    if costuras:
        for k in (1, -1):
            poligono(c, P([(k * 42, 2), (k * 112, 22)]), stroke=costuras, lw=1, dash=[3, 2], cerrado=False)
            poligono(c, P([(k * 113, 26), (k * 122, 108)]), stroke=costuras, lw=1, dash=[3, 2], cerrado=False)
        poligono(c, P([(-122, 318), (122, 318)]), stroke=costuras, lw=1, dash=[3, 2], cerrado=False)


def pieza_completa(contorno):
    """Pieza a doblez -> pieza entera (espejo)."""
    der = contorno
    izq = [(-x, y) for x, y in reversed(contorno)]
    return der + izq


def dibujar_pieza(c, pts, ox, oy, s, fill=ACC_L, stroke=INK, lw=0.8):
    poligono(c, [(ox + x * s, oy + y * s) for x, y in pts], fill=fill, stroke=stroke, lw=lw)


# ======================================================================= PÁGINAS
@doc.pagina('portada')
def portada(c):
    c.setFillColor(INK); c.rect(0, 0, PW, PH, fill=1, stroke=0)
    c.setFillColor(COVER_C1); c.circle(PW + 10, Y(150), 260, fill=1, stroke=0)
    c.setFillColor(COVER_C2); c.circle(-30, Y(650), 150, fill=1, stroke=0)
    texto(c, 57, 68, 'PATRÓN EN PDF  ·  ESCALA 1:5  ·  A4', 'PM', 7.2, PINK, spacing=0.3)
    c.setFillColor(ACC); c.rect(57, Y(91), 62, 3, fill=1, stroke=0)
    texto(c, 55, 170, 'CAMISETA', 'PB', 50, white)
    texto(c, 57, 246, 'MANGA CORTA', 'PB', 36, ACC)
    parrafo(c, 57, 274, 360, 'Patrón para trazar con cuadrícula y manual paso a paso, pensado para quien nunca ha cosido. Tallas de hombre XS a XL.',
            12, white, 19, 'PL')
    camiseta_dibujo(c, PW / 2, 372, 0.84, ACC, ACC_D, RIB, white)
    texto(c, PW / 2, 685, 'TALLAS DE HOMBRE', 'PB', 6.5, PINK, 'center')
    for i, t in enumerate(TALLAS):
        pastilla(c, PW / 2 + (i - 2) * 48, 706, t, 40, 20)
    c.setFillColor(ACC); c.rect(0, 0, PW, Y(745), fill=1, stroke=0)
    for i, (n, s) in enumerate([('1:5', 'Patrones con cuadrícula'), ('7', 'Pasos ilustrados'), ('5', 'Tallas, XS a XL')]):
        x = PW / 6 * (2 * i + 1)
        texto(c, x, 790, n, 'PB', 20, white, 'center')
        texto(c, x, 810, s, 'PM', 7, white, 'center')
        if i: linea(c, PW / 3 * i, 762, PW / 3 * i, 818, PINK, 0.5)
    texto(c, PW / 2, 832, 'Cuello redondo con tira · manga corta · dobladillos sin overlock', 'P', 6.2, PINK, 'center')


@doc.pagina('bienvenida')
def bienvenida(c):
    cabecera(c, 'Antes de empezar', 'Bienvenida')
    y = 86
    y += parrafo(c, ML, y, CW, 'Con este manual vas a hacer una <b>camiseta básica de hombre con cuello redondo y manga corta</b>, '
                 'desde cero y sin experiencia previa. Solo necesitas <b>una máquina de coser, papel y tela</b>. Incluye las '
                 '<b>5 tallas (XS, S, M, L y XL)</b>. Cada pieza del patrón aparece <b>entera en una hoja, a escala 1:5</b>, con una '
                 'cuadrícula, los centímetros de cada costura y una tabla de coordenadas para <b>trazarla a tamaño real</b> en tu papel.',
                 10.2, INK, 15) + 16
    w = (CW - 2 * 10) / 3
    for i, (e, t, s) in enumerate([('Nivel', 'Principiante', 'sin conocimientos previos'),
                                   ('Tiempo', '3 – 4 horas', 'la primera vez (con el patrón)'),
                                   ('Tallas', 'XS · S · M · L · XL', 'de hombre')]):
        tarjeta(c, ML + i * (w + 10), y, w, 62, e, t, s)
    y = seccion(c, y + 80, 'Las piezas de tu camiseta')
    piezas = [('Delantero', 'x1'), ('Espalda', 'x1'), ('Manga', 'x2'), ('Tira del cuello', 'x1')]
    pw = (CW - 3 * 8) / 4
    fd = pieza_completa(R[M]['del_'][0]); fe = pieza_completa(R[M]['esp'][0]); fm = pieza_completa(R[M]['man'][0])
    for i, (n, q) in enumerate(piezas):
        x = ML + i * (pw + 8)
        rrect(c, x, y, pw, 92, 9, fill=CREAM)
        cx = x + pw / 2
        if i == 0: dibujar_pieza(c, fd, cx, y + 10, 0.85)
        if i == 1: dibujar_pieza(c, fe, cx, y + 10, 0.85, ACC_M)
        if i == 2: dibujar_pieza(c, fm, cx, y + 18, 1.9)
        if i == 3:
            rrect(c, cx - 45, y + 32, 90, 14, 2, fill=ACC_D); linea(c, cx - 43, y + 39, cx + 43, y + 39, white, 0.6, [2, 1.5])
        if i in (0, 1): linea(c, cx, y + 10, cx, y + 10 + LARGO[M] * .85, INK, 0.5, [2, 2])
        texto(c, cx, y + 84, n, 'PS', 8, INK, 'center')
        texto(c, cx, y + 104, q, 'P', 6.5, MUTED, 'center')
    y = seccion(c, y + 124, 'Qué encontrarás en este PDF')
    toc = [('Materiales y herramientas', 'materiales'), ('Guía de tallas: cómo medirte y elegir talla', 'tallas'),
           ('Medidas de la prenda terminada y de cada costura', 'medidas'), ('Cómo pasar el patrón a tu papel (escala 1:5 a 1:1)', 'copiar'),
           ('Cómo leer los dibujos y márgenes de costura', 'simbolos'), ('Cómo cortar la tela', 'cortar'),
           ('Antes de coser: lo esencial', 'esencial'), ('Paso a paso de la costura (7 pasos)', 'pasos'),
           ('Patrón: delantero (dibujo + coordenadas)', 'p_del'), ('Patrón: espalda', 'p_esp'),
           ('Patrón: manga', 'p_man'), ('Tira del cuello (rectángulo)', 'p_tira')]
    for s, a in toc:
        texto(c, ML, y + 4, s, 'P', 8.8, INK)
        n = str(doc.num(a)); x1 = ML + ancho(s, 'P', 8.8) + 6; x2 = PW - ML - ancho(n, 'PB', 8.8) - 6
        linea(c, x1, y + 3, x2, y + 3, GRID, 0.5, [0.6, 1.8])
        texto(c, PW - ML, y + 4, n, 'PB', 8.8, ACC_D, 'right')
        y += 16
    consejo(c, y + 18, 'Consejo antes de vender o regalar',
            'Si es la primera vez que usas este patrón, haz una prueba con una tela barata y de tu talla antes de cortar la tela buena. '
            'Así compruebas el ajuste y practicas cada paso sin miedo a equivocarte.')


@doc.pagina('materiales')
def materiales(c):
    cabecera(c, 'Prepárate', 'Materiales y herramientas')
    y = seccion(c, 70, 'Lo que necesitas comprar')
    items = [('Tela de punto para camiseta', 'Punto liso (<i>jersey</i>) de algodón con un 5 % de elastano, de 160 a 200 g/m². Ancho mínimo: 150 cm.'),
             ('Hilo de poliéster', '1 bobina del color de la tela. El poliéster aguanta mejor que el algodón cuando la costura estira.'),
             ('Agujas de punta redonda', '<i>Ballpoint</i> / jersey 80/12 (o 75/11 si la tela es muy fina). Con aguja normal se saltan puntadas.'),
             ('Aguja doble (opcional)', 'Aguja doble <i>stretch</i> de 4 mm para que los dobladillos queden como los de tienda. Sin ella, se hacen con zigzag.'),
             ('La tira del cuello', 'Sale de la <b>misma tela</b>: no hay que comprar nada más. Si prefieres canalé (<i>rib</i>), compra 0,2 m.')]
    for i, (t, s) in enumerate(items, 1):
        rrect(c, ML, y, CW, 41, 9, fill=CREAM)
        circulo_num(c, ML + 15, y + 21, i, 7, size=7.5)
        texto(c, ML + 32, y + 16, t, 'PS', 9, INK)
        parrafo(c, ML + 32, y + 20, CW - 44, s, 7.8, MUTED)
        y += 46
    y = seccion(c, y + 8, 'Herramientas')
    h1 = ['Máquina de coser con zigzag (no hace falta overlock)', 'Tijeras de costura o cortador rotativo con base', 'Clips de costura o alfileres',
          'Cinta métrica y regla larga (60 cm o más)', 'Escuadra o cartabón']
    h2 = ['Papel de patronaje, de estraza o folios pegados', 'Lápiz, goma y tiza de sastre', 'Plancha y tabla de planchar', 'Descosedor (por si te equivocas)']
    for i, s in enumerate(h1): check(c, ML + 2, y + i * 17, s)
    for i, s in enumerate(h2): check(c, ML + CW / 2 + 2, y + i * 17, s)
    y = seccion(c, y + 5 * 17 + 14, 'Cuánto necesitas según tu talla')
    y = tabla_tallas(c, y, [('Tela de 150 cm de ancho (m)', TELA),
                            ('Tira del cuello: corte (largo x alto, cm)', V(lambda t: f"{R[t]['tira'][0]} x {R[t]['tira'][1]}")),
                            ('Hilo (bobinas)', ['1'] * 5)], primera=CW * 0.4)
    vinetas(c, ML, y + 14, CW, [
        '<b>Prelava y seca la tela</b> igual que lavarás la camiseta: así no encoge después de coserla.',
        'Calculado para tela de 150 cm de ancho, sin dirección en el dibujo. Si tiene dibujo o pelo, añade 20 cm.',
        'La tira del cuello sale de un trozo que sobra al cortar: ya está incluida en los metros de tela.'])


@doc.pagina('tallas')
def tallas(c):
    cabecera(c, 'Elige tu talla', 'Guía de tallas')
    # silueta
    x0, y0 = ML + 5, 66
    c.setFillColor(HexColor('#EFE6D8'))
    c.circle(x0 + 75, Y(y0 + 30), 26, fill=1, stroke=0)
    poligono(c, [(x0 + 62, y0 + 50), (x0 + 88, y0 + 50), (x0 + 92, y0 + 66), (x0 + 135, y0 + 80), (x0 + 145, y0 + 190), (x0 + 132, y0 + 192),
                 (x0 + 125, y0 + 120), (x0 + 122, y0 + 225), (x0 + 28, y0 + 225), (x0 + 25, y0 + 120), (x0 + 18, y0 + 192), (x0 + 5, y0 + 190),
                 (x0 + 15, y0 + 80), (x0 + 58, y0 + 66)], fill=HexColor('#EFE6D8'))
    for i, (n, yy) in enumerate([('Pecho', y0 + 102), ('Cintura', y0 + 150), ('Cadera', y0 + 200)], 1):
        linea(c, x0 + (12 if i == 1 else 26), yy, x0 + 160, yy, ACC, 1.4)
        circulo_num(c, x0 + 167, yy, i, 6.5)
        texto(c, x0 + 178, yy + 3, n, 'P', 8, INK)
    xr = ML + 245
    y = seccion(c, 70, 'Cómo medirte', xr)
    y = lista_numerada(c, xr, y, CW - 245, [
        '<b>Pecho:</b> rodea la parte más ancha del pecho, por debajo de las axilas, con la cinta horizontal y sin apretar.',
        '<b>Cintura:</b> rodea la parte más estrecha del torso, a la altura del ombligo.',
        '<b>Cadera:</b> rodea la parte más ancha de la cadera, con los pies juntos.'], 8.6, 9)
    consejo(c, y + 4, 'Importante', 'Mídete con ropa fina o sin ropa, de pie y relajado. Si puedes, que te ayude otra persona. '
            '<b>Elige la talla por la medida del pecho.</b>', xr, CW - 245)
    y = seccion(c, 306, 'Medidas del cuerpo (cm)')
    y = tabla_tallas(c, y, [('Contorno de pecho', V(lambda t: f'{PECHO[t][0]}–{PECHO[t][1]}')),
                            ('Contorno de cintura', V(lambda t: f'{CINTURA[t][0]}–{CINTURA[t][1]}')),
                            ('Contorno de cadera', V(lambda t: f'{CADERA[t][0]}–{CADERA[t][1]}')),
                            ('Altura aproximada', V(lambda t: ALTURA[t]))], fila_h=22)
    y += 18
    w = (CW - 20) / 3
    for i, (e, t, s) in enumerate([('Ajuste', 'Regular', 'El patrón da 8 cm de holgura sobre el pecho: camiseta cómoda, ni ceñida ni oversize.'),
                                   ('Si dudas', 'Entre dos tallas', 'Elige la que corresponda a tu pecho. ¿Más ajustada? Baja una. ¿Más holgada? Sube una.'),
                                   ('Largos', 'Largo y manga', 'El largo crece 2 cm y la manga 1 cm por talla. Alarga o acorta al cortar si lo necesitas.')]):
        tarjeta(c, ML + i * (w + 10), y, w, 92, e, t, s, tsize=12.5)
    consejo(c, y + 108, 'Cómo se calcula cada talla',
            'Las tallas están calculadas con el límite alto de cada rango de pecho (por ejemplo, la M con 104 cm) más 8 cm de holgura. '
            'Las medidas de la prenda terminada están en la página siguiente.')


@doc.pagina('medidas')
def medidas(c):
    cabecera(c, 'Tabla de medidas', 'Medidas de la prenda terminada')
    # dibujo con letras
    cx, cy, s = ML + 96, 112, 0.36
    camiseta_dibujo(c, cx, cy, s, ACC_L, ACC_M, RIB, None)
    P = lambda x, y: (cx + x * s, cy + y * s)
    def cota(x1, y1, x2, y2, L, lx, ly):
        flecha(c, *P(x1, y1), *P(x2, y2), INK, 0.6, 3, dos=True); letra(c, *P(lx, ly), L, 5.5)
    cota(-128, 125, 128, 125, 'A', 40, 125); cota(70, 4, 70, 330, 'B', 70, 250)
    cota(-116, -24, 116, -24, 'C', 0, -24); cota(118, 6, 207, 84, 'D', 175, 40)
    cota(-40, -18, 40, -18, 'E', -70, -36); cota(170, 150, 214, 104, 'F', 205, 140)
    cota(-128, 348, 128, 348, 'G', 0, 348)
    letra(c, *P(-52, 18), 'H', 5.5)
    filas = [('A', 'Ancho de pecho (plano)', V(lambda t: ANCHO_PLANO[t])),
             ('B', 'Largo total (desde el hombro)', V(lambda t: LARGO[t])),
             ('C', 'Ancho de hombros', V(lambda t: HOMBROS[t])),
             ('D', 'Largo de manga', V(lambda t: LARGO_MANGA[t])),
             ('E', 'Ancho del cuello', V(lambda t: 2 * CUELLO_MEDIO[t])),
             ('F', 'Boca de la manga (contorno)', V(lambda t: 2 * R[t]['man'][2]['boca'])),
             ('G', 'Ancho del bajo (plano)', V(lambda t: ANCHO_PLANO[t])),
             ('H', 'Alto de la tira del cuello', [TIRA_ALTO_FINAL] * 5)]
    x0 = ML + 205; w = CW - 205
    rrect(c, x0, 82, w, 20, 6, fill=INK)
    texto(c, x0 + 10, 95, 'Medida', 'PS', 7.6, white)
    cw = (w - 150) / 5
    for i, t in enumerate(TALLAS): pastilla(c, x0 + 150 + cw * (i + .5), 92, t)
    yy = 102
    for k, (L_, d, v) in enumerate(filas):
        if k % 2: c.setFillColor(CREAM); c.rect(x0, Y(yy + 19.5), w, 19.5, fill=1, stroke=0)
        texto(c, x0 + 9, yy + 12.5, L_, 'PS', 7.6, INK); texto(c, x0 + 84, yy + 12.5, d, 'P', 7.6, INK, 'center')
        for i, val in enumerate(v): texto(c, x0 + 150 + cw * (i + .5), yy + 12.5, fmt(val), 'P', 7.8, INK, 'center')
        yy += 19.5
    linea(c, x0, yy, x0 + w, yy, GRID, 0.6)
    y = seccion(c, 282, 'Longitud de cada costura (cm, sin margen)')
    y = tabla_tallas(c, y, [
        ('Hombro (x2)', med('del_', 'hombro')),
        ('Sisa curva del delantero y de la espalda (cada una)', med('del_', 'sisa')),
        ('Copa curva de la manga (mitad) = igual que la sisa', med('man', 'copa')),
        ('Profundidad de la sisa (desde el cuello)', V(lambda t: SISA[t])),
        ('Altura de la copa de la manga', V(lambda t: ALTURA_COPA[t])),
        ('Ancho de la manga en la axila', V(lambda t: 2 * R[t]['man'][2]['ancho'])),
        ('Costado: de la axila al bajo', med('del_', 'costado')),
        ('Bajomanga: de la boca a la axila', med('man', 'bajomanga')),
        ('Cuello delantero / espalda (mitad)', V(lambda t: f"{fmt(R[t]['del_'][2]['cuello'])} / {fmt(R[t]['esp'][2]['cuello'])}")),
        ('Escote completo (contorno)', V(lambda t: R[t]['escote'])),
        ('Bajo del cuerpo (contorno)', V(lambda t: 4 * CUARTO[t])),
    ], primera=CW * 0.45, fila_h=18.5, size=7.9)
    y = seccion(c, y + 16, 'Tira del cuello: rectángulo de corte (largo x alto, cm)')
    y = tabla_tallas(c, y, [('Tira del cuello (cortar 1)', V(lambda t: f"{R[t]['tira'][0]} x {R[t]['tira'][1]}"))], primera=CW * 0.45)
    parrafo(c, ML, y + 10, CW, 'El <b>largo</b> es el 85 % del escote (así el cuello queda plano y no se da de sí) e incluye 1 cm de margen '
            'en cada extremo; el alto es el doble de la tira terminada (2 cm) más los márgenes. El largo va en el sentido en que más estira la tela.',
            7.8, MUTED)


@doc.pagina('copiar')
def copiar(c):
    cabecera(c, 'Escala 1:5 a 1:1', 'Cómo pasar el patrón a tu papel')
    y = 84 + parrafo(c, ML, 84, CW, 'Cada pieza está dibujada <b>entera en una hoja, a escala 1:5</b>: 1 cm del dibujo son 5 cm de tela. En tu papel '
                     'de patronaje la vas a trazar a <b>tamaño real</b> con regla. Tienes dos métodos; el primero es el más exacto y el segundo, el más visual.',
                     9.6, INK, 14.5) + 16
    w = (CW - 14) / 2
    for i, (e, t, pasos) in enumerate([
        ('El más exacto', 'Método A · Por coordenadas', [
            'En la hoja de <b>puntos de trazado</b> de cada pieza, busca la columna de tu talla (colores).',
            'Marca la esquina superior izquierda de tu papel como <b>(0, 0)</b>. Mide <b>x</b> hacia la derecha e <b>y</b> hacia abajo.',
            'Marca cada punto con un lápiz y une los puntos con regla. Las curvas (cuello, sisa y copa) se unen con una línea suave.',
            'Comprueba cada costura con la cinta: debe coincidir con la cifra de color.']),
        ('El más visual', 'Método B · Por cuadrícula', [
            'Dibuja en tu papel cuadros de <b>10 x 10 cm</b> (los mismos que ves en el dibujo).',
            'Fíjate en qué cuadro empieza y acaba la línea de tu talla y márcalo en tu papel, <b>cuadro a cuadro</b>.',
            'Usa las <b>letras (A, B, C…)</b> y los números en cm de cada costura para comprobar medidas.',
            'Une con regla y repasa a mano las curvas.'])]):
        x = ML + i * (w + 14)
        rrect(c, x, y, w, 196, 10, fill=CREAM)
        texto(c, x + 14, y + 20, e.upper(), 'PB', 6.3, ACC_D)
        texto(c, x + 14, y + 36, t, 'PS', 10, INK)
        lista_numerada(c, x + 14, y + 48, w - 26, pasos, 7.9, 5)
    y = seccion(c, y + 212, 'Así se copia con la cuadrícula')
    texto(c, ML, y + 4, 'DIBUJO DEL PDF (1:5)', 'PB', 6.3, ACC_D)
    gx, gy, q = ML + 8, y + 12, 17
    for i in range(5): linea(c, gx + i * q, gy, gx + i * q, gy + 3 * q, GRID, .5)
    for j in range(4): linea(c, gx, gy + j * q, gx + 4 * q, gy + j * q, GRID, .5)
    c.setFillColor(PINK); c.rect(gx + q, Y(gy + 2 * q), q, q, fill=1, stroke=0)
    curva = [(0.3, 2.8), (1.2, 1.0), (2.2, 0.6), (3.3, 1.4), (3.6, 2.9)]
    poligono(c, [(gx + a * q, gy + b * q) for a, b in curva], stroke=ACC_D, lw=1.3, cerrado=False)
    texto(c, gx + 4 * q + 12, gy + 20, 'cuadro = 10 cm reales', 'P', 7, INK)
    texto(c, gx + 4 * q + 12, gy + 30, '(2 cm en el dibujo)', 'P', 7, MUTED)
    flecha(c, ML + 255, gy + 72, ML + 255, gy + 92, ACC_D, 0.9, 4)
    texto(c, ML + 265, gy + 84, 'copia cuadro a cuadro', 'PB', 7, ACC_D)
    gx2, gy2, Q = ML + 128, gy + 112, 62
    texto(c, gx2 + 4 * Q, gy2 - 8, 'TU PAPEL (1:1)', 'PB', 6.3, ACC_D, 'right')
    flecha(c, gx2, gy2 - 8, gx2 + Q, gy2 - 8, INK, .6, 3, dos=True); texto(c, gx2 + Q / 2, gy2 - 12, '10 cm', 'PB', 6.5, INK, 'center')
    c.setFillColor(PINK); c.rect(gx2 + Q, Y(gy2 + 2 * Q), Q, Q, fill=1, stroke=0)
    for i in range(5): linea(c, gx2 + i * Q, gy2, gx2 + i * Q, gy2 + 3 * Q, GRID, .7)
    for j in range(4): linea(c, gx2, gy2 + j * Q, gx2 + 4 * Q, gy2 + j * Q, GRID, .7)
    poligono(c, [(gx2 + a * Q, gy2 + b * Q) for a, b in curva], stroke=ACC_D, lw=2, cerrado=False)
    texto(c, gx2, gy2 + 3 * Q + 12, 'cuadro marcado: 10 x 10 cm dibujado con regla', 'PB', 6.5, ACC_D)
    consejo(c, gy2 + 3 * Q + 26, 'Antes de trazar',
            'Usa papel de al menos <b>40 x 80 cm</b> para el delantero y la espalda (varias hojas pegadas sirven). Dibuja siempre la '
            '<b>línea de costura</b>; el <b>margen</b> se añade al final con una paralela (pág. ' + str(doc.num('simbolos')) + '). '
            'En las piezas con doblez dibuja solo la mitad.')


@doc.pagina('simbolos')
def simbolos(c):
    cabecera(c, 'Símbolos y márgenes', 'Cómo leer los dibujos')
    y = seccion(c, 70, 'Símbolos')
    for t in TALLAS:
        linea(c, ML, y + 4, ML + 40, y + 4, TALLA_COLOR[t], 1.3, TALLA_DASH[t])
        texto(c, ML + 50, y + 7, f'Línea de costura de la talla {t}', 'P', 8.3, TALLA_COLOR[t])
        y += 17
    y += 6
    sim = [('doblez', 'DOBLEZ: borde sobre el doblez de la tela (sin margen de costura)'),
           ('hilo', 'HILO: la flecha va paralela al doblez o al orillo de la tela'),
           ('letra', 'LETRA en un círculo (A, B, C…): punto de la tabla de coordenadas'),
           ('caja', 'CAJA CON 5 NÚMEROS: longitud en cm de esa costura, de XS a XL, en los colores de cada talla'),
           ('flecha', 'FLECHA DOBLE en la tira: sentido en que más estira la tela')]
    for k, s in sim:
        if k == 'doblez': c.setFillColor(INK); c.rect(ML + 9, Y(y + 12), 3.5, 13, fill=1, stroke=0)
        if k == 'hilo': flecha(c, ML + 11, y, ML + 11, y + 13, INK, .7, 3, dos=True)
        if k == 'letra': letra(c, ML + 11, y + 6, 'A', 6)
        if k == 'caja': rrect(c, ML + 1, y, 20, 12, 3, stroke=GRID, lw=.6); texto(c, ML + 11, y + 8.5, '14,6', 'PB', 5, TALLA_COLOR['XS'], 'center')
        if k == 'flecha': flecha(c, ML + 1, y + 6, ML + 21, y + 6, ACC_D, .8, 3, dos=True)
        texto(c, ML + 32, y + 9, s, 'P', 8, INK)
        y += 20
    y = seccion(c, y + 8, 'Margen de costura (se añade hacia fuera de la línea)')
    y = tabla(c, y, ['Pieza', 'Margen', 'Dónde'], [
        ['Delantero y espalda', '1,5 cm', 'hombros, sisas y costados'],
        ['', '1 cm', 'escote (cuello)'],
        ['', '2,5 cm', 'bajo (dobladillo) · en el doblez: 0'],
        ['Manga', '1,5 cm', 'copa y bajomanga'],
        ['', '2,5 cm', 'boca de la manga (dobladillo) · en el doblez: 0'],
        ['Tira del cuello', '1 cm', 'ya incluido en la medida de corte del rectángulo']],
        [120, 70, CW - 190], alinear=['left', 'center', 'center'], col0_bold=True)
    y = seccion(c, y + 16, 'Piezas y cantidad')
    y = tabla(c, y, ['Pieza', 'N.º', 'Tela y forma de cortarla'], [
        ['Delantero', '1', 'mitad del patrón sobre el doblez de la tela'],
        ['Espalda', '1', 'mitad del patrón sobre el doblez de la tela'],
        ['Manga', '2', 'pieza entera, tela doblada (salen las dos)'],
        ['Tira del cuello', '1', 'rectángulo · el largo en el sentido que más estira']],
        [120, 50, CW - 170], alinear=['left', 'center', 'center'], col0_bold=True)
    consejo(c, y + 16, 'La línea de tu talla', 'Las 5 tallas están dibujadas juntas, una dentro de otra. Antes de trazar, '
            '<b>resalta con un rotulador de su color la línea de tu talla</b> para no confundirte.')


@doc.pagina('cortar')
def cortar(c):
    cabecera(c, 'Corte', 'Cómo cortar la tela')
    # plano de corte (talla M) en una franja de 75 cm (tela de 150 doblada)
    x0, y0, s = ML + 12, 96, 3.0
    W75, L = 75 * s * .98, 222 * s * .98
    sc = 0.98 * s
    texto(c, x0 + W75 / 2 + 6, y0 - 4, '75 cm (tela de 150 doblada)', 'P', 6.5, MUTED, 'center')
    Lf = TELA[2] * 100 * 2.95
    rrect(c, x0 - 4, y0, W75 + 20, Lf + 16, 10, fill=white, stroke=GRID_L, lw=.8)
    rrect(c, x0 + 6, y0 + 8, W75, Lf, 2, fill=HexColor('#FBF8F2'))
    linea(c, x0 + 6, y0 + 8, x0 + 6, y0 + 8 + Lf, INK, 2)
    texto(c, x0 + 6 + W75 / 2, y0 + Lf + 30, f'largo de tela para la talla M: {fmt(TELA[2])} m', 'PB', 6.5, MUTED, 'center')
    fd, pd, _ = R[M]['del_']; fe, pe, _ = R[M]['esp']; fm, pm, mm = R[M]['man']
    k = 2.95
    oy = y0 + 14
    dibujar_pieza(c, fd, x0 + 6, oy + 4, k, ACC_L, INK, .6)
    texto(c, x0 + 6 + 14 * k, oy + 40 * k, 'DELANTERO', 'PB', 6.5, white, 'center')
    oy2 = oy + (LARGO[M] + 4) * k
    dibujar_pieza(c, fe, x0 + 6, oy2, k, ACC_M, INK, .6)
    texto(c, x0 + 6 + 14 * k, oy2 + 40 * k, 'ESPALDA', 'PB', 6.5, white, 'center')
    full = pieza_completa(fm)
    mx = x0 + 6 + (CUARTO[M] + 4) * k + mm['ancho'] * k
    dibujar_pieza(c, full, mx, oy + 4, k, ACC, INK, .6)
    texto(c, mx, oy + 4 + 14 * k, 'MANGAS x2', 'PB', 6.5, white, 'center')
    texto(c, mx, oy + 4 + 18 * k, '(2 capas)', 'PB', 6.5, white, 'center')
    ty = oy2 + (LARGO[M] + 4) * k
    rrect(c, x0 + 6 + 2 * k, ty, R[M]['tira'][0] * k * .5 * 0 + 42 * k, 6 * k, 1, fill=ACC_D)
    texto(c, x0 + 6 + 2 * k + 21 * k, ty + 3 * k + 2.5, 'TIRA DEL CUELLO', 'PB', 6, white, 'center')
    flecha(c, x0 + 6 + 2 * k, ty + 6 * k + 6, x0 + 6 + 44 * k, ty + 6 * k + 6, ACC_D, .6, 3, dos=True)
    texto(c, x0 + 6 + 23 * k, ty + 6 * k + 16, 'sentido en que más estira', 'P', 5.8, ACC_D, 'center')
    xr = ML + 265; wr = CW - 265
    y = seccion(c, 70, 'Prepara tu patrón y la tela', xr)
    y = vinetas(c, xr, y, wr, ['Traza cada pieza en papel y <b>recórtala con su margen</b> (1,5 cm; 1 cm en el escote; 2,5 cm en los bajos).',
                               'Plancha la tela y dóblala por la mitad a lo largo, <b>derecho con derecho</b> y con los orillos juntos.'], 8.4, 4)
    y = seccion(c, y + 6, 'Corta las piezas', xr)
    y = lista_numerada(c, xr, y, wr, [
        '<b>Delantero y espalda:</b> la mitad del patrón con el borde DOBLEZ sobre el doblez de la tela; la flecha de hilo, paralela al doblez.',
        '<b>Mangas:</b> la pieza entera abierta sobre las dos capas: salen las dos mangas.',
        '<b>Tira del cuello:</b> dibuja con regla el rectángulo de tu talla (pág. ' + str(doc.num('p_tira')) + ') con el largo en el sentido en que más estira la tela, y córtala.',
        '<b>Marca con tiza</b> el centro de la copa de cada manga (punto A) y el centro del delantero y de la espalda en el escote.'], 8.4, 6)
    parrafo(c, xr, y + 2, wr, 'Dibujo para la talla M. En las tallas L y XL las mangas no caben junto al delantero: colócalas debajo de la espalda.', 7, MUTED)
    consejo(c, y + 40, 'Truco', 'Fija cada pieza con pesas o clips y corta con tijeras bien afiladas, <b>sin levantar ni estirar la tela</b>: '
            'el punto se deforma con facilidad.', xr, wr)


@doc.pagina('esencial')
def esencial(c):
    cabecera(c, 'Si nunca has cosido', 'Antes de coser: lo esencial')
    y = 82; w = (CW - 20) / 3
    for i, (t, s) in enumerate([('Derecho con derecho', 'Las caras bonitas de la tela se miran: la costura queda por dentro.'),
                                ('Retroceso', 'Cose 3 puntadas, vuelve atrás y avanza otra vez: la costura no se deshace.'),
                                ('Margen de costura', 'Cose siempre a la distancia indicada del borde: es la distancia entre el borde y la costura.')]):
        x = ML + i * (w + 10)
        rrect(c, x, y, w, 132, 10, fill=CREAM)
        if i == 0:
            for j, (col, lab) in enumerate([(GREY, 'revés'), (ACC_L, 'derecho'), (ACC_L, 'derecho'), (GREY, 'revés')]):
                c.setFillColor(col); c.rect(x + 12, Y(y + 34 + j * 9 + 8), 90, 8, fill=1, stroke=0)
                texto(c, x + 108, y + 41 + j * 9, lab, 'PM' if j in (1, 2) else 'P', 6, ACC_D if j in (1, 2) else MUTED)
            c.setStrokeColor(INK); c.setLineWidth(.6); c.rect(x + 12, Y(y + 70), 90, 36, fill=0, stroke=1)
            texto(c, x + w / 2, y + 88, 'DERECHO CON DERECHO', 'PB', 6, INK, 'center')
        if i == 1:
            for j, (a, b, col) in enumerate([(14, 46, ACC), (46, 20, INK), (20, 140, ACC)]):
                flecha(c, x + a, y + 38 + j * 6, x + b, y + 38 + j * 6, col, 1, 3)
                texto(c, x + 8, y + 40 + j * 6, str(j + 1), 'PB', 5.5, ACC_D)
            linea(c, x + 14, y + 44, x + 150, y + 44, MUTED, .4, [2, 2])
            texto(c, x + w / 2, y + 88, 'RETROCESO al empezar y al acabar', 'PB', 6, INK, 'center')
        if i == 2:
            c.setFillColor(ACC_L); c.setStrokeColor(INK); c.setLineWidth(.6); c.rect(x + 14, Y(y + 76), 132, 56, fill=1, stroke=1)
            linea(c, x + 32, y + 20, x + 32, y + 80, ACC_D, 1.3, [3, 2])
            flecha(c, x + 14, y + 34, x + 32, y + 34, INK, .6, 2.5, dos=True)
            texto(c, x + 22, y + 30, '1,5 cm', 'PB', 5.8, INK, 'center')
            texto(c, x + 92, y + 56, 'cose por la línea', 'P', 6, white, 'center'); texto(c, x + 92, y + 64, 'discontinua', 'P', 6, white, 'center')
            texto(c, x + w / 2, y + 88, 'MARGEN DE COSTURA', 'PB', 6, INK, 'center')
        texto(c, x + 12, y + 106, t, 'PS', 9, INK)
        parrafo(c, x + 12, y + 110, w - 22, s, 7.4, MUTED, 9.8)
    y = seccion(c, y + 148, 'Pequeño diccionario')
    dic = [('Derecho', 'La cara bonita de la tela, la que se ve por fuera.'), ('Revés', 'La cara de dentro de la tela.'),
           ('Hilo de la tela', 'Dirección de los hilos. Las flechas del patrón van paralelas al doblez.'),
           ('Punto (jersey)', 'La tela de las camisetas: estira mucho de lado a lado y poco de arriba abajo.'),
           ('Clips', 'Sujetan las capas antes de coser; en tela de punto son mejores que los alfileres.'),
           ('Dobladillo', 'Borde doblado hacia dentro y cosido: el bajo de la camiseta y de las mangas.')]
    w2 = (CW - 12) / 2
    for i, (t, s) in enumerate(dic):
        x = ML + (i % 2) * (w2 + 12); yy = y + (i // 2) * 52
        rrect(c, x, yy, w2, 46, 8, fill=white, stroke=GRID_L)
        texto(c, x + 12, yy + 15, t, 'PS', 8.6, ACC_D)
        parrafo(c, x + 12, yy + 20, w2 - 22, s, 7.6, INK, 10.5)
    y = seccion(c, y + 3 * 52 + 8, 'Ajustes de la máquina para tela de punto')
    for k, (a, b) in enumerate([('Aguja', 'Punta redonda (ballpoint) 80/12'), ('Hilo', 'Poliéster'),
                                ('Puntada', 'Zigzag estrecho: ancho 1–1,5 y largo 2,5–3 (o puntada elástica)'),
                                ('Presión del prensatelas', 'Ligera, si tu máquina lo permite'),
                                ('Antes de empezar', 'Prueba siempre en un retal doble de la misma tela')]):
        if k % 2 == 0: rrect(c, ML, y, CW, 16, 4, fill=CREAM)
        texto(c, ML + 10, y + 11, a, 'PS', 7.8, INK); texto(c, ML + 160, y + 11, b, 'P', 7.8, INK)
        y += 17
    y = seccion(c, y + 14, 'Cinco reglas de oro')
    vinetas(c, ML, y, CW, ['<b>Lee cada paso entero</b> antes de coser.', '<b>Plancha</b> las costuras en cada paso: la prenda quedará mucho más profesional.',
                           '<b>No tires de la tela</b> mientras coses: deja que la máquina la lleve.',
                           '<b>Mide dos veces, corta una.</b> Comprueba la talla en la tabla antes de cortar.',
                           'Si te equivocas, <b>descose y repite</b>. A todos nos pasa, sobre todo al principio.'], 8.4, 3)


# ---------------------------------------------------------------- pasos
def caja_paso(c, y):
    rrect(c, ML, y, 227, 226, 10, fill=CREAM)


def paso(c, mitad, n, titulo, items, consejo_txt, dibujo):
    y0 = 82 + mitad * 388
    circulo_num(c, ML + 13, y0 + 17, n, 13, size=12)
    texto(c, ML + 38, y0 + 6, f'PASO {n}', 'PB', 6.3, ACC_D)
    texto(c, ML + 38, y0 + 23, titulo, 'PS', 13, INK)
    caja_paso(c, y0 + 42)
    dibujo(c, ML, y0 + 42, 227, 226)
    lista_numerada(c, ML + 240, y0 + 44, CW - 240, items, 8.4, 5)
    consejo(c, y0 + 279, 'Consejo', consejo_txt)


def d_hombros(c, x, y, w, h):
    fd = pieza_completa(R[M]['del_'][0]); fe = pieza_completa(R[M]['esp'][0]); k = 2.6
    cx = x + w / 2 + 6
    dibujar_pieza(c, fe, cx - 10, y + 30, k, GREY, INK, .6)
    dibujar_pieza(c, fd, cx, y + 22, k, ACC_L, INK, .7)
    B, C_ = R[M]['del_'][1]['B'], R[M]['del_'][1]['C']
    for sg in (1, -1):
        linea(c, cx + sg * B[0] * k, y + 22 + B[1] * k + 3, cx + sg * C_[0] * k, y + 22 + C_[1] * k + 3, INK, 1.1, [3, 2])
    texto(c, cx, y + 120, 'delantero', 'PB', 7, white, 'center')
    texto(c, cx, y + 130, '(derecho arriba)', 'P', 6, white, 'center')


def d_tira(c, x, y, w, h):
    rrect(c, x + 22, y + 30, 183, 22, 2, fill=ACC_D)
    texto(c, x + 113, y + 44, 'tira (talla M: 42 x 6 cm)', 'PB', 6.5, white, 'center')
    flecha(c, x + 22, y + 60, x + 205, y + 60, ACC_D, .7, 3, dos=True)
    texto(c, x + 113, y + 70, 'largo = sentido que más estira', 'P', 6, ACC_D, 'center')
    circulo_num(c, x + 30, y + 98, 2, 6)
    c.setStrokeColor(ACC_D); c.setLineWidth(9); c.ellipse(x + 50, Y(y + 200), x + 177, Y(y + 110), stroke=1, fill=0)
    marks = [(x + 113.5, y + 110, 'costura'), (x + 113.5, y + 200, ''), (x + 50, y + 155, ''), (x + 177, y + 155, '')]
    for i, (mx, my, lab) in enumerate(marks):
        c.setFillColor(white); c.circle(mx, Y(my), 4.5, fill=1, stroke=0)
        c.setFillColor(INK); c.circle(mx, Y(my), 2, fill=1, stroke=0)
    texto(c, x + 113.5, y + 102, 'costura (centro espalda)', 'PM', 6, INK, 'center')
    texto(c, x + 113.5, y + 214, 'centro delantero', 'PM', 6, INK, 'center')
    texto(c, x + 113.5, y + 152, 'aro doblado', 'PB', 6.5, ACC_D, 'center')
    texto(c, x + 113.5, y + 162, 'por la mitad', 'PB', 6.5, ACC_D, 'center')
    circulo_num(c, x + 30, y + 150, 4, 6)


def d_cuello(c, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2 + 6
    c.setFillColor(ACC_L); c.ellipse(cx - 92, Y(cy + 62), cx + 92, Y(cy - 62), fill=1, stroke=0)
    c.setFillColor(CREAM); c.ellipse(cx - 58, Y(cy + 40), cx + 58, Y(cy - 40), fill=1, stroke=0)
    c.setStrokeColor(ACC_D); c.setLineWidth(8); c.ellipse(cx - 62, Y(cy + 44), cx + 62, Y(cy - 44), fill=0, stroke=1)
    c.setStrokeColor(white); c.setLineWidth(.8); c.setDash([2.5, 2]); c.ellipse(cx - 68, Y(cy + 49), cx + 68, Y(cy - 49), fill=0, stroke=1); c.setDash([])
    for i, (mx, my, lab, ly) in enumerate([(cx, cy - 44, 'centro espalda', -52), (cx, cy + 44, 'centro delantero', 60),
                                           (cx - 62, cy, '', 0), (cx + 62, cy, '', 0)]):
        circulo_num(c, mx, my, i + 1, 5.5, fill=INK, size=6)
        if lab: texto(c, cx, cy + ly, lab, 'PM', 6.3, INK, 'center')
    texto(c, cx, cy - 3, 'tira por fuera', 'PB', 6.3, ACC_D, 'center')
    texto(c, cx, cy + 7, '(se estira entre marcas)', 'P', 5.8, ACC_D, 'center')
    texto(c, cx - 105, cy + 3, 'marca', 'P', 5.8, INK, 'center'); texto(c, cx + 105, cy + 3, 'marca', 'P', 5.8, INK, 'center')


def d_mangas(c, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2
    c.setFillColor(ACC_L); c.setStrokeColor(INK); c.setLineWidth(.6)
    c.rect(cx - 30, Y(cy + 85), 60, 170, fill=1, stroke=1)
    texto(c, cx, cy - 50, 'DELANTERO', 'PB', 6.5, white, 'center'); texto(c, cx, cy + 58, 'ESPALDA', 'PB', 6.5, white, 'center')
    linea(c, cx - 30, cy, cx + 30, cy, INK, .5, [2, 2])
    for sg in (1, -1):
        pts = [(cx + sg * 30, cy - 40), (cx + sg * 30, cy + 40), (cx + sg * 95, cy + 24), (cx + sg * 95, cy - 24)]
        poligono(c, pts, fill=ACC_M, stroke=INK, lw=.6)
        linea(c, cx + sg * 33, cy - 38, cx + sg * 33, cy + 38, ACC_D, 1.1, [3, 2])
        texto(c, cx + sg * 64, cy + 3, 'MANGA', 'PB', 6.3, white, 'center')
    c.setFillColor(white); c.circle(cx + 30, Y(cy), 3, fill=1, stroke=0); c.circle(cx - 30, Y(cy), 3, fill=1, stroke=0)
    texto(c, cx + 52, cy - 52, 'centro de la copa', 'PM', 6, INK, 'left')
    texto(c, cx + 52, cy - 44, '= costura del hombro', 'PM', 6, INK, 'left')
    flecha(c, cx + 60, cy - 40, cx + 33, cy - 4, INK, .6, 3)


def d_costados(c, x, y, w, h):
    cx, top = x + w / 2, y + 30
    texto(c, cx, top - 6, 'doblez = línea de los hombros', 'PB', 6.3, INK, 'center')
    pts = [(x + 14, top), (x + w - 14, top), (x + w - 14, top + 40), (cx + 36, top + 52), (cx + 36, top + 170), (cx - 36, top + 170),
           (cx - 36, top + 52), (x + 14, top + 40)]
    poligono(c, pts, fill=ACC_L, stroke=INK, lw=.6)
    linea(c, x + 14, top, x + w - 14, top, INK, 1.6)
    texto(c, cx, top + 70, 'DELANTERO', 'PB', 6.5, white, 'center')
    for sg in (1, -1):
        poligono(c, [(cx + sg * (w / 2 - 14), top + 37), (cx + sg * 36, top + 49), (cx + sg * 33, top + 167)], stroke=INK, lw=1.2, dash=[3, 2], cerrado=False)
    letra(c, x + w - 20, top + 42, 'A', 6); letra(c, cx + 36, top + 176, 'B', 6)


def d_dobladillo(c, x, y, w, h, manga=True):
    cx = x + w / 2
    if manga:
        poligono(c, [(x + 30, y + 40), (x + w - 30, y + 40), (x + w - 16, y + 170), (x + 16, y + 170)], fill=ACC_L, stroke=INK, lw=.6)
        texto(c, cx, y + 80, 'MANGA (del revés)', 'PB', 6.5, white, 'center')
    else:
        poligono(c, [(x + 22, y + 30), (x + w - 22, y + 30), (x + w - 22, y + 170), (x + 22, y + 170)], fill=ACC_L, stroke=INK, lw=.6)
        texto(c, cx, y + 80, 'CUERPO (del revés)', 'PB', 6.5, white, 'center')
    yb = y + 170
    c.setFillColor(ACC_M); c.rect(x + (16 if manga else 22), Y(yb), w - (32 if manga else 44), 28, fill=1, stroke=0)
    linea(c, x + (16 if manga else 22), yb - 28, x + w - (16 if manga else 22), yb - 28, INK, .6, [1, 1.5])
    for dy, col in ((-22, white), (-17, white)):
        linea(c, x + (18 if manga else 24), yb + dy, x + w - (18 if manga else 24), yb + dy, col, 1, [3, 2])
    flecha(c, x + w - 8, yb - 28, x + w - 8, yb, INK, .6, 2.5, dos=True)
    texto(c, x + w - 12, yb - 32, '2,5 cm', 'PB', 6, INK, 'right')
    texto(c, cx, yb + 16, 'dobla 2,5 cm hacia dentro · cose a 2 cm del doblez', 'PM', 6, INK, 'center')
    texto(c, cx, yb + 26, 'línea discontinua blanca = costura (aguja doble o zigzag)', 'P', 5.6, MUTED, 'center')


@doc.pagina('pasos')
def pasos12(c):
    cabecera(c, 'Pasos 1 y 2', 'Montaje paso a paso')
    paso(c, 0, 1, 'Une los hombros', [
        'Pon el <b>delantero</b> sobre la mesa con el derecho hacia arriba.',
        'Coloca la <b>espalda</b> encima, con el derecho hacia abajo (<b>derecho con derecho</b>). Alinea hombros y cuello.',
        'Sujeta cada hombro con clips.',
        'Cose los dos hombros a <b>1,5 cm</b> del borde, del cuello hacia la manga, con retroceso al empezar y al acabar.',
        'Plancha los márgenes hacia la espalda.'],
        'Usa zigzag estrecho (ancho 1, largo 2,5) en todas las costuras: así estiran con la tela y no se rompen.', d_hombros)
    paso(c, 1, 2, 'Prepara la tira del cuello', [
        'Corta la tira con la medida de tu talla (pág. ' + str(doc.num('p_tira')) + '). El <b>largo</b> va en el sentido en que más estira la tela.',
        'Dobla la tira por la mitad uniendo los <b>extremos cortos</b>, derecho con derecho, y cose a <b>1 cm</b>: queda un aro.',
        'Abre esa costura con los dedos y dobla el aro por la mitad a lo largo, <b>con el revés dentro</b>: queda una tira de 3 cm con los dos bordes juntos.',
        'Marca <b>4 puntos iguales</b> con clips: la costura (será el centro de la espalda), el lado contrario y los dos puntos de en medio.'],
        'La tira es más corta que el escote a propósito: así el cuello queda plano, pegado al cuerpo y no se da de sí.', d_tira)


@doc.pagina()
def pasos34(c):
    cabecera(c, 'Pasos 3 y 4', 'Montaje paso a paso')
    paso(c, 0, 3, 'Cose la tira al cuello', [
        'Marca también <b>4 puntos</b> en el escote: dobla el cuello por el centro del delantero y de la espalda, y luego otra vez por la mitad.',
        'Con la camiseta del derecho, pon la tira por fuera, con los bordes juntos sobre el borde del escote y su costura en el <b>centro de la espalda</b>.',
        'Casa las 4 marcas de la tira con las 4 del escote y sujeta con clips.',
        'Cose a <b>1 cm</b> con zigzag <b>estirando solo la tira</b> (no el escote) para que llegue de marca a marca.',
        'Dobla el margen hacia el cuerpo y plancha con vapor. Si quieres, pespuntea a 0,5 cm por fuera.'],
        'Cose con la tira hacia arriba para ver cuánto la estiras. Ve despacio y para con la aguja abajo en cada marca.', d_cuello)
    paso(c, 1, 4, 'Cose las mangas', [
        'Extiende el cuerpo plano, con el derecho hacia arriba: delantero arriba y espalda abajo, unidos por los hombros.',
        'Coloca una manga encima, <b>derecho con derecho</b>, con su copa curva sobre la sisa curva.',
        'Casa el <b>centro de la copa</b> (punto A, marcado con tiza) con la costura del hombro y fija con clips hacia los extremos.',
        'Cose a <b>1,5 cm</b> con retroceso. No hace falta estirar: copa y sisa miden lo mismo.',
        'Repite con la otra manga y plancha los márgenes hacia la manga.'],
        'Si al llegar al final sobra tela en un lado, la manga no está centrada: suelta los clips y vuelve a casar el centro con el hombro.', d_mangas)


@doc.pagina()
def pasos56(c):
    cabecera(c, 'Pasos 5 y 6', 'Montaje paso a paso')
    paso(c, 0, 5, 'Cierra costados y mangas', [
        'Dobla la camiseta por la línea de los hombros, <b>derecho con derecho</b>, con las mangas extendidas.',
        'Casa las costuras de las axilas y sujétalas con un clip. Luego casa el borde de la manga y el bajo.',
        'Cose en <b>una sola costura</b> a 1,5 cm: del borde de la manga (A), pasando por debajo del brazo, hasta el bajo del cuerpo (B).',
        'Cruza la axila despacio. Puedes reforzarla con una segunda pasada.',
        'Repite en el otro lado y plancha los márgenes hacia la espalda.'],
        'Mide la costura de la manga y la del costado y compáralas con la tabla (pág. ' + str(doc.num('medidas')) + '): deben coincidir con tu talla.', d_costados)
    paso(c, 1, 6, 'Dobladillo de las mangas', [
        'Con la camiseta del revés, dobla <b>2,5 cm</b> hacia dentro el borde de cada manga.',
        'Plancha el doblez y sujétalo con clips.',
        'Da la vuelta a la camiseta (del derecho) y cose a <b>2 cm</b> del borde doblado, dando la vuelta completa a la manga.',
        '<b>Con aguja doble</b> salen dos líneas rectas por fuera; <b>sin aguja doble</b>, usa zigzag estrecho.',
        'Acaba cosiendo 2 cm encima del inicio para rematar.'],
        'Mete la manga en el brazo libre de la máquina (quita la mesita de la base) para coserla en redondo más fácil.',
        lambda c, x, y, w, h: d_dobladillo(c, x, y, w, h, True))


@doc.pagina()
def paso7(c):
    cabecera(c, 'Paso 7', 'Montaje paso a paso')
    paso(c, 0, 7, 'Dobladillo del bajo', [
        'Con la camiseta del revés, dobla <b>2,5 cm</b> hacia dentro todo el bajo y plancha.',
        'Sujeta con clips cada 10 cm, empezando por las costuras de los costados.',
        'Del derecho, cose a <b>2 cm</b> del borde doblado, empezando en un costado y dando la vuelta completa.',
        'Acaba cosiendo 2 cm encima del inicio para rematar.',
        'Plancha todo el bajo con vapor.'],
        'Si el bajo ondula, sube el largo de puntada a 3 y baja la presión del prensatelas. No tires de la tela.',
        lambda c, x, y, w, h: d_dobladillo(c, x, y, w, h, False))
    y = seccion(c, 82 + 388, 'Resumen de la costura')
    filas = [['1', 'Hombros', '1,5 cm', 'zigzag estrecho'], ['2', 'Aro de la tira', '1 cm', 'recta o zigzag'],
             ['3', 'Tira al escote', '1 cm', 'zigzag, estirando la tira'], ['4', 'Mangas a la sisa', '1,5 cm', 'zigzag estrecho'],
             ['5', 'Costados y bajomangas', '1,5 cm', 'zigzag estrecho'], ['6', 'Dobladillo de mangas', 'doblar 2,5 · coser a 2', 'aguja doble o zigzag'],
             ['7', 'Dobladillo del bajo', 'doblar 2,5 · coser a 2', 'aguja doble o zigzag']]
    tabla(c, y, ['Paso', 'Costura', 'Margen', 'Puntada'], filas, [50, 170, 130, CW - 350], alinear=['center', 'left', 'center', 'center'])


@doc.pagina()
def remate(c):
    cabecera(c, 'Última página del manual', 'Remate y revisión')
    texto(c, ML, 98, '¡Tu camiseta está lista!', 'PS', 14, INK)
    rrect(c, ML, 110, 245, 178, 10, fill=CREAM)
    camiseta_dibujo(c, ML + 122, 140, 0.44, ACC_L, ACC_M, RIB, white)
    lista_numerada(c, ML + 260, 112, CW - 260, ['Recorta los hilos sueltos de todas las costuras.', 'Plancha toda la prenda con vapor, sin aplastar el cuello.',
                                                'Compara las medidas con la tabla (pág. ' + str(doc.num('medidas')) + ').', 'Pruébatela y revisa la lista de abajo.'], 8.6, 6)
    y = seccion(c, 300, 'Lista de comprobación')
    l1 = ['El cuello queda plano y no hace ondas', 'Los hombros quedan planos y sin arrugas', 'Las dos mangas miden lo mismo']
    l2 = ['Los costados caen rectos', 'Los dobladillos no ondulan', 'Ninguna costura cruje al estirar']
    for i, s in enumerate(l1): casilla(c, ML, y + i * 17, s)
    for i, s in enumerate(l2): casilla(c, ML + CW / 2, y + i * 17, s)
    y = seccion(c, y + 66, 'Si algo sale mal')
    prob = [('El cuello hace ondas', 'La tira quedó larga o no la estiraste: descose, acorta la tira 2 cm y vuelve a coserla.'),
            ('El cuello se da de sí', 'Estiraste también el escote: estira solo la tira y cose con ella hacia arriba.'),
            ('Se saltan puntadas', 'Cambia la aguja por una nueva de punta redonda 80/12.'),
            ('Las costuras se rompen al estirar', 'Usa zigzag estrecho o puntada elástica, nunca recta sola.'),
            ('El dobladillo hace un túnel', 'Con aguja doble, baja un poco la tensión del hilo de arriba o usa zigzag.'),
            ('No me encaja la manga', 'Compara sisa y copa con la tabla y revisa que el centro de la manga coincida con el hombro.')]
    for k, (a, b) in enumerate(prob):
        hh = max(24, alto_parrafo(CW - 200, b, 7.8) + 12)
        if k % 2 == 0: rrect(c, ML, y, CW, hh, 6, fill=CREAM)
        texto(c, ML + 10, y + 15, a, 'PS', 7.8, INK)
        parrafo(c, ML + 190, y + 6, CW - 200, b, 7.8, INK)
        y += hh + 3
    consejo(c, y + 12, 'Cuidado de la prenda', 'Lávala del revés a 30 °C, sin lejía, y sécala en plano o a baja temperatura. Plancha a temperatura media.')


# ---------------------------------------------------------------- patrones
def caja_ref(pz, a, b):
    return f'{a}–{b}'


def puntos_talla(pieza, claves):
    return {t: [R[t][pieza][1][k] for k in claves] for t in TALLAS}


def mid(pts):
    return pts[len(pts) // 2]


def patron_cuerpo(c, pieza, titulo):
    cont = {t: R[t][pieza][0] for t in TALLAS}
    pts = R['XL'][pieza][1]; md = lambda k: med(pieza, k)
    cuello_xl = cuello('XL', ESCOTE_DEL['XL'] if pieza == 'del_' else 2)[0]
    sisa_xl = sisa('XL')[0]
    cajas = [
        {'titulo': 'Hombro', 'ref': 'B–C', 'vals': md('hombro'), 'ancla': ((pts['B'][0] + pts['C'][0]) / 2, (pts['B'][1] + pts['C'][1]) / 2)},
        {'titulo': 'Cuello (curva)', 'ref': 'curva A–B', 'vals': md('cuello'), 'ancla': mid(cuello_xl)},
        {'titulo': 'Sisa (curva)', 'ref': 'curva C–D', 'vals': md('sisa'), 'ancla': mid(sisa_xl)},
        {'titulo': 'Centro (doblez)', 'ref': 'A–F', 'vals': md('centro'), 'ancla': (0, 42)},
        {'titulo': 'Costado', 'ref': 'D–E', 'vals': md('costado'), 'ancla': (pts['D'][0], 52)},
        {'titulo': 'Bajo · mitad', 'ref': 'E–F', 'vals': md('bajo'), 'ancla': (pts['E'][0] / 2, pts['E'][1])},
    ]
    if pieza == 'esp':
        cajas[0], cajas[1] = cajas[1], cajas[0]
    for cj, yy in zip(cajas, [136, 178, 236, 420, 470, 552]):
        cj['y'] = yy
    letras = [('A', pts['A'], 7, 0), ('B', pts['B'], 2, 8), ('C', pts['C'], 7, 4), ('D', pts['D'], 7, 6), ('E', pts['E'], 7, 7), ('F', pts['F'], 8, -6)]
    pagina_patron(c, {
        'titulo': titulo, 'cortar': 'Cortar 1 · traza la mitad; en la tela, doblez sobre el doblez',
        'ancho_cm': 40, 'alto_cm': 80, 'contornos': cont, 'doblez': True, 'letras': letras, 'cajas': cajas,
        'puntos': {t: [R[t][pieza][1][k] for k in ('A', 'B', 'C', 'D', 'E', 'F')] for t in TALLAS},
        'hilo': (8, 30, 60), 'dims': {t: f'{fmt(CUARTO[t])} x {fmt(LARGO[t])} cm' for t in TALLAS},
        'nota': 'Dibuja en tu papel una cuadrícula de cuadros de <b>10 x 10 cm</b> (los cuadros grandes del dibujo) y copia la línea de tu talla '
                'cuadro a cuadro, o ve a la página siguiente y marca los <b>puntos con sus coordenadas</b>. Margen: 1 cm en el escote, '
                '1,5 cm en hombro, sisa y costado, 2,5 cm en el bajo; el doblez no lleva margen.'})


def filas_coord(pieza, desc):
    filas = []
    for k in R['M'][pieza][1].keys():
        curva = k[0] in 'cs' and len(k) > 1
        d = desc.get(k, 'curva del cuello' if k.startswith('c') else 'curva de la sisa' if pieza != 'man' else 'curva de la copa')
        filas.append((k, d, {t: tuple(r1(v) for v in R[t][pieza][1][k]) for t in TALLAS}, curva))
    orden = ['A'] + [f'c{i}' for i in range(1, 8)] + ['B', 'C'] + [f's{i}' for i in range(1, 9)] + ['D', 'E', 'F']
    if pieza == 'man': orden = ['A'] + [f's{i}' for i in range(1, 9)] + ['B', 'C', 'D']
    filas.sort(key=lambda f: orden.index(f[0]))
    return filas


DESC_CUERPO = {'A': 'Centro del cuello (en el doblez)', 'B': 'Cuello con hombro', 'C': 'Punta del hombro',
               'D': 'Axila (fin de la sisa)', 'E': 'Esquina del bajo', 'F': 'Bajo en el doblez'}


@doc.pagina('p_del')
def p_del(c):
    patron_cuerpo(c, 'del_', 'Delantero')


@doc.pagina()
def p_del_c(c):
    pagina_coordenadas(c, 'Delantero', filas_coord('del_', DESC_CUERPO),
                       'Las coordenadas de <b>c1 a c7</b> trazan la curva del cuello (A–B) y las de <b>s1 a s8</b> la curva de la sisa (C–D): '
                       'une los puntos con una curva suave. El cuello del delantero es más profundo que el de la espalda.')


@doc.pagina('p_esp')
def p_esp(c):
    patron_cuerpo(c, 'esp', 'Espalda')


@doc.pagina()
def p_esp_c(c):
    pagina_coordenadas(c, 'Espalda', filas_coord('esp', DESC_CUERPO),
                       'Las coordenadas de <b>c1 a c7</b> trazan la curva del cuello (A–B) y las de <b>s1 a s8</b> la curva de la sisa (C–D). '
                       'La sisa de la espalda es igual que la del delantero; solo cambia el cuello, que es casi recto.')


@doc.pagina('p_man')
def p_man(c):
    cont = {t: R[t]['man'][0] for t in TALLAS}
    pts = R['XL']['man'][1]; md = lambda k: med('man', k)
    copa_xl = copa('XL', R['XL']['man'][2]['ancho'])
    cajas = [{'titulo': 'Copa (curva) · mitad', 'ref': 'curva A–B', 'vals': md('copa'), 'ancla': mid(copa_xl), 'y': 136},
             {'titulo': 'Centro (doblez)', 'ref': 'A–D', 'vals': md('centro'), 'ancla': (0, 14), 'y': 190},
             {'titulo': 'Bajomanga', 'ref': 'B–C', 'vals': md('bajomanga'), 'ancla': ((pts['B'][0] + pts['C'][0]) / 2, (pts['B'][1] + pts['C'][1]) / 2), 'y': 240},
             {'titulo': 'Boca · mitad', 'ref': 'C–D', 'vals': md('boca'), 'ancla': (pts['C'][0] / 2, pts['C'][1]), 'y': 290}]
    letras = [('A', pts['A'], 10, 9), ('B', pts['B'], 7, -4), ('C', pts['C'], 7, 7), ('D', pts['D'], 8, 7)]
    pagina_patron(c, {
        'titulo': 'Manga', 'cortar': 'Cortar 2 · abre el papel (pieza entera); tela doblada', 'ancho_cm': 30, 'alto_cm': 30,
        'contornos': cont, 'doblez': True, 'letras': letras, 'cajas': cajas,
        'puntos': {t: [R[t]['man'][1][k] for k in ('A', 'B', 'C', 'D')] for t in TALLAS},
        'hilo': (6, 9, 21), 'dims': {t: f"{fmt(R[t]['man'][2]['ancho'])} x {fmt(LARGO_MANGA[t])} cm" for t in TALLAS},
        'nota': 'Dibuja la mitad con la cuadrícula o con las coordenadas de la página siguiente y luego <b>dobla el papel por el doblez</b> y recorta: '
                'así sale la manga entera y simétrica. La copa mide lo mismo que la sisa del cuerpo (cifras de la caja). '
                'Margen: 1,5 cm en copa y bajomanga, 2,5 cm en la boca.'})


@doc.pagina()
def p_man_c(c):
    pagina_coordenadas(c, 'Manga', filas_coord('man', {'A': 'Centro de la copa arriba (doblez)', 'B': 'Axila de la manga (fin de la copa)',
                                                        'C': 'Boca de la manga (borde del lado)', 'D': 'Centro de la boca (doblez)'}),
                       'Las coordenadas de <b>s1 a s8</b> trazan la curva de la copa (A–B). Une los puntos con una curva suave. '
                       'Después dobla el papel por el lado izquierdo (doblez) y recorta para tener la manga entera.',
                       pasos=['Marca en tu papel la esquina superior izquierda: es el punto <b>(0, 0)</b>. El lado izquierdo es el doblez.',
                              'Para cada punto de tu talla, mide <b>x</b> hacia la derecha y <b>y</b> hacia abajo con la regla y marca un punto.',
                              'Une A con los puntos <b>s1…s8</b> y B con una <b>curva suave</b>; luego B–C, C–D y D–A con regla.',
                              'Dibuja el margen (1,5 cm en copa y bajomanga, 2,5 cm en la boca), dobla el papel por el doblez y recorta.'])


@doc.pagina('p_tira')
def p_tira(c):
    cabecera(c, 'Pieza rectangular · se corta midiendo', 'Tira del cuello')
    y = 84 + parrafo(c, ML, 84, CW, 'La tira del cuello es un <b>rectángulo</b>: dibújalo con regla y tiza directamente sobre la tela con la medida de tu talla '
                     'y córtalo. El <b>largo</b> va en el sentido en que más estira la tela (normalmente, de orillo a orillo). El dibujo no está a escala; '
                     'las medidas sí son reales.', 9.4, INK, 14) + 10
    y = seccion(c, y, 'TIRA DEL CUELLO · cortar 1', size=12)
    texto(c, PW / 2, y + 12, 'talla M: 42 x 6 cm  (línea blanca = doblez)', 'PB', 7.8, INK, 'center')
    rrect(c, PW / 2 - 190, y + 22, 380, 56, 2, fill=ACC_D)
    linea(c, PW / 2 - 186, y + 50, PW / 2 + 186, y + 50, white, .8, [3, 2])
    for sg in (1, -1):
        c.setFillColor(ACC); c.rect(PW / 2 + sg * 190 - (6 if sg > 0 else 0), Y(y + 78), 6, 56, fill=1, stroke=0)
    flecha(c, PW / 2 - 190, y + 90, PW / 2 + 190, y + 90, INK, .7, 3.5, dos=True)
    texto(c, PW / 2, y + 102, 'largo (sentido de más elasticidad)', 'P', 7.4, INK, 'center')
    flecha(c, PW / 2 + 200, y + 22, PW / 2 + 200, y + 78, INK, .7, 3, dos=True)
    texto(c, PW / 2 + 206, y + 53, '6 cm', 'PB', 7, INK)
    texto(c, PW / 2 - 186 + 2, y + 30, '1 cm', 'P', 5.5, white)
    y = tabla_tallas(c, y + 118, [('Medida de corte (largo x alto, cm)', V(lambda t: f"{R[t]['tira'][0]} x {R[t]['tira'][1]}")),
                                  ('Escote de la camiseta (cm)', V(lambda t: R[t]['escote'])),
                                  ('Tira terminada (alto, cm)', [TIRA_ALTO_FINAL] * 5)], primera=CW * 0.4)
    y = seccion(c, y + 20, 'Cómo se ha calculado (por si quieres cambiar de tela)')
    y = vinetas(c, ML, y, CW, ['El largo es el <b>85 % del escote</b> más 1 cm de margen en cada extremo. Con tela de camiseta normal queda perfecto.',
                               'Si usas <b>canalé (rib)</b>, que estira más, corta la tira al <b>80 %</b> del escote: por ejemplo, en la M, 39 cm en vez de 42.',
                               'Si tu tela estira muy poco, corta al <b>90 %</b>. Haz siempre una prueba: dobla la tira y estírala alrededor de la cabeza.'], 8.6, 4)
    y = consejo(c, y + 10, 'Recuerda', 'La medida de corte ya incluye los márgenes de 1 cm. La tira terminada mide <b>2 cm de alto</b>: '
                '6 cm de corte = 2 cm por fuera + 2 cm por dentro + 1 cm de margen en cada borde.')
    # regla 1:1
    yR = 770
    texto(c, ML, yR - 14, 'Regla 1:1 (15 cm)', 'PB', 7, INK)
    linea(c, ML, yR, ML + 15 * cm, yR, INK, .8)
    for i in range(31):
        h = 8 if i % 10 == 0 else 5 if i % 2 == 0 else 3
        linea(c, ML + i * cm / 2, yR - h, ML + i * cm / 2, yR, INK, .6)
        if i % 10 == 0: texto(c, ML + i * cm / 2, yR + 10, str(i // 2), 'P', 6, MUTED, 'center')


if __name__ == '__main__':
    n = doc.construir()
    print('PDF generado:', OUT, n, 'páginas')
