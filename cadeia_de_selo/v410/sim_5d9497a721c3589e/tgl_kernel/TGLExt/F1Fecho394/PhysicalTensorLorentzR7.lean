import TGLExt.F1Fecho394.SpacetimeLorentzFourierR3
import TGLExt.F1Fecho394.CovariantTensorPullbackR3
import TGLExt.F1Fecho394.PhysicalFourierDerivativeR4
import TGLExt.F1Fecho394.MaxwellLocalizedInclusionR2
import TGLExt.FlagNetV31

/-! Actual transformed real Schwartz tensors, including all covariant indices.
Fourier covariance and wedge support are derived from the existing matrix
Lorentz action; covariance of the H1 smearing is the next separate consumer. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Matrix
open scoped FourierTransform
namespace F1Fecho.PhysicalTensorLorentz
open TGLExt F1Fecho.MaxwellGlobal F1Fecho.MaxwellLocalization
open SpacetimeLorentz CovariantTensor

def transform (L:LorentzGrp) : SchwartzTensor→L[ℂ]SchwartzTensor :=
  (SchwartzMap.postcompCLM (pull ((L⁻¹).val.map Complex.ofReal))).comp
    (SchwartzMap.compCLMOfContinuousLinearEquiv ℂ (action L).symm)

theorem transform_apply (L:LorentzGrp) (f:SchwartzTensor) (x:Spacetime) :
    transform L f x=pull ((L⁻¹).val.map Complex.ofReal) (f ((action L).symm x)) := rfl

theorem transform_real (L:LorentzGrp) (f:SchwartzTensor) (hf:IsRealTest f) :
    IsRealTest (transform L f) := by
  intro x μ ν
  exact pull_real (L⁻¹).val _ (hf ((action L).symm x)) μ ν

theorem transform_support (L:LorentzGrp) (f:SchwartzTensor) :
    Function.support (transform L f :Spacetime→TensorValue) ⊆
      action L '' Function.support (f:Spacetime→TensorValue) := by
  intro x hx
  refine ⟨(action L).symm x,?_,(action L).apply_symm_apply x⟩
  change f ((action L).symm x)≠0
  intro hz
  apply hx
  rw [transform_apply,hz,map_zero]

theorem physicalFourier_transform (L:LorentzGrp) (f:SchwartzTensor) (p:Spacetime) :
    physicalFourierCLM (transform L f) p=
      pull ((L⁻¹).val.map Complex.ofReal)
        (physicalFourierCLM f ((action L).symm p)) := by
  let A:TensorValue→L[ℂ]TensorValue := pull ((L⁻¹).val.map Complex.ofReal)
  let g:SchwartzTensor := SchwartzMap.compCLMOfContinuousLinearEquiv ℂ (action L).symm f
  have ht:transform L f=SchwartzMap.postcompCLM A g := rfl
  have hF := schwartz_fourierInv_postcomp A g
  have hFp:=congrArg (fun h:SchwartzTensor=>h ((2*Real.pi)⁻¹ • metricFlip p)) hF
  have hLor:=angular_inverse_lorentz L (f:Spacetime→TensorValue) p
  have hgf:(𝓕⁻ g) ((2*Real.pi)⁻¹ • metricFlip p)=
      (𝓕⁻ f) ((2*Real.pi)⁻¹ • metricFlip ((action L).symm p)) := by
    simp only [SchwartzMap.fourierInv_coe]
    exact hLor
  calc
    physicalFourierCLM (transform L f) p =
        (𝓕⁻ (SchwartzMap.postcompCLM A g)) ((2*Real.pi)⁻¹ • metricFlip p) := by
          rw [ht]; exact physicalFourier_apply _ _
    _ = A ((𝓕⁻ g) ((2*Real.pi)⁻¹ • metricFlip p)) := hFp
    _ = A ((𝓕⁻ f) ((2*Real.pi)⁻¹ • metricFlip ((action L).symm p))) := congrArg A hgf
    _ = A (physicalFourierCLM f ((action L).symm p)) := by
      congr 1
    _ = _ := rfl

theorem boost_wedge (s:ℝ) (x:Spacetime) (hx:x∈physicalRightWedge) :
    action (theBoost s) x∈physicalRightWedge := by
  have h : (fun i=>x i)∈TGL.SpecificAQFT.rightWedge := hx
  have hm := Set.mem_image_of_mem (TGLExt.ContratoQGv31.wedgeBoostMap s) h
  rw [TGLExt.ContratoQGv31.FlagNet.boost_image_rightWedge] at hm
  exact hm

theorem transform_boost_support (s:ℝ) (f:SchwartzTensor)
    (hf:Function.support (f:Spacetime→TensorValue)⊆physicalRightWedge) :
    Function.support (transform (theBoost s) f:Spacetime→TensorValue)⊆physicalRightWedge := by
  intro x hx
  obtain ⟨y,hy,rfl⟩:=transform_support (theBoost s) f hx
  exact boost_wedge s y (hf hy)

end F1Fecho.PhysicalTensorLorentz
#print axioms F1Fecho.PhysicalTensorLorentz.transform_real
#print axioms F1Fecho.PhysicalTensorLorentz.transform_support
#print axioms F1Fecho.PhysicalTensorLorentz.physicalFourier_transform
#print axioms F1Fecho.PhysicalTensorLorentz.boost_wedge
#print axioms F1Fecho.PhysicalTensorLorentz.transform_boost_support
