"""Freeze paired multiplication graphs, projection blocks and weighted original-S tests."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NAMES = ['ScalarPairedMultiplicationGraph', 'HilbertProjectionOrder', 'ScalarPairedProjectionBlocks', 'ScalarWeightedProjectionTest']
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

parent_path = ROOT / 'square_resolvent_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
assert parent['original_S_characterized_by_selfadjoint_square_tests'] and not parent['KMS_proved']
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
report = ROOT / 'RELATORIO_BLOCOS_PARES_TESTE_PONDERADO_DEV.md'
create(report, f'''# Blocos da álgebra de pares e teste ponderado original — DEV

{DATE}. [REAL — quatro módulos/27 alvos compilados; revisão e integração pendentes]

[REAL] No mesmo espaço GNS e com a mesma álgebra não unital E dos pares
direitos, G_η=fecho{{(j(a),aη):a∈E}}. Para η∈D(S), Sη=η, o pareamento é
simétrico e Π(aη,−j(a))=0. A invariância diagonal vale para η arbitrário.

[REAL] Para Π=[A B;B* D], 0≤A≤I, A é injetivo,
BB*=A(I−A) e BD=(I−A)B. E'=M é demonstrado com a imagem GNS efetiva;
logo A,B,D pertencem a essa mesma M. Para η fixo por S:
B j(a)=A(aη), B(aη)=(I−A)j(a), B*(aη)=D j(a).
Não se presume [A,B]=0; A não é o operador modular Δ.

[REAL] Se e∈M, e*=e e [e,A]=0, o operador limitado K=e(I−A)B
realiza as duas ações exigidas pelo teste original-S. Assim
Yη=eBB*η pertence a D(S) e S(Yη)=Zη=B*eBη.
A escolha de K e suas ações são provadas; as hipóteses sobre e ficam explícitas.
Para η obtido pela solução variacional de fase, Re z>0 e ξ∈Fix F,
2〈ξ,Zη〉=z〈η,Zη〉+conj(z)〈Yη,η〉.

[OPEN] Ainda faltam a estimativa que usa e=(I−cA)+, a cota inferior uniforme
positiva de A e seu inverso limitado. Injetividade não fornece tal cota.
Seguem abertos a inclusão inversa pelo J original, Δ^it/KMS, traço/escala/canto
Three Locks, H1/H2/H3 físicos, setor interagente e consumo por certificados/runtime.

[REAL — fiação preservada] As seis flags maiores qgf/gpf não entram diretamente
em evaluate_quantum_gravity_closure: o selo legado lê qgc_, qgp_ e o feed
experimental; kernel_frontier é anexado depois. As novas provas não mudam
o selo legado nem essas seis flags. Objetivo integral ativo.

Integração anterior: {parent['integrated_records']} registros,
{parent['controls']} controles, {parent['audit_declarations']} declarações Audit.
Este DEV não altera um.py nem as 34 memórias; atualização pendente de revisão
nesta sessão. Cópia `{sha(ROOT / 'um.py')}`, mãe `{sha(parent_path)}`.
Tentativas Lean recusadas e seus logs foram preservados; somente
logs rc0 dos bytes atuais são aceitos. Nenhum monólito executado/importado.
'''.encode('utf-8'))
manifest = {'timestamp': DATE, 'status': 'DEV_COMPILED__REVIEW_AND_INTEGRATION_PENDING',
    'modules': modules, 'targets': targets, 'report_path': str(report), 'report_sha256': sha(report),
    'parent_custody_path': str(parent_path), 'parent_custody_sha256': sha(parent_path),
    'integrated_working_sha256': sha(ROOT / 'um.py'),
    'paired_graph_and_blocks_same_GNS': True,
    'weighted_projection_pair_in_original_S': True,
    'phase_variational_weighted_equation': True,
    'projection_block_uniform_lower_bound_proved': False,
    'original_weight_J_not_replaced': True,
    'KMS_proved': False, 'modular_square_flow_identified': False,
    'independent_review_complete': False, 'integrated': False,
    'memory_update_pending_review_in_this_turn': True,
    'gate_changed': False, 'full_goal_complete': False}
create(ROOT / 'paired_blocks_draft_status.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'integrated': False}))
