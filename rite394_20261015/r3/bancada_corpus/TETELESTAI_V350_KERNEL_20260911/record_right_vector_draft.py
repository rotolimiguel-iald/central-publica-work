"""Freeze actual dense right vectors and their closable original-adjoint involution."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NAMES = ['ScalarGaussianRightPairs', 'ScalarRightPairVector', 'ScalarRightHilbertCore']
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

parent_path = ROOT / 'paired_right_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
assert parent['paired_right_algebra_generates_commutant'] and not parent['KMS_proved']
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
assert len(targets) == 25
report = ROOT / 'RELATORIO_VETORES_DIREITOS_DENSOS_DEV.md'
create(report, f'''# Vetores direitos densos e involução original — DEV

{DATE}. [REAL — três módulos/25 alvos compilados; revisão e integração pendentes]

No mesmo H_I e ideal completo n_ν, CΛν(a)=ρ(a)Ωg foi estendido
ao mapa gaussiano original. Para B∈ρ(N)', C*BC tem par direito real
(C*BΩg,C*B*Ωg). C não foi invertido e o J original não foi trocado.

[REAL] O vetor de um par é único para cada operador; o operador é único
para cada vetor. A escolha de representante produz uma aplicação linear
injetiva j da álgebra de operadores pareados em H_I, independente da escolha.
A imagem de j é densa em NORMA de H_I, usando C injetivo e a órbita
densa do comutante auxiliar. Vale j(ab)=a j(b) e F j(a)=j(a*), no F original.

[REAL] Foram provados o bound ||j(ab)||≤||a||_op ||j(b)|| e a identidade
de produto interno <j(ab),j(c)>=<j(b),j(a*c)>. K_h(I)=R_h*R_h fornece
aproximação forte da identidade por operadores pareados. Os próprios
produtos j(ab) são densos em H_I. O fecho do grafo da involução em j(A)
está contido no grafo fechado do F original e não tem parte vertical não nula.

[OPEN] Falta a IGUALDADE desse fecho com o grafo de F; densidade Hilbert
e densidade de produtos não são densidade na norma de grafo. Não se afirmou
plenitude de álgebra de Hilbert, reconstrução R=Jπ(b)J, inclusão inversa
π(N)'⊆Jπ(N)J ou fechamento von Neumann da imagem π(N).
Δ^it/KMS, traço/escala/canto Three Locks, H1/H2/H3 físicos, setor interagente
e consumo por certificados tipados/runtime continuam abertos.
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
    'full_weight_gaussian_right_pairs_constructed': True,
    'right_vector_injective_dense_embedding_constructed': True,
    'right_vector_products_dense_and_involution_closable': True,
    'original_weight_J_not_replaced': True,
    'KMS_proved': False, 'modular_square_flow_identified': False,
    'independent_review_complete': False, 'integrated': False,
    'memory_update_pending_review_in_this_turn': True,
    'gate_changed': False, 'full_goal_complete': False}
create(ROOT / 'right_vector_draft_status.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'integrated': False}))
