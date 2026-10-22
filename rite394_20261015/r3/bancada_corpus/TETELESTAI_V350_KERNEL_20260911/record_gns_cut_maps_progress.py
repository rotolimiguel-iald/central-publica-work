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
MODULES = ['ScalarGNSCutMaps', 'ScalarGNSCutNorm']
MARKER = 'TETELESTAI_V350_GNS_CUT_MAPS_20260912'
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
review = ROOT / 'revisao/REVIEW_GNS_CUT_MAPS.md'
assert review.is_file() and review.stat().st_size > 500
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
previous = json.loads((ROOT / 'bounded_scalar_cuts_custody.json').read_bytes())
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

# Later development is pinned separately, never counted as reviewed integration.
development = {}
development_targets = 0
for name in ['ScalarCutVacuum', 'ScalarCutCyclicSpace', 'ScalarCutVectorFunctional', 'ScalarCutGNSProperties']:
    source = ROOT / 'kernel/TGLV350' / (name + '.lean')
    matches = []
    for log in (ROOT / 'logs').glob(name + '_*.json'):
        row = json.loads(log.read_bytes())
        if row['returncode'] == 0 and row['sha256'] == digest(source):
            matches.append((log, row))
    assert matches, name
    log, row = sorted(matches, key=lambda pair: pair[1]['timestamp'])[-1]
    assert row['source_unchanged_during_compile']
    assert digest(ROOT / 'build/TGLV350' / (name + '.olean')) == row['output_sha256']
    output = Path(row['stdout']).read_text(encoding='utf-8')
    names = re.findall(r'^#print axioms ([\w.]+)$', source.read_text(encoding='utf-8'), re.M)
    for name0 in names:
        full = 'TGLV350.Regular.' + name0
        m = re.search(re.escape("'" + full + "' depends on axioms:") + r'\s*\[([^\]]*)\]', output)
        assert m and {s.strip() for s in m.group(1).split(',')} <= {'propext', 'Classical.choice', 'Quot.sound'}
    development_targets += len(names)
    development[name] = {'source_sha256': digest(source), 'log': str(log),
                         'log_sha256': digest(log), 'output_sha256': row['output_sha256'],
                         'independently_reviewed': False, 'integrated': False}
assert development_targets == 26


report_path = ROOT / 'RELATORIO_MAPAS_GNS_DE_CORTE.md'
template = ROOT / 'MINUTA_MAPAS_GNS_DE_CORTE.md'
report_fields = dict(
    date=DATE, target_count=len(targets), build_count=len(build['records']),
    controls=tests['passed'], audit_count=tests['axiom_report_entries'],
    embedded_count=integration['embedded_files'], base_sha=integration['base_sha256'],
    working_sha=integration['working_sha256'], review_path=review.as_posix())
report = template.read_text(encoding='utf-8')
for key, value in report_fields.items():
    report = report.replace('{' + key + '}', str(value))
assert all('{' + key + '}' not in report for key in report_fields)
write_atomic(report_path, report.encode('utf-8'))
note = f"""

## {MARKER} — {DATE}

[REAL — Lean em cópia, revisão independente] T_R:H_I→L² ambiente é
contração complexo-linear, definida pelo indicador (-R,R]. Ela entrelaça
π_I e a mesma ρ ambiente. Para A∈I e R≥0, ‖T_RΛ(A)‖²=Re ψ_R(A*A),
com o fator Haar original. Todos os cortes naturais juntos distinguem
vetores, por interseção AE enumerável e exaustão da reta. Não se afirma
preservação de H_I ou fidelidade/injetividade individual dos cortes.
O campo geral do lema é fortemente contínuo e uniformemente limitado.
Dois módulos/{len(targets)} alvos; {len(build['records'])} registros Lean;
{tests['passed']} controles; {tests['axiom_report_entries']} declarações Audit;
{integration['embedded_files']} arquivos embutidos. Base `{integration['base_sha256']}`;
cópia `{integration['working_sha256']}`. AST Python fora do dicionário
Lean igual à etapa anterior, gate inalterado, seis flags maiores false.
[Relatório](<{report_path.as_posix()}>).
[Parecer independente](<{review.as_posix()}>).

[OPEN] Falta (0,y)∈fecho(G_Tomita)⇒T_n y=0, antes de usar injetividade
conjunta. Ponte apropriada com domínio escalar máximo (não presumir
I=n_ν), Tomita fechado, KMS, traço/escala dual, interfaces necessárias,
Three Locks/H1, H2/H3 físicos, setor interagente e certificado compatível
consumido pelo gate continuam abertos. Runtime integral pendente.
Original não executado/importado; inventário I/O histórico não o libera.
Turno anterior classificado como progresso: integração/custódia dos
funcionais efetivamente concluída. O objetivo integral permanece ativo.

[REAL — DEV posterior, sem revisão ou integração] Quatro módulos/26
declarações constroem Ω_R=√c·1_(-R,R]η e H_R=fecho(ρ(N)Ω_R), com
representação restrita, vetor cíclico e seminorma exata de ψ_R para R≥0.
T_R passa a ter contradomínio H_R, entrelaça π_I e π_R, tem imagem densa,
é contrativo e mantém injetividade conjunta natural. Não se afirma
sobrejetividade, fidelidade individual, vetor separante, normalidade de
π_R ou fechabilidade. R≤0 pode dar espaço zero. As tentativas rc1 foram
preservadas; só rc0 e pins finais compõem este registro DEV.
Não entram nas contagens e no parecer integrado acima.
[Rota](<{(ROOT / 'ROTA_GNS_CICLICO_DE_CORTE_RASCUNHO.md').as_posix()}>).
[Precisão de domínio e pesquisa](<{(ROOT / 'PESQUISA_FECHABILIDADE_PESOS_20260912.md').as_posix()}>).
"""
surfaces = [ROOT / name for name in (
    'MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'MEMORIA_DA_LINHAGEM.md',
    'DESENHO_DO_FECHAMENTO_QG.md', 'RESPOSTA_GATE_V350.md', 'TRACO_PROXIMAS_OBRIGACOES.md',
    'ROTA_APOS_CORTES_DUAIS.md', 'ROTA_VARIACIONAL_DO_RESOLVENTE.md',
    'RELATORIO_SUPORTE_E_OPERADOR_DUAL.md', 'RELATORIO_ENERGIA_E_RAIZ_DUAL.md',
    'RELATORIO_REPRESENTACAO_DA_FORMA_DUAL.md', 'RELATORIO_RESOLVENTE_FIXO_DUAL.md',
    'RELATORIO_AFILIACAO_DA_FORMA_FIXA.md', 'RELATORIO_PESO_FORMA_FIXA.md',
    'RELATORIO_IDEAL_SEMIFINITO.md', 'RELATORIO_VALORES_LIMITADOS.md',
    'RELATORIO_LOCALIDADE_FIXA.md', 'RELATORIO_FIBRA_CONSTANTE.md', 'RELATORIO_BASE_FIXA.md',
    'RELATORIO_PESO_ESCALAR_DUAL.md', 'RELATORIO_DOMINIO_MODULAR.md',
    'RELATORIO_REPRESENTACAO_GNS.md', 'RELATORIO_DOMINIO_INICIAL_TOMITA.md', 'RELATORIO_NORMALIDADE_GNS.md', 'RELATORIO_FUNCIONAIS_LIMITADOS.md')]
