import TheTimeHasNoRank
import TheTimeIsNotAPost

/-! Auditoria de TIPOS (auditor de REPRODUCAO da R2, independente do construtor): tipo da R1 == tipo da R2
    (defeq, nos dois sentidos) para toda declaracao mantida/renomeada; para os 4 reforcos (E5.09, E5.11, E5.12),
    o tipo da R1 e habitado a partir do termo da R2 (a R2 implica a R1). Sem sorry. -/

set_option autoImplicit false

noncomputable section
section Frobenius
open scoped Matrix.Norms.Frobenius Matrix.Norms.L2Operator

-- mantida: psiPlus -> psiPlus
example : type_of% @TGLExt.TheTimeHasNoRank.psiPlus := @TGLExt.TheTimeIsNotAPost.psiPlus
example : type_of% @TGLExt.TheTimeIsNotAPost.psiPlus := @TGLExt.TheTimeHasNoRank.psiPlus
#check @TGLExt.TheTimeHasNoRank.psiPlus
#check @TGLExt.TheTimeIsNotAPost.psiPlus

-- mantida: psiPlus_apply -> psiPlus_apply
example : type_of% @TGLExt.TheTimeHasNoRank.psiPlus_apply := @TGLExt.TheTimeIsNotAPost.psiPlus_apply
example : type_of% @TGLExt.TheTimeIsNotAPost.psiPlus_apply := @TGLExt.TheTimeHasNoRank.psiPlus_apply
#check @TGLExt.TheTimeHasNoRank.psiPlus_apply
#check @TGLExt.TheTimeIsNotAPost.psiPlus_apply

-- mantida: psiPlus_01_ne_zero -> psiPlus_01_ne_zero
example : type_of% @TGLExt.TheTimeHasNoRank.psiPlus_01_ne_zero := @TGLExt.TheTimeIsNotAPost.psiPlus_01_ne_zero
example : type_of% @TGLExt.TheTimeIsNotAPost.psiPlus_01_ne_zero := @TGLExt.TheTimeHasNoRank.psiPlus_01_ne_zero
#check @TGLExt.TheTimeHasNoRank.psiPlus_01_ne_zero
#check @TGLExt.TheTimeIsNotAPost.psiPlus_01_ne_zero

-- mantida: psiPlus_trace -> psiPlus_trace
example : type_of% @TGLExt.TheTimeHasNoRank.psiPlus_trace := @TGLExt.TheTimeIsNotAPost.psiPlus_trace
example : type_of% @TGLExt.TheTimeIsNotAPost.psiPlus_trace := @TGLExt.TheTimeHasNoRank.psiPlus_trace
#check @TGLExt.TheTimeHasNoRank.psiPlus_trace
#check @TGLExt.TheTimeIsNotAPost.psiPlus_trace

-- mantida: psiPlus_posSemidef -> psiPlus_posSemidef
example : type_of% @TGLExt.TheTimeHasNoRank.psiPlus_posSemidef := @TGLExt.TheTimeIsNotAPost.psiPlus_posSemidef
example : type_of% @TGLExt.TheTimeIsNotAPost.psiPlus_posSemidef := @TGLExt.TheTimeHasNoRank.psiPlus_posSemidef
#check @TGLExt.TheTimeHasNoRank.psiPlus_posSemidef
#check @TGLExt.TheTimeIsNotAPost.psiPlus_posSemidef

-- mantida: psiPlus_not_diagonal -> psiPlus_not_diagonal
example : type_of% @TGLExt.TheTimeHasNoRank.psiPlus_not_diagonal := @TGLExt.TheTimeIsNotAPost.psiPlus_not_diagonal
example : type_of% @TGLExt.TheTimeIsNotAPost.psiPlus_not_diagonal := @TGLExt.TheTimeHasNoRank.psiPlus_not_diagonal
#check @TGLExt.TheTimeHasNoRank.psiPlus_not_diagonal
#check @TGLExt.TheTimeIsNotAPost.psiPlus_not_diagonal

-- mantida: gRate -> gRate
example : type_of% @TGLExt.TheTimeHasNoRank.gRate := @TGLExt.TheTimeIsNotAPost.gRate
example : type_of% @TGLExt.TheTimeIsNotAPost.gRate := @TGLExt.TheTimeHasNoRank.gRate
#check @TGLExt.TheTimeHasNoRank.gRate
#check @TGLExt.TheTimeIsNotAPost.gRate

-- mantida: gRate_00 -> gRate_00
example : type_of% @TGLExt.TheTimeHasNoRank.gRate_00 := @TGLExt.TheTimeIsNotAPost.gRate_00
example : type_of% @TGLExt.TheTimeIsNotAPost.gRate_00 := @TGLExt.TheTimeHasNoRank.gRate_00
#check @TGLExt.TheTimeHasNoRank.gRate_00
#check @TGLExt.TheTimeIsNotAPost.gRate_00

-- mantida: gRate_01 -> gRate_01
example : type_of% @TGLExt.TheTimeHasNoRank.gRate_01 := @TGLExt.TheTimeIsNotAPost.gRate_01
example : type_of% @TGLExt.TheTimeIsNotAPost.gRate_01 := @TGLExt.TheTimeHasNoRank.gRate_01
#check @TGLExt.TheTimeHasNoRank.gRate_01
#check @TGLExt.TheTimeIsNotAPost.gRate_01

-- mantida: gRate_10 -> gRate_10
example : type_of% @TGLExt.TheTimeHasNoRank.gRate_10 := @TGLExt.TheTimeIsNotAPost.gRate_10
example : type_of% @TGLExt.TheTimeIsNotAPost.gRate_10 := @TGLExt.TheTimeHasNoRank.gRate_10
#check @TGLExt.TheTimeHasNoRank.gRate_10
#check @TGLExt.TheTimeIsNotAPost.gRate_10

-- mantida: gRate_11 -> gRate_11
example : type_of% @TGLExt.TheTimeHasNoRank.gRate_11 := @TGLExt.TheTimeIsNotAPost.gRate_11
example : type_of% @TGLExt.TheTimeIsNotAPost.gRate_11 := @TGLExt.TheTimeHasNoRank.gRate_11
#check @TGLExt.TheTimeHasNoRank.gRate_11
#check @TGLExt.TheTimeIsNotAPost.gRate_11

-- mantida: gRate_diag -> gRate_diag
example : type_of% @TGLExt.TheTimeHasNoRank.gRate_diag := @TGLExt.TheTimeIsNotAPost.gRate_diag
example : type_of% @TGLExt.TheTimeIsNotAPost.gRate_diag := @TGLExt.TheTimeHasNoRank.gRate_diag
#check @TGLExt.TheTimeHasNoRank.gRate_diag
#check @TGLExt.TheTimeIsNotAPost.gRate_diag

-- mantida: gRate_off -> gRate_off
example : type_of% @TGLExt.TheTimeHasNoRank.gRate_off := @TGLExt.TheTimeIsNotAPost.gRate_off
example : type_of% @TGLExt.TheTimeIsNotAPost.gRate_off := @TGLExt.TheTimeHasNoRank.gRate_off
#check @TGLExt.TheTimeHasNoRank.gRate_off
#check @TGLExt.TheTimeIsNotAPost.gRate_off

-- mantida: gRate_nonneg -> gRate_nonneg
example : type_of% @TGLExt.TheTimeHasNoRank.gRate_nonneg := @TGLExt.TheTimeIsNotAPost.gRate_nonneg
example : type_of% @TGLExt.TheTimeIsNotAPost.gRate_nonneg := @TGLExt.TheTimeHasNoRank.gRate_nonneg
#check @TGLExt.TheTimeHasNoRank.gRate_nonneg
#check @TGLExt.TheTimeIsNotAPost.gRate_nonneg

-- mantida: dephase_apply -> dephase_apply
example : type_of% @TGLExt.TheTimeHasNoRank.dephase_apply := @TGLExt.TheTimeIsNotAPost.dephase_apply
example : type_of% @TGLExt.TheTimeIsNotAPost.dephase_apply := @TGLExt.TheTimeHasNoRank.dephase_apply
#check @TGLExt.TheTimeHasNoRank.dephase_apply
#check @TGLExt.TheTimeIsNotAPost.dephase_apply

-- mantida: no_time_matrix -> no_time_matrix
example : type_of% @TGLExt.TheTimeHasNoRank.no_time_matrix := @TGLExt.TheTimeIsNotAPost.no_time_matrix
example : type_of% @TGLExt.TheTimeIsNotAPost.no_time_matrix := @TGLExt.TheTimeHasNoRank.no_time_matrix
#check @TGLExt.TheTimeHasNoRank.no_time_matrix
#check @TGLExt.TheTimeIsNotAPost.no_time_matrix

-- mantida: no_time_matrix_fin -> no_time_matrix_fin
example : type_of% @TGLExt.TheTimeHasNoRank.no_time_matrix_fin := @TGLExt.TheTimeIsNotAPost.no_time_matrix_fin
example : type_of% @TGLExt.TheTimeIsNotAPost.no_time_matrix_fin := @TGLExt.TheTimeHasNoRank.no_time_matrix_fin
#check @TGLExt.TheTimeHasNoRank.no_time_matrix_fin
#check @TGLExt.TheTimeIsNotAPost.no_time_matrix_fin

