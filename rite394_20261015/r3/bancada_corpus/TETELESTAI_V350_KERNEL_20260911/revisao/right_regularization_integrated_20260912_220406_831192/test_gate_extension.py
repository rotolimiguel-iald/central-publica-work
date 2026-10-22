"""Exercise exact-type defenses and the actual isolated gate, without importing um.py."""
import ast
import copy
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
source = (ROOT / 'um.py').read_text(encoding='utf-8')
tree = ast.parse(source)
base_raw = (ROOT / 'fontes/um_v350_original.py').read_bytes()
base_tree = ast.parse(base_raw)
required_functions = {
    'verify_v350_modular_provenance', 'finalize_v350_modular_frontier',
    'v350_frontier_flag_has_proof', 'v350_gravity_flags_have_proof',
    'evaluate_v350_kernel_frontier', 'evaluate_quantum_gravity_closure',
    'prove_qg_closure_gate'}
required_constants = {'_V350_MODULAR_CONTRACTS', '_QG_CERTIFICATE_FLAGS', '_QG_PHYSICS_FLAGS'}
nodes = [n for n in tree.body if (
    isinstance(n, ast.FunctionDef) and n.name in required_functions) or (
    isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in required_constants
                                     for t in n.targets))]
namespace = {}
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(ROOT / 'um.py'), 'exec'), namespace)
compiled = json.loads((ROOT / 'integrated_compile.json').read_bytes())
assert compiled['incremental_build_ok'] is True
integration = json.loads((ROOT / 'integration.json').read_bytes())
assert len(compiled['records']) == len(integration['added_kernel_files']) + len(integration['updated_kernel_files'])
source_verified = all(hashlib.sha256(Path(r['source']).read_bytes()).hexdigest() == r['sha256']
                      and r['returncode'] == 0 for r in compiled['records'])
assert source_verified
for row in compiled['records']:
    output = ROOT / 'build' / Path(row['source']).relative_to(ROOT / 'kernel').with_suffix('.olean')
    assert hashlib.sha256(output.read_bytes()).hexdigest() == row['output_sha256']
dependencies = json.loads((ROOT / 'dependency_artifacts.json').read_bytes())
assert hashlib.sha256(base_raw).hexdigest() == dependencies['base_source_sha256']
changed_outputs = {str(Path(r['source']).relative_to(ROOT / 'kernel').with_suffix('.olean')).replace('\\', '/')
                   for r in compiled['records']}
dependencies_verified = all(
    rel in changed_outputs or hashlib.sha256((ROOT / 'build' / rel).read_bytes()).hexdigest() == row['sha256']
    for rel, row in dependencies['files'].items())
assert dependencies_verified
axioms = {}
audit_record = compiled['records'][-1]
assert audit_record['source'].endswith('Audit.lean')
audit_raw = Path(audit_record['stdout']).read_bytes()
audit_stream_sha256 = hashlib.sha256(audit_raw).hexdigest()
blob = audit_raw.decode('utf-8')
for name, body in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", blob, re.S):
    axioms[name] = [a.strip() for a in body.replace('\n', ' ').split(',') if a.strip()]
for name in re.findall(r"'([\w.']+)' does not depend on any axioms", blob):
    axioms.setdefault(name, [])
