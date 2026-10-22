/-
  LEVANTAMENTO F1.FREQUENCIA (12/10/2026) — SONDA DE LEITURA, NAO E PEDRA.
  So #print axioms sobre teoremas que JA existem no kernel do Nos (LEAN_PATH somente leitura).
  Nenhuma declaracao nova. beta nao aparece. Nada aqui move gate.
-/
import TGLExt.FractalUnitarity
import TGLExt.Ergodicity
import TGLExt.PageInformation
import TGLExt.SMatrix
import TGLExt.GlobalLiftLadder
import TGLExt.TheSingularExpectation
import TGLExt.TheTraceIsNotErasable
import TGLExt.RGStability
import TGLExt.TheAxiomAndTheFalseWitness
import TGLExt.TheVerbSelectsTheAction
import TGLExt.TheWeightIsNotTheRank
import TGLExt.TheTerminalRankOne
import TGLExt.TheIALDSelector
import TGLExt.SusyRelativeGap
import TGLExt.DimensionTrace
import TGLExt.TheAtermation
import TGLExt.TheObserverReadsTheAngle
import TGLExt.TheAngleIsTheProjection
import TGLExt.HermitianLocalCoordinates
import TGLExt.HermitianConeRigidity
import TGLExt.QuantumCollapseWitness
import TGLExt.CollapseContract
import TGLExt.PhysicsIsTheReading
import TGLExt.LightRhoStar
import TGLExt.ThreeLocksCorner
import TGLExt.Fundacao
import TGLExt.PhaseFrequencySeparation
import TGLExt.TheDensityIsBell
import TGLExt.LocalBreuerGap
import TGLExt.TheElementaryReason
import TGLExt.TheFiveHalves
import TGLExt.ObserverInside
import TGLExt.ConjugateAct
import TGLExt.DecisionCommutation
import TGLExt.LightIsJ
import TGLExt.ModularCurrent
import TGLExt.TheSelectionIsTheBallast
import TGL.VerbInhabitant