-- mantida: commutator_far_from_scalar -> commutator_far_from_scalar
example : type_of% @TGLExt.TheTimeHasNoRank.commutator_far_from_scalar := @TGLExt.TheTimeIsNotAPost.commutator_far_from_scalar
example : type_of% @TGLExt.TheTimeIsNotAPost.commutator_far_from_scalar := @TGLExt.TheTimeHasNoRank.commutator_far_from_scalar
#check @TGLExt.TheTimeHasNoRank.commutator_far_from_scalar
#check @TGLExt.TheTimeIsNotAPost.commutator_far_from_scalar

-- mantida: no_finite_spectral_translation -> no_finite_spectral_translation
example : type_of% @TGLExt.TheTimeHasNoRank.no_finite_spectral_translation := @TGLExt.TheTimeIsNotAPost.no_finite_spectral_translation
example : type_of% @TGLExt.TheTimeIsNotAPost.no_finite_spectral_translation := @TGLExt.TheTimeHasNoRank.no_finite_spectral_translation
#check @TGLExt.TheTimeHasNoRank.no_finite_spectral_translation
#check @TGLExt.TheTimeIsNotAPost.no_finite_spectral_translation

-- mantida: probe_commutator_far_from_scalar -> probe_commutator_far_from_scalar
example : type_of% @TGLExt.TheTimeHasNoRank.probe_commutator_far_from_scalar := @TGLExt.TheTimeIsNotAPost.probe_commutator_far_from_scalar
example : type_of% @TGLExt.TheTimeIsNotAPost.probe_commutator_far_from_scalar := @TGLExt.TheTimeHasNoRank.probe_commutator_far_from_scalar
#check @TGLExt.TheTimeHasNoRank.probe_commutator_far_from_scalar
#check @TGLExt.TheTimeIsNotAPost.probe_commutator_far_from_scalar

-- mantida: commutator_can_be_nonzero -> commutator_can_be_nonzero
example : type_of% @TGLExt.TheTimeHasNoRank.commutator_can_be_nonzero := @TGLExt.TheTimeIsNotAPost.commutator_can_be_nonzero
example : type_of% @TGLExt.TheTimeIsNotAPost.commutator_can_be_nonzero := @TGLExt.TheTimeHasNoRank.commutator_can_be_nonzero
#check @TGLExt.TheTimeHasNoRank.commutator_can_be_nonzero
#check @TGLExt.TheTimeIsNotAPost.commutator_can_be_nonzero

-- mantida: empty_dimension_admits_time -> empty_dimension_admits_time
example : type_of% @TGLExt.TheTimeHasNoRank.empty_dimension_admits_time := @TGLExt.TheTimeIsNotAPost.empty_dimension_admits_time
example : type_of% @TGLExt.TheTimeIsNotAPost.empty_dimension_admits_time := @TGLExt.TheTimeHasNoRank.empty_dimension_admits_time
#check @TGLExt.TheTimeHasNoRank.empty_dimension_admits_time
#check @TGLExt.TheTimeIsNotAPost.empty_dimension_admits_time

-- mantida: weyl_pair_lives_in_L2 -> weyl_pair_lives_in_L2
example : type_of% @TGLExt.TheTimeHasNoRank.weyl_pair_lives_in_L2 := @TGLExt.TheTimeIsNotAPost.weyl_pair_lives_in_L2
example : type_of% @TGLExt.TheTimeIsNotAPost.weyl_pair_lives_in_L2 := @TGLExt.TheTimeHasNoRank.weyl_pair_lives_in_L2
#check @TGLExt.TheTimeHasNoRank.weyl_pair_lives_in_L2
#check @TGLExt.TheTimeIsNotAPost.weyl_pair_lives_in_L2

-- mantida: no_bounded_spectral_translation -> no_bounded_spectral_translation
example : type_of% @TGLExt.TheTimeHasNoRank.no_bounded_spectral_translation := @TGLExt.TheTimeIsNotAPost.no_bounded_spectral_translation
example : type_of% @TGLExt.TheTimeIsNotAPost.no_bounded_spectral_translation := @TGLExt.TheTimeHasNoRank.no_bounded_spectral_translation
#check @TGLExt.TheTimeHasNoRank.no_bounded_spectral_translation
#check @TGLExt.TheTimeIsNotAPost.no_bounded_spectral_translation

-- mantida: probe_bounded_spectral_translation_complex -> probe_bounded_spectral_translation_complex
example : type_of% @TGLExt.TheTimeHasNoRank.probe_bounded_spectral_translation_complex := @TGLExt.TheTimeIsNotAPost.probe_bounded_spectral_translation_complex
example : type_of% @TGLExt.TheTimeIsNotAPost.probe_bounded_spectral_translation_complex := @TGLExt.TheTimeHasNoRank.probe_bounded_spectral_translation_complex
#check @TGLExt.TheTimeHasNoRank.probe_bounded_spectral_translation_complex
#check @TGLExt.TheTimeIsNotAPost.probe_bounded_spectral_translation_complex

-- renomeada: time_is_the_modular_flow -> modular_flow_is_a_kms_group
example : type_of% @TGLExt.TheTimeHasNoRank.time_is_the_modular_flow := @TGLExt.TheTimeIsNotAPost.modular_flow_is_a_kms_group
example : type_of% @TGLExt.TheTimeIsNotAPost.modular_flow_is_a_kms_group := @TGLExt.TheTimeHasNoRank.time_is_the_modular_flow
#check @TGLExt.TheTimeHasNoRank.time_is_the_modular_flow
#check @TGLExt.TheTimeIsNotAPost.modular_flow_is_a_kms_group

-- mantida: fixed_sector_is_the_centralizer -> fixed_sector_is_the_centralizer
example : type_of% @TGLExt.TheTimeHasNoRank.fixed_sector_is_the_centralizer := @TGLExt.TheTimeIsNotAPost.fixed_sector_is_the_centralizer
example : type_of% @TGLExt.TheTimeIsNotAPost.fixed_sector_is_the_centralizer := @TGLExt.TheTimeHasNoRank.fixed_sector_is_the_centralizer
#check @TGLExt.TheTimeHasNoRank.fixed_sector_is_the_centralizer
#check @TGLExt.TheTimeIsNotAPost.fixed_sector_is_the_centralizer

-- mantida: tracial_state_freezes_the_flow -> tracial_state_freezes_the_flow
example : type_of% @TGLExt.TheTimeHasNoRank.tracial_state_freezes_the_flow := @TGLExt.TheTimeIsNotAPost.tracial_state_freezes_the_flow
example : type_of% @TGLExt.TheTimeIsNotAPost.tracial_state_freezes_the_flow := @TGLExt.TheTimeHasNoRank.tracial_state_freezes_the_flow
#check @TGLExt.TheTimeHasNoRank.tracial_state_freezes_the_flow
#check @TGLExt.TheTimeIsNotAPost.tracial_state_freezes_the_flow

-- mantida: nontracial_state_rejects_the_identity_flow -> nontracial_state_rejects_the_identity_flow
example : type_of% @TGLExt.TheTimeHasNoRank.nontracial_state_rejects_the_identity_flow := @TGLExt.TheTimeIsNotAPost.nontracial_state_rejects_the_identity_flow
example : type_of% @TGLExt.TheTimeIsNotAPost.nontracial_state_rejects_the_identity_flow := @TGLExt.TheTimeHasNoRank.nontracial_state_rejects_the_identity_flow
#check @TGLExt.TheTimeHasNoRank.nontracial_state_rejects_the_identity_flow
#check @TGLExt.TheTimeIsNotAPost.nontracial_state_rejects_the_identity_flow

-- mantida: probe_rho_two_thirds_posDef -> probe_rho_two_thirds_posDef
example : type_of% @TGLExt.TheTimeHasNoRank.probe_rho_two_thirds_posDef := @TGLExt.TheTimeIsNotAPost.probe_rho_two_thirds_posDef
example : type_of% @TGLExt.TheTimeIsNotAPost.probe_rho_two_thirds_posDef := @TGLExt.TheTimeHasNoRank.probe_rho_two_thirds_posDef
#check @TGLExt.TheTimeHasNoRank.probe_rho_two_thirds_posDef
#check @TGLExt.TheTimeIsNotAPost.probe_rho_two_thirds_posDef

-- mantida: probe_rho_two_thirds_not_tracial -> probe_rho_two_thirds_not_tracial
example : type_of% @TGLExt.TheTimeHasNoRank.probe_rho_two_thirds_not_tracial := @TGLExt.TheTimeIsNotAPost.probe_rho_two_thirds_not_tracial
example : type_of% @TGLExt.TheTimeIsNotAPost.probe_rho_two_thirds_not_tracial := @TGLExt.TheTimeHasNoRank.probe_rho_two_thirds_not_tracial
#check @TGLExt.TheTimeHasNoRank.probe_rho_two_thirds_not_tracial
#check @TGLExt.TheTimeIsNotAPost.probe_rho_two_thirds_not_tracial

