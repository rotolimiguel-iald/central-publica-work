import TGLExt.V350ScalarGNSCompletion
import TGLExt.V350DualOrbitStrongLimits
import TGLExt.V350FiniteDualStarCore

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory Filter
open scoped Topology
noncomputable section

/-- Left regularization suffices on the finite ideal itself. -/
def scalarGNSLeftRegularization (P : SiteProfile) (A : finiteDualLeftIdeal P) (h : ℝ) :
    finiteDualLeftIdeal P :=
  scalarGNSLeftProduct P
    ⟨star (regularAverage P h),
      (regularCoreAlgebra P).toStarSubalgebra.star_mem' (regularAverage_mem P h)⟩ A

theorem scalarGNSLeftRegularization_mem_starCore (P : SiteProfile)
    (A : finiteDualLeftIdeal P) (h : ℝ) (hh : 0 < h) :
    (scalarGNSLeftRegularization P A h).val ∈ finiteDualStarCore P := by
  refine ⟨(scalarGNSLeftRegularization P A h).property, ?_⟩
  change HasFiniteDualSquare (star (star (regularAverage P h) * A.val.val))
  rw [star_mul,star_star]
  exact HasFiniteDualSquare.left_mul _ _ (regularAverage_hasFiniteDualSquare P h hh)

theorem scalarGNSOrbit_leftRegularization_tendsto (P : SiteProfile)
    (A : finiteDualLeftIdeal P) :
    Tendsto (fun h : ℝ => scalarGNSOrbit P (scalarGNSLeftRegularization P A h))
      (𝓝[>] 0) (𝓝 (scalarGNSOrbit P A)) := by
  have hb : ∀ h : ℝ, ‖star (regularAverage P h)‖ ≤ 1 := by
    intro h
    exact (_root_.norm_star (regularAverage P h)).le.trans (regularAverage_norm_le_one P h)
  have hs : ∀ v, Tendsto (fun h : ℝ => star (regularAverage P h) v)
      (𝓝[>] 0) (𝓝 ((1 : RegularHilbert (TowerHilbert P) →L[ℂ] _) v)) := by
    intro v
    exact (regularAverage_star_tendsto_identity P v).mono_left
      (nhdsWithin_mono _ (by intro h hh; exact ne_of_gt hh))
  have ht := dualOrbit_tendsto_of_uniformly_bounded
    (fun h : ℝ => star (regularAverage P h)) 1 1 hb hs (scalarGNSOrbit P A)
  rw [map_one] at ht
  have he : (fun h : ℝ => scalarGNSOrbit P (scalarGNSLeftRegularization P A h)) =
      (fun h : ℝ => dualOrbitRepresentation (star (regularAverage P h)) (scalarGNSOrbit P A)) := by
    funext h
    exact (scalarGNSAmbientAction_intertwines P
      ⟨star (regularAverage P h),
        (regularCoreAlgebra P).toStarSubalgebra.star_mem' (regularAverage_mem P h)⟩ A).symm
  rw [he]
  exact ht

#print axioms scalarGNSLeftRegularization
#print axioms scalarGNSLeftRegularization_mem_starCore
#print axioms scalarGNSOrbit_leftRegularization_tendsto
end
end TGLV350.Regular
