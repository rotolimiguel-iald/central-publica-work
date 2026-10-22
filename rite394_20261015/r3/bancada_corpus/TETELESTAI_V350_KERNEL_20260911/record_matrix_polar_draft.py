"""Freeze eight modules proving matrix-unit root and polar transport."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NAMES = ['PositiveRootIntertwining', 'ScaledPositiveResolvent', 'ScaledResolventRoots', 'ScaledRootGraphTransport', 'MatrixUnitResolventScaling', 'MatrixUnitRootScaling', 'MatrixUnitPolarTransport', 'MatrixUnitPolarCommutation']
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

parent_path = ROOT / 'regular_polar_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
assert parent['actual_polar_conjugates_regular_generator'] and not parent['KMS_proved']
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
assert len(targets) == 32
report = ROOT / 'RELATORIO_CONJUGACAO_POLAR_MATRICIAL_DEV.md'
create(report, f'''# Conjugação polar matricial — DEV

{DATE}. [REAL — oito módulos/32 alvos compilados; revisão e integração pendentes]

No mesmo H_I do peso escalar, A=S†S, T=(I+A)⁻¹, B=√A e
J=scalarTomitaPolarFactor P continuam os objetos efetivos já construídos.
Para r=w_i/w_j>0 e R_ij a ação direita da unidade matricial:

    B R_ij x=√r R_ij Bx, para TODO x∈D(B), com R_ij D(B)⊆D(B);
    J π(e_ij*) J⁻¹=√r R_ij;
    J π(e_ij) J⁻¹=√(w_j/w_i) R_ji.

A passagem usa D=rI+(1-r)T estritamente positivo, Q=T D⁻¹ positivo≤I,
T R_ij=R_ij Q e cálculo funcional sobre a união compacta dos espectros.
O gráfico parametrizado por √T e √(1-T) é transportado inteiro, usando
apenas a sobrejetividade da raiz de D⁻¹, que é limitada e inversível.
Não se supõe inversa limitada de B nem invertibilidade de R_ij.
Usando S=JB em D(B), prova-se √r·J R_ij=π(e_ij*)J em Ran(B); a densidade de Ran(B) e a continuidade dos dois membros estendem essa identidade a H_I. O fator polar J é o mesmo já construído.

Toda direita homogênea construída comuta com TODO π(a), a∈N, por
associatividade no domínio escalar completo n_ν e densidade. Portanto o
J-conjugado de cada unidade matricial local da base comuta com todo π(N).
Isso soma-se à família regular e sua continuidade forte já integradas.
A pendência de escala matricial até a raiz/J do estágio anterior está resolvida.

[OPEN] Estender dos geradores/níveis locais ao fecho da álgebra representada
e provar a igualdade global Jπ(N)J=π(N)', não só as inclusões nos geradores.
Ainda faltam identificação de A^it com o fluxo/KMS do mesmo peso,
traço/escala/canto Three Locks, H1/H2/H3 físicos compatíveis, setor quântico
interagente e composição/consumo pelos certificados/runtime.
Reutilizar Einstein/Fisher/gauge de Chatgpt com suas hipóteses. Seis flags falsas.

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
    'matrix_unit_same_root_scaling_proved': True,
    'actual_polar_conjugates_base_matrix_units': True,
    'matrix_unit_root_domain_preserved': True,
    'homogeneous_right_commutes_with_every_left_element': True,
    'KMS_proved': False, 'modular_square_flow_identified': False,
    'independent_review_complete': False, 'integrated': False,
    'memory_update_pending_review_in_this_turn': True,
    'gate_changed': False, 'full_goal_complete': False}
create(ROOT / 'matrix_polar_draft_status.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'integrated': False}))