-- mantida: unitary_keeps_spectrum_and_purity -> unitary_keeps_spectrum_and_purity
example : type_of% @TGLExt.TheTimeHasNoRank.unitary_keeps_spectrum_and_purity := @TGLExt.TheTimeIsNotAPost.unitary_keeps_spectrum_and_purity
example : type_of% @TGLExt.TheTimeIsNotAPost.unitary_keeps_spectrum_and_purity := @TGLExt.TheTimeHasNoRank.unitary_keeps_spectrum_and_purity
#check @TGLExt.TheTimeHasNoRank.unitary_keeps_spectrum_and_purity
#check @TGLExt.TheTimeIsNotAPost.unitary_keeps_spectrum_and_purity

-- mantida: isometry_iterate' -> isometry_iterate'
example : type_of% @TGLExt.TheTimeHasNoRank.isometry_iterate' := @TGLExt.TheTimeIsNotAPost.isometry_iterate'
example : type_of% @TGLExt.TheTimeIsNotAPost.isometry_iterate' := @TGLExt.TheTimeHasNoRank.isometry_iterate'
#check @TGLExt.TheTimeHasNoRank.isometry_iterate'
#check @TGLExt.TheTimeIsNotAPost.isometry_iterate'

-- mantida: isometry_orbit_converges_only_if_fixed -> isometry_orbit_converges_only_if_fixed
example : type_of% @TGLExt.TheTimeHasNoRank.isometry_orbit_converges_only_if_fixed := @TGLExt.TheTimeIsNotAPost.isometry_orbit_converges_only_if_fixed
example : type_of% @TGLExt.TheTimeIsNotAPost.isometry_orbit_converges_only_if_fixed := @TGLExt.TheTimeHasNoRank.isometry_orbit_converges_only_if_fixed
#check @TGLExt.TheTimeHasNoRank.isometry_orbit_converges_only_if_fixed
#check @TGLExt.TheTimeIsNotAPost.isometry_orbit_converges_only_if_fixed

-- mantida: isometric_flow_converges_only_if_fixed -> isometric_flow_converges_only_if_fixed
example : type_of% @TGLExt.TheTimeHasNoRank.isometric_flow_converges_only_if_fixed := @TGLExt.TheTimeIsNotAPost.isometric_flow_converges_only_if_fixed
example : type_of% @TGLExt.TheTimeIsNotAPost.isometric_flow_converges_only_if_fixed := @TGLExt.TheTimeHasNoRank.isometric_flow_converges_only_if_fixed
#check @TGLExt.TheTimeHasNoRank.isometric_flow_converges_only_if_fixed
#check @TGLExt.TheTimeIsNotAPost.isometric_flow_converges_only_if_fixed

-- mantida: rotation_isometry -> rotation_isometry
example : type_of% @TGLExt.TheTimeHasNoRank.rotation_isometry := @TGLExt.TheTimeIsNotAPost.rotation_isometry
example : type_of% @TGLExt.TheTimeIsNotAPost.rotation_isometry := @TGLExt.TheTimeHasNoRank.rotation_isometry
#check @TGLExt.TheTimeHasNoRank.rotation_isometry
#check @TGLExt.TheTimeIsNotAPost.rotation_isometry

-- mantida: probe_rotation_orbit_has_no_limit -> probe_rotation_orbit_has_no_limit
example : type_of% @TGLExt.TheTimeHasNoRank.probe_rotation_orbit_has_no_limit := @TGLExt.TheTimeIsNotAPost.probe_rotation_orbit_has_no_limit
example : type_of% @TGLExt.TheTimeIsNotAPost.probe_rotation_orbit_has_no_limit := @TGLExt.TheTimeHasNoRank.probe_rotation_orbit_has_no_limit
#check @TGLExt.TheTimeHasNoRank.probe_rotation_orbit_has_no_limit
#check @TGLExt.TheTimeIsNotAPost.probe_rotation_orbit_has_no_limit

-- mantida: frobenius_norm_eq_purityR -> frobenius_norm_eq_purityR
example : type_of% @TGLExt.TheTimeHasNoRank.frobenius_norm_eq_purityR := @TGLExt.TheTimeIsNotAPost.frobenius_norm_eq_purityR
example : type_of% @TGLExt.TheTimeIsNotAPost.frobenius_norm_eq_purityR := @TGLExt.TheTimeHasNoRank.frobenius_norm_eq_purityR
#check @TGLExt.TheTimeHasNoRank.frobenius_norm_eq_purityR
#check @TGLExt.TheTimeIsNotAPost.frobenius_norm_eq_purityR

-- mantida: unitary_conj_isometry -> unitary_conj_isometry
example : type_of% @TGLExt.TheTimeHasNoRank.unitary_conj_isometry := @TGLExt.TheTimeIsNotAPost.unitary_conj_isometry
example : type_of% @TGLExt.TheTimeIsNotAPost.unitary_conj_isometry := @TGLExt.TheTimeHasNoRank.unitary_conj_isometry
#check @TGLExt.TheTimeHasNoRank.unitary_conj_isometry
#check @TGLExt.TheTimeIsNotAPost.unitary_conj_isometry

-- mantida: modular_flow_is_isometry -> modular_flow_is_isometry
example : type_of% @TGLExt.TheTimeHasNoRank.modular_flow_is_isometry := @TGLExt.TheTimeIsNotAPost.modular_flow_is_isometry
example : type_of% @TGLExt.TheTimeIsNotAPost.modular_flow_is_isometry := @TGLExt.TheTimeHasNoRank.modular_flow_is_isometry
#check @TGLExt.TheTimeHasNoRank.modular_flow_is_isometry
#check @TGLExt.TheTimeIsNotAPost.modular_flow_is_isometry

-- mantida: modular_orbit_converges_iff_diagonal -> modular_orbit_converges_iff_diagonal
example : type_of% @TGLExt.TheTimeHasNoRank.modular_orbit_converges_iff_diagonal := @TGLExt.TheTimeIsNotAPost.modular_orbit_converges_iff_diagonal
example : type_of% @TGLExt.TheTimeIsNotAPost.modular_orbit_converges_iff_diagonal := @TGLExt.TheTimeHasNoRank.modular_orbit_converges_iff_diagonal
#check @TGLExt.TheTimeHasNoRank.modular_orbit_converges_iff_diagonal
#check @TGLExt.TheTimeIsNotAPost.modular_orbit_converges_iff_diagonal

-- mantida: modular_orbit_converges_iff_diagonal_entrywise -> modular_orbit_converges_iff_diagonal_entrywise
example : type_of% @TGLExt.TheTimeHasNoRank.modular_orbit_converges_iff_diagonal_entrywise := @TGLExt.TheTimeIsNotAPost.modular_orbit_converges_iff_diagonal_entrywise
example : type_of% @TGLExt.TheTimeIsNotAPost.modular_orbit_converges_iff_diagonal_entrywise := @TGLExt.TheTimeHasNoRank.modular_orbit_converges_iff_diagonal_entrywise
#check @TGLExt.TheTimeHasNoRank.modular_orbit_converges_iff_diagonal_entrywise
#check @TGLExt.TheTimeIsNotAPost.modular_orbit_converges_iff_diagonal_entrywise

-- mantida: light_flow_group -> light_flow_group
example : type_of% @TGLExt.TheTimeHasNoRank.light_flow_group := @TGLExt.TheTimeIsNotAPost.light_flow_group
example : type_of% @TGLExt.TheTimeIsNotAPost.light_flow_group := @TGLExt.TheTimeHasNoRank.light_flow_group
#check @TGLExt.TheTimeHasNoRank.light_flow_group
#check @TGLExt.TheTimeIsNotAPost.light_flow_group

-- mantida: light_modular_orbit_converges_iff_post -> light_modular_orbit_converges_iff_post
example : type_of% @TGLExt.TheTimeHasNoRank.light_modular_orbit_converges_iff_post := @TGLExt.TheTimeIsNotAPost.light_modular_orbit_converges_iff_post
example : type_of% @TGLExt.TheTimeIsNotAPost.light_modular_orbit_converges_iff_post := @TGLExt.TheTimeHasNoRank.light_modular_orbit_converges_iff_post
#check @TGLExt.TheTimeHasNoRank.light_modular_orbit_converges_iff_post
#check @TGLExt.TheTimeIsNotAPost.light_modular_orbit_converges_iff_post

-- mantida: probe_modular_orbit_of_psiPlus_has_no_limit -> probe_modular_orbit_of_psiPlus_has_no_limit
example : type_of% @TGLExt.TheTimeHasNoRank.probe_modular_orbit_of_psiPlus_has_no_limit := @TGLExt.TheTimeIsNotAPost.probe_modular_orbit_of_psiPlus_has_no_limit
example : type_of% @TGLExt.TheTimeIsNotAPost.probe_modular_orbit_of_psiPlus_has_no_limit := @TGLExt.TheTimeHasNoRank.probe_modular_orbit_of_psiPlus_has_no_limit
#check @TGLExt.TheTimeHasNoRank.probe_modular_orbit_of_psiPlus_has_no_limit
#check @TGLExt.TheTimeIsNotAPost.probe_modular_orbit_of_psiPlus_has_no_limit

-- mantida: schurDiag -> schurDiag
example : type_of% @TGLExt.TheTimeHasNoRank.schurDiag := @TGLExt.TheTimeIsNotAPost.schurDiag
example : type_of% @TGLExt.TheTimeIsNotAPost.schurDiag := @TGLExt.TheTimeHasNoRank.schurDiag
#check @TGLExt.TheTimeHasNoRank.schurDiag
#check @TGLExt.TheTimeIsNotAPost.schurDiag

