import TGLExt.F1Fecho394.RegularConjugationAmbientR2
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularConjugationAmbient
open TGLV350.Regular F1Fecho.RegularCovariantCore
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
theorem base_fibre_strongly_continuous (B : UnitaryFlow H)
    (z : RegularHilbert (RegularHilbert H)) :
    Continuous (fun t : ℝ => fibre (fibre (boostCLM B t)) z) := by
  have hin (v : RegularHilbert H) :
      Continuous (fun t : ℝ => fibreIsometry ((boostIso B t).toLinearIsometry) v) :=
    fibre_strongly_continuous (fun t => (boostIso B t).toLinearIsometry)
      (boostIso_strong B) v
  have hout := fibre_strongly_continuous
    (fun t => fibreIsometry ((boostIso B t).toLinearIsometry)) hin z
  exact hout
end F1Fecho.RegularConjugationAmbient
#print axioms F1Fecho.RegularConjugationAmbient.base_fibre_strongly_continuous
