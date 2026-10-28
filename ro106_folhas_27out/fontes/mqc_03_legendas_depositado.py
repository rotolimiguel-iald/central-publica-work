# Quais pontos/trechos de dado estavam sob a legenda (ou caixa de texto) no depositado e agora ficam visiveis?
# Roda as funcoes do script de origem (savefig interceptado), mede a caixa da legenda e conta os vertices de curva / pontos de
# dispersao dentro dela. Figs. 5 e 7 do PCT sao a variante da Central (legendas em cantos vazios, vistos na imagem depositada).
import sys, json, pathlib
sys.path.insert(0, r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes')
import numpy as np
import mqc_folhas as nf
import matplotlib.pyplot as plt
from matplotlib.collections import PathCollection
W = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out')
m = nf.m
res = {}
cur = {'n': None}
real = plt.savefig


def fake(*a, **k):
    fig = plt.gcf()
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    out = []
    for ia, ax in enumerate(fig.axes):
        title = ax.get_title()
        boxes = []
        lg = ax.get_legend()
        if lg is not None:
            boxes.append(('legenda', lg.get_window_extent(r)))
        for t in ax.texts:
            if t.get_bbox_patch() is not None:
                boxes.append(('caixa de texto', t.get_bbox_patch().get_window_extent(r)))
        for kind, bb in boxes:
            n_pts = 0
            xs_hidden = []
            ys_hidden = []
            n_refs = 0
            for ln in ax.lines:
                xy = np.asarray(ln.get_xydata(), float)
                if len(xy) <= 2:
                    d = ax.transData.transform(xy)
                    if len(d) == 2 and np.isfinite(d).all() and nf._seg_hits(d, bb):
                        n_refs += 1
                    continue
                d = ax.transData.transform(xy)
                ok = np.isfinite(d).all(axis=1)
                inside = ok & (d[:, 0] >= bb.x0) & (d[:, 0] <= bb.x1) & (d[:, 1] >= bb.y0) & (d[:, 1] <= bb.y1)
                n_pts += int(inside.sum())
                # trecho da poligonal sob a caixa (amostragem densa: 40 pontos por segmento)
                t = np.linspace(0, 1, 40)[None, :, None]
                dense = (d[:-1, None, :] * (1 - t) + d[1:, None, :] * t).reshape(-1, 2)
                xyd = (xy[:-1, None, :] * (1 - t) + xy[1:, None, :] * t).reshape(-1, 2)
                okd = np.isfinite(dense).all(axis=1)
                ins2 = okd & (dense[:, 0] >= bb.x0) & (dense[:, 0] <= bb.x1) & (dense[:, 1] >= bb.y0) & (dense[:, 1] <= bb.y1)
                if ins2.any():
                    xs_hidden += list(xyd[ins2, 0])
                    ys_hidden += list(xyd[ins2, 1])
            for c in ax.collections:
                if isinstance(c, PathCollection):
                    off = np.asarray(c.get_offsets(), float)
                    d = ax.transData.transform(off)
                    ok = np.isfinite(d).all(axis=1)
                    inside = ok & (d[:, 0] >= bb.x0) & (d[:, 0] <= bb.x1) & (d[:, 1] >= bb.y0) & (d[:, 1] <= bb.y1)
                    n_pts += int(inside.sum())
                    if inside.any():
                        xs_hidden += list(off[inside, 0])
                        ys_hidden += list(off[inside, 1])
            out.append({'painel': title, 'o_que_cobre': kind, 'pontos_de_dado_sob_a_caixa': n_pts, 'linhas_de_referencia_cruzadas': n_refs,
                        'faixa_x_dos_pontos': [float(min(xs_hidden)), float(max(xs_hidden))] if xs_hidden else None,
                        'faixa_y_dos_pontos': [float(min(ys_hidden)), float(max(ys_hidden))] if ys_hidden else None,
                        'opacidade_da_legenda_no_depositado': 'framealpha 0,8 (padrao do matplotlib): o dado sob a legenda aparecia esmaecido, nao apagado'})
    res[cur['n']] = out


plt.savefig = fake
for n, name in ((1, 'gerar_figura_1_topologia'), (2, 'gerar_figura_2_estabilizacao'), (3, 'gerar_figura_3_termodinamica'),
                (4, 'gerar_figura_4_translacao'), (6, 'gerar_figura_6_convergencia')):
    cur['n'] = n
    getattr(m, name)()
plt.savefig = real
(W / 'conferencia' / 'mqc_legendas_do_depositado.json').write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding='utf-8')
for n, v in res.items():
    for x in v:
        print(n, x['painel'][:40], x['o_que_cobre'], x['pontos_de_dado_sob_a_caixa'], x['linhas_de_referencia_cruzadas'], x['faixa_x_dos_pontos'], x['faixa_y_dos_pontos'])
