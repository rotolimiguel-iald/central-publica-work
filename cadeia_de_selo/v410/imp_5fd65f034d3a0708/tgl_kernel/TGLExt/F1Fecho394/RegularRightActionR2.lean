import TGLExt.F1Fecho394.RegularRightAverageR3
import TGLExt.F1Fecho394.RegularRightContinuityR2
import TGLExt.V350ScalarRegularRightGNS
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.RegularRightAction
open TGLV350.Regular MeasureTheory
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
def ambient (t : ℝ) : RegularHilbert (RegularHilbert H) →L[ℂ] RegularHilbert (RegularHilbert H) :=
  characterMultiplier t * fibre (shift t)
theorem ambient_zero : ambient (H:=H) 0 = 1 := by
  simp only [ambient,characterMultiplier_zero,shift_zero,fibre_one,one_mul]
theorem ambient_mul (s t : ℝ) : ambient (H:=H) s * ambient t = ambient (s+t) := by
  unfold ambient
  calc
    _ = characterMultiplier s * (fibre (shift (H:=H) s) * characterMultiplier t) * fibre (shift t) := by simp only [mul_assoc]
    _ = (characterMultiplier s * characterMultiplier t) * (fibre (shift (H:=H) s) * fibre (shift t)) := by
      rw [← characterMultiplier_commutes_fibre]
      simp only [mul_assoc]
    _ = _ := by rw [characterMultiplier_mul,← fibre_mul,shift_mul]
theorem ambient_star (t : ℝ) : star (ambient (H:=H) t) = ambient (-t) := by
  simp only [ambient,star_mul,← fibre_star,shift_star,characterMultiplier_star]
  exact (characterMultiplier_commutes_fibre (H:=RegularHilbert H) (-t) (shift (-t))).symm
 theorem weight_right_regular (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (M : VonNeumannAlgebra H)
    (v : RegularHilbert H) (hv : ∀ t : ℝ, fibre (F1Fecho.RegularCovariantCore.boostCLM B t) v=v)
    (A : (F1Fecho.RegularCovariantCore.core B M).toStarSubalgebra) (t : ℝ) :
    dualQuadraticIntegral (star (A.val * F1Fecho.RegularCovariantCore.regularUnitary B t) *
      (A.val * F1Fecho.RegularCovariantCore.regularUnitary B t)) v =
      dualQuadraticIntegral (star A.val * A.val) v := by
  simp only [dualQuadraticIntegral,dualQuadraticIntegrand_star_mul]
  congr 1
  apply lintegral_congr
  intro s
  rw [F1Fecho.RegularRightAverage.scalarOrbit_right_regular B M v hv A s t]
  simp only [norm_smul,characterPhase_norm,one_mul,shift_norm]
end F1Fecho.RegularRightAction
#print axioms F1Fecho.RegularRightAction.ambient_zero
#print axioms F1Fecho.RegularRightAction.ambient_mul
#print axioms F1Fecho.RegularRightAction.ambient_star
#print axioms F1Fecho.RegularRightAction.weight_right_regular
