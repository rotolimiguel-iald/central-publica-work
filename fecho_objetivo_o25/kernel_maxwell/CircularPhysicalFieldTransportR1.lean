import FockSegalUnitaryTransportR1
import RegularCircularTransportR2
import PhysicalSmearTranslationR2
import UnitaryFourierRealStressR2

/-! Candidate R50. Explicit circular/linear-screen transport on the SAME
canonical H1, Fock and regular coherent domain. The old physicalField remains
unchanged. The normalized field uses the fixed amplitude sqrt((2*pi)^(-3))
already determined by the angular/unitary Fourier chain.
Bilocal Wick covariance below does not assert a coincident-point limit or an
identification with the local calibrated Maxwell tensor. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
noncomputable section

namespace F1Fecho.MaxwellGlobal
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.BosonicFockGroupActions
open F1Fecho.Exponential F1Fecho.Annihilation F1Fecho.Creation
open F1Fecho.FockSegalTransport F1Fecho.OrbitalScreen F1Fecho.MaxwellLocalization

/-- The existing circular smearing, now bundled as a continuous linear map. -/
def circularSmearCLM : SchwartzTensor →L[ℂ] H1 :=
  circularH1.symm.toLinearIsometry.toContinuousLinearMap.comp physicalSmearCLM

theorem circularSmearCLM_apply (f : SchwartzTensor) :
    circularSmearCLM f = circularSmear f := rfl

theorem circularH1_circularSmear (f : SchwartzTensor) :
    circularH1 (circularSmearCLM f) = physicalSmearCLM f :=
  circularH1.apply_symm_apply (physicalSmearCLM f)

theorem regularFockDomain_le_exponentialDomain : regularFockDomain ≤ domain := by
  rw [regularFockDomain_eq_span]
  apply Submodule.span_le.mpr
  rintro v ⟨h, rfl⟩
  exact exponential_mem_domain h.val

def regularDomainInput : regularFockDomain →ₗ[ℂ] domain :=
  Submodule.inclusion regularFockDomain_le_exponentialDomain

theorem domainGamma_regularCircular (ψ : regularFockDomain) :
    domainGamma circularH1 (regularDomainInput ψ) =
      regularDomainInput (regularCircular ψ) := by
  apply Subtype.ext
  rfl

def regularCircularInverse (ψ : regularFockDomain) : regularFockDomain :=
  regularGamma circularH1.symm strongRegularProfile_circular_symm ψ

theorem regularCircular_left_inverse (ψ : regularFockDomain) :
    regularCircularInverse (regularCircular ψ) = ψ := by
  apply Subtype.ext
  change gamma circularH1.symm (gamma circularH1 ψ.val) = ψ.val
  rw [gamma_symm, LinearIsometryEquiv.symm_apply_apply]

theorem regularCircular_right_inverse (ψ : regularFockDomain) :
    regularCircular (regularCircularInverse ψ) = ψ := by
  apply Subtype.ext
  change gamma circularH1 (gamma circularH1.symm ψ.val) = ψ.val
  rw [gamma_symm, LinearIsometryEquiv.apply_symm_apply]

theorem regularCircular_norm (ψ : regularFockDomain) :
    ‖(regularCircular ψ).val‖ = ‖ψ.val‖ :=
  (gamma circularH1).norm_map ψ.val

theorem gamma_circular_U1 (a : Fin 4 → ℝ) (ψ : F) :
    gamma circularH1 (gamma (U1 a) ψ) =
      gamma (U1 a) (gamma circularH1 ψ) := by
  have hu : (U1 a).trans circularH1 = circularH1.trans (U1 a) := by
    apply LinearIsometryEquiv.ext
    intro h
    exact fiberLift_U1 circularFiber a h
  have hg := congrArg gamma hu
  rw [gamma_trans, gamma_trans] at hg
  exact congrArg (fun e : F ≃ₗᵢ[ℂ] F => e ψ) hg

