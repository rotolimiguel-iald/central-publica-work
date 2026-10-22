import TheTimeHasNoRank

/-!
# Auditoria independente da pedra candidata `TheTimeHasNoRank` (F1.TEMPO, sandbox)

Importa o `.olean` COMPILADO da pedra (não o fonte) e:
1. enumera TODA constante do espaço `TGLExt.TheTimeHasNoRank` (inclusive auxiliares geradas), imprime o tipo
   de declaração e os axiomas de que depende, e RECUSA (erro) se houver axioma fora do trio
   {propext, Classical.choice, Quot.sound} ou declaração `axiom` nova;
2. imprime `#check` de cada alvo pré-registrado, para o auditor comparar com a assinatura do PREREGISTRO.json.
Este arquivo não declara nada.
-/

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  let mut count := 0
  for (n, ci) in env.constants.map₁.toList do
    if (`TGLExt.TheTimeHasNoRank).isPrefixOf n then
      let axs ← collectAxioms n
      let kind := match ci with
        | .axiomInfo _ => "axiom"
        | .thmInfo _ => "theorem"
        | .defnInfo _ => "definition"
        | _ => "other"
      IO.println ("AUDIT_DECL\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++
        String.intercalate "," (axs.toList.map Name.toString))
      count := count + 1
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      if kind == "axiom" then throwError "NEW_AXIOM_REFUSED: {n}"
  IO.println ("AUDIT_TOTAL\t" ++ toString count)

#check @TGLExt.TheTimeHasNoRank.no_time_matrix
#check @TGLExt.TheTimeHasNoRank.no_time_matrix_fin
#check @TGLExt.TheTimeHasNoRank.commutator_far_from_scalar
#check @TGLExt.TheTimeHasNoRank.no_finite_spectral_translation
#check @TGLExt.TheTimeHasNoRank.no_bounded_spectral_translation
#check @TGLExt.TheTimeHasNoRank.time_is_the_modular_flow
#check @TGLExt.TheTimeHasNoRank.fixed_sector_is_the_centralizer
#check @TGLExt.TheTimeHasNoRank.tracial_state_freezes_the_flow
#check @TGLExt.TheTimeHasNoRank.nontracial_state_rejects_the_identity_flow
#check @TGLExt.TheTimeHasNoRank.unitary_keeps_spectrum_and_purity
#check @TGLExt.TheTimeHasNoRank.isometry_orbit_converges_only_if_fixed
#check @TGLExt.TheTimeHasNoRank.isometric_flow_converges_only_if_fixed
#check @TGLExt.TheTimeHasNoRank.unitary_conj_isometry
#check @TGLExt.TheTimeHasNoRank.modular_flow_is_isometry
#check @TGLExt.TheTimeHasNoRank.modular_orbit_converges_iff_diagonal
#check @TGLExt.TheTimeHasNoRank.modular_orbit_converges_iff_diagonal_entrywise
#check @TGLExt.TheTimeHasNoRank.light_modular_orbit_converges_iff_post
#check @TGLExt.TheTimeHasNoRank.schurDiag
#check @TGLExt.TheTimeHasNoRank.schurDiag_mulVec
#check @TGLExt.TheTimeHasNoRank.schurDiag_is_the_dephasing
#check @TGLExt.TheTimeHasNoRank.schurDiag_is_the_modular_flow
#check @TGLExt.TheTimeHasNoRank.dephase_volume
#check @TGLExt.TheTimeHasNoRank.dephase_volume_lt_one
#check @TGLExt.TheTimeHasNoRank.modular_volume_one
#check @TGLExt.TheTimeHasNoRank.modular_factor_norm_one
#check @TGLExt.TheTimeHasNoRank.dephase_factor_norm_le_one
#check @TGLExt.TheTimeHasNoRank.the_face_lands
#check @TGLExt.TheTimeHasNoRank.fixed_set_of_dephasing_is_the_diagonal
#check @TGLExt.TheTimeHasNoRank.volume_kept_yet_lands
#check @TGLExt.TheTimeHasNoRank.global_attractor_needs_volume_loss
#check @TGLExt.TheTimeHasNoRank.the_record_is_invariant
#check @TGLExt.TheTimeHasNoRank.dephase_fixed_states_not_unique
#check @TGLExt.TheTimeHasNoRank.purityR_dephase
#check @TGLExt.TheTimeHasNoRank.purity_never_grows_under_dephasing
#check @TGLExt.TheTimeHasNoRank.purityR_dephase_lt
#check @TGLExt.TheTimeHasNoRank.purity_of_hermitian
#check @TGLExt.TheTimeHasNoRank.purityR_sigma
#check @TGLExt.TheTimeHasNoRank.purityR_modular
#check @TGLExt.TheTimeHasNoRank.dephase_inverse
#check @TGLExt.TheTimeHasNoRank.inverse_dephasing_not_positive
#check @TGLExt.TheTimeHasNoRank.coherenceScaling
#check @TGLExt.TheTimeHasNoRank.the_coherence_obeys_agape
#check @TGLExt.TheTimeHasNoRank.the_coherence_obeys_agape_explicit
#check @TGLExt.TheTimeHasNoRank.the_record_does_not_scale
#check @TGLExt.TheTimeHasNoRank.past_null_ray_contracts
#check @TGLExt.TheTimeHasNoRank.flow_isIdempotentElem_iff
#check @TGLExt.TheTimeHasNoRank.flow_isUnit
#check @TGLExt.TheTimeHasNoRank.post_not_isUnit
#check @TGLExt.TheTimeHasNoRank.flow_full_rank
#check @TGLExt.TheTimeHasNoRank.post_rank_lt
#check @TGLExt.TheTimeHasNoRank.no_finite_instant_is_the_post
#check @TGLExt.TheTimeHasNoRank.the_time_has_no_rank
#check @TGLExt.TheTimeHasNoRank.clock_faithful_iff_one_turn
#check @TGLExt.TheTimeHasNoRank.clock_reciprocal_temperature
#check @TGLExt.TheTimeHasNoRank.clock_reads_modulo_period
#check @TGLExt.TheTimeHasNoRank.frozen_clock
#check @TGLExt.TheTimeHasNoRank.angle_has_no_limit
#check @TGLExt.TheTimeHasNoRank.angle_is_periodic
#check @TGLExt.TheTimeHasNoRank.face_has_a_limit
#check @TGLExt.TheTimeHasNoRank.face_distinguishes_instants
#check @TGLExt.TheTimeHasNoRank.modular_clock_rotates_without_shrinking
#check @TGLExt.TheTimeHasNoRank.the_post_is_not_moved
#check @TGLExt.TheTimeHasNoRank.the_state_is_not_moved
#check @TGLExt.TheTimeHasNoRank.the_vector_is_not_moved
#check @TGLExt.TheTimeHasNoRank.optical_attractor_is_the_absolute_one
#check @TGLExt.TheTimeHasNoRank.the_absolute_one_has_no_clock
#check @TGLExt.TheTimeHasNoRank.optical_attractor_clock_stops
#check @TGLExt.TheTimeHasNoRank.the_two_regimes_of_time
#check @TGLExt.TheTimeHasNoRank.commutator_can_be_nonzero
#check @TGLExt.TheTimeHasNoRank.empty_dimension_admits_time
#check @TGLExt.TheTimeHasNoRank.weyl_pair_lives_in_L2
#check @TGLExt.TheTimeHasNoRank.dephasing_lands_without_being_fixed
#check @TGLExt.TheTimeHasNoRank.no_coherence_no_loss
#check @TGLExt.TheTimeHasNoRank.unitary_keeps_purity
#check @TGLExt.TheTimeHasNoRank.purity_grows_backwards
#check @TGLExt.TheTimeHasNoRank.control_inverse_at_time_zero
#check @TGLExt.TheTimeHasNoRank.control_inverse_on_diagonal
#check @TGLExt.TheTimeHasNoRank.unitary_inverse_is_a_channel
#check @TGLExt.TheTimeHasNoRank.wrong_rate_breaks_scaling
#check @TGLExt.TheTimeHasNoRank.flow_of_one_is_idempotent
#check @TGLExt.TheTimeHasNoRank.flow_at_zero_is_idempotent
#check @TGLExt.TheTimeHasNoRank.frozen_clock_not_faithful
#check @TGLExt.TheTimeHasNoRank.face_clock_has_no_period
#check @TGLExt.TheTimeHasNoRank.flow_at_one_is_not_idempotent
#check @TGLExt.TheTimeHasNoRank.modular_iff_needs_injective_weights
#check @TGLExt.TheTimeHasNoRank.dephasing_iff_needs_positive_rates
#check @TGLExt.TheTimeHasNoRank.centralizer_iff_needs_injective_weights
