"""
Geometría de la camiseta básica de hombre (cuello redondo, manga corta), tallas XS–XL.
Todas las medidas en cm, SIN margen de costura. Origen (0,0) arriba a la izquierda
de cada pieza; x hacia la derecha, y hacia abajo. El borde x = 0 es el doblez.
"""
import math
from plantilla import TALLAS, bezier, longitud, muestras, r1

# ---- Medidas del cuerpo (las mismas que la sudadera, para que la guía de tallas coincida)
PECHO = {'XS': (84, 88), 'S': (92, 96), 'M': (100, 104), 'L': (108, 112), 'XL': (116, 120)}
CINTURA = {'XS': (72, 76), 'S': (80, 84), 'M': (88, 92), 'L': (96, 100), 'XL': (104, 108)}
CADERA = {'XS': (88, 92), 'S': (96, 100), 'M': (104, 108), 'L': (112, 116), 'XL': (120, 124)}
ALTURA = {'XS': '164–170', 'S': '170–175', 'M': '175–180', 'L': '180–185', 'XL': '185–190'}

HOLGURA = 8          # cm sobre el pecho: camiseta cómoda, ni ceñida ni oversize
CAIDA_HOMBRO = 4     # cm que baja el hombro desde el cuello
MARGEN = 1.5         # margen general
MARGEN_CUELLO = 1    # escote y tira del cuello
DOBLADILLO = 2.5     # bajo del cuerpo y de la manga
TIRA_ALTO_FINAL = 2  # tira del cuello terminada
TIRA_PROPORCION = 0.85

idx = {t: i for i, t in enumerate(TALLAS)}
lin = lambda a, b: {t: a + b * i for i, t in enumerate(TALLAS)}   # a en XS, +b por talla

ANCHO_PLANO = {t: (PECHO[t][1] + HOLGURA) / 2 for t in TALLAS}  # 48..64
CUARTO = {t: ANCHO_PLANO[t] / 2 for t in TALLAS}                 # 24..32
LARGO = lin(68, 2)              # desde el punto alto del hombro (cuello) hasta el bajo
HOMBROS = lin(42, 2)            # ancho de hombros, de punta a punta
CUELLO_MEDIO = lin(8.5, 0.25)   # mitad del ancho del escote
ESCOTE_DEL = lin(8, 0.25)       # profundidad del escote delantero
ESCOTE_ESP = {t: 2 for t in TALLAS}
SISA = lin(22, 1)               # profundidad de sisa desde la línea del cuello
LARGO_MANGA = lin(19, 1)
ALTURA_COPA = lin(7.5, 0.5)


def cuello(t, prof, n=7):
    """Cuarto de elipse de A (0,prof) a B (ancho,0). Devuelve (curva densa, puntos c1..cn)."""
    b = CUELLO_MEDIO[t]
    dens = [(b * math.sin(a), prof * math.cos(a)) for a in [i / 60 * math.pi / 2 for i in range(61)]]
    return dens, muestras(dens, n)


def sisa(t, n=8):
    cx, cy = HOMBROS[t] / 2, CAIDA_HOMBRO
    dx, dy = CUARTO[t], SISA[t]
    dens = bezier((cx, cy), (cx - 0.8, cy + 0.5 * (dy - cy)), (cx - 0.2, dy), (dx, dy), 80)
    return dens, muestras(dens, n)


def copa(t, W, n=8):
    h = ALTURA_COPA[t]
    return bezier((0, 0), (0.45 * W, 0), (0.8 * W, 0.45 * h), (W, h), 80)


def resolver_manga(t):
    """Ancho de media manga para que la copa mida igual que la sisa."""
    La = longitud(sisa(t)[0])
    lo, hi = 5, 40
    for _ in range(60):
        mid = (lo + hi) / 2
        if longitud(copa(t, mid)) < La: lo = mid
        else: hi = mid
    return r1(mid)


def cuerpo(t, delantero=True):
    prof = ESCOTE_DEL[t] if delantero else ESCOTE_ESP[t]
    cdens, cpts = cuello(t, prof)
    sdens, spts = sisa(t)
    A = (0, prof); B = (CUELLO_MEDIO[t], 0); C = (HOMBROS[t] / 2, CAIDA_HOMBRO)
    D = (CUARTO[t], SISA[t]); E = (CUARTO[t], LARGO[t]); F = (0, LARGO[t])
    contorno = cdens + [C] + sdens + [E, F, A]
    puntos = {'A': A, 'B': B, 'C': C, 'D': D, 'E': E, 'F': F}
    for i, p in enumerate(cpts, 1): puntos[f'c{i}'] = p
    for i, p in enumerate(spts, 1): puntos[f's{i}'] = p
    med = {
        'hombro': math.dist(B, C), 'cuello': longitud(cdens), 'sisa': longitud(sdens),
        'centro': LARGO[t] - prof, 'costado': LARGO[t] - SISA[t], 'bajo': CUARTO[t],
    }
    return contorno, puntos, med


def manga(t):
    W = resolver_manga(t)
    h = ALTURA_COPA[t]; L = LARGO_MANGA[t]; Wb = W - 1.5
    cdens = copa(t, W)
    spts = muestras(cdens, 8)
    A, B, C, D = (0, 0), (W, h), (Wb, L), (0, L)
    contorno = cdens + [C, D, A]
    puntos = {'A': A}
    for i, p in enumerate(spts, 1): puntos[f's{i}'] = p
    puntos.update({'B': B, 'C': C, 'D': D})
    med = {'copa': longitud(cdens), 'bajomanga': math.dist(B, C), 'boca': Wb, 'ancho': W, 'centro': L}
    return contorno, puntos, med


def todo():
    R = {}
    for t in TALLAS:
        fd, pd, md = cuerpo(t, True)
        fe, pe, me = cuerpo(t, False)
        fm, pm, mm = manga(t)
        escote = 2 * md['cuello'] + 2 * me['cuello']
        tira_largo = round(TIRA_PROPORCION * escote) + 2 * MARGEN_CUELLO
        tira_alto = 2 * (TIRA_ALTO_FINAL + MARGEN_CUELLO)
        R[t] = dict(del_=(fd, pd, md), esp=(fe, pe, me), man=(fm, pm, mm), escote=escote,
                    tira=(tira_largo, tira_alto))
    return R


if __name__ == '__main__':
    R = todo()
    for t in TALLAS:
        _, pd, md = R[t]['del_']; _, pe, me = R[t]['esp']; _, pm, mm = R[t]['man']
        print(t, 'pecho plano', ANCHO_PLANO[t], 'largo', LARGO[t],
              '| sisa %.1f copa %.1f' % (md['sisa'], mm['copa']),
              '| manga ancho axila %.1f boca %.1f' % (2 * mm['ancho'], 2 * mm['boca']),
              '| hombro %.1f cuello del %.1f esp %.1f escote %.1f tira %s' % (md['hombro'], md['cuello'], me['cuello'], R[t]['escote'], R[t]['tira']))
