# -*- coding: utf-8 -*-
"""Revisor R2, item 3: repeticao natural (sem injecao) do teste intermitente, isolado e sob carga.

Fase S: N execucoes sequenciais do unico teste. Fase P: N execucoes com K processos em paralelo (a carga e a propria
concorrencia de disco/CPU). Fase V: N execucoes em paralelo com um 'varredor' que abre (rb) todo arquivo novo em
hb/tests/tmp por 30 ms, como faria um antivirus/indexador que nao compartilha DELETE. Guarda da auditoria ligada.
Grava runs/s3c_heartbeat_repeticao.json com as mensagens de falha (so a linha do assert)."""
import json
import os
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REV = Path(__file__).resolve().parents[1]
HB = REV / 'copia' / 'testes_r2' / 'hb' / 'tests'
PY = r'C:\Python314\python.exe'
TEST = 'test_heartbeat_v2.HeartbeatD3Tests.test_sixty_beats_in_process_zero_or_one_memory_event'


def env():
    e = dict(os.environ)
    tmp = '\\\\?\\' + str(HB / 'tmp')
    e.update(PYTHONPATH=str(REV / 'copia' / 'guard'), ACOM_AUDIT_ROOT=str(REV), TEMP=tmp, TMP=tmp,
             PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', PYTHONIOENCODING='utf-8', NO_PROXY='*')
    return e


def one(_):
    t0 = time.time()
    p = subprocess.run([PY, '-B', '-X', 'utf8', '-m', 'unittest', TEST], cwd=str(HB), env=env(), capture_output=True, timeout=600)
    err = p.stderr.decode('utf-8', 'replace')
    msg = None
    if p.returncode:
        m = re.search(r'(AssertionError: .*|PermissionError: .*|Error: .*)', err)
        msg = m.group(1)[:200] if m else err[-300:]
    return {'rc': p.returncode, 's': round(time.time() - t0, 2), 'msg': msg}


stop = threading.Event()


def varredor():
    seen = {}
    root = HB / 'tmp'
    while not stop.is_set():
        for dp, _, fs in os.walk(root):
            for f in fs:
                p = os.path.join(dp, f)
                try:
                    with open(p, 'rb') as h:
                        h.read(64)
                        time.sleep(0.03)
                except OSError:
                    pass
        time.sleep(0.005)


def fase(nome, n, k, com_varredor=False):
    th = None
    if com_varredor:
        stop.clear()
        th = threading.Thread(target=varredor, daemon=True)
        th.start()
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=k) as ex:
        res = list(ex.map(one, range(n)))
    if th:
        stop.set()
        th.join(5)
    falhas = [r for r in res if r['rc']]
    return {'n': n, 'paralelo': k, 'varredor': com_varredor, 'falhas': len(falhas),
            'mensagens': sorted({r['msg'] for r in falhas if r['msg']}), 'segundos': round(time.time() - t0, 1),
            'tempo_medio_s': round(sum(r['s'] for r in res) / len(res), 2)}


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    out = {'S_sequencial': fase('S', n, 1), 'P_paralelo_8': fase('P', n * 2, 8), 'V_paralelo_4_com_varredor': fase('V', n, 4, True)}
    (REV / 'runs' / 's3c_heartbeat_repeticao.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
