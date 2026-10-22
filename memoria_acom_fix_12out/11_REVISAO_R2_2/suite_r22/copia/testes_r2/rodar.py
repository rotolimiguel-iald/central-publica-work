# -*- coding: utf-8 -*-
"""Roda TODAS as suítes contra o candidato, em cópias, sob a guarda sitecustomize da auditoria
(PYTHONPATH=4_INTEGRACAO/guard, ACOM_AUDIT_ROOT=4_INTEGRACAO: sem rede, sem escrita/sqlite gravável fora da
pasta, sem abrir confidenciais, só subprocessos Python). TEMP/TMP dentro da pasta, com prefixo estendido nas
suítes do app (os nomes do outbox estouram MAX_PATH; LongPathsEnabled=0) e simples nas demais (sqlite URI). O «D:» dos testes é tmp/arquivo_D (o D: real não
é tocado). Escreve RESULTADOS_TESTES.json e TESTES.md. Nenhuma chamada a provedor.
"""
from __future__ import annotations
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent          # testes
INT = HERE.parent                                # 4_INTEGRACAO
SUITE = HERE / 'suite'
PY = r'C:\Python314\python.exe'
FILA55 = json.loads((HERE / 'SUITE_MANIFEST.json').read_text(encoding='utf-8'))['fila55_modulos']
CORE = str(SUITE / 'core')
SUITES = [
    # (rótulo, cwd, módulos, PYTHONPATH extra, TEMP com prefixo estendido?)
    ('CORE 20 (origem, 1 reescrita D1/D2)', HERE / 'nucleo' / 'tests', ['test_store'], [str(HERE / 'nucleo' / 'copia' / 'MEMORIA_IALD' / 'lib'), str(HERE / 'nucleo' / 'tests')], False),
    ('NUCLEO novos 34 (frente 1)', HERE / 'nucleo' / 'tests', ['test_store_v2'], [str(HERE / 'nucleo' / 'copia' / 'MEMORIA_IALD' / 'lib'), str(HERE / 'nucleo' / 'tests')], False),
    ('SESSOES 17 (origem)', SUITE / 'sessions', ['test_sessions', 'test_hooks'], [], False),
    ('SESSOES novos 24 (frente 3)', SUITE / 'sessions', ['test_filters', 'test_guard'], [], False),
    ('APP 31 (origem, 1 reescrita D3)', SUITE / 'app', ['test_app_memory'], [], True),
    ('APP novos 9 (frente 3)', SUITE / 'app', ['test_app_filters'], [], True),
    ('HEARTBEAT novos 15 (frente 2)', HERE / 'hb' / 'tests', ['test_heartbeat_v2', 'test_heartbeat_stub_server'], [], True),
    ('FILA 55 (origem)', SUITE / 'queue', FILA55, [CORE], False, SUITE / 'queue' / 'rodar_fila55.py'),
    ('FILA novos 5 (frente 3)', SUITE / 'queue', ['test_filters_queue'], [CORE], False),
    ('BLOCOS 5 (frente 3)', SUITE / 'blocos', ['test_blocks'], [], False),
    ('INTEGRACAO novos (esta frente)', SUITE / 'integracao', ['test_integracao'], [CORE], False),
    ('R2 novos (achados bloqueantes 13/10)', SUITE / 'r2', ['test_r2'], [CORE, str(SUITE / 'sessions')], False),
    ('R2.1 novos (revisao R2 13/10)', SUITE / 'r2_1', ['test_r2_1'], [CORE, str(SUITE / 'sessions')], False),
    ('R2.1 heartbeat novos (revisao R2 13/10)', HERE / 'hb' / 'tests', ['test_heartbeat_r2_1'], [], True),
    ('R2.2 novos (revisao R2.1 13/10)', SUITE / 'r2_2', ['test_r2_2'], [CORE, str(SUITE / 'sessions')], False),
    ('R2.2 app novos (revisao R2.1 13/10)', SUITE / 'app', ['test_app_r2_2'], [], True),
]
LINE = re.compile(r'^(?P<name>test_\w+) \((?P<cls>[\w.]+)\)(?: \.\.\.)?(?: (?P<res>ok|FAIL|ERROR|skipped.*|expected failure|unexpected success))?\s*$')
# um print do código testado pode cair entre o nome e o veredito (ex.: "[Memoria] ERRO lendo ..."): o veredito vem na linha seguinte
LINE_PRINT = re.compile(r'^(?P<name>test_\w+) \((?P<cls>[\w.]+)\) \.\.\. (?P<rest>.+)$')
TAIL = re.compile(r'^.* \.\.\. (?P<res>ok|FAIL|ERROR|skipped.*)$')
OUTCOME = re.compile(r'^(?P<res>ERROR|FAIL): (?P<name>test_\w+) \((?P<cls>[\w.]+)\)')


