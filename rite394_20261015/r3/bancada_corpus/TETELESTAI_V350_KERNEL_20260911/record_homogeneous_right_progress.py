"""Record the reviewed homogeneous right GNS integration and full memory lineage."""
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
MARKER = 'TETELESTAI_V350_HOMOGENEOUS_RIGHT_GNS_INTEGRATED_20260912'
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
    assignment = next(n for n in tree.body if isinstance(n, ast.Assign) and any(
        isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in n.targets))
    assignment.value = ast.Constant('EXCLUDED_EMBEDDED_LEAN')
    return ast.dump(tree, include_attributes=False)

assert '--review-read' in sys.argv
parent_path = ROOT / 'scalar_weight_gns_custody.json'
parent = json.loads(parent_path.read_bytes())
memory_path = ROOT / 'homogeneous_right_dev_custody.json'
memory = json.loads(memory_path.read_bytes())
draft_path = ROOT / 'homogeneous_right_draft_status.json'
draft = json.loads(draft_path.read_bytes())
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
original = Path(json.loads((ROOT / 'environment.json').read_bytes())['original_source'])
reviews = [ROOT / 'revisao/REVIEW_HOMOGENEOUS_RIGHT_GNS.md',
           ROOT / 'revisao/REVIEW_HOMOGENEOUS_RIGHT_GNS_INTEGRATED.md']
assert 'HOMOGENEOUS_RIGHT_GNS_DEV_REVIEW' in reviews[0].read_text(encoding='utf-8')
assert 'INTEGRATED_HOMOGENEOUS_RIGHT_GNS_REVIEW' in reviews[1].read_text(encoding='utf-8')
assert sha(reviews[0]) == memory['review_sha256']
assert sha(original) == sha(ROOT / 'fontes/um_v350_original.py') == integration['base_sha256']
assert sha(ROOT / 'um.py') == integration['working_sha256'] == tests['working_um_sha256']
assert draft['integrated_working_sha256'] == parent['working_sha256']
assert draft['parent_custody_sha256'] == memory['previous_custody_sha256'] == sha(parent_path)
assert memory['working_sha256'] == parent['working_sha256']
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
assert len(modules) == 5 and len(targets) == 28
assert all(evidence[k] is False for k in parent['remaining_flags'])
surfaces = [Path(p) for p in memory['surface_sha256']]
assert len(surfaces) == 34
before_surfaces = {str(p): p.read_bytes() for p in surfaces}
for path in surfaces:
    assert MARKER.encode() not in before_surfaces[str(path)]
    assert sha(path) == memory['surface_sha256'][str(path)]

report_path = ROOT / 'RELATORIO_DIREITA_MODULAR_GNS_INTEGRADA.md'
report = f'''# Direita modular e adjunto no mesmo GNS — integração revisada

{DATE}. [REAL — cinco módulos/28 alvos integrados e revisados]

A direita de cada unidade matricial local y=e_ij agora está embutida na cópia
do um.py e participa do Audit integrado. Para quaisquer A,B∈n_ν, no mesmo H_I:

    ⟨Λ_ν(Ay),Λ_ν(B)⟩ = ⟨Λ_ν(A),Λ_ν(Bρy*ρ⁻¹)⟩.

O produto preserva n_ν; o operador direito é limitado e preserva o completamento
anterior. A torção do adjunto foi transportada da torre por uma fórmula explícita
de órbita dual, com deslocamento s−log(w_i/w_j). Nenhuma hipótese KMS é inserida.
O contrato genérico foi instanciado pelas unidades matriciais e sua torção.

{len(build['records'])} registros incrementais rc0; {tests['passed']} controles;
{tests['axiom_report_entries']} declarações Audit; {integration['embedded_files']}
arquivos Lean embutidos. Os cinco módulos e os dois arquivos raiz foram
verificados na integração; dependências anteriores foram reutilizadas com pins.
Revisão DEV incluiu recompilação própria, com cinco binários idênticos; a revisão
integrada confere transposição, evidências, tipos/axiomas e scripts de custódia.
O Python fora do bloco Lean embutido permaneceu idêntico ao estágio anterior.
Os controles preservam as seis flags maiores falsas; gate legado inalterado.

[OPEN] Falta identificar o fluxo candidato com (S†S)^it e provar KMS global,
construir o traço canônico/escala dual/canto Three Locks, entregar H1/H2/H3
físicos compatíveis no mesmo modelo e o setor quântico interagente, e consumir
essas construções no certificado/runtime completos. O pareamento direito
local não é KMS global nem uma representação direita de toda N. A passagem
por somas a toda matriz local ainda não foi acrescentada nesta etapa.

A regra de consumo continua exigindo os termos e suas pontes de tipo exato
compiladas em Lean, com proveniência e axiomas conferidos no Python. Novas
obrigações não se descarregam pela existência isolada de nomes ou rótulos.
Einstein, Fisher e gauge já localizados em Chatgpt permanecem reutilizáveis
com suas hipóteses; não serão reabertos por homonímia.

[Provas DEV](<{(ROOT / 'RELATORIO_DIREITA_MODULAR_GNS_DEV.md').as_posix()}>).
[Revisão DEV](<{reviews[0].as_posix()}>).
[Revisão integrada](<{reviews[1].as_posix()}>).
[Tabela de pendências anterior](<{(ROOT / 'RELATORIO_DIREITA_MODULAR_GNS_REVISADO.md').as_posix()}>).

Original relido `{sha(original)}`; cópia `{sha(ROOT / 'um.py')}`.
Mãe matemática `{sha(parent_path)}`; mãe imediata da memória `{sha(memory_path)}`.
Sem execução/importação do original ou runtime integral do monólito.
O histórico DEV sem integração permanece ao lado; objetivo integral ativo.
'''
write(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — integração revisada] Cinco módulos/28 alvos da direita homogênea
foram embutidos na cópia do um.py. O produto Ay preserva n_ν, a ação direita
preserva o mesmo H_I, e R_y*=R_(ρy*ρ⁻¹) fornece o pareamento para quaisquer
A,B∈n_ν e cada unidade matricial local y. As instâncias descarregam os campos
do contrato; nenhuma hipótese KMS é introduzida. O DEV anterior fica histórico.

