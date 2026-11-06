import TGLExt.V351ScaledResolventFunctions
import TGLExt.V351ResolventImaginaryIntertwining
import TGLExt.V350ScaledPositiveResolvent

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open ChatgptAudit
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem positive_contraction_spectrum_bounds (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) {x : ℝ} (hx : x ∈ spectrum ℝ T) :
    x ∈ Set.Icc (0 : ℝ) 1 := by
  refine ⟨spectrum_nonneg_of_nonneg hT hx,?_⟩
  exact (le_algebraMap_iff_spectrum_le (IsSelfAdjoint.of_nonneg hT)).mp
    (by simpa only [map_one] using h1) x hx

theorem scaledResolventDenominator_real_cfc (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (r : ℝ) :
    cfc (fun x : ℝ => r+(1-r)*x) T = scaledResolventDenominator T r := by
  rw [cfc_const_add r (fun x : ℝ => (1-r)*x) T (by fun_prop) hT,
    cfc_const_mul_id (1-r) T hT,Algebra.algebraMap_eq_smul_one]
  rfl

theorem scaledResolventCoordinate_cfc (T : H →L[ℂ] H) (hT : 0 ≤ T) (h1 : T ≤ 1)
    (r : ℝ) (hr : 0<r) :
    cfc (fun z : ℂ => (scaledResolventCoordinate r z.re : ℂ)) T = scaledPositiveResolvent T r := by
  rw [← cfc_real_eq_complex (scaledResolventCoordinate r) (IsSelfAdjoint.of_nonneg hT)]
  unfold scaledResolventCoordinate scaledPositiveResolvent
  rw [cfc_map_div (fun x : ℝ => x) (fun x : ℝ => r+(1-r)*x) T
      (fun x hx => (scaledResolventDenominator_scalar_pos r hr x
        (positive_contraction_spectrum_bounds T hT h1 hx)).ne')
      (by fun_prop) (by fun_prop) (IsSelfAdjoint.of_nonneg hT),
    cfc_id' ℝ T (IsSelfAdjoint.of_nonneg hT),
    scaledResolventDenominator_real_cfc T (IsSelfAdjoint.of_nonneg hT)]

theorem scaledResolventCoordinate_continuousOn_spectrum (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) :
    ContinuousOn (fun z : ℂ => (scaledResolventCoordinate r z.re : ℂ)) (spectrum ℂ T) := by
  intro z hz
  have hd : r+(1-r)*z.re ≠ 0 := (scaledResolventDenominator_scalar_pos r hr z.re
    (positive_contraction_spectrum_bounds T hT h1 ((IsSelfAdjoint.of_nonneg hT).spectrumRestricts.apply_mem hz))).ne'
  apply ContinuousAt.continuousWithinAt
  unfold scaledResolventCoordinate
  fun_prop

theorem scaledResolventDampingFactor_continuousOn_spectrum (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) :
    ContinuousOn (fun z : ℂ => (scaledResolventDampingFactor r z.re : ℂ)) (spectrum ℂ T) := by
  intro z hz
  have hd : r+(1-r)*z.re ≠ 0 := (scaledResolventDenominator_scalar_pos r hr z.re
    (positive_contraction_spectrum_bounds T hT h1 ((IsSelfAdjoint.of_nonneg hT).spectrumRestricts.apply_mem hz))).ne'
  apply ContinuousAt.continuousWithinAt
  unfold scaledResolventDampingFactor
  have hd2 : (r+(1-r)*z.re)^2 ≠ 0 := pow_ne_zero 2 hd
  fun_prop

/-- The invertible bounded correction to the damping under positive scaling. -/
def scaledResolventDampingOperator (T : H →L[ℂ] H) (r : ℝ) : H →L[ℂ] H :=
  cfc (fun z : ℂ => (scaledResolventDampingFactor r z.re : ℂ)) T

theorem scaledResolventDampingOperator_isUnit (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) :
    IsUnit (scaledResolventDampingOperator T r) := by
  apply (isUnit_cfc_iff _ T (scaledResolventDampingFactor_continuousOn_spectrum T hT h1 r hr)
    (IsSelfAdjoint.of_nonneg hT).isStarNormal).mpr
  intro z hz
  apply Complex.ofReal_ne_zero.mpr
  exact div_ne_zero hr.ne' (pow_ne_zero 2 (scaledResolventDenominator_scalar_pos r hr z.re
    (positive_contraction_spectrum_bounds T hT h1 ((IsSelfAdjoint.of_nonneg hT).spectrumRestricts.apply_mem hz))).ne')

theorem scaledPositiveResolvent_damping (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) :
    resolventDampingOperator (scaledPositiveResolvent T r) =
      resolventDampingOperator T * scaledResolventDampingOperator T r := by
  rw [← resolventDampingOperator_cfc _ (IsSelfAdjoint.of_nonneg (scaledPositiveResolvent_nonneg T hT h1 r hr))]
  rw [← scaledResolventCoordinate_cfc T hT h1 r hr,← cfc_comp'
    (fun z : ℂ => (resolventDamping z.re : ℂ))
    (fun z : ℂ => (scaledResolventCoordinate r z.re : ℂ)) T
    (by unfold resolventDamping; fun_prop)
    (scaledResolventCoordinate_continuousOn_spectrum T hT h1 r hr)
    (IsSelfAdjoint.of_nonneg hT).isStarNormal]
  simp only [Complex.ofReal_re]
  have he : cfc (fun z : ℂ => (resolventDamping (scaledResolventCoordinate r z.re) : ℂ)) T =
      cfc (fun z : ℂ => (resolventDamping z.re : ℂ)*(scaledResolventDampingFactor r z.re : ℂ)) T := by
    apply cfc_congr
    intro z hz
    dsimp only
    rw [scaledResolventCoordinate_damping r z.re (scaledResolventDenominator_scalar_pos r hr z.re
      (positive_contraction_spectrum_bounds T hT h1 ((IsSelfAdjoint.of_nonneg hT).spectrumRestricts.apply_mem hz))).ne',Complex.ofReal_mul]
  rw [he,cfc_mul _ _ T (by unfold resolventDamping; fun_prop)
    (scaledResolventDampingFactor_continuousOn_spectrum T hT h1 r hr),
    resolventDampingOperator_cfc T (IsSelfAdjoint.of_nonneg hT)]
  rfl

theorem scaledPositiveResolvent_phase (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) (t : ℝ) :
    resolventPhaseOperator (scaledPositiveResolvent T r) t =
      modularPhase t (Real.log r) • (resolventPhaseOperator T t * scaledResolventDampingOperator T r) := by
  unfold resolventPhaseOperator
  rw [← scaledResolventCoordinate_cfc T hT h1 r hr,← cfc_comp'
    (fun z : ℂ => resolventPhaseFunction t z.re)
    (fun z : ℂ => (scaledResolventCoordinate r z.re : ℂ)) T
    (((resolventPhaseFunction_continuous t).comp Complex.continuous_re).continuousOn)
    (scaledResolventCoordinate_continuousOn_spectrum T hT h1 r hr)
    (IsSelfAdjoint.of_nonneg hT).isStarNormal]
  simp only [Complex.ofReal_re]
  have he : cfc (fun z : ℂ => resolventPhaseFunction t (scaledResolventCoordinate r z.re)) T =
      cfc (fun z : ℂ => modularPhase t (Real.log r) *
        (resolventPhaseFunction t z.re*(scaledResolventDampingFactor r z.re : ℂ))) T := by
    apply cfc_congr
    intro z hz
    dsimp only
    rw [scaledResolventCoordinate_phase r hr t z.re (scaledResolventDenominator_scalar_pos r hr z.re
      (positive_contraction_spectrum_bounds T hT h1 ((IsSelfAdjoint.of_nonneg hT).spectrumRestricts.apply_mem hz))).ne',mul_assoc]
  rw [he,cfc_const_mul _ _ T (by
      exact (((resolventPhaseFunction_continuous t).comp Complex.continuous_re).continuousOn.mul
        (scaledResolventDampingFactor_continuousOn_spectrum T hT h1 r hr))),
    cfc_mul (fun z : ℂ => resolventPhaseFunction t z.re)
      (fun z : ℂ => (scaledResolventDampingFactor r z.re : ℂ)) T
      (((resolventPhaseFunction_continuous t).comp Complex.continuous_re).continuousOn)
      (scaledResolventDampingFactor_continuousOn_spectrum T hT h1 r hr)]
  rfl

#print axioms positive_contraction_spectrum_bounds
#print axioms scaledResolventDenominator_real_cfc
#print axioms scaledResolventCoordinate_cfc
#print axioms scaledResolventCoordinate_continuousOn_spectrum
#print axioms scaledResolventDampingFactor_continuousOn_spectrum
#print axioms scaledResolventDampingOperator
#print axioms scaledResolventDampingOperator_isUnit
#print axioms scaledPositiveResolvent_damping
#print axioms scaledPositiveResolvent_phase
end
end TGLV350.Regular
