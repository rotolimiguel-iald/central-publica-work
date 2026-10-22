"""Freeze the Gaussian polar unitary and cyclic separating vector construction."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NAMES = ['DenseLinearPolarExtension', 'BoundedInjectivePolar', 'ScalarGaussianImage', 'ScalarGaussianUnitary']
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

parent_path = ROOT / 'core_polar_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
assert parent['actual_polar_conjugates_core_into_commutant'] and not parent['KMS_proved']
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
assert len(targets) == 34
report = ROOT / 'RELATORIO_POLAR_GAUSSIANO_CICLICO_DEV.md'
create(report, f'''# Polar gaussiano e vetor cíclico separante — DEV

{DATE}. [REAL — quatro módulos/34 alvos compilados; revisão e integração pendentes]

No mesmo H_I=ScalarGNSHilbert P, com a mesma representação π do core N,
C=scalarGaussianGNSMap P é o mapa injetivo já construído. Seu contradomínio
correto para a parte polar é K=closure(Ran C), não o ambiente L² inteiro.

[REAL] Provados K redutor e Ωg∈K por médias regulares de quadrado finito,
limitadas por 1, com h↓0. A densidade das inscrições e a invariância dão
K=closure(dualOrbit(N) Ωg). Não se usa C^{-1} limitado nem C(H_I)⊆H_I.

Para C_K:H_I→K, D=(C_K†C_K)^(1/2) tem imagem densa e
||Dx||=||C_Kx||. A regra V(Dx)=C_Kx estende uma UNITÁRIA LINEAR V.
O entrelaçamento para a e a* prova Vπ(a)=ρ_K(a)V. Logo
ξ=V^{-1}Ωg pertence ao H_I ORIGINAL e é cíclico separante para a MESMA π.
Não se afirma norma 1; ξ representa o funcional gaussiano, não o peso
semifinito original. Todas as densidades são demonstradas na aplicação.

[OPEN] V não é J. O Tomita/conjugação do novo vetor ξ não foi identificado
com S/J do peso. A inclusão de gráficos por C não autoriza cancelar D:
sua inversa pode ser não limitada e os domínios precisam ser controlados.
A inclusão direta Jπ(N)J⊆π(N)' da etapa anterior permanece provada.
Esta preparação cíclica NÃO prova a inclusão inversa com o J original.

Continuam abertos Δ^it/KMS do mesmo peso, traço/escala/canto Three Locks,
H1/H2/H3 físicos compatíveis, setor interagente e consumo por certificados
tipados/runtime. Reutilizar as provas anteriores de Chatgpt com suas hipóteses.
Seis flags maiores falsas; o gate não muda por esta preparação.

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
    'gaussian_polar_unitary_constructed': True,
    'gaussian_closed_image_identified': True,
    'same_scalar_GNS_cyclic_separating_vector_constructed': True,
    'original_weight_J_not_replaced': True,
    'KMS_proved': False, 'modular_square_flow_identified': False,
    'independent_review_complete': False, 'integrated': False,
    'memory_update_pending_review_in_this_turn': True,
    'gate_changed': False, 'full_goal_complete': False}
create(ROOT / 'gaussian_polar_draft_status.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'integrated': False}))
