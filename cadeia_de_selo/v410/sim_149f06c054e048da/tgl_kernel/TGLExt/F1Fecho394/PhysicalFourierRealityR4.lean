import TGLExt.F1Fecho394.PhysicalTensorLorentzR7

/-! Spacetime inversion of real test tensors is complex conjugation of the
physical positive-angular Fourier transform. No localization consequence is
assumed in this Fourier identity. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open MeasureTheory Complex SchwartzMap
open scoped ComplexConjugate
open scoped FourierTransform
namespace F1Fecho.MaxwellLocalization
open F1Fecho.MaxwellGlobal F1Fecho.SpacetimeLorentz
open ChatgptAudit.WignerOrbit016

def invertTest : SchwartzTensor→L[ℂ]SchwartzTensor :=
  SchwartzMap.compCLMOfContinuousLinearEquiv ℂ (ContinuousLinearEquiv.neg ℝ)

theorem invertTest_apply (f:SchwartzTensor) (x:Spacetime) : invertTest f x=f (-x) := rfl

theorem invertTest_real (f:SchwartzTensor) (hf:IsRealTest f) : IsRealTest (invertTest f) :=
  fun x μ ν=>hf (-x) μ ν

theorem invertTest_support (f:SchwartzTensor) :
    Function.support (invertTest f:Spacetime→TensorValue)=
      (fun x:Spacetime=>-x) '' Function.support (f:Spacetime→TensorValue) := by
  ext x
  constructor
  · intro hx
    exact ⟨-x,hx,neg_neg x⟩
  · rintro ⟨y,hy,rfl⟩
    simpa only [Function.mem_support,invertTest_apply,neg_neg] using hy

theorem physicalFourier_component (f:SchwartzTensor) (p:Spacetime) (μ ν:Fin 4) :
    physicalFourierCLM f p μ ν=
      ∫x:Spacetime,exp ((orbitPairing (fun i=>x i) (fun i=>p i):ℂ)*I)*f x μ ν := by
  let A:TensorValue→L[ℂ]ℂ :=
    (ContinuousLinearMap.proj ν : (Fin 4 → ℂ) →L[ℂ] ℂ).comp
      (ContinuousLinearMap.proj μ : TensorValue →L[ℂ] (Fin 4 → ℂ))
  let g:𝓢(Spacetime,ℂ):=SchwartzMap.postcompCLM A f
  have he:=congrArg (fun h:𝓢(Spacetime,ℂ)=>h ((2*Real.pi)⁻¹ • metricFlip p))
    (schwartz_fourierInv_postcomp A f)
  calc
    physicalFourierCLM f p μ ν=(𝓕⁻ g) ((2*Real.pi)⁻¹ • metricFlip p) := by
      rw [physicalFourier_apply]
      simpa [A,g,SchwartzMap.postcompCLM_apply] using he.symm
    _ = _ := by
      simpa [g,A,SchwartzMap.postcompCLM_apply,SchwartzMap.fourierInv_coe] using angular_inverse_integral (g:Spacetime→ℂ) p

theorem physicalFourier_invert_real (f:SchwartzTensor) (hf:IsRealTest f)
    (p:Spacetime) (μ ν:Fin 4) :
    physicalFourierCLM (invertTest f) p μ ν=conj (physicalFourierCLM f p μ ν) := by
  rw [physicalFourier_component,physicalFourier_component,←integral_conj]
  have hi:=integral_neg_eq_self
    (fun x:Spacetime=>exp ((orbitPairing (fun i=>x i) (fun i=>p i):ℂ)*I)*invertTest f x μ ν)
  rw [←hi]
  apply integral_congr_ae
  apply ae_of_all
  intro x
  have hr:conj (f x μ ν)=f x μ ν := Complex.conj_eq_iff_im.mpr (hf x μ ν)
  simp only [invertTest_apply,neg_neg,map_mul,←Complex.exp_conj,hr,
    Complex.conj_ofReal,Complex.conj_I,mul_neg]
  congr 2
  simp [orbitPairing,Pi.neg_apply,Complex.ofReal_neg]
  <;> ring

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.invertTest_support
#print axioms F1Fecho.MaxwellLocalization.physicalFourier_component
#print axioms F1Fecho.MaxwellLocalization.physicalFourier_invert_real
