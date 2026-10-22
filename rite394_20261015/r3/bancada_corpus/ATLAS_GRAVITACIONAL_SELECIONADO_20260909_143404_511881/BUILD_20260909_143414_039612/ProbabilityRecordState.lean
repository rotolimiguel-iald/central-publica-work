import GeneralAngularTensorCodec
import TGLExt.DiagonalStateCurve

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit.ProbabilityRecordState
open Matrix Set TGLExt ChatgptAudit.AngularTensorCodec ChatgptAudit.Micro021
open scoped ContDiff
noncomputable section

abbrev StateIndex := (Fin 4 × Fin 4) × Fin 2

/-- Uniformly labelled Bernoulli components; branch one is reflection. -/
def labelledState (p : Tensor4) (k : StateIndex) : ℝ :=
  if k.2 = 1 then p k.1.1 k.1.2 / 16 else (1 - p k.1.1 k.1.2) / 16

def recordState {U : Set Coordinate4} (R : ProbabilityFieldRecord U) :
    Coordinate4 → StateIndex → ℝ :=
  fun x => labelledState (R.probabilities x)

theorem labelled_state_reflection (p : Tensor4) (i j : Fin 4) :
    labelledState p ((i,j),1) = p i j / 16 := by
  simp [labelledState]

theorem labelled_state_transmission (p : Tensor4) (i j : Fin 4) :
    labelledState p ((i,j),0) = (1-p i j) / 16 := by
  simp [labelledState]

theorem labelled_state_pair_mass (p : Tensor4) (a : Fin 4 × Fin 4) :
    (∑ b : Fin 2, labelledState p (a,b)) = 1/16 := by
  simp only [Fin.sum_univ_two]
  rw [labelled_state_transmission, labelled_state_reflection]
  ring

theorem labelled_state_normalized (p : Tensor4) :
    ∑ k : StateIndex, labelledState p k = 1 := by
  rw [Fintype.sum_prod_type]
  simp only [labelled_state_pair_mass]
  norm_num

theorem record_state_normalized {U : Set Coordinate4} (R : ProbabilityFieldRecord U) :
    ∀ x, ∑ k : StateIndex, recordState R x k = 1 := by
  intro x
  exact labelled_state_normalized (R.probabilities x)

theorem record_state_positive {U : Set Coordinate4} (R : ProbabilityFieldRecord U) :
    ∀ x ∈ U, ∀ k : StateIndex, 0 < recordState R x k := by
  intro x hx k
  obtain ⟨hp, hq⟩ := R.interior x hx k.1.1 k.1.2
  unfold recordState labelledState
  split_ifs <;> positivity

theorem record_state_smooth {U : Set Coordinate4} (R : ProbabilityFieldRecord U) :
    ∀ k : StateIndex, ContDiffOn ℝ ∞ (fun x => recordState R x k) U := by
  intro k
  unfold recordState labelledState
  split_ifs
  · exact (R.smooth k.1.1 k.1.2).div_const 16
  · exact (contDiffOn_const.sub (R.smooth k.1.1 k.1.2)).div_const 16

theorem record_state_recovers_probability {U : Set Coordinate4}
    (R : ProbabilityFieldRecord U) (x : Coordinate4) (i j : Fin 4) :
    16 * recordState R x ((i,j),1) = R.probabilities x i j := by
  unfold recordState
  rw [labelled_state_reflection]
  ring

/-- The inverse reads only the reflected weight of each labelled pair. -/
def stateProbabilities (Q : StateIndex → ℝ) : Tensor4 :=
  fun i j => 16 * Q ((i,j),1)

theorem state_probabilities_of_labelled_state (p : Tensor4) :
    stateProbabilities (labelledState p) = p := by
  funext i j
  unfold stateProbabilities
  rw [labelled_state_reflection]
  ring

theorem labelled_state_of_state_probabilities (Q : StateIndex → ℝ)
    (hpair : ∀ a : Fin 4 × Fin 4, Q (a,0) + Q (a,1) = 1/16) :
    labelledState (stateProbabilities Q) = Q := by
  funext k
  obtain ⟨⟨i,j⟩,b⟩ := k
  by_cases hb : b = 1
  · subst b
    rw [labelled_state_reflection]
    unfold stateProbabilities
    ring
  · have hb0 : b = 0 := by omega
    subst b
    rw [labelled_state_transmission]
    unfold stateProbabilities
    have h := hpair (i,j)
    linarith

theorem labelled_state_injective : Function.Injective labelledState := by
  intro p q h
  simpa only [state_probabilities_of_labelled_state] using congrArg stateProbabilities h

