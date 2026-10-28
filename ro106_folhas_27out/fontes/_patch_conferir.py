import pathlib
p = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes\conferir.py')
s = p.read_text(encoding='utf-8')
add = r'''

TALL = re.compile('[A-Z0-9bdfhkl\u03b2\u03b8\u03c6\u2113\u03b4\u03bb\u03b6\u03be\u03c8\u03c7\u0394\u0393\u0398\u039b\u039e\u03a0\u03a3\u03a6\u03a8\u03a9]')


def linhas_texto_altura(pg, dpi=600):
    """Altura MEDIDA no render: por linha de texto vivo, a maior componente conexa de glifo (linha posta na posicao de leitura).
    Linhas com maiuscula/algarismo/ascendente entram no criterio 0,32 cm; as so com letras sem haste (altura-x) ficam listadas a parte."""
    import math
    g = render_gray(pg, dpi, aa=True)
    pxcm = dpi / 2.54
    k = dpi / 72.0
    out = []
    for b in pg.get_text('dict')['blocks']:
        if b.get('type') != 0:
            continue
        for ln in b['lines']:
            txt = ''.join(s['text'] for s in ln['spans']).strip()
            if not txt:
                continue
            x0, y0, x1, y1 = ln['bbox']
            c = g[max(0, int(y0 * k) - 3):int(y1 * k) + 3, max(0, int(x0 * k) - 3):int(x1 * k) + 3] < 128
            dx, dy = ln['dir']
            ang = math.degrees(math.atan2(dy, dx))
            if abs(ang) > 0.5:
                best = None
                for sgn in (1, -1):
                    r = ndi.rotate(c.astype(np.uint8), sgn * ang, reshape=True, order=0) > 0
                    ys, xs = np.where(r)
                    if len(ys) == 0:
                        continue
                    asp = (xs.max() - xs.min() + 1) / float(ys.max() - ys.min() + 1)
                    if best is None or asp > best[0]:
                        best = (asp, r)
                if best is None:
                    continue
                c = best[1]
            lab, n = ndi.label(c, structure=np.ones((3, 3)))
            hs = []
            for sl in ndi.find_objects(lab):
                if sl is None:
                    continue
                h = sl[0].stop - sl[0].start
                w = sl[1].stop - sl[1].start
                if h < 0.12 * pxcm:
                    continue
                if w > 3.2 * h and w > 0.8 * pxcm:
                    continue
                if h > 1.0 * pxcm:
                    continue
                hs.append(h)
            if not hs:
                continue
            cls = 'cap_alg_asc' if TALL.search(txt) else 'so_altura_x'
            out.append({'texto': txt, 'h_max_cm': round(max(hs) / pxcm, 3), 'classe': cls,
                        'caixa_cm': [round(v * 2.54 / 72, 2) for v in ln['bbox']]})
    return out


def cruzamentos(pg):
    """Vetorial: palavra cruzada por traco desenhado (texto sobre linha) e palavra sobre palavra."""
    import math
    segs = []
    for d in pg.get_drawings():
        if d.get('color') is None or d.get('type') not in ('s', 'fs'):
            continue
        for it in d['items']:
            if it[0] == 'l':
                segs.append((it[1], it[2]))
            elif it[0] == 're':
                r = it[1]
                P = [fitz.Point(r.x0, r.y0), fitz.Point(r.x1, r.y0), fitz.Point(r.x1, r.y1), fitz.Point(r.x0, r.y1)]
                segs += [(P[j], P[(j + 1) % 4]) for j in range(4)]
            elif it[0] == 'qu':
                q = it[1]
                P = [q.ul, q.ur, q.lr, q.ll]
                segs += [(P[j], P[(j + 1) % 4]) for j in range(4)]
            elif it[0] == 'c':
                p1, p2, p3, p4 = it[1:5]
                pts = []
                for t in np.linspace(0, 1, 13):
                    x = (1 - t) ** 3 * p1.x + 3 * (1 - t) ** 2 * t * p2.x + 3 * (1 - t) * t ** 2 * p3.x + t ** 3 * p4.x
                    y = (1 - t) ** 3 * p1.y + 3 * (1 - t) ** 2 * t * p2.y + 3 * (1 - t) * t ** 2 * p3.y + t ** 3 * p4.y
                    pts.append(fitz.Point(x, y))
                segs += [(pts[j], pts[j + 1]) for j in range(12)]
    words = pg.get_text('words')
    cross = []
    for w in words:
        r = fitz.Rect(w[:4])
        hh, ww = r.height, r.width
        rs = fitz.Rect(r.x0 + 0.04 * ww, r.y0 + 0.22 * hh, r.x1 - 0.04 * ww, r.y1 - 0.22 * hh)
        for a, b in segs:
            L = math.hypot(b.x - a.x, b.y - a.y)
            n = max(2, int(L / 0.7))
            hit = False
            for t in np.linspace(0, 1, n):
                x = a.x + t * (b.x - a.x)
                y = a.y + t * (b.y - a.y)
                if rs.x0 <= x <= rs.x1 and rs.y0 <= y <= rs.y1:
                    hit = True
                    break
            if hit:
                cross.append({'palavra': w[4], 'caixa_cm': [round(v * 2.54 / 72, 2) for v in w[:4]]})
                break
    over = []
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            a, b = fitz.Rect(words[i][:4]), fitz.Rect(words[j][:4])
            ii = a & b
            if not ii.is_empty and ii.get_area() > 0.25 * min(a.get_area(), b.get_area()):
                over.append({'a': words[i][4], 'b': words[j][4], 'caixa_cm': [round(v * 2.54 / 72, 2) for v in tuple(ii)]})
    return cross, over
'''
marker = "\n\ndef conferir(pdf, label, ref_pdf=None, rotated=()):"
assert s.count(marker) == 1
s = s.replace(marker, add + marker)
m2 = "        # legendas (Figura N) por texto vivo"
assert s.count(m2) == 1
s = s.replace(m2, """        lt = linhas_texto_altura(pg)
        capl = [x for x in lt if x['classe'] == 'cap_alg_asc']
        xl = [x for x in lt if x['classe'] == 'so_altura_x']
        f['altura_por_linha_texto_vivo'] = {
            'n_linhas_cap_alg_asc': len(capl),
            'h_min_cap_alg_asc_cm': min([x['h_max_cm'] for x in capl]) if capl else None,
            'linhas_abaixo_032_cap_alg_asc': [x for x in capl if x['h_max_cm'] < 0.32],
            'n_linhas_so_altura_x': len(xl),
            'so_altura_x_abaixo_032': [x for x in xl if x['h_max_cm'] < 0.32]}
        cr, ov = cruzamentos(pg)
        f['texto_cruzado_por_traco'] = cr
        f['texto_sobre_texto'] = ov
""" + m2)
m3 = "    out['resumo'] = {'altura_minima_de_linha_cm_todas_as_folhas': glob_min,"
assert s.count(m3) == 1
s = s.replace(m3, """    hm = [f['altura_por_linha_texto_vivo']['h_min_cap_alg_asc_cm'] for f in out['folhas'] if f['altura_por_linha_texto_vivo']['h_min_cap_alg_asc_cm'] is not None]
    out['resumo'] = {'altura_minima_cap_alg_asc_cm_todas_as_folhas_texto_vivo': min(hm) if hm else None,
                     'linhas_abaixo_032_cap_alg_asc_total': sum(len(f['altura_por_linha_texto_vivo']['linhas_abaixo_032_cap_alg_asc']) for f in out['folhas']),
                     'palavras_cruzadas_por_traco_total': sum(len(f['texto_cruzado_por_traco']) for f in out['folhas']),
                     'palavras_sobrepostas_total': sum(len(f['texto_sobre_texto']) for f in out['folhas']),
                     'altura_minima_de_linha_cm_metodo_A5': glob_min,""")
m4 = "        print(f['folha'], f['tamanho_cm'], 'margens', f['margens_medidas_cm'], 'ok' if f['margens_ok'] else 'FALHA',"
assert s.count(m4) == 1
s = s.replace(m4, """        al = f['altura_por_linha_texto_vivo']
        print(f['folha'], 'h_min(vivo,cap/alg/asc)', al['h_min_cap_alg_asc_cm'], 'abaixo', len(al['linhas_abaixo_032_cap_alg_asc']), 'xheight<0.32', len(al['so_altura_x_abaixo_032']), 'cruz', len(f['texto_cruzado_por_traco']), 'sobre', len(f['texto_sobre_texto']))
        print('  ', f['tamanho_cm'], 'margens', {k: float(v) for k, v in f['margens_medidas_cm'].items()}, 'ok' if f['margens_ok'] else 'FALHA',""")
p.write_text(s, encoding='utf-8')
print('patched')
