import ExpectationAlgebra
import Mathlib.Analysis.InnerProductSpace.Positive

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Expectation047

open TGLExt Filter MeasureTheory
open ChatgptAudit.Aperiodic046
open scoped Topology ComplexOrder

noncomputable section

/-- Simultaneous modular transport of both test vectors is the actual conjugation form. -/
theorem modular_conjugation_inner (P : SiteProfile) (t : ℝ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (v w : TowerHilbert P) :
    inner ℂ v (modularConjugation P t A w) =
      inner ℂ (modularFlow P (-t) v) (A (modularFlow P (-t) w)) := by
  have h := (modularFlowIsometry P t).inner_map_map
    (modularFlow P (-t) v) (A (modularFlow P (-t) w))
  change inner ℂ (modularFlow P t (modularFlow P (-t) v))
      (modularFlow P t (A (modularFlow P (-t) w))) = _ at h
  rw [modularFlow_group, add_neg_cancel, modularFlow_zero_time] at h
  exact h

theorem modular_conjugation_inner_continuous (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (v w : TowerHilbert P) :
    Continuous (fun t : ℝ => inner ℂ v (modularConjugation P t A w)) :=
  continuous_const.inner (modular_orbit_continuous A w)

/-- The continuous vector functional commutes with the finite-time average. -/
theorem period_average_inner (P : SiteProfile) (T : ℝ) (hT : 0 < T)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (v w : TowerHilbert P) :
    inner ℂ v (periodAverage P T hT A w) =
      T⁻¹ • (∫ t in (0 : ℝ)..T, inner ℂ v (modularConjugation P t A w)) := by
  rw [(period_average_operator T hT A).1]
  change (innerSL ℂ v)
      (T⁻¹ • (∫ t in (0 : ℝ)..T, modularConjugation P t A w)) = _
  rw [(innerSL ℂ v).map_smul_of_tower,
    ← (innerSL ℂ v).intervalIntegral_comp_comm
      ((modular_orbit_continuous A w).intervalIntegrable 0 T)]
  rfl

theorem period_average_re_inner (P : SiteProfile) (T : ℝ) (hT : 0 < T)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (v w : TowerHilbert P) :
    (inner ℂ v (periodAverage P T hT A w)).re =
      T⁻¹ * (∫ t in (0 : ℝ)..T, (inner ℂ v (modularConjugation P t A w)).re) := by
  have hi := Complex.reCLM.intervalIntegral_comp_comm (μ := volume)
    ((modular_conjugation_inner_continuous P A v w).intervalIntegrable 0 T)
  change (∫ t in (0 : ℝ)..T, (inner ℂ v (modularConjugation P t A w)).re) =
    (∫ t in (0 : ℝ)..T, inner ℂ v (modularConjugation P t A w)).re at hi
  rw [period_average_inner P T hT A v w]
  change Complex.reCLM
      (T⁻¹ • (∫ t in (0 : ℝ)..T, inner ℂ v (modularConjugation P t A w))) = _
  rw [Complex.reCLM.map_smul]
  change T⁻¹ * (∫ t in (0 : ℝ)..T, inner ℂ v (modularConjugation P t A w)).re = _
  rw [← hi]

/-- Positive input gives a nonnegative real diagonal form for every interval length T>0. -/
theorem period_average_re_inner_nonneg (P : SiteProfile) (T : ℝ) (hT : 0 < T)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A.IsPositive)
    (v : TowerHilbert P) :
    0 ≤ (inner ℂ v (periodAverage P T hT A v)).re := by
  rw [period_average_re_inner P T hT A v v]
  apply mul_nonneg (inv_nonneg.mpr hT.le)
  apply intervalIntegral.integral_nonneg_of_forall hT.le
  intro t
  rw [modular_conjugation_inner]
  exact hA.re_inner_nonneg_right _

/-- Nonnegativity passes through the strong limit; any contract agrees with the constructed one. -/
theorem expectation_re_inner_nonneg (P : SiteProfile) (I : ExpectationInput P)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : A ∈ theFactorObject P) (hA : A.IsPositive) (v : TowerHilbert P) :
    0 ≤ (inner ℂ v (I.E A v)).re := by
  have he : I.E A = aperiodicExpectation P A :=
    the_expectation_is_unique I (aperiodicExpectationInput P) A hmem
  rw [he]
  have hv := (aperiodic_expectation_spec P A hmem).2.2 v
  have hi := (tendsto_const_nhds (x := v)).inner (𝕜 := ℂ) hv
  have hr := (Complex.continuous_re.tendsto
    (inner ℂ v (aperiodicExpectation P A v))).comp hi
  change Tendsto
    (fun n : ℕ => (inner ℂ v
      (periodAverage P ((n : ℝ) + 1) (by positivity) A v)).re)
    atTop (𝓝 (inner ℂ v (aperiodicExpectation P A v)).re) at hr
  exact le_of_tendsto_of_tendsto tendsto_const_nhds hr
    (Filter.Eventually.of_forall fun n =>
      period_average_re_inner_nonneg P ((n : ℝ) + 1) (by positivity) A hA v)

/-- Positivity on the factor is proved from averages and adjoint preservation. -/
theorem general_expectation_isPositive (P : SiteProfile) (I : ExpectationInput P)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : A ∈ theFactorObject P) (hA : A.IsPositive) :
    (I.E A).IsPositive := by
  apply ContinuousLinearMap.isPositive_def'.mpr
  constructor
  · change star (I.E A) = I.E A
    rw [← expectation_star P I A hmem, hA.isSelfAdjoint.star_eq]
  · intro v
    change 0 ≤ RCLike.re (inner ℂ (I.E A v) v)
    rw [inner_re_symm]
    exact expectation_re_inner_nonneg P I A hmem hA v

/-- The order-theoretic form of positivity, restricted to the actual factor. -/
theorem general_expectation_nonnegative (P : SiteProfile) (I : ExpectationInput P)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : A ∈ theFactorObject P) (hA : 0 ≤ A) :
    0 ≤ I.E A := by
  apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
  exact general_expectation_isPositive P I A hmem
    ((ContinuousLinearMap.nonneg_iff_isPositive A).mp hA)

#print axioms modular_conjugation_inner
#print axioms modular_conjugation_inner_continuous
#print axioms period_average_inner
#print axioms period_average_re_inner
#print axioms period_average_re_inner_nonneg
#print axioms expectation_re_inner_nonneg
#print axioms general_expectation_isPositive
#print axioms general_expectation_nonnegative

end

end ChatgptAudit.Expectation047
