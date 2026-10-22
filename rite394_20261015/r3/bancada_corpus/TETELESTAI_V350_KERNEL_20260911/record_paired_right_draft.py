"""Freeze actual right pairs, their original maximal adjoint and generated commutant."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NAMES = ['ScalarRightAdjointPair', 'ScalarCommutantSandwich', 'ScalarPairedRightAlgebra']
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

parent_path = ROOT / 'right_regularization_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
assert parent['full_weight_right_averages_constructed'] and not parent['KMS_proved']
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
assert len(targets) == 29
report = ROOT / 'RELATORIO_ALGEBRA_DIREITA_ADJUNTO_DEV.md'
create(report, f'''# Álgebra direita e adjunto original — DEV

{DATE}. [REAL — três módulos/29 alvos compilados; revisão e integração pendentes]

No mesmo H_I, com o ideal completo n_ν e os operadores fechados originais
S e F=S†, ScalarRightAdjointPair dá dois vetores η, ζ para um operador limitado R:
RΛν(a)=π(a)η e R*Λν(a)=π(a)ζ para todo a∈n_ν.
[REAL] A relação Fη=ζ é PROVADA dessas identidades, não incluída nas hipóteses.
A prova regulariza, passa ao limite no pareamento e usa o fecho do grafo
completo de S e a caracterização maximal do adjunto original.

[REAL] Para todo T∈π(N)', K_h(T)=R_h* T R_h possui esse par direito,
com η=R_h*Tη_h e ζ=R_h*T*η_h, onde η_h=Λν(e_h), h>0.
||K_h(T)||≤||T|| e K_h(T)→T fortemente-* quando h↓0.
A ordem dos fatores é preservada: não se supõe que T comute com R_h.
R_h*→I usa o bound de contração; não se presume continuidade geral de star em SOT.

[REAL] Os operadores com par direito formam uma NonUnitalStarSubalgebra:
zero, soma, multiplicação escalar, produto e adjunto foram construídos.
A álgebra de von Neumann gerada por ela é TODO o comutante π(N)'.

[OPEN] Isso é uma álgebra de operadores limitados com dois vetores direitos.
Ainda não é a plenitude de uma álgebra de Hilbert, nem a densidade de um
núcleo de grafo para F, nem a reconstrução R=Jπ(b)J. A inclusão inversa
π(N)'⊆Jπ(N)J e o fechamento von Neumann da imagem π(N) continuam abertos.
O J original não foi trocado por conjugação de estado gaussiano.
Permanecem abertos Δ^it/KMS, traço/escala/canto Three Locks, H1/H2/H3 físicos,
setor interagente e consumo por certificados tipados/runtime.
Seis flags maiores falsas; esta construção não muda o gate.

[REAL — fiação preservada] As seis flags maiores qgf/gpf não entram diretamente
em evaluate_quantum_gravity_closure: o selo legado lê qgc_, qgp_ e o feed
experimental; kernel_frontier é anexado depois. O consumo por certificado
tipado continua necessário para que novas provas movam esse selo.

Integração anterior: {parent['integrated_records']} registros,
{parent['controls']} controles, {parent['audit_declarations']} declarações Audit.
Este DEV não altera um.py nem as 34 memórias; atualização pendente de revisão
nesta sessão. Cópia `{sha(ROOT / 'um.py')}`, mãe `{sha(parent_path)}`.
Tentativas Lean recusadas e fontes anteriores foram preservadas; somente
logs rc0 dos bytes atuais são aceitos. Nenhum monólito executado/importado.
'''.encode('utf-8'))
manifest = {'timestamp': DATE, 'status': 'DEV_COMPILED__REVIEW_AND_INTEGRATION_PENDING',
    'modules': modules, 'targets': targets, 'report_path': str(report), 'report_sha256': sha(report),
    'parent_custody_path': str(parent_path), 'parent_custody_sha256': sha(parent_path),
    'integrated_working_sha256': sha(ROOT / 'um.py'),
    'original_adjoint_right_pairs_constructed': True,
    'paired_right_star_algebra_constructed': True,
    'paired_right_algebra_generates_commutant': True,
    'original_weight_J_not_replaced': True,
    'KMS_proved': False, 'modular_square_flow_identified': False,
    'independent_review_complete': False, 'integrated': False,
    'memory_update_pending_review_in_this_turn': True,
    'gate_changed': False, 'full_goal_complete': False}
create(ROOT / 'paired_right_draft_status.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'integrated': False}))
