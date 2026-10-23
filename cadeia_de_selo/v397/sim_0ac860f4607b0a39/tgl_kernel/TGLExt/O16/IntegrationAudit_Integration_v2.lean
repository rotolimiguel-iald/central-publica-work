import Lean
import TGLExt.O16.TheEquationOfTruth_T20_v3
import TGLExt.O16.QubitScalarEntropy
import TGLExt.O16.IdempotentDephasing_v2
import TGLExt.O16.InfiniteLimitUniformControl_v2
import TGLExt.O16.ModularGeneratorControl
import TGLExt.O16.InscriptionBridge_Integration_v2
import TGLExt.O16.PenaltyThreeLocksBridge_v2
import TGLExt.O16.QubitEntropyDerivative_v3
import TGLExt.O16.FiniteGapRate_v2
import TGLExt.O16.OperatorContourBridge_v2_Integration_v2
import TGLExt.O16.TheEquationOfTruth_T20_controles_v3_Integration_v2
import TGLExt.O16.NegativeControlsCompleteness_v2_Integration_v2

-- All twelve sources coexist; no new theorem or physical identification.
#print axioms ORDEM016.EquationOfTruth.H_mul_proj
#print axioms ORDEM016.EquationOfTruth.IdempotentDephasing.exp_complement_idempotent
#print axioms ORDEM016.EquationOfTruth.IdempotentDephasing.exp_mul_of_eigenfactor
#print axioms ORDEM016.EquationOfTruth.InfiniteLimitControl.no_uniform_small_error
#print axioms ORDEM016.EquationOfTruth.InfiniteLimitControl.scalar_pointwise_limit
#print axioms ORDEM016.EquationOfTruth.InfiniteLimitControl.uniform_error_lower_bound
#print axioms ORDEM016.EquationOfTruth.ModularGeneratorControl.example_generator_nonzero
#print axioms ORDEM016.EquationOfTruth.ModularGeneratorControl.exists_normalized_nonzero_generator
#print axioms ORDEM016.EquationOfTruth.ModularGeneratorControl.modularGen_zero_iff_commute
#print axioms ORDEM016.EquationOfTruth.ModularGeneratorControl.rhoExample_posDef
#print axioms ORDEM016.EquationOfTruth.ModularGeneratorControl.rhoExample_trace
#print axioms ORDEM016.EquationOfTruth.ModularGeneratorControl.scalar_modularGen_zero
#print axioms ORDEM016.EquationOfTruth.NegativeControls.C1_1_oblique_algebra
#print axioms ORDEM016.EquationOfTruth.NegativeControls.C1_1_oblique_flow_fails
#print axioms ORDEM016.EquationOfTruth.NegativeControls.C1_2_kernel_selected
#print axioms ORDEM016.EquationOfTruth.NegativeControls.C1_2_nonsymmetric
#print axioms ORDEM016.EquationOfTruth.NegativeControls.C1_3a_indefinite_no_limit
#print axioms ORDEM016.EquationOfTruth.NegativeControls.C1_3b_product_conserved
#print axioms ORDEM016.EquationOfTruth.NegativeControls.C1_3b_reader_continuous
#print axioms ORDEM016.EquationOfTruth.NegativeControls.C1_3b_reader_not_factor
#print axioms ORDEM016.EquationOfTruth.NegativeControls.C1_4_not_continuous
#print axioms ORDEM016.EquationOfTruth.NegativeControls.C1_4_reader_conserved
#print axioms ORDEM016.EquationOfTruth.NegativeControls.C1_4_reader_not_factor
#print axioms ORDEM016.EquationOfTruth.NegativeControls.C1_5_constant_false_positive
#print axioms ORDEM016.EquationOfTruth.NegativeControls.C1_6_outside_bits
#print axioms ORDEM016.EquationOfTruth.NegativeControls.C1_7_bad_pruning
#print axioms ORDEM016.EquationOfTruth.NegativeControls.C1_8_signed_penalty
#print axioms ORDEM016.EquationOfTruth.NegativeControls.C1_9_invalid_qubit
#print axioms ORDEM016.EquationOfTruth.NegativeControls.constant_reader_always_conserved
#print axioms ORDEM016.EquationOfTruth.NegativeControls.diagonalFlow_eq
#print axioms ORDEM016.EquationOfTruth.NegativeControls.diagonalFlow_mulVec
#print axioms ORDEM016.EquationOfTruth.NegativeControls.fixedP_idempotent
#print axioms ORDEM016.EquationOfTruth.NegativeControls.fixedP_selects_kernel
#print axioms ORDEM016.EquationOfTruth.NegativeControls.indefinite_kernel_zero
#print axioms ORDEM016.EquationOfTruth.NegativeControls.invalidDensity_determinant
#print axioms ORDEM016.EquationOfTruth.NegativeControls.invalidDensity_not_positive
#print axioms ORDEM016.EquationOfTruth.NegativeControls.invalidDensity_trace_one
#print axioms ORDEM016.EquationOfTruth.NegativeControls.negative_unit_flow
#print axioms ORDEM016.EquationOfTruth.NegativeControls.negative_unit_kernel
#print axioms ORDEM016.EquationOfTruth.QubitScalar.asymptotic_argument_mem
#print axioms ORDEM016.EquationOfTruth.QubitScalar.deficit_antitoneOn
#print axioms ORDEM016.EquationOfTruth.QubitScalar.deficit_nonneg
#print axioms ORDEM016.EquationOfTruth.QubitScalar.deriv_entropy
#print axioms ORDEM016.EquationOfTruth.QubitScalar.entropy_abs_identity
#print axioms ORDEM016.EquationOfTruth.QubitScalar.entropy_argument_mem
#print axioms ORDEM016.EquationOfTruth.QubitScalar.entropy_le_diagonal
#print axioms ORDEM016.EquationOfTruth.QubitScalar.entropy_log_ratio
#print axioms ORDEM016.EquationOfTruth.QubitScalar.entropy_monotoneOn
#print axioms ORDEM016.EquationOfTruth.QubitScalar.entropy_strictMonoOn
#print axioms ORDEM016.EquationOfTruth.QubitScalar.hasDerivAt_entropy
#print axioms ORDEM016.EquationOfTruth.QubitScalar.hasDerivAt_radius
#print axioms ORDEM016.EquationOfTruth.QubitScalar.radicand_nonneg
#print axioms ORDEM016.EquationOfTruth.QubitScalar.radius_antitone
#print axioms ORDEM016.EquationOfTruth.QubitScalar.radius_lower_bound
#print axioms ORDEM016.EquationOfTruth.QubitScalar.radius_lt_one
#print axioms ORDEM016.EquationOfTruth.QubitScalar.radius_nonneg
#print axioms ORDEM016.EquationOfTruth.QubitScalar.radius_strictAnti
#print axioms ORDEM016.EquationOfTruth.T_add
#print axioms ORDEM016.EquationOfTruth.T_apply_eigen
#print axioms ORDEM016.EquationOfTruth.T_decomp
#print axioms ORDEM016.EquationOfTruth.T_fix_of_mem_ker
#print axioms ORDEM016.EquationOfTruth.apply_eq_apply_iff
#print axioms ORDEM016.EquationOfTruth.conserved_iff_factors
#print axioms ORDEM016.EquationOfTruth.conserved_iff_factors_T
#print axioms ORDEM016.EquationOfTruth.conserved_iff_factors_of_nonneg
#print axioms ORDEM016.EquationOfTruth.conserved_iff_factors_penalty
#print axioms ORDEM016.EquationOfTruth.diagonal_norm_bound
#print axioms ORDEM016.EquationOfTruth.distinguishing_reading_iff
#print axioms ORDEM016.EquationOfTruth.distinguishing_verdict_eq
#print axioms ORDEM016.EquationOfTruth.equation_criterion_can_fail
#print axioms ORDEM016.EquationOfTruth.equation_of_truth_is_not_static
#print axioms ORDEM016.EquationOfTruth.exp_apply_of_eigen
#print axioms ORDEM016.EquationOfTruth.exp_mul_eq_of_mul_eq_zero
#print axioms ORDEM016.EquationOfTruth.finite_gap_norm_rate
#print axioms ORDEM016.EquationOfTruth.flowTendsToFamily_of_finiteDimensional
#print axioms ORDEM016.EquationOfTruth.flow_derivative_ne_zero_at_zero
#print axioms ORDEM016.EquationOfTruth.flow_identity_of_kernel_top
#print axioms ORDEM016.EquationOfTruth.flow_mul_proj
#print axioms ORDEM016.EquationOfTruth.flow_preserves_inscription_form
#print axioms ORDEM016.EquationOfTruth.hasDerivAt_flow
#print axioms ORDEM016.EquationOfTruth.hasDerivAt_flow_apply
#print axioms ORDEM016.EquationOfTruth.hasDerivAt_profA
#print axioms ORDEM016.EquationOfTruth.hasDerivAt_profQ
#print axioms ORDEM016.EquationOfTruth.hasDerivAt_reading_T
#print axioms ORDEM016.EquationOfTruth.hasDerivAt_reading_flow
#print axioms ORDEM016.EquationOfTruth.inscription_form_survives
#print axioms ORDEM016.EquationOfTruth.isSelfAdjoint_penalty
#print axioms ORDEM016.EquationOfTruth.iterate_T_eq_nat_time
#print axioms ORDEM016.EquationOfTruth.ker_penalty
#print axioms ORDEM016.EquationOfTruth.ker_threeLocks
#print axioms ORDEM016.EquationOfTruth.mem_range_iff_fixed
#print axioms ORDEM016.EquationOfTruth.mul_exp_eq_of_mul_eq_zero
#print axioms ORDEM016.EquationOfTruth.name_verifies_T
#print axioms ORDEM016.EquationOfTruth.name_verifies_T_iterate
#print axioms ORDEM016.EquationOfTruth.operator_zero_of_kernel_top
#print axioms ORDEM016.EquationOfTruth.penalty_eq_kernel_H3L
#print axioms ORDEM016.EquationOfTruth.positive_time_changes_nonfixed_content
#print axioms ORDEM016.EquationOfTruth.pow_eq_self
#print axioms ORDEM016.EquationOfTruth.profA_deriv_zero
#print axioms ORDEM016.EquationOfTruth.profA_second_deriv_zero
#print axioms ORDEM016.EquationOfTruth.profA_zero
#print axioms ORDEM016.EquationOfTruth.profQ_deriv_zero
#print axioms ORDEM016.EquationOfTruth.profQ_zero
#print axioms ORDEM016.EquationOfTruth.proj_mul_H
#print axioms ORDEM016.EquationOfTruth.proj_mul_T
#print axioms ORDEM016.EquationOfTruth.proj_mul_flow
#print axioms ORDEM016.EquationOfTruth.re_inner_adjoint_mul_self
#print axioms ORDEM016.EquationOfTruth.re_inner_penalty
#print axioms ORDEM016.EquationOfTruth.reading_T
#print axioms ORDEM016.EquationOfTruth.reading_eigen_zero
#print axioms ORDEM016.EquationOfTruth.reading_eq_kernel_PF
#print axioms ORDEM016.EquationOfTruth.reading_zero_of_kernel_bot
#print axioms ORDEM016.EquationOfTruth.same_form_changed_name
#print axioms ORDEM016.EquationOfTruth.sampling_zero_conserves_every_reader
#print axioms ORDEM016.EquationOfTruth.selector_nonpos
#print axioms ORDEM016.EquationOfTruth.single_time_conserved_iff_factors
#print axioms ORDEM016.EquationOfTruth.starProjection_range_iff_fixed
#print axioms ORDEM016.EquationOfTruth.transportedInscription
#print axioms ORDEM016.EquationOfTruth.transported_name_eq_flow
#print axioms ORDEM016.EquationOfTruth.truthBit_bivalent
#print axioms ORDEM016.EquationOfTruth.truthBit_eq_one_iff
#print axioms ORDEM016.EquationOfTruth.truthBit_eq_zero_iff
#print axioms ORDEM016.EquationOfTruth.truthValue_table
#print axioms ORDEM016.EquationOfTruth.unit_operator_flow_real
#print axioms ORDEM016.EquationOfTruth.verdict_T
#print axioms ORDEM016.EquationOfTruth.verdict_eq_one_iff
#print axioms ORDEM016.EquationOfTruth.verdict_one_of_kernel_bot
#print axioms ORDEM016.EquationOfTruth.zero_operator_reading_real
#print axioms TGLExt.the_criterion_can_fail
#print axioms TGLExt.truth_is_not_static_equality


-- Engineering audit: all declarations introduced by this compilation unit.
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    let kind := match ci with
      | .axiomInfo _ => "axiom"
      | .thmInfo _ => "theorem"
      | .defnInfo _ => "definition"
      | _ => "generated_or_type"
    IO.println ("BENCH_DECL\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++
      String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    if kind == "axiom" then throwError "NEW_AXIOM_REFUSED: {n}"
