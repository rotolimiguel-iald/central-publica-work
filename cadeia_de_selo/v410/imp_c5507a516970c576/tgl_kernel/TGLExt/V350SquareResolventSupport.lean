import TGLExt.V350DualResolvent
import TGLExt.V350ScaledPositiveResolvent

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 200000

namespace TGLV350.Regular
open Filter
open scoped Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Rational cutoffs for a bounded operator; the theorems require selfadjointness. -/
def squareResolvent (A : H →L[ℂ] H) (n : ℕ) : H →L[ℂ] H :=
  positiveResolvent (((n : ℝ)+1) • (A*A))

private theorem selfadjointSquare_nonneg (A : H →L[ℂ] H) (hA : star A = A) :
    0 ≤ A*A := by
  simpa only [hA] using star_mul_self_nonneg A

private theorem scaledSelfadjointSquare_nonneg (A : H →L[ℂ] H)
    (hA : star A = A) (n : ℕ) : 0 ≤ ((n : ℝ)+1) • (A*A) :=
  smul_nonneg (by positivity) (selfadjointSquare_nonneg A hA)

theorem squareResolvent_nonneg (A : H →L[ℂ] H) (hA : star A = A) (n : ℕ) :
    0 ≤ squareResolvent A n :=
  positiveResolvent_nonneg _ (scaledSelfadjointSquare_nonneg A hA n)

theorem squareResolvent_le_one (A : H →L[ℂ] H) (hA : star A = A) (n : ℕ) :
    squareResolvent A n ≤ 1 :=
  positiveResolvent_le_one _ (scaledSelfadjointSquare_nonneg A hA n)

theorem squareResolvent_antitone (A : H →L[ℂ] H) (hA : star A = A) :
    Antitone (squareResolvent A) := by
  intro n m hnm
  apply positiveResolvent_antitone (scaledSelfadjointSquare_nonneg A hA n)
  exact smul_le_smul_of_nonneg_right
    (show (n : ℝ)+1 ≤ (m : ℝ)+1 by
      have hc : (n : ℝ) ≤ m := by exact_mod_cast hnm
      linarith)
    (selfadjointSquare_nonneg A hA)

theorem squareResolvent_commutes (A : H →L[ℂ] H) (hA : star A = A) (n : ℕ) :
    Commute A (squareResolvent A n) := by
  apply ring_inverse_commutes_of_unit
  · change A * (1 + ((n : ℝ)+1) • (A*A)) =
      (1 + ((n : ℝ)+1) • (A*A)) * A
    simp only [mul_add, add_mul, mul_smul_comm, smul_mul_assoc, mul_one, one_mul,
      mul_assoc]
  · exact (one_add_strictlyPositive _ (scaledSelfadjointSquare_nonneg A hA n)).isUnit

/-- The energy bound does not assume an injective A or a spectral gap. -/
theorem squareResolvent_energy_bound (A : H →L[ℂ] H) (hA : star A = A)
    (n : ℕ) (v : H) :
    ((n : ℝ)+1) * ‖squareResolvent A n (A v)‖^2 ≤ ‖v‖^2 / 4 := by
  have hsym := ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mp hA
  have hinner : (inner ℂ (squareResolvent A n v)
      (A (A (squareResolvent A n v)))).re = ‖A (squareResolvent A n v)‖^2 := by
    exact (congrArg Complex.re (hsym (squareResolvent A n v)
      (A (squareResolvent A n v)))).symm.trans (inner_self_eq_norm_sq (𝕜 := ℂ) _)
  have he := positiveResolvent_energy_bound _ (scaledSelfadjointSquare_nonneg A hA n) v
  change (inner ℂ (squareResolvent A n v)
    (((((n : ℝ)+1) : ℝ) : ℂ) • A (A (squareResolvent A n v)))).re ≤ _ at he
  simp only [inner_smul_right, Complex.mul_re, Complex.ofReal_re,
    Complex.ofReal_im, zero_mul, sub_zero] at he
  rw [hinner] at he
  have hc := congrArg (fun T : H →L[ℂ] H => T v) (squareResolvent_commutes A hA n).eq
  change A (squareResolvent A n v) = squareResolvent A n (A v) at hc
  rwa [hc] at he

private theorem annihilatesRangeFromEnergy (A L : H →L[ℂ] H) (hA : star A = A)
    (ht : ∀ v, Tendsto (fun n => squareResolvent A n v) atTop (𝓝 (L v)))
    (v : H) : L (A v) = 0 := by
  have hb : ∀ k : ℕ, (k : ℝ) * ‖L (A v)‖^2 ≤ ‖v‖^2 / 4 := by
    intro k
    apply le_of_tendsto ((ht (A v)).norm.pow 2 |>.const_mul (k : ℝ))
    filter_upwards [eventually_ge_atTop k] with n hkn
    exact (mul_le_mul_of_nonneg_right
      (show (k : ℝ) ≤ (n : ℝ)+1 by exact_mod_cast Nat.le_succ_of_le hkn)
      (sq_nonneg _)).trans (squareResolvent_energy_bound A hA n v)
  have hz : ‖L (A v)‖^2 = 0 := by
    by_contra hn
    have hp : 0 < ‖L (A v)‖^2 := lt_of_le_of_ne (sq_nonneg _) (Ne.symm hn)
    obtain ⟨k,hk⟩ := exists_nat_gt ((‖v‖^2 / 4) / ‖L (A v)‖^2)
    have hc := (div_lt_iff₀ hp).mp hk
    exact (not_lt_of_ge (hb k)) hc
  exact norm_eq_zero.mp (sq_eq_zero_iff.mp hz)

/-- Strong convergence to zero on the support. No operator-norm convergence is claimed. -/
theorem squareResolvent_tendsto_zero_on_rangeClosure (A : H →L[ℂ] H)
    (hA : star A = A) (x : H) (hx : x ∈ closure (Set.range A)) :
    Tendsto (fun n => squareResolvent A n x) atTop (𝓝 0) := by
  obtain ⟨L,_,_,_,ht,_⟩ := vonNeumann_antitone_contraction_limit
    (generatedAlgebra (Set.univ : Set (H →L[ℂ] H))) (squareResolvent A)
    (fun n => generator_mem (Set.mem_univ (squareResolvent A n)))
    (squareResolvent_nonneg A hA) (squareResolvent_le_one A hA)
    (squareResolvent_antitone A hA)
  have hr : closure (Set.range A) ⊆ {x : H | L x = 0} := by
    apply closure_minimal
    · rintro _ ⟨v,rfl⟩
      exact annihilatesRangeFromEnergy A L hA ht v
    · exact isClosed_eq L.continuous continuous_const
  have hx0 : L x = 0 := hr hx
  simpa only [hx0] using ht x

#print axioms squareResolvent_nonneg
#print axioms squareResolvent_le_one
#print axioms squareResolvent_antitone
#print axioms squareResolvent_commutes
#print axioms squareResolvent_energy_bound
#print axioms squareResolvent_tendsto_zero_on_rangeClosure
end
end TGLV350.Regular
