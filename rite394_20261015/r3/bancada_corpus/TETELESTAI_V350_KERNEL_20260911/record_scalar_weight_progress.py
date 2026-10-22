"""Record the reviewed scalar dual weight with exact-byte memory backups."""
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
MODULES = ['FixedBaseEquivalence', 'BoundedBaseDualValues', 'ScalarDualWeightFaithfulness', 'ScalarDualWeight']
MARKER = 'TETELESTAI_V350_SCALAR_WEIGHT_20260912'
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
BACKUPS = {}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_atomic(path, raw):
    assert path.resolve().is_relative_to(ROOT) or path.resolve() in (
        CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md')
    before = path.read_bytes() if path.exists() else None
    if before == raw:
        return
    if before is not None:
        backup = path.with_name(path.name + '.bak_' + STAMP)
        with backup.open('xb') as handle:
            handle.write(before)
        assert backup.read_bytes() == before
        BACKUPS[str(path)] = str(backup)
    temporary = path.with_name(path.name + '.tmp_' + STAMP)
    with temporary.open('xb') as handle:
        handle.write(raw)
    assert temporary.stat().st_size == len(raw) > 0 and temporary.read_bytes() == raw
    temporary.replace(path)
    assert path.read_bytes() == raw


def append(path, text):
    before = path.read_bytes()
    assert MARKER.encode() not in before, 'Already recorded: ' + str(path)
    newline = '\r\n' if b'\r\n' in before else '\n'
    raw = before + text.replace('\r\n', '\n').replace('\n', newline).encode('utf-8')
    assert raw.startswith(before) and len(raw) > len(before)
    write_atomic(path, raw)


def python_body(raw):
    tree = ast.parse(raw)
    found = False
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in node.targets):
            node.value = ast.Constant(value='EMBEDDED_KERNEL_EXCLUDED')
            found = True
    assert found
    return ast.dump(tree, include_attributes=False)


assert '--review-read' in sys.argv, 'Read the completed review before recording.'
review = ROOT / 'revisao/REVIEW_SCALAR_DUAL_WEIGHT.md'
assert review.is_file() and review.stat().st_size > 500
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
previous = json.loads((ROOT / 'fixed_base_custody.json').read_bytes())
assert build['incremental_build_ok'] and tests['passed'] == len(tests['checks'])
assert all(row['passed'] for row in tests['checks'])
assert not tests['full_monolithic_runtime_run']
assert digest(ROOT / 'um.py') == tests['working_um_sha256'] == integration['working_sha256']
assert digest(ORIGINAL) == digest(ROOT / 'fontes/um_v350_original.py') == integration['base_sha256']
prior_copy = next((p for p in ROOT.glob('um.py.bak_*')
                   if digest(p) == previous['working_sha256']), None)
assert prior_copy is not None
assert python_body(prior_copy.read_bytes()) == python_body((ROOT / 'um.py').read_bytes())
new_sources = {'TGLExt/V350' + name + '.lean' for name in MODULES} | {'TGLExt.lean', 'TGL/Audit.lean'}
assert new_sources <= {Path(r['source']).relative_to(ROOT / 'kernel').as_posix()
                       for r in build['records']}
for row in build['records']:
    source = Path(row['source'])
    output = ROOT / 'build' / source.relative_to(ROOT / 'kernel').with_suffix('.olean')
    assert row['returncode'] == 0 and digest(source) == row['sha256']
    assert digest(output) == row['output_sha256']
    if source.relative_to(ROOT / 'kernel').as_posix() in new_sources:
        assert row.get('source_unchanged_during_compile') is True
