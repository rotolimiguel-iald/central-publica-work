import TGLExt.F1Fecho394.PhysicalSmearTranslationR2
import TGLExt.F1Fecho394.CircularConjugationR1

/-! Actual almost-everywhere rapidity formula for the physical Maxwell map
after the fixed circular change of basis. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter
namespace F1Fecho.MaxwellLocalization
open F1Fecho.MaxwellGlobal F1Fecho.OrbitalScreen
open TGLExt.ImportedSQ AuditF13v31 ChatgptAudit.WignerRapidityMeasure016

theorem circularSmear_ae (f : SchwartzTensor) :
    circularSmear f =ᵐ[orbitalMeasure 0] fun p =>
      circularFiber.symm (globalCoefficient (physicalFourierCLM f) p) := by
  have he : circularH1 (circularSmear f)=physicalSmearCLM f :=
    circularH1.apply_symm_apply _
  filter_upwards [fiberLiftMap_ae circularFiber (circularSmear f),physicalSmear_ae f] with p hp hf
  have hv := congrArg (fun v : H1 => v p) he
  change fiberLiftMap circularFiber (circularSmear f) p=physicalSmearCLM f p at hv
  rw [hp,hf] at hv
  exact circularFiber.injective (by rw [hv,circularFiber.apply_symm_apply])

theorem circularSmear_rapidity_ae (f : SchwartzTensor) :
    toRapidity (circularSmear f) =ᵐ[momentumMeasure] fun y =>
      circularFiber.symm (globalCoefficient (physicalFourierCLM f) (rapidityChart 0 y)) := by
  have hc := (rapidityChart_measurePreserving 0).quasiMeasurePreserving.ae (circularSmear_ae f)
  filter_upwards [orbitalL2Pullback_ae 0 (circularSmear f),hc] with y hp hc
  exact hp.trans hc

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.circularSmear_ae
#print axioms F1Fecho.MaxwellLocalization.circularSmear_rapidity_ae