def parse(err):
    tests, index, pending = [], {}, None
    for raw in err.splitlines():
        line = raw.strip()
        m = LINE.match(line)
        if m:
            res = m.group('res')
            item = {'module': m.group('cls').split('.')[0], 'class': m.group('cls'), 'test': m.group('name'),
                    'result': ('PASSA' if res == 'ok' else 'PULADO' if res and res.startswith('skipped') else 'FALHA' if res else 'PENDENTE'),
                    'raw': res or ''}
            tests.append(item)
            index[(m.group('cls'), m.group('name'))] = item
            pending = item if not res else None
            continue
        mp = LINE_PRINT.match(line)
        if mp and not re.match(r'^(ok|FAIL|ERROR|skipped)', mp.group('rest')):
            item = {'module': mp.group('cls').split('.')[0], 'class': mp.group('cls'), 'test': mp.group('name'),
                    'result': 'PENDENTE', 'raw': '(print entre o nome e o veredito)'}
            tests.append(item)
            index[(mp.group('cls'), mp.group('name'))] = item
            pending = item
            continue
        if pending is not None and re.match(r'^(ok|FAIL|ERROR|skipped)', line):
            res = line.split()[0]
            pending['result'] = 'PASSA' if res == 'ok' else 'PULADO' if res.startswith('skipped') else 'FALHA'
            pending['raw'] = line[:40]
            pending = None
            continue
        if pending is not None:
            t = TAIL.match(line)
            if t:
                res = t.group('res')
                pending['result'] = 'PASSA' if res == 'ok' else 'PULADO' if res.startswith('skipped') else 'FALHA'
                pending['raw'] = res
                pending = None
                continue
        o = OUTCOME.match(line)
        if o and (o.group('cls'), o.group('name')) in index:
            item = index[(o.group('cls'), o.group('name'))]
            item['result'] = 'FALHA'
            item['raw'] = o.group('res') + ' (subtest)'
    for item in tests:
        if item['result'] == 'PENDENTE':  # subtests all passed: unittest -v prints no trailing ok
            item['result'], item['raw'] = 'PASSA', 'ok (subtests)'
    return tests


def run(label, cwd, modules, extra_path, ext, script=None):
    env = dict(os.environ)
    tmp = INT / 'tmp' / 'run'
    tmp.mkdir(parents=True, exist_ok=True)
    (INT / 'tmp' / 'arquivo_D').mkdir(parents=True, exist_ok=True)
    ext_tmp = ('\\\\?\\' + str(tmp)) if ext else str(tmp)
    env.update(PYTHONPATH=os.pathsep.join([str(INT / 'guard')] + extra_path), ACOM_AUDIT_ROOT=str(INT),
               TEMP=ext_tmp, TMP=ext_tmp, TMPDIR=ext_tmp, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1',
               PYTHONIOENCODING='utf-8', NO_PROXY='*', HTTP_PROXY='', HTTPS_PROXY='',
               IALD_MEMORY_SNAPSHOT_ARCHIVE_DIR=str(INT / 'tmp' / 'arquivo_D'),
               NUCLEO_EVIDENCIAS=str(HERE / 'nucleo' / 'evidencias'),
               INTEGRACAO_EVIDENCIAS=str(INT / 'evidencias_r2'))
    (INT / 'guard_log').mkdir(exist_ok=True)
    start = time.time()
    cmd = [PY, '-B', '-X', 'utf8', str(script)] if script else [PY, '-B', '-X', 'utf8', '-m', 'unittest', '-v'] + modules
    proc = subprocess.run(cmd, cwd=str(cwd), env=env, capture_output=True, timeout=1800)
    err = proc.stderr.decode('utf-8', 'replace')
    out = proc.stdout.decode('utf-8', 'replace')
    tests = parse(err + '\n' + out)
    ran = re.search(r'Ran (\d+) tests? in ([\d.]+)s', err)
    ok = proc.returncode == 0 and err.rstrip().endswith('OK')
    (INT / 'evidencias_r2' / 'unittest').mkdir(parents=True, exist_ok=True)
    slug = re.sub(r'[^A-Za-z0-9]+', '_', label).strip('_')
    (INT / 'evidencias_r2' / 'unittest' / f'{slug}.txt').write_text(err + '\n--- stdout ---\n' + out, encoding='utf-8')
    return {'suite': label, 'cwd': str(cwd), 'modules': modules, 'returncode': proc.returncode,
            'ran': int(ran.group(1)) if ran else None, 'seconds': round(time.time() - start, 2), 'ok': ok,
            'tests': tests, 'stderr_tail': err[-5000:]}


