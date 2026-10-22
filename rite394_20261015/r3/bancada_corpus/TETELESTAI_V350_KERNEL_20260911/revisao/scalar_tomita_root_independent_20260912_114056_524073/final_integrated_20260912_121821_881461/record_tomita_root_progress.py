"""Record the reviewed positive root integration; keep prior evidence immutable."""
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
MARKER = 'TETELESTAI_V350_TOMITA_ROOT_INTEGRATED_20260912'
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
    assign = next(n for n in tree.body if isinstance(n, ast.Assign) and any(
        isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in n.targets))
    assign.value = ast.Constant('EXCLUDED_EMBEDDED_LEAN')
    return ast.dump(tree, include_attributes=False)

assert '--review-read' in sys.argv
parent_path = ROOT / 'REEXAME_CHATGPT_20260912/custody.json'
parent = json.loads(parent_path.read_bytes())
square_path = ROOT / 'tomita_square_custody.json'
square = json.loads(square_path.read_bytes())
draft = json.loads((ROOT / 'tomita_root_draft_status.json').read_bytes())
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
original = Path(json.loads((ROOT / 'environment.json').read_bytes())['original_source'])
review = ROOT / 'revisao/REVIEW_SCALAR_TOMITA_ROOT_INTEGRATED.md'
assert 'INTEGRATED_TOMITA_ROOT_REVIEW' in review.read_text(encoding='utf-8')
assert sha(original) == sha(ROOT / 'fontes/um_v350_original.py') == integration['base_sha256']
assert sha(ROOT / 'um.py') == integration['working_sha256'] == tests['working_um_sha256']
assert draft['integrated_working_sha256'] == square['working_sha256'] == parent['working_sha256']
assert parent['parent_sha256'] == sha(square_path)
prior = next(p for p in ROOT.glob('um.py.bak_*') if sha(p) == parent['working_sha256'])
assert body(prior) == body(ROOT / 'um.py')
assert build['incremental_build_ok'] and all(r['returncode'] == 0 for r in build['records'])
assert tests['passed'] == len(tests['checks']) and all(c['passed'] for c in tests['checks'])
assert not tests['full_monolithic_runtime_run'] and not tests['frontier']['legacy_gate_changed']
for row in build['records']:
    source = Path(row['source'])
    binary = ROOT / 'build' / source.relative_to(ROOT / 'kernel').with_suffix('.olean')
    assert sha(source) == row['sha256'] and sha(binary) == row['output_sha256']
targets, modules = {}, {}
for name, row in draft['modules'].items():
    source = ROOT / 'kernel/TGLV350' / (name + '.lean')
    final = ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean')
    raw = source.read_text(encoding='utf-8')
    assert sha(source) == row['source_sha256']
    assert re.sub(r'^import TGLV350\.', 'import TGLExt.V350', raw, flags=re.M) == final.read_text(encoding='utf-8')
    for short in re.findall(r'^#print axioms ([\w.]+)$', raw, re.M):
        name_full = 'TGLV350.Regular.' + short
        axioms = evidence['axiom_report'][name_full]
        assert set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'}
        assert sorted(axioms) == draft['targets'][name_full]
        targets[name_full] = axioms
    modules[name] = {'development_sha256': sha(source), 'integrated_sha256': sha(final)}
assert len(modules) == 5 and len(targets) == 30
assert all(evidence[k] is False for k in parent['remaining_flags'])
report_path = ROOT / 'RELATORIO_RAIZ_TOMITA_INTEGRADA.md'
report = f'''# Resolvente e raiz positiva de S†S — integração revisada

{DATE}. [REAL — compilação incremental e revisão independente em cópia]

No mesmo H_I, A=S†S possui o resolvente R=(I+A)⁻¹ limitado, injetivo,
auto-adjunto e 0≤R≤I. A equação R(z)=x com x+Ax=z inclui x∈D(A).
Os grafos das raízes CFC limitadas √R e √(I−R) definem B positivo,
auto-adjunto, fechado e densamente definido. B²=A como mapas parciais,
com igualdade do domínio sucessivo inteiro. Em D(A), ‖Bx‖²=‖Sx‖².
O núcleo de B é trivial; isso não prova gap.

Cinco módulos/30 alvos integrados; {len(build['records'])} registros rc0,
{tests['passed']} controles e {tests['axiom_report_entries']} declarações distintas
no Audit existente ampliado. Compilação incremental com reutilização de
dependências pinadas, não rebuild global nem execução integral do monólito.
O corpo Python fora das fontes Lean incorporadas é idêntico ao da etapa anterior.

[OPEN] Ainda faltam D(B)=D(S), energia nesse domínio inteiro, construção de J
como fator polar do S atual e identificação modular/KMS com o peso. Traço e
escala dual, canto contínuo/Three Locks e H1, H2/H3 físicos compatíveis,
setor quântico interagente e certificado completo consumido seguem pendentes.
As seis flags maiores permanecem falsas e o gate legado não foi alterado.

[DEV e hipóteses](<{(ROOT / 'RELATORIO_RAIZ_TOMITA_DEV.md').as_posix()}>).
[Revisão matemática independente](<{(ROOT / 'revisao/REVIEW_SCALAR_TOMITA_ROOT.md').as_posix()}>).
[Revisão desta integração](<{review.as_posix()}>).
[Reexame de Chatgpt: resultados a reutilizar](<{(ROOT / 'REEXAME_CHATGPT_20260912/RELATORIO_REAPROVEITAMENTO.md').as_posix()}>).
[DEV posterior, fora desta integração](<{(ROOT / 'RELATORIO_DOMINIO_GRAFICO_DEV.md').as_posix()}>):
dois módulos/10 alvos mostram D(S†S) como núcleo do gráfico de S no mesmo H_I.
Ainda sem revisão independente; não provam D(B)=D(S) e não entram nas contagens acima.

Original relido `{sha(original)}`; cópia `{sha(ROOT / 'um.py')}`;
{integration['embedded_files']} arquivos Lean incorporados. Original não executado
ou importado. Objetivo integral ainda incompleto.
'''
write(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — cópia integrada e revisão independente] R=(I+S†S)⁻¹ limitado,
injetivo, auto-adjunto e 0≤R≤I no mesmo H_I. A raiz positiva parcial B
satisfaz B²=S†S com igualdade dos domínios sucessivos. Energia S/B
provada em D(S†S); núcleo de B trivial, sem gap. Cinco módulos/30 alvos;
{len(build['records'])} registros incrementais rc0, {tests['passed']} controles,
{tests['axiom_report_entries']} declarações Audit, {integration['embedded_files']} arquivos embutidos.
Parecer DEV e parecer da integração lidos integralmente.