base_embedded = ast.literal_eval(next(n for n in base_tree.body if isinstance(n, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in n.targets)).value)
audit_targets = set(re.findall(r'^#print axioms ([\w.\']+)', base_embedded['TGL/Audit.lean'], re.M))
assert audit_targets <= axioms.keys(), sorted(audit_targets - axioms.keys())
assert all(set(values) <= {'propext', 'Classical.choice', 'Quot.sound'} for values in axioms.values())
baseline_document = json.loads((ROOT / 'fontes/um_absoluto.json').read_bytes())
baseline = baseline_document['core']['kernel_formalization']
kf = copy.deepcopy(baseline)
kf.update({'lake_build_ok': False, 'build_returncode': None,
           'incremental_build_ok': True, 'dependency_hashes_verified': True,
           'changed_source_hashes_verified': True, 'audit_returncode': 0,
           'all_verified': True, 'axiom_report': axioms,
           'verification_mode': compiled['mode'],
           'audit_stdout_sha256': audit_stream_sha256,
           'audit_capture_sha256_full': audit_stream_sha256,
           'audit_stdout_path': audit_record['stdout'],
           'audit_hash_scope': 'CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES',
           'historical_v350_audit_metadata': {key: baseline.get(key) for key in
               ('audit_stdout_sha256', 'audit_capture_sha256_full')},
           'full_monolithic_runtime_run': False})
finalize = namespace['finalize_v350_modular_frontier']
proofs = namespace['verify_v350_modular_provenance']
frontier = namespace['evaluate_v350_kernel_frontier']
assert all(proofs(kf).values())
finalize(kf)
checks = []


def check(name, value):
    assert value, name
    checks.append({'name': name, 'passed': True})


check('current_audit_hashes_match_current_raw_stream',
      kf['audit_stdout_sha256'] == kf['audit_capture_sha256_full'] ==
      hashlib.sha256(Path(kf['audit_stdout_path']).read_bytes()).hexdigest())
check('historical_v350_audit_hashes_preserved_as_history',
      kf['historical_v350_audit_metadata'] == {key: baseline.get(key) for key in
          ('audit_stdout_sha256', 'audit_capture_sha256_full')})
check('real_compiled_exact_type_bridges', all(proofs(kf).values()))
check('v350_baseline_does_not_inherit_new_proofs', not any(proofs(baseline).values()))
check('empty_inputs_fail_closed', not any(proofs({}).values()))
for control in ('all_verified', 'incremental_build_ok', 'dependency_hashes_verified',
                'changed_source_hashes_verified'):
    candidate = copy.deepcopy(kf)
    candidate[control] = False
    check('missing_' + control, not any(proofs(candidate).values()))
candidate = copy.deepcopy(kf)
candidate['audit_returncode'] = 1
check('audit_failure_with_valid_prints_is_rejected', not any(proofs(candidate).values()))
for flag, names in namespace['_V350_MODULAR_CONTRACTS'].items():
    for name in names:
        candidate = copy.deepcopy(kf)
        candidate['axiom_report'].pop(name)
        check('missing_declaration_' + name, not proofs(candidate)[flag])
    for bad_axioms in (['sorryAx'], ['Lean.trustCompiler'], ['Foreign.hiddenPremise'], 'propext'):
        candidate = copy.deepcopy(kf)
        candidate['axiom_report'][names[1]] = bad_axioms
        check('reject_' + flag + '_' + str(bad_axioms), not proofs(candidate)[flag])

old_evaluator = next(n for n in base_tree.body if isinstance(n, ast.FunctionDef)
                     and n.name == 'evaluate_quantum_gravity_closure')
new_evaluator = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                     and n.name == 'evaluate_quantum_gravity_closure')
check('legacy_evaluator_AST_unchanged', ast.dump(old_evaluator) == ast.dump(new_evaluator))
evaluate = namespace['evaluate_quantum_gravity_closure']
formal = {key: kf.get('qgc_' + key) is True for key in namespace['_QG_CERTIFICATE_FLAGS']}
physics = {key: kf.get('qgp_' + key) is True for key in namespace['_QG_PHYSICS_FLAGS']}
experiment = {key: True for key in ('independent_v3_profiles_unblinded',
    'independent_v3_survey_mocks_passed', 'independent_v3_systematics_passed',
    'independent_v3_powered_verdict_emitted')}
for key in formal:
    candidate = {**formal, key: False}
    check('drop_formal_' + key, not evaluate(candidate, physics, experiment)['mathematical_model_constructed'])
