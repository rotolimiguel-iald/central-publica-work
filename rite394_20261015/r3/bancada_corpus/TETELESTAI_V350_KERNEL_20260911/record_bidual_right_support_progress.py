"""Record the reviewed original-S variational identity and byte lineage."""
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
MARKER = 'TETELESTAI_V350_BIDUAL_RIGHT_SUPPORT_GENERATOR_INTEGRATED_20260913'
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

parent_path = ROOT / 'phase_variational_custody.json'
parent, draft = read(parent_path.name), read('bidual_right_support_draft_status.json')
integration, build, tests = read('integration.json'), read('integrated_compile.json'), read('gate_tests.json')
evidence = read('kernel_incremental_evidence.json')
reviews = [ROOT / 'revisao/REVIEW_BIDUAL_RIGHT_SUPPORT_DEV.md', ROOT / 'revisao/REVIEW_BIDUAL_RIGHT_SUPPORT_INTEGRATED.md']
assert 'BIDUAL_RIGHT_SUPPORT_DEV_REVIEW' in reviews[0].read_text(encoding='utf-8')
assert 'BIDUAL_RIGHT_SUPPORT_INTEGRATED_REVIEW' in reviews[1].read_text(encoding='utf-8')
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
assert len(modules) == 2 and len(targets) == 9 and set(targets) == set(draft['targets'])
surfaces = [Path(p) for p in parent['surface_sha256']]
before = {str(p): p.read_bytes() for p in surfaces}
assert len(surfaces) == 34
for p in surfaces:
    assert sha(p) == parent['surface_sha256'][str(p)] and MARKER.encode() not in before[str(p)]

report = ROOT / 'RELATORIO_BIDUAL_SUPORTE_DIREITO_INTEGRADA.md'
write(report, f'''# Bidual original e suporte direito e continuidade — integração revisada

{DATE}. [REAL — dois módulos/9 alvos integrados e revisados]

[REAL] O adjunto maximal de F é exatamente o S ORIGINAL, incluindo todo
seu domínio. O pareamento contra D(F) é equivalente à pertinência ao grafo de
S. A prova usa a conjugação polar J já construída, F=JSJ e a maximalidade de
F; não redefine S/F/J nem pressupõe a inclusão inversa dos comutantes.

[REAL] Se a=a* é um par direito e T=T* pertence ao comutante inteiro,
comutando com a, então Ta é um par direito auto-adjunto com inscrição
j(Ta)=Tj(a). T não precisa previamente pertencer à álgebra dos pares direitos.
A construção exibe os dois vetores do par e as duas leis de multiplicação.
Para qualquer par direito R, sua inscrição pertence ao fecho normado de Ran R,
provado pelas médias regulares no ideal do peso original. Não se supõe uma
cota uniforme para os vetores GNS dessas médias.

[OPEN] Os lemas preparam cortes racionais e a aproximação por combinações de
quadrados, mas não provam ainda que esses quadrados sejam núcleo de grafo
para F. Tampouco colocam automaticamente o par ponderado no domínio de S.
Faltam essa aproximação, o teste ponderado, a cota inferior uniforme do bloco
A e o multiplicador limitado. Inclusão inversa pelo J original, Delta^it/KMS,
traço/escala/canto Three Locks, H1/H2/H3 físicos, setor interagente e consumo
por certificados/runtime continuam abertos. Seis flags maiores falsas.

[REAL — fiação preservada] As seis flags maiores qgf/gpf não entram diretamente
em evaluate_quantum_gravity_closure: o selo legado lê qgc_, qgp_ e o feed
experimental; kernel_frontier é anexado depois. O consumo por certificado
tipado continua necessário para que novas provas movam esse selo.

{len(build['records'])} registros incrementais rc0; {tests['passed']} controles;
{tests['axiom_report_entries']} declarações Audit; {integration['embedded_files']} fontes embutidas.
Revisões DEV e integrada lidas. Dependências reutilizadas com pins; corpo
Python fora do embutido e gate preservados. Audit atual e histórico conferidos.
Nenhum runtime integral/importação de monólito. Tentativas recusadas preservadas.

[Rota racional por energia e limite antítono — DERIVED, não compilada](<{(ROOT / 'revisao/CONSULTA_RESOLVENTE_RACIONAL_QUADRADOS.md').as_posix()}>).

[Consulta sobre o bloco limitado — DERIVED, não compilada](<{(ROOT / 'revisao/CONSULTA_RVD56_BLOCO_INVERSIVEL_CFC.md').as_posix()}>).
[Proposta de aproximação por quadrados — DERIVED, não compilada](<{(ROOT / 'revisao/CONSULTA_CFC_QUADRADOS_TESTE_P.md').as_posix()}>).

[Revisão DEV](<{reviews[0].as_posix()}>).
[Revisão integrada](<{reviews[1].as_posix()}>).
[Registro anterior: inclusão direta preservada; inversa ainda aberta](<{(ROOT / 'RELATORIO_REGULARIZACAO_COMUTANTE_INTEGRADA.md').as_posix()}>).
[Reaproveitamento de Chatgpt](<{(ROOT / 'REEXAME_CHATGPT_20260912/RELATORIO_REAPROVEITAMENTO.md').as_posix()}>).

Original relido `{sha(original)}`; cópia `{sha(ROOT / 'um.py')}`;
mãe integrada/documental `{sha(parent_path)}`. Objetivo integral ativo.
'''.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — integração revisada] Dois módulos/9 alvos.

