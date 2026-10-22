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
MARKER = 'TETELESTAI_V350_TOMITA_INVOLUTION_INTEGRATED_20260912'
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
parent_path = ROOT / 'tomita_polar_custody.json'
parent = json.loads(parent_path.read_bytes())
memory_path = ROOT / 'tomita_involution_dev_memory_custody.json'
memory = json.loads(memory_path.read_bytes())
assert memory['parent_custody_sha256'] == sha(parent_path)
assert memory['working_sha256'] == parent['working_sha256']
draft_names = ['tomita_involution_draft_status.json']
drafts = [json.loads((ROOT / name).read_bytes()) for name in draft_names]
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
original = Path(json.loads((ROOT / 'environment.json').read_bytes())['original_source'])
review = ROOT / 'revisao/REVIEW_SCALAR_TOMITA_INVOLUTION_INTEGRATED.md'
assert 'INTEGRATED_TOMITA_INVOLUTION_REVIEW' in review.read_text(encoding='utf-8')
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
assert len(modules) == 4 and len(targets) == 19
assert all(evidence[k] is False for k in parent['remaining_flags'])
surfaces = [Path(p) for p in memory['surface_sha256']]
before_surfaces = {str(p): p.read_bytes() for p in surfaces}
for path in surfaces:
    assert MARKER.encode() not in before_surfaces[str(path)]
    assert sha(path) == memory['surface_sha256'][str(path)]
report_path = ROOT / 'RELATORIO_INVOLUCAO_POLAR_TOMITA_INTEGRADA.md'
report = f'''# Involução polar no H_I original — integração revisada

{DATE}. [REAL — quatro módulos/19 alvos integrados e revisados]

O fator U construído a partir do S fechado e da raiz B no mesmo H_I satisfaz
U²=I. Isso foi provado a partir de SR=(I−R)S em D(S), UR=(I−R)U, conjugação
positiva das raízes e S²=I sobre Ran √R densa. A prova de conjugação usa
antiunitariedade, sem assumir involução. A igualdade exata D(B)=D(S) e S=UB
do pacote anterior são consumidas. As quatro fontes e suas dezenove declarações
receberam revisão DEV e foram transportadas literalmente, exceto importações,
para TGLExt.V350; as raízes e o Audit da cópia foram compilados.

{len(build['records'])} registros incrementais rc0, {tests['passed']} controles,
{tests['axiom_report_entries']} declarações Audit, {integration['embedded_files']}
arquivos Lean embutidos. Os alvos novos usam apenas propext, Classical.choice e
Quot.sound. A execução reutilizou dependências anteriores com pins; não é um
rebuild global nem runtime integral. O corpo Python fora do embutido é idêntico
ao estágio polar anterior. Os testes verificam também que a nova involução não
descarrega indevidamente KMS, traço ou as hipóteses físicas do gate.

[OPEN] Identificar S com o domínio máximo do peso, realizar o fluxo modular/KMS,
construir o traço canônico com sua escala dual e o canto Three Locks no mesmo
modelo. Entregar H1/H2/H3 físicos compatíveis e consumi-los na ponte de Einstein
já existente. Completar o setor quântico interagente/BRST/QME e o certificado
integral consumido pelo gate. U²=I sozinho não fornece essas etapas nem identifica
U com qualquer outro objeto chamado J. O original permanece preservado; seis
flags maiores falsas, gate legado inalterado e objetivo integral ativo.

O ideal inicial I exige limite uniforme da forma em todos os vetores
(`HasFiniteDualSquare`); o domínio n_ν exige finitude do peso escalar. A rota
de identificação deve justificar o completamento e o núcleo do gráfico no
domínio máximo. Não se presume nem se impõe aqui igualdade literal I=n_ν.

[Prova DEV, domínios e falhas preservadas](<{(ROOT / 'RELATORIO_INVOLUCAO_POLAR_TOMITA_DEV.md').as_posix()}>).
[Revisão independente DEV](<{(ROOT / 'revisao/REVIEW_SCALAR_TOMITA_INVOLUTION.md').as_posix()}>).
[Revisão integrada](<{review.as_posix()}>).
[Reaproveitamento do acervo Chatgpt](<{(ROOT / 'REEXAME_CHATGPT_20260912/RELATORIO_REAPROVEITAMENTO.md').as_posix()}>).

Original relido `{sha(original)}`; cópia `{sha(ROOT / 'um.py')}`.
Mãe matemática `{sha(parent_path)}`; mãe de memória `{sha(memory_path)}`.
Os relatos anteriores de U²=I aberto e de DEV pendente permanecem históricos.
'''
write(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — integração revisada] U²=I foi agora integrado na cópia, no mesmo H_I e
para o mesmo fator de S=UB. Quatro módulos/19 alvos, com tipos e domínios exatos,
somente o trio lógico permitido. A troca do resolvente e das raízes positivas
usa a antiunitariedade de U; a involução é conclusão, não hipótese inserida.
Os registros anteriores, inclusive o DEV sem integração, permanecem históricos.

