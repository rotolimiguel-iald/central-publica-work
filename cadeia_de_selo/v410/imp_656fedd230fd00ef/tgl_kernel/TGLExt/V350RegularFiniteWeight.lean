import TGLExt.V350RegularApproximation
import TGLExt.V350FourierL1L2
import TGLExt.V350DualWeightForm
import Mathlib.MeasureTheory.Measure.Haar.NormedSpace
import Mathlib.MeasureTheory.Function.LpSeminorm.Indicator

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 2500000

namespace TGLV350.Regular
open MeasureTheory FourierTransform
open scoped FourierTransform ENNReal
noncomputable section

/-- The actual Hilbert-valued regular orbit restricted to a finite interval. -/
def regularOrbitCut (P : TGLExt.SiteProfile) (h : ℝ)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    ℝ → RegularHilbert (TGLExt.TowerHilbert P) :=
  (Set.Ioc 0 h).indicator (fun t => regularUnitary P t v)

theorem regularOrbitCut_memLp (P : TGLExt.SiteProfile) (h : ℝ)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) (p : ℝ≥0∞) :
    MemLp (regularOrbitCut P h v) p := by
  have hc := memLp_indicator_const p measurableSet_Ioc ‖v‖
    (Or.inr (show volume (Set.Ioc 0 h) ≠ ⊤ by simp [Real.volume_Ioc]))
  apply hc.congr_norm
    ((regular_strongly_continuous P v).stronglyMeasurable.indicator measurableSet_Ioc).aestronglyMeasurable
  filter_upwards [] with t
  by_cases ht : t ∈ Set.Ioc 0 h
  · simp [ht, regular_norm_map]
  · simp [ht]

theorem regularOrbitCut_integrable (P : TGLExt.SiteProfile) (h : ℝ)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    Integrable (regularOrbitCut P h v) :=
  memLp_one_iff_integrable.mp (regularOrbitCut_memLp P h v 1)

theorem regularOrbitCut_integral_norm_sq (P : TGLExt.SiteProfile) (h : ℝ) (hh : 0 < h)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    (∫ t : ℝ, ‖regularOrbitCut P h v t‖ ^ 2) = h * ‖v‖ ^ 2 := by
  have heq : (fun t => ‖regularOrbitCut P h v t‖ ^ 2) =
      (Set.Ioc 0 h).indicator (fun _ => ‖v‖ ^ 2) := by
    funext t
    by_cases ht : t ∈ Set.Ioc 0 h <;> simp [regularOrbitCut, ht, regular_norm_map]
  rw [heq, integral_indicator measurableSet_Ioc, setIntegral_const]
  simp [Measure.real, Real.volume_Ioc, ENNReal.toReal_ofReal hh.le]

theorem regularAverage_dual_fourier (P : TGLExt.SiteProfile) (s h : ℝ) (hh : 0 < h)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    dualAmbient s (regularAverage P h) v =
      h⁻¹ • (𝓕 (regularOrbitCut P h v)) (s / (2 * Real.pi)) := by
  rw [regularAverage_dual_apply, Real.fourier_real_eq_integral_exp_smul]
  congr 1
  rw [intervalIntegral.integral_of_le hh.le]
  have heq : (fun t : ℝ => Complex.exp (↑(-2 * Real.pi * t * (s / (2 * Real.pi))) * Complex.I) •
      regularOrbitCut P h v t) =
      (Set.Ioc 0 h).indicator (fun t => characterPhase s t • regularUnitary P t v) := by
    funext t
    by_cases ht : t ∈ Set.Ioc 0 h
    · simp only [regularOrbitCut, Set.indicator_of_mem ht]
      congr 2
      push_cast
      field_simp
    · simp [regularOrbitCut, ht]
  rw [heq, integral_indicator measurableSet_Ioc]
  rfl

theorem regularAverage_dual_sq_integrable (P : TGLExt.SiteProfile) (h : ℝ) (hh : 0 < h)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    Integrable (fun s : ℝ => ‖dualAmbient s (regularAverage P h) v‖ ^ 2) := by
  have hf := Fourier.fourier_integral_memLp_two _
    (regularOrbitCut_integrable P h v) (regularOrbitCut_memLp P h v 2)
  have hi := ((memLp_two_iff_integrable_sq_norm hf.1).mp hf).comp_div
    (show (2 * Real.pi : ℝ) ≠ 0 by positivity)
  simpa only [regularAverage_dual_fourier P _ h hh v, norm_smul, Real.norm_eq_abs, mul_pow]
    using hi.const_mul (|h⁻¹| ^ 2)