for key in physics:
    candidate = {**physics, key: False}
    check('drop_physics_' + key, not evaluate(formal, candidate, experiment)['physical_quantum_gravity_constructed'])
check('perfect_experiment_does_not_supply_kernel', not evaluate({}, physics, experiment)['mathematical_model_constructed'])
gate = namespace['prove_qg_closure_gate'](1, kf,
    independent_rite=baseline_document['core']['void_floor_v11'])
check('legacy_gate_reproduces_sealed_v350_inputs',
      gate['gate']['verdict'] == baseline_document['core']['qg_closure']['gate']['verdict'])
check('extension_consumed_by_actual_gate_function', gate['gate']['kernel_frontier'] == frontier(kf))
check('historical_probe_accepts_only_typed_modular_proof',
      namespace['v350_frontier_flag_has_proof'](kf, 'red_clause_JMJ_contains'))
candidate = copy.deepcopy(kf)
candidate['gpf_H1_internal_susy_relative_gap_discharged'] = True
check('invented_H1_is_rejected', not namespace['v350_gravity_flags_have_proof'](candidate))
check('modular_does_not_discharge_later_fronts', not frontier(kf)['full_plan_complete'])
check('normality_does_not_discharge_continuous_core',
      'TGLV350.Regular.regularCoreEmbedding_preserves_positive_directed_isLUB' in axioms
      and kf.get('qgf_continuous_modular_realization_constructed') is False)
check('zero_trace_countermodel_does_not_discharge_corner_or_full_witness',
      'TGLV350.ContractAudit.zeroTraceLegacyCore_has_no_threeLocks' in axioms
      and kf.get('qgf_unconditional_continuous_corner_proved') is False
      and kf.get('qgf_full_TGL_witness_constructed') is False)
check('extended_dual_integral_is_not_a_canonical_trace_certificate',
      'TGLV350.Regular.dualQuadraticIntegral_eq_iSup_cuts' in axioms
      and 'TGLV350.Regular.dualQuadraticIntegral_dual_invariant' in axioms
      and kf.get('qgf_continuous_modular_realization_constructed') is False)
check('infinite_unit_does_not_supply_a_finite_three_locks_corner',
      'TGLV350.Regular.dual_unit_cut_supremum_infinite' in axioms
      and kf.get('qgf_unconditional_continuous_corner_proved') is False
      and kf.get('gpf_H1_internal_susy_relative_gap_discharged') is False)
check('closed_form_affiliation_does_not_supply_canonical_trace',
      'TGLV350.Regular.dualAffiliatedPositiveForm' in axioms
      and 'TGLV350.Regular.dualQuadraticIntegral_lowerSemicontinuous' in axioms
      and kf.get('qgf_continuous_modular_realization_constructed') is False)
check('constructed_finite_domain_does_not_supply_semifinitude_or_three_locks',
      'TGLV350.Regular.dualClosedPositiveForm_one_domain' in axioms
      and 'TGLV350.Regular.dualClosedPositiveForm_zero_domain' in axioms
      and kf.get('qgf_unconditional_continuous_corner_proved') is False
      and kf.get('gpf_H1_internal_susy_relative_gap_discharged') is False)
check('bimodule_form_does_not_supply_a_base_valued_weight',
      'TGLV350.Regular.dualBaseConjugatedForm_value' in axioms
      and 'TGLV350.Regular.dualQuadraticIntegral_vector_dual_invariant' in axioms
      and kf.get('qgf_continuous_modular_realization_constructed') is False)
check('faithful_form_family_does_not_discharge_semifinite_trace_or_finite_corner',
      'TGLV350.Regular.dualQuadraticIntegral_faithful' in axioms
      and kf.get('qgf_continuous_modular_realization_constructed') is False
      and kf.get('qgf_unconditional_continuous_corner_proved') is False
      and kf.get('qgf_full_TGL_witness_constructed') is False)
