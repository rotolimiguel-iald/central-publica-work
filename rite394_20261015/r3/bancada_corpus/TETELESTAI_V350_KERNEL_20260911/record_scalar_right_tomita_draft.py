"""Freeze the closed-Tomita right-domain bridge and append its honest DEV status."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
CENTRAL = ROOT.parent.parent
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
NAMES = ['ScalarRightStarGraph', 'ScalarRightClosedTomita']
MARKER = 'TETELESTAI_V350_RIGHT_CLOSED_TOMITA_DEV_20260912'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def create(path, raw):
    assert raw and not path.exists() and path.resolve().is_relative_to(ROOT)
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw
    temp.replace(path)
    assert path.read_bytes() == raw

parent_path = ROOT / 'homogeneous_right_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
assert parent['right_adjoint_pairing_on_same_full_GNS'] and not parent['KMS_proved']
for name, pin in parent['artifacts'].items():
    assert sha(ROOT / name) == pin, name
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
    stdout = Path(row['stdout'])
    output = stdout.read_text(encoding='utf-8')
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
        'stdout_sha256': sha(stdout),
        'failed_attempts': [str(p) for p, v in history if v['returncode']]}
assert len(targets) == 12
report = ROOT / 'RELATORIO_DIREITA_TOMITA_FECHADO_DEV.md'
create(report, f'''# A direita preserva o domínio do mesmo Tomita fechado — DEV

{DATE}. [REAL — dois módulos/12 alvos compilados; revisão independente e integração pendentes]

No mesmo GNS completo H_I e para os dados homogêneos já construídos:

    R_y D(S) ⊆ D(S),       S R_y x = π(y*) S x   para todo x∈D(S).

S é literalmente scalarClosedTomita P, a extensão fechada cujo gráfico foi
identificado com o fecho da estrela de n_ν∩n_ν*. R_y é a ação direita limitada
do pacote anterior. O lado direito usa multiplicação à esquerda por y*, e
não por modTwist(y). A torção pertence à identidade de adjunto R_y*; são
relações diferentes com domínios explícitos.

A prova constrói Ay no núcleo involutivo completo: Ay∈n_ν pela direita
homogênea, e (Ay)*=y*A*∈n_ν por ideal à esquerda. As duas inscrições são
respectivamente R_yΛ(A) e π(y*)Λ(A*). O mapa contínuo do par de coordenadas
preserva o gráfico algébrico e, por continuidade, seu fecho. A unicidade do
valor no gráfico fechado dá a igualdade para TODO D(S), não só para o núcleo.
Não se pressupõe continuidade de S nem uma igualdade D(S)=Λ(n_ν∩n_ν*).

As instâncias matrixUnitRightData fornecem o resultado para cada unidade
matricial local, no mesmo modelo da etapa integrada. O contrato genérico
recebe as pertinências e a homogeneidade já demonstradas, sem hipótese KMS.

[OPEN] Ainda faltam identificação de S†S com o fluxo candidato e KMS global,
traço/escala dual/canto Three Locks, H1/H2/H3 físicos compatíveis, setor
quântico interagente e consumo pelo certificado/runtime. A invariância do
domínio de S e a igualdade acima são novos insumos para essa identificação;
não são a identificação completa e não promovem nenhuma das seis flags.

Dois módulos/12 alvos, apenas propext, Classical.choice, Quot.sound nos logs
rc0 aceitos. Mãe integrada `{sha(parent_path)}`; cópia `{sha(ROOT / 'um.py')}`.
Esta etapa DEV ainda não integra o um.py; a integração anterior permanece
com {parent['integrated_records']} registros, {parent['controls']} controles
e {parent['audit_declarations']} declarações Audit. Originais preservados;
sem runtime integral. Revisão independente dos 12 alvos ainda pendente.
'''.encode('utf-8'))
manifest_path = ROOT / 'scalar_right_tomita_draft_status.json'
record = {'timestamp': DATE, 'status': 'DEV_COMPILED__REVIEW_AND_INTEGRATION_PENDING',
    'modules': modules, 'targets': targets, 'report_sha256': sha(report),
    'parent_custody_path': str(parent_path), 'parent_custody_sha256': sha(parent_path),
    'integrated_working_sha256': sha(ROOT / 'um.py'),
    'same_closed_Tomita_domain_right_invariant': True,
    'closed_Tomita_right_intertwining_on_full_domain': True,
    'KMS_proved': False, 'modular_square_flow_identified': False,
    'integrated': False, 'independent_review_complete': False,
    'gate_changed': False, 'full_goal_complete': False}
create(manifest_path, json.dumps(record, ensure_ascii=False, indent=2).encode('utf-8'))
surfaces = [Path(p) for p in parent['surface_sha256']]
before = {str(p): p.read_bytes() for p in surfaces}
assert len(surfaces) == 34
for p in surfaces:
    assert p.resolve().is_relative_to(ROOT) or p.resolve() in (
        CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md')
    assert sha(p) == parent['surface_sha256'][str(p)]
    assert MARKER.encode() not in before[str(p)]
note = f'''

## {MARKER} — {DATE}

[REAL — DEV compilado; revisão independente e integração pendentes] A direita
homogênea preserva o domínio do mesmo S fechado e S R_y x=π(y*)Sx para todo
x∈D(S). A prova transporta as duas coordenadas do gráfico de n_ν∩n_ν* e usa
continuidade do mapa de pares para passar ao fecho; não supõe S contínuo.
As instâncias matriciais são as do mesmo modelo/GNS já integrado.

Dois módulos/12 alvos, apenas trio lógico permitido. Este DEV não está no
um.py. Integração anterior: {parent['integrated_records']} registros,
{parent['controls']} controles, {parent['audit_declarations']} declarações Audit.
Seis flags maiores falsas; original preservado; nenhum runtime integral novo.

[OPEN] Identificação de S†S/fluxo e KMS global, traço/escala/canto Three Locks,
H1/H2/H3 físicos compatíveis, interação quântica e consumo pelo gate. A nova
relação é um insumo, não a quitação dessas obrigações. Objetivo integral ativo.

[Prova e limites](<{report.as_posix()}>).
[Manifesto DEV](<{manifest_path.as_posix()}>).
'''
backups = {}
for path in surfaces:
    raw = before[str(path)]
    assert path.read_bytes() == raw
    backup = path.with_name(path.name + '.bak_' + STAMP)
    with backup.open('xb') as stream:
        stream.write(raw)
    assert backup.read_bytes() == raw
    backups[str(path)] = str(backup)
    newline = '\r\n' if b'\r\n' in raw else '\n'
    after = raw + note.replace('\n', newline).encode('utf-8')
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    with temp.open('xb') as stream:
        stream.write(after)
    assert temp.read_bytes() == after and after.startswith(raw) and len(after) > len(raw)
    assert path.read_bytes() == raw
    temp.replace(path)
    assert path.read_bytes() == after
state = {'timestamp': DATE, 'previous_custody_path': str(parent_path),
    'previous_custody_sha256': sha(parent_path), 'draft_sha256': sha(manifest_path),
    'report_sha256': sha(report), 'working_sha256': sha(ROOT / 'um.py'),
    'surface_sha256': {str(p): sha(p) for p in surfaces}, 'backups': backups,
    'surface_before_sha256': {str(p): sha(Path(backups[str(p)])) for p in surfaces},
    'remaining_flags': parent['remaining_flags'], 'independent_review_complete': False,
    'integrated': False, 'gate_changed': False, 'full_goal_complete': False}
assert state['surface_before_sha256'] == parent['surface_sha256']
for p in surfaces:
    assert p.read_bytes().startswith(Path(backups[str(p)]).read_bytes())
    assert sha(p) == state['surface_sha256'][str(p)]
create(ROOT / 'scalar_right_tomita_draft_memory.json',
       json.dumps(state, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets),
    'surfaces': len(surfaces), 'independent_review_complete': False, 'integrated': False}))
