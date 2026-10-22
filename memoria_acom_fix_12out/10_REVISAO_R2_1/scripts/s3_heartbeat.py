# -*- coding: utf-8 -*-
"""Revisor c1 R2.1, passo 3: o heartbeat (o «3 != 1») na MINHA copia da suite, teste ORIGINAL, sem injecao.

Fases:
  V30  : 4 em paralelo + varredor externo que abre (rb, sem FILE_SHARE_DELETE) cada arquivo novo do tmp por 30 ms
         (a forma do revisor R2 e do construtor), N execucoes;
  V150 : idem com o varredor segurando 150 ms (forma nova, mais agressiva, ainda < 3 s de nova tentativa).
Cada execucao separa o veredito do CORPO do teste (antes do tearDown) do erro do tearDown (s3_hb_um.py).
Guarda da auditoria ligada (ACOM_AUDIT_ROOT = a copia). Grava runs/s3_heartbeat.json.
    python s3_heartbeat.py [n_V30] [n_V150]
"""
import json
import os
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ME = Path(__file__).resolve().parents[1]
COPIA = ME / 'suite_r21' / 'copia'
HB = COPIA / 'testes_r2' / os.environ.get('HB_NOME', 'hb') / 'tests'
PY = r'C:\Python314\python.exe'
UM = ME / 'scripts' / 's3_hb_um.py'


def env():
    e = dict(os.environ)
    tmp = '\\\\?\\' + str(HB / 'tmp')
    e.update(PYTHONPATH=str(COPIA / 'guard'), ACOM_AUDIT_ROOT=str(COPIA), TEMP=tmp, TMP=tmp,
             PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', PYTHONIOENCODING='utf-8', NO_PROXY='*')
    return e


def one(_):
    t0 = time.time()
    p = subprocess.run([PY, '-B', '-X', 'utf8', str(UM), str(HB)], cwd=str(HB), env=env(), capture_output=True, timeout=600)
    out = p.stdout.decode('utf-8', 'replace').strip().splitlines()
    try:
        r = json.loads(out[-1])
    except (IndexError, ValueError):
        r = {'ok': False, 'corpo_ok': None, 'parse_falhou': p.stderr.decode('utf-8', 'replace')[-300:]}
    r['s'] = round(time.time() - t0, 2)
    return r


stop = threading.Event()
aberturas = [0]


def varredor(hold):
    root = HB / 'tmp'
    while not stop.is_set():
        for dp, _, fs in os.walk(root):
            for f in fs:
                try:
                    with open(os.path.join(dp, f), 'rb') as h:
                        h.read(64)
                        aberturas[0] += 1
                        time.sleep(hold)
                except OSError:
                    pass
        time.sleep(0.005)


def fase(n, k, hold):
    stop.clear()
    aberturas[0] = 0
    th = threading.Thread(target=varredor, args=(hold,), daemon=True) if hold else None
    if th:
        th.start()
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=k) as ex:
        res = list(ex.map(one, range(n)))
    stop.set()
    if th:
        th.join(5)
    msgs = {}
    for r in res:
        for m in r.get('msgs') or []:
            msgs[m[:120]] = msgs.get(m[:120], 0) + 1
    return {'n': n, 'paralelo': k, 'hold_s': hold, 'aberturas_do_varredor': aberturas[0],
            'ok': sum(bool(r.get('ok')) for r in res),
            'corpo_falhou': sum(r.get('corpo_ok') is False for r in res),
            'corpo_desconhecido': sum(r.get('corpo_ok') is None for r in res),
            'so_teardown': sum(r.get('corpo_ok') is True and not r.get('ok') for r in res),
            'erros_no_corpo_por_traceback': sum(o == 'corpo' for r in res for o in (r.get('onde') or [])),
            'erros_no_tearDown_por_traceback': sum(o == 'tearDown' for r in res for o in (r.get('onde') or [])),
            'teardown_exc_amostra': sorted({(r.get('teardown_exc') or '')[:110] for r in res if r.get('teardown_exc')})[:3],
            'mensagens': msgs, 'tres_diferente_de_um': sum('3 != 1' in m for r in res for m in (r.get('msgs') or [])),
            'segundos': round(time.time() - t0, 1)}


def main():
    n30 = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    n150 = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    import hashlib
    out = {'teste': 'test_heartbeat_v2.HeartbeatD3Tests.test_sixty_beats_in_process_zero_or_one_memory_event (original)',
           'web_server_da_copia_sha16': hashlib.sha256((HB.parent / 'copia' / 'projetos_pyhton' / 'IALD' /
                                                        'iald_web_server.py').read_bytes()).hexdigest()[:16],
           'test_heartbeat_v2_sha16': hashlib.sha256((HB / 'test_heartbeat_v2.py').read_bytes()).hexdigest()[:16]}
    out['V30'] = fase(n30, 4, 0.03)
    out['V150'] = fase(n150, 4, 0.15)
    (ME / 'runs' / os.environ.get('HB_OUT', 's3_heartbeat.json')).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
