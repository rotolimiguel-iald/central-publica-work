import TGLExt.F1Fecho394.RegularRightActionR2
import TGLExt.V350DualOrbitRepresentation
/-! The actual regular-conjugation candidate reduces to the base unitary
flow on the physical fibre. This is an algebraic identity, not yet its
identification with the modular imaginary powers of the weight. -/
set_option autoImplicit false
set_option maxHeartbeats 1300000
noncomputable section
namespace F1Fecho.RegularConjugationAmbient
open TGLV350.Regular MeasureTheory
open F1Fecho.RegularCovariantCore
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (B : UnitaryFlow H)
theorem phase_comm (s t : ℝ) : characterPhase s t=characterPhase t s := by
  unfold characterPhase
  congr 1
  ring

theorem dualOrbit_regular (t : ℝ) :
    dualOrbitRepresentation (regularUnitary B t) =
      characterMultiplier t * fibre (regularUnitary B t) := by
  ext1 f
  apply Lp.ext
  filter_upwards [operatorFieldLift_ae (dualIntegralFamily (regularUnitary B t)) f,
    characterMultiplier_ae t (fibre (regularUnitary B t) f),
    fibre_ae (regularUnitary B t) f] with s h1 h2 h3
  change operatorFieldLift (dualIntegralFamily (regularUnitary B t)) f s =
    characterMultiplier t (fibre (regularUnitary B t) f) s
  rw [h1,h2,h3]
  change dualAmbient s (regularUnitary B t) (f s) = _
  rw [dual_on_regular B s t]
  change characterPhase s t • regularUnitary B t (f s) = _
  rw [phase_comm s t]
  rfl

theorem regular_conjugation_is_base_fibre (t : ℝ) :
    dualOrbitRepresentation (regularUnitary B t) *
      F1Fecho.RegularRightAction.ambient (H:=H) (-t) =
        fibre (fibre (boostCLM B t)) := by
  rw [dualOrbit_regular B t]
  unfold F1Fecho.RegularRightAction.ambient
  calc
    _ = characterMultiplier t * (fibre (regularUnitary B t) * characterMultiplier (-t)) *
        fibre (shift (-t)) := by simp only [mul_assoc]
    _ = (characterMultiplier t * characterMultiplier (-t)) *
        (fibre (regularUnitary B t) * fibre (shift (-t))) := by
      rw [← characterMultiplier_commutes_fibre]
      simp only [mul_assoc]
    _ = fibre (regularUnitary B t * shift (-t)) := by
      rw [characterMultiplier_mul,add_neg_cancel,characterMultiplier_zero,one_mul,← fibre_mul]
    _ = _ := by
      congr 1
      simp only [F1Fecho.RegularCovariantCore.regularUnitary,mul_assoc,shift_mul,add_neg_cancel,shift_zero,mul_one]
end F1Fecho.RegularConjugationAmbient
#print axioms F1Fecho.RegularConjugationAmbient.dualOrbit_regular
#print axioms F1Fecho.RegularConjugationAmbient.regular_conjugation_is_base_fibre