targets = set()
for name in MODULES:
    content = (ROOT / 'kernel/TGLV350' / (name + '.lean')).read_text(encoding='utf-8')
    integrated = (ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean')).read_text(encoding='utf-8')
    assert re.sub(r'^import TGLV350\.', 'import TGLExt.V350', content, flags=re.M) == integrated
    namespace = 'TGLV350.Regular.'
    targets.update(namespace + target for target in
                   re.findall(r'^#print axioms ([\w.]+)$', content, re.M))
for target in targets:
    assert target in evidence['axiom_report']
    assert set(evidence['axiom_report'][target]) <= {'propext', 'Classical.choice', 'Quot.sound'}
open_flags = ('qgf_continuous_modular_realization_constructed',
              'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
              'gpf_H1_internal_susy_relative_gap_discharged',
              'gpf_H2_smooth_modular_four_frame_discharged',
              'gpf_H3_local_horizon_equilibrium_discharged')
assert all(evidence[flag] is False for flag in open_flags)
runtime_inventory = json.loads((ROOT / 'runtime_io_inventory.json').read_bytes())
assert runtime_inventory['source_sha256'] == previous['runtime_io_inventory_source_sha256']
assert digest(ROOT / 'runtime_io_inventory.json') == previous['runtime_io_inventory_sha256']
assert runtime_inventory['monolith_executed_or_imported'] is False
assert not runtime_inventory['parse_failures']


report_path = ROOT / 'RELATORIO_PESO_ESCALAR_DUAL.md'
template = ROOT / 'MINUTA_PESO_ESCALAR_DUAL.md'
report = template.read_text(encoding='utf-8').format(
    date=DATE, target_count=len(targets), build_count=len(build['records']),
    controls=tests['passed'], audit_count=tests['axiom_report_entries'],
    embedded_count=integration['embedded_files'], base_sha=integration['base_sha256'],
    working_sha=integration['working_sha256'], review_path=review.as_posix())
write_atomic(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — Lean em cópia] Peso escalar ν(A)=q_A(η), η=eΩ, no cone positivo
da mesma N: zero, aditividade, homogeneidade positiva, monotonia, fidelidade
e normalidade para supremos dirigidos internos. O ideal complexo esquerdo
de quadrados finitos já construído é fortemente denso e seus quadrados têm
ν finito. A prova de fidelidade usa η separante para F e Rη=η⇒R=I,
seguida da identidade de energia com finitude explícita.
A amplificação M→F está empacotada como equivalência de álgebras e ordem;
valores positivos limitados do peso estão em M e ν=f_Ω nesses valores.
Quatro módulos; {len(targets)} alvos novos; {len(build['records'])} registros Lean;
{tests['passed']} controles; {tests['axiom_report_entries']} declarações no Audit;
{integration['embedded_files']} arquivos embutidos. Base `{integration['base_sha256']}`;
cópia `{integration['working_sha256']}`. Corpo Python fora do dicionário Lean
inalterado por AST; gate legado inalterado.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

[OPEN] Grupo modular de ν/KMS, gerador afiliado, perturbação e traço
canônico com escala dual; correspondência geral espectral/predual e
interface padrão de peso operatorial; Three Locks/H1, H2/H3 físicos,
interações/BRST/QME/anomalias/UV, contrato ampliado e runtime integral.
ν não é promovido a traço. Seis flags maiores false. Inventário I/O histórico,
sem liberação do runtime atual. Objetivo ativo; original não importado/executado.
'''
surfaces = [ROOT / name for name in (
    'MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'MEMORIA_DA_LINHAGEM.md',
    'DESENHO_DO_FECHAMENTO_QG.md', 'RESPOSTA_GATE_V350.md', 'TRACO_PROXIMAS_OBRIGACOES.md',
    'ROTA_APOS_CORTES_DUAIS.md', 'ROTA_VARIACIONAL_DO_RESOLVENTE.md',
    'RELATORIO_SUPORTE_E_OPERADOR_DUAL.md', 'RELATORIO_ENERGIA_E_RAIZ_DUAL.md',
    'RELATORIO_REPRESENTACAO_DA_FORMA_DUAL.md', 'RELATORIO_RESOLVENTE_FIXO_DUAL.md',
    'RELATORIO_AFILIACAO_DA_FORMA_FIXA.md', 'RELATORIO_PESO_FORMA_FIXA.md',
    'RELATORIO_IDEAL_SEMIFINITO.md', 'RELATORIO_VALORES_LIMITADOS.md',
    'RELATORIO_LOCALIDADE_FIXA.md', 'RELATORIO_FIBRA_CONSTANTE.md', 'RELATORIO_BASE_FIXA.md')]
surfaces += [CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md']
for surface in surfaces:
    append(surface, note)
    assert MARKER.encode() in surface.read_bytes()
custody = {
    'timestamp': DATE, 'original_unchanged': True,
    'original_sha256': digest(ORIGINAL), 'working_sha256': digest(ROOT / 'um.py'),
    'previous_working_copy': str(prior_copy), 'python_body_unchanged_from_previous_stage': True,
    'modules': {name: digest(ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean')) for name in MODULES},
    'review_sha256': digest(review), 'report_sha256': digest(report_path),
    'surface_sha256': {str(p): digest(p) for p in surfaces}, 'backups': BACKUPS.copy(),
    'integrated_records': len(build['records']), 'controls': tests['passed'],
    'audit_declarations': tests['axiom_report_entries'], 'full_runtime': False,
    'finite_square_left_ideal_constructed': True,
    'finite_square_left_ideal_strong_approximation': True,
    'exact_regular_average_weight': True,
    'ordinary_fourier_agrees_with_L2_on_L1_L2': True,
    'finite_values_as_bounded_operators_in_F': True,
    'fixed_algebra_commutes_with_all_measurable_cuts': True,
    'fixed_algebra_commutes_with_ordinary_translations': True,
    'fixed_algebra_operators_are_constant_fibres': True,
    'constant_fibre_belongs_to_original_base': True,
    'ordered_affiliated_form_cone': True,
    'faithful_normal_fixed_form_weight': True,
    'bimodule_over_entire_fixed_algebra': True,
    'general_spectral_predual_correspondence': False,
    'fixed_algebra_identified_with_base': True,
    'fixed_base_algebra_and_order_equivalence': True,
    'bounded_positive_dual_values_in_original_base': True,
    'faithful_normal_scalar_dual_weight': True,
    'scalar_square_finite_left_ideal_strongly_dense': True,
    'scalar_weight_modular_group_identified': False,
    'operator_valued_weight_semifinite': False,
    'canonical_trace_constructed': False, 'full_goal_complete': False,
    'runtime_io_inventory_sha256': digest(ROOT / 'runtime_io_inventory.json'),
    'runtime_io_inventory_source_sha256': runtime_inventory['source_sha256'],
    'reviewed_template_sha256': digest(template),
}
write_atomic(ROOT / 'scalar_weight_custody.json',
             json.dumps(custody, ensure_ascii=False, indent=2).encode())
print(json.dumps(custody, ensure_ascii=False))
