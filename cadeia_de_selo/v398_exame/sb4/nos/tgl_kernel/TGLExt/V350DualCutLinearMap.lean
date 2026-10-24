import TGLExt.V350DualWeightCuts

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 900000

namespace TGLV350.Regular
open MeasureTheory
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem dualWeightCut_add (R : ℝ)
    (A B : RegularHilbert H →L[ℂ] RegularHilbert H) :
    dualWeightCut R (A+B) = dualWeightCut R A + dualWeightCut R B := by
  ext1 v
  simp only [dualWeightCut_apply,map_add,add_apply]
  exact intervalIntegral.integral_add
    ((dualAmbient_strongly_continuous A v).intervalIntegrable (-R) R)
    ((dualAmbient_strongly_continuous B v).intervalIntegrable (-R) R)

theorem dualWeightCut_smul (R : ℝ) (c : ℂ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    dualWeightCut R (c • A) = c • dualWeightCut R A := by
  ext1 v
  simp only [dualWeightCut_apply,map_smul,smul_apply,intervalIntegral.integral_smul]

/-- A bounded linear map of operators, obtained from strong vector integrals.
It does not require norm-continuity of the dual automorphism group. -/
def dualWeightCutCLM (R : ℝ) :
    (RegularHilbert H →L[ℂ] RegularHilbert H) →L[ℂ]
      (RegularHilbert H →L[ℂ] RegularHilbert H) :=
  ({ toFun := dualWeightCut R
     map_add' := dualWeightCut_add R
     map_smul' := dualWeightCut_smul R } :
    (RegularHilbert H →L[ℂ] RegularHilbert H) →ₗ[ℂ]
      (RegularHilbert H →L[ℂ] RegularHilbert H)).mkContinuous
    |2*R| (fun A => by
      change ‖dualWeightCut R A‖ ≤ |2*R| * ‖A‖
      simpa only [mul_comm] using dualWeightCut_norm_le R A)

#print axioms dualWeightCut_add
#print axioms dualWeightCut_smul
#print axioms dualWeightCutCLM
end
end TGLV350.Regular
