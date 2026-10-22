# -*- coding: utf-8 -*-
"""R2.1 (diagnóstico): repete a fase V do s3c na cópia dada até juntar `k` falhas e grava o traceback COMPLETO de cada
uma (o s3c só guarda a linha do erro). Grava runs/diag_s3c_<copia>.json."""
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.argv = [sys.argv[0], sys.argv[1]] + sys.argv[2:]
NOME, K, N = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
sys.path.insert(0, str(Path(__file__).resolve().parent))
import s3c_heartbeat_repeticao_r2_1 as s3  # noqa: E402
import subprocess  # noqa: E402


def one(_):
    p = subprocess.run([s3.PY, '-B', '-X', 'utf8', '-m', 'unittest', s3.TEST], cwd=str(s3.HB), env=s3.env(),
                       capture_output=True, timeout=600)
    return {'rc': p.returncode, 'stderr': p.stderr.decode('utf-8', 'replace')[-3500:] if p.returncode else None}


s3.stop.clear()
th = threading.Thread(target=s3.varredor, daemon=True)
th.start()
falhas = []
feitos = 0
with ThreadPoolExecutor(max_workers=4) as ex:
    for r in ex.map(one, range(N)):
        feitos += 1
        if r['rc']:
            falhas.append(r['stderr'])
s3.stop.set()
th.join(5)
out = {'copia': NOME, 'execucoes': feitos, 'falhas': len(falhas), 'tracebacks': falhas[:K]}
(s3.R21 / 'runs' / ('diag_s3c_%s.json' % NOME)).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print(feitos, len(falhas))
