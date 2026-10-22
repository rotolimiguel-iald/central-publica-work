# -*- coding: utf-8 -*-
"""Resumo da guarda da auditoria sobre a minha rodada da suite (so leitura dos guard_log em suite_r22)."""
import collections
import glob
import json
import sys
from pathlib import Path

ME = Path(__file__).resolve().parents[1]
pasta = sys.argv[1] if len(sys.argv) > 1 else str(ME / 'suite_r22' / 'copia' / 'guard_log')
sep = chr(92)
kinds = collections.Counter()
cats = collections.Counter()
suspeitos = set()
for f in glob.glob(pasta + '/guard_*.jsonl'):
    for linha in open(f, encoding='utf-8', errors='replace'):
        try:
            d = json.loads(linha)
        except ValueError:
            continue
        k = d.get('kind') or d.get('k')
        kinds[k] += 1
        if k in ('READ_OUTSIDE', 'SQLITE_RO_OUTSIDE', 'BLOCK_NETWORK', 'BLOCK_WRITE', 'BLOCK'):
            p = str(d.get('path') or d.get('detail') or d).lower().replace(sep, '/')
            if 'appdata' in p:
                cats['appdata'] += 1
            elif '__pycache__' in p:
                cats['pycache'] += 1
            elif 'python314' in p:
                cats['python314'] += 1
            else:
                cats[p[:70]] += 1
            if ('memoria_iald/state' in p and 'suite_r22' not in p) or 'psion' in p or p.endswith('.env') or 'escritorio' in p:
                suspeitos.add(k + ' ' + p[:140])
print(json.dumps({'kinds': kinds, 'categorias': cats.most_common(12), 'suspeitos': sorted(suspeitos)[:20]}, ensure_ascii=False, indent=1))
