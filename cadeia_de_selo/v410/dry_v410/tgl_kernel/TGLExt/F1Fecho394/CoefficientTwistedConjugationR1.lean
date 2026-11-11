import TGLExt.F1Fecho394.CoefficientBoostR1
import TGLExt.F1Fecho394.CoefficientConjugationR2

/-! The antiunitary f(a) -> B_a J f(-a). Its involution is proved from
the named base conjugation/flow relations, not asserted as a new field. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open MeasureTheory
namespace F1Fecho.CoefficientTwistedConjugation
open TGLV350.Regular F1Fecho.RegularCovariantCore
open F1Fecho.CoefficientConjugation
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (B : UnitaryFlow H) (J : H≃ₛₗᵢ[starRingEnd ℂ]H)

def twist : RegularHilbert H≃ₛₗᵢ[starRingEnd ℂ]RegularHilbert H :=
  (reflection.trans (lift J)).trans (CoefficientBoost.unitary B 1)

theorem twist_ae (f : RegularHilbert H) :
    twist B J f =ᵐ[volume] fun a : ℝ => B.U a (J (f (-a))) := by
  filter_upwards [CoefficientBoost.unitary_ae B 1 (lift J (reflection f)),
    lift_ae J (reflection f),reflectionMap_ae f] with a ha hb hc
  change CoefficientBoost.unitary B 1 (lift J (reflection f)) a = _
  rw [ha,hb]
  change B.U (1*a) (J (reflectionMap f a))=_
  rw [hc,one_mul]

theorem twist_involutive (hJ : Function.Involutive J)
    (hBJ : ∀ a x, J (B.U a x)=B.U a (J x)) : Function.Involutive (twist B J) := by
  intro f
  apply Lp.ext
  have hn := (Measure.measurePreserving_neg (volume : Measure ℝ)).quasiMeasurePreserving.ae
    (twist_ae B J f)
  filter_upwards [twist_ae B J (twist B J f),hn] with a ha hb
  rw [ha,hb,neg_neg,hBJ,hJ]
  have h := congrArg (fun U : H≃ₗᵢ[ℂ]H => U (f a)) (B.add a (-a))
  simp only [add_neg_cancel,B.zero,LinearIsometryEquiv.trans_apply] at h
  exact h.symm

theorem twist_fibre (A C : H→L[ℂ]H)
    (hJC : ∀ x, J (A x)=C (J x))
    (hBC : ∀ a x, B.U a (C x)=C (B.U a x)) (f : RegularHilbert H) :
    twist B J (fibre A f)=fibre C (twist B J f) := by
  apply Lp.ext
  have hn := (Measure.measurePreserving_neg (volume : Measure ℝ)).quasiMeasurePreserving.ae
    (fibre_ae A f)
  filter_upwards [twist_ae B J (fibre A f),hn,fibre_ae C (twist B J f),
    twist_ae B J f] with a ha hb hc hd
  rw [ha,hb,hJC,hBC,hc,hd]

end F1Fecho.CoefficientTwistedConjugation
#print axioms F1Fecho.CoefficientTwistedConjugation.twist
#print axioms F1Fecho.CoefficientTwistedConjugation.twist_ae
#print axioms F1Fecho.CoefficientTwistedConjugation.twist_involutive
#print axioms F1Fecho.CoefficientTwistedConjugation.twist_fibre
