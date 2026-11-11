import TGLExt.F1Fecho394.CanonicalFockRightAverageR3
import TGLExt.F1Fecho394.CanonicalFockWeightOrbitR3
import TGLExt.F1Fecho394.CanonicalFockGNSR5
import Mathlib.MeasureTheory.Integral.DominatedConvergence

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000
set_option synthInstance.maxHeartbeats 1000000

namespace F1Fecho.CanonicalFockWeightCompletion
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockFiniteWeight F1Fecho.CanonicalFockWeightDomain F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockWeightOrbit F1Fecho.CanonicalFockRightAverage
open scoped Topology ENNReal
noncomputable section

/-- The original uniformly finite ideal approximates every n_ν vector in the
actual scalar GNS norm, not just in the strong operator topology. -/
theorem scalarWeightOrbit_rightRegularization_tendsto 
    (A : scalarWeightLeftIdeal ) :
    Tendsto (fun h : ℝ => F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit (scalarWeightRightRegularization A h))
      (𝓝[≠] 0) (𝓝 (F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit A)) := by
  let f := fun s : ℝ => dualAmbient s A.val.val regularFockVacuum
  let g := fun h s : ℝ => dualAmbient s (A.val.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h) regularFockVacuum
  have hm := scalarWeightOrbit_memLp A.val.val A.property
  have hb (h s : ℝ) : ‖g h s - f s‖ ^ 2 ≤ 4 * ‖f s‖ ^ 2 := by
    have hnorm : ‖g h s‖ ≤ ‖f s‖ := scalarOrbit_right_average_norm_le A.val s h
    have hd : ‖g h s - f s‖ ≤ 2 * ‖f s‖ :=
      (norm_sub_le _ _).trans (by linarith)
    calc
      _ ≤ (2 * ‖f s‖)^2 := pow_le_pow_left₀ (norm_nonneg _) hd 2
      _ = _ := by ring
  have hI : Tendsto (fun h : ℝ => ∫ s : ℝ, ‖g h s-f s‖ ^ 2)
      (𝓝[≠] 0) (𝓝 (∫ _s : ℝ, (0 : ℝ))) := by
    apply tendsto_integral_filter_of_dominated_convergence (fun s : ℝ => 4 * ‖f s‖ ^ 2)
    · exact Eventually.of_forall fun h =>
        (((dualAmbient_strongly_continuous (A.val.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h) regularFockVacuum).sub
          (dualAmbient_strongly_continuous A.val.val regularFockVacuum)).norm.pow 2).aestronglyMeasurable
    · exact Eventually.of_forall fun h => Eventually.of_forall fun s => by
        simpa only [Real.norm_eq_abs,abs_of_nonneg (sq_nonneg (‖g h s-f s‖))] using hb h s
    · exact ((memLp_two_iff_integrable_sq_norm hm.1).mp hm).const_mul 4
    · exact Eventually.of_forall fun s => by
        have ht := ((scalarOrbit_right_average_tendsto A.val s).sub
          (tendsto_const_nhds (x := f s))).norm.pow 2
        simpa only [f,g,sub_self,norm_zero,zero_pow (by norm_num : (2 : ℕ) ≠ 0)] using ht
  have he (h : ℝ) :
      ‖F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit (scalarWeightRightRegularization A h)-F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit A‖^2 =
        dualHaarFactor * ∫ s : ℝ, ‖g h s-f s‖^2 := by
    change ‖F1Fecho.CanonicalFockWeightOrbit.scalarWeightLinear (scalarWeightRightRegularization A h)-F1Fecho.CanonicalFockWeightOrbit.scalarWeightLinear A‖^2 = _
    rw [← map_sub]
    change ‖F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit (scalarWeightRightRegularization A h-A)‖^2 = _
    rw [F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit_norm_sq_real]
    congr 1
    apply integral_congr_ae
    exact Eventually.of_forall fun s => by
      change ‖dualAmbient s (A.val.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h-A.val.val) regularFockVacuum‖^2 = _
      rw [map_sub]
      rfl
  have hs : Tendsto (fun h : ℝ =>
      ‖F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit (scalarWeightRightRegularization A h)-F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit A‖^2)
      (𝓝[≠] 0) (𝓝 (0 : ℝ)) := by
    simpa only [he,integral_zero,mul_zero] using hI.const_mul dualHaarFactor
  have hn := Real.continuous_sqrt.continuousAt.tendsto.comp hs
  apply tendsto_iff_dist_tendsto_zero.mpr
  simpa only [Function.comp_def,Real.sqrt_sq_eq_abs,abs_norm,Real.sqrt_zero,dist_eq_norm] using hn

theorem scalarWeightOrbit_mem_original_GNS  (A : scalarWeightLeftIdeal ) :
    F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit A ∈ GNSSubspace := by
  change F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit A ∈ closure (Set.range (scalarGNSLinear ))
  have ht : Tendsto (fun h : ℝ => F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit (scalarWeightRightRegularization A h))
      (𝓝[>] (0 : ℝ)) (𝓝 (F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit A)) :=
    (scalarWeightOrbit_rightRegularization_tendsto A).mono_left
      (nhdsWithin_mono (0 : ℝ) (by intro h hh; exact ne_of_gt hh))
  apply isClosed_closure.mem_of_tendsto ht
  filter_upwards [self_mem_nhdsWithin] with h hh
  let a : finiteLeftIdeal := ⟨(scalarWeightRightRegularization A h).val,
    scalarWeightRightRegularization_uniform A h hh⟩
  apply subset_closure
  refine ⟨a,?_⟩
  exact (F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit_uniform a).symm

theorem scalarWeight_completion_eq  :
    (F1Fecho.CanonicalFockWeightOrbit.scalarWeightLinear ).range.topologicalClosure = GNSSubspace := by
  apply le_antisymm
  · apply Submodule.topologicalClosure_minimal
    · rintro _ ⟨A,rfl⟩
      exact scalarWeightOrbit_mem_original_GNS A
    · exact Submodule.isClosed_topologicalClosure _
  · apply Submodule.topologicalClosure_mono
    rintro _ ⟨A,rfl⟩
    exact ⟨Submodule.inclusion (finiteDualLeftIdeal_le_scalarWeight ) A,F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit_uniform A⟩

def scalarWeightGNSEmbedding  : scalarWeightLeftIdeal →ₗ[ℂ] GNSHilbert :=
  (F1Fecho.CanonicalFockWeightOrbit.scalarWeightLinear ).codRestrict (GNSSubspace) (scalarWeightOrbit_mem_original_GNS )

theorem scalarWeightGNSEmbedding_uniform  (A : finiteLeftIdeal) :
    scalarWeightGNSEmbedding (Submodule.inclusion (finiteDualLeftIdeal_le_scalarWeight ) A) =
      GNSEmbedding A := Subtype.ext (F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit_uniform A)

end
end F1Fecho.CanonicalFockWeightCompletion
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.CanonicalFockWeightCompletion).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
