"""Freeze actual bounded right regularization of the entire commutant."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NAMES = ['ScalarRightRegularization', 'ScalarCommutantRegularization']
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

parent_path = ROOT / 'gaussian_polar_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
assert parent['gaussian_polar_unitary_constructed'] and not parent['KMS_proved']
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
report = ROOT / 'RELATORIO_REGULARIZACAO_COMUTANTE_DEV.md'
create(report, f'''# Regularização de todo o comutante — DEV

{DATE}. [REAL — dois módulos/19 alvos compilados; revisão e integração pendentes]

No mesmo H_I e com o ideal completo n_ν do peso original, foi construído
R_h Λν(a)=Λν(a e_h), onde e_h é a média regular existente.
O bound de peso prova ||R_h||≤1 e a convergência GNS das inscrições,
estendida por equicontinuidade, prova R_h→I fortemente quando h→0, h≠0.
Para h>0, η_h=Λν(e_h) existe e R_hΛν(a)=π(a)η_h.

[REAL] Para qualquer T∈π(N)', T R_h é um multiplicador direito limitado,
com vetor Tη_h, ||T R_h||≤||T|| e T R_h→T fortemente. Esses multiplicadores
comutam com π(N). Todo T pertence à álgebra de von Neumann gerada por eles.
Não se restringe T aos geradores conhecidos nem se pressupõe sua reconstrução.

[OPEN] ScalarRightBounded significa um vetor η e um operador limitado R
com RΛν(a)=π(a)η. Não inclui vetor adjunto, fechamento por star, plenitude
de álgebra de Hilbert ou R=Jπ(b)J. Essas conclusões não foram promovidas.
A reconstrução polar dos multiplicadores e o fechamento da imagem π(N)
ainda precisam de prova; a inclusão inversa com J original permanece aberta.
O novo critério scalarCommutant_mem_of_rightBounded assume explicitamente
Q von Neumann e a inclusão dos multiplicadores em Q; a hipótese não é descartada.

Nenhum peso foi substituído pelo funcional gaussiano. Permanecem abertos
Δ^it/KMS do mesmo peso, traço/escala/canto Three Locks, H1/H2/H3 físicos,
setor interagente e consumo por certificados tipados/runtime.
Seis flags maiores falsas; o gate não muda por esta regularização.

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
    'full_weight_right_averages_constructed': True,
    'commutant_right_bounded_approximation_constructed': True,
    'right_bounded_reconstruction_still_open': True,
    'original_weight_J_not_replaced': True,
    'KMS_proved': False, 'modular_square_flow_identified': False,
    'independent_review_complete': False, 'integrated': False,
    'memory_update_pending_review_in_this_turn': True,
    'gate_changed': False, 'full_goal_complete': False}
create(ROOT / 'right_regularization_draft_status.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'integrated': False}))
