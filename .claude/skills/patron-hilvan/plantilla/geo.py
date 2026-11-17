"""Geometría del patrón de camiseta H-031 (tallas XS-XL), en cm.
Los datos de costura vienen del patrón original (coordenadas, sin margen).
Aquí se suavizan las curvas y se añade el margen de costura para obtener la línea de corte."""
from shapely.geometry import LineString, Polygon, Point
from shapely.ops import substring

SIZES = ['XS', 'S', 'M', 'L', 'XL']

# ---------- Datos de costura (x hacia la derecha, y hacia abajo) ----------
FRONT_NECK = {  # A, c1..c7
    'XS': [(0, 8), (1.6, 7.9), (3.2, 7.4), (4.6, 6.7), (5.9, 5.7), (7, 4.5), (7.8, 3.1), (8.3, 1.6)],
    'S':  [(0, 8.2), (1.7, 8.1), (3.3, 7.7), (4.8, 6.9), (6.1, 5.9), (7.2, 4.7), (8, 3.2), (8.6, 1.7)],
    'M':  [(0, 8.5), (1.7, 8.3), (3.4, 7.9), (4.9, 7.1), (6.3, 6.1), (7.4, 4.8), (8.3, 3.3), (8.8, 1.7)],
    'L':  [(0, 8.8), (1.8, 8.6), (3.5, 8.1), (5, 7.3), (6.4, 6.3), (7.6, 5), (8.5, 3.4), (9.1, 1.8)],
    'XL': [(0, 9), (1.8, 8.8), (3.6, 8.3), (5.2, 7.5), (6.6, 6.4), (7.8, 5.1), (8.7, 3.5), (9.3, 1.8)],
}
BACK_NECK = {
    'XS': [(0, 2), (1.1, 2), (2.3, 1.9), (3.4, 1.8), (4.5, 1.7), (5.6, 1.5), (6.7, 1.2), (7.8, .8)],
    'S':  [(0, 2), (1.2, 2), (2.3, 1.9), (3.5, 1.8), (4.6, 1.7), (5.8, 1.5), (6.9, 1.2), (8, .8)],
    'M':  [(0, 2), (1.2, 2), (2.4, 1.9), (3.6, 1.8), (4.8, 1.7), (5.9, 1.5), (7.1, 1.2), (8.2, .8)],
    'L':  [(0, 2), (1.2, 2), (2.4, 1.9), (3.7, 1.8), (4.9, 1.7), (6.1, 1.5), (7.3, 1.2), (8.4, .8)],
    'XL': [(0, 2), (1.3, 2), (2.5, 1.9), (3.8, 1.8), (5, 1.7), (6.2, 1.5), (7.5, 1.2), (8.6, .8)],
}
B = {'XS': (8.5, 0), 'S': (8.8, 0), 'M': (9, 0), 'L': (9.2, 0), 'XL': (9.5, 0)}
C = {'XS': (21, 4), 'S': (22, 4), 'M': (23, 4), 'L': (24, 4), 'XL': (25, 4)}
ARMHOLE = {  # s1..s8
    'XS': [(20.8, 6.1), (20.7, 8.3), (20.7, 10.4), (20.7, 12.5), (20.8, 14.7), (21.1, 16.8), (21.5, 18.9), (22.3, 20.9)],
    'S':  [(21.8, 6.3), (21.7, 8.6), (21.7, 10.9), (21.8, 13.2), (21.9, 15.5), (22.3, 17.8), (22.9, 20), (24, 22)],
    'M':  [(22.8, 6.5), (22.7, 9), (22.7, 11.4), (22.8, 13.9), (23, 16.4), (23.5, 18.8), (24.3, 21.2), (25.7, 23.2)],
    'L':  [(23.8, 6.7), (23.7, 9.3), (23.7, 12), (23.9, 14.6), (24.2, 17.3), (24.7, 19.9), (25.7, 22.3), (27.5, 24.3)],
    'XL': [(24.8, 6.8), (24.7, 9.7), (24.8, 12.5), (24.9, 15.3), (25.3, 18.1), (26, 20.9), (27.2, 23.4), (29.3, 25.3)],
}
D = {'XS': (24, 22), 'S': (26, 23), 'M': (28, 24), 'L': (30, 25), 'XL': (32, 26)}
E = {'XS': (24, 68), 'S': (26, 70), 'M': (28, 72), 'L': (30, 74), 'XL': (32, 76)}

