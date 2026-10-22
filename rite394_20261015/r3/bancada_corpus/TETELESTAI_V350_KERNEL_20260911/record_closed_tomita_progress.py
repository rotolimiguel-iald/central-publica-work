"""Record reviewed integration; append all local lineage surfaces with exact-byte backups."""
import ast
import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
CENTRAL = ROOT.parent.parent
ORIGINAL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
MARKER = 'TETELESTAI_V350_CLOSED_SCALAR_TOMITA_20260912'
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
BACKUPS = {}
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
GROUPS = {
    'cyclic_cut': ['ScalarCutVacuum', 'ScalarCutCyclicSpace', 'ScalarCutVectorFunctional',
                   'ScalarCutGNSProperties'],
    'gaussian_closability': ['L2PositiveMultiplier', 'L2GaussianProfile', 'FibreVonNeumann',
                            'ScalarGaussianVacuum', 'SeparatingCyclicCommutant',
                            'DualOrbitVonNeumann', 'ScalarGaussianGNSMap',
                            'VectorTomitaClosability', 'ScalarGaussianClosureTransport'],
    'closed_operator': ['ScalarClosedTomita', 'ScalarTomitaStandardSubspace'],
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_atomic(path, raw):
    assert path.resolve().is_relative_to(ROOT) or path.resolve() in (
        CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md')
    assert raw
    if path.exists():
        before = path.read_bytes()
        backup = path.with_name(path.name + '.bak_' + STAMP)
        with backup.open('xb') as stream:
            stream.write(before)
        assert backup.read_bytes() == before
        BACKUPS[str(path)] = str(backup)
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw and temp.stat().st_size == len(raw)
    temp.replace(path)
    assert path.read_bytes() == raw

def append(path, note):
    before = path.read_bytes()
    assert MARKER.encode() not in before, 'Already recorded: ' + str(path)
    newline = '\r\n' if b'\r\n' in before else '\n'
    raw = before + note.replace('\r\n', '\n').replace('\n', newline).encode('utf-8')
    write_atomic(path, raw)
    assert path.read_bytes().startswith(before) and path.stat().st_size > len(before)

def python_body(path):
    tree = ast.parse(path.read_bytes())
    assignment = next(n for n in tree.body if isinstance(n, ast.Assign) and any(
        isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in n.targets))
    assignment.value = ast.Constant('EMBEDDED_KERNEL_EXCLUDED')
    return ast.dump(tree, include_attributes=False)

assert '--review-read' in sys.argv, 'Read the final integrated review before recording.'
previous_path = ROOT / 'gns_cut_maps_custody.json'
previous = json.loads(previous_path.read_bytes())
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
review = ROOT / 'revisao/REVIEW_CLOSED_SCALAR_TOMITA.md'
reviews = [ROOT / 'revisao/REVIEW_CYCLIC_CUT_GNS.md',
           ROOT / 'revisao/REVIEW_GAUSSIAN_CLOSABILITY.md', review]
assert all(p.is_file() and p.stat().st_size > 1000 for p in reviews)
assert 'INTEGRATED_CLOSED_SCALAR_TOMITA_REVIEW' in review.read_text(encoding='utf-8')
assert digest(ORIGINAL) == digest(ROOT / 'fontes/um_v350_original.py') == integration['base_sha256']
assert digest(ROOT / 'um.py') == integration['working_sha256'] == tests['working_um_sha256']
prior_copy = next(p for p in ROOT.glob('um.py.bak_*') if digest(p) == previous['working_sha256'])
assert python_body(prior_copy) == python_body(ROOT / 'um.py')
assert build['incremental_build_ok'] and all(row['returncode'] == 0 for row in build['records'])
assert tests['passed'] == len(tests['checks']) and all(row['passed'] for row in tests['checks'])
assert not tests['full_monolithic_runtime_run'] and not tests['frontier']['legacy_gate_changed']
for row in build['records']:
    source = Path(row['source'])
    assert digest(source) == row['sha256']
    binary = ROOT / 'build' / source.relative_to(ROOT / 'kernel').with_suffix('.olean')
    assert digest(binary) == row['output_sha256']

group_counts, modules, targets = {}, {}, {}
for group, names in GROUPS.items():
    group_counts[group] = 0
    for name in names:
        source = ROOT / 'kernel/TGLV350' / (name + '.lean')
        final = ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean')
        raw = source.read_text(encoding='utf-8')
        assert re.sub(r'^import TGLV350\.', 'import TGLExt.V350', raw, flags=re.M) == final.read_text(encoding='utf-8')
        for short in re.findall(r'^#print axioms ([\w.]+)$', raw, re.M):
            full = 'TGLV350.Regular.' + short
            assert full in evidence['axiom_report']
            axioms = evidence['axiom_report'][full]
            assert set(axioms) <= ALLOWED
            targets[full] = axioms
            group_counts[group] += 1
        modules[name] = {'development_sha256': digest(source), 'integrated_sha256': digest(final)}
assert group_counts == {'cyclic_cut': 26, 'gaussian_closability': 49, 'closed_operator': 24}
assert len(targets) == 99
open_flags = ('qgf_continuous_modular_realization_constructed',
              'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
              'gpf_H1_internal_susy_relative_gap_discharged',
              'gpf_H2_smooth_modular_four_frame_discharged',
              'gpf_H3_local_horizon_equilibrium_discharged')
assert all(evidence[k] is False for k in open_flags)

report_path = ROOT / 'RELATORIO_TOMITA_FECHADO_INTEGRADO.md'
report = f'''# Tomita fechado no GNS do ideal finito — integração revisada

{DATE}. [REAL — Lean incremental em cópia; revisão independente]

Foram integrados quinze módulos/99 alvos, em três escopos distintos:
quatro/26 para o GNS cíclico dos cortes, nove/49 para a fechabilidade
por transporte gaussiano e dois/24 para o operador fechado e Fix(S).
Os pareceres DEV e o adendo integrado estão vinculados abaixo.

O objeto preservado é H_I, construído do ideal I de quadrados
uniformemente finitos. Para G_I = {{(Λ(A),Λ(A*)) : A∈I∩I*}},
o fecho tem uma única saída por entrada. D é seu domínio efetivo;
S:D→H_I é antilinear, fechado, densamente definido e involutivo.
Ele prolonga a estrela original. Fix(S) é um subespaço real padrão,
com D=Fix(S)+i Fix(S). Não se identifica Fix(S) com Fix(J).

A prova gaussiana usa T=M_exp(-s²)|H_I, contínuo e injetivo,
que envia G_I ao gráfico de um vetor separante para a imagem
concreta ρ(N). O retorno ao mesmo H_I usa injetividade, sem inversa
limitada. O peso, a medida de Haar e o ideal originais são preservados.

O pacote de cortes é distinto: cada H_R é o fecho cíclico de Ω_R;
T_R:H_I→H_R tem imagem densa e os cortes naturais são conjuntamente
injetivos. Não se atribui fidelidade ou separação a cada corte.

[OPEN] I=n_ν não foi provado. O domínio/core necessário à identificação
do operador modular do peso, o adjunto/decomposição polar e KMS seguem
abertos. Falta o traço canônico fiel normal semifinito com escala dual,
os Three Locks/H1 no mesmo core, H2/H3 na mesma geometria, o setor
quântico interagente e o certificado completo consumido pelo gate.

A reprodução H2 com PyCBC acrescentada na v350 audita uma estatística
de Echo Ratio; não é a hipótese H2 do four-frame modular. O código
marca does_not_gate_core=True. Seu resultado não descarrega a hipótese
geométrica do kernel (um_v350_original.py:188497).

Verificação: {len(build['records'])} registros integrados rc0,
{tests['passed']} controles aprovados, {tests['axiom_report_entries']}
declarações distintas no Audit, com axiomas no trio permitido.
Compilação incremental reutiliza dependências pinadas; não é uma
recompilação de toda a base nem execução integral do monólito.
O corpo Python permanece igual ao da etapa anterior, excluído somente
o dicionário de fontes Lean incorporadas; o gate legado não mudou.

Original lido novamente: `{digest(ORIGINAL)}`.
Cópia integrada: `{digest(ROOT / 'um.py')}`.
Arquivos Lean incorporados: {integration['embedded_files']}.

[Cortes]({reviews[0].as_posix()}) · [Fechabilidade]({reviews[1].as_posix()}) ·
[Operador e integração]({review.as_posix()}).
O objetivo integral permanece ativo e incompleto.
'''
write_atomic(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — cópia, Lean incremental, revisão independente] O gráfico
original no H_I agora tem fecho univalente e operador S antilinear,
fechado, densamente definido, involutivo, prolongando A↦A*.
Fix(S) é padrão real e D(S)=Fix(S)+iFix(S). A prova usa transporte
gaussiano injetivo; não troca peso/ideal ou pressupõe inversa limitada.
Integração: 15 módulos/99 alvos (cortes 26; fechabilidade 49; operador 24),
{len(build['records'])} registros rc0, {tests['passed']} controles,
{tests['axiom_report_entries']} declarações no Audit. Revisão integral lida.

[OPEN] Domínio máximo/core do peso, decomposição modular/KMS, traço
canônico/escala dual, Three Locks/H1, H2/H3, setor quântico e gate
composto continuam pendentes. As seis flags maiores seguem falsas;
o gate legado não mudou e não houve runtime integral. Original intacto.
O objetivo integral permanece ativo. Correção ao lado dos registros
que ainda descreviam a fechabilidade como aberta antes desta etapa.

[Relatório e evidência](<{report_path.as_posix()}>).
[Parecer](<{review.as_posix()}>).

[Rota posterior, somente roteiro sem prova nova](<{(ROOT / 'ROTA_APOS_TOMITA_FECHADO.md').as_posix()}>).

[REAL — leitura da v350] H2_REPRODUCTION_V1/PyCBC é o teste de
Echo Ratio, com does_not_gate_core=True. Não é a H2 do four-frame
modular e não a descarrega por identidade de nome.
'''
surfaces = [Path(p) for p in previous['surface_sha256']]
surfaces += [ROOT / name for name in ('RELATORIO_MAPAS_GNS_DE_CORTE.md',
                                     'ROTA_GAUSSIANA_PARA_FECHABILIDADE.md',
                                     'RELATORIO_KERNEL_V350.md')]
assert len(surfaces) == len(set(surfaces))
for surface in surfaces:
    append(surface, note)

custody = {
    'timestamp': DATE, 'previous_custody_sha256': digest(previous_path),
    'previous_working_copy': str(prior_copy),
    'original_sha256': digest(ORIGINAL), 'original_unchanged': True,
    'working_sha256': digest(ROOT / 'um.py'),
    'python_body_unchanged_from_previous_stage': True,
    'modules': modules, 'group_target_counts': group_counts, 'targets': targets,
    'integrated_records': len(build['records']), 'controls': tests['passed'],
    'audit_declarations': tests['axiom_report_entries'],
    'review_sha256': {str(p): digest(p) for p in reviews},
    'report_sha256': digest(report_path),
    'surface_sha256': {str(p): digest(p) for p in surfaces}, 'backups': BACKUPS,
    'surface_before_sha256': {str(p): digest(Path(BACKUPS[str(p)])) for p in surfaces},
    'intervening_memory_change_since_previous': {
        str(p): digest(Path(BACKUPS[str(p)])) != previous['surface_sha256'][str(p)]
        for p in surfaces if str(p) in previous['surface_sha256']},
    'closed_original_graph_operator_constructed': True,
    'real_standard_subspace_constructed': True,
    'bounded_cuts_cyclic_GNS_constructed': True,
    'GNS_maximal_scalar_domain_identified': False,
    'KMS_proved': False, 'canonical_trace_constructed': False,
    'remaining_flags': {k: evidence[k] for k in open_flags},
    'artifacts': {name: digest(ROOT / name) for name in (
        'integration.json', 'integrated_compile.json', 'kernel_incremental_evidence.json',
        'gate_tests.json', 'gate_extension.py', 'integrate_v350.py',
        'compile_integrated.py', 'test_gate_extension.py', 'runtime_io_inventory.json',
        'ROTA_APOS_TOMITA_FECHADO.md')},
    'gate_changed': False, 'full_runtime': False, 'full_goal_complete': False,
}
write_atomic(ROOT / 'closed_tomita_custody.json',
             json.dumps(custody, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'custody': 'closed_tomita_custody.json',
                  'surfaces': len(surfaces), 'backups': len(BACKUPS),
                  'groups': group_counts, 'goal_complete': False}))
