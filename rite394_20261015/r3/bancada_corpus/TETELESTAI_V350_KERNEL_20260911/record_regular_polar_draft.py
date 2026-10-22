"""Freeze the two full-domain right-scaling modules before independent review."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NAMES = ['ScalarRegularRightPolar', 'ScalarRegularPolarCommutation', 'ScalarRegularRightContinuity']
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

parent_path = ROOT / 'regular_right_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
assert parent['regular_right_commutes_on_full_square_domain'] and not parent['KMS_proved']
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
assert len(targets) == 16
report = ROOT / 'RELATORIO_CONJUGACAO_POLAR_REGULAR_DEV.md'
create(report, f'''# Conjugação polar regular — DEV

{DATE}. [REAL — três módulos/16 alvos compilados; revisão e integração pendentes]

No mesmo H_I do peso escalar, A=S†S, T=(I+A)⁻¹, B=√A e
J=scalarTomitaPolarFactor P são os objetos efetivamente construídos de S.

    T R_t=R_t T;  R_tD(B)=D(B);  B R_t x=R_t Bx;
    J R_t J⁻¹=π(λ_t*);          J π(λ_t) J⁻¹=R_(-t).

O resolvente é a inversa real de I+A. A prova da raiz reutiliza o transporte
genérico de gráficos já integrado; a identidade polar usa a mesma B com
imagem densa e S=JB no domínio completo. Não se escolhe outro J para a fórmula.
[R_t,π(a)]=0 para TODO a∈N, por associatividade em n_ν e densidade.
Logo o J-conjugado de cada λ_t comuta com todo π(N). O resultado cobre a
família regular: ainda não é a igualdade Jπ(N)J=π(N)' para N inteiro.

π(λ_t) e R_t são fortemente contínuos no mesmo GNS. O limite uniforme
1 descarrega o transporte da representação; a identidade polar fornece
continuidade de R_t. A pendência de continuidade do estágio anterior está
resolvida. Não se afirma continuidade na norma de operadores.

[OPEN] Tratar os geradores da álgebra-base no mesmo J e completar a identificação
de A^it/fluxo/KMS global. Próximo insumo: transportar a relação matricial
A R_y=(w_i/w_j)R_yA, já provada em todo D(A), à raiz e ao fator polar.
Também restam traço/escala/canto Three Locks, H1/H2/H3 físicos compatíveis,
setor quântico interagente e composição/consumo pelos certificados/runtime.
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
    'same_actual_root_domain_regular_invariant': True,
    'actual_polar_conjugates_regular_generator': True,
    'regular_right_strongly_continuous': True,
    'regular_right_commutes_with_every_left_element': True,
    'KMS_proved': False, 'modular_square_flow_identified': False,
    'independent_review_complete': False, 'integrated': False,
    'memory_update_pending_review_in_this_turn': True,
    'gate_changed': False, 'full_goal_complete': False}
create(ROOT / 'regular_polar_draft_status.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'integrated': False}))
