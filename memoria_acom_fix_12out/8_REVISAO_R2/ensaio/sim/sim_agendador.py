# -*- coding: utf-8 -*-
"""Agendador SIMULADO (ensaio R2, achado 3). Modela a tarefa «IALD Web Server» como lida em 13/10 [REAL]:
MultipleInstances IgnoreNew, RestartCount 3, RestartInterval (aqui em segundos, curto), Disabled bloqueia início e
relançamento. Uma instância = um processo sim_supervisor.py lançado por este agendador.

Arquivos em <sim_dir>: tarefa.json (lido a cada volta), comandos/*.json (start/stop/exit; responde *.ack),
estado_agendador.json, eventos.jsonl. Sem rede. Só processos Python. No Windows a troca de um arquivo falha enquanto
outro processo o lê: toda troca tem novas tentativas curtas, e um erro numa volta é registrado sem matar o agendador.
"""
import json
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path

SIM = Path(sys.argv[1])
CMD = SIM / 'comandos'
CMD.mkdir(parents=True, exist_ok=True)


def ev(kind, **kw):
    line = dict(t=time.time(), quem='agendador', pid=os.getpid(), kind=kind, **kw)
    with open(SIM / 'eventos.jsonl', 'a', encoding='utf-8') as f:
        f.write(json.dumps(line) + '\n')


def tarefa():
    for _ in range(100):
        try:
            return json.loads((SIM / 'tarefa.json').read_text(encoding='utf-8'))
        except (OSError, ValueError):
            time.sleep(0.02)
    raise RuntimeError('tarefa.json ilegível')


def trocar(src, dst):
    for i in range(100):
        try:
            os.replace(src, dst)
            return
        except PermissionError:
            if i == 99:
                raise
            time.sleep(0.02)


def escrever(path, data):
    tmp = path.with_name(path.name + '.tmp_%d' % os.getpid())
    tmp.write_text(json.dumps(data), encoding='utf-8')
    trocar(tmp, path)


def lancar(motivo):
    t = tarefa()
    p = subprocess.Popen([sys.executable, '-X', 'utf8', str(Path(t['scripts']) / 'sim_supervisor.py'), str(SIM), 'agendador'],
                         stdout=open(SIM / 'saida_supervisor.log', 'ab'), stderr=subprocess.STDOUT)
    ev('LAUNCH', motivo=motivo, instancia_pid=p.pid)
    return p


inst = None
parado_pelo_agendador = False
restarts = 0
restart_em = None
ev('AGENDADOR_ON')
while True:
    try:
        t = tarefa()
        for c in sorted(CMD.glob('*.json')):
            try:
                cmd = json.loads(c.read_text(encoding='utf-8'))
            except (OSError, ValueError):
                continue
            op, res = cmd.get('op'), None
            if op == 'start':
                t = tarefa()        # relido: Enable-ScheduledTask pode ter chegado nesta mesma volta
                if not t['enabled']:
                    res = 'recusado_desabilitada'
                elif inst is not None and inst.poll() is None:
                    res = 'ignorado_instancia_viva'      # IgnoreNew
                else:
                    inst, parado_pelo_agendador, restarts, restart_em = lancar('start'), False, 0, None
                    res = 'iniciado'
            elif op == 'stop':
                if inst is not None and inst.poll() is None:
                    parado_pelo_agendador = True
                    inst.terminate()
                    inst.wait(10)
                    res = 'parado'
                else:
                    res = 'nada_a_parar'
                restart_em = None
            elif op == 'exit':
                res = 'saindo'
            ev('COMANDO', op=op, resultado=res)
            escrever(c.with_suffix('.ack'), {'op': op, 'resultado': res})
            trocar(c, c.with_suffix('.feito'))
            if op == 'exit':
                raise SystemExit(0)
        if inst is not None and inst.poll() is not None:
            code = inst.returncode
            ev('INSTANCIA_TERMINOU', codigo=code, parado_pelo_agendador=parado_pelo_agendador)
            if code != 0 and not parado_pelo_agendador and t['enabled'] and restarts < t['restart_count']:
                restart_em = time.time() + float(t['restart_interval_s'])
                ev('RESTART_AGENDADO', em_s=t['restart_interval_s'])
            inst = None
        if restart_em is not None and time.time() >= restart_em:
            restart_em = None
            if tarefa()['enabled']:
                inst, parado_pelo_agendador = lancar('restart_on_failure'), False
                restarts += 1
            else:
                ev('RESTART_SUPRIMIDO_DESABILITADA')
        escrever(SIM / 'estado_agendador.json', {'instancia_pid': inst.pid if inst is not None and inst.poll() is None else None,
                                                 'restarts': restarts, 'restart_pendente': restart_em is not None, 'em': time.time()})
    except SystemExit:
        raise
    except Exception:  # noqa: BLE001 - registrado; o agendador continua
        ev('AGENDADOR_ERRO', tb=traceback.format_exc()[-800:])
    time.sleep(0.1)
