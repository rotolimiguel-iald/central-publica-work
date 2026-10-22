"""Record the reviewed full-weight GNS integration with immediate byte backups."""
import ast
import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
CENTRAL = ROOT.parent.parent
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
MARKER = 'TETELESTAI_V350_FULL_WEIGHT_GNS_INTEGRATED_20260912'
BACKUPS = {}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, raw, before=None):
    assert path.resolve().is_relative_to(ROOT) or path.resolve() in (
        CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md')
    assert raw
    if before is None:
        assert not path.exists(), path
    else:
        assert path.read_bytes() == before
        backup = path.with_name(path.name + '.bak_' + STAMP)
        with backup.open('xb') as stream:
            stream.write(before)
        assert backup.read_bytes() == before
        BACKUPS[str(path)] = str(backup)
    temporary = path.with_name(path.name + '.tmp_' + STAMP)
    with temporary.open('xb') as stream:
        stream.write(raw)
    assert temporary.read_bytes() == raw
    if before is not None:
        assert path.read_bytes() == before and raw.startswith(before) and len(raw) > len(before)
    temporary.replace(path)
    assert path.read_bytes() == raw

def body(path):
    tree = ast.parse(path.read_bytes())
    assign = next(n for n in tree.body if isinstance(n, ast.Assign) and any(
        isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in n.targets))
    assign.value = ast.Constant('EXCLUDED_EMBEDDED_LEAN')
    return ast.dump(tree, include_attributes=False)

assert '--review-read' in sys.argv
parent_path = ROOT / 'tomita_involution_custody.json'
parent = json.loads(parent_path.read_bytes())
draft_path = ROOT / 'scalar_weight_gns_draft_status.json'
draft = json.loads(draft_path.read_bytes())
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
original = Path(json.loads((ROOT / 'environment.json').read_bytes())['original_source'])
reviews = [ROOT / 'revisao/REVIEW_SCALAR_WEIGHT_GNS.md',
           ROOT / 'revisao/REVIEW_SCALAR_WEIGHT_GNS_INTEGRATED.md']
assert 'SCALAR_WEIGHT_GNS_DEV_REVIEW' in reviews[0].read_text(encoding='utf-8')
assert 'INTEGRATED_SCALAR_WEIGHT_GNS_REVIEW' in reviews[1].read_text(encoding='utf-8')
assert sha(original) == sha(ROOT / 'fontes/um_v350_original.py') == integration['base_sha256']
assert sha(ROOT / 'um.py') == integration['working_sha256'] == tests['working_um_sha256']
assert draft['integrated_working_sha256'] == parent['working_sha256']
assert draft['parent_custody_sha256'] == sha(parent_path)
prior = next(p for p in ROOT.glob('um.py.bak_*') if sha(p) == parent['working_sha256'])
assert body(prior) == body(ROOT / 'um.py')
assert build['incremental_build_ok'] and all(r['returncode'] == 0 for r in build['records'])
assert tests['passed'] == len(tests['checks']) and all(c['passed'] for c in tests['checks'])
assert not tests['full_monolithic_runtime_run'] and not tests['frontier']['legacy_gate_changed']
for row in build['records']:
    source = Path(row['source']).resolve()
    assert source.is_relative_to(ROOT / 'kernel')
    binary = ROOT / 'build' / source.relative_to(ROOT / 'kernel').with_suffix('.olean')
    assert row['output_exists'] and sha(source) == row['sha256']
    assert sha(binary) == row['output_sha256']
targets, modules = {}, {}
for name, row in draft['modules'].items():
    source = ROOT / 'kernel/TGLV350' / (name + '.lean')
    final = ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean')
    raw = source.read_text(encoding='utf-8')
    assert sha(source) == row['source_sha256']
    assert sha(ROOT / 'build/TGLV350' / (name + '.olean')) == row['binary_sha256']
    assert re.sub(r'^import TGLV350\.', 'import TGLExt.V350', raw, flags=re.M) == final.read_text(encoding='utf-8')
    for short in re.findall(r'^#print axioms ([\w.]+)$', raw, re.M):
        full = 'TGLV350.Regular.' + short
        axioms = evidence['axiom_report'][full]
        assert set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'}
        assert sorted(axioms) == draft['targets'][full]
        targets[full] = axioms
    modules[name] = {'development_sha256': sha(source), 'integrated_sha256': sha(final),
        'development_binary_sha256': sha(ROOT / 'build/TGLV350' / (name + '.olean'))}
assert len(modules) == 9 and len(targets) == 60
assert all(evidence[k] is False for k in parent['remaining_flags'])
surfaces = [Path(p) for p in parent['surface_sha256']]
before_surfaces = {str(p): p.read_bytes() for p in surfaces}
for path in surfaces:
    assert MARKER.encode() not in before_surfaces[str(path)]
    assert sha(path) == parent['surface_sha256'][str(path)]
report_path = ROOT / 'RELATORIO_GNS_PESO_COMPLETO_INTEGRADO.md'
report = f'''# GNS completo e gráfico de Tomita do mesmo peso — integração revisada

{DATE}. [REAL — nove módulos/60 alvos integrados e revisados]

O completamento de Λ_ν(n_ν) é exatamente o H_I anterior. A inscrição preserva
o peso ν(A* A), é injetiva e entrelaça a representação existente. A aproximação
A X_h converge em norma GNS por convergência dominada; os sandwiches X_h* A X_h
e seus adjuntos dão a aproximação simultânea das duas coordenadas do gráfico.
Assim, o gráfico do S fechado anterior é exatamente o fecho da involução no
núcleo completo n_ν ∩ n_ν*. A mesma construção polar S=UB e U²=I permanece.

Não se afirmou igualdade dos ideais I=n_ν, nem D(S)=Λ_ν(n_ν ∩ n_ν*) sem
fechamento. O que foi identificado é o completamento e o fecho de gráfico.
Não há hipótese KMS inserida na prova. Foram reutilizados os operadores e
lemas de aproximação do mesmo modelo; nenhuma mudança de espaço foi postulada.

{len(build['records'])} registros incrementais rc0, {tests['passed']} controles,
{tests['axiom_report_entries']} declarações Audit e {integration['embedded_files']}
arquivos Lean embutidos. Revisão DEV com recompilação própria; revisão da
integração e custódia. Dependências anteriores reutilizadas com pins, sem
rebuild global nem runtime integral. O corpo Python fora do embutido é idêntico
ao estágio anterior. Os controles preservam as seis flags maiores falsas.

[OPEN] Identificar o fluxo modular de ν e provar KMS; construir o traço
canônico e sua escala dual, realizar o canto Three Locks; entregar H1/H2/H3
físicos compatíveis no mesmo modelo; completar o setor quântico interagente
e o consumo efetivo pelo certificado e runtime integrais. Essas obrigações
podem mover o gate quando satisfeitas com suas hipóteses e tipos completos.
O gráfico identificado não fornece essas conclusões sozinho.

O reexame da pasta Chatgpt já localizou a ponte de Einstein, a métrica de Fisher
e a invariância de gauge linearizada geral. Reutilizá-las com as hipóteses
exatas, sem apresentar implicações condicionais como testemunhas físicas novas.
Nesta etapa foram relidos também tower_kms (TGLExt/TowerModular.lean) e
tState_kms (TGLExt/RightMult.lean): seus enunciados são identidades dos estados
matriciais em cada andar N. O transporte para a condição KMS do peso no core
contínuo ainda exige prova; o nome KMS não efetua essa passagem.

[Provas e alcance DEV](<{(ROOT / 'RELATORIO_GNS_PESO_COMPLETO_DEV.md').as_posix()}>).
[Revisão DEV](<{reviews[0].as_posix()}>).
[Revisão integrada](<{reviews[1].as_posix()}>).
[Reaproveitamento do acervo](<{(ROOT / 'REEXAME_CHATGPT_20260912/RELATORIO_REAPROVEITAMENTO.md').as_posix()}>).

Original relido `{sha(original)}`; cópia `{sha(ROOT / 'um.py')}`.
Mãe matemática e de memória `{sha(parent_path)}`. Original preservado e nunca
executado/importado; gate legado inalterado, objetivo integral ativo.
Registros anteriores de identificação do domínio completo em aberto são
históricos; KMS, traço e as obrigações físicas continuam abertos.
'''
write(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — integração revisada] O completamento de Λ_ν(n_ν) foi identificado com
o H_I anterior, e o fecho da involução do núcleo completo n_ν ∩ n_ν* é o
gráfico do mesmo S fechado. A aproximação é em norma GNS nas duas coordenadas,
com sandwiches do ideal anterior. Não se presume I=n_ν nem que o gráfico
algébrico já seja fechado. Nove módulos/60 alvos, somente o trio lógico permitido.

{len(build['records'])} registros incrementais rc0; {tests['passed']} controles;
{tests['axiom_report_entries']} declarações Audit; {integration['embedded_files']}
embutidos. Revisões DEV e integrada lidas. Dependências reutilizadas com pins;
sem runtime integral. Cópia {sha(ROOT / 'um.py')}; original preservado.

[OPEN] Identificação do fluxo modular/KMS, traço/canto Three Locks, H1/H2/H3
físicos no mesmo modelo, setor quântico interagente e consumo integral no gate.
Seis flags maiores falsas; gate legado inalterado e objetivo integral ativo.
Einstein, Fisher e gauge já localizados em Chatgpt são reutilizáveis com suas
hipóteses, conforme o reexame. O histórico anterior permanece ao lado.
As identidades tower_kms e tState_kms relidas são por andar matricial N;
não fornecem automaticamente a condição KMS do peso no core contínuo.

[Relatório atual](<{report_path.as_posix()}>).
[Revisão integrada](<{reviews[1].as_posix()}>).
'''
for path in surfaces:
    raw = before_surfaces[str(path)]
    newline = '\r\n' if b'\r\n' in raw else '\n'
    write(path, raw + note.replace('\n', newline).encode('utf-8'), raw)
artifact_names = ['integration.json', 'integrated_compile.json', 'kernel_incremental_evidence.json',
    'gate_tests.json', 'gate_extension.py', 'integrate_v350.py', 'compile_integrated.py',
    'test_gate_extension.py', 'RELATORIO_GNS_PESO_COMPLETO_DEV.md',
    'record_scalar_weight_gns_draft.py', 'prepare_scalar_weight_gns_stage.py',
    'record_scalar_weight_gns_progress.py', 'verify_scalar_weight_gns_custody.py',
    'scalar_weight_gns_draft_status.json', 'prepare_scalar_weight_orbit.py']
custody = {'timestamp': DATE, 'previous_custody_path': str(parent_path),
    'previous_custody_sha256': sha(parent_path), 'original_sha256': sha(original),
    'working_sha256': sha(ROOT / 'um.py'), 'previous_working_copy': str(prior),
    'python_body_unchanged_from_previous_stage': True,
    'modules': modules, 'targets': targets, 'integrated_records': len(build['records']),
    'controls': tests['passed'], 'audit_declarations': tests['axiom_report_entries'],
    'surface_sha256': {str(p): sha(p) for p in surfaces}, 'backups': BACKUPS,
    'surface_before_sha256': {str(p): sha(Path(BACKUPS[str(p)])) for p in surfaces},
    'review_sha256': {str(p): sha(p) for p in reviews},
    'report_path': str(report_path), 'report_sha256': sha(report_path),
    'artifacts': {name: sha(ROOT / name) for name in artifact_names},
    'remaining_flags': {key: evidence[key] for key in parent['remaining_flags']},
    'root_domain_equals_Tomita_domain': True, 'energy_on_full_Tomita_domain': True,
    'polar_antiunitary_constructed': True, 'factorization_on_full_domain': True,
    'polar_involution_proved': True, 'full_scalar_weight_GNS_identified': True,
    'full_scalar_weight_closed_graph_identified': True,
    'literal_ideal_equality_claimed': False, 'raw_graph_equals_closed_graph_claimed': False,
    'KMS_proved': False, 'canonical_trace_constructed': False,
    'gate_changed': False, 'full_runtime': False, 'full_goal_complete': False}
write(ROOT / 'scalar_weight_gns_custody.json', json.dumps(custody, ensure_ascii=False, indent=2).encode())
print(json.dumps({'custody': 'scalar_weight_gns_custody.json', 'surfaces': len(surfaces),
    'modules': len(modules), 'targets': len(targets), 'goal_complete': False}))
