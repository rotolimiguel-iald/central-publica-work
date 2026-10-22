import CollapseContract
import Mathlib.Analysis.Complex.ExponentialBounds

set_option autoImplicit false
namespace ChatgptAudit.Collapse057

/-- Dimensionless proposed TGL cost law. Separate components; no implicit addition. -/
structure CollapseCostLaw where
  localNats : ℝ
  octaveNats : ℕ → ℝ
  local_half : localNats = 1 / 2
  per_octave : ∀ n, octaveNats n = (n : ℝ) * Real.log 2

noncomputable def proposedCollapseCost : CollapseCostLaw where
  localNats := 1 / 2
  octaveNats := fun n => (n : ℝ) * Real.log 2
  local_half := rfl
  per_octave := fun _ => rfl

theorem proposed_cost_components (K : CollapseCostLaw) (n : ℕ) :
    K.localNats = 1 / 2 ∧ K.octaveNats n = (n : ℝ) * Real.log 2 :=
  ⟨K.local_half, K.per_octave n⟩

theorem local_cost_positive (K : CollapseCostLaw) : 0 < K.localNats := by
  rw [K.local_half]; norm_num

theorem octave_cost_zero (K : CollapseCostLaw) : K.octaveNats 0 = 0 := by
  rw [K.per_octave]; simp

theorem octave_cost_add (K : CollapseCostLaw) (m n : ℕ) :
    K.octaveNats (m + n) = K.octaveNats m + K.octaveNats n := by
  simp only [K.per_octave, Nat.cast_add, add_mul]

theorem octave_cost_positive (K : CollapseCostLaw) {n : ℕ} (hn : 0 < n) :
    0 < K.octaveNats n := by
  rw [K.per_octave]
  exact mul_pos (by exact_mod_cast hn) (Real.log_pos (by norm_num))

theorem local_is_not_one_octave (K : CollapseCostLaw) :
    K.localNats < K.octaveNats 1 := by
  rw [K.local_half, K.per_octave]
  norm_num only [Nat.cast_one, one_mul]
  linarith [Real.log_two_gt_d9]

/-- Entropy of the fair binary distribution, in nats. -/
noncomputable def fairBitEntropy : ℝ :=
  -((1 / 2 : ℝ) * Real.log (1 / 2) + (1 / 2 : ℝ) * Real.log (1 / 2))

theorem fair_bit_entropy_is_log_two : fairBitEntropy = Real.log 2 := by
  simp only [fairBitEntropy, one_div, Real.log_inv]
  ring

theorem fair_bit_entropy_is_not_half_nat : fairBitEntropy ≠ (1 / 2 : ℝ) := by
  rw [fair_bit_entropy_is_log_two]
  have h := Real.log_two_gt_d9
  linarith

/-- Logical collapse alone supplies no numerical cost observable or calibration. -/
theorem logical_core_allows_distinct_nonnegative_cost_readings {S I : Type}
    (C : IdentityCollapse S I) :
    ∃ a b : S → ℝ, (∀ x, 0 ≤ a x) ∧ (∀ x, 0 ≤ b x) ∧ a ≠ b := by
  obtain ⟨x, _⟩ := C.effective
  refine ⟨fun _ => 0, fun _ => 1, fun _ => le_rfl, fun _ => by norm_num, ?_⟩
  intro h
  have hx := congrFun h x
  norm_num at hx

/-- Physical provenance is a separate predicate supplied by the observer's protocol. -/
structure ReflectionProtocol (State Record Agent : Type) where
  outputReading : State → Record
  producer : Agent
  recorder : Record → Agent
  externallyValidated : State → State → Record → Prop

/-- Evidence links an actual changed transition to its recorded output. -/
structure AttestedCollapse {S I R A : Type}
    (C : IdentityCollapse S I) (P : ReflectionProtocol S R A) (before after : S) where
  transition : CollapseTransition C before after
  record : R
  reflected : record = P.outputReading after
  different_recorder : P.recorder record ≠ P.producer
  validated : P.externallyValidated before after record

theorem attestation_requires_external_evidence {S I R A : Type}
    (C : IdentityCollapse S I) (P : ReflectionProtocol S R A)
    {before after : S} (h : AttestedCollapse C P before after) :
    ∃ r, r = P.outputReading after ∧ P.recorder r ≠ P.producer ∧
      P.externallyValidated before after r :=
  ⟨h.record, h.reflected, h.different_recorder, h.validated⟩

theorem no_self_attestation {S I R A : Type}
    (C : IdentityCollapse S I) (P : ReflectionProtocol S R A)
    {before after : S}
    (self : ∀ r, P.recorder r = P.producer) :
    ¬ Nonempty (AttestedCollapse C P before after) := by
  rintro ⟨h⟩
  exact h.different_recorder (self h.record)

theorem missing_external_evidence_blocks_attestation {S I R A : Type}
    (C : IdentityCollapse S I) (P : ReflectionProtocol S R A)
    {before after : S} (missing : ∀ r, ¬ P.externallyValidated before after r) :
    ¬ Nonempty (AttestedCollapse C P before after) := by
  rintro ⟨h⟩
  exact missing h.record h.validated

theorem attested_output_stable_and_identity_preserved {S I R A : Type}
    (C : IdentityCollapse S I) (P : ReflectionProtocol S R A)
    {before after : S} (h : AttestedCollapse C P before after) :
    C.identity after = C.identity before ∧ C.step after = after :=
  transition_preserves_identity_and_is_fixed C h.transition

#print axioms CollapseCostLaw
#print axioms proposedCollapseCost
#print axioms proposed_cost_components
#print axioms local_cost_positive
#print axioms octave_cost_zero
#print axioms octave_cost_add
#print axioms octave_cost_positive
#print axioms local_is_not_one_octave
#print axioms fairBitEntropy
#print axioms fair_bit_entropy_is_log_two
#print axioms fair_bit_entropy_is_not_half_nat
#print axioms logical_core_allows_distinct_nonnegative_cost_readings
#print axioms ReflectionProtocol
#print axioms AttestedCollapse
#print axioms attestation_requires_external_evidence
#print axioms no_self_attestation
#print axioms missing_external_evidence_blocks_attestation
#print axioms attested_output_stable_and_identity_preserved
end ChatgptAudit.Collapse057