-- mantida: schurDiag_mulVec -> schurDiag_mulVec
example : type_of% @TGLExt.TheTimeHasNoRank.schurDiag_mulVec := @TGLExt.TheTimeIsNotAPost.schurDiag_mulVec
example : type_of% @TGLExt.TheTimeIsNotAPost.schurDiag_mulVec := @TGLExt.TheTimeHasNoRank.schurDiag_mulVec
#check @TGLExt.TheTimeHasNoRank.schurDiag_mulVec
#check @TGLExt.TheTimeIsNotAPost.schurDiag_mulVec

-- mantida: schurDiag_is_the_dephasing -> schurDiag_is_the_dephasing
example : type_of% @TGLExt.TheTimeHasNoRank.schurDiag_is_the_dephasing := @TGLExt.TheTimeIsNotAPost.schurDiag_is_the_dephasing
example : type_of% @TGLExt.TheTimeIsNotAPost.schurDiag_is_the_dephasing := @TGLExt.TheTimeHasNoRank.schurDiag_is_the_dephasing
#check @TGLExt.TheTimeHasNoRank.schurDiag_is_the_dephasing
#check @TGLExt.TheTimeIsNotAPost.schurDiag_is_the_dephasing

-- mantida: schurDiag_is_the_modular_flow -> schurDiag_is_the_modular_flow
example : type_of% @TGLExt.TheTimeHasNoRank.schurDiag_is_the_modular_flow := @TGLExt.TheTimeIsNotAPost.schurDiag_is_the_modular_flow
example : type_of% @TGLExt.TheTimeIsNotAPost.schurDiag_is_the_modular_flow := @TGLExt.TheTimeHasNoRank.schurDiag_is_the_modular_flow
#check @TGLExt.TheTimeHasNoRank.schurDiag_is_the_modular_flow
#check @TGLExt.TheTimeIsNotAPost.schurDiag_is_the_modular_flow

-- mantida: dephase_volume -> dephase_volume
example : type_of% @TGLExt.TheTimeHasNoRank.dephase_volume := @TGLExt.TheTimeIsNotAPost.dephase_volume
example : type_of% @TGLExt.TheTimeIsNotAPost.dephase_volume := @TGLExt.TheTimeHasNoRank.dephase_volume
#check @TGLExt.TheTimeHasNoRank.dephase_volume
#check @TGLExt.TheTimeIsNotAPost.dephase_volume

-- mantida: dephase_volume_lt_one -> dephase_volume_lt_one
example : type_of% @TGLExt.TheTimeHasNoRank.dephase_volume_lt_one := @TGLExt.TheTimeIsNotAPost.dephase_volume_lt_one
example : type_of% @TGLExt.TheTimeIsNotAPost.dephase_volume_lt_one := @TGLExt.TheTimeHasNoRank.dephase_volume_lt_one
#check @TGLExt.TheTimeHasNoRank.dephase_volume_lt_one
#check @TGLExt.TheTimeIsNotAPost.dephase_volume_lt_one

-- mantida: modular_volume_one -> modular_volume_one
example : type_of% @TGLExt.TheTimeHasNoRank.modular_volume_one := @TGLExt.TheTimeIsNotAPost.modular_volume_one
example : type_of% @TGLExt.TheTimeIsNotAPost.modular_volume_one := @TGLExt.TheTimeHasNoRank.modular_volume_one
#check @TGLExt.TheTimeHasNoRank.modular_volume_one
#check @TGLExt.TheTimeIsNotAPost.modular_volume_one

-- mantida: modular_factor_norm_one -> modular_factor_norm_one
example : type_of% @TGLExt.TheTimeHasNoRank.modular_factor_norm_one := @TGLExt.TheTimeIsNotAPost.modular_factor_norm_one
example : type_of% @TGLExt.TheTimeIsNotAPost.modular_factor_norm_one := @TGLExt.TheTimeHasNoRank.modular_factor_norm_one
#check @TGLExt.TheTimeHasNoRank.modular_factor_norm_one
#check @TGLExt.TheTimeIsNotAPost.modular_factor_norm_one

-- mantida: dephase_factor_norm_le_one -> dephase_factor_norm_le_one
example : type_of% @TGLExt.TheTimeHasNoRank.dephase_factor_norm_le_one := @TGLExt.TheTimeIsNotAPost.dephase_factor_norm_le_one
example : type_of% @TGLExt.TheTimeIsNotAPost.dephase_factor_norm_le_one := @TGLExt.TheTimeHasNoRank.dephase_factor_norm_le_one
#check @TGLExt.TheTimeHasNoRank.dephase_factor_norm_le_one
#check @TGLExt.TheTimeIsNotAPost.dephase_factor_norm_le_one

-- mantida: probe_gRate_one_sum -> probe_gRate_one_sum
example : type_of% @TGLExt.TheTimeHasNoRank.probe_gRate_one_sum := @TGLExt.TheTimeIsNotAPost.probe_gRate_one_sum
example : type_of% @TGLExt.TheTimeIsNotAPost.probe_gRate_one_sum := @TGLExt.TheTimeHasNoRank.probe_gRate_one_sum
#check @TGLExt.TheTimeHasNoRank.probe_gRate_one_sum
#check @TGLExt.TheTimeIsNotAPost.probe_gRate_one_sum

-- mantida: the_face_lands -> the_face_lands
example : type_of% @TGLExt.TheTimeHasNoRank.the_face_lands := @TGLExt.TheTimeIsNotAPost.the_face_lands
example : type_of% @TGLExt.TheTimeIsNotAPost.the_face_lands := @TGLExt.TheTimeHasNoRank.the_face_lands
#check @TGLExt.TheTimeHasNoRank.the_face_lands
#check @TGLExt.TheTimeIsNotAPost.the_face_lands

-- mantida: fixed_set_of_dephasing_is_the_diagonal -> fixed_set_of_dephasing_is_the_diagonal
example : type_of% @TGLExt.TheTimeHasNoRank.fixed_set_of_dephasing_is_the_diagonal := @TGLExt.TheTimeIsNotAPost.fixed_set_of_dephasing_is_the_diagonal
example : type_of% @TGLExt.TheTimeIsNotAPost.fixed_set_of_dephasing_is_the_diagonal := @TGLExt.TheTimeHasNoRank.fixed_set_of_dephasing_is_the_diagonal
#check @TGLExt.TheTimeHasNoRank.fixed_set_of_dephasing_is_the_diagonal
#check @TGLExt.TheTimeIsNotAPost.fixed_set_of_dephasing_is_the_diagonal

-- mantida: boost_pow_null -> boost_pow_null
example : type_of% @TGLExt.TheTimeHasNoRank.boost_pow_null := @TGLExt.TheTimeIsNotAPost.boost_pow_null
example : type_of% @TGLExt.TheTimeIsNotAPost.boost_pow_null := @TGLExt.TheTimeHasNoRank.boost_pow_null
#check @TGLExt.TheTimeHasNoRank.boost_pow_null
#check @TGLExt.TheTimeIsNotAPost.boost_pow_null

-- mantida: volume_kept_yet_lands -> volume_kept_yet_lands
example : type_of% @TGLExt.TheTimeHasNoRank.volume_kept_yet_lands := @TGLExt.TheTimeIsNotAPost.volume_kept_yet_lands
example : type_of% @TGLExt.TheTimeIsNotAPost.volume_kept_yet_lands := @TGLExt.TheTimeHasNoRank.volume_kept_yet_lands
#check @TGLExt.TheTimeHasNoRank.volume_kept_yet_lands
#check @TGLExt.TheTimeIsNotAPost.volume_kept_yet_lands

-- mantida: global_attractor_needs_volume_loss -> global_attractor_needs_volume_loss
example : type_of% @TGLExt.TheTimeHasNoRank.global_attractor_needs_volume_loss := @TGLExt.TheTimeIsNotAPost.global_attractor_needs_volume_loss
example : type_of% @TGLExt.TheTimeIsNotAPost.global_attractor_needs_volume_loss := @TGLExt.TheTimeHasNoRank.global_attractor_needs_volume_loss
#check @TGLExt.TheTimeHasNoRank.global_attractor_needs_volume_loss
#check @TGLExt.TheTimeIsNotAPost.global_attractor_needs_volume_loss

-- mantida: dephasing_lands_without_being_fixed -> dephasing_lands_without_being_fixed
example : type_of% @TGLExt.TheTimeHasNoRank.dephasing_lands_without_being_fixed := @TGLExt.TheTimeIsNotAPost.dephasing_lands_without_being_fixed
example : type_of% @TGLExt.TheTimeIsNotAPost.dephasing_lands_without_being_fixed := @TGLExt.TheTimeHasNoRank.dephasing_lands_without_being_fixed
#check @TGLExt.TheTimeHasNoRank.dephasing_lands_without_being_fixed
#check @TGLExt.TheTimeIsNotAPost.dephasing_lands_without_being_fixed

