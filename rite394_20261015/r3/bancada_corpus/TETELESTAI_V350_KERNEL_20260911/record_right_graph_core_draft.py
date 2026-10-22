"""Freeze the right-algebra graph core of the original maximal adjoint F."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NAMES = ['ComplexGraphProjection', 'ScalarRightMultiplicationGraph', 'HilbertProjectionBlocks', 'ScalarRightProjectionPair', 'FixedVectorGraphCore', 'ScalarRightGraphCore']
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

parent_path = ROOT / 'scalar_vna_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
assert parent['actual_scalar_GNS_image_von_neumann'] and not parent['KMS_proved']
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
assert len(targets) == 57
report = ROOT / 'RELATORIO_GRAPH_CORE_ADJUNTO_ORIGINAL_F_DEV.md'
create(report, f'''# Graph core do adjunto original F — DEV

{DATE}. [REAL — seis módulos/57 alvos compilados; revisão e integração pendentes]

[REAL] O fecho do grafo da involução em j(A_right) é agora igual
ao grafo do adjunto maximal F ORIGINAL, no H_I original e no ideal completo
do peso escalar. scalarRightPairGraph_closure_eq_original prova a igualdade;
o adjunto não foi redefinido a partir desse fecho.

Para η em Fix(F), o grafo complexo auxiliar fecha os pares (Λa,π(a)η).
A identidade de pareamento S/F torna-o simétrico, e sua projeção comuta
com a ação diagonal de π(N). Seus blocos A,B,D fornecem um par direito
limitado efetivo B com vetores Aη e η−Dη. O elemento auto-adjunto B+B*
tem inscrição vη=Aη+η−Dη e satisfaz
Re<η,vη>=||P(η,0)||²+||Pperp(0,η)||²>0 para η diferente de zero.
A estrita positividade usa a densidade de Λ, sem supor limitada
a multiplicação direita a↦π(a)η.

Essa detecção positiva prova a densidade REAL das inscrições auto-adjuntas
em Fix(F). A decomposição do domínio da involução original em h+ik,
F(h+ik)=h−ik, e a continuidade dessa mistura dão a densidade no grafo.
O grafo complexo auxiliar não foi confundido com o grafo real de F.
Todas as hipóteses do lema genérico foram descarregadas nos objetos
concretos: fecho, domínio invariante, involutividade, pareamento e detecção.
S, F e J originais não foram substituídos; não há graph-core recebido
como campo de uma estrutura nem sorryAx na rodada aceita.

[OPEN] Permanecem a reconstrução R=Jπ(b)J e a inclusão inversa
π(N)'⊆Jπ(N)J para o J original. A igualdade de grafos entrega uma
obrigação necessária, não essa conclusão inteira automaticamente.
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
    'original_F_fixed_vectors_detected': True,
    'right_selfadjoint_vectors_dense_in_original_F_fixed_space': True,
    'right_pair_graph_core_equals_original_F': True,
    'original_weight_J_not_replaced': True,
    'KMS_proved': False, 'modular_square_flow_identified': False,
    'independent_review_complete': False, 'integrated': False,
    'memory_update_pending_review_in_this_turn': True,
    'gate_changed': False, 'full_goal_complete': False}
create(ROOT / 'right_graph_core_draft_status.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'integrated': False}))