[REAL] O adjunto maximal de F é exatamente o S ORIGINAL, incluindo todo
seu domínio. O pareamento contra D(F) é equivalente à pertinência ao grafo de
S. A prova usa a conjugação polar J já construída, F=JSJ e a maximalidade de
F; não redefine S/F/J nem pressupõe a inclusão inversa dos comutantes.

[REAL] Se a=a* é um par direito e T=T* pertence ao comutante inteiro,
comutando com a, então Ta é um par direito auto-adjunto com inscrição
j(Ta)=Tj(a). T não precisa previamente pertencer à álgebra dos pares direitos.
A construção exibe os dois vetores do par e as duas leis de multiplicação.
Para qualquer par direito R, sua inscrição pertence ao fecho normado de Ran R,
provado pelas médias regulares no ideal do peso original. Não se supõe uma
cota uniforme para os vetores GNS dessas médias.

[OPEN] Os lemas preparam cortes racionais e a aproximação por combinações de
quadrados, mas não provam ainda que esses quadrados sejam núcleo de grafo
para F. Tampouco colocam automaticamente o par ponderado no domínio de S.
Faltam essa aproximação, o teste ponderado, a cota inferior uniforme do bloco
A e o multiplicador limitado. Inclusão inversa pelo J original, Delta^it/KMS,
traço/escala/canto Three Locks, H1/H2/H3 físicos, setor interagente e consumo
por certificados/runtime continuam abertos. Seis flags maiores falsas.

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
    'test_gate_extension.py', 'bidual_right_support_draft_status.json', 'record_bidual_right_support_draft.py',
    'RELATORIO_BIDUAL_SUPORTE_DIREITO_DEV.md', 'prepare_bidual_right_support_stage.py',
    'record_bidual_right_support_progress.py', 'verify_bidual_right_support_custody.py']
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
    'original_S_is_maximal_adjoint_of_F': True,
    'selfadjoint_right_pairs_stable_under_commuting_multipliers': True,
    'right_pair_vectors_in_multiplier_range_closure': True,
    'original_weight_J_not_replaced': True,
    'modular_square_flow_identified': False, 'KMS_proved': False, 'canonical_trace_constructed': False,
    'gate_changed': False, 'full_runtime': False, 'full_goal_complete': False}
write(ROOT / 'bidual_right_support_custody.json', json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'custody': 'bidual_right_support_custody.json', 'surfaces': len(surfaces),
    'modules': len(modules), 'targets': len(targets), 'goal_complete': False}))