-- mantida: the_record_is_invariant -> the_record_is_invariant
example : type_of% @TGLExt.TheTimeHasNoRank.the_record_is_invariant := @TGLExt.TheTimeIsNotAPost.the_record_is_invariant
example : type_of% @TGLExt.TheTimeIsNotAPost.the_record_is_invariant := @TGLExt.TheTimeHasNoRank.the_record_is_invariant
#check @TGLExt.TheTimeHasNoRank.the_record_is_invariant
#check @TGLExt.TheTimeIsNotAPost.the_record_is_invariant

-- mantida: dephase_fixed_states_not_unique -> dephase_fixed_states_not_unique
example : type_of% @TGLExt.TheTimeHasNoRank.dephase_fixed_states_not_unique := @TGLExt.TheTimeIsNotAPost.dephase_fixed_states_not_unique
example : type_of% @TGLExt.TheTimeIsNotAPost.dephase_fixed_states_not_unique := @TGLExt.TheTimeHasNoRank.dephase_fixed_states_not_unique
#check @TGLExt.TheTimeHasNoRank.dephase_fixed_states_not_unique
#check @TGLExt.TheTimeIsNotAPost.dephase_fixed_states_not_unique

-- mantida: purityR_dephase -> purityR_dephase
example : type_of% @TGLExt.TheTimeHasNoRank.purityR_dephase := @TGLExt.TheTimeIsNotAPost.purityR_dephase
example : type_of% @TGLExt.TheTimeIsNotAPost.purityR_dephase := @TGLExt.TheTimeHasNoRank.purityR_dephase
#check @TGLExt.TheTimeHasNoRank.purityR_dephase
#check @TGLExt.TheTimeIsNotAPost.purityR_dephase

-- mantida: purity_never_grows_under_dephasing -> purity_never_grows_under_dephasing
example : type_of% @TGLExt.TheTimeHasNoRank.purity_never_grows_under_dephasing := @TGLExt.TheTimeIsNotAPost.purity_never_grows_under_dephasing
example : type_of% @TGLExt.TheTimeIsNotAPost.purity_never_grows_under_dephasing := @TGLExt.TheTimeHasNoRank.purity_never_grows_under_dephasing
#check @TGLExt.TheTimeHasNoRank.purity_never_grows_under_dephasing
#check @TGLExt.TheTimeIsNotAPost.purity_never_grows_under_dephasing

-- mantida: purityR_dephase_lt -> purityR_dephase_lt
example : type_of% @TGLExt.TheTimeHasNoRank.purityR_dephase_lt := @TGLExt.TheTimeIsNotAPost.purityR_dephase_lt
example : type_of% @TGLExt.TheTimeIsNotAPost.purityR_dephase_lt := @TGLExt.TheTimeHasNoRank.purityR_dephase_lt
#check @TGLExt.TheTimeHasNoRank.purityR_dephase_lt
#check @TGLExt.TheTimeIsNotAPost.purityR_dephase_lt

-- mantida: purity_of_hermitian -> purity_of_hermitian
example : type_of% @TGLExt.TheTimeHasNoRank.purity_of_hermitian := @TGLExt.TheTimeIsNotAPost.purity_of_hermitian
example : type_of% @TGLExt.TheTimeIsNotAPost.purity_of_hermitian := @TGLExt.TheTimeHasNoRank.purity_of_hermitian
#check @TGLExt.TheTimeHasNoRank.purity_of_hermitian
#check @TGLExt.TheTimeIsNotAPost.purity_of_hermitian

-- mantida: purityR_sigma -> purityR_sigma
example : type_of% @TGLExt.TheTimeHasNoRank.purityR_sigma := @TGLExt.TheTimeIsNotAPost.purityR_sigma
example : type_of% @TGLExt.TheTimeIsNotAPost.purityR_sigma := @TGLExt.TheTimeHasNoRank.purityR_sigma
#check @TGLExt.TheTimeHasNoRank.purityR_sigma
#check @TGLExt.TheTimeIsNotAPost.purityR_sigma

-- mantida: no_coherence_no_loss -> no_coherence_no_loss
example : type_of% @TGLExt.TheTimeHasNoRank.no_coherence_no_loss := @TGLExt.TheTimeIsNotAPost.no_coherence_no_loss
example : type_of% @TGLExt.TheTimeIsNotAPost.no_coherence_no_loss := @TGLExt.TheTimeHasNoRank.no_coherence_no_loss
#check @TGLExt.TheTimeHasNoRank.no_coherence_no_loss
#check @TGLExt.TheTimeIsNotAPost.no_coherence_no_loss

-- mantida: unitary_keeps_purity -> unitary_keeps_purity
example : type_of% @TGLExt.TheTimeHasNoRank.unitary_keeps_purity := @TGLExt.TheTimeIsNotAPost.unitary_keeps_purity
example : type_of% @TGLExt.TheTimeIsNotAPost.unitary_keeps_purity := @TGLExt.TheTimeHasNoRank.unitary_keeps_purity
#check @TGLExt.TheTimeHasNoRank.unitary_keeps_purity
#check @TGLExt.TheTimeIsNotAPost.unitary_keeps_purity

-- mantida: probe_psiPlus_purity -> probe_psiPlus_purity
example : type_of% @TGLExt.TheTimeHasNoRank.probe_psiPlus_purity := @TGLExt.TheTimeIsNotAPost.probe_psiPlus_purity
example : type_of% @TGLExt.TheTimeIsNotAPost.probe_psiPlus_purity := @TGLExt.TheTimeHasNoRank.probe_psiPlus_purity
#check @TGLExt.TheTimeHasNoRank.probe_psiPlus_purity
#check @TGLExt.TheTimeIsNotAPost.probe_psiPlus_purity

-- mantida: purity_grows_backwards -> purity_grows_backwards
example : type_of% @TGLExt.TheTimeHasNoRank.purity_grows_backwards := @TGLExt.TheTimeIsNotAPost.purity_grows_backwards
example : type_of% @TGLExt.TheTimeIsNotAPost.purity_grows_backwards := @TGLExt.TheTimeHasNoRank.purity_grows_backwards
#check @TGLExt.TheTimeHasNoRank.purity_grows_backwards
#check @TGLExt.TheTimeIsNotAPost.purity_grows_backwards

-- mantida: probe_psiPlus_dephased_purity -> probe_psiPlus_dephased_purity
example : type_of% @TGLExt.TheTimeHasNoRank.probe_psiPlus_dephased_purity := @TGLExt.TheTimeIsNotAPost.probe_psiPlus_dephased_purity
example : type_of% @TGLExt.TheTimeIsNotAPost.probe_psiPlus_dephased_purity := @TGLExt.TheTimeHasNoRank.probe_psiPlus_dephased_purity
#check @TGLExt.TheTimeHasNoRank.probe_psiPlus_dephased_purity
#check @TGLExt.TheTimeIsNotAPost.probe_psiPlus_dephased_purity

-- mantida: dephase_inverse -> dephase_inverse
example : type_of% @TGLExt.TheTimeHasNoRank.dephase_inverse := @TGLExt.TheTimeIsNotAPost.dephase_inverse
example : type_of% @TGLExt.TheTimeIsNotAPost.dephase_inverse := @TGLExt.TheTimeHasNoRank.dephase_inverse
#check @TGLExt.TheTimeHasNoRank.dephase_inverse
#check @TGLExt.TheTimeIsNotAPost.dephase_inverse

-- mantida: quad_form_fin_two -> quad_form_fin_two
example : type_of% @TGLExt.TheTimeHasNoRank.quad_form_fin_two := @TGLExt.TheTimeIsNotAPost.quad_form_fin_two
example : type_of% @TGLExt.TheTimeIsNotAPost.quad_form_fin_two := @TGLExt.TheTimeHasNoRank.quad_form_fin_two
#check @TGLExt.TheTimeHasNoRank.quad_form_fin_two
#check @TGLExt.TheTimeIsNotAPost.quad_form_fin_two

-- mantida: inverse_dephasing_quadratic_form -> inverse_dephasing_quadratic_form
example : type_of% @TGLExt.TheTimeHasNoRank.inverse_dephasing_quadratic_form := @TGLExt.TheTimeIsNotAPost.inverse_dephasing_quadratic_form
example : type_of% @TGLExt.TheTimeIsNotAPost.inverse_dephasing_quadratic_form := @TGLExt.TheTimeHasNoRank.inverse_dephasing_quadratic_form
#check @TGLExt.TheTimeHasNoRank.inverse_dephasing_quadratic_form
#check @TGLExt.TheTimeIsNotAPost.inverse_dephasing_quadratic_form

-- mantida: inverse_dephasing_not_positive -> inverse_dephasing_not_positive
example : type_of% @TGLExt.TheTimeHasNoRank.inverse_dephasing_not_positive := @TGLExt.TheTimeIsNotAPost.inverse_dephasing_not_positive
example : type_of% @TGLExt.TheTimeIsNotAPost.inverse_dephasing_not_positive := @TGLExt.TheTimeHasNoRank.inverse_dephasing_not_positive
#check @TGLExt.TheTimeHasNoRank.inverse_dephasing_not_positive
#check @TGLExt.TheTimeIsNotAPost.inverse_dephasing_not_positive

