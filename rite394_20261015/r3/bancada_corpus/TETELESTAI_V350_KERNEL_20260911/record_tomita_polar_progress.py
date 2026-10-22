"""Record the reviewed exact-domain and polar integration, with byte backups and artifact pins."""
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
MARKER = 'TETELESTAI_V350_TOMITA_POLAR_INTEGRATED_20260912'
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
parent_path = ROOT / 'tomita_root_custody.json'
parent = json.loads(parent_path.read_bytes())
draft_names = ['tomita_root_domain_draft_status.json', 'tomita_polar_draft_status.json']
drafts = [json.loads((ROOT / name).read_bytes()) for name in draft_names]
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
original = Path(json.loads((ROOT / 'environment.json').read_bytes())['original_source'])
review = ROOT / 'revisao/REVIEW_SCALAR_TOMITA_POLAR_INTEGRATED.md'
assert 'INTEGRATED_TOMITA_POLAR_REVIEW' in review.read_text(encoding='utf-8')
assert sha(original) == sha(ROOT / 'fontes/um_v350_original.py') == integration['base_sha256']
assert sha(ROOT / 'um.py') == integration['working_sha256'] == tests['working_um_sha256']
assert all(d['integrated_working_sha256'] == parent['working_sha256'] for d in drafts)
assert all(d['parent_custody_sha256'] == sha(parent_path) for d in drafts)
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
for draft in drafts:
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
assert len(modules) == 9 and len(targets) == 41
assert all(evidence[k] is False for k in parent['remaining_flags'])
surfaces = [Path(p) for p in parent['surface_sha256']]
before_surfaces = {str(p): p.read_bytes() for p in surfaces}
for path in surfaces:
    assert MARKER.encode() not in before_surfaces[str(path)]
    assert sha(path) == parent['surface_sha256'][str(path)]
report_path = ROOT / 'RELATORIO_FATOR_POLAR_TOMITA_INTEGRADO.md'
report = f'''# Domínio exato e fator antiunitário de Tomita — integração revisada

{DATE}. [REAL — cópia integrada, compilação incremental e revisão independente]

No mesmo H_I, D(S†S) é núcleo de gráfico de S e da raiz positiva B.
A igualdade das normas no domínio comum, a completude e o fechamento dos dois
gráficos dão D(B)=D(S) e ‖Bx‖²=‖Sx‖² em todo esse domínio. A imagem de B é densa,
por auto-adjunção e núcleo zero. A regra U(Bx)=Sx estende-se a todo H_I como
isometria conjugado-linear; sua imagem fechada contém a imagem densa de S.
Logo U é antiunitário sobrejetivo e S=UB em todo D(S), no espaço original.

Nove módulos/41 alvos novos: seis/25 para domínio e três/16 para fator polar.
{len(build['records'])} registros rc0 de compilação incremental, {tests['passed']} controles,
{tests['axiom_report_entries']} declarações distintas no Audit ampliado e
{integration['embedded_files']} arquivos Lean incorporados. Todos os novos alvos
usam somente propext, Classical.choice e Quot.sound. Dependências anteriores
foram reutilizadas com pins; não houve rebuild global nem runtime integral.
O corpo Python fora das fontes Lean embutidas coincide com a etapa anterior.

[OPEN] U²=I e identificação como conjugação modular J, identificação com o
domínio máximo do peso e KMS, traço e escala dual, canto contínuo Three Locks,
H1/H2/H3 físicos no mesmo horizonte, setor quântico interagente, certificado
completo consumido pelo gate e runtime integral. A fatoração não afirma B
limitado, D(B)=H_I, invariância do domínio por B ou gap. As seis flags maiores
ficam falsas e o gate legado permanece inalterado. Objetivo integral ativo.

[Domínios e hipóteses](<{(ROOT / 'RELATORIO_DOMINIO_RAIZ_TOMITA_DEV.md').as_posix()}>).
[Fator polar e hipóteses](<{(ROOT / 'RELATORIO_FATOR_POLAR_TOMITA_DEV.md').as_posix()}>).
[Revisão DEV do domínio](<{(ROOT / 'revisao/REVIEW_SCALAR_TOMITA_DOMAIN.md').as_posix()}>).
[Revisão DEV polar](<{(ROOT / 'revisao/REVIEW_SCALAR_TOMITA_POLAR.md').as_posix()}>).
[Revisão integrada](<{review.as_posix()}>).
[Acervo Chatgpt já reaproveitável](<{(ROOT / 'REEXAME_CHATGPT_20260912/RELATORIO_REAPROVEITAMENTO.md').as_posix()}>).

[DEV posterior separado](<{(ROOT / 'RELATORIO_TROCA_RESOLVENTE_TOMITA_DEV.md').as_posix()}>):
dois módulos/quatro alvos provam SR=(I−R)S em D(S) e UR=(I−R)U em H_I.
Ainda sem revisão independente ou integração, fora dos nove/41. A troca das
raízes e U²=I permanecem abertas; a rota proposta está tipada no relatório DEV.

Original relido `{sha(original)}`; cópia `{sha(ROOT / 'um.py')}`;
mãe `{sha(parent_path)}`. Original não executado, importado ou modificado.
'''
write(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — integração revisada na cópia] A igualdade exata D(B)=D(S) e a energia
no domínio inteiro estão agora integradas; os registros anteriores em que
constavam abertas permanecem históricos. A regra U(Bx)=Sx fornece um fator
antiunitário no mesmo H_I e S=UB para todo x∈D(S). Nove módulos/41 alvos novos,
{len(build['records'])} registros incrementais rc0, {tests['passed']} controles,
{tests['axiom_report_entries']} declarações Audit e {integration['embedded_files']} arquivos Lean embutidos.
Revisões DEV e integrada lidas; original preservado; sem runtime do monólito.

