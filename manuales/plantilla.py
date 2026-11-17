"""
Plantilla común de los manuales de patrones (formato de la sudadera con capucha).

Todas las prendas usan este archivo para que los PDF salgan idénticos:
A4, fuente Poppins, cabecera azul marino con bloque naranja, tarjetas crema,
5 tallas (XS–XL) con color y tipo de línea propios, patrones a escala 1:5 con
cuadrícula, cajas de medidas y tablas de coordenadas.

Cada prenda (p. ej. camiseta.py) solo define su geometría, sus textos y el orden
de las páginas, y llama a las funciones de aquí.
"""
import math, os
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm

# ---------------------------------------------------------------- fuentes
_F = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fuentes')
for nombre, archivo in [('P', 'Regular'), ('PM', 'Medium'), ('PB', 'Bold'), ('PL', 'Light'),
                        ('PI', 'Italic'), ('PS', 'SemiBold')]:
    pdfmetrics.registerFont(TTFont(nombre, os.path.join(_F, f'Poppins-{archivo}.ttf')))
pdfmetrics.registerFontFamily('P', normal='P', bold='PB', italic='PI', boldItalic='PB')

# ---------------------------------------------------------------- colores (sacados del PDF de la sudadera)
INK = HexColor('#1F2430')      # azul marino: texto, cabeceras, tablas
ACC = HexColor('#F2542D')      # naranja principal
ACC_D = HexColor('#C63F1B')    # naranja oscuro (letras, etiquetas)
ACC_L = HexColor('#F6836A')    # salmón (piezas en los dibujos)
ACC_M = HexColor('#E5694F')    # salmón medio
PINK = HexColor('#FFD9CC')     # rosa claro
CREAM = HexColor('#F7F1E8')    # fondo de tarjetas
MUTED = HexColor('#6F7585')    # texto secundario
GRID = HexColor('#BDBAB1')     # cuadrícula fuerte / bordes
GRID_L = HexColor('#E7E5E0')   # cuadrícula suave
RIB = HexColor('#12151C')      # canalé / tiras oscuras
GREY = HexColor('#D9D5CE')     # pieza de debajo en los dibujos
COVER_C1 = HexColor('#262C3A')
COVER_C2 = HexColor('#2C3342')

TALLAS = ['XS', 'S', 'M', 'L', 'XL']
TALLA_COLOR = {'XS': HexColor('#7E3FF2'), 'S': HexColor('#1E88E5'), 'M': HexColor('#16A34A'),
               'L': HexColor('#E08A00'), 'XL': HexColor('#E11D48')}
TALLA_DASH = {'XS': [1, 2.2], 'S': [4.5, 2.2], 'M': [7, 2.2, 1.4, 2.2], 'L': [10, 2.8], 'XL': []}

PW, PH = A4
ML = 45                 # margen izquierdo
CW = PW - 2 * ML        # ancho útil
HEADER_H = 57
ESCALA = 0.2 * cm       # 1 cm real = 0,2 cm en el papel (escala 1:5)


def fmt(v, dec=1):
    """Número en formato español: 26.2 -> '26,2', 26.0 -> '26'."""
    if isinstance(v, str):
        return v
    r = round(v, dec)
    s = f'{r:.{dec}f}'.rstrip('0').rstrip('.') if dec else str(int(round(r)))
    return s.replace('.', ',')


# ---------------------------------------------------------------- documento
class Manual:
    """Lista de páginas (funciones). Se dibujan al final, cuando ya se sabe el total."""

    def __init__(self, ruta, titulo, asunto, pie, autor):
        self.ruta, self.titulo, self.asunto, self.pie, self.autor = ruta, titulo, asunto, pie, autor
        self.paginas = []          # (funcion, ancla)
        self.anclas = {}

    def pagina(self, ancla=None):
        def deco(f):
            self.paginas.append((f, ancla))
            return f
        return deco

    def num(self, ancla):
        return self.anclas[ancla]

    def construir(self):
        for i, (_, a) in enumerate(self.paginas, start=1):
            if a:
                self.anclas[a] = i
        c = rl_canvas.Canvas(self.ruta, pagesize=A4)
        c.setTitle(self.titulo); c.setSubject(self.asunto); c.setAuthor(self.autor)
        c.setCreator('anonymous')
        total = len(self.paginas)
        for i, (f, _) in enumerate(self.paginas, start=1):
            f(c)
            if i > 1:
                pie(c, i, total, self.pie)
            c.showPage()
        c.save()
        return total