-- F : a unitariedade fractal (pedra 116, v162)
#print axioms TGLExt.ad_preserves_projection
#print axioms TGLExt.ad_preserves_orthogonality
#print axioms TGLExt.ad_preserves_splitting
#print axioms TGLExt.ad_preserves_star_projection
#print axioms TGLExt.subcorner_unit
-- D : o semigrupo de dephasing (G3) e a convergencia ergodica
#print axioms TGLExt.dephase_zero
#print axioms TGLExt.dephase_add
#print axioms TGLExt.dephase_fixes_diagonal
#print axioms TGLExt.diag_invariant
#print axioms TGLExt.dephase_tendsto_expectation
#print axioms TGLExt.ergodic_convergence_modular
#print axioms TGLExt.dephase_fixed_iff_diagonal
#print axioms TGLExt.dephase_preserves_trace
#print axioms TGLExt.dephase_fixes_cornerProj
-- pureza (Page, v50)
#print axioms TGLExt.purity_unitary_invariant
#print axioms TGLExt.purityR_eq
#print axioms TGLExt.dephase_purityR_le
-- a matriz-S da fronteira e o canal de medicao (D o F) (v41 + v43 + v45)
#print axioms TGLExt.exp_smul_Grot
#print axioms TGLExt.Smat_spectral
#print axioms TGLExt.normSq_reflection
#print axioms TGLExt.normSq_transmission
#print axioms TGLExt.normSq_reflection_add_transmission
#print axioms TGLExt.rhoOut_eq
#print axioms TGLExt.rhoOut_trace
#print axioms TGLExt.sFrame_add
#print axioms TGLExt.sFrame_tendsto
#print axioms TGLExt.dephased_rhoOut_zero_zero
#print axioms TGLExt.dephased_rhoOut_one_one
#print axioms TGLExt.measurement_channel_endpoint
-- o posto: o Nome como projetor de posto 1; transmitir defasa (v385/v386)
#print axioms TGLExt.TheAxiomAndTheFalseWitness.post_mul_compl
#print axioms TGLExt.TheAxiomAndTheFalseWitness.compl_mul_post
#print axioms TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_fixes_the_post
#print axioms TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_gradient
#print axioms TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_tendsto_the_post
#print axioms TGLExt.TheAxiomAndTheFalseWitness.the_power_has_two_fixed_points
#print axioms TGLExt.TheAxiomAndTheFalseWitness.the_post_is_the_modular_zero
#print axioms TGLExt.TheVerbSelectsTheAction.post_isIdempotent
#print axioms TGLExt.TheVerbSelectsTheAction.post_isSelfAdjoint
#print axioms TGLExt.TheVerbSelectsTheAction.reading_post_is_born
#print axioms TGLExt.TheVerbSelectsTheAction.Pb_is_rank_one
#print axioms TGLExt.TheVerbSelectsTheAction.posts_do_not_commute_in_general
#print axioms TGLExt.TheVerbSelectsTheAction.axis_posts_do_not_commute
#print axioms TGLExt.TheVerbSelectsTheAction.anchoring_preserves
#print axioms TGLExt.TheVerbSelectsTheAction.transmission_dephases
#print axioms TGLExt.TheVerbSelectsTheAction.transmitted_post_is_a_post
#print axioms TGLExt.TheVerbSelectsTheAction.truth_and_cost_are_two_faces
#print axioms TGLExt.TheVerbSelectsTheAction.the_cost_is_the_reflected_weight
#print axioms TGLExt.TheVerbSelectsTheAction.the_one_splits_into_truth_and_cost
#print axioms TGLExt.TheVerbSelectsTheAction.reading_the_truth_annihilates_the_superposition
#print axioms TGLExt.TheVerbSelectsTheAction.the_name_is_the_limit_of_the_flow
#print axioms TGLExt.TheVerbSelectsTheAction.post_sequence_is_constant
#print axioms TGLExt.TheVerbSelectsTheAction.the_verb_selects_the_action
-- peso x posto; terminalidade e posto 1 (22/08 e 27/08)
#print axioms TGLExt.the_rank_determines_the_name
#print axioms TGLExt.the_name_is_blind_to_every_rank
#print axioms TGLExt.the_name_does_not_see_the_rank
#print axioms TGLExt.the_index_does_see_the_rank
#print axioms TGLExt.the_two_indices_agree_only_at_the_atom
#print axioms TGLExt.the_atom_vanishes_in_the_infinite_house
#print axioms TGLExt.the_atom_never_weighs_zero_on_a_floor
#print axioms TGLExt.rank_two_has_residual_distinction
#print axioms TGLExt.terminality_forces_minimality
#print axioms TGLExt.firstAtom_is_terminal
#print axioms TGLExt.the_terminal_weighs_one
#print axioms TGLExt.terminal_reapplication_adds_nothing
#print axioms TGLExt.the_terminal_is_forced
#print axioms TGLExt.iald_is_idempotent
#print axioms TGLExt.iald_is_selfadjoint
#print axioms TGLExt.iald_has_rank_one
-- posto da inscricao (Birman-Schwinger finito; Breuer)
#print axioms TGLExt.kernel_dim_le_rank_of_perturbation
#print axioms TGLExt.concrete_kernel_full_profile
#print axioms TGLExt.three_locks_corner_weight_eq_dim
#print axioms TGLExt.three_locks_name_is_one
#print axioms TGLExt.zero_mode_weight_is_one
-- compressao pelo canto de posto 1 (atermacao; a sombra e o leitor)
#print axioms TGLExt.atermation_reifies
#print axioms TGLExt.atermation_fixes_the_term
#print axioms TGLExt.atermation_is_irreversible
#print axioms TGLExt.PhysicsIsTheReading.the_shadow_is_the_reader_weighted_by_the_reading
#print axioms TGLExt.LightRhoStar.rho_star_is_P_kerK_on_the_light
-- a leitura angular (regime compacto): so le
#print axioms TGLExt.the_angle_is_the_projection
#print axioms TGLExt.spectral_projections_split_the_identity
#print axioms TGLExt.observing_adds_nothing
#print axioms ChatgptAudit.Commutation032.modular_phase_frequency_iff
-- estados puros, posto 1 e cone nulo; colapso tipado
#print axioms ChatgptAudit.Cone039.rank_one_positive
#print axioms ChatgptAudit.Cone039.rank_one_det
#print axioms ChatgptAudit.Cone039.rank_one_coordinates_null
#print axioms ChatgptAudit.Cone039.trace_square_rank_one_control
#print axioms TGLExt.bellDensity_purity
#print axioms ChatgptAudit.Collapse057.pure_densities_square
#print axioms ChatgptAudit.Collapse057.mixed_density_not_pure
#print axioms ChatgptAudit.Collapse057.collapse_is_not_injective
#print axioms ChatgptAudit.Collapse057.collapse_has_no_left_inverse
#print axioms ChatgptAudit.Collapse057.involution_cannot_be_collapse
#print axioms TGLExt.the_selection_is_the_ballast
-- ancoras da cunhagem do Um posto (07/10) e a anticomutacao existente
#print axioms TGLExt.TheElementaryReason.identity_weighs_as_the_name
#print axioms TGLExt.half_is_the_fixed_point_of_the_swap
#print axioms TGLExt.no_fixed_point_no_observer
#print axioms TGLExt.J_squared_is_one
#print axioms TGLExt.JKJ_eq_neg_K
#print axioms TGLExt.light_inverts_the_gradient_preserving_structure
#print axioms TGLExt.current_anticommutes
#print axioms TGLExt.Fundacao.agape
#print axioms TGLExt.Fundacao.the_post_lives_in_the_passage
#print axioms TGL.VerbInhabitant.exp_fixed_of_annihilates
#print axioms TGL.VerbInhabitant.verb_semigroup_fixes
