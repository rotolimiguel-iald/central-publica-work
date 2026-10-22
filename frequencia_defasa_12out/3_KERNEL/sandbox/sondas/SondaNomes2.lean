import Mathlib
import TGLExt.GlobalLiftLadder
import TGLExt.TheSingularExpectation
import TGLExt.TheTraceIsNotErasable
import TGLExt.PageInformation
import TGLExt.FractalUnitarity
import TGLExt.TheWeightIsNotTheRank
import TGLExt.TheVerbalCoupling
import TGLExt.TheSameBetaReadsThreeFaces
import TGLExt.IALDJones
import TGLExt.TheVerbSelectsTheAction
import TGLExt.TheAxiomAndTheFalseWitness
open Lean in
#eval show CoreM Unit from do
  let env ← getEnv
  let nomes : List String := ["nullity", "rank_add_nullity", "rank_eq_zero_iff", "matrix_rank_eq_zero_iff", "pure_iff_rank_one", "pure_iff_idempotent", "trace_sq_fin_two", "pure_iff_rank_one_fin_two", "rankOne_density", "rankOne_density_normalized", "rhoStar_rank_nullity", "half_identity_rank_nullity", "zero_rank_nullity", "trace_one_rank_pos", "rank_one_iff_nullity", "rank_one_iff_nullity_succ", "compression_by_rank_one", "reading_returns_the_post", "reading_of_the_attractor_state", "reading_weights_are_truth_and_cost", "trace_eq_rank_of_projection", "normalized_projection_name", "normalized_projection_index", "name_meets_rank_only_at_the_atom", "rhoStar", "rhoStar_trace", "rhoStar_rank", "rhoStar_idem", "rhoStar_herm", "rhoStar_det", "rhoStar_eq", "range_rhoStar", "Qtheta", "Qtheta_eq", "Q0", "Q0_eq", "Rot", "anticomm", "anticomm_eq", "anticomm_zero_iff", "anticomm_trace", "anticomm_frob", "anticomm_at_thetaMiguel", "leak_eq", "leak_eq_rhoOut", "leak_eq_reflected_weight", "leak_at_thetaMiguel", "ad_trace", "ad_rank", "ad_rhoStar", "ad_projection", "fractal_one_is_rank_one", "endpoint_eq", "endpoint_det", "endpoint_trace", "endpoint_rank_two_iff", "endpoint_rank_one_iff", "endpoint_purity", "endpoint_at_thetaMiguel", "dephased_rhoOut_eq", "dephased_det", "dephased_rank_two_iff", "dephased_trace", "rank_not_preserved_by_dephasing", "trace_survives_dephasing", "leak_survives_dephasing", "anticomm_dephased_eq", "anticomm_dephased_zero_iff", "anticomm_limit", "Smat_pow", "leak_after_n_passes", "angular_leak_no_limit", "angular_leak_zero_converges", "nothing_branch", "dephasing_trivial_iff", "literal_transmission_does_not_force_dephasing", "literal_leak_does_not_force_dephasing", "dephasing_acts_iff_transmits_and_leaks", "inscription_at_thetaMiguel", "psd_is_necessary", "normalization_is_necessary", "trace_one_not_rank_one", "reading_needs_weight", "reading_needs_rank_one", "nonunitary_changes_trace", "singular_kills_rank", "zero_rate_no_dephasing", "nondiagonal_reader_sees_time", "halfId", "dephasingActs", "plusReader", "unitRates", "rank_two_iff", "rank_one_iff_fin_two", "sin_two_mul_eq_zero_iff", "nullity_pos_iff_det_eq_zero", "rank_eq_card_iff_det_ne_zero", "ne_zero_of_trace_ne_zero", "rank_pos_of_trace_ne_zero", "conj_trace", "conj_diag_sq", "conj_diag_eq_iff", "hermitian_spectral", "sum_sq_eq_one_iff_idem", "idem_iff_card_support_one", "rank_eq_card_eig", "trace_eq_sum_eig", "pure_spectral_facts", "pure_core", "e0", "sin_sq_thetaMiguel", "cos_sq_thetaMiguel", "cos_thetaMiguel", "sin_two_thetaMiguel_eq_zero_iff", "rhoOut_zero", "rhoOut_pi_div_two", "dephase_rhoStar", "dephase_Q0", "rhoOut_eq_diag_iff", "cs_sq_eq_zero_iff", "sin_sq_shift_identity", "sin_sq_double", "plus_reader_value", "Rot_eq_conjTranspose", "Rot_transpose", "Qtheta_eq_rot", "Qtheta_zero", "rank_diag_two_iff"]
  for s in nomes do
    for pre in ["", "Matrix.", "Filter.", "Topology.", "TGLExt.", "TGLExt.TheUnitIsTheRank."] do
      let n := (pre ++ s).toName
      if env.contains n then IO.println s!"EXISTE {n}"
  IO.println "FIM"
