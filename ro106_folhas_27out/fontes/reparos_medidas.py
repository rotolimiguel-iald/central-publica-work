# Medidas ANTES/DEPOIS de cada ponto reparado (rodada 2), por script, sobre os PDFs da rodada 1 (_tmp\base) e os atuais.
import sys, json, math, pathlib
import numpy as np
import fitz
sys.path.insert(0, r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes')
import conferir as C

W = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out')
PT = 2.54 / 72


def strokes_pts(pg):
    pts = []
    for d in pg.get_drawings():
        if d.get('color') is None or d['type'] not in ('s', 'fs'):
            continue
        for it in d['items']:
            pp = C._poly_of([it])
            for j in range(len(pp) - 1):
                a, b = np.array(pp[j]), np.array(pp[j + 1])
                n = max(2, int(np.hypot(*(b - a)) / 0.8) + 1)
                for t in np.linspace(0, 1, n):
                    pts.append(a + t * (b - a))
    return np.array(pts)


def folga_cm(pg, palavra, sp):
    """Menor distancia (cm) entre a caixa da palavra (caixa da fonte, maior que a tinta) e o traco mais proximo; 0 = sobreposto."""
    out = []
    for w in pg.get_text('words'):
        if w[4] == palavra:
            x0, y0, x1, y1 = w[:4]
            dx = np.maximum(np.maximum(x0 - sp[:, 0], 0), sp[:, 0] - x1)
            dy = np.maximum(np.maximum(y0 - sp[:, 1], 0), sp[:, 1] - y1)
            out.append(float(np.min(np.hypot(dx, dy))) * PT)
    return round(min(out), 2) if out else None


def pontas_fig1(pdf):
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
        cand = [c for c in heads if wb[3] < c[1] < wa[1] and wa[0] - 2 < c[0] < wa[2] + 40]
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


def run():
    out = {'metodo': 'vetorial, em ordem de pintura (oclusao_rapida/conferir.oclusao); folga = menor distancia da caixa do texto ao traco',
           'antes': 'PDFs da rodada 1 (_tmp\\base\\*_antes.pdf = FOLHAS_SUBSTITUTIVAS_*.pdf.bak_20261027_094406)', 'depois': 'PDFs desta rodada'}
    for k, antes_pdf, depois_pdf in (('050576', W / '_tmp/base/apr_antes.pdf', W / 'FOLHAS_SUBSTITUTIVAS_050576.pdf'),
                                     ('050579', W / '_tmp/base/mqc_antes.pdf', W / 'FOLHAS_SUBSTITUTIVAS_050579.pdf')):
        res = {'folhas': []}
        da, dd = fitz.open(str(antes_pdf)), fitz.open(str(depois_pdf))
        for i in range(max(len(da), len(dd))):
            row = {'folha': i + 1}
            for tag, doc in (('antes', da), ('depois', dd)):
                if i < len(doc):
                    pg = doc[i]
                    o = C.oclusao(pg)
                    r = C.marcacao_RO(pg)
                    row[tag] = {'oclusoes': len(o), 'pontos_de_traco_cobertos_por_fundo_branco': int(sum(x['pontos_de_traco_cobertos'] for x in o)),
                                'RO_livre': r['livres'], 'RO_tinta_px': {kk: vv for kk, vv in r.items() if kk not in ('livres', 'distancia_da_tinta_ao_canto_superior_direito_cm')}}
            res['folhas'].append(row)
        if k == '050576':
            res['setas_fig1'] = {'antes': pontas_fig1(antes_pdf), 'depois': pontas_fig1(depois_pdf)}
            # folgas por palavra (folha onde esta)
            plano = {'Próxima': 2, 'geração': 2, 'Vácuo': 4, 'angular': 4}
            fa, fd = {}, {}
            for doc, dst in ((da, fa), (dd, fd)):
                cache = {}
                for pal, pi in plano.items():
                    if pi not in cache:
                        cache[pi] = strokes_pts(doc[pi])
                    # 'angular' tambem esta em «Bucket angular b» (eixo): a folga vale para a ocorrencia mais proxima de traco
                    dst[pal] = folga_cm(doc[pi], pal, cache[pi])
            res['folga_texto_traco_cm'] = {'antes': fa, 'depois': fd}
        out[k] = res
    return out


if __name__ == '__main__':
    o = run()
    (W / 'conferencia' / 'reparos_rodada2.json').write_text(json.dumps(o, indent=1, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != 'folhas'} for k, v in o.items() if k.startswith('05')}, indent=1, ensure_ascii=False))
    for k in ('050576', '050579'):
        for row in o[k]['folhas']:
            print(k, row['folha'], 'antes', row.get('antes', {}).get('oclusoes'), row.get('antes', {}).get('pontos_de_traco_cobertos_por_fundo_branco'), row.get('antes', {}).get('RO_livre'), '| depois', row.get('depois', {}).get('oclusoes'), row.get('depois', {}).get('RO_livre'))
