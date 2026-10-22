import TGLExt.LikelihoodPreparedState
import Mathlib.Topology.Algebra.Module.FiniteDimension

set_option autoImplicit false
set_option maxHeartbeats 600000
namespace ChatgptAudit.FiniteLevel
open TGLExt ChatgptAudit ChatgptAudit.Cocycle030 Matrix Set
open scoped Matrix.Norms.Operator
noncomputable section

local instance finiteLevelNormedAlgebraRat (P : SiteProfile) :
    NormedAlgebra ℚ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _

theorem finite_level_norm_closed (P : SiteProfile) (N : ℕ) :
    IsClosed (levelOperatorAlgebra P N : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) := by
  change IsClosed (Set.range (towerPiLinear P N))
  exact (LinearMap.range (towerPiLinear P N)).closed_of_finiteDimensional

theorem finite_level_exp_mem (P : SiteProfile) (N : ℕ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ levelOperatorAlgebra P N) :
    NormedSpace.exp A ∈ levelOperatorAlgebra P N := by
  rcases hA with ⟨a,rfl⟩
  exact ⟨NormedSpace.exp a,tower_pi_exp P N a⟩

theorem finite_level_exp_smul_mem (P : SiteProfile) (N : ℕ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ levelOperatorAlgebra P N) (c : ℂ) :
    NormedSpace.exp (c • A) ∈ levelOperatorAlgebra P N :=
  finite_level_exp_mem P N _ ((levelOperatorAlgebra P N).smul_mem hA c)

theorem finite_level_cocycle_mem (P : SiteProfile) (N : ℕ)
    (H V : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hH : H ∈ levelOperatorAlgebra P N) (hV : V ∈ levelOperatorAlgebra P N) (t : ℝ) :
    NormedSpace.exp (((t : ℂ)*Complex.I) • (H+V)) *
        NormedSpace.exp (((-t : ℂ)*Complex.I) • H) ∈ levelOperatorAlgebra P N :=
  (levelOperatorAlgebra P N).mul_mem
    (finite_level_exp_smul_mem P N _ ((levelOperatorAlgebra P N).add_mem hH hV) _)
    (finite_level_exp_smul_mem P N _ hH _)

theorem finite_level_mono (P : SiteProfile) {N M : ℕ} (h : N ≤ M) :
    levelOperatorAlgebra P N ≤ levelOperatorAlgebra P M := by
  rintro A ⟨a,rfl⟩
  exact ⟨tPush h a,towerPi_compat h a⟩

#print axioms finiteLevelNormedAlgebraRat
#print axioms finite_level_norm_closed
#print axioms finite_level_exp_mem
#print axioms finite_level_exp_smul_mem
#print axioms finite_level_cocycle_mem
#print axioms finite_level_mono
end
end ChatgptAudit.FiniteLevel
