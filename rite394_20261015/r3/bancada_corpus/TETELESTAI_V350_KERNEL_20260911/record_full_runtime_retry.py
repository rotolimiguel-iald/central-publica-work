"""Preserve the failed attempt and record the shortened runtime path."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os

ROOT = Path(__file__).resolve().parent
RUN = ROOT / 'r'
PARENT = ROOT / 'runtime_preparation_custody.json'
STAMP = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
MARKER = 'TETELESTAI_V350_RETORNO_CAMINHO_CURTO_20260913'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, data):
    temp = p.with_name(p.name + '.tmp_' + STAMP)
    with temp.open('xb') as f: f.write(data)
    assert temp.read_bytes() == data
    os.replace(temp, p)
    assert p.read_bytes() == data
def encode(x): return (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
parent = json.loads(PARENT.read_bytes())
state = json.loads((RUN / 'runtime_process_02.json').read_bytes())
assert state['status'] == 'RUNNING'
assert sha(ROOT / 'um.py') == sha(RUN / 'um.py') == parent['working_sha256']
paths = [Path(p) for p in parent['surface_sha256']]
extra = [ROOT / 'RELATORIO_EXECUCAO_INTEGRAL.md', ROOT / 'RUNTIME_ATIVO.json']
before = {p: p.read_bytes() for p in paths + extra}
assert all(sha(p) == parent['surface_sha256'][str(p)] for p in paths)
assert all(MARKER.encode() not in raw for raw in before.values())
note = f'''

## {MARKER} — {datetime.now().astimezone().isoformat(timespec='seconds')}

[REAL — falha de ambiente preservada] A tentativa01 teve Lake build rc1:
não conseguiu abrir IntegralRepresentation.olean.server.hash pelo caminho longo.
A auditoria rc1 encontrou V350GateContract.olean ausente em consequência da build
incompleta. A rodada foi interrompida, com as capturas copiadas byte a byte para
`{(RUN / 'failed_attempt_01').as_posix()}`. Nenhuma prova foi alterada.

[REAL — retomada operacional] A pasta física foi renomeada dentro da área autorizada
para `{RUN.as_posix()}`; o endereço longo anterior virou junção para esta mesma
cópia, preservando os links históricos. Nova execução em {state['started']},
PID {state['pid']}, stdout/stderr com sufixo02. [EM CURSO] Resultado final ainda
pendente; não reiniciar enquanto estiver ativa. A captura principal anterior só
será substituída quando a nova build/auditoria terminarem; conferir timestamp e etapa.

[ESCOPO] As 11 entradas já ligadas continuam sendo o contrato. Nenhuma nova
função de prova, requisito matemático ou alteração de gate foi acrescentada.
Estado atual: `{(RUN / 'runtime_process_02.json').as_posix()}`.
'''.encode('utf-8')
backups = {}
for p, raw in before.items():
    backup = p.with_name(p.name + '.bak_' + STAMP)
    with backup.open('xb') as f: f.write(raw)
    assert backup.read_bytes() == raw
    backups[str(p)] = str(backup)
for p in paths + [extra[0]]:
    assert p.read_bytes() == before[p]
    write(p, before[p] + note)
locator = json.loads(before[extra[1]])
locator.update({'runtime_directory': str(RUN), 'pid_at_start': state['pid'],
    'attempt': 2, 'process_status_file': str(RUN / 'runtime_process_02.json'),
    'stdout': str(RUN / 'runtime_stdout_02.txt'), 'stderr': str(RUN / 'runtime_stderr_02.txt'),
    'previous_attempt_archive': str(RUN / 'failed_attempt_01'),
    'custody': str(ROOT / 'runtime_short_path_custody.json')})
write(extra[1], encode(locator))
c = dict(parent)
artifacts = dict(parent['artifacts'])
for name in artifacts:
    p = ROOT / name
    if p in before: artifacts[name] = sha(p)
for p in [Path(__file__), ROOT / 'run_full_runtime_attempt02.py', *extra, RUN / 'failed_attempt_01/failure_record.json']:
    artifacts[str(p.relative_to(ROOT))] = sha(p)
c.update({'timestamp': datetime.now().astimezone().isoformat(), 'status': 'FULL_RUNTIME_ATTEMPT02_RUNNING',
    'previous_custody_path': str(PARENT), 'previous_custody_sha256': sha(PARENT),
    'surface_before_sha256': parent['surface_sha256'], 'surface_sha256': {str(p): sha(p) for p in paths},
    'backups': backups, 'artifacts': artifacts, 'marker': MARKER,
    'runtime_directory': str(RUN), 'runtime_pid_at_start': state['pid'], 'runtime_attempt': 2,
    'runtime_result_pending': True, 'full_goal_complete': False,
    'report_sha256': sha(extra[0]), 'new_modules_integrated_this_record': 0})
target = ROOT / 'runtime_short_path_custody.json'
assert not target.exists()
write(target, encode(c))
print(json.dumps({'recorded': True, 'memory_surfaces': len(paths), 'backups': len(backups),
    'custody_sha256': sha(target), 'attempt': 2, 'pid': state['pid']}))
