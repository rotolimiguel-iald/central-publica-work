import PhysicalSchwartzMaxwellR1
import SchwartzMaxwellDivergenceR2

/-! The angular inverse Fourier derivative identity, with no change of the
underlying H1 or density. Constant tensor injection commutes with Fourier. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open SchwartzMap FourierTransform MeasureTheory
open scoped FourierTransform LineDeriv Topology

variable {E G : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E] [CompleteSpace E]
  [NormedAddCommGroup G] [NormedSpace ℂ G] [CompleteSpace G]

theorem schwartz_fourier_postcomp (L : E →L[ℂ] G) (f : 𝓢(Spacetime,E)) :
    𝓕 (SchwartzMap.postcompCLM L f)=SchwartzMap.postcompCLM L (𝓕 f) := by
  ext p : 1
  change (𝓕 (fun x => L (f x))) p = L ((𝓕 (f : Spacetime→E)) p)
  rw [Real.fourier_eq,Real.fourier_eq,← L.integral_comp_comm ((Real.fourierIntegral_convergent_iff p).2 f.integrable)]
  apply integral_congr_ae
  filter_upwards [] with x
  simp only [Circle.smul_def,map_smul]

theorem schwartz_fourierInv_postcomp (L : E →L[ℂ] G) (f : 𝓢(Spacetime,E)) :
    𝓕⁻ (SchwartzMap.postcompCLM L f)=SchwartzMap.postcompCLM L (𝓕⁻ f) := by
  rw [SchwartzMap.fourierInv_apply_eq,schwartz_fourier_postcomp]
  ext p : 1
  rfl

def scalarPhysicalFourier (f : 𝓢(Spacetime,ℂ)) : 𝓢(Spacetime,ℂ) :=
  SchwartzMap.compCLMOfContinuousLinearEquiv ℂ physicalFourierArgument (𝓕⁻ f)

theorem physicalFourier_postcomp (L : ℂ →L[ℂ] TensorValue) (b : 𝓢(Spacetime,ℂ)) :
    physicalFourierCLM (SchwartzMap.postcompCLM L b)=
      SchwartzMap.postcompCLM L (scalarPhysicalFourier b) := by
  ext p : 1
  rw [physicalFourier_apply,schwartz_fourierInv_postcomp]
  rfl

def spacetimeBasis (μ : Fin 4) : Spacetime := EuclideanSpace.single μ 1

theorem physicalFourier_derivative (f : SchwartzTensor) (μ : Fin 4) (p : Spacetime) :
    physicalFourierCLM (∂_{spacetimeBasis μ} f) p =
      (-Complex.I*(metricFlip p μ:ℂ)) • physicalFourierCLM f p := by
  rw [physicalFourier_apply,SchwartzMap.fourierInv_lineDerivOp_eq]
  have ht : (fun x : Spacetime => inner ℝ x (spacetimeBasis μ)).HasTemperateGrowth := by fun_prop
  simp only [SchwartzMap.smul_apply,SchwartzMap.smulLeftCLM_apply ht,
    spacetimeBasis,EuclideanSpace.inner_single_right,map_one,one_mul,map_id,
    PiLp.smul_apply,smul_eq_mul,Complex.ofReal_mul,physicalFourier_apply]
  rw [← Complex.ofReal_smul,smul_smul]
  congr 1
  push_cast
  field_simp
  ring

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.schwartz_fourier_postcomp
#print axioms F1Fecho.MaxwellGlobal.schwartz_fourierInv_postcomp
#print axioms F1Fecho.MaxwellGlobal.physicalFourier_postcomp
#print axioms F1Fecho.MaxwellGlobal.physicalFourier_derivative
