import TGLExt.V350ScalarWeightAction
import TGLExt.V350ScalarGNSStrongContinuity
import TGLExt.V350FiniteDualStarCore

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory Filter
open scoped Topology ENNReal
noncomputable section

def scalarWeightSandwich (P : SiteProfile) (A : scalarWeightLeftIdeal P) (h : ℝ) :
    scalarWeightLeftIdeal P :=
  scalarWeightLeftProduct P
    ⟨star (regularAverage P h),
      (regularCoreAlgebra P).toStarSubalgebra.star_mem' (regularAverage_mem P h)⟩
    (scalarWeightRightRegularization P A h)

theorem scalarWeightSandwich_val (P : SiteProfile) (A : scalarWeightLeftIdeal P) (h : ℝ) :
    (scalarWeightSandwich P A h).val = regularSandwich P A.val h := by
  apply Subtype.ext
  exact (mul_assoc _ _ _).symm

/-- The sandwich converges in the actual scalar GNS norm. The adjoint limit
uses the established contraction lemma, not continuity of star in SOT. -/
theorem scalarWeightGNSEmbedding_sandwich_tendsto (P : SiteProfile)
    (A : scalarWeightLeftIdeal P) :
    Tendsto (fun h : ℝ => scalarWeightGNSEmbedding P (scalarWeightSandwich P A h))
      (𝓝[≠] 0) (𝓝 (scalarWeightGNSEmbedding P A)) := by
  let T : ℝ → (regularCoreAlgebra P).toStarSubalgebra := fun h =>
    ⟨star (regularAverage P h),
      (regularCoreAlgebra P).toStarSubalgebra.star_mem' (regularAverage_mem P h)⟩
  have hb (h : ℝ) : ‖(T h).val‖ ≤ (1 : ℝ) := by
    simpa only [T,_root_.norm_star] using regularAverage_norm_le_one P h
  have hv : Tendsto (fun h : ℝ =>
      scalarWeightGNSEmbedding P (scalarWeightRightRegularization P A h))
      (𝓝[≠] 0) (𝓝 (scalarWeightGNSEmbedding P A)) :=
    tendsto_subtype_rng.mpr (scalarWeightOrbit_rightRegularization_tendsto P A)
  have hf : Tendsto (fun h : ℝ => scalarGNSRepresentation P (T h)
      (scalarWeightGNSEmbedding P A)) (𝓝[≠] 0) (𝓝 (scalarWeightGNSEmbedding P A)) := by
    have ht := scalarGNSRepresentation_tendsto_of_uniformly_bounded P T 1 1 hb
      (regularAverage_star_tendsto_identity P) (scalarWeightGNSEmbedding P A)
    simpa only [map_one,ContinuousLinearMap.one_apply] using ht
  have hu (h : ℝ) : ‖scalarGNSRepresentation P (T h)‖ ≤ (1 : ℝ) :=
    (scalarGNSAction_norm_le P (T h)).trans (hb h)
  have ht := bounded_application_tendsto (𝓝[≠] (0 : ℝ))
    (fun h => scalarGNSRepresentation P (T h)) 1 hu
    (fun h => scalarWeightGNSEmbedding P (scalarWeightRightRegularization P A h))
    (scalarWeightGNSEmbedding P A) (scalarWeightGNSEmbedding P A) hv hf
  simpa only [scalarWeightGNSAction_intertwines,scalarWeightSandwich,T] using ht

#print axioms scalarWeightSandwich
#print axioms scalarWeightSandwich_val
#print axioms scalarWeightGNSEmbedding_sandwich_tendsto
end
end TGLV350.Regular