# ---------------------------------------------------------------- utilidades de dibujo (y medido desde ARRIBA)
def Y(y):
    return PH - y


def texto(c, x, y, s, font='P', size=9, color=INK, align='left', spacing=0):
    c.setFont(font, size); c.setFillColor(color)
    if spacing:
        t = c.beginText(); t.setFont(font, size); t.setCharSpace(spacing)
        w = pdfmetrics.stringWidth(s, font, size) + spacing * (len(s) - 1)
        x0 = x - w / 2 if align == 'center' else x - w if align == 'right' else x
        t.setTextOrigin(x0, Y(y)); t.textOut(s); c.drawText(t)
        return
    if align == 'center':
        c.drawCentredString(x, Y(y), s)
    elif align == 'right':
        c.drawRightString(x, Y(y), s)
    else:
        c.drawString(x, Y(y), s)


def ancho(s, font='P', size=9):
    return pdfmetrics.stringWidth(s, font, size)


def parrafo(c, x, y, w, html, size=9.5, color=INK, leading=None, font='P', align=0):
    """Texto con <b>, <i>. Devuelve la altura usada."""
    st = ParagraphStyle('p', fontName=font, fontSize=size, leading=leading or size * 1.45,
                        textColor=color, alignment=align)
    p = Paragraph(html, st)
    _, h = p.wrap(w, 1000)
    p.drawOn(c, x, Y(y) - h)
    return h


def alto_parrafo(w, html, size=9.5, leading=None, font='P'):
    st = ParagraphStyle('p', fontName=font, fontSize=size, leading=leading or size * 1.45)
    return Paragraph(html, st).wrap(w, 1000)[1]


def rrect(c, x, y, w, h, r=8, fill=None, stroke=None, lw=1):
    c.setLineWidth(lw)
    if fill is not None: c.setFillColor(fill)
    if stroke is not None: c.setStrokeColor(stroke)
    c.roundRect(x, Y(y) - h, w, h, r, fill=1 if fill is not None else 0, stroke=1 if stroke is not None else 0)


def poligono(c, pts, fill=None, stroke=None, lw=1, cerrado=True, dash=None):
    """pts en coordenadas de página con y desde arriba."""
    p = c.beginPath(); p.moveTo(pts[0][0], Y(pts[0][1]))
    for x, y in pts[1:]:
        p.lineTo(x, Y(y))
    if cerrado: p.close()
    c.setLineWidth(lw); c.setDash(dash or [])
    if fill is not None: c.setFillColor(fill)
    if stroke is not None: c.setStrokeColor(stroke)
    c.setLineJoin(1); c.setLineCap(1)
    c.drawPath(p, fill=1 if fill is not None else 0, stroke=1 if stroke is not None else 0)
    c.setDash([])


def linea(c, x1, y1, x2, y2, color=INK, lw=1, dash=None):
    c.setStrokeColor(color); c.setLineWidth(lw); c.setDash(dash or []); c.setLineCap(1)
    c.line(x1, Y(y1), x2, Y(y2)); c.setDash([])


def circulo_num(c, x, y, n, r=6.5, fill=ACC, color=white, size=7.5):
    c.setFillColor(fill); c.circle(x, Y(y), r, fill=1, stroke=0)
    texto(c, x, y + size * 0.36, str(n), 'PB', size, color, 'center')


def letra(c, x, y, s, r=5.5):
    """Letra en un círculo (punto de la tabla de coordenadas)."""
    c.setFillColor(white); c.setStrokeColor(ACC_D); c.setLineWidth(0.8)
    c.circle(x, Y(y), r, fill=1, stroke=1)
    texto(c, x, y + 2.3, s, 'PB', 6, ACC_D, 'center')


def pastilla(c, x, y, talla, w=27, h=11):
    """Pastilla de color con el nombre de la talla (x,y = centro)."""
    rrect(c, x - w / 2, y - h / 2, w, h, h / 2, fill=TALLA_COLOR[talla])
    texto(c, x, y + 2.3, talla, 'PB', 6, white, 'center')