theorem regularAverage_dual_integral_norm_sq (P : TGLExt.SiteProfile) (h : ℝ) (hh : 0 < h)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    (∫ s : ℝ, ‖dualAmbient s (regularAverage P h) v‖ ^ 2) =
      (2 * Real.pi) * h⁻¹ * ‖v‖ ^ 2 := by
  simp_rw [regularAverage_dual_fourier P _ h hh v, norm_smul, Real.norm_eq_abs, mul_pow]
  let g : ℝ → ℝ := fun x => ‖(𝓕 (regularOrbitCut P h v)) x‖ ^ 2
  have hd := Measure.integral_comp_div g (2 * Real.pi)
  change (∫ x : ℝ, ‖(𝓕 (regularOrbitCut P h v)) (x / (2 * Real.pi))‖ ^ 2) =
    |2 * Real.pi| • (∫ x : ℝ, ‖(𝓕 (regularOrbitCut P h v)) x‖ ^ 2) at hd
  rw [integral_const_mul, hd,
    Fourier.fourier_integral_norm_sq _ (regularOrbitCut_integrable P h v)
      (regularOrbitCut_memLp P h v 2), regularOrbitCut_integral_norm_sq P h hh v]
  rw [abs_of_pos (inv_pos.mpr hh), abs_of_pos (by positivity : 0 < 2 * Real.pi)]
  simp only [smul_eq_mul]
  field_simp

theorem dualQuadraticIntegrand_star_mul
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) (s : ℝ) :
    dualQuadraticIntegrand (star A * A) v s =
      ENNReal.ofReal (‖dualAmbient s A v‖ ^ 2) := by
  unfold dualQuadraticIntegrand
  rw [map_mul, map_star]
  change ENNReal.ofReal (inner ℂ v ((dualAmbient s A).adjoint (dualAmbient s A v))).re = _
  rw [ContinuousLinearMap.adjoint_inner_right]
  exact congrArg ENNReal.ofReal (inner_self_eq_norm_sq (𝕜 := ℂ) (dualAmbient s A v))

/-- Uniform finite form for the square of the averaging operator. The coefficient
is 1/h with the already fixed dual Haar convention, not an imposed normalization. -/
theorem regularAverage_dualQuadraticIntegral (P : TGLExt.SiteProfile) (h : ℝ) (hh : 0 < h)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    dualQuadraticIntegral (star (regularAverage P h) * regularAverage P h) v =
      ENNReal.ofReal (h⁻¹ * ‖v‖ ^ 2) := by
  simp only [dualQuadraticIntegral, dualQuadraticIntegrand_star_mul]
  rw [← ofReal_integral_eq_lintegral_ofReal (regularAverage_dual_sq_integrable P h hh v)
    (Filter.Eventually.of_forall (fun s => sq_nonneg _)),
    regularAverage_dual_integral_norm_sq P h hh v,
    ← ENNReal.ofReal_mul dualHaarFactor_pos.le]
  congr 1
  unfold dualHaarFactor
  field_simp

theorem regularAverage_dualQuadraticIntegral_lt_top (P : TGLExt.SiteProfile)
    (h : ℝ) (hh : 0 < h) (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    dualQuadraticIntegral (star (regularAverage P h) * regularAverage P h) v < ⊤ := by
  rw [regularAverage_dualQuadraticIntegral P h hh v]
  exact ENNReal.ofReal_lt_top

#print axioms regularOrbitCut
#print axioms regularOrbitCut_memLp
#print axioms regularOrbitCut_integrable
#print axioms regularOrbitCut_integral_norm_sq
#print axioms regularAverage_dual_fourier
#print axioms regularAverage_dual_sq_integrable
#print axioms regularAverage_dual_integral_norm_sq
#print axioms dualQuadraticIntegrand_star_mul
#print axioms regularAverage_dualQuadraticIntegral
#print axioms regularAverage_dualQuadraticIntegral_lt_top
end
end TGLV350.Regular
