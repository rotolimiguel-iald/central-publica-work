import SelectionOutcomeRecord

set_option autoImplicit false
set_option maxHeartbeats 600000

namespace ChatgptAudit.ScatteringRecord
open Matrix Complex TGLExt ChatgptAudit.SelectionAngle ChatgptAudit.SelectionRecord
  ChatgptAudit.Collapse057
open scoped ComplexOrder
noncomputable section

/-- The outgoing column of the canonical S matrix for the incident channel e1. -/
def outgoingColumn (θ : ℝ) : Matrix (Fin 2) (Fin 1) ℂ :=
  fun i _ => (Smat θ).mulVec e1 i

theorem canonical_density_is_outgoing_outer_product (θ : ℝ) :
    rhoOut θ = outgoingColumn θ * (outgoingColumn θ)ᴴ := by
  rw [rhoOut_eq]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [outgoingColumn, Matrix.mul_apply, Matrix.conjTranspose_apply,
      Smat_transmission, Smat_reflection, pow_two] <;> ring

theorem canonical_scattering_density_positive (θ : ℝ) :
    (rhoOut θ).PosSemidef := by
  rw [canonical_density_is_outgoing_outer_product]
  exact Matrix.posSemidef_self_mul_conjTranspose (outgoingColumn θ)

/-- A genuine member of the canonical positive trace-one state type. -/
def scatteringDensity (θ : ℝ) : QubitDensity :=
  ⟨rhoOut θ, canonical_scattering_density_positive θ, rhoOut_trace θ⟩

/-- The selected probability is transmission for label 0, reflection for label 1. -/
def selectedProbability (p : ℝ) (outcome : Fin 2) : ℝ :=
  if outcome = 0 then 1 - p else p

def scatteringRecord (p : ℝ) (outcome : Fin 2) : WeightedPhaseRecord :=
  ⟨selectedProbability p outcome, phaseReading (Smat (selectionAngle p)), outcome⟩

/-- Reflection weight can be recovered from a branch weight only with its label. -/
def recoveredReflectionWeight (r : WeightedPhaseRecord) : ℝ :=
  if r.outcome = 0 then 1 - r.weight else r.weight

theorem selected_probabilities_normalized (p : ℝ) :
    selectedProbability p 0 + selectedProbability p 1 = 1 := by
  simp [selectedProbability]

theorem selected_probability_range {p : ℝ} (h0 : 0 ≤ p) (h1 : p ≤ 1)
    (outcome : Fin 2) :
    0 ≤ selectedProbability p outcome ∧ selectedProbability p outcome ≤ 1 := by
  fin_cases outcome <;> simp [selectedProbability] <;> constructor <;> linarith

theorem scattering_record_recovers_reflection_weight (p : ℝ) (outcome : Fin 2) :
    recoveredReflectionWeight (scatteringRecord p outcome) = p := by
  fin_cases outcome <;> simp [recoveredReflectionWeight, scatteringRecord, selectedProbability]

theorem scattering_record_decodes_form_and_label (p : ℝ) (outcome : Fin 2) :
    decodeRecord (scatteringRecord p outcome) = (Smat (selectionAngle p), outcome) := by
  change (angularDecoder (phaseReading (Smat (selectionAngle p))), outcome) = _
  rw [← angular_form_is_the_boundary_s_matrix]
  rw [angular_family_reconstructed_from_one_selected_face]

theorem canonical_branch_weight_is_selected_probability {p : ℝ}
    (h0 : 0 ≤ p) (h1 : p ≤ 1) (outcome : Fin 2) :
    branchWeight (rhoOut (selectionAngle p)) outcome =
      (selectedProbability p outcome : ℂ) := by
  fin_cases outcome
  · change rhoOut (selectionAngle p) 0 0 = ((1 - p : ℝ) : ℂ)
    rw [rhoOut_zero_zero]
    exact_mod_cast selection_angle_transmission h0 h1
  · change rhoOut (selectionAngle p) 1 1 = (p : ℂ)
    rw [rhoOut_one_one]
    exact_mod_cast selection_angle_reflection h0 h1