def flecha(c, x1, y1, x2, y2, color=INK, lw=0.8, cabeza=4, dos=False):
    linea(c, x1, y1, x2, y2, color, lw)
    def punta(xa, ya, xb, yb):
        a = math.atan2(yb - ya, xb - xa)
        pts = [(xb, yb), (xb - cabeza * math.cos(a - .4), yb - cabeza * math.sin(a - .4)),
               (xb - cabeza * math.cos(a + .4), yb - cabeza * math.sin(a + .4))]
        poligono(c, pts, fill=color)
    punta(x1, y1, x2, y2)
    if dos: punta(x2, y2, x1, y1)


# ---------------------------------------------------------------- piezas de página
def cabecera(c, antetitulo, titulo):
    c.setFillColor(INK); c.rect(0, Y(HEADER_H), PW, HEADER_H, fill=1, stroke=0)
    c.setFillColor(ACC); c.rect(0, Y(HEADER_H), 34, HEADER_H, fill=1, stroke=0)
    texto(c, 51, 27, antetitulo.upper(), 'P', 6.8, PINK)
    texto(c, 51, 45, titulo, 'PB', 15.5, white)


def pie(c, n, total, s):
    linea(c, ML, 806, PW - ML, 806, GRID_L, 0.6)
    texto(c, ML, 820, s, 'P', 6.5, MUTED)
    texto(c, PW - ML, 820, f'{n} / {total}', 'PB', 7, INK, 'right')


def seccion(c, y, s, x=ML, size=12):
    c.setFillColor(ACC); c.rect(x, Y(y + 3), 4, 15, fill=1, stroke=0)
    texto(c, x + 11, y + 9, s, 'PS', size, INK)
    return y + 26


def tarjeta(c, x, y, w, h, etiqueta=None, titulo=None, sub=None, fondo=CREAM, barra=True, tsize=14):
    rrect(c, x, y, w, h, 9, fill=fondo)
    if barra:
        c.setFillColor(ACC); c.roundRect(x, Y(y) - h, 4, h, 2, fill=1, stroke=0)
    yy = y + 18
    if etiqueta:
        texto(c, x + 16, yy, etiqueta.upper(), 'PB', 6.3, ACC_D); yy += 20
    if titulo:
        texto(c, x + 16, yy, titulo, 'PS', tsize, INK); yy += 14
    if sub:
        parrafo(c, x + 16, yy - 6, w - 28, sub, 7.5, MUTED, 10)


def consejo(c, y, etiqueta, html, x=ML, w=CW, size=8.6):
    """Caja crema a lo ancho con barra naranja (CONSEJO, TRUCO, IMPORTANTE...). Devuelve y final."""
    h = alto_parrafo(w - 32, html, size) + 36
    rrect(c, x, y, w, h, 9, fill=CREAM)
    c.setFillColor(ACC); c.roundRect(x, Y(y) - h, 4, h, 2, fill=1, stroke=0)
    texto(c, x + 16, y + 16, etiqueta.upper(), 'PB', 6.3, ACC_D)
    parrafo(c, x + 16, y + 22, w - 32, html, size, INK)
    return y + h


def lista_numerada(c, x, y, w, items, size=8.6, gap=7, r=6):
    for i, it in enumerate(items, 1):
        circulo_num(c, x + r, y + r + 1, i, r, size=size * 0.82)
        h = parrafo(c, x + 2 * r + 6, y, w - 2 * r - 6, it, size, INK)
        y += h + gap
    return y


def vinetas(c, x, y, w, items, size=8.6, gap=5):
    for it in items:
        c.setFillColor(ACC); c.circle(x + 2.5, Y(y + 7), 2.2, fill=1, stroke=0)
        h = parrafo(c, x + 14, y, w - 14, it, size, INK)
        y += h + gap
    return y


