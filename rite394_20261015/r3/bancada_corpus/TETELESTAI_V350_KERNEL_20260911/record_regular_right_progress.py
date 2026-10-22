"""Record the reviewed right-scaling integration and append the full memory lineage."""
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
MARKER = 'TETELESTAI_V350_REGULAR_RIGHT_UNITARY_INTEGRATED_20260912'
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

parent_path = ROOT / 'right_square_custody.json'
parent, draft = read(parent_path.name), read('regular_right_draft_status.json')
integration, build, tests = read('integration.json'), read('integrated_compile.json'), read('gate_tests.json')
evidence = read('kernel_incremental_evidence.json')
reviews = [ROOT / 'revisao/REVIEW_REGULAR_RIGHT_DEV.md', ROOT / 'revisao/REVIEW_REGULAR_RIGHT_INTEGRATED.md']
assert 'REGULAR_RIGHT_DEV_REVIEW' in reviews[0].read_text(encoding='utf-8')
assert 'REGULAR_RIGHT_INTEGRATED_REVIEW' in reviews[1].read_text(encoding='utf-8')
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
assert len(modules) == 3 and len(targets) == 36 and set(targets) == set(draft['targets'])
surfaces = [Path(p) for p in parent['surface_sha256']]
before = {str(p): p.read_bytes() for p in surfaces}
assert len(surfaces) == 34
for p in surfaces:
    assert sha(p) == parent['surface_sha256'][str(p)] and MARKER.encode() not in before[str(p)]

report = ROOT / 'RELATORIO_DIREITA_UNITARIA_REGULAR_INTEGRADA.md'
write(report, f'''# Direita unitária regular — integração revisada

{DATE}. [REAL — três módulos/36 alvos integrados e revisados]

No mesmo GNS H_I do peso escalar completo, R_t Λ(a)=Λ(a λ_t), R_0=I,
R_s R_t=R_(s+t) e R_t*=R_(-t). A órbita já existente foi reaproveitada
como caráter na coordenada exterior vezes shift na fibra interior.

O MESMO S fechado satisfaz S R_t=π(λ_t*)S em D(S), e seu adjunto máximo
F=S† satisfaz Fπ(λ_t)=R_t*F em D(F). A composição A=S†S, já provada
positiva e auto-adjunta nos estágios anteriores, agora satisfaz:

    R_t x ∈ D(A) ↔ x ∈ D(A),        A R_t x = R_t A x.

A igualdade usa TODO o domínio composto. A inversa R_(-t) dá o retorno;
não se assume continuidade de S, KMS ou igualdade com um fluxo candidato.
Este resultado resolve a pendência para o gerador regular registrada no
[relatório anterior](<{(ROOT / 'RELATORIO_ESCALA_DIREITA_SQUARED_INTEGRADA.md').as_posix()}>).
As unidades matriciais locais já tinham A R_y=(w_i/w_j)R_y A; os dois
resultados agora se referem ao mesmo operador e ao mesmo GNS.

[OPEN] Isto não identifica A^it com o fluxo modular completo, nem prova
KMS global, nem estende por si só a ação direita a toda N. Não foi provada
nova continuidade forte de R_t nesta etapa. Restam traço/escala/canto
Three Locks, H1/H2/H3 físicos no mesmo modelo, setor quântico interagente
e consumo pelos certificados/runtime. Einstein/Fisher/gauge encontrados
na pasta Chatgpt serão reutilizados com suas hipóteses. Seis flags falsas.

[REAL — leitura da fiação] As seis flags maiores qgf/gpf não entram
diretamente em evaluate_quantum_gravity_closure: o selo legado lê qgc_,
qgp_ e o feed experimental. kernel_frontier é anexado ao resultado.
Uma prova nova exige certificado tipado, proveniência e ligação explícita
ao consumo correspondente; acrescentar lemas ou marcar a flag não muda
automaticamente esse selo. A fiação foi preservada nesta etapa.

{len(build['records'])} registros incrementais rc0; {tests['passed']} controles;
{tests['axiom_report_entries']} declarações Audit; {integration['embedded_files']}
fontes embutidas. Revisões DEV e integrada lidas, dependências reutilizadas
com pins. Corpo Python fora do embutido preservado; metadados Audit atuais
verificados. Nenhum monólito executado/importado. Gate legado inalterado.

[Revisão DEV](<{reviews[0].as_posix()}>).
[Revisão integrada](<{reviews[1].as_posix()}>).
[Reaproveitamento de Chatgpt](<{(ROOT / 'REEXAME_CHATGPT_20260912/RELATORIO_REAPROVEITAMENTO.md').as_posix()}>).

Original relido `{sha(original)}`; cópia `{sha(ROOT / 'um.py')}`;
mãe integrada e de memória `{sha(parent_path)}`. Objetivo integral ativo.
'''.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — integração revisada] Três módulos/36 alvos constroem a direita
unitária R_t do gerador regular λ_t no mesmo GNS H_I e provam, no MESMO
A=S†S, R_t x∈D(A) ↔ x∈D(A) e A R_t x=R_t A x. A fórmula de órbita
scalarOrbit_right_regular foi reutilizada; os domínios completos de S e
S† foram transportados antes da composição. Não se postulou KMS.
Esta pendência para λ_t no registro anterior está resolvida. A relação
matricial local de escala anterior e a nova comutação usam o mesmo A.

