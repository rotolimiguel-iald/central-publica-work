import TGLExt.V350DualWeightCuts
import Mathlib.MeasureTheory.Group.LIntegral
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1400000

namespace TGLV350.Regular
open MeasureTheory
open scoped ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Dual Haar normalization for Lebesgue dt and characters exp(-i*s*t).
This fixes the Fourier convention; it is not a normalization by cutoff length. -/
def dualHaarFactor : ℝ := (2 * Real.pi)⁻¹

theorem dualHaarFactor_pos : 0 < dualHaarFactor := by
  unfold dualHaarFactor
  positivity

def normalizedDualCut (R : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) :=
  dualHaarFactor • dualWeightCut R A

theorem normalizedDualCut_nonneg (R : ℝ) (hR : 0 ≤ R)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) :
    0 ≤ normalizedDualCut R A := by
  change 0 ≤ (dualHaarFactor : ℂ) • dualWeightCut R A
  rw [ContinuousLinearMap.nonneg_iff_isPositive]
  exact ((ContinuousLinearMap.nonneg_iff_isPositive _).mp
    (dualWeightCut_nonneg R hR A hA)).smul_of_nonneg
    (by exact_mod_cast dualHaarFactor_pos.le)

theorem normalizedDualCut_mem (P : TGLExt.SiteProfile) (R : ℝ)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P)) (hA : A ∈ regularCoreAlgebra P) :
    normalizedDualCut R A ∈ regularCoreAlgebra P := by
  change ((dualHaarFactor : ℂ) • dualWeightCut R A) ∈ regularCoreAlgebra P
  exact (regularCoreAlgebra P).toStarSubalgebra.smul_mem (dualWeightCut_mem P R A hA) _

def dualQuadraticIntegrand (A : RegularHilbert H →L[ℂ] RegularHilbert H)
    (v : RegularHilbert H) (s : ℝ) : ℝ≥0∞ :=
  ENNReal.ofReal (inner ℂ v (dualAmbient s A v)).re

theorem dualQuadraticIntegrand_measurable
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    Measurable (dualQuadraticIntegrand A v) :=
  (ENNReal.continuous_ofReal.comp (Complex.continuous_re.comp
    (continuous_const.inner (dualAmbient_strongly_continuous A v)))).measurable

theorem dualQuadratic_nonneg (A : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hA : 0 ≤ A) (v : RegularHilbert H) (s : ℝ) :
    0 ≤ (inner ℂ v (dualAmbient s A v)).re :=
  ((ContinuousLinearMap.nonneg_iff_isPositive _).mp
    (dualAmbient_nonneg s A hA)).re_inner_nonneg_right v

/-- Extended integral of quadratic evaluations on the actual regular Hilbert space.
The positive-input laws are proved below. This is not yet an operator-valued weight
with values in the base algebra, nor a faithful normal semifinite scalar trace. -/
def dualQuadraticIntegral (A : RegularHilbert H →L[ℂ] RegularHilbert H)
    (v : RegularHilbert H) : ℝ≥0∞ :=
  ENNReal.ofReal dualHaarFactor * ∫⁻ s : ℝ, dualQuadraticIntegrand A v s

theorem dualQuadraticIntegral_zero (v : RegularHilbert H) :
    dualQuadraticIntegral (0 : RegularHilbert H →L[ℂ] RegularHilbert H) v = 0 := by
  simp [dualQuadraticIntegral, dualQuadraticIntegrand]

theorem dualQuadraticIntegral_zero_vector
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) : dualQuadraticIntegral A 0 = 0 := by
  simp [dualQuadraticIntegral, dualQuadraticIntegrand]

