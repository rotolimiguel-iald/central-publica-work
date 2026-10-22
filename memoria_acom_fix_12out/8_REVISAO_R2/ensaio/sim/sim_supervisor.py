# -*- coding: utf-8 -*-
"""Supervisor SIMULADO (ensaio R2): o papel do start_iald_web.ps1 — trava de instância única (como o mutex
Global\\IALD_WebSupervisor_8082) e relançamento do filho web 0,5 s depois que ele morre. Sem rede."""
import json
import msvcrt
import os
import subprocess
import sys
import time
from pathlib import Path

SIM = Path(sys.argv[1])
ORIGEM = sys.argv[2] if len(sys.argv) > 2 else '?'
PIDS = SIM / 'pids'
PIDS.mkdir(parents=True, exist_ok=True)


def ev(kind, **kw):
    with open(SIM / 'eventos.jsonl', 'a', encoding='utf-8') as f:
        f.write(json.dumps(dict(t=time.time(), quem='supervisor', pid=os.getpid(), kind=kind, **kw)) + '\n')


lock = open(SIM / 'mutex.lock', 'a+b')
try:
    lock.seek(0)
    msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
except OSError:
    ev('SUP_RECUSADO_MUTEX', origem=ORIGEM)
    raise SystemExit(3)
(PIDS / ('sup_%d.json' % os.getpid())).write_text(json.dumps({'pid': os.getpid(), 'origem': ORIGEM, 't': time.time()}), encoding='utf-8')
ev('SUP_START', origem=ORIGEM)
def _ler_tarefa():
    for _ in range(100):   # a troca do tarefa.json pelo simulador pode coincidir com esta leitura
        try:
            return json.loads((SIM / 'tarefa.json').read_text(encoding='utf-8'))
        except (OSError, ValueError):
            time.sleep(0.02)
    raise SystemExit('tarefa.json ilegível')


t = _ler_tarefa()
while True:
    p = subprocess.Popen([sys.executable, '-X', 'utf8', str(Path(t['scripts']) / 'sim_web.py'), str(SIM)],
                         stdout=open(SIM / 'saida_web.log', 'ab'), stderr=subprocess.STDOUT)
    ev('WEB_LAUNCH', web_pid=p.pid)
    p.wait()
    ev('WEB_DIED', web_pid=p.pid, codigo=p.returncode)
    time.sleep(0.5)
