import TGLExt.F1Fecho394.RegularOrbitMultiplicationR1
set_option autoImplicit false
noncomputable section
namespace F1Fecho.RegularOrbitMultiplication
open TGLV350.Regular MeasureTheory
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
theorem apply_orbit_ae (A B:RegularHilbert H→L[ℂ]RegularHilbert H)
    (v:RegularHilbert H) (c:ℝ) (f:RegularHilbert (RegularHilbert H))
    (hf:f=ᵐ[volume] fun s=>c • dualAmbient s A v) :
    dualOrbitRepresentation B f=ᵐ[volume] fun s=>c • dualAmbient s (B*A) v := by
  filter_upwards [operatorFieldLift_ae (dualIntegralFamily B) f,hf] with s h1 h2
  change operatorFieldLift (dualIntegralFamily B) f s=_
  rw [h1]
  change dualAmbient s B (f s)=_
  rw [h2]
  change dualAmbient s B ((c:ℂ) • dualAmbient s A v)=(c:ℂ) • dualAmbient s (B*A) v
  rw [map_smul,map_mul]
  rfl
end F1Fecho.RegularOrbitMultiplication
#print axioms F1Fecho.RegularOrbitMultiplication.apply_orbit_ae
