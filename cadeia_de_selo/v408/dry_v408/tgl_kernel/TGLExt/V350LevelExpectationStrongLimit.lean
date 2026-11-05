import TGLExt.V350LevelExpectationUniformBound
import TGLExt.V350ScalarGNSStrongContinuity
import TGLExt.ExpectationContinuity

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit Filter
open scoped Topology
noncomputable section

/-- The existing finite-level expectations approximate every factor operator
strongly, with the same uniform bound at every level. -/
theorem levelExpectation_strong_tendsto (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P)
    (v : TowerHilbert P) :
    Tendsto (fun N => towerExpectation P N A v) atTop (𝓝 (A v)) := by
  apply ChatgptAudit.Expectation047.bounded_omega_tendsto P atTop
    (fun N => towerExpectation P N A) A (4 * ‖A‖) (by positivity)
    (fun N => expectation_mem_factor N A) hA
    (fun N => levelExpectation_uniform_norm_bound P N A hA)
  simpa only [expectation_omega] using levelProject_tendsto (A (hOmega P))

def levelCoreApproximation (P : SiteProfile) (N : ℕ)
    (A : (theFactorObject P).toStarSubalgebra) : (regularCoreAlgebra P).toStarSubalgebra :=
  regularCoreEmbedding P ⟨towerExpectation P N A.val, expectation_mem_factor N A.val⟩

theorem levelCoreApproximation_uniform_bound (P : SiteProfile) (N : ℕ)
    (A : (theFactorObject P).toStarSubalgebra) :
    ‖(levelCoreApproximation P N A).val‖ ≤ 4 * ‖A.val‖ :=
  (fibre_norm_le _).trans (levelExpectation_uniform_norm_bound P N A.val A.property)

theorem levelCoreApproximation_strong_tendsto (P : SiteProfile)
    (A : (theFactorObject P).toStarSubalgebra) (v : RegularHilbert (TowerHilbert P)) :
    Tendsto (fun N => (levelCoreApproximation P N A).val v) atTop
      (𝓝 ((regularCoreEmbedding P A).val v)) :=
  fibre_tendsto_of_uniformly_bounded (fun N => towerExpectation P N A.val) A.val
    (4 * ‖A.val‖) (fun N => levelExpectation_uniform_norm_bound P N A.val A.property)
      (levelExpectation_strong_tendsto P A.val A.property) v

/-- This limit is in the same completed scalar GNS representation as S, B and J. -/
theorem represented_levelExpectation_strong_tendsto (P : SiteProfile)
    (A : (theFactorObject P).toStarSubalgebra) (v : ScalarGNSHilbert P) :
    Tendsto (fun N => scalarGNSRepresentation P (levelCoreApproximation P N A) v) atTop
      (𝓝 (scalarGNSRepresentation P (regularCoreEmbedding P A) v)) :=
  scalarGNSRepresentation_tendsto_of_uniformly_bounded P
    (fun N => levelCoreApproximation P N A) (regularCoreEmbedding P A) (4 * ‖A.val‖)
    (fun N => levelCoreApproximation_uniform_bound P N A)
    (levelCoreApproximation_strong_tendsto P A) v

#print axioms levelExpectation_strong_tendsto
#print axioms levelCoreApproximation
#print axioms levelCoreApproximation_uniform_bound
#print axioms levelCoreApproximation_strong_tendsto
#print axioms represented_levelExpectation_strong_tendsto
end
end TGLV350.Regular