theorem scattering_record_matches_canonical_branch {p : ℝ}
    (h0 : 0 ≤ p) (h1 : p ≤ 1) (outcome : Fin 2) :
    recordMatchesBranch (scatteringDensity (selectionAngle p)).val
      (scatteringRecord p outcome) :=
  canonical_branch_weight_is_selected_probability h0 h1 outcome

theorem scattering_record_reconstructs_branch {p : ℝ}
    (h0 : 0 ≤ p) (h1 : p ≤ 1) (outcome : Fin 2) :
    ((scatteringRecord p outcome).weight : ℂ) • recordReadout (scatteringRecord p outcome) =
      unnormalizedBranch (rhoOut (selectionAngle p)) outcome :=
  matching_record_reconstructs_unnormalized_branch _ _
    (scattering_record_matches_canonical_branch h0 h1 outcome)

theorem scattering_record_normalizes_nonzero_branch {p : ℝ}
    (h0 : 0 ≤ p) (h1 : p ≤ 1) (outcome : Fin 2)
    (hp : selectedProbability p outcome ≠ 0) :
    (branchWeight (rhoOut (selectionAngle p)) outcome)⁻¹ •
      unnormalizedBranch (rhoOut (selectionAngle p)) outcome =
        recordReadout (scatteringRecord p outcome) :=
  matching_nonzero_record_reconstructs_normalized_branch _ _
    (scattering_record_matches_canonical_branch h0 h1 outcome) hp

theorem scattering_record_zero_weight_zero_branch {p : ℝ}
    (h0 : 0 ≤ p) (h1 : p ≤ 1) (outcome : Fin 2)
    (hp : selectedProbability p outcome = 0) :
    unnormalizedBranch (rhoOut (selectionAngle p)) outcome = 0 :=
  matching_zero_record_has_zero_branch _ _
    (scattering_record_matches_canonical_branch h0 h1 outcome) hp

theorem fair_scattering_records_equal_fair_records (outcome : Fin 2) :
    scatteringRecord (1 / 2) outcome = fairRecord outcome := by
  fin_cases outcome <;> norm_num [scatteringRecord, selectedProbability, fairRecord, selectionRecord]

theorem fair_scattering_labels_remain_distinct :
    scatteringRecord (1 / 2) 0 ≠ scatteringRecord (1 / 2) 1 := by
  rw [fair_scattering_records_equal_fair_records, fair_scattering_records_equal_fair_records]
  exact fair_records_are_distinct

theorem scattering_record_parameters_are_recovered (p : ℝ) (outcome : Fin 2) :
    (recoveredReflectionWeight (scatteringRecord p outcome),
      (scatteringRecord p outcome).outcome) = (p, outcome) := by
  rw [scattering_record_recovers_reflection_weight]
  rfl

theorem scattering_record_separates_parameters {p q : ℝ} {i j : Fin 2}
    (h : scatteringRecord p i = scatteringRecord q j) : p = q ∧ i = j := by
  have hp := congrArg recoveredReflectionWeight h
  rw [scattering_record_recovers_reflection_weight,
    scattering_record_recovers_reflection_weight] at hp
  exact ⟨hp, congrArg WeightedPhaseRecord.outcome h⟩

#print axioms outgoingColumn
#print axioms canonical_density_is_outgoing_outer_product
#print axioms canonical_scattering_density_positive
#print axioms scatteringDensity
#print axioms selectedProbability
#print axioms scatteringRecord
#print axioms recoveredReflectionWeight
#print axioms selected_probabilities_normalized
#print axioms selected_probability_range
#print axioms scattering_record_recovers_reflection_weight
#print axioms scattering_record_decodes_form_and_label
#print axioms canonical_branch_weight_is_selected_probability
#print axioms scattering_record_matches_canonical_branch
#print axioms scattering_record_reconstructs_branch
#print axioms scattering_record_normalizes_nonzero_branch
#print axioms scattering_record_zero_weight_zero_branch
#print axioms fair_scattering_records_equal_fair_records
#print axioms fair_scattering_labels_remain_distinct
#print axioms scattering_record_parameters_are_recovered
#print axioms scattering_record_separates_parameters

end
end ChatgptAudit.ScatteringRecord
