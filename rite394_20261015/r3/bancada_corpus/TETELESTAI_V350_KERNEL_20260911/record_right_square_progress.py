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
MARKER = 'TETELESTAI_V350_RIGHT_SQUARE_SCALING_INTEGRATED_20260912'
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

parent_path = ROOT / 'scalar_right_tomita_custody.json'
parent, draft = read(parent_path.name), read('right_square_draft_status.json')
integration, build, tests = read('integration.json'), read('integrated_compile.json'), read('gate_tests.json')
evidence = read('kernel_incremental_evidence.json')
reviews = [ROOT / 'revisao/REVIEW_RIGHT_SQUARE_DEV.md', ROOT / 'revisao/REVIEW_RIGHT_SQUARE_INTEGRATED.md']
assert 'RIGHT_SQUARE_DEV_REVIEW' in reviews[0].read_text(encoding='utf-8')
assert 'RIGHT_SQUARE_INTEGRATED_REVIEW' in reviews[1].read_text(encoding='utf-8')
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
assert len(modules) == 2 and len(targets) == 13 and set(targets) == set(draft['targets'])
surfaces = [Path(p) for p in parent['surface_sha256']]
before = {str(p): p.read_bytes() for p in surfaces}
assert len(surfaces) == 34
for p in surfaces:
    assert sha(p) == parent['surface_sha256'][str(p)] and MARKER.encode() not in before[str(p)]

report = ROOT / 'RELATORIO_ESCALA_DIREITA_SQUARED_INTEGRADA.md'
write(report, f'''# Escala direita no domínio completo de S†S — integração revisada

{DATE}. [REAL — dois módulos/13 alvos integrados e revisados]

No mesmo H_I, o mesmo operador A=S†S satisfaz, para toda unidade matricial
local y=e_ij, todo x∈D(A) e r=w_i/w_j>0:

    R_y x ∈ D(A),        A R_y x = r R_y A x.

O transporte de domínio antes aberto agora está provado. A identidade vale
em todo o domínio composto, e não somente no núcleo algébrico. O resultado
genérico usa dados homogêneos d,e cujo elemento esquerdo de e é a estrela
do de d; então A R_d=R_e* A. A instância matricial descarrega essa condição.
A passagem R_e*=rR_y usa tanto a torção ρ e_ij ρ⁻¹=r e_ij quanto a igualdade
de frequências −log(w_j/w_i)=log(w_i/w_j). Não há troca de operador ou GNS.

[OPEN] Falta identificar as potências unitárias de A com o fluxo completo
e provar KMS global. A relação local de escala não fornece, sozinha, essa
identificação nem uma representação direita já estendida a toda a álgebra
regular. Traço canônico, escala dual, canto Three Locks, H1/H2/H3 físicos,
setor quântico interagente e consumo pelo certificado/runtime continuam
abertos. As pontes de Einstein, Fisher e gauge existentes serão reutilizadas
com suas hipóteses. As seis flags maiores permanecem falsas; gate inalterado.

O próximo gerador tem um insumo já existente: scalarOrbit_right_regular
descreve a multiplicação à direita por regularUnitary como fase vezes shift.
[OPEN] Reutilizar essa fórmula para construir a direita unitária no mesmo
GNS, transportar os domínios e demonstrar a comutação correspondente com A.
Nem essa extensão nem a identificação do fluxo são declaradas provadas aqui.

{len(build['records'])} registros incrementais rc0; {tests['passed']} controles;
{tests['axiom_report_entries']} declarações Audit; {integration['embedded_files']}
arquivos embutidos. Dependências anteriores reutilizadas com pins. Revisões
DEV e integrada lidas. Corpo Python fora do embutido preservado. Hashes
globais do Audit conferidos contra o stream atual, com histórico preservado.
Não houve execução/importação do original nem runtime integral do monólito.

[Revisão DEV](<{reviews[0].as_posix()}>).
[Revisão integrada](<{reviews[1].as_posix()}>).
[Tabela geral de pendências](<{(ROOT / 'RELATORIO_DOMINIOS_TOMITA_ADJUNTO_INTEGRADOS.md').as_posix()}>).
A indicação de composição de domínio ainda aberta naquela tabela é superada
por este registro; as demais obrigações físicas/modulares permanecem.

Original relido `{sha(original)}`; cópia `{sha(ROOT / 'um.py')}`;
mãe integrada e de memória `{sha(parent_path)}`. Objetivo integral ativo.
'''.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — integração revisada] Dois módulos/13 alvos provam para o MESMO A=S†S:
R_yD(A)⊆D(A) e A R_yx=(w_i/w_j)R_yAx para cada unidade matricial local y=e_ij
e TODO x∈D(A). A torção de e_ji e a frequência correspondente descarregam
a instância. O alvo de transporte do domínio composto anteriormente aberto
foi resolvido; não se afirma que R_y seja inversível nem que seja o fluxo.

{len(build['records'])} registros incrementais rc0; {tests['passed']} controles;
{tests['axiom_report_entries']} declarações Audit. Revisões DEV e integrada lidas.
Cópia {sha(ROOT / 'um.py')}; original preservado; seis flags maiores falsas.
Hash do Audit atual conferido; valores históricos preservados. Sem runtime integral.

[OPEN] Identificação das potências de A com o fluxo/KMS global, traço/escala/
canto Three Locks, H1/H2/H3 físicos compatíveis, interação quântica e consumo
pelo certificado. Reutilizar Einstein/Fisher/gauge com suas hipóteses.
A relação local de escala não quita esses elos. Objetivo integral ativo.
Próximo reuso: scalarOrbit_right_regular já descreve a órbita direita do
gerador unitário regular; sua ação GNS e comutação com A ainda exigem prova.

[Prova, revisão e limites](<{report.as_posix()}>).
'''
for p in surfaces:
    raw = before[str(p)]
    newline = '\r\n' if b'\r\n' in raw else '\n'
    write(p, raw + note.replace('\n', newline).encode('utf-8'), raw)
artifacts = ['integration.json', 'integrated_compile.json', 'kernel_incremental_evidence.json',
    'gate_tests.json', 'gate_extension.py', 'integrate_v350.py', 'compile_integrated.py',
    'test_gate_extension.py', 'right_square_draft_status.json', 'record_right_square_draft.py',
    'RELATORIO_ESCALA_DIREITA_SQUARED_DEV.md', 'prepare_right_square_stage.py',
    'record_right_square_progress.py', 'verify_right_square_custody.py']
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
    'same_actual_square_domain_right_invariant': True,
    'matrix_unit_right_scaling_on_full_square_domain': True,
    'modular_square_flow_identified': False, 'KMS_proved': False, 'canonical_trace_constructed': False,
    'gate_changed': False, 'full_runtime': False, 'full_goal_complete': False}
write(ROOT / 'right_square_custody.json', json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'custody': 'right_square_custody.json', 'surfaces': len(surfaces),
    'modules': len(modules), 'targets': len(targets), 'goal_complete': False}))