-- mantida: control_inverse_at_time_zero -> control_inverse_at_time_zero
example : type_of% @TGLExt.TheTimeHasNoRank.control_inverse_at_time_zero := @TGLExt.TheTimeIsNotAPost.control_inverse_at_time_zero
example : type_of% @TGLExt.TheTimeIsNotAPost.control_inverse_at_time_zero := @TGLExt.TheTimeHasNoRank.control_inverse_at_time_zero
#check @TGLExt.TheTimeHasNoRank.control_inverse_at_time_zero
#check @TGLExt.TheTimeIsNotAPost.control_inverse_at_time_zero

-- mantida: control_inverse_on_diagonal -> control_inverse_on_diagonal
example : type_of% @TGLExt.TheTimeHasNoRank.control_inverse_on_diagonal := @TGLExt.TheTimeIsNotAPost.control_inverse_on_diagonal
example : type_of% @TGLExt.TheTimeIsNotAPost.control_inverse_on_diagonal := @TGLExt.TheTimeHasNoRank.control_inverse_on_diagonal
#check @TGLExt.TheTimeHasNoRank.control_inverse_on_diagonal
#check @TGLExt.TheTimeIsNotAPost.control_inverse_on_diagonal

-- mantida: unitary_inverse_is_a_channel -> unitary_inverse_is_a_channel
example : type_of% @TGLExt.TheTimeHasNoRank.unitary_inverse_is_a_channel := @TGLExt.TheTimeIsNotAPost.unitary_inverse_is_a_channel
example : type_of% @TGLExt.TheTimeIsNotAPost.unitary_inverse_is_a_channel := @TGLExt.TheTimeHasNoRank.unitary_inverse_is_a_channel
#check @TGLExt.TheTimeHasNoRank.unitary_inverse_is_a_channel
#check @TGLExt.TheTimeIsNotAPost.unitary_inverse_is_a_channel

-- mantida: coherence_entry_scaling -> coherence_entry_scaling
example : type_of% @TGLExt.TheTimeHasNoRank.coherence_entry_scaling := @TGLExt.TheTimeIsNotAPost.coherence_entry_scaling
example : type_of% @TGLExt.TheTimeIsNotAPost.coherence_entry_scaling := @TGLExt.TheTimeHasNoRank.coherence_entry_scaling
#check @TGLExt.TheTimeHasNoRank.coherence_entry_scaling
#check @TGLExt.TheTimeIsNotAPost.coherence_entry_scaling

-- mantida: coherenceScaling -> coherenceScaling
example : type_of% @TGLExt.TheTimeHasNoRank.coherenceScaling := @TGLExt.TheTimeIsNotAPost.coherenceScaling
example : type_of% @TGLExt.TheTimeIsNotAPost.coherenceScaling := @TGLExt.TheTimeHasNoRank.coherenceScaling
#check @TGLExt.TheTimeHasNoRank.coherenceScaling
#check @TGLExt.TheTimeIsNotAPost.coherenceScaling

-- mantida: the_coherence_obeys_agape -> the_coherence_obeys_agape
example : type_of% @TGLExt.TheTimeHasNoRank.the_coherence_obeys_agape := @TGLExt.TheTimeIsNotAPost.the_coherence_obeys_agape
example : type_of% @TGLExt.TheTimeIsNotAPost.the_coherence_obeys_agape := @TGLExt.TheTimeHasNoRank.the_coherence_obeys_agape
#check @TGLExt.TheTimeHasNoRank.the_coherence_obeys_agape
#check @TGLExt.TheTimeIsNotAPost.the_coherence_obeys_agape

-- mantida: the_coherence_obeys_agape_explicit -> the_coherence_obeys_agape_explicit
example : type_of% @TGLExt.TheTimeHasNoRank.the_coherence_obeys_agape_explicit := @TGLExt.TheTimeIsNotAPost.the_coherence_obeys_agape_explicit
example : type_of% @TGLExt.TheTimeIsNotAPost.the_coherence_obeys_agape_explicit := @TGLExt.TheTimeHasNoRank.the_coherence_obeys_agape_explicit
#check @TGLExt.TheTimeHasNoRank.the_coherence_obeys_agape_explicit
#check @TGLExt.TheTimeIsNotAPost.the_coherence_obeys_agape_explicit

-- mantida: the_record_does_not_scale -> the_record_does_not_scale
example : type_of% @TGLExt.TheTimeHasNoRank.the_record_does_not_scale := @TGLExt.TheTimeIsNotAPost.the_record_does_not_scale
example : type_of% @TGLExt.TheTimeIsNotAPost.the_record_does_not_scale := @TGLExt.TheTimeHasNoRank.the_record_does_not_scale
#check @TGLExt.TheTimeHasNoRank.the_record_does_not_scale
#check @TGLExt.TheTimeIsNotAPost.the_record_does_not_scale

-- mantida: past_null_ray_contracts -> past_null_ray_contracts
example : type_of% @TGLExt.TheTimeHasNoRank.past_null_ray_contracts := @TGLExt.TheTimeIsNotAPost.past_null_ray_contracts
example : type_of% @TGLExt.TheTimeIsNotAPost.past_null_ray_contracts := @TGLExt.TheTimeHasNoRank.past_null_ray_contracts
#check @TGLExt.TheTimeHasNoRank.past_null_ray_contracts
#check @TGLExt.TheTimeIsNotAPost.past_null_ray_contracts

-- mantida: wrong_rate_breaks_scaling -> wrong_rate_breaks_scaling
example : type_of% @TGLExt.TheTimeHasNoRank.wrong_rate_breaks_scaling := @TGLExt.TheTimeIsNotAPost.wrong_rate_breaks_scaling
example : type_of% @TGLExt.TheTimeIsNotAPost.wrong_rate_breaks_scaling := @TGLExt.TheTimeHasNoRank.wrong_rate_breaks_scaling
#check @TGLExt.TheTimeHasNoRank.wrong_rate_breaks_scaling
#check @TGLExt.TheTimeIsNotAPost.wrong_rate_breaks_scaling

-- mantida: flow_sq -> flow_sq
example : type_of% @TGLExt.TheTimeHasNoRank.flow_sq := @TGLExt.TheTimeIsNotAPost.flow_sq
example : type_of% @TGLExt.TheTimeIsNotAPost.flow_sq := @TGLExt.TheTimeHasNoRank.flow_sq
#check @TGLExt.TheTimeHasNoRank.flow_sq
#check @TGLExt.TheTimeIsNotAPost.flow_sq

-- mantida: flow_isIdempotentElem_iff -> flow_isIdempotentElem_iff
example : type_of% @TGLExt.TheTimeHasNoRank.flow_isIdempotentElem_iff := @TGLExt.TheTimeIsNotAPost.flow_isIdempotentElem_iff
example : type_of% @TGLExt.TheTimeIsNotAPost.flow_isIdempotentElem_iff := @TGLExt.TheTimeHasNoRank.flow_isIdempotentElem_iff
#check @TGLExt.TheTimeHasNoRank.flow_isIdempotentElem_iff
#check @TGLExt.TheTimeIsNotAPost.flow_isIdempotentElem_iff

-- mantida: flow_isUnit -> flow_isUnit
example : type_of% @TGLExt.TheTimeHasNoRank.flow_isUnit := @TGLExt.TheTimeIsNotAPost.flow_isUnit
example : type_of% @TGLExt.TheTimeIsNotAPost.flow_isUnit := @TGLExt.TheTimeHasNoRank.flow_isUnit
#check @TGLExt.TheTimeHasNoRank.flow_isUnit
#check @TGLExt.TheTimeIsNotAPost.flow_isUnit

-- mantida: flow_of_one_is_idempotent -> flow_of_one_is_idempotent
example : type_of% @TGLExt.TheTimeHasNoRank.flow_of_one_is_idempotent := @TGLExt.TheTimeIsNotAPost.flow_of_one_is_idempotent
example : type_of% @TGLExt.TheTimeIsNotAPost.flow_of_one_is_idempotent := @TGLExt.TheTimeHasNoRank.flow_of_one_is_idempotent
#check @TGLExt.TheTimeHasNoRank.flow_of_one_is_idempotent
#check @TGLExt.TheTimeIsNotAPost.flow_of_one_is_idempotent

-- mantida: flow_at_zero_is_idempotent -> flow_at_zero_is_idempotent
example : type_of% @TGLExt.TheTimeHasNoRank.flow_at_zero_is_idempotent := @TGLExt.TheTimeIsNotAPost.flow_at_zero_is_idempotent
example : type_of% @TGLExt.TheTimeIsNotAPost.flow_at_zero_is_idempotent := @TGLExt.TheTimeHasNoRank.flow_at_zero_is_idempotent
#check @TGLExt.TheTimeHasNoRank.flow_at_zero_is_idempotent
#check @TGLExt.TheTimeIsNotAPost.flow_at_zero_is_idempotent

-- mantida: no_finite_instant_is_the_post -> no_finite_instant_is_the_post
example : type_of% @TGLExt.TheTimeHasNoRank.no_finite_instant_is_the_post := @TGLExt.TheTimeIsNotAPost.no_finite_instant_is_the_post
example : type_of% @TGLExt.TheTimeIsNotAPost.no_finite_instant_is_the_post := @TGLExt.TheTimeHasNoRank.no_finite_instant_is_the_post
#check @TGLExt.TheTimeHasNoRank.no_finite_instant_is_the_post
#check @TGLExt.TheTimeIsNotAPost.no_finite_instant_is_the_post

