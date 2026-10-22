"""Freeze four modules extending polar commutation to the entire base algebra."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NAMES = ['LevelExpectationUniformBound', 'LevelExpectationStrongLimit', 'LocalBasePolarCommutation', 'BasePolarStrongLimit']
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

parent_path = ROOT / 'matrix_polar_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
assert parent['actual_polar_conjugates_base_matrix_units'] and not parent['KMS_proved']
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
assert len(targets) == 19
report = ROOT / 'RELATORIO_CONJUGACAO_POLAR_BASE_DEV.md'
create(report, f'''# Conjugação polar da álgebra-base — DEV

{DATE}. [REAL — quatro módulos/19 alvos compilados; revisão e integração pendentes]

M=theFactorObject P, N=regularCoreAlgebra P, π=scalarGNSRepresentation P,
ι=regularCoreEmbedding P, Δ=S†S e J=scalarTomitaPolarFactor P permanecem os mesmos.
As esperanças E_n dos níveis finitos satisfazem, para TODO x∈M:

    ||E_n(x)|| ≤ 4 ||x||, uniformemente em n;
    E_n(x) → x fortemente;
    π(ι(E_n(x))) → π(ι(x)) fortemente no mesmo H_I.

A ordem positiva herdada de M é construída usando a raiz quadrada dentro
da álgebra fechada em norma. A positividade e a unidade da família dos níveis
produzem a cota explícita por quatro partes positivas. A constante 4 é
suficiente para o limite; não se afirma que seja a norma ótima.
LevelExpectationFamily não é o contrato centralizante ExpectationInput.

A indução matricial trata todos os coeficientes complexos com conjugação:
J(cX)J⁻¹=conj(c) JXJ⁻¹. A comutação passa ao limite forte contra cada
operador limitado fixo. Conclusão no MESMO H_I e com o MESMO J:

    [J π(ι(x)) J⁻¹, π(y)] = 0, para TODO x∈M e TODO y∈N.

[REAL] A pendência de passar das unidades matriciais/níveis finitos à
álgebra-base inteira foi resolvida. A família regular λ_t já estava coberta.
[OPEN] Isso ainda não é Jπ(N)J=π(N)'. Falta passar desses geradores ao
core inteiro na representação e obter a inclusão inversa/global.
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
    'finite_level_expectations_uniformly_bounded': True,
    'actual_polar_conjugates_entire_base_into_commutant': True,
    'finite_level_expectations_strongly_approximate_base': True,
    'base_polar_commutes_with_every_core_left_element': True,
    'KMS_proved': False, 'modular_square_flow_identified': False,
    'independent_review_complete': False, 'integrated': False,
    'memory_update_pending_review_in_this_turn': True,
    'gate_changed': False, 'full_goal_complete': False}
create(ROOT / 'base_polar_draft_status.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'integrated': False}))