surfaces += [CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md']
for surface in surfaces:
    append(surface, note)
    assert MARKER.encode() in surface.read_bytes()
custody = {
    'timestamp': DATE, 'original_unchanged': True,
    'original_sha256': digest(ORIGINAL), 'working_sha256': digest(ROOT / 'um.py'),
    'previous_working_copy': str(prior_copy), 'python_body_unchanged_from_previous_stage': True,
    'modules': {name: digest(ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean')) for name in MODULES},
    'review_sha256': digest(review),
    'prior_bounded_scalar_cuts_review_sha256': digest(ROOT / 'revisao/REVIEW_BOUNDED_SCALAR_CUTS.md'), 'report_sha256': digest(report_path),
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
    'candidate_flow_invariance_proved': True,
    'dependent_regular_scalar_weight_certificate_constructed': True,
    'finite_star_core_constructed': True,
    'bounded_strong_star_approximation': True,
    'new_certificate_consumed_by_Python': False,
    'GNS_finite_ideal_completion_constructed': True,
    'GNS_finite_ideal_representation_faithful': True,
    'GNS_maximal_scalar_domain_identified': False,
    'bounded_scalar_positive_cuts_constructed': True,
    'scalar_weight_is_supremum_of_bounded_cuts': True,
    'bounded_cuts_monotone_convergence_criterion_proved': True,
    'bounded_cuts_GNS_intertwiners_constructed': True,
    'bounded_cuts_GNS_target': 'EXISTING_AMBIENT_L2',
    'bounded_cuts_GNS_norm_identity_proved': True,
    'bounded_cuts_GNS_joint_injectivity_proved': True,
    'bounded_cuts_cyclic_GNS_constructed': False,
    'GNS_representation_normality_proved': True,
    'GNS_normality_scope': 'POSITIVE_DIRECTED_INTERNAL_SUPREMA_TO_AMBIENT_SUPREMA',
    'GNS_general_predual_equivalence_proved': False,
    'GNS_star_domain_norm_dense': True,
    'Tomita_initial_graph_single_valued': True,
    'Tomita_initial_graph_swap_invariant': True,
    'Tomita_initial_domain_dense': True,
    'Tomita_graph_closure_single_valued': False,
    'Tomita_operator_constructed_for_scalar_weight': False,
    'KMS_proved': False,
    'operator_valued_weight_semifinite': False,
    'canonical_trace_constructed': False, 'full_goal_complete': False,
    'runtime_io_inventory_sha256': digest(ROOT / 'runtime_io_inventory.json'),
    'runtime_io_inventory_source_sha256': runtime_inventory['source_sha256'],
    'reviewed_template_sha256': digest(template),
    'post_scope_development': development,
    'post_scope_development_targets': development_targets,
    'post_scope_note_sha256': digest(ROOT / 'ROTA_GNS_CICLICO_DE_CORTE_RASCUNHO.md'),
    'domain_research_note_sha256': digest(ROOT / 'PESQUISA_FECHABILIDADE_PESOS_20260912.md'),
}
write_atomic(ROOT / 'gns_cut_maps_custody.json',
             json.dumps(custody, ensure_ascii=False, indent=2).encode())
print(json.dumps(custody, ensure_ascii=False))
