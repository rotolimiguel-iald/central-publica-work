"""Freeze five modules extending polar commutation to the entire core."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NAMES = ['FiniteSetFibreRead', 'FibreSlices', 'ReducingCommutantTransport', 'ScalarGNSGeneratorTransport', 'CorePolarInclusion']
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

parent_path = ROOT / 'base_polar_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
assert parent['actual_polar_conjugates_entire_base_into_commutant'] and not parent['KMS_proved']
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
assert len(targets) == 28
report = ROOT / 'RELATORIO_INCLUSAO_POLAR_CORE_DEV.md'
create(report, f'''# Inclusão polar do core inteiro — DEV

{DATE}. [REAL — cinco módulos/28 alvos compilados; revisão e integração pendentes]

No mesmo espaço H_I=ScalarGNSHilbert P do peso escalar,
N=regularCoreAlgebra P, π=scalarGNSRepresentation P, Δ=S†S e
J=scalarTomitaPolarFactor P permanecem os objetos já construídos.

Os operadores de inserção E_S(v)=1_S v, com S mensurável de medida finita, satisfazem
E_S†f=integral_S f. Todas essas leituras juntas determinam f em L².
Seus coeficientes E_S† T E_U determinam cada operador limitado T.
Isso transporta a comutação dos geradores para sua álgebra gerada por
bicomutante na amplificação fibre. A conjugação dualOrbit e a extensão
por zero no complemento ortogonal transportam a geração ao GNS atual.
O lema genérico de restrição exige geração ambiente; essa premissa é
demonstrada na aplicação efetiva scalarGNS_commutation_from_generators.

Combinando a base inteira e os unitários regulares, já cobertos, a
involução do MESMO J e a geração agora demonstrada fornecem:

    [J π(x) J⁻¹, π(y)] = 0, para TODO x∈N e TODO y∈N;
    J π(N) J ⊆ π(N)'.

[REAL] A passagem dos geradores ao core inteiro foi resolvida para a
inclusão acima. Não há troca pelo J da torre, nem hipótese de densidade
ou normalidade restante no enunciado concreto. Não se usa avaliação
pontual de representantes L² ou função constante não integrável na reta.
[OPEN] A inclusão inversa π(N)'⊆Jπ(N)J ainda não foi provada. J²=I
e a inclusão direta não a fornecem automaticamente.
Também permanecem identificação de Δ^it com o fluxo/KMS do mesmo peso,
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
    'finite_set_reads_total': True,
    'actual_polar_conjugates_core_into_commutant': True,
    'scalar_GNS_generator_transport_proved': True,
    'core_polar_commutes_with_every_core_left_element': True,
    'KMS_proved': False, 'modular_square_flow_identified': False,
    'independent_review_complete': False, 'integrated': False,
    'memory_update_pending_review_in_this_turn': True,
    'gate_changed': False, 'full_goal_complete': False}
create(ROOT / 'core_polar_draft_status.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'integrated': False}))
