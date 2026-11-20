"""Geometría de la bermuda de hombre H-032 (tallas XS-XL), en cm.
Coordenadas de cada pieza: x hacia la derecha, y hacia abajo desde el borde de arriba (unión con la cinturilla).
Línea de costura sin margen; cut_outline() añade el margen."""
from shapely.geometry import LineString
from geo import catmull, cut_outline

SIZES = ['XS', 'S', 'M', 'L', 'XL']
HIP_BODY = dict(zip(SIZES, [92, 100, 108, 116, 124]))      # cadera del cuerpo (límite alto)
WAIST_BODY = dict(zip(SIZES, [76, 84, 92, 100, 108]))      # cintura del cuerpo (límite alto)
EASE = 10                                                   # holgura de cadera: bermuda relajada
RISE = dict(zip(SIZES, [23, 23.5, 24, 24.5, 25]))          # del borde de arriba a la línea de entrepierna
LEN = dict(zip(SIZES, [49, 50.5, 52, 53.5, 55]))           # del borde de arriba al bajo (sin cinturilla)
OPENING = dict(zip(SIZES, [54, 57, 60, 63, 66]))           # contorno de la boca de la pierna
BAND_H = 4                                                  # alto de la cinturilla terminada
SA = {'top': 1.0, 'side': 1.5, 'hem': 3.5, 'inseam': 1.5, 'crotch': 1.5, 'pocket': 1.0}


def qbez(p0, c, p1, n=24):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1]) for t in [i / n for i in range(n + 1)]]


def params(s):
    H = HIP_BODY[s] + EASE
    return H, RISE[s], LEN[s], OPENING[s]


def front_seam(s):
    H, R, L, O = params(s)
    fe, fw = H / 16, H / 4 - 1
    W = fe + fw
    hem = O / 2 - 1
    xi = (W - hem) * .62
    xo = xi + hem
    top = [(fe, 0), (W, 0)]
    side = [(W, 0), (W, .55 * R), (xo, L)]
    hemL = [(xo, L), (xi, L)]
    ins = [(xi, L), (0, R)]
    curve = qbez((0, R), (fe, R), (fe, R - fe))
    crotch = curve + [(fe, 0)]
    return {'top': top, 'side': side, 'hem': hemL, 'inseam': ins, 'crotch': crotch}


def back_seam(s):
    H, R, L, O = params(s)
    fe = H / 16
    be, bw = 1.7 * fe, H / 4 + 1
    W = be + bw
    hem = O / 2 + 1
    xi = (W - hem) * .62
    xo = xi + hem
    drop = .5
    cbt = (be + 2, -2.5)                 # centro de la espalda arriba: más alto y metido hacia dentro
    yh = .6 * R
    # recta del tiro trasero: de cbt hacia (be, yh), prolongada
    def on_cb(y):
        return cbt[0] + (be - cbt[0]) * (y - cbt[1]) / (yh - cbt[1])
    y1 = R - .5 * be
    p1 = (on_cb(y1), y1)
    ctrl = (on_cb(R + drop), R + drop)
    top = [cbt, (W, 0)]
    side = [(W, 0), (W, .55 * R), (xo, L)]
    hemL = [(xo, L), (xi, L)]
    ins = [(xi, L), (0, R + drop)]
    curve = qbez((0, R + drop), ctrl, p1)
    crotch = curve + [cbt]
    return {'top': top, 'side': side, 'hem': hemL, 'inseam': ins, 'crotch': crotch}


ORDER = ['top', 'side', 'hem', 'inseam', 'crotch']


def piece(s, back=False):
    e = back_seam(s) if back else front_seam(s)
    seam = []
    for k in ORDER:
        seam += e[k][:-1]
    edges = [(e[k], SA[k]) for k in ORDER]
    cut = cut_outline(edges, seam + [e['top'][0]])
    segs = dict(zip(ORDER, cut_outline.last_segs))
    return {'seam': seam, 'cut': cut, 'segs': segs, 'edges': e}


# Bolsillo (talla única): el borde recto x=0 va en el costado
POCKET_SEAM_CURVE = catmull([(0, 0), (11, 0), (15, 4.5), (16.5, 13), (15.5, 21), (11.5, 26), (5, 27.5), (0, 25)], n=10)
POCKET_OPEN = (2.0, 18.0)       # boca del bolsillo, medida desde el borde de arriba del pantalón


def pocket():
    curve = POCKET_SEAM_CURVE
    straight = [(0, 25), (0, 0)]
    edges = [(curve, SA['pocket']), (straight, SA['side'])]
    cut = cut_outline(edges, curve[:-1] + straight)
    return {'seam': curve[:-1] + straight, 'cut': cut, 'segs': dict(zip(['curve', 'straight'], cut_outline.last_segs))}


def length(pts):
    return LineString(pts).length


def measures(s):
    f, b = front_seam(s), back_seam(s)
    ftop, btop = length(f['top']), length(b['top'])
    H, R, L, O = params(s)
    return {
        'ftop': ftop, 'btop': btop,
        'waist_relaxed': 2 * (ftop + btop),
        'hip': H,
        'side_f': length(f['side']), 'side_b': length(b['side']),
        'ins_f': length(f['inseam']), 'ins_b': length(b['inseam']),
        'rise_f': length(f['crotch']), 'rise_b': length(b['crotch']),
        'opening': O,
        'band_cut_half': round((ftop + btop) / 2 + 1, 1),   # cinturilla: media pieza al doblez, con 1 cm de margen en el extremo
        'band_cut_h': BAND_H * 2 + 2 * SA['top'],
        'elastic': round(WAIST_BODY[s] * .92) + 2,
    }


if __name__ == '__main__':
    for s in SIZES:
        m = measures(s)
        pf, pb = piece(s), piece(s, True)
        bb = lambda pts: [round(min(p[0] for p in pts), 1), round(max(p[0] for p in pts), 1), round(min(p[1] for p in pts), 1), round(max(p[1] for p in pts), 1)]
        print(s, {k: round(v, 1) for k, v in m.items()}, 'del', bb(pf['cut']), 'tras', bb(pb['cut']))
    print('bolsillo', [round(v, 1) for v in [min(p[0] for p in pocket()['cut']), max(p[0] for p in pocket()['cut']), min(p[1] for p in pocket()['cut']), max(p[1] for p in pocket()['cut'])]])