SLEEVE_CAP = {  # A, s1..s8, B
    'XS': [(0, 0), (2.1, .1), (4.3, .4), (6.4, .8), (8.4, 1.5), (10.4, 2.3), (12.2, 3.3), (14, 4.5), (15.6, 5.9), (17.1, 7.5)],
    'S':  [(0, 0), (2.3, .1), (4.6, .4), (6.9, .9), (9.1, 1.6), (11.2, 2.4), (13.2, 3.5), (15.1, 4.8), (16.9, 6.3), (18.5, 8)],
    'M':  [(0, 0), (2.5, .1), (4.9, .4), (7.4, .9), (9.7, 1.6), (12, 2.6), (14.2, 3.8), (16.3, 5.1), (18.2, 6.7), (19.9, 8.5)],
    'L':  [(0, 0), (2.7, .1), (5.3, .4), (7.9, 1), (10.4, 1.7), (12.9, 2.7), (15.3, 4), (17.5, 5.4), (19.5, 7.1), (21.4, 9)],
    'XL': [(0, 0), (2.8, .1), (5.7, .4), (8.4, 1), (11.2, 1.8), (13.8, 2.9), (16.3, 4.2), (18.7, 5.7), (20.9, 7.5), (22.9, 9.5)],
}
SLEEVE_CUFF = {'XS': (15.6, 19), 'S': (17, 20), 'M': (18.4, 21), 'L': (19.9, 22), 'XL': (21.4, 23)}

# Márgenes de costura (cm)
SA = {'neck': 1.0, 'shoulder': 1.5, 'armhole': 1.5, 'side': 1.5, 'hem': 2.5, 'fold': 0.0,
      'cap': 1.5, 'underarm': 1.5, 'cuff': 2.5}


# ---------- Utilidades ----------
def catmull(pts, n=14, start_tangent_pt=None):
    """Curva suave que pasa por todos los puntos (Catmull-Rom)."""
    P = list(pts)
    first = start_tangent_pt if start_tangent_pt else (2 * P[0][0] - P[1][0], 2 * P[0][1] - P[1][1])
    last = (2 * P[-1][0] - P[-2][0], 2 * P[-1][1] - P[-2][1])
    ext = [first] + P + [last]
    out = []
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            x = .5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = .5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(P[-1])
    return out


def _extend(line, L=15):
    c = list(line.coords)
    (x0, y0), (x1, y1) = c[0], c[1]
    d = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** .5 or 1
    s = (x0 - (x1 - x0) / d * L, y0 - (y1 - y0) / d * L)
    (xa, ya), (xb, yb) = c[-2], c[-1]
    d = ((xb - xa) ** 2 + (yb - ya) ** 2) ** .5 or 1
    e = (xb + (xb - xa) / d * L, yb + (yb - ya) / d * L)
    return LineString([s] + c + [e])


def _nearest(geom, ref):
    pts = []
    if geom.is_empty:
        return None
    if geom.geom_type == 'Point':
        pts = [geom]
    elif hasattr(geom, 'geoms'):
        for g in geom.geoms:
            if g.geom_type == 'Point':
                pts.append(g)
            else:
                pts += [Point(c) for c in g.coords]
    else:
        pts = [Point(c) for c in geom.coords]
    return min(pts, key=lambda p: p.distance(Point(ref)))


