"""Freeze the two full-domain right-scaling modules before independent review."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NAMES = ['HomogeneousRightSquareDomain', 'MatrixUnitRightSquare']
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

parent_path = ROOT / 'scalar_right_tomita_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
assert parent['both_intertwinings_on_full_domains'] and not parent['KMS_proved']
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
assert len(targets) == 13
report = ROOT / 'RELATORIO_ESCALA_DIREITA_SQUARED_DEV.md'
create(report, f'''# Ação direita no domínio de S†S — DEV

{DATE}. [REAL — dois módulos/13 alvos compilados; revisão e integração pendentes]

No mesmo H_I, A=scalarTomitaSquare P é literalmente S†S no domínio composto.
Para toda unidade matricial local y=e_ij, todo x∈D(A) e r=w_i/w_j>0:

    R_y x ∈ D(A),        A R_y x = r R_y A x.

A prova usa os dois entrelaçamentos no domínio completo do estágio anterior.
Dados homogêneos d,e com elemento esquerdo de e igual à estrela do de d
fornecem A R_d x=R_e* A x. As instâncias e_ij/e_ji satisfazem essa condição.
O adjunto torcido de e_ji é ρ e_ij ρ⁻¹=r e_ij, enquanto a frequência
−log(w_j/w_i)=log(w_i/w_j). A igualdade de operadores direitos no GNS usa
esses dois dados; não se identifica operadores só pelo nome ou pelo vácuo.

A preservação é inclusão de domínio, não bijetividade de R_y. O domínio é
todo D(A), não apenas o núcleo algébrico. A mesma composição anterior foi
mantida, sem construir outro operador modular para obter o resultado.

[OPEN] Isto não identifica A^it com o fluxo candidato e não prova KMS global.
Faltam a passagem da relação local ao fluxo completo, traço/escala/canto
Three Locks, H1/H2/H3 físicos compatíveis, setor quântico interagente e consumo
integral pelo certificado/runtime. Todas as seis flags permanecem falsas.

Integração anterior: {parent['integrated_records']} registros,
{parent['controls']} controles, {parent['audit_declarations']} declarações Audit.
Esta etapa ainda não altera o um.py nem suas 34 memórias; a atualização fica
pendente para após revisão nesta sessão. Cópia `{sha(ROOT / 'um.py')}`;
mãe `{sha(parent_path)}`. Nenhum monólito foi executado/importado.
'''.encode('utf-8'))
manifest = {'timestamp': DATE, 'status': 'DEV_COMPILED__REVIEW_AND_INTEGRATION_PENDING',
    'modules': modules, 'targets': targets, 'report_path': str(report), 'report_sha256': sha(report),
    'parent_custody_path': str(parent_path), 'parent_custody_sha256': sha(parent_path),
    'integrated_working_sha256': sha(ROOT / 'um.py'),
    'same_actual_square_domain_right_invariant': True,
    'matrix_unit_right_scaling_on_full_square_domain': True,
    'KMS_proved': False, 'modular_square_flow_identified': False,
    'independent_review_complete': False, 'integrated': False,
    'memory_update_pending_review_in_this_turn': True,
    'gate_changed': False, 'full_goal_complete': False}
create(ROOT / 'right_square_draft_status.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'integrated': False}))
