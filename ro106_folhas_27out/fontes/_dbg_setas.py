import fitz, numpy as np, sys
W = r'C:\IALD\Central de Patentes\work\ro106_folhas_27out'
for nome in (W + r'\_tmp\base\apr_antes.pdf', W + r'\FOLHAS_SUBSTITUTIVAS_050576.pdf'):
    d = fitz.open(nome)
    pg = d[0]
    print(nome)
    for w in pg.get_text('words'):
        if w[4] in ('[1]', '[3]', '[4]', '[5]'):
            print('  word', w[4], [round(v * 2.54 / 72, 2) for v in w[:4]])
    n = 0
    for dr in pg.get_drawings():
        if dr['type'] in ('f', 'fs') and dr.get('fill') == (0.0, 0.0, 0.0):
            r = dr['rect']
            if r.width * r.height < 25 * 25:
                pts = []
                for it in dr['items']:
                    if it[0] == 'l':
                        pts += [(it[1].x, it[1].y), (it[2].x, it[2].y)]
                    elif it[0] == 'c':
                        pts += [(it[1].x, it[1].y), (it[4].x, it[4].y)]
                if not pts:
                    continue
                c = np.mean(pts, axis=0)
                print('  head', [round(v * 2.54 / 72, 2) for v in c], 'n', len(dr['items']), 'w/h cm', round(r.width * 2.54 / 72, 2), round(r.height * 2.54 / 72, 2))
                n += 1
        if n > 30:
            break