theorem record_state_equality_iff {U : Set Coordinate4} (R S : ProbabilityFieldRecord U) :
    recordState R = recordState S ↔ R.probabilities = S.probabilities := by
  constructor
  · intro h
    funext x
    apply labelled_state_injective
    exact congrFun h x
  · intro h
    unfold recordState
    rw [h]

theorem record_state_eqOn_iff {U : Set Coordinate4} (R S : ProbabilityFieldRecord U) :
    Set.EqOn (recordState R) (recordState S) U ↔
      Set.EqOn R.probabilities S.probabilities U := by
  constructor
  · intro h x hx
    exact labelled_state_injective (h hx)
  · intro h x hx
    exact congrArg labelledState (h hx)

theorem record_state_injective {U : Set Coordinate4} :
    Function.Injective (@recordState U) := by
  intro R S h
  have hp := (record_state_equality_iff R S).mp h
  cases R
  cases S
  cases hp
  rfl

def stateProbabilityField (Q : Coordinate4 → StateIndex → ℝ) : TensorField4 :=
  fun x => stateProbabilities (Q x)

theorem state_probability_field_of_record {U : Set Coordinate4} (R : ProbabilityFieldRecord U) :
    stateProbabilityField (recordState R) = R.probabilities := by
  funext x
  exact state_probabilities_of_labelled_state (R.probabilities x)

theorem decode_record_from_state {U : Set Coordinate4} (R : ProbabilityFieldRecord U) :
    decodeTensorField (stateProbabilityField (recordState R)) = decodeRecord R := by
  rw [state_probability_field_of_record]
  rfl

theorem same_state_same_decoded_metric_on {U : Set Coordinate4}
    (R S : ProbabilityFieldRecord U) (h : Set.EqOn (recordState R) (recordState S) U) :
    Set.EqOn (decodeRecord R) (decodeRecord S) U :=
  same_probabilities_same_decoded_field R S ((record_state_eqOn_iff R S).mp h)

/-- The differential of the labelled state applies the same fixed normalization. -/
def labelledTangent (w : Tensor4) (k : StateIndex) : ℝ :=
  if k.2 = 1 then w k.1.1 k.1.2 / 16 else -(w k.1.1 k.1.2) / 16

theorem labelled_state_derivative (p : ℝ → Tensor4) (w : Tensor4) (t : ℝ)
    (h : ∀ i j, HasDerivAt (fun s => p s i j) (w i j) t) :
    ∀ k : StateIndex, HasDerivAt
      (fun s => labelledState (p s) k) (labelledTangent w k) t := by
  intro k
  by_cases hk : k.2 = 1
  · simpa only [labelledState, labelledTangent, hk, if_true] using
      (h k.1.1 k.1.2).div_const 16
  · simpa only [labelledState, labelledTangent, hk, if_false] using
      ((h k.1.1 k.1.2).const_sub 1).div_const 16

/-- Fisher is the mean of the sixteen Bernoulli contributions, not their unscaled sum. -/
theorem labelled_state_fisher_average (p w : Tensor4)
    (hp : ∀ i j, 0 < p i j ∧ p i j < 1) :
    diagonalFisher (labelledState p) (labelledTangent w) =
      (1/16) * ∑ a : Fin 4 × Fin 4, (w a.1 a.2)^2 /
        (p a.1 a.2 * (1 - p a.1 a.2)) := by
  unfold diagonalFisher
  rw [Fintype.sum_prod_type, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro a _
  simp only [Fin.sum_univ_two, labelledState, labelledTangent]
  norm_num
  have hpn : p a.1 a.2 ≠ 0 := ne_of_gt (hp a.1 a.2).1
  have hqn : 1 - p a.1 a.2 ≠ 0 := ne_of_gt (sub_pos.mpr (hp a.1 a.2).2)
  field_simp [hpn, hqn]
  ring

#print axioms StateIndex
#print axioms labelledState
#print axioms recordState
#print axioms labelled_state_reflection
#print axioms labelled_state_transmission
#print axioms labelled_state_pair_mass
#print axioms labelled_state_normalized
#print axioms record_state_normalized
#print axioms record_state_positive
#print axioms record_state_smooth
#print axioms record_state_recovers_probability
#print axioms stateProbabilities
#print axioms state_probabilities_of_labelled_state
#print axioms labelled_state_of_state_probabilities
#print axioms labelled_state_injective
#print axioms record_state_equality_iff
#print axioms record_state_eqOn_iff
#print axioms record_state_injective
#print axioms stateProbabilityField
#print axioms state_probability_field_of_record
#print axioms decode_record_from_state
#print axioms same_state_same_decoded_metric_on
#print axioms labelledTangent
#print axioms labelled_state_derivative
#print axioms labelled_state_fisher_average

end
end ChatgptAudit.ProbabilityRecordState