[OPEN] D(B)=D(S), polar/KMS e traço não foram pagos; Three Locks/H1,
H2/H3 físicos, setor quântico, certificado completo e runtime integral
continuam pendentes. Seis flags maiores falsas, gate legado inalterado,
original preservado. Objetivo integral ativo. O reexame de Chatgpt foi
registrado nesta sessão: reutilizar geometria, Einstein e subespaço padrão
já existentes; não confundir hipóteses físicas com implicações já provadas.

[Relatório](<{report_path.as_posix()}>).
[Parecer integrado](<{review.as_posix()}>).

[REAL — DEV separado, sem revisão/integração] RealGraphCore e
ScalarTomitaGraphCore compilam com 10 alvos: D(S†S) é núcleo do gráfico
de S no mesmo H_I. Isso fornece x_n→x e Sx_n→Sx para x_n∈D(S†S),
mas ainda não D(B)=D(S). Não entra nos 30 alvos/contagens integradas.
[Rascunho e histórico de falhas corrigidas](<{(ROOT / 'RELATORIO_DOMINIO_GRAFICO_DEV.md').as_posix()}>).
'''
surfaces = [Path(p) for p in parent['surface_sha256']]
for path in surfaces:
    raw = path.read_bytes()
    assert MARKER.encode() not in raw and sha(path) == parent['surface_sha256'][str(path)]
    newline = '\r\n' if b'\r\n' in raw else '\n'
    updated = raw + note.replace('\n', newline).encode('utf-8')
    write(path, updated, raw)
    assert path.read_bytes().startswith(raw) and len(updated) > len(raw)
artifacts = ['integration.json', 'integrated_compile.json', 'kernel_incremental_evidence.json',
    'gate_tests.json', 'gate_extension.py', 'integrate_v350.py', 'compile_integrated.py',
    'test_gate_extension.py', 'tomita_root_draft_status.json', 'RELATORIO_RAIZ_TOMITA_DEV.md',
    'record_tomita_root_progress.py', 'verify_tomita_root_custody.py',
    'REEXAME_CHATGPT_20260912/custody.json', 'REEXAME_CHATGPT_20260912/source_evidence.json',
    'REEXAME_CHATGPT_20260912/RELATORIO_REAPROVEITAMENTO.md',
    'graph_core_draft_status.json', 'RELATORIO_DOMINIO_GRAFICO_DEV.md']
custody = {'timestamp': DATE, 'previous_custody_path': str(parent_path),
    'previous_custody_sha256': sha(parent_path), 'mathematical_parent_custody_sha256': sha(square_path),
    'original_sha256': sha(original), 'working_sha256': sha(ROOT / 'um.py'),
    'previous_working_copy': str(prior), 'python_body_unchanged_from_previous_stage': True,
    'modules': modules, 'targets': targets, 'integrated_records': len(build['records']),
    'controls': tests['passed'], 'audit_declarations': tests['axiom_report_entries'],
    'surface_sha256': {str(p): sha(p) for p in surfaces}, 'backups': BACKUPS,
    'surface_before_sha256': {str(p): sha(Path(BACKUPS[str(p)])) for p in surfaces},
    'review_sha256': {str(p): sha(p) for p in [review, ROOT / 'revisao/REVIEW_SCALAR_TOMITA_ROOT.md']},
    'report_path': str(report_path), 'report_sha256': sha(report_path),
    'artifacts': {n: sha(ROOT / n) for n in artifacts},
    'remaining_flags': {k: evidence[k] for k in parent['remaining_flags']},
    'positive_root_square_exact': True, 'energy_on_square_domain': True,
    'root_domain_equals_Tomita_domain': False, 'polar_identified': False, 'KMS_proved': False,
    'canonical_trace_constructed': False, 'gate_changed': False, 'full_runtime': False,
    'full_goal_complete': False}
write(ROOT / 'tomita_root_custody.json', json.dumps(custody, ensure_ascii=False, indent=2).encode())
print(json.dumps({'custody': 'tomita_root_custody.json', 'surfaces': len(surfaces),
    'modules': len(modules), 'targets': len(targets), 'goal_complete': False}))
