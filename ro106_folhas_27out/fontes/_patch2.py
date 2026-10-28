import pathlib, re
p = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes\conferir.py')
s = p.read_text(encoding='utf-8')
a = s.index('def cruzamentos(pg):')
b = s.index('\n\ndef conferir(pdf, label')
new = r'''def cruzamentos(pg):
    """Vetorial, com ordem de pintura: palavra cruzada por traco desenhado (que nao esteja coberto por preenchimento branco
    pintado depois) e palavra sobre palavra. Palavras inclinadas (nem horizontais nem verticais) vao para 'verificar_visualmente'."""
    import math
    dr = pg.get_drawings()
    segs = []      # (p, q, seq)
    whites = []    # (rect, seq)
    for d in dr:
        seq = d.get('seqno', 0)
        fill = d.get('fill')
        if fill is not None and tuple(round(float(x), 2) for x in fill) == (1.0, 1.0, 1.0):
            whites.append((d['rect'], seq))
        if d.get('color') is None or d.get('type') not in ('s', 'fs'):
            continue
        for it in d['items']:
            if it[0] == 'l':
                segs.append((it[1], it[2], seq))
            elif it[0] == 're':
                r = it[1]
                P = [fitz.Point(r.x0, r.y0), fitz.Point(r.x1, r.y0), fitz.Point(r.x1, r.y1), fitz.Point(r.x0, r.y1)]
                segs += [(P[j], P[(j + 1) % 4], seq) for j in range(4)]
            elif it[0] == 'qu':
                q = it[1]
                P = [q.ul, q.ur, q.lr, q.ll]
                segs += [(P[j], P[(j + 1) % 4], seq) for j in range(4)]
            elif it[0] == 'c':
                p1, p2, p3, p4 = it[1:5]
                pts = []
                for t in np.linspace(0, 1, 13):
                    x = (1 - t) ** 3 * p1.x + 3 * (1 - t) ** 2 * t * p2.x + 3 * (1 - t) * t ** 2 * p3.x + t ** 3 * p4.x
                    y = (1 - t) ** 3 * p1.y + 3 * (1 - t) ** 2 * t * p2.y + 3 * (1 - t) * t ** 2 * p3.y + t ** 3 * p4.y
                    pts.append(fitz.Point(x, y))
                segs += [(pts[j], pts[j + 1], seq) for j in range(12)]
    # direcao de cada palavra (pela linha que a contem)
    dirs = []
    for b_ in pg.get_text('dict')['blocks']:
        if b_.get('type') != 0:
            continue
        for ln in b_['lines']:
            dirs.append((fitz.Rect(ln['bbox']), ln['dir']))
    words = pg.get_text('words')
    cross, incl = [], []
    for w in words:
        if '\u221a' in w[4]:
            continue                      # radical: o vinculo faz parte do glifo
        r = fitz.Rect(w[:4])
        d = (1.0, 0.0)
        for lr, ldir in dirs:
            if (lr & r).get_area() > 0.5 * r.get_area():
                d = ldir
                break
        ang = abs(math.degrees(math.atan2(d[1], d[0])))
        hh, ww = r.height, r.width
        if ang < 1 or abs(ang - 180) < 1:
            rs = fitz.Rect(r.x0 + 0.04 * ww, r.y0 + 0.22 * hh, r.x1 - 0.04 * ww, r.y1 - 0.22 * hh)
        elif abs(ang - 90) < 1:
            rs = fitz.Rect(r.x0 + 0.22 * ww, r.y0 + 0.04 * hh, r.x1 - 0.22 * ww, r.y1 - 0.04 * hh)
        else:
            incl.append({'palavra': w[4], 'caixa_cm': [round(v * 2.54 / 72, 2) for v in w[:4]]})
            continue
        hit = False
        for a_, b2, seq in segs:
            L = math.hypot(b2.x - a_.x, b2.y - a_.y)
            n = max(2, int(L / 0.7))
            for t in np.linspace(0, 1, n):
                x = a_.x + t * (b2.x - a_.x)
                y = a_.y + t * (b2.y - a_.y)
                if rs.x0 <= x <= rs.x1 and rs.y0 <= y <= rs.y1:
                    covered = any(wr.contains(rs) and wseq > seq for wr, wseq in whites)
                    if not covered:
                        hit = True
                    break
            if hit:
                break
        if hit:
            cross.append({'palavra': w[4], 'caixa_cm': [round(v * 2.54 / 72, 2) for v in w[:4]]})
    over = []
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            a_, b2 = fitz.Rect(words[i][:4]), fitz.Rect(words[j][:4])
            ii = a_ & b2
            if not ii.is_empty and ii.get_area() > 0.25 * min(a_.get_area(), b2.get_area()):
                over.append({'a': words[i][4], 'b': words[j][4], 'caixa_cm': [round(v * 2.54 / 72, 2) for v in tuple(ii)]})
    return cross, over, incl'''
s = s[:a] + new + s[b:]
s = s.replace("cr, ov = cruzamentos(pg)\n        f['texto_cruzado_por_traco'] = cr", "cr, ov, incl = cruzamentos(pg)\n        f['texto_inclinado_verificar_visualmente'] = incl\n        f['texto_cruzado_por_traco'] = cr")
p.write_text(s, encoding='utf-8')
print('ok')
