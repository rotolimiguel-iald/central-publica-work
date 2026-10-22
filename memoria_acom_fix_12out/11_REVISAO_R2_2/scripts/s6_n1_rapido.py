# -*- coding: utf-8 -*-
"""Medida rapida de N1 (caminho com muitos componentes) no guard do candidato R2.2 (copia na minha suite) e no da R2.1
(copia do revisor anterior). So sintetico; nada de producao."""
import importlib
import json
import sys
import time
from pathlib import Path

ME = Path(__file__).resolve().parents[1]
sep = chr(92)


def medir(lib, rotulo):
    for m in [k for k in sys.modules if k.startswith('iald_memory')]:
        del sys.modules[m]
    sys.path.insert(0, str(lib))
    try:
        g = importlib.import_module('iald_memory.guard')
        raiz = str(ME / 'tmp' / 'n1')
        out = {}
        for n in (2000, 16000):
            p = raiz + sep + sep.join(['a'] * n) + sep + 'x.json'
            t = time.time()
            try:
                r = g.path_reason(p, [raiz])
            except Exception as e:  # noqa: BLE001
                r = 'EXC ' + type(e).__name__
            out['comp_%d' % n] = [r, round(time.time() - t, 3)]
        p = raiz + sep + ('b' * 40000) + '.json'
        t = time.time()
        try:
            r = g.path_reason(p, [raiz])
        except Exception as e:  # noqa: BLE001
            r = 'EXC ' + type(e).__name__
        out['len_40000'] = [r, round(time.time() - t, 3)]
        p = raiz + sep + sep.join(['pasta'] * 40) + sep + 'nota.json'
        out['ordinario_40_componentes'] = g.path_reason(p, [raiz])
        return out
    finally:
        sys.path.pop(0)


res = {'R2_2': medir(ME / 'suite_r22' / 'copia' / 'testes_r2' / 'suite' / 'core', 'R2_2')}
r21 = ME.parent / '10_REVISAO_R2_1' / 'suite_r21' / 'copia' / 'testes_r2' / 'suite' / 'core'
res['R2_1'] = medir(r21, 'R2_1') if (r21 / 'iald_memory').exists() else 'sem core R2.1'
print(json.dumps(res, ensure_ascii=False, indent=1))
(ME / 'runs' / 's6_n1_rapido.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
