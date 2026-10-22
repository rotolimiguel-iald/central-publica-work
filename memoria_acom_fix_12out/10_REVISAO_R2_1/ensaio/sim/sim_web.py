# -*- coding: utf-8 -*-
"""Filho web SIMULADO (ensaio R2). Ao nascer registra o pid e o sha256 do store.py/guard.py que encontraria na
lib da cópia (prova de QUAL código um app (re)lançado carregaria), marca a saúde por arquivo e dorme. Sem rede."""
import hashlib
import json
import os
import sys
import time
from pathlib import Path

SIM = Path(sys.argv[1])
PIDS = SIM / 'pids'
def _ler_tarefa():
    for _ in range(100):   # a troca do tarefa.json pelo simulador pode coincidir com esta leitura
        try:
            return json.loads((SIM / 'tarefa.json').read_text(encoding='utf-8'))
        except (OSError, ValueError):
            time.sleep(0.02)
    raise SystemExit('tarefa.json ilegível')


t = _ler_tarefa()
lib = Path(t['mem_root']) / 'lib' / 'iald_memory'


def sha16(p):
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()[:16]
    except OSError:
        return None


info = {'pid': os.getpid(), 't': time.time(), 'store_sha16': sha16(lib / 'store.py'), 'guard_sha16': sha16(lib / 'guard.py')}
(PIDS / ('web_%d.json' % os.getpid())).write_text(json.dumps(info), encoding='utf-8')
with open(SIM / 'eventos.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(dict(t=time.time(), quem='web', pid=os.getpid(), kind='WEB_START', store_sha16=info['store_sha16'])) + '\n')
if t.get('web_morre_ao_nascer'):
    raise SystemExit(7)
time.sleep(float(t.get('saude_atraso_s', 0) or 0))
(PIDS / ('saude_%d' % os.getpid())).write_text('200', encoding='utf-8')
while True:
    time.sleep(0.5)