def check(c, x, y, s, size=8.6):
    c.setStrokeColor(ACC); c.setLineWidth(1.6); c.setLineCap(1); c.setLineJoin(1)
    p = c.beginPath(); p.moveTo(x, Y(y + 5)); p.lineTo(x + 3, Y(y + 8.5)); p.lineTo(x + 8.5, Y(y + 1)); c.drawPath(p, stroke=1, fill=0)
    texto(c, x + 16, y + 8, s, 'P', size, INK)


def casilla(c, x, y, s, size=8.6):
    rrect(c, x, y, 10, 10, 2.5, stroke=ACC, lw=1.1)
    texto(c, x + 18, y + 8, s, 'P', size, INK)


def tabla_tallas(c, y, filas, x=ML, w=CW, primera=None, fila_h=19.5, size=8.3, cabecera_h=20, negrita_col0=False):
    """Tabla con cabecera oscura y pastillas de talla. filas = [(etiqueta, [XS,S,M,L,XL])]."""
    c0 = primera or w * 0.38
    cw = (w - c0) / 5
    rrect(c, x, y, w, cabecera_h, 6, fill=INK)
    for i, t in enumerate(TALLAS):
        pastilla(c, x + c0 + cw * (i + .5), y + cabecera_h / 2, t)
    yy = y + cabecera_h
    for k, (et, vals) in enumerate(filas):
        if k % 2 == 1:
            c.setFillColor(CREAM); c.rect(x, Y(yy + fila_h), w, fila_h, fill=1, stroke=0)
        texto(c, x + 8, yy + fila_h * .64, et, 'PM' if negrita_col0 else 'P', size, INK)
        for i, v in enumerate(vals):
            texto(c, x + c0 + cw * (i + .5), yy + fila_h * .64, fmt(v) if not isinstance(v, str) else v, 'P', size, INK, 'center')
        yy += fila_h
    linea(c, x, yy, x + w, yy, GRID, 0.6)
    return yy


def tabla(c, y, cabeceras, filas, anchos, x=ML, fila_h=19.5, size=8.3, alinear=None, cabecera_h=20, col0_bold=False):
    """Tabla genérica con cabecera oscura. anchos = lista de anchos de columna."""
    w = sum(anchos)
    rrect(c, x, y, w, cabecera_h, 6, fill=INK)
    alinear = alinear or ['left'] + ['center'] * (len(anchos) - 1)
    xs = [x]
    for a in anchos[:-1]:
        xs.append(xs[-1] + a)
    for i, h in enumerate(cabeceras):
        tx = xs[i] + 8 if alinear[i] == 'left' else xs[i] + anchos[i] / 2
        texto(c, tx, y + 13, h, 'PS', 7.6, white, 'left' if alinear[i] == 'left' else 'center')
    yy = y + cabecera_h
    for k, fila in enumerate(filas):
        if k % 2 == 1:
            c.setFillColor(CREAM); c.rect(x, Y(yy + fila_h), w, fila_h, fill=1, stroke=0)
        for i, v in enumerate(fila):
            tx = xs[i] + 8 if alinear[i] == 'left' else xs[i] + anchos[i] / 2
            texto(c, tx, yy + fila_h * .64, v, 'PS' if (i == 0 and col0_bold) else 'P', size, INK,
                  'left' if alinear[i] == 'left' else 'center')
        yy += fila_h
    linea(c, x, yy, x + w, yy, GRID, 0.6)
    return yy


def leyenda_tallas(c, y, x=ML):
    texto(c, x, y + 3, 'TALLAS', 'PB', 6.5, ACC_D)
    for i, t in enumerate(TALLAS):
        xx = x + 60 + i * 96
        linea(c, xx, y, xx + 32, y, TALLA_COLOR[t], 1.2, TALLA_DASH[t])
        texto(c, xx + 38, y + 3, t, 'PB', 7, TALLA_COLOR[t])


def barra_escala(c, y, x=ML + 120):
    """Barra de comprobación: 25 cm reales = 5 cm en el papel."""
    texto(c, ML, y + 3, 'COMPROBACIÓN DE ESCALA', 'PB', 6.5, ACC_D)
    L = 25 * ESCALA
    linea(c, x, y + 3, x + L, y + 3, INK, 0.8)
    for i in range(6):
        h = 6 if i in (0, 5) else 3.5
        linea(c, x + L * i / 5, y + 3 - h, x + L * i / 5, y + 3, INK, 0.8)
    texto(c, x + L + 8, y + 5, 'esta barra debe medir 5 cm al imprimir (= 25 cm reales)', 'P', 6.5, MUTED)


