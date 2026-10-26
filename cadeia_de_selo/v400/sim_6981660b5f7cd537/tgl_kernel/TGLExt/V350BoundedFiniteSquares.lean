import TGLExt.V350BoundedDualValues
import TGLExt.V350DualSemifiniteIdeal

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 2200000

namespace TGLV350.Regular
open Filter MeasureTheory
open scoped Topology ENNReal NNReal
noncomputable section

/-- A finite square in the already constructed ideal has an actual bounded
positive value in the same fixed algebra, not only a finite quadratic reading. -/
theorem HasFiniteDualSquare.exists_bounded_value (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P))
    (hm : A ∈ regularCoreAlgebra P) (hfinite : HasFiniteDualSquare A) :
    ∃ B : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P),
      B ∈ dualFixedCore P ∧ 0 ≤ B ∧
      (∀ v, dualQuadraticIntegral (star A * A) v = ENNReal.ofReal (inner ℂ v (B v)).re) := by
  obtain ⟨C,hC⟩ := hfinite
  have hsq := (regularCoreAlgebra P).mul_mem
    ((regularCoreAlgebra P).toStarSubalgebra.star_mem' hm) hm
  obtain ⟨B,hmB,hB,_,hrep⟩ := exists_boundedDualValue_in_fixedCore P (star A*A)
    hsq (star_mul_self_nonneg A) (C : ℝ) C.property (fun v => by
      change dualQuadraticIntegral (star A * A) v ≤ ENNReal.ofReal ((C : ℝ) * ‖v‖ ^ 2)
      rw [ENNReal.ofReal_mul (show 0 ≤ (C : ℝ) from C.property),
        ENNReal.ofReal_coe_nnreal (p := C)]
      exact hC v)
  exact ⟨B,hmB,hB,hrep⟩

/-- Scalar identity values follow from the Fourier computation with its fixed
Haar normalization; the scalar coefficient is not chosen by the representative. -/
theorem regularAverage_bounded_value (P : TGLExt.SiteProfile) (h : ℝ) (hh : 0 < h) :
    let B : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P) :=
      h⁻¹ • 1
    B ∈ dualFixedCore P ∧ 0 ≤ B ∧
      (∀ v, dualQuadraticIntegral (star (regularAverage P h) * regularAverage P h) v =
        ENNReal.ofReal (inner ℂ v (B v)).re) := by
  dsimp only
  refine ⟨?_, ?_, ?_⟩
  · change ((h⁻¹ : ℝ) : ℂ) • (1 : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P)) ∈ dualFixedCore P
    exact (dualFixedCore P).toStarSubalgebra.smul_mem (dualFixedCore P).one_mem _
  · change 0 ≤ ((h⁻¹ : ℝ) : ℂ) • (1 : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P))
    apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
    exact ((ContinuousLinearMap.nonneg_iff_isPositive _).mp
      (zero_le_one : (0 : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
        RegularHilbert (TGLExt.TowerHilbert P)) ≤ 1)).smul_of_nonneg
      (by exact_mod_cast (inv_pos.mpr hh).le)
  · intro v
    rw [regularAverage_dualQuadraticIntegral P h hh v]
    congr 1
    change h⁻¹ * ‖v‖ ^ 2 = (inner ℂ v (((h⁻¹ : ℝ) : ℂ) • v)).re
    rw [inner_smul_right]
    simp only [Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero]
    rw [show (inner ℂ v v).re = ‖v‖ ^ 2 from inner_self_eq_norm_sq (𝕜 := ℂ) v]

/-- Every core operator is strongly approximated by square-finite inputs whose
values are bounded operators of F. This theorem does not identify F with the base
or assert the scalar canonical trace or the full operator-valued-weight interface. -/
theorem boundedFiniteSquares_strong_approximation (P : TGLExt.SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    (∀ h : ℝ, 0 < h → ∃ B : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
        RegularHilbert (TGLExt.TowerHilbert P),
      B ∈ dualFixedCore P ∧ 0 ≤ B ∧
      (∀ v, dualQuadraticIntegral
          (star (A.val * regularAverage P h) * (A.val * regularAverage P h)) v =
        ENNReal.ofReal (inner ℂ v (B v)).re)) ∧
    (∀ h : ℝ, A.val * regularAverage P h ∈ regularCoreAlgebra P) ∧
    (∀ v, Tendsto (fun h : ℝ => (A.val * regularAverage P h) v) (𝓝[>] 0) (𝓝 (A.val v))) := by
  obtain ⟨hf,hm,ht⟩ := finiteDualLeftIdeal_strong_approximation P A
  exact ⟨fun h hh => HasFiniteDualSquare.exists_bounded_value P _ (hm h) (hf h hh),hm,ht⟩

#print axioms HasFiniteDualSquare.exists_bounded_value
#print axioms regularAverage_bounded_value
#print axioms boundedFiniteSquares_strong_approximation
end
end TGLV350.Regular