[REAL — leitura da fiação] As seis flags maiores qgf/gpf não entram
diretamente em evaluate_quantum_gravity_closure: o selo legado lê qgc_,
qgp_ e o feed experimental. kernel_frontier é anexado ao resultado.
Uma prova nova exige certificado tipado, proveniência e ligação explícita
ao consumo correspondente; acrescentar lemas ou marcar a flag não muda
automaticamente esse selo. A fiação foi preservada nesta etapa.

{len(build['records'])} registros incrementais rc0; {tests['passed']} controles;
{tests['axiom_report_entries']} declarações Audit. Revisões DEV e integrada lidas.
Cópia {sha(ROOT / 'um.py')}; original preservado; seis flags maiores falsas.
Metadados Audit atuais conferidos; sem runtime integral; gate inalterado.

[OPEN] Potências de A e identificação do fluxo/KMS global; continuidade
forte e extensão da direita ainda não demonstradas neste novo módulo;
traço/escala/canto Three Locks, H1/H2/H3 físicos compatíveis, interação
quântica e consumo pelo certificado. Reutilizar Einstein/Fisher/gauge já
encontrados, descarregando suas hipóteses. Objetivo integral ativo.

[Prova, revisão e limites](<{report.as_posix()}>).
'''
for p in surfaces:
    raw = before[str(p)]
    newline = '\r\n' if b'\r\n' in raw else '\n'
    write(p, raw + note.replace('\n', newline).encode('utf-8'), raw)
artifacts = ['integration.json', 'integrated_compile.json', 'kernel_incremental_evidence.json',
    'gate_tests.json', 'gate_extension.py', 'integrate_v350.py', 'compile_integrated.py',
    'test_gate_extension.py', 'regular_right_draft_status.json', 'record_regular_right_draft.py',
    'RELATORIO_DIREITA_UNITARIA_REGULAR_DEV.md', 'prepare_regular_right_stage.py',
    'record_regular_right_progress.py', 'verify_regular_right_custody.py']
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
    'same_actual_square_domain_regular_invariant': True,
    'regular_right_commutes_on_full_square_domain': True,
    'modular_square_flow_identified': False, 'KMS_proved': False, 'canonical_trace_constructed': False,
    'gate_changed': False, 'full_runtime': False, 'full_goal_complete': False}
write(ROOT / 'regular_right_custody.json', json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'custody': 'regular_right_custody.json', 'surfaces': len(surfaces),
    'modules': len(modules), 'targets': len(targets), 'goal_complete': False}))
