"""Record the reviewed formal stage without claiming the full runtime completed."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import re

ROOT = Path(__file__).resolve().parent
RUN = ROOT / 'r'
PARENT = ROOT / 'runtime_short_path_custody.json'
STAMP = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
MARKER = 'TETELESTAI_V350_ETAPA_FORMAL_INTEGRAL_VERIFICADA_20260913'
REVIEW = ROOT / 'revisao/REVIEW_FULL_RUNTIME_FORMAL_STAGE.md'
REVIEW_DATA = ROOT / 'revisao/full_runtime_formal_stage_20260913_093418_886098/evidence.json'

def sha(path):
    with path.open('rb') as f: return hashlib.file_digest(f, 'sha256').hexdigest()
def encode(value): return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
def atomic(path, raw):
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    with temp.open('xb') as f: f.write(raw)
    assert temp.read_bytes() == raw
    os.replace(temp, path)
    assert path.read_bytes() == raw

parent = json.loads(PARENT.read_bytes())
own = json.loads((RUN / 'formal_stage_verification.json').read_bytes())
review = json.loads(REVIEW_DATA.read_bytes())
state = json.loads((RUN / 'runtime_process_02.json').read_bytes())
assert state['status'] == 'RUNNING'
assert own['audited_unique_terms'] == 7133 and own['principal_gate_terms_verified']
assert len(review['axiom_report']) == 7133 and len(review['gate_entries']) == 11
assert review['missing'] == review['extra'] == review['conflicts'] == []
assert 'Nenhum achado P0–P2' in REVIEW.read_text(encoding='utf-8')
assert sha(ROOT / 'um.py') == sha(RUN / 'um.py') == parent['working_sha256']
original = Path(json.loads((ROOT / 'environment.json').read_bytes())['original_source'])
assert sha(original) == parent['original_sha256']

# Extract the exact normalized stdout represented by the capture writer.
capture = (RUN / 'tgl_kernel_audit_capture.txt').read_text(encoding='utf-8')
stdout = capture.split('--- STDOUT ---\n', 1)[1].rsplit('\n--- STDERR ---\n', 1)[0]
assert len(stdout) == int(re.search(r'# len\(stdout\)=(\d+)', capture).group(1))
stdout_path = RUN / 'audit_principal.stdout.txt'
assert not stdout_path.exists()
atomic(stdout_path, stdout.encode('utf-8'))

paths = [Path(p) for p in parent['surface_sha256']]
extra = [ROOT / 'RELATORIO_EXECUCAO_INTEGRAL.md', ROOT / 'RUNTIME_ATIVO.json']
before = {p: p.read_bytes() for p in paths + extra}
for p in paths:
    assert sha(p) == parent['surface_sha256'][str(p)] and MARKER.encode() not in before[p]
note = f'''

## {MARKER} — {datetime.now().astimezone().isoformat(timespec='seconds')}

[REAL — etapa formal da tentativa02] Lake build e Audit concluíram rc0. Foram
conferidos os 7.133 nomes únicos pedidos por #print axioms, com sete repetições
consistentes e 50 declarações sem axiomas. Nenhum nome faltante/extra, conflito ou
axioma fora de propext/Classical.choice/Quot.sound. Os onze fornecedores formais
do gate principal estão presentes. Nenhum módulo/prova/condição foi acrescentado.

[REAL — revisão independente parcial] O revisor leu as capturas novas, comparou
os 922 arquivos embutidos/materializados e os onze fornecedores, e não encontrou
P0–P2. Não recompilou o kernel. A cobertura individual de axiomas refere-se aos
comandos #print; os #check não viraram uma exigência adicional.
[Parecer integral](<{REVIEW.as_posix()}>).
[Verificação autoral](<{(RUN / 'formal_stage_verification.json').as_posix()}>).

[EM CURSO] O programa continua seus cálculos. Autoteste, selo, JSONs e resultados
finais ainda não foram conferidos. A etapa formal aprovada não declara conclusão
da execução integral. Processo {state['pid']}, sessão autoral94059; não reiniciar.
Ler RUNTIME_ATIVO.json e runtime_process_02.json antes de retomar. O contrato
continua consolidação/reuso; não retomar novas provas de original-S/KMS/UV.
'''.encode('utf-8')
backups = {}
for p, raw in before.items():
    b = p.with_name(p.name + '.bak_' + STAMP)
    with b.open('xb') as f: f.write(raw)
    assert b.read_bytes() == raw
    backups[str(p)] = str(b)
for p in paths + [extra[0]]:
    assert p.read_bytes() == before[p]
    atomic(p, before[p] + note)
    assert p.read_bytes().startswith(before[p])
locator = json.loads(before[extra[1]])
locator.update({'formal_stage_verified': True, 'formal_stage_independent_review_completed': True,
    'formal_stage_audit_terms': 7133, 'formal_stage_gate_terms': 11,
    'full_runtime_result_pending': True,
    'remaining_action': 'Validate full numerical execution, fail-closed selftest, final seals and JSONs; no new proofs.',
    'custody': str(ROOT / 'runtime_formal_stage_custody.json')})
atomic(extra[1], encode(locator))

artifacts = dict(parent['artifacts'])
for name in artifacts:
    p = ROOT / name
    if p in before: artifacts[name] = sha(p)
new = [Path(__file__), *extra, REVIEW, REVIEW_DATA,
       ROOT / 'revisao/review_full_runtime_formal_stage.py',
       RUN / 'formal_stage_verification.json', stdout_path,
       RUN / 'tgl_kernel_build_capture.txt', RUN / 'tgl_kernel_audit_capture.txt']
for p in new: artifacts[str(p.relative_to(ROOT))] = sha(p)
c = dict(parent)
c.update({'timestamp': datetime.now().astimezone().isoformat(),
    'status': 'FULL_RUNTIME_FORMAL_STAGE_VERIFIED_AND_REVIEWED__REST_PENDING',
    'previous_custody_path': str(PARENT), 'previous_custody_sha256': sha(PARENT),
    'surface_before_sha256': parent['surface_sha256'], 'surface_sha256': {str(p): sha(p) for p in paths},
    'backups': backups, 'artifacts': artifacts, 'marker': MARKER,
    'runtime_result_pending': True, 'new_full_runtime_performed': False, 'full_goal_complete': False,
    'runtime_formal_stage_verified': True, 'runtime_formal_stage_independently_reviewed': True,
    'runtime_formal_gate_terms_verified': 11, 'runtime_formal_audit_terms': 7133,
    'current_audit_stdout_path': str(stdout_path), 'current_audit_stdout_sha256': sha(stdout_path),
    'current_audit_stdout_kind': 'UTF8_LF_STDOUT_EXTRACTED_FROM_PRINCIPAL_CAPTURE',
    'runtime_formal_review_path': str(REVIEW), 'runtime_formal_review_sha256': sha(REVIEW),
    'report_sha256': sha(extra[0]), 'new_modules_integrated_this_record': 0})
p = ROOT / 'runtime_formal_stage_custody.json'
assert not p.exists()
atomic(p, encode(c))
print(json.dumps({'recorded': True, 'memory_surfaces': len(paths), 'backups': len(backups),
    'custody_sha256': sha(p), 'original_unchanged': sha(original) == parent['original_sha256'],
    'formal_stage_verified': True, 'full_runtime_pending': True}))
