import TGLExt.F1Fecho394.CoefficientBoostR1

/-! The existing generic regular representation is conjugate to translation,
using the already constructed coefficient boost multiplier. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open MeasureTheory
namespace F1Fecho.RegularPositiveFlow
open TGLV350.Regular F1Fecho.RegularCovariantCore
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem absorption_shift (B : UnitaryFlow H) (t : ℝ) (f : RegularHilbert H) :
    CoefficientBoost.unitary B 1 (shift t f)=
      RegularCovariantCore.regularUnitary B t (CoefficientBoost.unitary B 1 f) := by
  apply Lp.ext
  filter_upwards [CoefficientBoost.unitary_ae B 1 (shift t f), shift_ae t f,
    fibre_ae (boostCLM B t) (shift t (CoefficientBoost.unitary B 1 f)),
    shift_ae t (CoefficientBoost.unitary B 1 f),
    (measurePreserving_sub_right volume t).quasiMeasurePreserving.ae
      (CoefficientBoost.unitary_ae B 1 f)] with a h1 h2 h3 h4 h5
  change CoefficientBoost.unitary B 1 (shift t f) a=
    fibre (boostCLM B t) (shift t (CoefficientBoost.unitary B 1 f)) a
  rw [h1,h2,h3,h4,h5]
  simp only [one_mul]
  change B.U a (f (a-t))=B.U t (B.U (a-t) (f (a-t)))
  have he:=congrArg (fun V : H≃ₗᵢ[ℂ]H=>V (f (a-t))) (B.add t (a-t))
  simpa only [add_sub_cancel,LinearIsometryEquiv.trans_apply] using he

end F1Fecho.RegularPositiveFlow
#print axioms F1Fecho.RegularPositiveFlow.absorption_shift