def tamanos_pieza(c, y, dims):
    """Fila de 5 cajas 'XS 25 x 59 cm'."""
    texto(c, ML, y, 'TAMAÑO DE LA PIEZA (sin margen, ancho x alto)', 'PB', 6.5, ACC_D)
    w = (CW - 4 * 4) / 5
    for i, t in enumerate(TALLAS):
        x = ML + i * (w + 4)
        rrect(c, x, y + 8, w, 24, 6, fill=CREAM)
        c.setFillColor(TALLA_COLOR[t]); c.circle(x + 11, Y(y + 20), 3.6, fill=1, stroke=0)
        texto(c, x + 19, y + 22.5, f'{t}  {dims[t]}', 'PB', 6.6, TALLA_COLOR[t])
    return y + 34


# ---------------------------------------------------------------- página de patrón a escala 1:5
def caja_medida(c, x, y, w, titulo, ref, vals, h=37):
    rrect(c, x, y, w, h, 7, fill=white, stroke=GRID, lw=0.8)
    texto(c, x + 9, y + 12, titulo, 'PS', 7.8, INK)
    texto(c, x + w - 9, y + 12, ref, 'P', 6, MUTED, 'right')
    cwid = (w - 18) / 5
    for i, t in enumerate(TALLAS):
        cx = x + 9 + cwid * (i + .5)
        texto(c, cx, y + 21, t, 'PB', 4.8, TALLA_COLOR[t], 'center')
        texto(c, cx, y + 31, fmt(vals[i]), 'PB', 8.4, TALLA_COLOR[t], 'center')