def guard_summary(before):
    folder = INT / 'guard_log'
    kinds, blocks, procs = {}, [], 0
    for path in sorted(folder.glob('guard_*.jsonl')):
        if path.name in before:
            continue
        procs += 1
        for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
            try:
                item = json.loads(line)
            except ValueError:
                continue
            k = item.get('kind', '')
            kinds[k] = kinds.get(k, 0) + 1
            if k.startswith('BLOCK'):
                blocks.append({x: item.get(x) for x in ('kind', 'event', 'path', 'src', 'dst', 'args', 'mode')})
    return {'processes': procs, 'kinds': kinds, 'blocks': blocks[:60], 'n_blocks': len(blocks)}


def main(selected=None):
    before = {p.name for p in (INT / 'guard_log').glob('guard_*.jsonl')}
    specs = [s for s in SUITES if not selected or any(k in s[0] for k in selected)]
    results = [run(*spec) for spec in specs]
    summary = guard_summary(before)
    total = sum(len(r['tests']) for r in results)
    passed = sum(t['result'] == 'PASSA' for r in results for t in r['tests'])
    failed = sum(t['result'] == 'FALHA' for r in results for t in r['tests'])
    skipped = sum(t['result'] == 'PULADO' for r in results for t in r['tests'])
    all_ok = all(r['ok'] for r in results)
    report = {'at': datetime.now(timezone.utc).isoformat(), 'python': PY, 'all_ok': all_ok, 'total': total,
              'passed': passed, 'failed': failed, 'skipped': skipped, 'suites': results, 'guard': summary}
    name = 'RESULTADOS_TESTES.json' if not selected else 'RESULTADOS_TESTES_parcial.json'
    (HERE / name).write_text(json.dumps(report, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    lines = ['# TESTES — INTEGRAÇÃO R2 (conserto ACOM 12/10; candidato_r2)', '',
             'Rodados em %s com `%s` sobre CÓPIAS do candidato (`testes\\`), sob a guarda `sitecustomize.py` da auditoria. '
             'Nenhuma chamada a provedor. Resultado medido aqui [REAL]: **%d testes, %d PASSA, %d FALHA, %d pulado(s)** — %s.'
             % (report['at'], PY, total, passed, failed, skipped, 'todas as suítes OK' if all_ok else 'HÁ SUÍTE COM FALHA'), '',
             '| suíte | módulos | rodados | PASSA | FALHA | segundos | OK |', '|---|---|---|---|---|---|---|']
    for r in results:
        p = sum(t['result'] == 'PASSA' for t in r['tests'])
        f = sum(t['result'] == 'FALHA' for t in r['tests'])
        lines.append('| %s | %s | %s | %d | %d | %s | %s |' % (r['suite'], ', '.join(r['modules']), r['ran'], p, f, r['seconds'], 'sim' if r['ok'] else 'NÃO'))
    lines += ['', '## Cada teste', '', '| suíte | módulo | teste | resultado |', '|---|---|---|---|']
    for r in results:
        for t in r['tests']:
            lines.append('| %s | `%s` | `%s` | %s |' % (r['suite'], t['module'], t['test'], t['result']))
    lines += ['', '## Guarda de execução (auditoria)', '',
              'processos sob guarda nesta rodada: %d; eventos por tipo: `%s`; bloqueios: %d' % (summary['processes'], json.dumps(summary['kinds']), summary['n_blocks']), '']
    for b in summary['blocks'][:20]:
        lines.append('- BLOQUEIO: `%s`' % json.dumps(b, ensure_ascii=False))
    for r in results:
        if not r['ok']:
            lines += ['', '## Saída da suíte com falha: %s' % r['suite'], '', '```', r['stderr_tail'], '```']
    (HERE / ('TESTES.md' if not selected else 'TESTES_parcial.md')).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({'all_ok': all_ok, 'total': total, 'passed': passed, 'failed': failed, 'skipped': skipped,
                      'suites': [(r['suite'], r['ran'], r['ok'], r['seconds']) for r in results],
                      'guard_blocks': summary['n_blocks'], 'guard_kinds': summary['kinds']}, ensure_ascii=False))
    return 0 if all_ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:] or None))
