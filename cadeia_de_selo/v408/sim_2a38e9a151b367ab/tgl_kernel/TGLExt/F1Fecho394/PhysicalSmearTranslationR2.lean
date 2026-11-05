import TGLExt.F1Fecho394.PhysicalFourierTranslationR3
import TGLExt.F1Fecho394.PhysicalSchwartzMaxwellR1
import TGLExt.F1Fecho394.ScreenGeometricReflectionR4

/-! Actual translation covariance of the physical Maxwell test map, including
the fixed circular-basis transport required by the canonical J and KWR. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter
open scoped FourierTransform
namespace F1Fecho.MaxwellLocalization
open F1Fecho.MaxwellGlobal F1Fecho.PhysicalFourier F1Fecho.OrbitalScreen
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.WignerOrbit016

def translateTest (a : Spacetime) (f : SchwartzTensor) : SchwartzTensor :=
  SchwartzMap.compSubConstCLM ℂ a f

theorem translateTest_apply (a : Spacetime) (f : SchwartzTensor) (x : Spacetime) :
    translateTest a f x=f (x-a) := rfl

theorem translateTest_real (a : Spacetime) (f : SchwartzTensor) (hf : IsRealTest f) :
    IsRealTest (translateTest a f) := fun p μ ν => hf (p-a) μ ν

theorem physicalFourier_translate (a : Spacetime) (f : SchwartzTensor) (p : Spacetime) :
    physicalFourierCLM (translateTest a f) p =
      phase (orbitPairing (fun i => a i) (fun i => p i)) • physicalFourierCLM f p := by
  rw [physicalFourier_apply,physicalFourier_apply]
  simp only [SchwartzMap.fourierInv_coe]
  exact angular_inverse_fourier_translate (f : Spacetime → TensorValue) a p

theorem coefficient_translate (a : Spacetime) (f : SchwartzTensor) (p : MomentumCoordinates) :
    globalCoefficient (physicalFourierCLM (translateTest a f)) p =
      orbitalPhase 0 (fun i => a i) p • globalCoefficient (physicalFourierCLM f) p := by
  apply PiLp.ext
  intro j
  simp only [globalCoefficient, PiLp.toLp_apply, PiLp.smul_apply]
  rw [physicalFourier_translate]
  change (1/2:ℂ)*(∑ μ,∑ ν,(cartesianStrength p j μ ν:ℂ)*
      (orbitalPhase 0 (fun i => a i) p*physicalFourierCLM f (shellEmbedding p) μ ν)) =
    orbitalPhase 0 (fun i => a i) p*((1/2:ℂ)*(∑ μ,∑ ν,
      (cartesianStrength p j μ ν:ℂ)*physicalFourierCLM f (shellEmbedding p) μ ν))
  simp only [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro μ _
  apply Finset.sum_congr rfl
  intro ν _
  ring

theorem physicalSmear_translate (a : Spacetime) (f : SchwartzTensor) :
    physicalSmearCLM (translateTest a f)=U1 (fun i => a i) (physicalSmearCLM f) := by
  apply Lp.ext
  filter_upwards [physicalSmear_ae (translateTest a f),physicalSmear_ae f,
    orbitalTranslation_ae 0 (fun i => a i) (physicalSmearCLM f)] with p ht hf hu
  change U1 (fun i => a i) (physicalSmearCLM f) p=
    orbitalPhase 0 (fun i => a i) p • physicalSmearCLM f p at hu
  rw [ht,hu,hf,coefficient_translate]

def circularSmear (f : SchwartzTensor) : H1 := circularH1.symm (physicalSmearCLM f)

theorem circularSmear_translate (a : Spacetime) (f : SchwartzTensor) :
    circularSmear (translateTest a f)=U1 (fun i => a i) (circularSmear f) := by
  unfold circularSmear
  rw [physicalSmear_translate,circularH1_symm_U1]

theorem exists_nonzero_real_circularSmear : ∃ f : RealTest,circularSmear f.val≠0 := by
  obtain ⟨f,hf⟩:=exists_nonzero_real_physicalSmear
  refine ⟨f,?_⟩
  intro hz
  apply hf
  exact circularH1.symm.injective (by simpa [circularSmear] using hz)

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.physicalFourier_translate
#print axioms F1Fecho.MaxwellLocalization.coefficient_translate
#print axioms F1Fecho.MaxwellLocalization.physicalSmear_translate
#print axioms F1Fecho.MaxwellLocalization.circularSmear_translate
#print axioms F1Fecho.MaxwellLocalization.exists_nonzero_real_circularSmear
