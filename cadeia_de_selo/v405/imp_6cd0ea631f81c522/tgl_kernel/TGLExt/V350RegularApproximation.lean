import TGLExt.V350StrongOperatorIntegral
import TGLExt.V350DualWeightCuts
import TGLExt.V350DualQuadraticLaws
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Analysis.Calculus.Deriv.Slope

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open MeasureTheory Filter
open scoped Topology
noncomputable section

def regularBundledUnitary (P : TGLExt.SiteProfile) (t : ℝ) :
    unitary (RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P)) :=
  ⟨regularUnitary P t, Unitary.mem_iff.mpr (regular_unitary P t)⟩

theorem regular_norm_map (P : TGLExt.SiteProfile) (t : ℝ)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    ‖regularUnitary P t v‖ = ‖v‖ := Unitary.norm_map (regularBundledUnitary P t) v

def regularIntegralFamily (P : TGLExt.SiteProfile) :
    StrongIntegral.Family (H := RegularHilbert (TGLExt.TowerHilbert P)) where
  op := regularUnitary P
  continuous_apply := regular_strongly_continuous P
  bound := 1
  bound_nonneg := zero_le_one
  norm_bound := fun t => ContinuousLinearMap.opNorm_le_bound _ zero_le_one
    (fun v => by rw [regular_norm_map, one_mul])

/-- One-sided normalized averages of the actual regular unitaries. The value
at h=0 is zero; convergence is asserted on the punctured neighborhood. -/
def regularAverage (P : TGLExt.SiteProfile) (h : ℝ) :
    RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P) :=
  (h⁻¹ : ℝ) • StrongIntegral.operatorIntegral (regularIntegralFamily P) 0 h

theorem regularAverage_apply (P : TGLExt.SiteProfile) (h : ℝ)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    regularAverage P h v = h⁻¹ • ∫ t in 0..h, regularUnitary P t v := rfl

theorem regularAverage_mem (P : TGLExt.SiteProfile) (h : ℝ) :
    regularAverage P h ∈ regularCoreAlgebra P := by
  change ((h⁻¹ : ℝ) : ℂ) • StrongIntegral.operatorIntegral (regularIntegralFamily P) 0 h ∈ _
  apply (regularCoreAlgebra P).toStarSubalgebra.smul_mem
  exact StrongIntegral.operatorIntegral_mem _ _ _ _ (regularUnitary_mem P)

theorem regularAverage_norm_le_one (P : TGLExt.SiteProfile) (h : ℝ) :
    ‖regularAverage P h‖ ≤ 1 := by
  by_cases hh : h = 0
  · subst h
    simp [regularAverage]
  · have hb := StrongIntegral.operatorIntegral_norm_le (regularIntegralFamily P) 0 h
    change ‖StrongIntegral.operatorIntegral (regularIntegralFamily P) 0 h‖ ≤ 1 * |h-0| at hb
    simp only [sub_zero, one_mul] at hb
    calc
      ‖regularAverage P h‖ = |h⁻¹| * ‖StrongIntegral.operatorIntegral (regularIntegralFamily P) 0 h‖ := by
        change ‖((h⁻¹ : ℝ) : ℂ) • StrongIntegral.operatorIntegral (regularIntegralFamily P) 0 h‖ = _
        rw [norm_smul, Complex.norm_real, Real.norm_eq_abs]
      _ ≤ |h⁻¹| * |h| := mul_le_mul_of_nonneg_left hb (abs_nonneg _)
      _ = 1 := by rw [abs_inv, inv_mul_cancel₀ (abs_ne_zero.mpr hh)]

/-- The fundamental theorem of calculus gives strong convergence without
operator-norm continuity of the unitary group. -/
theorem regularAverage_tendsto_identity (P : TGLExt.SiteProfile)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    Tendsto (fun h : ℝ => regularAverage P h v) (𝓝[≠] 0) (𝓝 v) := by
  have hc := regular_strongly_continuous P v
  have hd := intervalIntegral.integral_hasDerivAt_right
    (hc.intervalIntegrable 0 0) hc.stronglyMeasurable.stronglyMeasurableAtFilter hc.continuousAt
  have ht := hd.tendsto_slope_zero
  simpa only [zero_add, intervalIntegral.integral_same, sub_zero,
    regular_zero, one_apply_eq_self, regularAverage_apply] using ht

theorem regularAverage_mul_tendsto (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P))
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    Tendsto (fun h : ℝ => (A * regularAverage P h) v) (𝓝[≠] 0) (𝓝 (A v)) :=
  A.continuous.continuousAt.tendsto.comp (regularAverage_tendsto_identity P v)

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem dualAmbient_strongIntegral_apply (s : ℝ)
    (F : StrongIntegral.Family (H := RegularHilbert H)) (a b : ℝ)
    (v : RegularHilbert H) :
    dualAmbient s (StrongIntegral.operatorIntegral F a b) v =
      ∫ t in a..b, dualAmbient s (F.op t) v := by
  change characterMultiplier s (∫ t in a..b, F.op t (star (characterMultiplier s) v)) =
    ∫ t in a..b, characterMultiplier s (F.op t (star (characterMultiplier s) v))
  exact ((characterMultiplier s).intervalIntegral_comp_comm (μ := volume)
    ((F.continuous_apply _).intervalIntegrable a b)).symm

/-- The dual orbit of the average is the Fourier-modulated vector integral
of the same regular unitary group. -/
theorem regularAverage_dual_apply (P : TGLExt.SiteProfile) (s h : ℝ)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    dualAmbient s (regularAverage P h) v =
      h⁻¹ • ∫ t in 0..h, characterPhase s t • regularUnitary P t v := by
  unfold regularAverage
  rw [dualAmbient_real_smul]
  change h⁻¹ • (dualAmbient s (StrongIntegral.operatorIntegral (regularIntegralFamily P) 0 h) v) = _
  rw [dualAmbient_strongIntegral_apply]
  congr 1
  apply intervalIntegral.integral_congr
  intro t _
  change dualAmbient s (regularUnitary P t) v = _
  rw [dualAmbient_regular]
  rfl

#print axioms regularBundledUnitary
#print axioms regular_norm_map
#print axioms regularIntegralFamily
#print axioms regularAverage
#print axioms regularAverage_apply
#print axioms regularAverage_mem
#print axioms regularAverage_norm_le_one
#print axioms regularAverage_tendsto_identity
#print axioms regularAverage_mul_tendsto
#print axioms dualAmbient_strongIntegral_apply
#print axioms regularAverage_dual_apply
end
end TGLV350.Regular
