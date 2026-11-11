import TGLExt.V350DualOrbitRepresentation
set_option autoImplicit false
set_option maxErrors 2
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularOrbitMultiplication
open TGLV350.Regular MeasureTheory
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
theorem apply_orbit
    (A B : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H)
    (c : ℝ) (f g : RegularHilbert (RegularHilbert H))
    (hf : (f : ℝ → RegularHilbert H) =ᵐ[volume] fun s => c • dualAmbient s A v)
    (hg : (g : ℝ → RegularHilbert H) =ᵐ[volume] fun s => c • dualAmbient s (B*A) v) :
    dualOrbitRepresentation B f = g := by
  apply Lp.ext
  filter_upwards [operatorFieldLift_ae (dualIntegralFamily B) f,hf,hg] with s h1 h2 h3
  change operatorFieldLift (dualIntegralFamily B) f s = _
  rw [h1,h3]
  change dualAmbient s B (f s) = _
  rw [h2]
  change dualAmbient s B ((c : ℂ) • dualAmbient s A v) =
    (c : ℂ) • dualAmbient s (B*A) v
  rw [map_smul,map_mul]
  rfl
end F1Fecho.RegularOrbitMultiplication
#print axioms F1Fecho.RegularOrbitMultiplication.apply_orbit
