import Mathlib.Analysis.Calculus.ParametricIntegral
import Mathlib.Tactic

/-! Differentiation under a Bochner integral along a closed parameter set.
This is the within-set counterpart of the mathlib dominated Lipschitz lemma;
all integrability, derivative, and domination hypotheses remain explicit. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory Filter
open scoped Topology
namespace F1Fecho.DominatedWithin

variable {X : Type*} [MeasurableSpace X] (μ : Measure X)
  {F : ℂ → X → ℂ} {D : X → ℂ} {B : X → ℝ} {s : Set ℂ} {z : ℂ}

theorem integral_hasDerivWithinAt
    (hF : ∀ w ∈ s, Integrable (F w) μ) (hz : z ∈ s)
    (hD : Integrable D μ) (hB : Integrable B μ)
    (hBn : ∀ᵐ x ∂μ, 0 ≤ B x)
    (hLip : ∀ᵐ x ∂μ, ∀ w ∈ s, ‖F w x-F z x‖ ≤ B x*‖w-z‖)
    (hd : ∀ᵐ x ∂μ, HasDerivWithinAt (fun w => F w x) (D x) s z) :
    HasDerivWithinAt (fun w => ∫ x, F w x ∂μ) (∫ x, D x ∂μ) s z := by
  let rem : ℂ → X → ℂ := fun w x => ‖w-z‖⁻¹ • (F w x-F z x-(w-z) • D x)
  have hrep : ∀ᶠ w in 𝓝[s] z,
      ‖w-z‖⁻¹*‖(∫ x,F w x ∂μ)-(∫ x,F z x ∂μ)-(w-z) • (∫ x,D x ∂μ)‖ =
        ‖∫ x,rem w x ∂μ‖ := by
    filter_upwards [self_mem_nhdsWithin] with w hw
    dsimp only [rem]
    rw [integral_smul,integral_sub,integral_sub,integral_smul,
      norm_smul_of_nonneg (inv_nonneg.mpr (norm_nonneg _))]
    exacts [hF w hw,hF z hz,(hF w hw).sub (hF z hz),hD.const_mul (w-z)]
  rw [hasDerivWithinAt_iff_tendsto,tendsto_congr' hrep,
    ←tendsto_zero_iff_norm_tendsto_zero]
  have hi : Tendsto (fun w => ∫ x, rem w x ∂μ) (𝓝[s] z) (𝓝 (∫ x, (0:ℂ) ∂μ)) := by
    apply tendsto_integral_filter_of_dominated_convergence (bound := fun x => B x+‖D x‖)
    · filter_upwards [self_mem_nhdsWithin] with w hw
      exact (((hF w hw).aestronglyMeasurable.sub (hF z hz).aestronglyMeasurable).sub
        (hD.aestronglyMeasurable.const_smul (w-z))).const_smul ‖w-z‖⁻¹
    · filter_upwards [self_mem_nhdsWithin] with w hw
      filter_upwards [hLip,hBn] with x hl hb
      dsimp only [rem]
      rw [norm_smul_of_nonneg (inv_nonneg.mpr (norm_nonneg _))]
      calc
        ‖w-z‖⁻¹*‖F w x-F z x-(w-z) • D x‖ ≤
            ‖w-z‖⁻¹*(‖F w x-F z x‖+‖(w-z) • D x‖) := by gcongr; exact norm_sub_le _ _
        _ ≤ ‖w-z‖⁻¹*(B x*‖w-z‖+‖w-z‖*‖D x‖) := by rw [norm_smul]; gcongr; exact hl w hw
        _ ≤ B x+‖D x‖ := by
          by_cases he : w=z
          · simp [he]; positivity
          · have hn : ‖w-z‖≠0 := norm_ne_zero_iff.mpr (sub_ne_zero.mpr he)
            field_simp
            ring_nf
            exact le_rfl
    · exact hB.add hD.norm
    · filter_upwards [hd] with x hx
      rw [tendsto_zero_iff_norm_tendsto_zero]
      simpa only [rem,norm_smul_of_nonneg (inv_nonneg.mpr (norm_nonneg _))] using
        hasDerivWithinAt_iff_tendsto.mp hx
  simpa only [integral_zero] using hi

end F1Fecho.DominatedWithin
#print axioms F1Fecho.DominatedWithin.integral_hasDerivWithinAt
