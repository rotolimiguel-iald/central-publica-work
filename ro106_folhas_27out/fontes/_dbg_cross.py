import fitz, math
import numpy as np
pg = fitz.open(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\_tmp\mqc_folhas\mqc_folhas.pdf')[1]
dr = pg.get_drawings()
words = [w for w in pg.get_text('words') if w[4] == 'Coerência'][:1]
w = words[0]
r = fitz.Rect(w[:4])
hh, ww = r.height, r.width
rs = fitz.Rect(r.x0 + 0.22 * ww, r.y0 + 0.04 * hh, r.x1 - 0.22 * ww, r.y1 - 0.04 * hh)
print('rs', [round(v * 2.54 / 72, 2) for v in rs])
for d in dr:
    if d.get('color') is None or d.get('type') not in ('s', 'fs'):
        continue
    for it in d['items']:
        pts = []
        if it[0] == 'l':
            pts = [(it[1], it[2])]
        elif it[0] == 're':
            q = it[1]
            P = [fitz.Point(q.x0, q.y0), fitz.Point(q.x1, q.y0), fitz.Point(q.x1, q.y1), fitz.Point(q.x0, q.y1)]
            pts = [(P[j], P[(j + 1) % 4]) for j in range(4)]
        for a, b in pts:
            L = math.hypot(b.x - a.x, b.y - a.y)
            n = max(2, int(L / 0.7))
            for t in np.linspace(0, 1, n):
                x = a.x + t * (b.x - a.x)
                y = a.y + t * (b.y - a.y)
                if rs.x0 <= x <= rs.x1 and rs.y0 <= y <= rs.y1:
                    print('HIT', d['type'], d.get('color'), d.get('width'), it[0], [round(v * 2.54 / 72, 2) for v in (a.x, a.y, b.x, b.y)])
                    break
