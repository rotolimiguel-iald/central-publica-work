# -*- coding: utf-8 -*-
"""R2.2: resumo das leituras fora da pasta e dos bloqueios da guarda na rodada final da suíte (cópia R2.2) e do ensaio.
Grava runs/s6_guarda_resumo.json. Só lê os logs da guarda."""
import collections
import json
import os
from pathlib import Path

R22 = Path(__file__).resolve().parents[1]
out = {}
for nome, pasta in (('suite_copia', R22 / 'copia' / 'guard_log'), ('ensaio', R22 / 'guard_log')):
    c, blocks, kinds = collections.Counter(), collections.Counter(), collections.Counter()
    for p in pasta.glob('guard_*.jsonl'):
        for ln in p.read_text(encoding='utf-8', errors='replace').splitlines():
            try:
                it = json.loads(ln)
            except ValueError:
                continue
            k = it.get('kind', '')
            kinds[k] += 1
            if k == 'READ_OUTSIDE':
                parts = Path(str(it.get('path') or '')).parts
                c[os.sep.join(parts[:5])] += 1
            if k.startswith('BLOCK'):
                blocks[k + ' ' + str(it.get('args') or it.get('path'))[:80]] += 1
    out[nome] = {'tipos': dict(kinds), 'leituras_fora_por_prefixo': dict(c.most_common(20)), 'bloqueios': dict(blocks)}
    toca_banco = [k for k in c if 'MEMORIA_IALD' + os.sep + 'state' in k]
    out[nome]['leitura_do_banco_de_producao'] = toca_banco
(R22 / 'runs' / 's6_guarda_resumo.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps(out, ensure_ascii=False, indent=1)[:4000])
