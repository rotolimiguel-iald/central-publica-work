import GeneralExpectationPositive

set_option autoImplicit false
set_option maxHeartbeats 1600000

namespace ChatgptAudit.Expectation047

open TGLExt Filter MeasureTheory
open ChatgptAudit.Aperiodic046
open scoped Topology ComplexOrder

noncomputable section

/-- The quadratic form of a finite operator block on arbitrary Hilbert vectors. -/
def blockQuadratic (P : SiteProfile) (k : ℕ)
    (A : Matrix (Fin k) (Fin k) (TowerHilbert P →L[ℂ] TowerHilbert P))
    (v : Fin k → TowerHilbert P) : ℂ :=
  ∑ i, ∑ j, inner ℂ (v i) (A i j (v j))

/-- Full block positivity; this is not entrywise positivity. -/
def BlockPositive (P : SiteProfile) (k : ℕ)
    (A : Matrix (Fin k) (Fin k) (TowerHilbert P →L[ℂ] TowerHilbert P)) : Prop :=
  (∀ i j, star (A i j) = A j i) ∧ ∀ v, 0 ≤ (blockQuadratic P k A v).re

theorem block_modular_quadratic (P : SiteProfile) (k : ℕ)
    (A : Matrix (Fin k) (Fin k) (TowerHilbert P →L[ℂ] TowerHilbert P))
    (t : ℝ) (v : Fin k → TowerHilbert P) :
    blockQuadratic P k (fun i j => modularConjugation P t (A i j)) v =
      blockQuadratic P k A (fun i => modularFlow P (-t) (v i)) := by
  simp only [blockQuadratic, modular_conjugation_inner]

/-- Finite sums and continuous real vector functionals commute with the actual averages. -/
theorem block_period_average_quadratic (P : SiteProfile) (k : ℕ)
    (A : Matrix (Fin k) (Fin k) (TowerHilbert P →L[ℂ] TowerHilbert P))
    (T : ℝ) (hT : 0 < T) (v : Fin k → TowerHilbert P) :
    (blockQuadratic P k (fun i j => periodAverage P T hT (A i j)) v).re =
      T⁻¹ * (∫ t in (0 : ℝ)..T,
        (blockQuadratic P k A (fun i => modularFlow P (-t) (v i))).re) := by
  have hi (i j : Fin k) :
      IntervalIntegrable
        (fun t : ℝ => (inner ℂ (v i) (modularConjugation P t (A i j) (v j))).re)
        volume 0 T :=
    (Complex.continuous_re.comp
      (modular_conjugation_inner_continuous P (A i j) (v i) (v j))).intervalIntegrable 0 T
  have hsum (i : Fin k) :
      IntervalIntegrable
        (fun t : ℝ => ∑ j, (inner ℂ (v i)
          (modularConjugation P t (A i j) (v j))).re) volume 0 T := by
    simpa only [Finset.sum_apply] using
      IntervalIntegrable.sum Finset.univ (fun j _ => hi i j)
  simp_rw [← block_modular_quadratic P k A, blockQuadratic, Complex.re_sum,
    period_average_re_inner]
  rw [intervalIntegral.integral_finsetSum (fun i _ => hsum i)]
  simp_rw [intervalIntegral.integral_finsetSum (fun j _ => hi _ j),
    Finset.mul_sum]

