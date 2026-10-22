"""Freeze the real variational solver and its original-S graph identity."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NAMES = ['ScalarTomitaBidual', 'ScalarRightFunctionalStability']
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

parent_path = ROOT / 'phase_variational_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
assert parent['original_S_graph_variational_identity'] and not parent['KMS_proved']
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
assert len(targets) == 9
report = ROOT / 'RELATORIO_BIDUAL_SUPORTE_DIREITO_DEV.md'
create(report, f'''# Bidual original e suporte direito — DEV

{DATE}. [REAL — dois módulos/9 alvos compilados; revisão e integração pendentes]

[REAL] O adjunto maximal de F é exatamente o S ORIGINAL, incluindo todo
seu domínio. O pareamento contra D(F) é equivalente à pertinência ao grafo de
S. A prova usa a conjugação polar J já construída, F=JSJ e a maximalidade de
F; não redefine S/F/J nem pressupõe a inclusão inversa dos comutantes.

[REAL] Se a=a* é um par direito e T=T* pertence ao comutante inteiro,
comutando com a, então Ta é um par direito auto-adjunto com inscrição
j(Ta)=Tj(a). T não precisa previamente pertencer à álgebra dos pares direitos.
A construção exibe os dois vetores do par e as duas leis de multiplicação.
Para qualquer par direito R, sua inscrição pertence ao fecho normado de Ran R,
provado pelas médias regulares no ideal do peso original. Não se supõe uma
cota uniforme para os vetores GNS dessas médias.

[OPEN] Os lemas preparam cortes racionais e a aproximação por combinações de
quadrados, mas não provam ainda que esses quadrados sejam núcleo de grafo
para F. Tampouco colocam automaticamente o par ponderado no domínio de S.
Faltam essa aproximação, o teste ponderado, a cota inferior uniforme do bloco
A e o multiplicador limitado. Inclusão inversa pelo J original, Delta^it/KMS,
traço/escala/canto Three Locks, H1/H2/H3 físicos, setor interagente e consumo
por certificados/runtime continuam abertos. Seis flags maiores falsas.

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
    'original_S_is_maximal_adjoint_of_F': True,
    'selfadjoint_right_pairs_stable_under_commuting_multipliers': True,
    'right_pair_vectors_in_multiplier_range_closure': True,
    'original_weight_J_not_replaced': True,
    'KMS_proved': False, 'modular_square_flow_identified': False,
    'independent_review_complete': False, 'integrated': False,
    'memory_update_pending_review_in_this_turn': True,
    'gate_changed': False, 'full_goal_complete': False}
create(ROOT / 'bidual_right_support_draft_status.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'integrated': False}))
