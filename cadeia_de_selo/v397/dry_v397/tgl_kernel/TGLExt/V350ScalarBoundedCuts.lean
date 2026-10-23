import TGLExt.V350DualCutLinearMap
import TGLExt.V350ScalarDualWeight

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 900000

namespace TGLV350.Regular
open TGLExt MeasureTheory
open scoped ENNReal ComplexOrder
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- A bounded complex-linear functional. Positivity requires R ≥ 0.
The normalization is the same dual Haar factor used in the scalar weight. -/
def dualCutFunctional (R : ℝ) (v : RegularHilbert H) :
    (RegularHilbert H →L[ℂ] RegularHilbert H) →L[ℂ] ℂ :=
  (dualHaarFactor : ℂ) • (innerSL ℂ v).comp
    ((ContinuousLinearMap.apply ℂ (RegularHilbert H) v).comp (dualWeightCutCLM R))

theorem dualCutFunctional_apply (R : ℝ) (v : RegularHilbert H)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    dualCutFunctional R v A = (dualHaarFactor : ℂ) * inner ℂ v (dualWeightCut R A v) := rfl

theorem dualCutFunctional_nonneg (R : ℝ) (hR : 0 ≤ R) (v : RegularHilbert H)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) :
    0 ≤ dualCutFunctional R v A := by
  have hp := ((ContinuousLinearMap.nonneg_iff_isPositive _).mp
    (normalizedDualCut_nonneg R hR A hA)).inner_nonneg_right v
  change 0 ≤ inner ℂ v ((dualHaarFactor : ℂ) • dualWeightCut R A v) at hp
  rw [inner_smul_right] at hp
  exact hp

theorem dualCutFunctional_ofReal_re (R : ℝ) (v : RegularHilbert H)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    ENNReal.ofReal (dualCutFunctional R v A).re =
      ENNReal.ofReal dualHaarFactor * ENNReal.ofReal (inner ℂ v (dualWeightCut R A v)).re := by
  rw [dualCutFunctional_apply,Complex.mul_re,Complex.ofReal_re,Complex.ofReal_im]
  simp only [zero_mul,sub_zero,ENNReal.ofReal_mul dualHaarFactor_pos.le]

/-- These bounded positive functionals are dominated by ν on N+.
No faithfulness of an individual finite cut is asserted. -/
theorem scalarDualWeight_dominates_cut (P : SiteProfile) (R : ℝ) (hR : 0 ≤ R)
    (A : PositiveCoreInput P) :
    ENNReal.ofReal (dualCutFunctional R (regularVacuum P) A.val).re ≤ scalarDualWeight P A := by
  rw [dualCutFunctional_ofReal_re]
  exact dualWeightCut_quadratic_le R hR A.val A.property.2 (regularVacuum P)

theorem scalarDualWeight_eq_iSup_boundedCuts (P : SiteProfile) (A : PositiveCoreInput P) :
    scalarDualWeight P A = ⨆ n : ℕ,
      ENNReal.ofReal (dualCutFunctional (n : ℝ) (regularVacuum P) A.val).re := by
  simp only [dualCutFunctional_ofReal_re]
  exact dualQuadraticIntegral_eq_iSup_cuts A.val A.property.2 (regularVacuum P)

#print axioms dualCutFunctional
#print axioms dualCutFunctional_apply
#print axioms dualCutFunctional_nonneg
#print axioms dualCutFunctional_ofReal_re
#print axioms scalarDualWeight_dominates_cut
#print axioms scalarDualWeight_eq_iSup_boundedCuts
end
end TGLV350.Regular
