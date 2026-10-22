"""Record the reviewed adjoint/square integration with immediate byte backups."""
import ast
import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
CENTRAL = ROOT.parent.parent
ORIGINAL = Path(json.loads((ROOT / 'environment.json').read_bytes())['original_source'])
MARKER = 'TETELESTAI_V350_TOMITA_SQUARE_20260912'
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
BACKUPS = {}
GROUPS = {'adjoint': ['AntilinearAdjointGraph', 'ScalarTomitaAdjoint'],
          'composition': ['AntilinearComposition', 'ScalarTomitaSquare'],
          'resolvent': ['ClosedAntilinearResolvent', 'PositiveSurjectiveResolvent'],
          'selfadjoint': ['ScalarTomitaSelfAdjoint']}
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_atomic(path, raw, expected=None):
    assert path.resolve().is_relative_to(ROOT) or path.resolve() in (
        CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md')
    assert raw
    if path.exists():
        before = path.read_bytes()
        assert expected is None or before == expected, 'Concurrent edit: ' + str(path)
        backup = path.with_name(path.name + '.bak_' + STAMP)
        with backup.open('xb') as stream:
            stream.write(before)
        assert backup.read_bytes() == before
        BACKUPS[str(path)] = str(backup)
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw and temp.stat().st_size == len(raw)
    if expected is not None:
        assert path.read_bytes() == expected, 'Concurrent edit before replace: ' + str(path)
    temp.replace(path)
    assert path.read_bytes() == raw

def append(path, note):
    before = path.read_bytes()
    assert MARKER.encode() not in before, 'Already recorded: ' + str(path)
    newline = '\r\n' if b'\r\n' in before else '\n'
    raw = before + note.replace('\r\n', '\n').replace('\n', newline).encode('utf-8')
    write_atomic(path, raw, before)
    assert path.read_bytes().startswith(before) and path.stat().st_size > len(before)

def python_body(path):
    tree = ast.parse(path.read_bytes())
    assignment = next(n for n in tree.body if isinstance(n, ast.Assign) and any(
        isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in n.targets))
    assignment.value = ast.Constant('EMBEDDED_KERNEL_EXCLUDED')
    return ast.dump(tree, include_attributes=False)

assert '--review-read' in sys.argv
previous_path = ROOT / 'closed_tomita_custody.json'
previous = json.loads(previous_path.read_bytes())
draft = json.loads((ROOT / 'tomita_square_draft_status.json').read_bytes())
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
review = ROOT / 'revisao/REVIEW_SCALAR_TOMITA_ADJOINT.md'
assert 'INTEGRATED_TOMITA_SQUARE_REVIEW' in review.read_text(encoding='utf-8')
assert digest(ORIGINAL) == digest(ROOT / 'fontes/um_v350_original.py') == integration['base_sha256']
assert digest(ROOT / 'um.py') == integration['working_sha256'] == tests['working_um_sha256']
assert digest(previous_path) == draft['parent_custody_sha256']
prior_copy = next(p for p in ROOT.glob('um.py.bak_*') if digest(p) == previous['working_sha256'])
assert python_body(prior_copy) == python_body(ROOT / 'um.py')
assert build['incremental_build_ok'] and all(row['returncode'] == 0 for row in build['records'])
assert tests['passed'] == len(tests['checks']) and all(row['passed'] for row in tests['checks'])
assert not tests['full_monolithic_runtime_run'] and not tests['frontier']['legacy_gate_changed']
for row in build['records']:
    source = Path(row['source'])
    binary = ROOT / 'build' / source.relative_to(ROOT / 'kernel').with_suffix('.olean')
    assert digest(source) == row['sha256'] and digest(binary) == row['output_sha256']
groups, modules, targets = {}, {}, {}
for group, names in GROUPS.items():
    groups[group] = 0
    for name in names:
        source = ROOT / 'kernel/TGLV350' / (name + '.lean')
        final = ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean')
        raw = source.read_text(encoding='utf-8')
        assert digest(source) == draft['modules'][name]['source_sha256']
        assert re.sub(r'^import TGLV350\.', 'import TGLExt.V350', raw, flags=re.M) == final.read_text(encoding='utf-8')
        for short in re.findall(r'^#print axioms ([\w.]+)$', raw, re.M):
            full = 'TGLV350.Regular.' + short
            axioms = evidence['axiom_report'][full]
            assert set(axioms) <= ALLOWED and sorted(axioms) == draft['targets'][full]
            targets[full] = axioms
            groups[group] += 1
        modules[name] = {'development_sha256': digest(source), 'integrated_sha256': digest(final)}
assert groups == {'adjoint': 23, 'composition': 18, 'resolvent': 6, 'selfadjoint': 6}
assert len(targets) == 53
open_flags = tuple(previous['remaining_flags'])
assert len(open_flags) == 6 and all(evidence[k] is False for k in open_flags)
report_path = ROOT / 'RELATORIO_ADJUNTO_QUADRADO_INTEGRADO.md'
report = f'''# Adjunto máximo e S†S positivo auto-adjunto — integração revisada

{DATE}. [REAL — Lean incremental em cópia, com revisão independente]

O pacote contém sete módulos/53 declarações novas: adjunto máximo (23),
composição (18), resolvente (6) e aplicação da auto-adjunticidade (6).
O mesmo H_I, ideal I, gráfico inicial e operador S fechado são preservados.

O domínio de S† é exatamente o dos representantes do pareamento
<Sx,y>=<S†y,x> para todo x∈D(S). O adjunto é antilinear, máximo,
fechado, densamente definido e involutivo no domínio invariante.
A densidade usa os vetores T*BΩg, o comutante da imagem ρ(N) e a
injetividade gaussiana. Não é usada uma inversa limitada de T.

A=S†S tem domínio exato {{x∈D(S):Sx∈D(S†)}}. A identidade quadrática
Re<x,Ax>=||Sx||² dá positividade e o pareamento dá simetria.
A projeção sobre o gráfico REAL de S no produto de Hilbert produz,
para cada z, x com x+Ax=z. Essa sobrejetividade, junto com positividade
e simetria, prova domínio denso e auto-adjunticidade usando o adjunto
máximo da Mathlib. O operador composto é fechado e seu núcleo é trivial.

[OPEN] Núcleo trivial não fornece gap. Não foram identificados a raiz
positiva/decomposição polar modular ou KMS do peso ν, nem provado I=n_ν.
A ponte de domínio/núcleo adequada ao peso, o traço canônico fiel normal
semifinito e sua escala dual seguem pendentes. Three Locks/H1, H2/H3,
setor quântico interagente e certificado completo consumido pelo gate
também não foram descarregados.

Verificação: {len(build['records'])} registros integrados rc0 (com
reutilização de fontes/binários pinados), {tests['passed']} controles,
{tests['axiom_report_entries']} declarações distintas no Audit no trio
propext/Classical.choice/Quot.sound. Não é recompilação global da base
nem execução integral do monólito. As seis flags maiores continuam
falsas, o gate legado não mudou e o objetivo integral está incompleto.

Original relido: `{digest(ORIGINAL)}`.
Cópia integrada: `{digest(ROOT / 'um.py')}`.
Arquivos Lean incorporados: {integration['embedded_files']}.

[Prova e limites em detalhe](<{(ROOT / 'RELATORIO_ADJUNTO_QUADRADO_DEV.md').as_posix()}>).
[Parecer independente e escopo de recompilação](<{review.as_posix()}>).
[Rota posterior, sem prova nova](<{(ROOT / 'ROTA_POLAR_MESMO_GNS.md').as_posix()}>).
'''
write_atomic(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — cópia, Lean incremental, revisão independente] Construído o
adjunto antilinear máximo de S no mesmo H_I, com domínio denso,
gráfico fechado e involução. Construído A=S†S no domínio exato da
composição, positivo, auto-adjunto, densamente definido e fechado,
com núcleo trivial. A prova usa sobrejetividade de I+A obtida pela
projeção no gráfico REAL de S. Não pressupõe domínio total nem
inversa gaussiana limitada. Sete módulos/53 declarações novas.

Integração: {len(build['records'])} registros rc0, {tests['passed']}
controles, {tests['axiom_report_entries']} declarações distintas no Audit.
O corpo Python permaneceu igual ao anterior, exceto fontes Lean
incorporadas. Original intacto; seis flags maiores falsas; gate legado
inalterado; sem runtime integral. Objetivo integral ainda incompleto.

[OPEN] Núcleo trivial não é gap. Raiz/decomposição polar e identificação
modular/KMS do peso, ponte de domínio/núcleo necessária, traço/escala
dual, Three Locks/H1, H2/H3 e setor quântico seguem abertos. I=n_ν
não foi provado nem convertido em obrigação automática. Correção ao
lado dos registros históricos que ainda listavam adjunto e
auto-adjunticidade da composição como pendentes.

[Relatório](<{report_path.as_posix()}>).
[Parecer](<{review.as_posix()}>).
[Rota posterior, sem prova nova](<{(ROOT / 'ROTA_POLAR_MESMO_GNS.md').as_posix()}>).
'''
surfaces = [Path(p) for p in previous['surface_sha256']]
surfaces += [ROOT / 'RELATORIO_TOMITA_FECHADO_INTEGRADO.md', ROOT / 'ROTA_APOS_TOMITA_FECHADO.md']
assert len(surfaces) == len(set(surfaces))
for surface in surfaces:
    append(surface, note)
custody = {
    'timestamp': DATE, 'previous_custody_sha256': digest(previous_path),
    'previous_working_copy': str(prior_copy), 'original_sha256': digest(ORIGINAL),
    'original_unchanged': True, 'working_sha256': digest(ROOT / 'um.py'),
    'python_body_unchanged_from_previous_stage': True, 'modules': modules,
    'group_target_counts': groups, 'targets': targets,
    'integrated_records': len(build['records']), 'controls': tests['passed'],
    'audit_declarations': tests['axiom_report_entries'],
    'review_sha256': {str(review): digest(review)}, 'report_sha256': digest(report_path),
    'surface_sha256': {str(p): digest(p) for p in surfaces}, 'backups': BACKUPS,
    'surface_before_sha256': {str(p): digest(Path(BACKUPS[str(p)])) for p in surfaces},
    'intervening_memory_change_since_previous': {
        str(p): digest(Path(BACKUPS[str(p)])) != previous['surface_sha256'][str(p)]
        for p in surfaces if str(p) in previous['surface_sha256']},
    'maximal_antilinear_adjoint_constructed': True, 'square_positive_selfadjoint': True,
    'square_domain_exact_and_dense': True, 'square_kernel_trivial': True,
    'polar_identified': False, 'KMS_proved': False, 'canonical_trace_constructed': False,
    'remaining_flags': {k: evidence[k] for k in open_flags},
    'artifacts': {name: digest(ROOT / name) for name in (
        'integration.json', 'integrated_compile.json', 'kernel_incremental_evidence.json',
        'gate_tests.json', 'gate_extension.py', 'integrate_v350.py', 'compile_integrated.py',
        'test_gate_extension.py', 'runtime_io_inventory.json', 'tomita_square_draft_status.json',
        'RELATORIO_ADJUNTO_QUADRADO_DEV.md', 'record_tomita_square_progress.py',
        'verify_tomita_square_custody.py', 'ROTA_POLAR_MESMO_GNS.md')},
    'gate_changed': False, 'full_runtime': False, 'full_goal_complete': False}
write_atomic(ROOT / 'tomita_square_custody.json',
    json.dumps(custody, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'custody': 'tomita_square_custody.json', 'surfaces': len(surfaces),
                  'backups': len(BACKUPS), 'groups': groups, 'goal_complete': False}))
