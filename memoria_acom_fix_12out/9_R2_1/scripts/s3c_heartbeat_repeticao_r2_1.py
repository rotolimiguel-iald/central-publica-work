# -*- coding: utf-8 -*-
"""R2.1: a repetição s3c do revisor (8_REVISAO_R2/scripts/s3c_heartbeat_repeticao.py), sem injeção, sobre uma das
cópias (copia_r2 = antes, copia = depois). O teste é o ORIGINAL da suíte (test_sixty_beats_in_process_zero_or_one_
memory_event, que não foi alterado). Fases: S (sequencial, sem varredor) e V (4 em paralelo com o «varredor» que abre
(rb) cada arquivo novo de hb/tests/tmp por 30 ms, como um antivírus/indexador). Guarda da auditoria ligada
(ACOM_AUDIT_ROOT = a cópia). Grava runs/s3c_<copia>.json.

    python -B s3c_heartbeat_repeticao_r2_1.py <copia|copia_r2> [n_S] [n_V]
"""
import json
import os
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

R21 = Path(__file__).resolve().parents[1]
NOME = sys.argv[1]
COPIA = R21 / NOME
HB = COPIA / 'testes_r2' / 'hb' / 'tests'
PY = sys.executable
TEST = 'test_heartbeat_v2.HeartbeatD3Tests.test_sixty_beats_in_process_zero_or_one_memory_event'


def env():
    e = dict(os.environ)
    tmp = '\\\\?\\' + str(HB / 'tmp')
    e.update(PYTHONPATH=str(COPIA / 'guard'), ACOM_AUDIT_ROOT=str(COPIA), TEMP=tmp, TMP=tmp,
             PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', PYTHONIOENCODING='utf-8', NO_PROXY='*')
    return e


def one(_):
    t0 = time.time()
    p = subprocess.run([PY, '-B', '-X', 'utf8', '-m', 'unittest', TEST], cwd=str(HB), env=env(), capture_output=True, timeout=600)
    err = p.stderr.decode('utf-8', 'replace')
    msg = None
    if p.returncode:
        m = re.search(r'(AssertionError: .*|PermissionError: .*|Error: .*)', err)
        msg = (m.group(1)[:140] if m else err[-200:]).strip()
    # R2.1: separa a falha DO TESTE (assert/erro no corpo) da falha só da LIMPEZA do tempdir no tearDown (o varredor
    # externo ainda segura um arquivo quando o tempfile tenta apagá-lo: fixture, não produto)
    classe = None
    if p.returncode:
        so_limpeza = 'in tearDown' in err and 'AssertionError' not in err and 'heartbeat_cycle' not in err             and 'test_sixty_beats' not in err.split('in tearDown')[0].split('Traceback')[-1]
        classe = 'limpeza_tearDown' if so_limpeza else 'falha_do_teste'
    return {'rc': p.returncode, 's': round(time.time() - t0, 2), 'msg': msg, 'classe': classe}


stop = threading.Event()
aberturas = [0]


def varredor():
    root = HB / 'tmp'
    while not stop.is_set():
        for dp, _, fs in os.walk(root):
            for f in fs:
                try:
                    with open(os.path.join(dp, f), 'rb') as h:
                        h.read(64)
                        aberturas[0] += 1
                        time.sleep(0.03)
                except OSError:
                    pass
        time.sleep(0.005)


def fase(n, k, com_varredor=False):
    th = None
    if com_varredor:
        stop.clear()
        aberturas[0] = 0
        th = threading.Thread(target=varredor, daemon=True)
        th.start()
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=k) as ex:
        res = list(ex.map(one, range(n)))
    if th:
        stop.set()
        th.join(5)
    falhas = [r for r in res if r['rc']]
    msgs = {}
    for r in falhas:
        msgs[r['msg']] = msgs.get(r['msg'], 0) + 1
    return {'n': n, 'paralelo': k, 'varredor': com_varredor, 'aberturas_do_varredor': aberturas[0] if com_varredor else None,
            'falhas': len(falhas), 'falhas_do_teste': sum(r['classe'] == 'falha_do_teste' for r in falhas),
            'falhas_so_da_limpeza_tearDown': sum(r['classe'] == 'limpeza_tearDown' for r in falhas), 'mensagens': msgs, 'segundos': round(time.time() - t0, 1),
            'tempo_medio_s': round(sum(r['s'] for r in res) / len(res), 2)}


def main():
    n_s = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    n_v = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    out = {'copia': NOME, 'teste': TEST, 'python': PY,
           'web_server_da_copia_sha16': __import__('hashlib').sha256(
               (COPIA / 'testes_r2' / 'hb' / 'copia' / 'projetos_pyhton' / 'IALD' / 'iald_web_server.py').read_bytes()).hexdigest()[:16],
           'S_sequencial': fase(n_s, 1), 'V_paralelo_4_com_varredor': fase(n_v, 4, True)}
    (R21 / 'runs' / ('s3c_%s.json' % NOME)).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