def pagina_patron(c, pieza):
    """
    pieza = {
      'titulo', 'cortar' (texto de la barra), 'ancho_cm', 'alto_cm' (cuadrícula),
      'contornos': {talla: [(x,y), ...]} en cm reales (y hacia abajo, 0,0 arriba-izq),
      'doblez': True si el borde x=0 va al doblez,
      'letras': [(letra, (x,y) en XL, dx, dy)],
      'cajas': [{'titulo','ref','vals':[5],'ancla':(x,y) en cm XL}],
      'hilo': (x, y1, y2) en cm, 'dims': {talla: '25 x 59 cm'}, 'nota': html,
      'marcas': [(x,y,'txt')] opcional
    }
    """
    cabecera(c, 'Dibujo con cuadrícula', f"{pieza['titulo']} · patrón a escala 1:5")
    # barra superior
    rrect(c, ML, 84, CW, 34, 9, fill=CREAM)
    texto(c, ML + 12, 99, 'CORTAR', 'PB', 6.3, ACC_D)
    texto(c, ML + 12, 111, pieza['cortar'], 'PS', 8.6, INK)
    texto(c, PW - ML - 12, 99, 'ESCALA 1:5', 'PB', 6.3, ACC_D, 'right')
    texto(c, PW - ML - 12, 111, '1 cm del dibujo = 5 cm reales · cuadro grande = 10 cm', 'P', 7, INK, 'right')

    gx, gy = ML + 26, 134                       # origen (0,0) de la cuadrícula
    W_, H_ = pieza['ancho_cm'], pieza['alto_cm']
    P = lambda x, y: (gx + x * ESCALA, gy + y * ESCALA)
    # cuadrícula fina (2 cm) y gruesa (10 cm)
    for xc in range(0, W_ + 1, 2):
        linea(c, *P(xc, 0), *P(xc, H_), GRID if xc % 10 == 0 else GRID_L, 0.6 if xc % 10 == 0 else 0.4)
    for yc in range(0, H_ + 1, 2):
        linea(c, *P(0, yc), *P(W_, yc), GRID if yc % 10 == 0 else GRID_L, 0.6 if yc % 10 == 0 else 0.4)
    # reglas
    texto(c, gx - 22, gy - 4, 'cm', 'P', 5.8, MUTED)
    for xc in range(0, W_ + 1, 10):
        texto(c, P(xc, 0)[0], gy - 4, str(xc), 'P', 5.8, MUTED, 'center')
    for yc in range(0, H_ + 1, 10):
        texto(c, gx - 6, P(0, yc)[1] + 2, str(yc), 'P', 5.8, MUTED, 'right')
    for xc in range(0, W_ + 1):
        linea(c, P(xc, 0)[0], gy, P(xc, 0)[0], gy + (2 if xc % 5 else 3.5), INK, 0.4)
    for yc in range(0, H_ + 1):
        linea(c, gx, P(0, yc)[1], gx + (2 if yc % 5 else 3.5), P(0, yc)[1], INK, 0.4)
    # doblez
    if pieza.get('doblez'):
        linea(c, *P(0, 0), *P(0, H_), INK, 2.2)
    # líneas de talla
    for t in TALLAS:
        pts = [P(x, y) for x, y in pieza['contornos'][t]]
        poligono(c, pts, stroke=TALLA_COLOR[t], lw=1.15, dash=TALLA_DASH[t], cerrado=pieza.get('cerrado', False))
        for x, y in pieza.get('puntos', {}).get(t, []):
            c.setFillColor(TALLA_COLOR[t]); c.circle(*(lambda p: (p[0], Y(p[1])))(P(x, y)), 1.1, fill=1, stroke=0)
    # hilo
    if pieza.get('hilo'):
        hx, h1, h2 = pieza['hilo']
        flecha(c, *P(hx, h1), *P(hx, h2), INK, 0.7, 3.5, dos=True)
        texto(c, P(hx, 0)[0] + 5, P(0, (h1 + h2) / 2)[1], 'HILO', 'PB', 5.5, INK)
    if pieza.get('doblez'):
        texto(c, P(0, 0)[0] + 4, P(0, H_)[1] - 10, 'DOBLEZ', 'PB', 5.8, INK)
    for m in pieza.get('marcas', []):
        texto(c, P(m[0], 0)[0], P(0, m[1])[1], m[2], 'PB', 5.8, INK)
    for s, (x, y), dx, dy in pieza['letras']:
        px, py = P(x, y)
        letra(c, px + dx, py + dy, s)
    # cajas de medidas a la derecha, con línea guía
    bx, bw = gx + W_ * ESCALA + 20, PW - ML - (gx + W_ * ESCALA + 20)
    bx = max(bx, ML + 300); bw = PW - ML - bx
    ocupado = []
    for caja in pieza['cajas']:
        ax, ay = P(*caja['ancla'])
        yb = caja.get('y', ay - 18)
        for o in ocupado:
            if abs(yb - o) < 42:
                yb = o + 42
        ocupado.append(yb)
        linea(c, ax, ay, bx, yb + 18, MUTED, 0.4)
        c.setFillColor(ACC); c.circle(ax, Y(ay), 1.6, fill=1, stroke=0)
        caja_medida(c, bx, yb, bw, caja['titulo'], caja['ref'], caja['vals'])
    yb = max([gy + H_ * ESCALA] + [o + 37 for o in ocupado]) + 22
    leyenda_tallas(c, yb)
    barra_escala(c, yb + 28)
    yy = tamanos_pieza(c, yb + 60, pieza['dims'])
    consejo(c, yy + 14, 'Cómo copiarlo', pieza['nota'])


def ejes_xy(c, x, y):
    """Dibujito del sistema de coordenadas (0,0) arriba a la izquierda."""
    rrect(c, x, y, 128, 118, 10, fill=CREAM)
    ox, oy = x + 26, y + 30
    flecha(c, ox, oy, ox + 88, oy, INK, 0.8, 3.5)
    flecha(c, ox, oy, ox, oy + 76, INK, 0.8, 3.5)
    texto(c, ox + 86, oy - 5, 'x', 'PB', 7, INK)
    texto(c, ox - 12, oy + 76, 'y', 'PB', 7, INK)
    texto(c, ox + 4, oy + 9, '(0, 0)', 'P', 5.5, MUTED)
    px, py = ox + 58, oy + 46
    linea(c, px, oy, px, py, ACC_D, 0.6, [2, 2]); linea(c, ox, py, px, py, ACC_D, 0.6, [2, 2])
    texto(c, ox + 30, oy - 5, 'x', 'PB', 7, ACC_D); texto(c, ox - 12, oy + 26, 'y', 'PB', 7, ACC_D)
    c.setFillColor(ACC); c.circle(px, Y(py), 3.2, fill=1, stroke=0)
    texto(c, px + 6, py + 3, 'punto', 'PB', 6.5, ACC_D)