theorem dualQuadraticIntegral_add
    (A B : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hB : 0 ≤ B)
    (v : RegularHilbert H) :
    dualQuadraticIntegral (A+B) v = dualQuadraticIntegral A v + dualQuadraticIntegral B v := by
  have heq : dualQuadraticIntegrand (A+B) v =
      fun s => dualQuadraticIntegrand A v s + dualQuadraticIntegrand B v s := by
    funext s
    simp only [dualQuadraticIntegrand, map_add, add_apply,
      inner_add_right, Complex.add_re]
    exact ENNReal.ofReal_add (dualQuadratic_nonneg A hA v s) (dualQuadratic_nonneg B hB v s)
  simp only [dualQuadraticIntegral, heq,
    lintegral_add_left (dualQuadraticIntegrand_measurable A v), mul_add]

theorem dualQuadraticIntegral_dual_invariant (r : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    dualQuadraticIntegral (dualAmbient r A) v = dualQuadraticIntegral A v := by
  have heq : dualQuadraticIntegrand (dualAmbient r A) v =
      fun s => dualQuadraticIntegrand A v (r+s) := by
    funext s
    simp only [dualQuadraticIntegrand, dualAmbient_add, StarAlgEquiv.trans_apply]
  unfold dualQuadraticIntegral
  rw [heq, lintegral_add_left_eq_self]

/-- Finite strong cuts and scalar Lebesgue integrals are the same evaluation. -/
theorem dualWeightCut_quadratic (R : ℝ) (hR : 0 ≤ R)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (v : RegularHilbert H) :
    ENNReal.ofReal (inner ℂ v (dualWeightCut R A v)).re =
      ∫⁻ s in Set.Ioc (-R) R, dualQuadraticIntegrand A v s := by
  change ENNReal.ofReal (inner ℂ v
    (StrongIntegral.operatorIntegral (dualIntegralFamily A) (-R) R v)).re = _
  rw [StrongIntegral.re_inner_operatorIntegral, intervalIntegral.integral_of_le (by linarith)]
  apply ofReal_integral_eq_lintegral_ofReal
  · exact ((Complex.continuous_re.comp
      (continuous_const.inner (dualAmbient_strongly_continuous A v))).integrableOn_Icc).mono_set
      Set.Ioc_subset_Icc_self
  · exact Filter.Eventually.of_forall (dualQuadratic_nonneg A hA v)

theorem dualWeightCut_quadratic_le (R : ℝ) (hR : 0 ≤ R)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (v : RegularHilbert H) :
    ENNReal.ofReal dualHaarFactor * ENNReal.ofReal (inner ℂ v (dualWeightCut R A v)).re
      ≤ dualQuadraticIntegral A v := by
  rw [dualWeightCut_quadratic R hR A hA v]
  exact mul_le_mul_right (setLIntegral_le_lintegral _ _) _

/-- The unit has an infinite dual integral at every nonzero vector. -/
theorem dualQuadraticIntegral_one (v : RegularHilbert H) (hv : v ≠ 0) :
    dualQuadraticIntegral (1 : RegularHilbert H →L[ℂ] RegularHilbert H) v = ⊤ := by
  have hnorm : 0 < ‖v‖^2 := sq_pos_of_pos (norm_pos_iff.mpr hv)
  have hn : ENNReal.ofReal (‖v‖^2) ≠ 0 := ne_of_gt (ENNReal.ofReal_pos.mpr hnorm)
  have hc : ENNReal.ofReal dualHaarFactor ≠ 0 :=
    ne_of_gt (ENNReal.ofReal_pos.mpr dualHaarFactor_pos)
  have hself : (inner ℂ v v).re = ‖v‖^2 := inner_self_eq_norm_sq (𝕜 := ℂ) v
  simp only [dualQuadraticIntegral, dualQuadraticIntegrand, map_one,
    one_apply_eq_self, hself, lintegral_const,
    Real.volume_univ, ENNReal.mul_top hn, ENNReal.mul_top hc]

#print axioms normalizedDualCut_nonneg
#print axioms normalizedDualCut_mem
#print axioms dualQuadraticIntegral_zero
#print axioms dualQuadraticIntegral_add
#print axioms dualQuadraticIntegral_dual_invariant
#print axioms dualWeightCut_quadratic
#print axioms dualWeightCut_quadratic_le
#print axioms dualQuadraticIntegral_one
end
end TGLV350.Regular