[OPEN] Não foi provado U²=I nem feita a identificação modular/KMS do peso.
Traço/canto Three Locks, H1/H2/H3 físicos compatíveis, setor quântico interagente,
certificado completo consumido e runtime integral continuam pendentes.
Seis flags maiores falsas; gate legado inalterado; objetivo integral ativo.
O reexame de Chatgpt continua valendo: reutilizar geometria, Einstein, BRST
clássico e subespaço padrão existentes, preservando suas hipóteses e limites.

[Relatório e caminho crítico](<{report_path.as_posix()}>).
[Revisão integrada](<{review.as_posix()}>).

[REAL — DEV posterior separado, sem revisão/integração] Dois módulos/quatro
alvos compilados: SR=(I−R)S em D(S), UR=(I−R)U em H_I. Não demonstram ainda
a troca das raízes ou U²=I, nem integram os nove/41.
[Rota, evidência e tentativa corrigida](<{(ROOT / 'RELATORIO_TROCA_RESOLVENTE_TOMITA_DEV.md').as_posix()}>).
'''
for path in surfaces:
    raw = before_surfaces[str(path)]
    newline = '\r\n' if b'\r\n' in raw else '\n'
    write(path, raw + note.replace('\n', newline).encode('utf-8'), raw)
artifact_names = ['integration.json', 'integrated_compile.json', 'kernel_incremental_evidence.json',
    'gate_tests.json', 'gate_extension.py', 'integrate_v350.py', 'compile_integrated.py',
    'test_gate_extension.py', 'RELATORIO_DOMINIO_RAIZ_TOMITA_DEV.md',
    'RELATORIO_FATOR_POLAR_TOMITA_DEV.md', 'record_tomita_polar_draft.py',
    'prepare_tomita_polar_stage.py', 'record_tomita_polar_progress.py',
    'verify_tomita_polar_custody.py', 'test_polar_custody_binary_check.py',
    'polar_custody_binary_check.json', 'RELATORIO_TROCA_RESOLVENTE_TOMITA_DEV.md',
    'tomita_resolvent_flip_draft_status.json', 'record_tomita_resolvent_flip_draft.py'] + draft_names
reviews = [review, ROOT / 'revisao/REVIEW_SCALAR_TOMITA_DOMAIN.md',
    ROOT / 'revisao/REVIEW_SCALAR_TOMITA_POLAR.md']
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
    'polar_involution_proved': False, 'modular_weight_identified': False,
    'KMS_proved': False, 'canonical_trace_constructed': False,
    'gate_changed': False, 'full_runtime': False, 'full_goal_complete': False}
write(ROOT / 'tomita_polar_custody.json', json.dumps(custody, ensure_ascii=False, indent=2).encode())
print(json.dumps({'custody': 'tomita_polar_custody.json', 'surfaces': len(surfaces),
    'modules': len(modules), 'targets': len(targets), 'goal_complete': False}))