def pagina_coordenadas(c, titulo, filas, nota, pasos=None):
    """filas = [(letra, descripcion, {talla:(x,y)}, es_curva)]."""
    cabecera(c, 'Coordenadas en cm', f'{titulo} · puntos de trazado')
    ejes_xy(c, ML, 82)
    pasos = pasos or [
        'Marca en tu papel la esquina superior izquierda: es el punto <b>(0, 0)</b>. El lado izquierdo es el doblez.',
        'Para cada punto de tu talla, mide <b>x</b> hacia la derecha y <b>y</b> hacia abajo con la regla y marca un punto.',
        'Une los puntos con regla (rectas). Los puntos <b>c1, c2…</b> (cuello) y <b>s1, s2…</b> (sisa y copa) forman una <b>curva</b>: únelos con una línea suave, a mano o con una regla flexible.',
        'Dibuja una paralela con el <b>margen de costura</b> de cada borde (lo tienes en la página de símbolos) y recorta.',
    ]
    lista_numerada(c, ML + 145, 84, CW - 145, pasos, 8.3, 5)
    y = 214
    x0 = ML; w = CW
    cP, cD = 36, 160
    cw = (w - cP - cD) / 10
    rrect(c, x0, y, w, 30, 6, fill=INK)
    texto(c, x0 + 8, y + 19, 'Punto', 'PS', 7.6, white)
    texto(c, x0 + cP + 4, y + 19, 'Dónde está', 'PS', 7.6, white)
    for i, t in enumerate(TALLAS):
        cx = x0 + cP + cD + cw * (2 * i + 1)
        pastilla(c, cx, y + 9, t)
        texto(c, cx - cw / 2, y + 25, 'x', 'P', 6, white, 'center')
        texto(c, cx + cw / 2, y + 25, 'y', 'P', 6, white, 'center')
    yy = y + 30
    fh = 16.5
    for k, (L_, desc, pts, curva) in enumerate(filas):
        if k % 2 == 0:
            c.setFillColor(CREAM); c.rect(x0, Y(yy + fh), w, fh, fill=1, stroke=0)
        texto(c, x0 + 8, yy + 11, L_, 'PB' if not curva else 'PS', 7.6, ACC_D if not curva else MUTED)
        texto(c, x0 + cP + 4, yy + 11, desc, 'P', 6.8, INK if not curva else MUTED)
        for i, t in enumerate(TALLAS):
            cx = x0 + cP + cD + cw * (2 * i + 1)
            px, py = pts[t]
            texto(c, cx - cw / 2, yy + 11, fmt(px), 'PM', 7.3, TALLA_COLOR[t], 'center')
            texto(c, cx + cw / 2, yy + 11, fmt(py), 'PM', 7.3, TALLA_COLOR[t], 'center')
        yy += fh
    linea(c, x0, yy, x0 + w, yy, GRID, 0.6)
    parrafo(c, ML, yy + 12, CW, nota, 7.6, MUTED)


# ---------------------------------------------------------------- geometría
def bezier(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        out.append((u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
    return out


def longitud(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


def muestras(pts, k):
    """k puntos intermedios repartidos por longitud a lo largo de una polilínea."""
    L = longitud(pts); out = []
    acc = [0]
    for i in range(len(pts) - 1):
        acc.append(acc[-1] + math.dist(pts[i], pts[i + 1]))
    for j in range(1, k + 1):
        tgt = L * j / (k + 1)
        for i in range(len(acc) - 1):
            if acc[i + 1] >= tgt:
                f = (tgt - acc[i]) / (acc[i + 1] - acc[i])
                out.append((pts[i][0] + f * (pts[i + 1][0] - pts[i][0]), pts[i][1] + f * (pts[i + 1][1] - pts[i][1])))
                break
    return out


def r1(v):
    return round(v * 10) / 10