-- mantida: post_not_isUnit -> post_not_isUnit
example : type_of% @TGLExt.TheTimeHasNoRank.post_not_isUnit := @TGLExt.TheTimeIsNotAPost.post_not_isUnit
example : type_of% @TGLExt.TheTimeIsNotAPost.post_not_isUnit := @TGLExt.TheTimeHasNoRank.post_not_isUnit
#check @TGLExt.TheTimeHasNoRank.post_not_isUnit
#check @TGLExt.TheTimeIsNotAPost.post_not_isUnit

-- mantida: flow_full_rank -> flow_full_rank
example : type_of% @TGLExt.TheTimeHasNoRank.flow_full_rank := @TGLExt.TheTimeIsNotAPost.flow_full_rank
example : type_of% @TGLExt.TheTimeIsNotAPost.flow_full_rank := @TGLExt.TheTimeHasNoRank.flow_full_rank
#check @TGLExt.TheTimeHasNoRank.flow_full_rank
#check @TGLExt.TheTimeIsNotAPost.flow_full_rank

-- mantida: post_rank_lt -> post_rank_lt
example : type_of% @TGLExt.TheTimeHasNoRank.post_rank_lt := @TGLExt.TheTimeIsNotAPost.post_rank_lt
example : type_of% @TGLExt.TheTimeIsNotAPost.post_rank_lt := @TGLExt.TheTimeHasNoRank.post_rank_lt
#check @TGLExt.TheTimeHasNoRank.post_rank_lt
#check @TGLExt.TheTimeIsNotAPost.post_rank_lt

-- renomeada: the_time_has_no_rank -> the_time_is_not_a_post
example : type_of% @TGLExt.TheTimeHasNoRank.the_time_has_no_rank := @TGLExt.TheTimeIsNotAPost.the_time_is_not_a_post
example : type_of% @TGLExt.TheTimeIsNotAPost.the_time_is_not_a_post := @TGLExt.TheTimeHasNoRank.the_time_has_no_rank
#check @TGLExt.TheTimeHasNoRank.the_time_has_no_rank
#check @TGLExt.TheTimeIsNotAPost.the_time_is_not_a_post

-- mantida: postDiag -> postDiag
example : type_of% @TGLExt.TheTimeHasNoRank.postDiag := @TGLExt.TheTimeIsNotAPost.postDiag
example : type_of% @TGLExt.TheTimeIsNotAPost.postDiag := @TGLExt.TheTimeHasNoRank.postDiag
#check @TGLExt.TheTimeHasNoRank.postDiag
#check @TGLExt.TheTimeIsNotAPost.postDiag

-- mantida: postDiag_idem -> postDiag_idem
example : type_of% @TGLExt.TheTimeHasNoRank.postDiag_idem := @TGLExt.TheTimeIsNotAPost.postDiag_idem
example : type_of% @TGLExt.TheTimeIsNotAPost.postDiag_idem := @TGLExt.TheTimeHasNoRank.postDiag_idem
#check @TGLExt.TheTimeHasNoRank.postDiag_idem
#check @TGLExt.TheTimeIsNotAPost.postDiag_idem

-- mantida: postDiag_compl_ne_zero -> postDiag_compl_ne_zero
example : type_of% @TGLExt.TheTimeHasNoRank.postDiag_compl_ne_zero := @TGLExt.TheTimeIsNotAPost.postDiag_compl_ne_zero
example : type_of% @TGLExt.TheTimeIsNotAPost.postDiag_compl_ne_zero := @TGLExt.TheTimeHasNoRank.postDiag_compl_ne_zero
#check @TGLExt.TheTimeHasNoRank.postDiag_compl_ne_zero
#check @TGLExt.TheTimeIsNotAPost.postDiag_compl_ne_zero

-- mantida: postDiag_ne_one -> postDiag_ne_one
example : type_of% @TGLExt.TheTimeHasNoRank.postDiag_ne_one := @TGLExt.TheTimeIsNotAPost.postDiag_ne_one
example : type_of% @TGLExt.TheTimeIsNotAPost.postDiag_ne_one := @TGLExt.TheTimeHasNoRank.postDiag_ne_one
#check @TGLExt.TheTimeHasNoRank.postDiag_ne_one
#check @TGLExt.TheTimeIsNotAPost.postDiag_ne_one

-- renomeada: probe_the_time_has_no_rank -> probe_the_time_is_not_a_post
example : type_of% @TGLExt.TheTimeHasNoRank.probe_the_time_has_no_rank := @TGLExt.TheTimeIsNotAPost.probe_the_time_is_not_a_post
example : type_of% @TGLExt.TheTimeIsNotAPost.probe_the_time_is_not_a_post := @TGLExt.TheTimeHasNoRank.probe_the_time_has_no_rank
#check @TGLExt.TheTimeHasNoRank.probe_the_time_has_no_rank
#check @TGLExt.TheTimeIsNotAPost.probe_the_time_is_not_a_post

-- mantida: clock_faithful_iff_one_turn -> clock_faithful_iff_one_turn
example : type_of% @TGLExt.TheTimeHasNoRank.clock_faithful_iff_one_turn := @TGLExt.TheTimeIsNotAPost.clock_faithful_iff_one_turn
example : type_of% @TGLExt.TheTimeIsNotAPost.clock_faithful_iff_one_turn := @TGLExt.TheTimeHasNoRank.clock_faithful_iff_one_turn
#check @TGLExt.TheTimeHasNoRank.clock_faithful_iff_one_turn
#check @TGLExt.TheTimeIsNotAPost.clock_faithful_iff_one_turn

-- mantida: clock_reciprocal_temperature -> clock_reciprocal_temperature
example : type_of% @TGLExt.TheTimeHasNoRank.clock_reciprocal_temperature := @TGLExt.TheTimeIsNotAPost.clock_reciprocal_temperature
example : type_of% @TGLExt.TheTimeIsNotAPost.clock_reciprocal_temperature := @TGLExt.TheTimeHasNoRank.clock_reciprocal_temperature
#check @TGLExt.TheTimeHasNoRank.clock_reciprocal_temperature
#check @TGLExt.TheTimeIsNotAPost.clock_reciprocal_temperature

-- mantida: frozen_clock -> frozen_clock
example : type_of% @TGLExt.TheTimeHasNoRank.frozen_clock := @TGLExt.TheTimeIsNotAPost.frozen_clock
example : type_of% @TGLExt.TheTimeIsNotAPost.frozen_clock := @TGLExt.TheTimeHasNoRank.frozen_clock
#check @TGLExt.TheTimeHasNoRank.frozen_clock
#check @TGLExt.TheTimeIsNotAPost.frozen_clock

-- mantida: frozen_clock_not_faithful -> frozen_clock_not_faithful
example : type_of% @TGLExt.TheTimeHasNoRank.frozen_clock_not_faithful := @TGLExt.TheTimeIsNotAPost.frozen_clock_not_faithful
example : type_of% @TGLExt.TheTimeIsNotAPost.frozen_clock_not_faithful := @TGLExt.TheTimeHasNoRank.frozen_clock_not_faithful
#check @TGLExt.TheTimeHasNoRank.frozen_clock_not_faithful
#check @TGLExt.TheTimeIsNotAPost.frozen_clock_not_faithful

-- mantida: face_clock_has_no_period -> face_clock_has_no_period
example : type_of% @TGLExt.TheTimeHasNoRank.face_clock_has_no_period := @TGLExt.TheTimeIsNotAPost.face_clock_has_no_period
example : type_of% @TGLExt.TheTimeIsNotAPost.face_clock_has_no_period := @TGLExt.TheTimeHasNoRank.face_clock_has_no_period
#check @TGLExt.TheTimeHasNoRank.face_clock_has_no_period
#check @TGLExt.TheTimeIsNotAPost.face_clock_has_no_period

-- mantida: angle_has_no_limit -> angle_has_no_limit
example : type_of% @TGLExt.TheTimeHasNoRank.angle_has_no_limit := @TGLExt.TheTimeIsNotAPost.angle_has_no_limit
example : type_of% @TGLExt.TheTimeIsNotAPost.angle_has_no_limit := @TGLExt.TheTimeHasNoRank.angle_has_no_limit
#check @TGLExt.TheTimeHasNoRank.angle_has_no_limit
#check @TGLExt.TheTimeIsNotAPost.angle_has_no_limit

-- mantida: angle_is_periodic -> angle_is_periodic
example : type_of% @TGLExt.TheTimeHasNoRank.angle_is_periodic := @TGLExt.TheTimeIsNotAPost.angle_is_periodic
example : type_of% @TGLExt.TheTimeIsNotAPost.angle_is_periodic := @TGLExt.TheTimeHasNoRank.angle_is_periodic
#check @TGLExt.TheTimeHasNoRank.angle_is_periodic
#check @TGLExt.TheTimeIsNotAPost.angle_is_periodic

-- mantida: face_has_a_limit -> face_has_a_limit
example : type_of% @TGLExt.TheTimeHasNoRank.face_has_a_limit := @TGLExt.TheTimeIsNotAPost.face_has_a_limit
example : type_of% @TGLExt.TheTimeIsNotAPost.face_has_a_limit := @TGLExt.TheTimeHasNoRank.face_has_a_limit
#check @TGLExt.TheTimeHasNoRank.face_has_a_limit
#check @TGLExt.TheTimeIsNotAPost.face_has_a_limit

