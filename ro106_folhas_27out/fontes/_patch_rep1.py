import pathlib
p = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes\reparos_medidas.py')
s = p.read_text(encoding='utf-8')
a = s.index('def pontas_fig1(pdf):')
b = s.index('def run():')
new = '''def pontas_fig1(pdf):
    """Sentido das pontas de seta entre [1]-[3] e [4]-[5] na Fig. 1 (folha 1, girada: o topo da figura fica a esquerda).
    Sentido = do outro extremo do traco (haste) para a ponta (cabeca preenchida colada ao fim da haste)."""
    pg = fitz.open(str(pdf))[0]
    words = {w[4]: w for w in pg.get_text('words') if w[4] in ('[1]', '[3]', '[4]', '[5]')}
    shafts = []
    heads = []
    for dr in pg.get_drawings():
        if dr['type'] == 's' and dr.get('color') is not None and not dr.get('dashes', '').startswith('[ ') :
            for it in dr['items']:
                if it[0] == 'l' and math.hypot(it[2].x - it[1].x, it[2].y - it[1].y) > 14:
                    shafts.append((np.array([it[1].x, it[1].y]), np.array([it[2].x, it[2].y])))
        if dr['type'] in ('f', 'fs') and dr.get('fill') == (0.0, 0.0, 0.0) and dr['rect'].width * dr['rect'].height < 25 * 25:
            pts = [(it[1].x, it[1].y) for it in dr['items'] if it[0] == 'l']
            if len(pts) >= 4:
                heads.append(np.array(pts[:4]).mean(axis=0))
    res = {}
    for par, (ka, kb) in {'[1]-[3]': ('[1]', '[3]'), '[4]-[5]': ('[4]', '[5]')}.items():
        wa, wb = words[ka], words[kb]
        cand = [c for c in heads if wb[3] < c[1] < wa[1] and wa[0] - 12 < c[0] < wa[2] + 40]
        if not cand:
            res[par] = 'ponta nao encontrada'
            continue
        c = cand[0]
        best = None
        for p0, p1 in shafts:
            for near, far in ((p1, p0), (p0, p1)):
                d = np.linalg.norm(near - c)
                if d < 12 and (best is None or d < best[0]):
                    best = (d, near, far)
        if best is None:
            res[par] = 'haste nao encontrada'
            continue
        v = best[1] - best[2]          # da cauda para a cabeca
        # folha girada: +y da pagina = em direcao a [1]/[4] (esquerda na figura); -y = em direcao a [3]/[5] (direita na figura)
        res[par] = ('aponta para %s (esquerda na figura)' % ka) if v[1] > 0 else ('aponta para %s (direita na figura)' % kb)
    return res


'''
s = s[:a] + new + s[b:]
# folgas so para texto horizontal, na folha certa
c = s.index("            plano = {'Pr")
d = s.index("            res['folga_texto_traco_cm'] = {'antes': fa, 'depois': fd}")
newf = '''            plano = {'Próxima': 2, 'geração': 2, 'Vácuo': 4, 'angular': 4}
            fa, fd = {}, {}
            for doc, dst in ((da, fa), (dd, fd)):
                cache = {}
                for pal, pi in plano.items():
                    if pi not in cache:
                        cache[pi] = strokes_pts(doc[pi])
                    # 'angular' tambem esta em «Bucket angular b» (eixo): a folga vale para a ocorrencia mais proxima de traco
                    dst[pal] = folga_cm(doc[pi], pal, cache[pi])
'''
s = s[:c] + newf + s[d:]
s = s.replace("""            f = {}
            for tag, pdf, shp in (('antes', antes_pdf, {'Próxima': 2, 'geração': 2, 'Vácuo': 4, 'angular': 4, 'VACUUM': 1, 'GRAVITON': 1, 'Comprimir': 1, 'Filtrar': 1}),
                                  ('depois', depois_pdf, {'Próxima': 2, 'geração': 2, 'Vácuo': 4, 'angular': 4, 'VACUUM': 1, 'GRAVITON': 1, 'Comprimir': 1, 'Filtrar': 1})):
                d = fitz.open(str(pdf))
                f[tag] = {}
                for pal, sh in shp.items():
                    pass
""", "")
p.write_text(s, encoding='utf-8')
print('ok')