check('normal_form_family_does_not_discharge_base_weight_trace_or_three_locks',
      'TGLV350.Regular.regularDualForm_preserves_internal_isLUB' in axioms
      and 'TGLV350.Regular.dualRealQuadratic_uniform_on_compact' in axioms
      and kf.get('qgf_continuous_modular_realization_constructed') is False
      and kf.get('qgf_unconditional_continuous_corner_proved') is False
      and kf.get('gpf_H1_internal_susy_relative_gap_discharged') is False
      and kf.get('qgf_full_TGL_witness_constructed') is False)
check('strong_resolvent_and_finite_range_do_not_supply_spectral_weight_or_trace',
      all('TGLV350.Regular.' + name in axioms for name in (
          'exists_dualResolvent_limit', 'dualResolvent_limit_energy_bound',
          'dualResolvent_limit_range_finite', 'dualResolvent_limit_one_eq_zero',
          'dualResolvent_limit_zero_eq_one'))
      and kf.get('qgf_continuous_modular_realization_constructed') is False
      and kf.get('qgf_unconditional_continuous_corner_proved') is False
      and kf.get('gpf_H1_internal_susy_relative_gap_discharged') is False
      and kf.get('qgf_full_TGL_witness_constructed') is False)
check('constructed_selfadjoint_support_operator_does_not_supply_weight_or_physics',
      all('TGLV350.Regular.' + name in axioms for name in (
          'dualResolvent_limit_minimizes_energy',
          'dualResolvent_kernel_eq_finiteDomain_orthogonal',
          'dualSupportOperator_selfadjoint', 'exists_dualSupportOperator'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
check('square_root_and_operator_domain_energy_do_not_supply_full_form_or_trace',
      all('TGLV350.Regular.' + name in axioms for name in (
          'dualSupportOperator_domain_finite', 'dualSupportOperator_energy_ennreal',
          'dualSupportSquareRoot_square', 'dualSupportSquareRoot_energy_on_operator_domain',
          'exists_dualSupportSquareRoot'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
check('full_form_representation_does_not_discharge_base_weight_trace_or_physical_hypotheses',
      all('TGLV350.Regular.' + name in axioms for name in (
          'dualSupportSquareRoot_domain_iff_finite', 'dualSupportSquareRoot_form_eq',
          'dualQuadraticIntegral_finite_iff_squareRoot_domain', 'exists_dualFormRepresentation'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
check('dual_fixed_resolvent_does_not_discharge_base_identification_weight_trace_or_physics',
      all('TGLV350.Regular.' + name in axioms for name in (
          'ClosedPositiveForm.minimizer_unique', 'dualResolvent_limit_dual_fixed',
          'dualFixedCore_mem_iff', 'amplified_factor_mem_dualFixedCore',
          'exists_dualFixedFormRepresentation'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
check('fixed_form_affiliation_including_infinity_does_not_supply_base_weight_trace_or_physics',
      all('TGLV350.Regular.' + name in axioms for name in (
          'dualSupportOperator_unitary_graph_iff', 'dualSupportSquareRoot_unitary_graph_iff',
          'dualQuadraticIntegral_unitary_commuting',
          'dualQuadraticIntegral_fixed_commutant_invariant', 'dualFixedAffiliatedPositiveForm'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
check('normal_faithful_fixed_weight_does_not_supply_semifinitude_trace_or_physics',
      all('TGLV350.Regular.' + name in axioms for name in (
          'AffiliatedPositiveForm.scale_laws', 'AffiliatedPositiveForm.add_mono',
          'dualFixedWeight_add', 'dualFixedWeight_scale', 'dualFixedWeight_bimodule',
          'dualFixedWeight_faithful', 'dualFixedWeight_preserves_internal_isLUB'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
check('finite_square_ideal_is_dense_but_does_not_discharge_trace_or_physics',
      all(name in axioms for name in (
          'TGLV350.Fourier.fourier_integral_ae_eq_L2',
          'TGLV350.Fourier.fourier_integral_lintegral_norm_sq',
          'TGLV350.Regular.regularAverage_dualQuadraticIntegral',
          'TGLV350.Regular.finiteDualLeftIdeal_left_mul',
          'TGLV350.Regular.finiteDualLeftIdeal_strong_approximation'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
check('bounded_values_in_fixed_algebra_do_not_discharge_base_trace_or_physics',
      all('TGLV350.Regular.' + name in axioms for name in (
          'dualQuadraticIntegral_eq_boundedCutLimit', 'boundedDualValue_unique',
          'boundedDualValue_dual_fixed', 'exists_boundedDualValue_in_fixedCore',
          'HasFiniteDualSquare.exists_bounded_value', 'regularAverage_bounded_value',
          'boundedFiniteSquares_strong_approximation'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
check('fixed_core_locality_does_not_discharge_base_trace_or_physics',
      all(name in axioms for name in (
          'TGLV350.Fourier.fourier_integral_ae_injective',
          'TGLV350.Regular.dualFixedCore_commutes_shift_and_character',
          'TGLV350.Regular.character_commutation_local_pairing',
          'TGLV350.Regular.character_commutation_measurableCut',
          'TGLV350.Regular.dualFixedCore_commutes_measurableCut'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
check('constant_fibre_identification_preserves_six_remaining_frontier_flags',
      all('TGLV350.Regular.' + name in axioms for name in (
          'unitIntervalProjection_eq_cut_shift_integral', 'commutation_fibreCandidate_read',
          'unitCut_mul_eq_zero_of_zero_read', 'eq_zero_of_shift_commutation_unitCut_zero',
          'eq_fibre_of_shift_character_commutation',
          'existsUnique_fibre_of_shift_character_commutation', 'dualFixedCore_eq_fibre_candidate'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
check('fixed_base_identification_preserves_trace_corner_and_physical_obligations',
      all('TGLV350.Regular.' + name in axioms for name in (
          'operatorFieldLift', 'operatorFieldLift_faithful',
          'operatorFieldLift_commutation_reflects', 'twistedCommutantLift_mem',
          'fibre_mem_regularCore_iff', 'dualFixedCore_fibreCandidate_mem',
          'dualFixedCore_eq_amplified_base', 'dualFixedCore_existsUnique_base'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
check('scalar_dual_weight_does_not_discharge_canonical_trace_or_physical_obligations',
      all('TGLV350.Regular.' + name in axioms for name in (
          'fixedBaseOrderIso', 'finiteBaseValues_strong_approximation',
          'dualQuadraticIntegral_vacuum_faithful', 'scalarDualWeight_add',
          'scalarDualWeight_scale', 'scalarDualWeight_faithful',
          'scalarDualWeight_normal', 'scalarDualWeight_square_finite_strong_density',
          'scalarDualWeight_bounded_base_value'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
check('modular_domain_and_invariance_do_not_discharge_KMS_trace_or_physical_obligations',
      all('TGLV350.Regular.' + name in axioms for name in (
          'scalarDualWeight_regular_invariant', 'regularScalarWeightCertificate',
          'contraction_adjoint_tendsto_identity', 'bounded_application_tendsto',
          'finiteDualStarCore', 'regularSandwich_norm_le',
          'finiteDualStarCore_strongStar_approximation', 'finiteDualStarCore_scalar_squares_finite'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
check('finite_ideal_GNS_representation_does_not_discharge_Tomita_KMS_trace',
      all('TGLV350.Regular.' + name in axioms for name in (
          'scalarGNSOrbit_norm_sq', 'scalarGNSLinear_injective',
          'operatorFieldLift_star', 'scalarGNSCompleteSpace',
          'scalarGNSAction_intertwines', 'scalarGNSEmbedding_denseRange',
          'scalarGNSRepresentation', 'scalarGNSRepresentation_injective'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
check("dense_initial_Tomita_graph_does_not_discharge_closed_Tomita_KMS_trace",
      all("TGLV350.Regular." + name in axioms for name in (
          "dualOrbit_tendsto_of_uniformly_bounded",
          "scalarGNSOrbit_leftRegularization_tendsto",
          "scalarGNSStarEmbedding_denseRange",
          "scalarTomitaGraph_single_valued",
          "scalarTomitaGraph_swap", "scalarTomitaGraph_domain_dense"))
      and all(kf.get(flag) is False for flag in (
          "qgf_continuous_modular_realization_constructed",
          "qgf_unconditional_continuous_corner_proved", "qgf_full_TGL_witness_constructed",
          "gpf_H1_internal_susy_relative_gap_discharged",
          "gpf_H2_smooth_modular_four_frame_discharged",
          "gpf_H3_local_horizon_equilibrium_discharged")))
check("GNS_order_normality_does_not_discharge_closed_Tomita_KMS_trace",
      all("TGLV350.Regular." + name in axioms for name in (
          "scalarGNSRepresentation_tendsto_of_uniformly_bounded",
          "scalarGNSRepresentation_nonneg", "scalarGNSRepresentation_monotone",
          "scalarGNSRepresentation_preserves_positive_isLUB",
          "scalarGNSRepresentation_preserves_positive_directed_isLUB"))
      and all(kf.get(flag) is False for flag in (
          "qgf_continuous_modular_realization_constructed",
          "qgf_unconditional_continuous_corner_proved", "qgf_full_TGL_witness_constructed",
          "gpf_H1_internal_susy_relative_gap_discharged",
          "gpf_H2_smooth_modular_four_frame_discharged",
          "gpf_H3_local_horizon_equilibrium_discharged")))
check("bounded_scalar_cuts_do_not_discharge_closed_Tomita_KMS_trace",
      all("TGLV350.Regular." + name in axioms for name in (
          "dualWeightCutCLM", "dualCutFunctional_nonneg",
          "scalarDualWeight_dominates_cut", "scalarDualWeight_eq_iSup_boundedCuts",
          "scalarCut_tendsto_internal_isLUB"))
      and all(kf.get(flag) is False for flag in (
          "qgf_continuous_modular_realization_constructed",
          "qgf_unconditional_continuous_corner_proved", "qgf_full_TGL_witness_constructed",
          "gpf_H1_internal_susy_relative_gap_discharged",
          "gpf_H2_smooth_modular_four_frame_discharged",
          "gpf_H3_local_horizon_equilibrium_discharged")))
check("GNS_cut_maps_do_not_discharge_closed_Tomita_KMS_trace",
      all("TGLV350.Regular." + name in axioms for name in (
          "scalarGNSCutMap", "scalarGNSCutMap_norm_le",
          "scalarGNSCutMap_intertwines", "scalarGNSCutMap_joint_zero",
          "scalarGNSCutMap_embedding_norm_sq"))
      and all(kf.get(flag) is False for flag in (
          "qgf_continuous_modular_realization_constructed",
          "qgf_unconditional_continuous_corner_proved", "qgf_full_TGL_witness_constructed",
          "gpf_H1_internal_susy_relative_gap_discharged",
          "gpf_H2_smooth_modular_four_frame_discharged",
          "gpf_H3_local_horizon_equilibrium_discharged")))
for stage, names in {
    'cyclic_cut_GNS': ('scalarCutRepresentation', 'scalarCutCyclicVector_functional',
                       'scalarGNSCutCyclicMap_denseRange', 'scalarGNSCutCyclicMap_joint_zero'),
    'Gaussian_closability': ('scalarGaussianGNSMap_injective', 'mem_dualOrbitVonNeumann_iff',
                             'scalarTomitaGraph_closure_vertical',
                             'scalarTomitaGraph_closure_single_valued'),
    'closed_Tomita_and_standard_subspace': ('scalarClosedTomita_graph_eq',
                                           'scalarClosedTomita_domain_dense',
                                           'scalarClosedTomita_involutive',
                                           'scalarTomitaStandardSubspace'),
    'maximal_antilinear_adjoint': ('scalarTomitaAdjoint_maximal',
                                  'scalarTomitaAdjoint_domain_dense',
                                  'scalarTomitaAdjoint_isClosed',
                                  'scalarTomitaAdjoint_involutive'),
    'positive_selfadjoint_Tomita_square': ('scalarTomitaSquare_domain_iff',
                                         'scalarTomitaSquare_quadratic',
                                         'scalarTomitaSquare_resolvent_surjective',
                                         'scalarTomitaSquare_selfadjoint',
                                         'scalarTomitaSquare_zero_only'),
    'bounded_Tomita_resolvent_and_exact_positive_root': (
        'scalarTomitaResolvent_equation', 'scalarTomitaResolvent_graph',
        'scalarTomitaPositiveRoot_selfadjoint', 'scalarTomitaPositiveRoot_square',
        'scalarTomitaPositiveRoot_energy_on_square_domain',
        'scalarTomitaPositiveRoot_zero_only'),
    'exact_root_domain_and_full_energy': (
        'scalarTomitaSquare_graph_core', 'scalarTomitaSquare_root_graph_core',
        'scalarTomitaPositiveRoot_domain_eq', 'scalarTomitaPositiveRoot_energy'),
    'same_GNS_polar_antiunitary_without_modular_promotion': (
        'scalarTomitaPositiveRoot_denseRange', 'scalarTomitaRootImage_denseRange',
        'scalarTomitaPolarFactor_factorization', 'scalarTomitaPolarFactor_surjective'),
    'same_GNS_resolvent_transport_without_weight_identification': (
        'scalarTomitaResolvent_flip', 'scalarTomitaPositiveRoot_resolvent_graph',
        'scalarTomitaPolarFactor_resolvent'),
    'same_GNS_polar_involution_without_KMS_promotion': (
        'antiunitaryConjugate_sqrt', 'scalarTomitaPolar_sqrt_resolvent',
        'scalarTomitaPolar_sqrt_complement', 'scalarTomitaPolarFactor_involutive'),
    'full_scalar_weight_GNS_completion_identification': (
        'scalarWeightOrbit_norm_sq', 'scalarWeight_completion_eq',
        'scalarWeightGNSAction_intertwines', 'scalarWeightGNSEmbedding_denseRange'),
    'full_scalar_weight_closed_Tomita_graph_identification': (
        'scalarWeightGNSEmbedding_sandwich_tendsto',
        'scalarWeightTomitaGraph_closure_eq', 'scalarClosedTomita_graph_eq_weight',
        'scalarClosedTomita_extends_weight_star'),
    'homogeneous_right_full_scalar_weight_domain': (
        'homogeneous_commutant_dual_intertwines', 'hasFiniteScalarSquare_iff_memLp',
        'scalarWeight_right_homogeneous_finite', 'scalarOrbit_right_matrixUnit'),
    'homogeneous_right_same_GNS_adjoint_pairing': (
        'homogeneousRightAmbient_preserves_GNS', 'homogeneousRightGNS_intertwines',
        'homogeneousRightGNS_adjoint', 'matrixUnit_scalarWeight_pairing'),
    'right_preserves_same_closed_Tomita_domain': (
        'homogeneousRightGraphMap_preserves_closed_graph', 'scalarRight_mem_closedTomitaDomain',
        'scalarClosedTomita_right_intertwines', 'matrixUnit_closedTomita_right_intertwines'),
    'left_preserves_same_maximal_Tomita_adjoint_domain': (
        'scalarRightTomitaAdjoint_pairing', 'scalarRightTomitaAdjoint_maximal',
        'scalarTomitaAdjoint_left_intertwines', 'matrixUnit_TomitaAdjoint_left_intertwines'),
    'same_square_full_domain_matrix_unit_right_scaling': (
        'scalarRight_mem_squareDomain', 'scalarTomitaSquare_right_intertwines',
        'matrixUnitRightGNS_star_reverse', 'matrixUnitRight_mem_squareDomain',
        'matrixUnit_TomitaSquare_right_scaling'),
    'same_square_regular_right_unitary_full_domain': (
        'regularRightGNS_unitary', 'regularRightGNS_intertwines',
        'scalarClosedTomita_regular_right_intertwines',
        'scalarTomitaAdjoint_regular_left_intertwines',
        'scalarTomitaSquare_regular_right_commutes', 'scalarRegularRight_squareDomain_iff'),
    'same_polar_regular_generator_and_strong_continuity': (
        'scalarTomitaResolvent_regular_right_commutes', 'scalarRegularRight_rootDomain_iff',
        'scalarTomitaPolarFactor_regular_right', 'regularRightGNS_commutes_left',
        'scalarTomitaPolar_regular_generator_commutes', 'regularRightGNS_strongly_continuous'),
    'same_polar_matrix_unit_root_scaling': (
        'positive_sqrt_intertwines', 'scaledResolventDenominator_positive',
        'resolvent_root_graph_scaled', 'matrixUnit_resolvent_right_scaling',
        'matrixUnit_positiveRoot_right_scaling', 'matrixUnit_polar_generator_commutes'),
    'same_polar_entire_base': (
        'levelExpectation_uniform_norm_bound', 'represented_levelExpectation_strong_tendsto',
        'localBase_polar_commutes', 'base_polar_commutes'),
    'same_polar_entire_core_inclusion': (
        'finiteSetEmbedding_reads_separate', 'fibre_generated_mem',
        'scalarGNS_commutation_from_generators', 'scalarTomitaPolar_core_commutant_mem'),
    'gaussian_unitary_and_same_GNS_cyclic_separating_vector': (
        'boundedInjectivePolar_intertwines', 'scalarGaussianImage_eq_orbit',
        'scalarGaussianUnitary_intertwines', 'scalarGNSCyclicVector_separating',
        'scalarGNSCyclicVector_cyclic'),
    'full_weight_right_regularization_and_commutant_approximation': (
        'scalarRightRegularization_embedding', 'scalarRightRegularization_tendsto',
        'scalarCommutant_rightBounded_approximation',
        'scalarCommutant_mem_generated_rightBounded'),
}.items():
    check(stage + '_does_not_discharge_KMS_trace_or_physical_frontier',
          all('TGLV350.Regular.' + name in axioms for name in names)
          and all(kf.get(flag) is False for flag in (
              'qgf_continuous_modular_realization_constructed',
              'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
              'gpf_H1_internal_susy_relative_gap_discharged',
              'gpf_H2_smooth_modular_four_frame_discharged',
              'gpf_H3_local_horizon_equilibrium_discharged'))
          and frontier(kf)['legacy_gate_changed'] is False
          and frontier(kf)['full_plan_complete'] is False)

report = {'checks': checks, 'passed': len(checks), 'axiom_report_entries': len(axioms),
          'verification_mode': compiled['mode'], 'full_monolithic_runtime_run': False,
          'working_um_sha256': hashlib.sha256((ROOT / 'um.py').read_bytes()).hexdigest(),
          'frontier': frontier(kf), 'legacy_gate': gate['gate']['verdict']}
for name, value in [('gate_tests.json', report), ('kernel_incremental_evidence.json', kf)]:
    target = ROOT / name
    if target.exists():
        before = target.read_bytes()
        backup = target.with_name(target.name + '.bak_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        backup.write_bytes(before)
        assert backup.read_bytes() == before
    temporary = target.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')
    assert temporary.stat().st_size > 0
    temporary.replace(target)
print(json.dumps({k: v for k, v in report.items() if k != 'checks'}, ensure_ascii=False))
