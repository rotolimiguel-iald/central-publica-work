import SchwartzMaxwellCoefficientR5
import Mathlib.Analysis.Distribution.SchwartzSpace.Fourier

/-! Explicit Fourier convention: mathlib uses exp(-2*pi*i*EuclideanInner).
The spatial metric flip therefore gives exp(-2*pi*i*(p0*x0-p_spatial*x_spatial)).
No identification of dimensionful momentum with angular frequency is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Matrix SchwartzMap
open scoped FourierTransform

def metricFlip : Spacetime ≃ₗᵢ[ℝ] Spacetime :=
  LinearIsometryEquiv.piLpCongrRight 2 (fun i : Fin 4 =>
    if i=0 then LinearIsometryEquiv.refl ℝ ℝ else LinearIsometryEquiv.neg ℝ)

theorem metricFlip_apply (p : Spacetime) (i : Fin 4) :
    metricFlip p i=if i=0 then p i else -p i := by
  simp only [metricFlip,LinearIsometryEquiv.piLpCongrRight_apply]
  split_ifs <;> rfl

theorem metricFlip_involutive : Function.Involutive metricFlip := by
  intro p
  apply PiLp.ext
  intro i
  simp only [metricFlip_apply]
  split_ifs <;> simp

theorem metricFlip_inner (p x : Spacetime) :
    inner ℝ (metricFlip p) x=p 0*x 0-p 1*x 1-p 2*x 2-p 3*x 3 := by
  rw [PiLp.inner_apply]
  have h20 : (2:Fin 4)≠0 := by decide
  have h30 : (3:Fin 4)≠0 := by decide
  simp [Fin.sum_univ_four,metricFlip_apply,h20,h30,real_inner_comm,sub_eq_add_neg]
  try ring

def minkowskiFourier (f : SchwartzTensor) : SchwartzTensor :=
  SchwartzMap.compCLMOfContinuousLinearEquiv ℂ metricFlip.toContinuousLinearEquiv (𝓕 f)

theorem minkowskiFourier_apply (f : SchwartzTensor) (p : Spacetime) :
    minkowskiFourier f p=(𝓕 f) (metricFlip p) := rfl

theorem minkowskiFourier_add (f g : SchwartzTensor) :
    minkowskiFourier (f+g)=minkowskiFourier f+minkowskiFourier g := by
  unfold minkowskiFourier
  rw [FourierTransform.fourier_add,map_add]

theorem minkowskiFourier_smul (c : ℂ) (f : SchwartzTensor) :
    minkowskiFourier (c•f)=c•minkowskiFourier f := by
  unfold minkowskiFourier
  rw [FourierTransform.fourier_smul,map_smul]

theorem minkowskiFourier_surjective : Function.Surjective minkowskiFourier := by
  intro g
  let h := SchwartzMap.compCLMOfContinuousLinearEquiv ℂ metricFlip.toContinuousLinearEquiv g
  refine ⟨𝓕⁻ h,?_⟩
  ext p : 1
  change (𝓕 (𝓕⁻ h)) (metricFlip p)=g p
  rw [FourierTransform.fourier_fourierInv_eq]
  change g (metricFlip (metricFlip p))=g p
  rw [metricFlip_involutive p]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.metricFlip_involutive
#print axioms F1Fecho.MaxwellGlobal.metricFlip_inner
#print axioms F1Fecho.MaxwellGlobal.minkowskiFourier_apply

#print axioms F1Fecho.MaxwellGlobal.minkowskiFourier_surjective
