import TGLExt.V350ScalarRightAverage
import TGLExt.V350ScalarGNSCompletion
import Mathlib.MeasureTheory.Integral.DominatedConvergence

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory Filter
open scoped Topology ENNReal
noncomputable section

/-- The original uniformly finite ideal approximates every n_ν vector in the
actual scalar GNS norm, not just in the strong operator topology. -/
theorem scalarWeightOrbit_rightRegularization_tendsto (P : SiteProfile)
    (A : scalarWeightLeftIdeal P) :
    Tendsto (fun h : ℝ => scalarWeightOrbit P (scalarWeightRightRegularization P A h))
      (𝓝[≠] 0) (𝓝 (scalarWeightOrbit P A)) := by
  let f := fun s : ℝ => dualAmbient s A.val.val (regularVacuum P)
  let g := fun h s : ℝ => dualAmbient s (A.val.val * regularAverage P h) (regularVacuum P)
  have hm := scalarWeightOrbit_memLp P A.val.val A.property
  have hb (h s : ℝ) : ‖g h s - f s‖ ^ 2 ≤ 4 * ‖f s‖ ^ 2 := by
    have hnorm : ‖g h s‖ ≤ ‖f s‖ := scalarOrbit_right_average_norm_le P A.val s h
    have hd : ‖g h s - f s‖ ≤ 2 * ‖f s‖ :=
      (norm_sub_le _ _).trans (by linarith)
    calc
      _ ≤ (2 * ‖f s‖)^2 := pow_le_pow_left₀ (norm_nonneg _) hd 2
      _ = _ := by ring
  have hI : Tendsto (fun h : ℝ => ∫ s : ℝ, ‖g h s-f s‖ ^ 2)
      (𝓝[≠] 0) (𝓝 (∫ _s : ℝ, (0 : ℝ))) := by
    apply tendsto_integral_filter_of_dominated_convergence (fun s : ℝ => 4 * ‖f s‖ ^ 2)
    · exact Eventually.of_forall fun h =>
        (((dualAmbient_strongly_continuous (A.val.val * regularAverage P h) (regularVacuum P)).sub
          (dualAmbient_strongly_continuous A.val.val (regularVacuum P))).norm.pow 2).aestronglyMeasurable
    · exact Eventually.of_forall fun h => Eventually.of_forall fun s => by
        simpa only [Real.norm_eq_abs,abs_of_nonneg (sq_nonneg (‖g h s-f s‖))] using hb h s
    · exact ((memLp_two_iff_integrable_sq_norm hm.1).mp hm).const_mul 4
    · exact Eventually.of_forall fun s => by
        have ht := ((scalarOrbit_right_average_tendsto P A.val s).sub
          (tendsto_const_nhds (x := f s))).norm.pow 2
        simpa only [f,g,sub_self,norm_zero,zero_pow (by norm_num : (2 : ℕ) ≠ 0)] using ht
  have he (h : ℝ) :
      ‖scalarWeightOrbit P (scalarWeightRightRegularization P A h)-scalarWeightOrbit P A‖^2 =
        dualHaarFactor * ∫ s : ℝ, ‖g h s-f s‖^2 := by
    change ‖scalarWeightLinear P (scalarWeightRightRegularization P A h)-scalarWeightLinear P A‖^2 = _
    rw [← map_sub]
    change ‖scalarWeightOrbit P (scalarWeightRightRegularization P A h-A)‖^2 = _
    rw [scalarWeightOrbit_norm_sq_real]
    congr 1
    apply integral_congr_ae
    exact Eventually.of_forall fun s => by
      change ‖dualAmbient s (A.val.val * regularAverage P h-A.val.val) (regularVacuum P)‖^2 = _
      rw [map_sub]
      rfl
  have hs : Tendsto (fun h : ℝ =>
      ‖scalarWeightOrbit P (scalarWeightRightRegularization P A h)-scalarWeightOrbit P A‖^2)
      (𝓝[≠] 0) (𝓝 (0 : ℝ)) := by
    simpa only [he,integral_zero,mul_zero] using hI.const_mul dualHaarFactor
  have hn := Real.continuous_sqrt.continuousAt.tendsto.comp hs
  apply tendsto_iff_dist_tendsto_zero.mpr
  simpa only [Function.comp_def,Real.sqrt_sq_eq_abs,abs_norm,Real.sqrt_zero,dist_eq_norm] using hn

theorem scalarWeightOrbit_mem_original_GNS (P : SiteProfile) (A : scalarWeightLeftIdeal P) :
    scalarWeightOrbit P A ∈ scalarGNSSubspace P := by
  change scalarWeightOrbit P A ∈ closure (Set.range (scalarGNSLinear P))
  have ht : Tendsto (fun h : ℝ => scalarWeightOrbit P (scalarWeightRightRegularization P A h))
      (𝓝[>] (0 : ℝ)) (𝓝 (scalarWeightOrbit P A)) :=
    (scalarWeightOrbit_rightRegularization_tendsto P A).mono_left
      (nhdsWithin_mono (0 : ℝ) (by intro h hh; exact ne_of_gt hh))
  apply isClosed_closure.mem_of_tendsto ht
  filter_upwards [self_mem_nhdsWithin] with h hh
  let a : finiteDualLeftIdeal P := ⟨(scalarWeightRightRegularization P A h).val,
    scalarWeightRightRegularization_uniform P A h hh⟩
  apply subset_closure
  refine ⟨a,?_⟩
  exact (scalarWeightOrbit_uniform P a).symm

theorem scalarWeight_completion_eq (P : SiteProfile) :
    (scalarWeightLinear P).range.topologicalClosure = scalarGNSSubspace P := by
  apply le_antisymm
  · apply Submodule.topologicalClosure_minimal
    · rintro _ ⟨A,rfl⟩
      exact scalarWeightOrbit_mem_original_GNS P A
    · exact Submodule.isClosed_topologicalClosure _
  · apply Submodule.topologicalClosure_mono
    rintro _ ⟨A,rfl⟩
    exact ⟨Submodule.inclusion (finiteDualLeftIdeal_le_scalarWeight P) A,scalarWeightOrbit_uniform P A⟩

def scalarWeightGNSEmbedding (P : SiteProfile) : scalarWeightLeftIdeal P →ₗ[ℂ] ScalarGNSHilbert P :=
  (scalarWeightLinear P).codRestrict (scalarGNSSubspace P) (scalarWeightOrbit_mem_original_GNS P)

theorem scalarWeightGNSEmbedding_uniform (P : SiteProfile) (A : finiteDualLeftIdeal P) :
    scalarWeightGNSEmbedding P (Submodule.inclusion (finiteDualLeftIdeal_le_scalarWeight P) A) =
      scalarGNSEmbedding P A := Subtype.ext (scalarWeightOrbit_uniform P A)

#print axioms scalarWeightOrbit_rightRegularization_tendsto
#print axioms scalarWeightOrbit_mem_original_GNS
#print axioms scalarWeight_completion_eq
#print axioms scalarWeightGNSEmbedding
#print axioms scalarWeightGNSEmbedding_uniform
end
end TGLV350.Regular
