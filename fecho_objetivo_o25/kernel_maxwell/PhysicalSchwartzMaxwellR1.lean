import GlobalMaxwellSegalR1

/-! ADDITIVE PHYSICAL CONVENTION ADAPTER. Existing negative-2pi Fourier maps
remain intact. Here inverse Fourier evaluated at metricFlip(p)/(2*pi) has
positive angular phase exp(+i p.x), matching the canonical U1 convention.
Translation covariance and wedge localization require their own consumers. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open SchwartzMap FourierTransform
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Creation F1Fecho.Annihilation
open scoped FourierTransform

def angularScale : Spacetime ≃L[ℝ] Spacetime :=
  { LinearEquiv.smulOfNeZero ℝ Spacetime ((2*Real.pi)⁻¹)
      (inv_ne_zero (mul_ne_zero (by norm_num) Real.pi_ne_zero)) with
    continuous_toFun := continuous_const_smul _
    continuous_invFun := continuous_const_smul _ }

def physicalFourierArgument : Spacetime ≃L[ℝ] Spacetime :=
  metricFlip.toContinuousLinearEquiv.trans angularScale

theorem physicalFourierArgument_apply (p : Spacetime) :
    physicalFourierArgument p=(2*Real.pi)⁻¹ • metricFlip p := rfl

def physicalFourierCLM : SchwartzTensor →L[ℂ] SchwartzTensor :=
  (SchwartzMap.compCLMOfContinuousLinearEquiv ℂ physicalFourierArgument).comp
    (FourierTransform.fourierInvCLM ℂ SchwartzTensor)

theorem physicalFourier_apply (f : SchwartzTensor) (p : Spacetime) :
    physicalFourierCLM f p=(𝓕⁻ f) ((2*Real.pi)⁻¹ • metricFlip p) := rfl

theorem physicalFourier_surjective : Function.Surjective physicalFourierCLM := by
  intro g
  let h:=SchwartzMap.compCLMOfContinuousLinearEquiv ℂ physicalFourierArgument.symm g
  refine ⟨𝓕 h,?_⟩
  ext p : 1
  change (𝓕⁻ (𝓕 h)) (physicalFourierArgument p)=g p
  rw [FourierTransform.fourierInv_fourier_eq]
  change g (physicalFourierArgument.symm (physicalFourierArgument p))=g p
  rw [ContinuousLinearEquiv.symm_apply_apply]

def physicalSmearCLM : SchwartzTensor →L[ℂ] H1 := momentumSmearCLM.comp physicalFourierCLM

theorem physicalSmear_ae (f : SchwartzTensor) :
    physicalSmearCLM f =ᵐ[ChatgptAudit.WignerRapidityMeasure016.orbitalMeasure 0]
      globalCoefficient (physicalFourierCLM f) :=
  (globalCoefficient_memLp (physicalFourierCLM f)).coeFn_toLp

theorem exists_nonzero_real_physicalSmear : ∃ f : RealTest,physicalSmearCLM f.val≠0 := by
  obtain ⟨g,hg⟩:=exists_nonzero_momentumSmear
  obtain ⟨f,hf⟩:=physicalFourier_surjective g
  have hn : physicalSmearCLM f≠0 := by
    change momentumSmear (physicalFourierCLM f)≠0
    rwa [hf]
  by_cases hr : physicalSmearCLM (realPart f)=0
  · refine ⟨⟨imagPart f,imagPart_real f⟩,?_⟩
    intro hi
    apply hn
    have hd:=congrArg physicalSmearCLM (real_imag_decomposition f)
    rw [map_add,map_smul,hr,hi,smul_zero,add_zero] at hd
    exact hd
  · exact ⟨⟨realPart f,realPart_real f⟩,hr⟩

def physicalField (f : RealTest) : F →ₗ.[ℂ] F := segal (physicalSmearCLM f.val)

theorem physicalField_essentially_selfadjoint (f : RealTest) :
    IsSelfAdjoint (physicalField f).closure := segal_essentially_selfadjoint _

theorem physicalField_has_exponential_core (f : RealTest) :
    (physicalField f).closure.HasCore domain := segal_closure_has_exponential_core _

theorem physicalField_vacuum (f : RealTest) :
    physicalField f ⟨vacuum,vacuum_mem_domain⟩ =
      ((Real.sqrt 2)⁻¹ : ℂ) • oneParticle (physicalSmearCLM f.val) := segal_vacuum _

theorem exists_nonzero_physicalField_vacuum : ∃ f : RealTest,
    physicalField f ⟨vacuum,vacuum_mem_domain⟩≠0 := by
  obtain ⟨f,hf⟩:=exists_nonzero_real_physicalSmear
  refine ⟨f,?_⟩
  rw [physicalField_vacuum]
  apply smul_ne_zero
  · exact inv_ne_zero (Complex.ofReal_ne_zero.mpr (Real.sqrt_ne_zero'.mpr (by norm_num)))
  · intro hz
    apply hf
    apply oneParticle.injective
    simpa using hz

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.physicalFourier_apply
#print axioms F1Fecho.MaxwellGlobal.physicalFourier_surjective
#print axioms F1Fecho.MaxwellGlobal.physicalSmear_ae
#print axioms F1Fecho.MaxwellGlobal.exists_nonzero_real_physicalSmear
#print axioms F1Fecho.MaxwellGlobal.physicalField_essentially_selfadjoint
#print axioms F1Fecho.MaxwellGlobal.physicalField_has_exponential_core
#print axioms F1Fecho.MaxwellGlobal.exists_nonzero_physicalField_vacuum
