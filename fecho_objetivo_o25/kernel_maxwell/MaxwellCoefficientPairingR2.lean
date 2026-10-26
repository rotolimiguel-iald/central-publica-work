import ProfileMaxwellWaveR5
import PhysicalFourierDerivativeR4

/-! Algebraic on-shell pairing for the actual 1/2 antisymmetric-tensor
contraction. The formula keeps the upper-index wave convention of the smearing;
metric lowering remains explicit in the stress consumer. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open TGLExt.ImportedSQ MeasureTheory SchwartzMap ChatgptAudit.WignerRapidityMeasure016
open scoped FourierTransform

 def tensorComponentCLM (μ ν : Fin 4) : TensorValue→L[ℂ]ℂ :=
  (ContinuousLinearMap.proj ν : (Fin 4→ℂ)→L[ℂ]ℂ).comp
    (ContinuousLinearMap.proj μ : TensorValue→L[ℂ](Fin 4→ℂ))

 def componentTest (f : SchwartzTensor) (μ ν : Fin 4) : 𝓢(Spacetime,ℂ) :=
  SchwartzMap.postcompCLM (tensorComponentCLM μ ν) f

 theorem componentTest_apply (f : SchwartzTensor) (μ ν : Fin 4) (x : Spacetime) :
    componentTest f μ ν x=f x μ ν := rfl

 theorem physicalFourier_component (f : SchwartzTensor) (μ ν : Fin 4) (p : Spacetime) :
    scalarPhysicalFourier (componentTest f μ ν) p=physicalFourierCLM f p μ ν := by
  change (𝓕⁻ (SchwartzMap.postcompCLM (tensorComponentCLM μ ν) f))
      ((2*Real.pi)⁻¹ • metricFlip p)=_
  rw [schwartz_fourierInv_postcomp]
  rfl

 theorem globalCoefficient_inner_profile (f : SchwartzTensor) (h : H1)
    (y : MomentumCoordinates) :
    inner ℂ (globalCoefficient f y) (h y)=
      (1/2:ℂ)*∑μ : Fin 4,∑ν : Fin 4,
        (starRingEnd ℂ) (f (shellEmbedding y) μ ν)*profileDensity h μ ν y := by
  simp only [globalCoefficient,PiLp.inner_apply,RCLike.inner_apply,
    PiLp.toLp_apply,map_mul,map_sum,map_div,map_one,map_ofNat,Complex.conj_ofReal]
  simp only [Finset.sum_mul,profileDensity,Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro μ _
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro ν _
  apply Finset.sum_congr rfl
  intro j _
  norm_num only [map_div,map_one,map_ofNat]
  ring

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.physicalFourier_component
#print axioms F1Fecho.MaxwellGlobal.globalCoefficient_inner_profile
