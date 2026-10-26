import PhysicalFourierDerivativeR4

/-! Actual spacetime derivative tests annihilate the global physical Maxwell
smearing. This consumes the inverse-angular Fourier derivative theorem and
the proved on-shell divergence; it does not assume a Fourier symbol equation
as the definition of differentiation. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open SchwartzMap FourierTransform MeasureTheory
open TGLExt.ImportedSQ
open scoped FourierTransform LineDeriv

def tensorEntry (μ ν : Fin 4) : ℂ →L[ℂ] TensorValue :=
  ContinuousLinearMap.pi (fun ρ => ContinuousLinearMap.pi (fun σ =>
    if ρ=μ ∧ σ=ν then ContinuousLinearMap.id ℂ ℂ else 0))

theorem tensorEntry_apply (μ ν ρ σ : Fin 4) (z : ℂ) :
    tensorEntry μ ν z ρ σ=if ρ=μ ∧ σ=ν then z else 0 := by
  by_cases h : ρ=μ ∧ σ=ν <;> simp [tensorEntry,h]

def spacetimeDivergence (b : 𝓢(Spacetime,ℂ)) (ν : Fin 4) : SchwartzTensor :=
  ∑ μ,∂_{spacetimeBasis μ} (SchwartzMap.postcompCLM (tensorEntry μ ν) b)

theorem physicalFourier_spacetimeDivergence (b : 𝓢(Spacetime,ℂ)) (ν : Fin 4) :
    physicalFourierCLM (spacetimeDivergence b ν)=
      (-Complex.I) • divergenceTensor (scalarPhysicalFourier b) ν := by
  ext p ρ σ
  simp only [spacetimeDivergence,map_sum,SchwartzMap.sum_apply,Finset.sum_apply,
    physicalFourier_derivative,physicalFourier_postcomp,SchwartzMap.postcompCLM_apply,
    Pi.smul_apply,smul_eq_mul,tensorEntry_apply,SchwartzMap.smul_apply,divergenceTensor_apply]
  by_cases hs : σ=ν
  · simp only [hs,and_true,mul_ite,mul_zero,Finset.sum_ite_eq,Finset.mem_univ,ite_true]
    ring
  · simp [hs]

theorem physicalSmear_spacetimeDivergence_zero (b : 𝓢(Spacetime,ℂ)) (ν : Fin 4) :
    physicalSmearCLM (spacetimeDivergence b ν)=0 := by
  change momentumSmearCLM (physicalFourierCLM (spacetimeDivergence b ν))=0
  rw [physicalFourier_spacetimeDivergence,map_smul]
  change (-Complex.I) • momentumSmear (divergenceTensor (scalarPhysicalFourier b) ν)=0
  rw [momentumSmear_divergence_zero,smul_zero]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.tensorEntry_apply
#print axioms F1Fecho.MaxwellGlobal.physicalFourier_spacetimeDivergence
#print axioms F1Fecho.MaxwellGlobal.physicalSmear_spacetimeDivergence_zero
