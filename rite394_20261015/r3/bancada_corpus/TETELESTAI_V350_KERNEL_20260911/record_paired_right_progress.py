"""Record reviewed original-adjoint right pairs with the complete memory lineage."""
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
MARKER = 'TETELESTAI_V350_PAIRED_RIGHT_GENERATOR_INTEGRATED_20260912'
BACKUPS = {}
assert '--review-read' in sys.argv

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(name):
    return json.loads((ROOT / name).read_bytes())

def write(path, raw, before=None):
    assert raw and (path.resolve().is_relative_to(ROOT) or path.resolve() in (
        CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md'))
    if before is None:
        assert not path.exists(), path
    else:
        assert path.read_bytes() == before and raw.startswith(before) and len(raw) > len(before)
        backup = path.with_name(path.name + '.bak_' + STAMP)
        with backup.open('xb') as stream:
            stream.write(before)
        assert backup.read_bytes() == before
        BACKUPS[str(path)] = str(backup)
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw
    if before is not None:
        assert path.read_bytes() == before
    temp.replace(path)
    assert path.read_bytes() == raw

def body(path):
    tree = ast.parse(path.read_bytes())
    node = next(n for n in tree.body if isinstance(n, ast.Assign) and any(
        isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in n.targets))
    node.value = ast.Constant('EXCLUDED_EMBEDDED_LEAN')
    return ast.dump(tree, include_attributes=False)

parent_path = ROOT / 'right_regularization_custody.json'
parent, draft = read(parent_path.name), read('paired_right_draft_status.json')
integration, build, tests = read('integration.json'), read('integrated_compile.json'), read('gate_tests.json')
evidence = read('kernel_incremental_evidence.json')
reviews = [ROOT / 'revisao/REVIEW_PAIRED_RIGHT_DEV.md', ROOT / 'revisao/REVIEW_PAIRED_RIGHT_INTEGRATED.md']
assert 'PAIRED_RIGHT_DEV_REVIEW' in reviews[0].read_text(encoding='utf-8')
assert 'PAIRED_RIGHT_INTEGRATED_REVIEW' in reviews[1].read_text(encoding='utf-8')
assert draft['parent_custody_sha256'] == sha(parent_path)
assert draft['integrated_working_sha256'] == parent['working_sha256']
original = Path(read('environment.json')['original_source'])
assert sha(original) == sha(ROOT / 'fontes/um_v350_original.py') == integration['base_sha256']
assert sha(ROOT / 'um.py') == integration['working_sha256'] == tests['working_um_sha256']
prior = next(p for p in ROOT.glob('um.py.bak_*') if sha(p) == parent['working_sha256'])
assert body(prior) == body(ROOT / 'um.py')
assert build['incremental_build_ok']
for row in build['records']:
    source = Path(row['source']).resolve()
    assert source.is_relative_to(ROOT / 'kernel')
    binary = ROOT / 'build' / source.relative_to(ROOT / 'kernel').with_suffix('.olean')
    assert row['returncode'] == 0 and row['output_exists']
    assert sha(source) == row['sha256'] and sha(binary) == row['output_sha256']
assert tests['passed'] == len(tests['checks']) and all(c['passed'] for c in tests['checks'])
assert not tests['full_monolithic_runtime_run'] and not tests['frontier']['legacy_gate_changed']
audit_stdout = Path(build['records'][-1]['stdout'])
assert evidence['audit_stdout_sha256'] == evidence['audit_capture_sha256_full'] == sha(audit_stdout)
assert evidence['audit_stdout_path'] == str(audit_stdout)
baseline = read('fontes/um_absoluto.json')['core']['kernel_formalization']
assert evidence['historical_v350_audit_metadata'] == {key: baseline.get(key) for key in
    ('audit_stdout_sha256', 'audit_capture_sha256_full')}
assert all(evidence[k] is False for k in parent['remaining_flags'])
modules, targets = {}, {}
for name, row in draft['modules'].items():
    source = ROOT / 'kernel/TGLV350' / (name + '.lean')
    final = ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean')
    raw = source.read_text(encoding='utf-8')
    assert sha(source) == row['source_sha256']
    assert sha(ROOT / 'build/TGLV350' / (name + '.olean')) == row['binary_sha256']
    assert re.sub(r'^import TGLV350\.', 'import TGLExt.V350', raw, flags=re.M) == final.read_text(encoding='utf-8')
    modules[name] = {'development_sha256': sha(source), 'integrated_sha256': sha(final),
        'development_binary_sha256': sha(ROOT / 'build/TGLV350' / (name + '.olean'))}
    for short in re.findall(r'^#print axioms ([\w.]+)$', raw, re.M):
        full = 'TGLV350.Regular.' + short
        axioms = evidence['axiom_report'][full]
        assert set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'}
        assert sorted(axioms) == draft['targets'][full]
        targets[full] = axioms
assert len(modules) == 3 and len(targets) == 29 and set(targets) == set(draft['targets'])
surfaces = [Path(p) for p in parent['surface_sha256']]
before = {str(p): p.read_bytes() for p in surfaces}
assert len(surfaces) == 34
for p in surfaces:
    assert sha(p) == parent['surface_sha256'][str(p)] and MARKER.encode() not in before[str(p)]

report = ROOT / 'RELATORIO_ALGEBRA_DIREITA_ADJUNTO_INTEGRADA.md'
write(report, f'''# Álgebra direita e adjunto original e continuidade — integração revisada

{DATE}. [REAL — três módulos/29 alvos integrados e revisados]

No mesmo H_I, com o ideal completo n_ν e os operadores fechados originais
S e F=S†, ScalarRightAdjointPair dá dois vetores η, ζ para um operador limitado R:
RΛν(a)=π(a)η e R*Λν(a)=π(a)ζ para todo a∈n_ν.
[REAL] A relação Fη=ζ é PROVADA dessas identidades, não incluída nas hipóteses.
A prova regulariza, passa ao limite no pareamento e usa o fecho do grafo
completo de S e a caracterização maximal do adjunto original.

[REAL] Para todo T∈π(N)', K_h(T)=R_h* T R_h possui esse par direito,
com η=R_h*Tη_h e ζ=R_h*T*η_h, onde η_h=Λν(e_h), h>0.
||K_h(T)||≤||T|| e K_h(T)→T fortemente-* quando h↓0.
A ordem dos fatores é preservada: não se supõe que T comute com R_h.
R_h*→I usa o bound de contração; não se presume continuidade geral de star em SOT.

[REAL] Os operadores com par direito formam uma NonUnitalStarSubalgebra:
zero, soma, multiplicação escalar, produto e adjunto foram construídos.
A álgebra de von Neumann gerada por ela é TODO o comutante π(N)'.

[OPEN] Isso é uma álgebra de operadores limitados com dois vetores direitos.
Ainda não é a plenitude de uma álgebra de Hilbert, nem a densidade de um
núcleo de grafo para F, nem a reconstrução R=Jπ(b)J. A inclusão inversa
π(N)'⊆Jπ(N)J e o fechamento von Neumann da imagem π(N) continuam abertos.
O J original não foi trocado por conjugação de estado gaussiano.
Permanecem abertos Δ^it/KMS, traço/escala/canto Three Locks, H1/H2/H3 físicos,
setor interagente e consumo por certificados tipados/runtime.
Seis flags maiores falsas; esta construção não muda o gate.

[REAL — fiação preservada] As seis flags maiores qgf/gpf não entram diretamente
em evaluate_quantum_gravity_closure: o selo legado lê qgc_, qgp_ e o feed
experimental; kernel_frontier é anexado depois. O consumo por certificado
tipado continua necessário para que novas provas movam esse selo.

{len(build['records'])} registros incrementais rc0; {tests['passed']} controles;
{tests['axiom_report_entries']} declarações Audit; {integration['embedded_files']} fontes embutidas.
Revisões DEV e integrada lidas. Dependências reutilizadas com pins; corpo
Python fora do embutido e gate preservados. Audit atual e histórico conferidos.
Nenhum runtime integral/importação de monólito. Tentativas recusadas preservadas.

[Revisão DEV](<{reviews[0].as_posix()}>).
[Revisão integrada](<{reviews[1].as_posix()}>).
[Registro anterior: inclusão direta preservada; inversa ainda aberta](<{(ROOT / 'RELATORIO_REGULARIZACAO_COMUTANTE_INTEGRADA.md').as_posix()}>).
[Reaproveitamento de Chatgpt](<{(ROOT / 'REEXAME_CHATGPT_20260912/RELATORIO_REAPROVEITAMENTO.md').as_posix()}>).

Original relido `{sha(original)}`; cópia `{sha(ROOT / 'um.py')}`;
mãe integrada/documental `{sha(parent_path)}`. Objetivo integral ativo.
'''.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — integração revisada] Três módulos/29 alvos.

No mesmo H_I, com o ideal completo n_ν e os operadores fechados originais
S e F=S†, ScalarRightAdjointPair dá dois vetores η, ζ para um operador limitado R:
RΛν(a)=π(a)η e R*Λν(a)=π(a)ζ para todo a∈n_ν.
[REAL] A relação Fη=ζ é PROVADA dessas identidades, não incluída nas hipóteses.
A prova regulariza, passa ao limite no pareamento e usa o fecho do grafo
completo de S e a caracterização maximal do adjunto original.

[REAL] Para todo T∈π(N)', K_h(T)=R_h* T R_h possui esse par direito,
com η=R_h*Tη_h e ζ=R_h*T*η_h, onde η_h=Λν(e_h), h>0.
||K_h(T)||≤||T|| e K_h(T)→T fortemente-* quando h↓0.
A ordem dos fatores é preservada: não se supõe que T comute com R_h.
R_h*→I usa o bound de contração; não se presume continuidade geral de star em SOT.

[REAL] Os operadores com par direito formam uma NonUnitalStarSubalgebra:
zero, soma, multiplicação escalar, produto e adjunto foram construídos.
A álgebra de von Neumann gerada por ela é TODO o comutante π(N)'.

[OPEN] Isso é uma álgebra de operadores limitados com dois vetores direitos.
Ainda não é a plenitude de uma álgebra de Hilbert, nem a densidade de um
núcleo de grafo para F, nem a reconstrução R=Jπ(b)J. A inclusão inversa
π(N)'⊆Jπ(N)J e o fechamento von Neumann da imagem π(N) continuam abertos.
O J original não foi trocado por conjugação de estado gaussiano.
Permanecem abertos Δ^it/KMS, traço/escala/canto Three Locks, H1/H2/H3 físicos,
setor interagente e consumo por certificados tipados/runtime.
Seis flags maiores falsas; esta construção não muda o gate.

[REAL — fiação preservada] As seis flags maiores qgf/gpf não entram diretamente
em evaluate_quantum_gravity_closure: o selo legado lê qgc_, qgp_ e o feed
experimental; kernel_frontier é anexado depois. O consumo por certificado
tipado continua necessário para que novas provas movam esse selo.

{len(build['records'])} registros rc0; {tests['passed']} controles; {tests['axiom_report_entries']} Audit.
Revisões DEV/integrada lidas. Cópia {sha(ROOT / 'um.py')}; original preservado.
34 memórias com backup imediato de bytes; gate legado e seis flags maiores preservados.
Objetivo integral ativo; nenhum runtime integral novo.

[Provas, revisão e limites](<{report.as_posix()}>).
'''
for p in surfaces:
    raw = before[str(p)]
    newline = '\r\n' if b'\r\n' in raw else '\n'
    write(p, raw + note.replace('\n', newline).encode('utf-8'), raw)
artifacts = ['integration.json', 'integrated_compile.json', 'kernel_incremental_evidence.json',
    'gate_tests.json', 'gate_extension.py', 'integrate_v350.py', 'compile_integrated.py',
    'test_gate_extension.py', 'paired_right_draft_status.json', 'record_paired_right_draft.py',
    'RELATORIO_ALGEBRA_DIREITA_ADJUNTO_DEV.md', 'prepare_paired_right_stage.py',
    'record_paired_right_progress.py', 'verify_paired_right_custody.py']
data = {'timestamp': DATE, 'previous_custody_path': str(parent_path),
    'previous_custody_sha256': sha(parent_path), 'original_sha256': sha(original),
    'working_sha256': sha(ROOT / 'um.py'), 'previous_working_copy': str(prior),
    'python_body_unchanged_from_previous_stage': True, 'modules': modules, 'targets': targets,
    'integrated_records': len(build['records']), 'controls': tests['passed'],
    'audit_declarations': tests['axiom_report_entries'],
    'current_audit_stdout_path': str(audit_stdout), 'current_audit_stdout_sha256': sha(audit_stdout),
    'surface_sha256': {str(p): sha(p) for p in surfaces}, 'backups': BACKUPS,
    'surface_before_sha256': {str(p): sha(Path(BACKUPS[str(p)])) for p in surfaces},
    'review_sha256': {str(p): sha(p) for p in reviews}, 'report_path': str(report),
    'report_sha256': sha(report), 'artifacts': {name: sha(ROOT / name) for name in artifacts},
    'remaining_flags': {key: evidence[key] for key in parent['remaining_flags']},
    'original_adjoint_right_pairs_constructed': True,
    'paired_right_star_algebra_constructed': True,
    'paired_right_algebra_generates_commutant': True,
    'original_weight_J_not_replaced': True,
    'modular_square_flow_identified': False, 'KMS_proved': False, 'canonical_trace_constructed': False,
    'gate_changed': False, 'full_runtime': False, 'full_goal_complete': False}
write(ROOT / 'paired_right_custody.json', json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'custody': 'paired_right_custody.json', 'surfaces': len(surfaces),
    'modules': len(modules), 'targets': len(targets), 'goal_complete': False}))