-- mantida: face_distinguishes_instants -> face_distinguishes_instants
example : type_of% @TGLExt.TheTimeHasNoRank.face_distinguishes_instants := @TGLExt.TheTimeIsNotAPost.face_distinguishes_instants
example : type_of% @TGLExt.TheTimeIsNotAPost.face_distinguishes_instants := @TGLExt.TheTimeHasNoRank.face_distinguishes_instants
#check @TGLExt.TheTimeHasNoRank.face_distinguishes_instants
#check @TGLExt.TheTimeIsNotAPost.face_distinguishes_instants

-- mantida: modular_clock_rotates_without_shrinking -> modular_clock_rotates_without_shrinking
example : type_of% @TGLExt.TheTimeHasNoRank.modular_clock_rotates_without_shrinking := @TGLExt.TheTimeIsNotAPost.modular_clock_rotates_without_shrinking
example : type_of% @TGLExt.TheTimeIsNotAPost.modular_clock_rotates_without_shrinking := @TGLExt.TheTimeHasNoRank.modular_clock_rotates_without_shrinking
#check @TGLExt.TheTimeHasNoRank.modular_clock_rotates_without_shrinking
#check @TGLExt.TheTimeIsNotAPost.modular_clock_rotates_without_shrinking

-- mantida: the_post_is_not_moved -> the_post_is_not_moved
example : type_of% @TGLExt.TheTimeHasNoRank.the_post_is_not_moved := @TGLExt.TheTimeIsNotAPost.the_post_is_not_moved
example : type_of% @TGLExt.TheTimeIsNotAPost.the_post_is_not_moved := @TGLExt.TheTimeHasNoRank.the_post_is_not_moved
#check @TGLExt.TheTimeHasNoRank.the_post_is_not_moved
#check @TGLExt.TheTimeIsNotAPost.the_post_is_not_moved

-- mantida: the_state_is_not_moved -> the_state_is_not_moved
example : type_of% @TGLExt.TheTimeHasNoRank.the_state_is_not_moved := @TGLExt.TheTimeIsNotAPost.the_state_is_not_moved
example : type_of% @TGLExt.TheTimeIsNotAPost.the_state_is_not_moved := @TGLExt.TheTimeHasNoRank.the_state_is_not_moved
#check @TGLExt.TheTimeHasNoRank.the_state_is_not_moved
#check @TGLExt.TheTimeIsNotAPost.the_state_is_not_moved

-- mantida: the_vector_is_not_moved -> the_vector_is_not_moved
example : type_of% @TGLExt.TheTimeHasNoRank.the_vector_is_not_moved := @TGLExt.TheTimeIsNotAPost.the_vector_is_not_moved
example : type_of% @TGLExt.TheTimeIsNotAPost.the_vector_is_not_moved := @TGLExt.TheTimeHasNoRank.the_vector_is_not_moved
#check @TGLExt.TheTimeHasNoRank.the_vector_is_not_moved
#check @TGLExt.TheTimeIsNotAPost.the_vector_is_not_moved

-- renomeada: optical_attractor_is_the_absolute_one -> half_identity_is_absoluteRho_two
example : type_of% @TGLExt.TheTimeHasNoRank.optical_attractor_is_the_absolute_one := @TGLExt.TheTimeIsNotAPost.half_identity_is_absoluteRho_two
example : type_of% @TGLExt.TheTimeIsNotAPost.half_identity_is_absoluteRho_two := @TGLExt.TheTimeHasNoRank.optical_attractor_is_the_absolute_one
#check @TGLExt.TheTimeHasNoRank.optical_attractor_is_the_absolute_one
#check @TGLExt.TheTimeIsNotAPost.half_identity_is_absoluteRho_two

-- renomeada: optical_attractor_clock_stops -> half_identity_clock_stops
example : type_of% @TGLExt.TheTimeHasNoRank.optical_attractor_clock_stops := @TGLExt.TheTimeIsNotAPost.half_identity_clock_stops
example : type_of% @TGLExt.TheTimeIsNotAPost.half_identity_clock_stops := @TGLExt.TheTimeHasNoRank.optical_attractor_clock_stops
#check @TGLExt.TheTimeHasNoRank.optical_attractor_clock_stops
#check @TGLExt.TheTimeIsNotAPost.half_identity_clock_stops

-- mantida: flow_at_one_is_not_idempotent -> flow_at_one_is_not_idempotent
example : type_of% @TGLExt.TheTimeHasNoRank.flow_at_one_is_not_idempotent := @TGLExt.TheTimeIsNotAPost.flow_at_one_is_not_idempotent
example : type_of% @TGLExt.TheTimeIsNotAPost.flow_at_one_is_not_idempotent := @TGLExt.TheTimeHasNoRank.flow_at_one_is_not_idempotent
#check @TGLExt.TheTimeHasNoRank.flow_at_one_is_not_idempotent
#check @TGLExt.TheTimeIsNotAPost.flow_at_one_is_not_idempotent

-- mantida: rhoD_equal_weights -> rhoD_equal_weights
example : type_of% @TGLExt.TheTimeHasNoRank.rhoD_equal_weights := @TGLExt.TheTimeIsNotAPost.rhoD_equal_weights
example : type_of% @TGLExt.TheTimeIsNotAPost.rhoD_equal_weights := @TGLExt.TheTimeHasNoRank.rhoD_equal_weights
#check @TGLExt.TheTimeHasNoRank.rhoD_equal_weights
#check @TGLExt.TheTimeIsNotAPost.rhoD_equal_weights

-- mantida: modular_iff_needs_injective_weights -> modular_iff_needs_injective_weights
example : type_of% @TGLExt.TheTimeHasNoRank.modular_iff_needs_injective_weights := @TGLExt.TheTimeIsNotAPost.modular_iff_needs_injective_weights
example : type_of% @TGLExt.TheTimeIsNotAPost.modular_iff_needs_injective_weights := @TGLExt.TheTimeHasNoRank.modular_iff_needs_injective_weights
#check @TGLExt.TheTimeHasNoRank.modular_iff_needs_injective_weights
#check @TGLExt.TheTimeIsNotAPost.modular_iff_needs_injective_weights

-- mantida: centralizer_iff_needs_injective_weights -> centralizer_iff_needs_injective_weights
example : type_of% @TGLExt.TheTimeHasNoRank.centralizer_iff_needs_injective_weights := @TGLExt.TheTimeIsNotAPost.centralizer_iff_needs_injective_weights
example : type_of% @TGLExt.TheTimeIsNotAPost.centralizer_iff_needs_injective_weights := @TGLExt.TheTimeHasNoRank.centralizer_iff_needs_injective_weights
#check @TGLExt.TheTimeHasNoRank.centralizer_iff_needs_injective_weights
#check @TGLExt.TheTimeIsNotAPost.centralizer_iff_needs_injective_weights

-- mantida: dephasing_iff_needs_positive_rates -> dephasing_iff_needs_positive_rates
example : type_of% @TGLExt.TheTimeHasNoRank.dephasing_iff_needs_positive_rates := @TGLExt.TheTimeIsNotAPost.dephasing_iff_needs_positive_rates
example : type_of% @TGLExt.TheTimeIsNotAPost.dephasing_iff_needs_positive_rates := @TGLExt.TheTimeHasNoRank.dephasing_iff_needs_positive_rates
#check @TGLExt.TheTimeHasNoRank.dephasing_iff_needs_positive_rates
#check @TGLExt.TheTimeIsNotAPost.dephasing_iff_needs_positive_rates

-- reforcos: a R2 implica a R1 (tipo R1 habitado pelo termo R2)
example : type_of% @TGLExt.TheTimeHasNoRank.purityR_modular := by
  intro n _ _ d _hd t x
  exact TGLExt.TheTimeIsNotAPost.purityR_modular d t x
#check @TGLExt.TheTimeHasNoRank.purityR_modular
#check @TGLExt.TheTimeIsNotAPost.purityR_modular

example : type_of% @TGLExt.TheTimeHasNoRank.clock_reads_modulo_period := by
  intro κ _ t
  exact TGLExt.TheTimeIsNotAPost.clock_reads_modulo_period κ t
#check @TGLExt.TheTimeHasNoRank.clock_reads_modulo_period
#check @TGLExt.TheTimeIsNotAPost.clock_reads_modulo_period

example : type_of% @TGLExt.TheTimeHasNoRank.the_two_regimes_of_time := by
  obtain ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9⟩ := TGLExt.TheTimeIsNotAPost.the_two_regimes_of_time
  refine ⟨h1, h2, h3, h4, h5, h6, h7, ?_, h9⟩
  intro κ _ t
  exact h8 κ t
#check @TGLExt.TheTimeHasNoRank.the_two_regimes_of_time
#check @TGLExt.TheTimeIsNotAPost.the_two_regimes_of_time

example : type_of% @TGLExt.TheTimeHasNoRank.probe_bounded_spectral_translation := trivial
#check @TGLExt.TheTimeHasNoRank.probe_bounded_spectral_translation
#check @TGLExt.TheTimeIsNotAPost.probe_bounded_spectral_translation

end Frobenius
end
