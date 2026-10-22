"""Freeze the actual scalar GNS image as a von Neumann algebra."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NAMES = ['ReducingCommutantCompression', 'ReducingBicommutantLift', 'SeparatingRestrictionVonNeumann', 'ScalarGNSVonNeumann']
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

parent_path = ROOT / 'right_vector_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
assert parent['right_vector_products_dense_and_involution_closable'] and not parent['KMS_proved']
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
assert len(targets) == 27
report = ROOT / 'RELATORIO_IMAGEM_ESCALAR_VON_NEUMANN_DEV.md'
create(report, f'''# Imagem escalar de von Neumann — DEV

{DATE}. [REAL — quatro módulos/27 alvos compilados; revisão e integração pendentes]

[REAL] A imagem da representação escalar π(N), no H_I original,
é agora provada igual ao seu bicomutante. Não se trata apenas de definir
a álgebra gerada: mem_scalarGNSVonNeumann_iff fornece para TODO elemento
dela uma pré-imagem efetiva em N; scalarGNSVonNeumann_coe prova a igualdade
com Set.range scalarGNSRepresentation.

A prova usa um levantamento limitado. Para M VNA, K redutor e Ω∈K
separante para M, a órbita M'Ω é densa. Para B no bicomutante da imagem
restrita, a coluna C=D∘incl tem Gram C*C no comutante dessa imagem.
B comuta com a raiz positiva, e ||DBΩ||≤||B|| ||DΩ||.
T(DΩ)=DBΩ estende-se a um operador limitado, que comuta com M'
e por isso pertence a M. A órbita projetada P_K M'Ω é densa em K;
a restrição de T é B. O levantamento satisfaz ||T||≤||B||.

Na aplicação, M é dualOrbitVonNeumann(regularCoreAlgebra P), K é
scalarGaussianImage P e Ω é scalarGaussianVacuum P. Redução, separação
e pertença do vetor foram descarregadas nos objetos concretos. A unidade
LINEAR scalarGaussianUnitary transporta a igualdade à representação π em H_I.
Essa unidade não foi identificada com o J modular; S, F e J originais
não foram substituídos.

[OPEN] Continuam pendentes a igualdade do grafo da involução em j(A_right)
com graph F, reconstrução R=Jπ(b)J e inclusão inversa π(N)'⊆Jπ(N)J.
A consulta CONSULTA_GRAPH_CORE_ORIGINAL_F.md propõe uma rota por blocos
da projeção do grafo de multiplicação direita, ainda sem formalização Lean.
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
    'restricted_bicommutant_bounded_lift_constructed': True,
    'separating_restriction_bicommutant_closed': True,
    'actual_scalar_GNS_image_von_neumann': True,
    'original_weight_J_not_replaced': True,
    'KMS_proved': False, 'modular_square_flow_identified': False,
    'independent_review_complete': False, 'integrated': False,
    'memory_update_pending_review_in_this_turn': True,
    'gate_changed': False, 'full_goal_complete': False}
create(ROOT / 'scalar_vna_draft_status.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'integrated': False}))
