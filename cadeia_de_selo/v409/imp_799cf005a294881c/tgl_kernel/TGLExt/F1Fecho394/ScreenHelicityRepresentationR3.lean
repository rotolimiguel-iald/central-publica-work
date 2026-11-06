import TGLExt.F1Fecho394.ScreenCircularBasisR2
import TGLExt.F1Fecho394.ScreenStrongContinuityR6
import TGLExt.F1Fecho394.ScreenPhysicalHelicityR2

/-! The physical screen action in circular helicity coordinates on the same H1.
This is a fixed unitary conjugation, not the scalar orbital representation.
Localization of real standard subspaces is a separate obligation. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter Matrix Complex
namespace F1Fecho.OrbitalScreen
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016 F1Fecho.OrbitalSpatial

def helicityUnitary (L : generatedLorentz) : H1 ≃ₗᵢ[ℂ] H1 :=
  circularH1.trans ((transverseUnitary L).trans circularH1.symm)

theorem helicityUnitary_apply (L : generatedLorentz) (f : H1) :
    helicityUnitary L f=circularH1.symm (transverseUnitary L (circularH1 f)) := rfl

theorem helicityUnitary_one (f : H1) : helicityUnitary 1 f=f := by
  rw [helicityUnitary_apply]
  change circularH1.symm (transverseAction 1 (circularH1 f))=f
  rw [transverseAction_one,circularH1.symm_apply_apply]

theorem helicityUnitary_mul (L M : generatedLorentz) (f : H1) :
    helicityUnitary (L*M) f=helicityUnitary L (helicityUnitary M f) := by
  simp only [helicityUnitary_apply,circularH1.apply_symm_apply]
  change circularH1.symm (transverseAction (L*M) (circularH1 f))=
    circularH1.symm (transverseAction L (transverseAction M (circularH1 f)))
  rw [transverseAction_mul]

def helicityUnitaryHom : generatedLorentz →* (H1 ≃ₗᵢ[ℂ] H1) where
  toFun := helicityUnitary
  map_one' := by apply LinearIsometryEquiv.ext; intro f; exact helicityUnitary_one f
  map_mul' L M := by apply LinearIsometryEquiv.ext; intro f; exact helicityUnitary_mul L M f

theorem helicityUnitary_strongly_continuous (f : H1) :
    Continuous (fun L : generatedLorentz => helicityUnitary L f) :=
  circularH1.symm.continuous.comp (transverseUnitary_strongly_continuous (circularH1 f))

theorem circularH1_symm_U1 (a : Fin 4 → ℝ) (f : H1) :
    circularH1.symm (U1 a f)=U1 a (circularH1.symm f) := by
  apply circularH1.injective
  rw [circularH1.apply_symm_apply]
  change U1 a f=fiberLift circularFiber (U1 a (circularH1.symm f))
  rw [fiberLift_U1]
  exact congrArg (U1 a) (circularH1.apply_symm_apply f).symm

theorem helicityUnitary_U1 (L : generatedLorentz) (a : Fin 4 → ℝ) (f : H1) :
    helicityUnitary L (U1 a f)=U1 (L.val.val.mulVec a) (helicityUnitary L f) := by
  simp only [helicityUnitary_apply]
  change circularH1.symm (transverseUnitary L (fiberLift circularFiber (U1 a f)))=_
  rw [fiberLift_U1,transverseUnitary_U1,circularH1_symm_U1]
  rfl

theorem helicityUnitary_boost (s : ℝ) (f : H1) :
    helicityUnitary (generatedBoost s) f=B0 s f := by
  rw [helicityUnitary_apply,transverseUnitary_boost]
  apply circularH1.injective
  rw [circularH1.apply_symm_apply]
  exact (fiberLift_B0 circularFiber s f).symm

def helicityPoincareH1 (a : Fin 4 → ℝ) (L : generatedLorentz) : H1 ≃ₗᵢ[ℂ] H1 :=
  (helicityUnitary L).trans (U1 a)

theorem helicityPoincareH1_mul (a b : Fin 4 → ℝ) (L M : generatedLorentz) (f : H1) :
    helicityPoincareH1 a L (helicityPoincareH1 b M f)=
      helicityPoincareH1 (a+L.val.val.mulVec b) (L*M) f := by
  change U1 a (helicityUnitary L (U1 b (helicityUnitary M f)))=
    U1 (a+L.val.val.mulVec b) (helicityUnitary (L*M) f)
  rw [helicityUnitary_U1,←helicityUnitary_mul]
  exact (orbitalTranslation_add 0 a (L.val.val.mulVec b) (helicityUnitary (L*M) f)).symm

end F1Fecho.OrbitalScreen
#print axioms F1Fecho.OrbitalScreen.helicityUnitaryHom
#print axioms F1Fecho.OrbitalScreen.helicityUnitary_strongly_continuous
#print axioms F1Fecho.OrbitalScreen.helicityUnitary_U1
#print axioms F1Fecho.OrbitalScreen.helicityUnitary_boost
#print axioms F1Fecho.OrbitalScreen.helicityPoincareH1_mul