theorem block_period_average_nonnegative (P : SiteProfile) (k : ℕ)
    (A : Matrix (Fin k) (Fin k) (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hA : BlockPositive P k A) (T : ℝ) (hT : 0 < T)
    (v : Fin k → TowerHilbert P) :
    0 ≤ (blockQuadratic P k (fun i j => periodAverage P T hT (A i j)) v).re := by
  rw [block_period_average_quadratic P k A T hT v]
  exact mul_nonneg (inv_nonneg.mpr hT.le)
    (intervalIntegral.integral_nonneg_of_forall hT.le (fun t => hA.2 _))

/-- The block form converges because every entry converges strongly and the sums are finite. -/
theorem block_average_quadratic_tendsto (P : SiteProfile) (I : ExpectationInput P)
    (k : ℕ)
    (A : Matrix (Fin k) (Fin k) (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hmem : ∀ i j, A i j ∈ theFactorObject P) (v : Fin k → TowerHilbert P) :
    Tendsto
      (fun n : ℕ => (blockQuadratic P k
        (fun i j => periodAverage P ((n : ℝ) + 1) (by positivity) (A i j)) v).re)
      atTop (𝓝 (blockQuadratic P k (fun i j => I.E (A i j)) v).re) := by
  have he (i j : Fin k) : I.E (A i j) = aperiodicExpectation P (A i j) :=
    the_expectation_is_unique I (aperiodicExpectationInput P) (A i j) (hmem i j)
  have hentry (i j : Fin k) :
      Tendsto (fun n : ℕ =>
        inner ℂ (v i) (periodAverage P ((n : ℝ) + 1) (by positivity) (A i j) (v j)))
        atTop (𝓝 (inner ℂ (v i) (I.E (A i j) (v j)))) := by
    rw [he i j]
    exact (tendsto_const_nhds (x := v i)).inner (𝕜 := ℂ)
      ((aperiodic_expectation_spec P (A i j) (hmem i j)).2.2 (v j))
  have hs := tendsto_finsetSum Finset.univ
    (fun i _ => tendsto_finsetSum Finset.univ (fun j _ => hentry i j))
  exact (Complex.continuous_re.tendsto _).comp hs

/-- Every finite amplification preserves the full Hilbert block form. -/
theorem general_expectation_block_positive (P : SiteProfile) (I : ExpectationInput P)
    (k : ℕ)
    (A : Matrix (Fin k) (Fin k) (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hmem : ∀ i j, A i j ∈ theFactorObject P) (hA : BlockPositive P k A) :
    BlockPositive P k (fun i j => I.E (A i j)) := by
  constructor
  · intro i j
    rw [← expectation_star P I (A i j) (hmem i j), hA.1 i j]
  · intro v
    exact le_of_tendsto_of_tendsto tendsto_const_nhds
      (block_average_quadratic_tendsto P I k A hmem v)
      (Filter.Eventually.of_forall fun n =>
        block_period_average_nonnegative P k A hA ((n : ℝ) + 1) (by positivity) v)

/-- Gram blocks are nonvacuous examples of the full condition. -/
theorem gram_block_quadratic (P : SiteProfile) (k : ℕ)
    (B : Fin k → TowerHilbert P →L[ℂ] TowerHilbert P)
    (v : Fin k → TowerHilbert P) :
    blockQuadratic P k (fun i j => star (B i) * B j) v =
      inner ℂ (∑ i, B i (v i)) (∑ j, B j (v j)) := by
  simp only [blockQuadratic, mul_apply_eq_comp,
    ContinuousLinearMap.star_eq_adjoint, ContinuousLinearMap.adjoint_inner_right,
    sum_inner, inner_sum]
  exact Finset.sum_comm

theorem gram_block_positive (P : SiteProfile) (k : ℕ)
    (B : Fin k → TowerHilbert P →L[ℂ] TowerHilbert P) :
    BlockPositive P k (fun i j => star (B i) * B j) := by
  constructor
  · intro i j
    simp only [star_mul, star_star]
  · intro v
    rw [gram_block_quadratic]
    exact inner_self_nonneg (𝕜 := ℂ) (x := ∑ i, B i (v i))

#print axioms blockQuadratic
#print axioms BlockPositive
#print axioms block_modular_quadratic
#print axioms block_period_average_quadratic
#print axioms block_period_average_nonnegative
#print axioms block_average_quadratic_tendsto
#print axioms general_expectation_block_positive
#print axioms gram_block_quadratic
#print axioms gram_block_positive

end

end ChatgptAudit.Expectation047
