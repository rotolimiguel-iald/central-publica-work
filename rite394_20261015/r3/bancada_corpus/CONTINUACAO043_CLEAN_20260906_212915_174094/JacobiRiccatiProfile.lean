import OpticalAreaFreedom

set_option autoImplicit false
set_option maxHeartbeats 2000000
namespace ChatgptAudit.Optical043
open Matrix Filter Set TGLExt ChatgptAudit ChatgptAudit.Optical036
open scoped Topology ContDiff
noncomputable section

/-- The affine null coordinate of the fixed plane-wave chart. -/
def opticalPhaseCoordinate (x : Coordinate4) : ℝ := x 0+x 3

/-- The logarithmic Jacobi rate, used only away from zeros in differential claims. -/
def jacobiLogDerivative (a t : ℝ) : ℝ :=
  jacobiOscillatorVelocity a t / jacobiOscillator a t

/-- An open domain excluding all zeros of the two chosen Jacobi solutions. -/
def opticalCongruenceDomain (a c : ℝ) : Set Coordinate4 :=
  {x | jacobiOscillator a (opticalPhaseCoordinate x)≠0 ∧
    jacobiOscillator c (opticalPhaseCoordinate x)≠0}

theorem optical_phase_coordinate_contDiff : ContDiff ℝ ∞ opticalPhaseCoordinate := by
  unfold opticalPhaseCoordinate
  fun_prop

theorem optical_phase_coordinate_hasFDerivAt (x : Coordinate4) :
    HasFDerivAt opticalPhaseCoordinate
      (ContinuousLinearMap.proj (0:Fin 4)+ContinuousLinearMap.proj (3:Fin 4)) x := by
  exact (hasFDerivAt_apply (𝕜 := ℝ) 0 x).add (hasFDerivAt_apply (𝕜 := ℝ) 3 x)

theorem optical_phase_coordinate_central (t : ℝ) :
    opticalPhaseCoordinate (centralNullCurve t)=t := by
  change t*(1/2:ℝ)+t*(1/2:ℝ)=t
  ring

theorem jacobi_oscillator_smooth (a : ℝ) : ContDiff ℝ ∞ (jacobiOscillator a) := by
  unfold jacobiOscillator
  fun_prop

theorem jacobi_velocity_smooth (a : ℝ) : ContDiff ℝ ∞ (jacobiOscillatorVelocity a) := by
  unfold jacobiOscillatorVelocity
  fun_prop

theorem jacobi_log_derivative_zero (a : ℝ) : jacobiLogDerivative a 0=0 := by
  simp [jacobiLogDerivative,jacobiOscillator,jacobiOscillatorVelocity]

theorem jacobi_log_derivative_mul (a t : ℝ) (ht : jacobiOscillator a t≠0) :
    jacobiLogDerivative a t*jacobiOscillator a t=jacobiOscillatorVelocity a t := by
  exact div_mul_cancel₀ _ ht

theorem jacobi_log_derivative_hasDerivAt (a : ℝ) (ha : 0≤a) (t : ℝ)
    (ht : jacobiOscillator a t≠0) :
    HasDerivAt (jacobiLogDerivative a) (-a-(jacobiLogDerivative a t)^2) t := by
  have h := (jacobi_oscillator_velocity_hasDerivAt a ha t).div
    (jacobi_oscillator_hasDerivAt a t) ht
  apply h.congr_deriv
  unfold jacobiLogDerivative
  field_simp [ht]
  ring

theorem jacobi_log_derivative_contDiffAt (a t : ℝ) (ht : jacobiOscillator a t≠0) :
    ContDiffAt ℝ ∞ (jacobiLogDerivative a) t :=
  (jacobi_velocity_smooth a).contDiffAt.div (jacobi_oscillator_smooth a).contDiffAt ht

theorem jacobi_log_profile_smooth (a : ℝ) (U : Set Coordinate4)
    (hU : ∀ x∈U, jacobiOscillator a (opticalPhaseCoordinate x)≠0) :
    ContDiffOn ℝ ∞ (fun x => jacobiLogDerivative a (opticalPhaseCoordinate x)) U := by
  have hn : ContDiff ℝ ∞ (fun x => jacobiOscillatorVelocity a (opticalPhaseCoordinate x)) :=
    (jacobi_velocity_smooth a).comp optical_phase_coordinate_contDiff
  have hd : ContDiff ℝ ∞ (fun x => jacobiOscillator a (opticalPhaseCoordinate x)) :=
    (jacobi_oscillator_smooth a).comp optical_phase_coordinate_contDiff
  exact hn.contDiffOn.div hd.contDiffOn hU

theorem optical_congruence_domain_open (a c : ℝ) :
    IsOpen (opticalCongruenceDomain a c) := by
  have ha : Continuous (fun x => jacobiOscillator a (opticalPhaseCoordinate x)) :=
    ((jacobi_oscillator_smooth a).comp optical_phase_coordinate_contDiff).continuous
  have hc : Continuous (fun x => jacobiOscillator c (opticalPhaseCoordinate x)) :=
    ((jacobi_oscillator_smooth c).comp optical_phase_coordinate_contDiff).continuous
  exact (isOpen_ne ha continuous_const).inter (isOpen_ne hc continuous_const)

theorem optical_congruence_domain_origin (a c : ℝ) :
    (0:Coordinate4)∈opticalCongruenceDomain a c := by
  simp [opticalCongruenceDomain,opticalPhaseCoordinate,jacobiOscillator]

theorem optical_congruence_domain_central_iff (a c t : ℝ) :
    centralNullCurve t∈opticalCongruenceDomain a c ↔
      jacobiOscillator a t≠0 ∧ jacobiOscillator c t≠0 := by
  simp only [opticalCongruenceDomain,Set.mem_setOf_eq,optical_phase_coordinate_central]

theorem optical_congruence_domain_eventually (a c : ℝ) :
    ∀ᶠ t in 𝓝 (0:ℝ), centralNullCurve t∈opticalCongruenceDomain a c := by
  have hp : centralNullCurve 0∈opticalCongruenceDomain a c := by
    simpa only [centralNullCurve,zero_smul] using optical_congruence_domain_origin a c
  exact (central_curve_derivative 0).continuousAt.eventually
    ((optical_congruence_domain_open a c).mem_nhds hp)

#print axioms opticalPhaseCoordinate
#print axioms jacobiLogDerivative
#print axioms opticalCongruenceDomain
#print axioms optical_phase_coordinate_contDiff
#print axioms optical_phase_coordinate_hasFDerivAt
#print axioms optical_phase_coordinate_central
#print axioms jacobi_oscillator_smooth
#print axioms jacobi_velocity_smooth
#print axioms jacobi_log_derivative_zero
#print axioms jacobi_log_derivative_mul
#print axioms jacobi_log_derivative_hasDerivAt
#print axioms jacobi_log_derivative_contDiffAt
#print axioms jacobi_log_profile_smooth
#print axioms optical_congruence_domain_open
#print axioms optical_congruence_domain_origin
#print axioms optical_congruence_domain_central_iff
#print axioms optical_congruence_domain_eventually
end
end ChatgptAudit.Optical043
