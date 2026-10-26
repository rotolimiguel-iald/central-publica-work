import TGLExt.V350ScalarRightAverage
import Mathlib.MeasureTheory.Integral.Lebesgue.Add
import Mathlib.Analysis.SpecificLimits.Basic

set_option autoImplicit false
set_option maxHeartbeats 1400000

namespace TGLV350.Regular
open TGLExt MeasureTheory Filter
open scoped Topology ENNReal
noncomputable section

/-- The existing averages recover every square value, including infinity.
The sequence of regularized squares is not asserted to be monotone or below
the original square in operator order. -/
theorem scalarWeight_square_eq_iSup_averages (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    dualQuadraticIntegral (star A.val*A.val) (regularVacuum P) =
      ⨆ n : ℕ, dualQuadraticIntegral
        (star (A.val*regularAverage P (1/((n : ℝ)+1))) *
          (A.val*regularAverage P (1/((n : ℝ)+1)))) (regularVacuum P) := by
  let d : ℕ → ℝ := fun n => 1/((n : ℝ)+1)
  let T := fun n => A.val*regularAverage P (d n)
  let f : ℕ → ℝ → ℝ≥0∞ := fun n s => ENNReal.ofReal dualHaarFactor *
    dualQuadraticIntegrand (star (T n)*T n) (regularVacuum P) s
  let g : ℝ → ℝ≥0∞ := fun s => ENNReal.ofReal dualHaarFactor *
    dualQuadraticIntegrand (star A.val*A.val) (regularVacuum P) s
  have hd : Tendsto d atTop (𝓝[≠] (0 : ℝ)) := by
    refine tendsto_nhdsWithin_iff.mpr ⟨tendsto_one_div_add_atTop_nhds_zero_nat, ?_⟩
    exact Eventually.of_forall fun n => by
      simp only [Set.mem_compl_iff,Set.mem_singleton_iff,d]
      positivity
  have hm (n : ℕ) : Measurable (f n) :=
    measurable_const.mul (dualQuadraticIntegrand_measurable _ _)
  have hlim (s : ℝ) : Tendsto (fun n => f n s) atTop (𝓝 (g s)) := by
    have ht := ((scalarOrbit_right_average_tendsto P A s).comp hd).norm.pow 2
    have he := ENNReal.continuous_ofReal.continuousAt.tendsto.comp ht
    have hh := (ENNReal.continuous_const_mul (a := ENNReal.ofReal dualHaarFactor)
      ENNReal.ofReal_ne_top).continuousAt.tendsto.comp he
    simpa only [f,g,T,Function.comp_def,dualQuadraticIntegrand_star_mul] using hh
  have hfint (n : ℕ) : (∫⁻ s, f n s) =
      dualQuadraticIntegral (star (T n)*T n) (regularVacuum P) := by
    exact lintegral_const_mul _ (dualQuadraticIntegrand_measurable _ _)
  have hgint : (∫⁻ s, g s) =
      dualQuadraticIntegral (star A.val*A.val) (regularVacuum P) := by
    exact lintegral_const_mul _ (dualQuadraticIntegrand_measurable _ _)
  apply le_antisymm
  · calc
      _ = ∫⁻ s, g s := hgint.symm
      _ = ∫⁻ s, liminf (fun n => f n s) atTop :=
        lintegral_congr_ae (Eventually.of_forall fun s => (hlim s).liminf_eq.symm)
      _ ≤ liminf (fun n => ∫⁻ s, f n s) atTop := lintegral_liminf_le hm
      _ ≤ _ := liminf_le_of_frequently_le'
        (Eventually.of_forall (fun n => by
          rw [hfint]
          exact le_iSup_of_le n le_rfl)).frequently
  · exact iSup_le fun n => scalarWeight_right_average_le P A (d n)

end
end TGLV350.Regular