{len(build['records'])} registros incrementais rc0; {tests['passed']} controles;
{tests['axiom_report_entries']} declarações Audit; {integration['embedded_files']}
embutidos. Revisões DEV e integrada lidas. Dependências reutilizadas com pins,
sem runtime integral do monólito. Original preservado, gate legado inalterado.

[OPEN] Domínio máximo do peso/KMS, traço/canto Three Locks, H1/H2/H3 físicos
no mesmo modelo, setor quântico interagente e consumo pelo certificado completo.
Seis flags maiores falsas; objetivo integral ativo. Reutilizar os teoremas de
Einstein, métrica e gauge já localizados em Chatgpt, mantendo suas hipóteses.
O ideal inicial uniforme e o domínio escalar n_ν são condições distintas;
identificar completamento e núcleo do gráfico não pressupõe I=n_ν.

[Relatório](<{report_path.as_posix()}>).
[Revisão integrada](<{review.as_posix()}>).
'''
for path in surfaces:
    raw = before_surfaces[str(path)]
    newline = '\r\n' if b'\r\n' in raw else '\n'
    write(path, raw + note.replace('\n', newline).encode('utf-8'), raw)
artifact_names = ['integration.json', 'integrated_compile.json', 'kernel_incremental_evidence.json',
    'gate_tests.json', 'gate_extension.py', 'integrate_v350.py', 'compile_integrated.py',
    'test_gate_extension.py', 'RELATORIO_INVOLUCAO_POLAR_TOMITA_DEV.md',
    'record_tomita_involution_draft.py', 'record_tomita_involution_memory.py',
    'prepare_tomita_involution_stage.py', 'record_tomita_involution_progress.py',
    'verify_tomita_involution_custody.py', 'generate_tomita_involution_record_helpers.py',
    'tomita_involution_dev_memory_custody.json'] + draft_names
reviews = [review, ROOT / 'revisao/REVIEW_SCALAR_TOMITA_INVOLUTION.md']
custody = {'timestamp': DATE, 'previous_custody_path': str(parent_path),
    'previous_custody_sha256': sha(parent_path), 'original_sha256': sha(original),
    'previous_memory_custody_path': str(memory_path),
    'previous_memory_custody_sha256': sha(memory_path),
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
    'polar_involution_proved': True, 'modular_weight_identified': False,
    'KMS_proved': False, 'canonical_trace_constructed': False,
    'gate_changed': False, 'full_runtime': False, 'full_goal_complete': False}
write(ROOT / 'tomita_involution_custody.json', json.dumps(custody, ensure_ascii=False, indent=2).encode())
print(json.dumps({'custody': 'tomita_involution_custody.json', 'surfaces': len(surfaces),
    'modules': len(modules), 'targets': len(targets), 'goal_complete': False}))
