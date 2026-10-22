"""Freeze the two full-domain right-scaling modules before independent review."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NAMES = ['ScalarRegularRightGNS', 'ScalarRegularRightTomita', 'ScalarRegularRightSquare']
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def create(path, raw):
    assert raw and not path.exists() and path.resolve().is_relative_to(ROOT)
    temp = path.with_suffix(path.suffix + '.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw
    temp.replace(path)
    assert path.read_bytes() == raw

parent_path = ROOT / 'right_square_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
assert parent['matrix_unit_right_scaling_on_full_square_domain'] and not parent['KMS_proved']
for name, pin in parent['artifacts'].items():
    assert sha(ROOT / name) == pin, name
for name, pin in parent['surface_sha256'].items():
    assert sha(Path(name)) == pin, name
modules, targets = {}, {}
for name in NAMES:
    source = ROOT / 'kernel/TGLV350' / (name + '.lean')
    binary = ROOT / 'build/TGLV350' / (name + '.olean')
    history = [(p, json.loads(p.read_bytes())) for p in sorted((ROOT / 'logs').glob(name + '_*.json'))]
    accepted = [(p, v) for p, v in history if v['returncode'] == 0 and
        v['sha256'] == sha(source) and v['output_sha256'] == sha(binary)]
    assert accepted, name
    log, row = accepted[-1]
    assert row['source_unchanged_during_compile']
    stdout, stderr = Path(row['stdout']), Path(row['stderr'])
    output = stdout.read_text(encoding='utf-8')
    assert stderr.read_bytes() == b''
    names = re.findall(r'^#print axioms ([\w.]+)$', source.read_text(encoding='utf-8'), re.M)
    for short in names:
        full = 'TGLV350.Regular.' + short
        match = re.search(re.escape("'" + full + "' depends on axioms: [") + r'([^]]*)\]', output)
        assert match, full
        axioms = sorted(x.strip() for x in match.group(1).split(',') if x.strip())
        assert set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'}
        assert full not in targets
        targets[full] = axioms
    modules[name] = {'source_sha256': sha(source), 'binary_sha256': sha(binary),
        'targets': len(names), 'final_log': str(log), 'final_log_sha256': sha(log),
        'stdout_sha256': sha(stdout), 'stderr_sha256': sha(stderr),
        'failed_attempts': [str(p) for p, v in history if v['returncode']]}
assert len(targets) == 36
report = ROOT / 'RELATORIO_DIREITA_UNITARIA_REGULAR_DEV.md'
create(report, f'''# Direita unitária regular no mesmo GNS — DEV

{DATE}. [REAL — três módulos/36 alvos compilados; revisão e integração pendentes]

Reutilizada scalarOrbit_right_regular para construir R_t Λ(A)=Λ(A λ_t)
no GNS do peso escalar completo. No espaço de órbitas, R_t é o multiplicador
de caráter na coordenada exterior composto com o shift na fibra interior.
São coordenadas diferentes. O produto A λ_t preserva n_ν e sua seminorma.
R_0=I, R_s R_t=R_(s+t), R_t*=R_(-t): a ação GNS é unitária.

No mesmo S fechado e seu adjunto máximo F=S†, o transporte do gráfico prova
R_t D(S)⊆D(S), S R_t=π(λ_t*)S; π(λ_t)D(F)⊆D(F), Fπ(λ_t)=R_t*F.
Daí, no MESMO A=S†S e em TODO domínio composto:

    R_t x ∈ D(A) ↔ x ∈ D(A),       A R_t x = R_t A x.

A equivalência de domínio usa a inversa já construída R_(-t). Nenhum campo
KMS ou igualdade de fluxo foi acrescentado como hipótese. A construção
atua na família λ_t; ainda não é uma representação direita provada de N inteiro.

[OPEN] Identificar A^it com o fluxo candidato e provar KMS global; traço,
escala dual, canto Three Locks, H1/H2/H3 físicos compatíveis, setor quântico
interagente e consumo integral pelo certificado/runtime. Seis flags falsas.
O vínculo de domínio antes aberto para λ_t foi reduzido por prova concreta.

Integração anterior: {parent['integrated_records']} registros,
{parent['controls']} controles, {parent['audit_declarations']} declarações Audit.
Este DEV ainda não altera um.py nem as 34 memórias: atualização pendente
após revisão nesta sessão. Cópia `{sha(ROOT / 'um.py')}`, mãe `{sha(parent_path)}`.
Monólito original e cópia não foram executados/importados integralmente.
Falha auxiliar de impressão cp1252 não afetou bytes da fonte nova; foi
conferida por releitura e pela compilação. Não houve falha matemática por isso.
'''.encode('utf-8'))
manifest = {'timestamp': DATE, 'status': 'DEV_COMPILED__REVIEW_AND_INTEGRATION_PENDING',
    'modules': modules, 'targets': targets, 'report_path': str(report), 'report_sha256': sha(report),
    'parent_custody_path': str(parent_path), 'parent_custody_sha256': sha(parent_path),
    'integrated_working_sha256': sha(ROOT / 'um.py'),
    'same_actual_square_domain_regular_invariant': True,
    'regular_right_commutes_on_full_square_domain': True,
    'KMS_proved': False, 'modular_square_flow_identified': False,
    'independent_review_complete': False, 'integrated': False,
    'memory_update_pending_review_in_this_turn': True,
    'gate_changed': False, 'full_goal_complete': False}
create(ROOT / 'regular_right_draft_status.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'integrated': False}))