theorem gamma_circular_B0 (s : ℝ) (ψ : F) :
    gamma circularH1 (gamma (B0 s) ψ) =
      gamma (B0 s) (gamma circularH1 ψ) := by
  have hu : (B0 s).trans circularH1 = circularH1.trans (B0 s) := by
    apply LinearIsometryEquiv.ext
    intro h
    exact fiberLift_B0 circularFiber s h
  have hg := congrArg gamma hu
  rw [gamma_trans, gamma_trans] at hg
  exact congrArg (fun e : F ≃ₗᵢ[ℂ] F => e ψ) hg

def circularField (f : RealTest) : F →ₗ.[ℂ] F :=
  segal (circularSmearCLM f.val)

theorem circularField_essentially_selfadjoint (f : RealTest) :
    IsSelfAdjoint (circularField f).closure := segal_essentially_selfadjoint _

/-- Field equality includes transport of the actual state and operator domain. -/
theorem circularField_intertwines (f : RealTest) (x : domain) :
    gamma circularH1 (circularField f x) =
      physicalField f (domainGamma circularH1 x) := by
  have ht := segal_gamma circularH1 (circularSmearCLM f.val) x
  rw [circularH1_circularSmear] at ht
  exact ht.symm

theorem circularField_intertwines_regular (f : RealTest) (ψ : regularFockDomain) :
    gamma circularH1 (circularField f (regularDomainInput ψ)) =
      physicalField f (regularDomainInput (regularCircular ψ)) := by
  rw [circularField_intertwines, domainGamma_regularCircular]

/-- Fixed positive amplitude from the already derived Fourier stress scale. -/
def unitaryFourierFieldAmplitude : ℝ := Real.sqrt unitaryFourierStressScale

theorem unitaryFourierFieldAmplitude_pos : 0 < unitaryFourierFieldAmplitude :=
  Real.sqrt_pos.mpr unitaryFourierStressScale_pos

theorem unitaryFourierFieldAmplitude_sq :
    unitaryFourierFieldAmplitude ^ 2 = unitaryFourierStressScale :=
  Real.sq_sqrt (le_of_lt unitaryFourierStressScale_pos)

def normalizedPhysicalSmearCLM : SchwartzTensor →L[ℂ] H1 :=
  (unitaryFourierFieldAmplitude : ℂ) • physicalSmearCLM

def normalizedCircularSmearCLM : SchwartzTensor →L[ℂ] H1 :=
  (unitaryFourierFieldAmplitude : ℂ) • circularSmearCLM

theorem circularH1_normalizedCircularSmear (f : SchwartzTensor) :
    circularH1 (normalizedCircularSmearCLM f) = normalizedPhysicalSmearCLM f := by
  change circularH1 ((unitaryFourierFieldAmplitude : ℂ) • circularSmearCLM f) =
    (unitaryFourierFieldAmplitude : ℂ) • physicalSmearCLM f
  rw [map_smul, circularH1_circularSmear]

def normalizedPhysicalField (f : RealTest) : F →ₗ.[ℂ] F :=
  segal (normalizedPhysicalSmearCLM f.val)

def normalizedCircularField (f : RealTest) : F →ₗ.[ℂ] F :=
  segal (normalizedCircularSmearCLM f.val)

theorem normalizedPhysicalField_eq_amplitude (f : RealTest) (x : domain) :
    normalizedPhysicalField f x =
      (unitaryFourierFieldAmplitude : ℂ) • physicalField f x :=
  segal_parameter_real_smul unitaryFourierFieldAmplitude (physicalSmearCLM f.val) x

theorem normalizedCircularField_essentially_selfadjoint (f : RealTest) :
    IsSelfAdjoint (normalizedCircularField f).closure := segal_essentially_selfadjoint _

theorem normalizedCircularField_intertwines_regular (f : RealTest) (ψ : regularFockDomain) :
    gamma circularH1 (normalizedCircularField f (regularDomainInput ψ)) =
      normalizedPhysicalField f (regularDomainInput (regularCircular ψ)) := by
  have ht := segal_gamma circularH1 (normalizedCircularSmearCLM f.val) (regularDomainInput ψ)
  rw [circularH1_normalizedCircularSmear, domainGamma_regularCircular] at ht
  exact ht.symm

