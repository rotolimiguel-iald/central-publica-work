# -*- coding: utf-8 -*-
"""R2 (13/10/2026) — conferências SÓ-LEITURA na produção. Nada é escrito fora de 4_INTEGRACAO; nenhum confidencial aberto;
nenhuma rede (nem a porta 8082 é chamada). Escreve evidencias_r2/PRODUCAO_R2_LEITURA.json.

  1. produção intocada (o conferir_producao_intocada.py do R1, com o resultado gravado aqui)
  2. o backend de PRODUÇÃO do implantar.py, só nas operações de LEITURA: a Tarefa Agendada (Get-ScheduledTask) e os
     processos (Win32_Process, Get-NetTCPConnection) — prova que a sintaxe PowerShell dessas consultas funciona aqui
  3. o filtro D4 sobre o banco real (sqlite mode=ro&immutable=1): por contexto, as regras do R1 e do R2 e o tempo de
     cada uma no estado corrente + objetivo — só CONTAGENS e nomes de regra, nunca texto
"""
from __future__ import annotations
import collections
import importlib.util
import json
import sqlite3
import sys
import time
import zlib
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / 'evidencias_r2' / 'PRODUCAO_R2_LEITURA.json'
DB = Path(r'C:\IALD\MEMORIA_IALD\state\memory.sqlite3')
sys.path.insert(0, str(HERE))


def guard_de(path, nome):
    """Carrega um guard.py isolado (o import relativo de .store é trocado por classes locais equivalentes)."""
    src = Path(path).read_text(encoding='utf-8').replace('from .store import MemoryError, ScopeViolation',
                                                         'class MemoryError(Exception): pass\nclass ScopeViolation(MemoryError): pass')
    mod = type(sys)(nome)
    exec(compile(src, str(path), 'exec'), mod.__dict__)
    return mod


def main():
    out = {'at': datetime.now(timezone.utc).isoformat()}
    # 1
    spec = importlib.util.spec_from_file_location('conferir', HERE / 'conferir_producao_intocada.py')
    conf = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conf)
    orig_out = HERE / 'evidencias' / 'PRODUCAO_INTOCADA.json'
    antes = orig_out.read_bytes()
    conf.main()
    out['producao_intocada'] = json.loads(orig_out.read_text(encoding='utf-8'))
    tmp = orig_out.with_name('PRODUCAO_INTOCADA.json.tmp_r2')
    tmp.write_bytes(antes)                     # o arquivo do R1 volta aos seus bytes; o resultado de hoje fica aqui
    tmp.replace(orig_out)
    # 2
    from implantacao_lib import ProcessosPS
    ps = ProcessosPS(r'C:\IALD\projetos_pyhton\IALD', 'IALD Web Server')
    t0 = time.time()
    out['tarefa_agendada'] = ps.tarefa_ler()
    out['processos'] = ps.listar()
    out['backend_producao_leitura_s'] = round(time.time() - t0, 2)
    # 3
    g1 = guard_de(HERE / 'candidato' / 'C' / 'IALD' / 'MEMORIA_IALD' / 'lib' / 'iald_memory' / 'guard.py', 'guard_r1')
    g2 = guard_de(HERE / 'candidato_r2' / 'C' / 'IALD' / 'MEMORIA_IALD' / 'lib' / 'iald_memory' / 'guard.py', 'guard_r2')
    c = sqlite3.connect('file:' + DB.as_posix() + '?mode=ro&immutable=1', uri=True)
    try:
        ctxs = []
        tot = collections.Counter()
        for cid, scope_json in c.execute('SELECT context_id, scope_json FROM contexts').fetchall():
            row = c.execute('SELECT revision, state_json FROM events WHERE context_id=? ORDER BY revision DESC LIMIT 1', (cid,)).fetchone()
            obj = zlib.decompress(c.execute('SELECT objective_blob FROM contexts WHERE context_id=?', (cid,)).fetchone()[0]).decode('utf-8', 'replace')
            text = (row[1] or '') + '\n' + obj
            t = time.perf_counter(); r1 = g1.scan_text(text); s1 = time.perf_counter() - t
            t = time.perf_counter(); r2 = g2.scan_text(text); s2 = time.perf_counter() - t
            ctxs.append({'context_id': cid, 'house': json.loads(scope_json).get('house'), 'revision': row[0], 'chars': len(text),
                         'r1_regras': r1, 'r2_regras': r2, 'r1_s': round(s1, 4), 'r2_s': round(s2, 4), 'igual': r1 == r2})
            tot['chars'] += len(text)
        out['banco'] = {'bytes': DB.stat().st_size, 'contextos': len(ctxs),
                        'contextos_recusados_r1': sum(1 for x in ctxs if x['r1_regras']),
                        'contextos_recusados_r2': sum(1 for x in ctxs if x['r2_regras']),
                        'decisao_igual_em_todos': all(x['igual'] for x in ctxs),
                        'chars_total': tot['chars'], 'r1_s_total': round(sum(x['r1_s'] for x in ctxs), 3),
                        'r2_s_total': round(sum(x['r2_s'] for x in ctxs), 3), 'por_contexto': ctxs}
    finally:
        c.close()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str) + '\n', encoding='utf-8')
    print(json.dumps({'producao_intocada': out['producao_intocada']['producao_intocada'], 'tarefa': out['tarefa_agendada'],
                      'processos': {k: len(v) for k, v in out['processos'].items() if isinstance(v, list)},
                      'banco': {k: v for k, v in out['banco'].items() if k != 'por_contexto'}}, ensure_ascii=False, default=str))


if __name__ == '__main__':
    main()
