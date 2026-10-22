# -*- coding: utf-8 -*-
"""R2.1: medidas do N1 (custo do nome com sufixos repetidos) e do N2 (path_reason de nomes *.env e variantes) nas duas
cópias, para o relatório (antes = copia_r2, depois = copia). Só sintético; arquivos .env* não são criados (a guarda da
auditoria proíbe; o nome basta). Rodar dentro de cada cópia:  python -B s4_medidas_nomes.py <copia|copia_r2>"""
import json
import sys
import time
from pathlib import Path

R21 = Path(__file__).resolve().parents[1]
NOME = sys.argv[1]
SUITE = R21 / NOME / 'testes_r2' / 'suite'
sys.path[:0] = [str(SUITE / 'core'), str(SUITE / 'sessions')]
from iald_memory import guard  # noqa: E402
import session_memory as sm  # noqa: E402

SB = R21 / NOME / 'tmp' / 'medidas'
SB.mkdir(parents=True, exist_ok=True)


def melhor(fn, *a, n=3):
    best = None
    for _ in range(n):
        t0 = time.perf_counter()
        try:
            fn(*a)
        except Exception:  # noqa: BLE001
            pass
        dt = time.perf_counter() - t0
        best = dt if best is None else min(best, dt)
    return round(best, 4)


out = {'copia': NOME, 'N1': {}, 'N2': {}}
for k in (2000, 4000, 8000, 16000):
    out['N1']['basename_bak_x%d' % k] = {'chars': 1 + 4 * k, 's': melhor(guard.confidential_basename, 'a' + '.bak' * k)}
for k in (8000,):
    p = str(SB / ('x' + '.bak' * k))
    out['N1']['path_reason_32k'] = {'chars': len(p), 's': melhor(guard.path_reason, p, [str(SB)])}
    out['N1']['read_allowed_file_32k'] = {'chars': len(p), 's': melhor(sm.read_allowed_file, p)}
for nm in ('central.env', 'prod.env', 'app.env.local', 'secrets.env~', '.env~', 'env', '.env', 'x.env_prod', '.envrc',
           'iald_psion_ѕtate.json', 'iald‐psion‐state.json', 'copia_iald_psion_state_32B.json',
           'IALD​_psion_state.json', 'server.key~', 'environment.json', 'objetivo.md'):
    out['N2'][ascii(nm)] = guard.path_reason(str(SB / nm), [str(SB)])
(R21 / 'runs' / ('s4_medidas_nomes_%s.json' % NOME)).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps(out, ensure_ascii=False))
