import TGLExt.V350RegularDualAction
set_option autoImplicit false
set_option maxErrors 2
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularRightContinuity
open TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
theorem rightAmbient_strongly_continuous (z : RegularHilbert (RegularHilbert H)) :
    Continuous (fun t : ℝ => (characterMultiplier (H := RegularHilbert H) t * fibre (H := RegularHilbert H) (shift (H := H) t)) z) := by
  have hf : Continuous (fun t : ℝ => fibre (H := RegularHilbert H) (shift (H := H) t) z) :=
    fibre_strongly_continuous (H := RegularHilbert H) (shiftIsometry (H := H))
      (fun v => shift_strongly_continuous v) z
  exact (characterMultiplier_jointly_continuous (H := RegularHilbert H)).comp
    (hf.prodMk continuous_id)
end F1Fecho.RegularRightContinuity
#print axioms F1Fecho.RegularRightContinuity.rightAmbient_strongly_continuous
