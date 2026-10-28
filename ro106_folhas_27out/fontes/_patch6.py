import pathlib
p = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes\conferir.py')
s = p.read_text(encoding='utf-8')
add = r'''

def _poly_of(items):
    """Poligono (lista de pontos) de um caminho preenchido, a partir dos itens do PyMuPDF."""
    pts = []
    for it in items:
        if it[0] == 're':
            r = it[1]
            pts += [(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1)]
        elif it[0] == 'qu':
            q = it[1]
            pts += [(q.ul.x, q.ul.y), (q.ur.x, q.ur.y), (q.lr.x, q.lr.y), (q.ll.x, q.ll.y)]
        elif it[0] == 'l':
            pts += [(it[1].x, it[1].y), (it[2].x, it[2].y)]
        elif it[0] == 'c':
            p1, p2, p3, p4 = it[1:5]
            for t in np.linspace(0, 1, 14):
                pts.append(((1 - t) ** 3 * p1.x + 3 * (1 - t) ** 2 * t * p2.x + 3 * (1 - t) * t ** 2 * p3.x + t ** 3 * p4.x,
                            (1 - t) ** 3 * p1.y + 3 * (1 - t) ** 2 * t * p2.y + 3 * (1 - t) * t ** 2 * p3.y + t ** 3 * p4.y))
    return pts


def oclusao(pg, min_pontos=3):
    """TESTE DE OCLUSAO (vetorial, em ordem de pintura): qualquer elemento opaco/de fundo branco que cubra traco ou marca de
    dado pintado ANTES dele. Conta pontos (amostrados a cada ~0,8 pt) de tracos/marcas dentro do poligono branco (reduzido 0,5 pt).
    Ignora: o fundo da pagina/tela (area > 40% da pagina) e o traco do proprio objeto."""
    from matplotlib.path import Path
    dr = pg.get_drawings(extended=True)
    pa = pg.rect.width * pg.rect.height
    strokes = []     # (seq, pts(np.array Nx2), eff, tipo)
    whites = []      # (seq, rect, polygon pts, eff)
    clips = {}
    for d in dr:
        if d['type'] == 'clip':
            lv = d.get('level', 0)
            clips[lv] = fitz.Rect(d['scissor'])
            for k in [k for k in clips if k > lv]:
                del clips[k]
            continue
        lv = d.get('level', 0)
        eff = None
        for k, rc in clips.items():
            if k < lv:
                eff = rc if eff is None else (eff & rc)
        seq = d.get('seqno', 0)
        fill = d.get('fill')
        isw = fill is not None and tuple(round(float(x), 2) for x in fill) == (1.0, 1.0, 1.0)
        isb = fill is not None and tuple(round(float(x), 2) for x in fill) == (0.0, 0.0, 0.0)
        rect = d['rect']
        if d['type'] in ('f', 'fs') and isw:
            if rect.width * rect.height > 0.40 * pa:
                pass
            else:
                whites.append((seq, rect, _poly_of(d['items']), eff))
        # tracos e marcas
        if d.get('color') is not None and d['type'] in ('s', 'fs'):
            samp = []
            for it in d['items']:
                segs = []
                if it[0] == 'l':
                    segs = [(it[1], it[2])]
                elif it[0] == 're':
                    r = it[1]
                    P = [fitz.Point(r.x0, r.y0), fitz.Point(r.x1, r.y0), fitz.Point(r.x1, r.y1), fitz.Point(r.x0, r.y1)]
                    segs = [(P[j], P[(j + 1) % 4]) for j in range(4)]
                elif it[0] == 'qu':
                    q = it[1]
                    P = [q.ul, q.ur, q.lr, q.ll]
                    segs = [(P[j], P[(j + 1) % 4]) for j in range(4)]
                elif it[0] == 'c':
                    pp = _poly_of([it])
                    segs = [(fitz.Point(*pp[j]), fitz.Point(*pp[j + 1])) for j in range(len(pp) - 1)]
                for a, b in segs:
                    L = max(abs(b.x - a.x), abs(b.y - a.y))
                    n = max(2, int(L / 0.8) + 1)
                    for t in np.linspace(0, 1, n):
                        samp.append((a.x + t * (b.x - a.x), a.y + t * (b.y - a.y)))
            if samp:
                strokes.append((seq, np.array(samp), eff, 'traco'))
        if d['type'] == 'f' and isb and rect.width * rect.height < 4.0 * 72 * 72 / 2.54 / 2.54:
            pp = _poly_of(d['items'])
            if pp:
                strokes.append((seq, np.array(pp), eff, 'marca preenchida'))
    out = []
    for seq, rect, poly, eff in whites:
        if len(poly) < 3:
            continue
        inset = fitz.Rect(rect.x0 + 0.5, rect.y0 + 0.5, rect.x1 - 0.5, rect.y1 - 0.5)
        if inset.is_empty:
            continue
        path = Path(np.array(poly))
        n_in = 0
        kinds = set()
        for sq, pts, eff2, tipo in strokes:
            if sq >= seq:
                continue
            m = (pts[:, 0] > inset.x0) & (pts[:, 0] < inset.x1) & (pts[:, 1] > inset.y0) & (pts[:, 1] < inset.y1)
            if not m.any():
                continue
            sub = pts[m]
            if eff2 is not None:
                m2 = (sub[:, 0] >= eff2.x0 - 0.01) & (sub[:, 0] <= eff2.x1 + 0.01) & (sub[:, 1] >= eff2.y0 - 0.01) & (sub[:, 1] <= eff2.y1 + 0.01)
                sub = sub[m2]
            if eff is not None and len(sub):
                m3 = (sub[:, 0] >= eff.x0 - 0.01) & (sub[:, 0] <= eff.x1 + 0.01) & (sub[:, 1] >= eff.y0 - 0.01) & (sub[:, 1] <= eff.y1 + 0.01)
                sub = sub[m3]
            if len(sub) == 0:
                continue
            ins = path.contains_points(sub)
            k = int(ins.sum())
            if k:
                n_in += k
                kinds.add(tipo)
        if n_in >= min_pontos:
            out.append({'fundo_branco_caixa_cm': [round(v * 2.54 / 72, 2) for v in rect], 'pontos_de_traco_cobertos': n_in, 'tipos': sorted(kinds)})
    return out


def marcacao_RO(pg):
    """O RO carimba cada folha de substituicao no canto superior direito (numero do pedido, data de recebimento) e na margem
    inferior (SUBSTITUTE SHEET (RULE 26)): essas areas tem de ficar LIVRES de tinta (render a 600 dpi, sem antialias)."""
    g6 = render_gray(pg, 600, aa=False)
    px = 600 / 2.54
    H, Wd = g6.shape
    ink = g6 < 255

    def n(x0, y0, x1, y1):
        return int(ink[int(y0 * px):int(y1 * px), int(x0 * px):int(x1 * px)].sum())
    wcm, hcm = Wd / px, H / px
    r = {'canto_superior_direito (x>=12 cm, y<3,5 cm)': n(12.0, 0, wcm, 3.5),
         'margem_superior (y<2,5 cm)': n(0, 0, wcm, 2.5),
         'margem_inferior (y>=28,7 cm)': n(0, hcm - 1.0, wcm, hcm),
         'margem_direita (x>=19,5 cm)': n(wcm - 1.5, 0, wcm, hcm)}
    r['livres'] = all(v == 0 for v in r.values())
    ys, xs = np.where(ink)
    r['distancia_da_tinta_ao_canto_superior_direito_cm'] = round(float(np.min(np.hypot((wcm - xs / px), ys / px))), 2)
    return r
'''
marker = "\n\ndef conferir(pdf, label, ref_pdf=None, rotated=()):"
assert s.count(marker) == 1
s = s.replace(marker, add + marker)
m2 = "        cr, ov, incl = cruzamentos(pg)\n"
assert s.count(m2) == 1
s = s.replace(m2, m2 + "        f['oclusao_fundo_branco_sobre_traco_ou_marca'] = oclusao(pg)\n        f['marcacao_do_RO_areas_livres'] = marcacao_RO(pg)\n")
m3 = "                     'palavras_sobrepostas_total': sum(len(f['texto_sobre_texto']) for f in out['folhas']),"
assert s.count(m3) == 1
s = s.replace(m3, m3 + "\n                     'oclusoes_total': sum(len(f['oclusao_fundo_branco_sobre_traco_ou_marca']) for f in out['folhas']),\n                     'folhas_com_marcacao_do_RO_livre': sum(1 for f in out['folhas'] if f['marcacao_do_RO_areas_livres']['livres']),")
m4 = "'cruz', len(f['texto_cruzado_por_traco']), 'sobre', len(f['texto_sobre_texto']))"
assert s.count(m4) == 1
s = s.replace(m4, "'cruz', len(f['texto_cruzado_por_traco']), 'sobre', len(f['texto_sobre_texto']), 'OCLUSAO', len(f['oclusao_fundo_branco_sobre_traco_ou_marca']), 'RO-livre', f['marcacao_do_RO_areas_livres']['livres'])")
p.write_text(s, encoding='utf-8')
print('ok')
