import json, hashlib, pathlib, os, time, sys
import fitz
sys.path.insert(0, r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes')
import reparos_medidas as R
W = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out')


def sh(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


for k in ('050576', '050579'):
    m = json.load(open(W / 'conferencia' / ('medidas_%s.json' % k), encoding='utf-8'))
    print(k, 'medidas.sha == pdf atual:', m['sha256'] == sh(W / ('FOLHAS_SUBSTITUTIVAS_%s.pdf' % k)), len(m['folhas']))
    c = json.load(open(W / ('CONFERENCIA_%s.json' % k), encoding='utf-8'))
    print('  conferencia.sha == pdf:', c['folhas_substitutivas']['sha256'] == sh(W / ('FOLHAS_SUBSTITUTIVAS_%s.pdf' % k)))
    print('  saidas:', [(x['arquivo'].split('\\')[-1], x['sha16']) for x in c['saidas_sha256']])
m = json.load(open(W / 'conferencia' / 'medidas_ALT_PHOT.json', encoding='utf-8'))
print('ALT sha ok', m['sha256'] == sh(W / 'ALTERNATIVA_FOLHA_1_050576_PHOT.pdf'))
for f in os.listdir(W / 'REVISAO'):
    p = W / 'REVISAO' / f
    if p.is_file():
        print(f, time.strftime('%H:%M:%S', time.localtime(p.stat().st_mtime)))
# folga por ocorrencia de 'angular' na folha 5 (depois)
d = fitz.open(str(W / 'FOLHAS_SUBSTITUTIVAS_050576.pdf'))
pg = d[4]
sp = R.strokes_pts(pg)
import numpy as np
for w in pg.get_text('words'):
    if w[4] in ('angular', 'Vácuo', 'Bucket'):
        x0, y0, x1, y1 = w[:4]
        dx = np.maximum(np.maximum(x0 - sp[:, 0], 0), sp[:, 0] - x1)
        dy = np.maximum(np.maximum(y0 - sp[:, 1], 0), sp[:, 1] - y1)
        print(w[4], [round(v * 2.54 / 72, 2) for v in w[:4]], 'folga', round(float(np.min(np.hypot(dx, dy))) * 2.54 / 72, 2))