def cut_outline(edges, closed_poly):
    """edges: lista de (polilínea de costura, margen). Devuelve la línea de corte cerrada."""
    poly = Polygon(closed_poly)
    offs = []
    for pts, d in edges:
        ln = LineString(pts)
        if d == 0:
            o = ln
        else:
            o = ln.offset_curve(d, join_style='mitre', mitre_limit=3)
            mid = o.interpolate(.5, normalized=True)
            if poly.contains(mid):
                o = ln.offset_curve(-d, join_style='mitre', mitre_limit=3)
            if o.geom_type == 'MultiLineString':
                o = max(o.geoms, key=lambda g: g.length)
            # offset_curve puede invertir el sentido: lo alineamos con la costura
            if Point(o.coords[0]).distance(Point(pts[0])) > Point(o.coords[-1]).distance(Point(pts[0])):
                o = LineString(list(o.coords)[::-1])
        offs.append(_extend(o))
    n = len(offs)
    corners = []
    for i in range(n):
        a, b = offs[i], offs[(i + 1) % n]
        ref = edges[i][0][-1]
        p = _nearest(a.intersection(b), ref)
        corners.append(p)
    out, segs = [], []
    for i in range(n):
        ln = offs[i]
        p0, p1 = corners[i - 1], corners[i]
        s, e = ln.project(p0), ln.project(p1)
        seg = list(substring(ln, s, e).coords)
        segs.append(seg)
        out += seg
    cut_outline.last_segs = segs
    return out


# ---------- Piezas ----------
def body(size, back=False):
    neck_pts = (BACK_NECK if back else FRONT_NECK)[size] + [B[size]]
    neck = catmull(neck_pts, start_tangent_pt=(-neck_pts[1][0], neck_pts[1][1]))
    shoulder = [B[size], C[size]]
    arm = catmull([C[size]] + ARMHOLE[size] + [D[size]])
    side = [D[size], E[size]]
    hem = [E[size], (0, E[size][1])]
    fold = [(0, E[size][1]), neck_pts[0]]
    seam = neck + arm + [E[size], (0, E[size][1])]
    edges = [(neck, SA['neck']), (shoulder, SA['shoulder']), (arm, SA['armhole']),
             (side, SA['side']), (hem, SA['hem']), (fold, SA['fold'])]
    cut = cut_outline(edges, seam)
    names = ['neck', 'shoulder', 'armhole', 'side', 'hem', 'fold']
    return {'seam': seam, 'cut': cut, 'segs': dict(zip(names, cut_outline.last_segs)), 'neck0': neck_pts[0], 'hemy': E[size][1]}


def sleeve(size):
    cap = SLEEVE_CAP[size]
    full = [(-x, y) for x, y in cap[::-1]] + cap[1:]
    capc = catmull(full)
    Bx, By = cap[-1]
    Cx, Cy = SLEEVE_CUFF[size]
    right = [(Bx, By), (Cx, Cy)]
    cuff = [(Cx, Cy), (-Cx, Cy)]
    left = [(-Cx, Cy), (-Bx, By)]
    seam = capc + [(Cx, Cy), (-Cx, Cy)]
    edges = [(capc, SA['cap']), (right, SA['underarm']), (cuff, SA['cuff']), (left, SA['underarm'])]
    cut = cut_outline(edges, seam)
    names = ['cap', 'right', 'cuff', 'left']
    return {'seam': seam, 'cut': cut, 'segs': dict(zip(names, cut_outline.last_segs)), 'cuffy': Cy}


def length(pts):
    return LineString(pts).length


if __name__ == '__main__':
    for s in SIZES:
        f = body(s); b = body(s, True); m = sleeve(s)
        neck_f = length(catmull(FRONT_NECK[s] + [B[s]], start_tangent_pt=(-FRONT_NECK[s][1][0], FRONT_NECK[s][1][1])))
        arm = length(catmull([C[s]] + ARMHOLE[s] + [D[s]]))
        cap = length(catmull([(-x, y) for x, y in SLEEVE_CAP[s][::-1]] + SLEEVE_CAP[s][1:])) / 2
        xs = [p[0] for p in f['cut']]; ys = [p[1] for p in f['cut']]
        mx = [p[0] for p in m['cut']]; my = [p[1] for p in m['cut']]
        print(s, 'cuello del', round(neck_f, 1), 'sisa', round(arm, 1), 'copa/2', round(cap, 1),
              '| delantero corte', round(min(xs), 1), round(max(xs), 1), round(min(ys), 1), round(max(ys), 1),
              '| manga', round(min(mx), 1), round(max(mx), 1), round(min(my), 1), round(max(my), 1))