{len(build['records'])} registros incrementais rc0; {tests['passed']} controles;
{tests['axiom_report_entries']} declarações Audit; {integration['embedded_files']}
embutidos. Revisões DEV e integrada lidas; dependências reutilizadas com pins.
Python fora do embutido preservado; sem runtime integral. Cópia {sha(ROOT / 'um.py')}.
Original preservado; seis flags maiores falsas; gate legado inalterado.

[OPEN] Identificação espectral de S†S/KMS global, traço/escala/canto Three Locks,
H1/H2/H3 físicos no mesmo modelo, setor quântico interagente e consumo integral
pelo certificado/runtime. O pareamento direito local não fornece esses elos
sozinho. Reutilizar Einstein/Fisher/gauge já encontrados com suas hipóteses.
O objetivo integral permanece ativo.

[Relatório atual](<{report_path.as_posix()}>).
[Revisão integrada](<{reviews[1].as_posix()}>).
'''
for path in surfaces:
    raw = before_surfaces[str(path)]
    newline = '\r\n' if b'\r\n' in raw else '\n'
    write(path, raw + note.replace('\n', newline).encode('utf-8'), raw)
artifacts = ['integration.json', 'integrated_compile.json', 'kernel_incremental_evidence.json',
    'gate_tests.json', 'gate_extension.py', 'integrate_v350.py', 'compile_integrated.py',
    'test_gate_extension.py', 'RELATORIO_DIREITA_MODULAR_GNS_DEV.md',
    'RELATORIO_DIREITA_MODULAR_GNS_REVISADO.md', 'record_homogeneous_right_draft.py',
    'record_homogeneous_right_memory.py', 'prepare_homogeneous_right_stage.py',
    'record_homogeneous_right_progress.py', 'verify_homogeneous_right_custody.py',
    'homogeneous_right_draft_status.json', 'homogeneous_right_dev_verification.json']
custody = {'timestamp': DATE, 'previous_custody_path': str(memory_path),
    'previous_custody_sha256': sha(memory_path),
    'previous_integrated_custody_path': str(parent_path),
    'previous_integrated_custody_sha256': sha(parent_path), 'original_sha256': sha(original),
    'working_sha256': sha(ROOT / 'um.py'), 'previous_working_copy': str(prior),
    'python_body_unchanged_from_previous_stage': True,
    'modules': modules, 'targets': targets, 'integrated_records': len(build['records']),
    'controls': tests['passed'], 'audit_declarations': tests['axiom_report_entries'],
    'surface_sha256': {str(p): sha(p) for p in surfaces}, 'backups': BACKUPS,
    'surface_before_sha256': {str(p): sha(Path(BACKUPS[str(p)])) for p in surfaces},
    'review_sha256': {str(p): sha(p) for p in reviews},
    'report_path': str(report_path), 'report_sha256': sha(report_path),
    'artifacts': {name: sha(ROOT / name) for name in artifacts},
    'remaining_flags': {key: evidence[key] for key in parent['remaining_flags']},
    'root_domain_equals_Tomita_domain': True, 'energy_on_full_Tomita_domain': True,
    'polar_antiunitary_constructed': True, 'factorization_on_full_domain': True,
    'polar_involution_proved': True, 'full_scalar_weight_GNS_identified': True,
    'full_scalar_weight_closed_graph_identified': True,
    'right_adjoint_pairing_on_same_full_GNS': True,
    'literal_ideal_equality_claimed': False, 'raw_graph_equals_closed_graph_claimed': False,
    'KMS_proved': False, 'canonical_trace_constructed': False,
    'gate_changed': False, 'full_runtime': False, 'full_goal_complete': False}
write(ROOT / 'homogeneous_right_custody.json', json.dumps(custody, ensure_ascii=False, indent=2).encode())
print(json.dumps({'custody': 'homogeneous_right_custody.json', 'surfaces': len(surfaces),
    'modules': len(modules), 'targets': len(targets), 'goal_complete': False}))
