"""Record operational progress with exact-byte memory backups; no new proof claims."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os

ROOT = Path(__file__).resolve().parent
RUN = ROOT / 'RODADA_INTEGRAL_20260913_082315'
PARENT = ROOT / 'gate_scope_correction_custody.json'
STAMP = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
MARKER = 'TETELESTAI_V350_RODADA_INTEGRAL_INICIADA_20260913'

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def atomic(path, data):
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    with temp.open('xb') as f:
        f.write(data)
    assert temp.read_bytes() == data
    os.replace(temp, path)
    assert path.read_bytes() == data

def emit(path, value):
    assert not path.exists()
    atomic(path, (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

parent = json.loads(PARENT.read_bytes())
manifest = json.loads((RUN / 'input_manifest.json').read_bytes())
tex = json.loads((RUN / 'tex_input_manifest.json').read_bytes())
process = json.loads((RUN / 'runtime_process.json').read_bytes())
assert process['status'] == 'RUNNING'
assert sha(ROOT / 'um.py') == sha(RUN / 'um.py') == parent['working_sha256']
original = Path(json.loads((ROOT / 'environment.json').read_bytes())['original_source'])
assert sha(original) == sha(ROOT / 'fontes/um_v350_original.py') == parent['original_sha256']
before = {Path(p): Path(p).read_bytes() for p in parent['surface_sha256']}
assert len(before) == 34
for p, raw in before.items():
    assert sha(p) == parent['surface_sha256'][str(p)]
    assert MARKER.encode() not in raw
    assert p.resolve().is_relative_to(ROOT) or p.resolve() in (
        ROOT.parent.parent / 'memory/TGL_ATLAS.md', ROOT.parent.parent / 'memory/TGL_INDICE_VIVO.md')

report = f'''# Execução integral da cópia — início registrado

[REAL] A execução começou em {process['started']}, processo {process['pid']}.
Programa em `{RUN.as_posix()}/um.py`, idêntico à cópia de trabalho por SHA-256.
O kernel embutido contém {manifest['embedded_files']} arquivos. Foram copiadas e
conferidas {manifest['copied_files']} entradas de programa/dados/dependências,
mais {tex['copied_files']} entradas do ambiente TeX. As dependências são cópias
físicas; as três raízes do MiKTeX foram confirmadas dentro da rodada.

[REAL] Modo formal strict, autoteste ativo, TGL_RITE_CHECKPOINT=0. Os dados são
os já disponíveis; a execução não inicia novas cadeias MCMC. O cache de compilação
copiado é uma entrada de desempenho, não evidência nova: o programa executa Lake
e a auditoria efetivamente. Os controles de rede dos dados estão em modo local.

[REAL] A primeira preparação parou com WinError 3 em CopyFile2. A retomada usou
prefixos de caminhos longos, conferiu os arquivos já copiados e terminou. Há dois
destinos acima de 260 caracteres (máximo 264); nenhuma falha virou sucesso presumido.

[EM CURSO] O kernel foi materializado e a compilação iniciou. Ainda não há
resultado final desta rodada, selo novo validado ou autoteste concluído.

[ESCOPO ATIVO] As 11 entradas do gate principal já estavam ligadas e auditadas.
Esta etapa valida a execução conjunta. Nenhum módulo Lean, prova matemática,
condição de gate ou flag principal foi acrescentado. A pesquisa adicional
permanece suspensa conforme o contrato ativo.

Consultar `runtime_process.json`, `runtime_stdout.txt`, `runtime_stderr.txt` e,
quando existirem, os JSONs/capturas emitidos em `{RUN.as_posix()}`. Não reiniciar
enquanto o processo ou seus filhos estiverem ativos. A saída completa e o
autoteste ainda precisam ser verificados antes de declarar a integração validada.
'''
report_path = ROOT / 'RELATORIO_EXECUCAO_INTEGRAL.md'
assert not report_path.exists()
atomic(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {datetime.now().astimezone().isoformat(timespec='seconds')}

[REAL — operação, não nova derivação] Execução integral iniciada na cópia
`{RUN.as_posix()}/um.py`, PID {process['pid']}; original preservado. Kernel de922
arquivos, modo strict, autoteste ativo, checkpoints de ritos desligados. Dados e
dependências copiados e conferidos. [EM CURSO] Compilação iniciada; ainda não há
veredito final validado desta execução. Nenhum novo módulo ou requisito do gate.

[RETOMADA] O contrato ativo continua sendo consolidação/reuso das 11 entradas já
ligadas. Aguardar e conferir esta rodada, sem reiniciá-la nem retomar novas provas.
[Relatório operacional](<{report_path.as_posix()}>).
Estado do processo: `{(RUN / 'runtime_process.json').as_posix()}`.
'''.encode('utf-8')
backups = {}
for p, raw in before.items():
    backup = p.with_name(p.name + '.bak_' + STAMP)
    with backup.open('xb') as f:
        f.write(raw)
    assert backup.read_bytes() == raw
    backups[str(p)] = str(backup)
for p, raw in before.items():
    assert p.read_bytes() == raw
    atomic(p, raw + note)
    assert p.read_bytes().startswith(raw) and len(p.read_bytes()) > len(raw)

artifacts = dict(parent['artifacts'])
for p in [report_path, ROOT / 'prepare_full_runtime.py', ROOT / 'run_full_runtime.py', Path(__file__),
          RUN / 'input_manifest.json', RUN / 'tex_input_manifest.json', RUN / 'preparation_status.json',
          RUN / 'environment_preflight/results.json', RUN / 'environment_preflight/command_1_stdout.txt']:
    artifacts[str(p.relative_to(ROOT))] = sha(p)
for p in before:
    if p.is_relative_to(ROOT) and str(p.relative_to(ROOT)) in artifacts:
        artifacts[str(p.relative_to(ROOT))] = sha(p)
custody = dict(parent)
custody.update({'timestamp': datetime.now().astimezone().isoformat(),
    'status': 'FULL_RUNTIME_STARTED__RESULT_PENDING', 'previous_custody_path': str(PARENT),
    'previous_custody_sha256': sha(PARENT), 'surface_before_sha256': parent['surface_sha256'],
    'surface_sha256': {str(p): sha(p) for p in before}, 'backups': backups, 'marker': MARKER,
    'artifacts': artifacts, 'runtime_directory': str(RUN), 'runtime_pid_at_start': process['pid'],
    'new_full_runtime_started': True, 'new_full_runtime_performed': False,
    'runtime_result_pending': True, 'report_path': str(report_path), 'report_sha256': sha(report_path),
    'full_goal_complete': False, 'new_modules_integrated_this_record': 0})
emit(ROOT / 'runtime_preparation_custody.json', custody)
emit(ROOT / 'RUNTIME_ATIVO.json', {'runtime_directory': str(RUN), 'pid_at_start': process['pid'],
    'process_status_file': str(RUN / 'runtime_process.json'), 'custody': str(ROOT / 'runtime_preparation_custody.json'),
    'remaining_action': 'Validate the running full program and fail-closed selftest; no new proofs.',
    'do_not_launch_duplicate': True})
print(json.dumps({'recorded': True, 'memory_surfaces': len(before),
    'custody_sha256': sha(ROOT / 'runtime_preparation_custody.json'),
    'working_sha256': sha(ROOT / 'um.py'), 'original_unchanged': sha(original) == parent['original_sha256']}, ensure_ascii=False))