/-- Transport of the bilocal Wick form on arbitrary regular finite coherent
sums. This statement keeps both test functions; it is not local coincidence. -/
theorem normalizedCircularWick_transport (f g : SchwartzTensor) (ψ χ : regularFockDomain) :
    F1Fecho.WickForm.quadratic (normalizedCircularSmearCLM f)
      (normalizedCircularSmearCLM g) (regularDomainInput ψ) (regularDomainInput χ) =
    F1Fecho.WickForm.quadratic (normalizedPhysicalSmearCLM f)
      (normalizedPhysicalSmearCLM g)
      (regularDomainInput (regularCircular ψ)) (regularDomainInput (regularCircular χ)) := by
  have ht := wick_quadratic_gamma circularH1 (normalizedCircularSmearCLM f)
    (normalizedCircularSmearCLM g) (regularDomainInput ψ) (regularDomainInput χ)
  rw [circularH1_normalizedCircularSmear, circularH1_normalizedCircularSmear,
    domainGamma_regularCircular, domainGamma_regularCircular] at ht
  exact ht.symm

theorem exists_nonzero_normalizedCircularField_vacuum :
    ∃ f : RealTest, normalizedCircularField f ⟨vacuum, vacuum_mem_domain⟩ ≠ 0 := by
  obtain ⟨f, hf⟩ := exists_nonzero_real_circularSmear
  refine ⟨f, ?_⟩
  change segal (normalizedCircularSmearCLM f.val) ⟨vacuum, vacuum_mem_domain⟩ ≠ 0
  rw [segal_vacuum]
  apply smul_ne_zero
  · exact inv_ne_zero (Complex.ofReal_ne_zero.mpr
      (Real.sqrt_ne_zero'.mpr (by norm_num : (0 : ℝ) < 2)))
  · intro hz
    have hh : normalizedCircularSmearCLM f.val = 0 :=
      oneParticle.injective (by simpa only [map_zero] using hz)
    have hn : (unitaryFourierFieldAmplitude : ℂ) • circularSmear f.val ≠ 0 :=
      smul_ne_zero (Complex.ofReal_ne_zero.mpr unitaryFourierFieldAmplitude_pos.ne') hf
    exact hn hh

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.circularSmearCLM_apply
#print axioms F1Fecho.MaxwellGlobal.circularH1_circularSmear
#print axioms F1Fecho.MaxwellGlobal.regularFockDomain_le_exponentialDomain
#print axioms F1Fecho.MaxwellGlobal.domainGamma_regularCircular
#print axioms F1Fecho.MaxwellGlobal.regularCircular_left_inverse
#print axioms F1Fecho.MaxwellGlobal.regularCircular_right_inverse
#print axioms F1Fecho.MaxwellGlobal.regularCircular_norm
#print axioms F1Fecho.MaxwellGlobal.gamma_circular_U1
#print axioms F1Fecho.MaxwellGlobal.gamma_circular_B0
#print axioms F1Fecho.MaxwellGlobal.circularField_essentially_selfadjoint
#print axioms F1Fecho.MaxwellGlobal.circularField_intertwines
#print axioms F1Fecho.MaxwellGlobal.circularField_intertwines_regular
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierFieldAmplitude_pos
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierFieldAmplitude_sq
#print axioms F1Fecho.MaxwellGlobal.circularH1_normalizedCircularSmear
#print axioms F1Fecho.MaxwellGlobal.normalizedPhysicalField_eq_amplitude
#print axioms F1Fecho.MaxwellGlobal.normalizedCircularField_essentially_selfadjoint
#print axioms F1Fecho.MaxwellGlobal.normalizedCircularField_intertwines_regular
#print axioms F1Fecho.MaxwellGlobal.normalizedCircularWick_transport
#print axioms F1Fecho.MaxwellGlobal.exists_nonzero_normalizedCircularField_vacuum

