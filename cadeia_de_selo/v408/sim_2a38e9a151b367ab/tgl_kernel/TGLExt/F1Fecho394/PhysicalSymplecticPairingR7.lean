import TGLExt.F1Fecho394.GenericSmearSymplecticR6
import TGLExt.F1Fecho394.PhysicalSmearTranslationR2
import TGLExt.F1Fecho394.PhysicalCompactPairLocalityR1

/-! The real bilinear symplectic pairing of the actual Maxwell test map.
No causal locality is assumed or proved by bilinearity alone. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.MaxwellLocalization
open F1Fecho.MaxwellGlobal F1Fecho.OrbitalScreen TGLExt.ImportedSQ

def circularSmearCLM : SchwartzTensor →L[ℂ] H1 :=
  circularH1.symm.toLinearIsometry.toContinuousLinearMap.comp physicalSmearCLM

theorem circularSmearCLM_apply (f : SchwartzTensor) :
    circularSmearCLM f = circularSmear f := rfl

def physicalTestPairing : SchwartzTensor →ₗ[ℝ] SchwartzTensor →ₗ[ℝ] ℝ :=
  GenericSmearSymplectic.pairing circularSmearCLM.toLinearMap

theorem physicalTestPairing_apply (f g : SchwartzTensor) :
    physicalTestPairing f g = (inner ℂ (circularSmear f) (circularSmear g)).im := rfl

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.physicalTestPairing
