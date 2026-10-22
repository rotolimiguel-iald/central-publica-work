"""Freeze the real variational solver and its original-S graph identity."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NAMES = ['RealPhaseVariational', 'ScalarPhaseVariational']
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

parent_path = ROOT / 'adjoint_polar_graph_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
assert parent['right_conjugate_graph_core_equals_original_S'] and not parent['KMS_proved']
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
assert len(targets) == 21
report = ROOT / 'RELATORIO_SELECAO_VARIACIONAL_GRAFO_ORIGINAL_DEV.md'
create(report, f'''# Seleção variacional e grafo original — DEV

{DATE}. [REAL — dois módulos/21 alvos compilados; revisão e integração pendentes]

[REAL] Para qualquer subespaço real fechado K de um Hilbert complexo e
Re(lambda)>0, a forma B_lambda(u,v)=Re(lambda< u,v >) é limitada e coerciva.
Lax-Milgram constrói uma solução real-linear contínua, única, com
Re(lambda)||eta||<=||xi||. Não se supõe simetria da forma. Em lambda=1,
a solução é a projeção ortogonal real. A cota é do VETOR, não do multiplicador.

[REAL] A construção foi instanciada no Fix S ORIGINAL sobre o Hilbert escalar
original. eta pertence ao domínio original de S e S eta=eta. Para xi em
Fix F original, o pareamento adjunto S/F e a decomposição do domínio de S
estendem a equação real à identidade complexa em TODO o grafo original:
2<xi,S u> = lambda<eta,S u> + conjugate(lambda)<u,eta>.
Foram reutilizados o subespaço padrão e a decomposição da bancada Chatgpt;
não foi escolhido outro S, F, J ou espaço de representação.

[OPEN] A identidade do grafo exige u em D(S). Ainda falta provar essa condição
para os pares ponderados da projeção do gráfico de multiplicação da álgebra
direita. Depois é preciso obter a cota inferior uniforme do bloco A e construir
o multiplicador limitado. A proposta de parte positiva por CFC consta da
consulta RVD56, com estatuto DERIVED, ainda não compilada. Seleção variacional
não prova por si só a inclusão inversa JRJ em pi(N). Fluxo Delta^it/KMS,
traço/escala/canto Three Locks, H1/H2/H3 físicos, setor interagente e consumo
por certificados tipados/runtime continuam abertos. Seis flags maiores falsas.

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
    'real_phase_variational_solution_unique': True,
    'original_S_phase_variational_constructed': True,
    'original_S_graph_variational_identity': True,
    'original_weight_J_not_replaced': True,
    'KMS_proved': False, 'modular_square_flow_identified': False,
    'independent_review_complete': False, 'integrated': False,
    'memory_update_pending_review_in_this_turn': True,
    'gate_changed': False, 'full_goal_complete': False}
create(ROOT / 'phase_variational_draft_status.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'integrated': False}))
