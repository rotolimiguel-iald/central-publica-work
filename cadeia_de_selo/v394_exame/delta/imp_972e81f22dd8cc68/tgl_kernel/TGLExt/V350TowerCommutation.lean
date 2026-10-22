import TGLExt.ExpectationBimodule
import TGLExt.TheDebtWithoutJ
import TGLExt.TheNameAndItsReferent
import TGLExt.TheConditionalCertificate

set_option autoImplicit false
set_option maxHeartbeats 2000000

namespace TGLV350
open TGLExt ChatgptAudit Filter Topology
noncomputable section
variable {P : SiteProfile}

/-- Finite compression only needs commutation with the right action. -/
theorem right_commutant_compression (N : ℕ)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hx : x ∈ commutantSet (rTowerImage P))
    {v : TowerHilbert P} (hv : v ∈ levelSpace P N) :
    towerExpectation P N x v = levelProject P N (x v) := by
  obtain ⟨b, rfl⟩ := hv
  change towerExpectation P N x ((tof P N b : TowerPre P) : TowerHilbert P) =
    levelProject P N (x ((tof P N b : TowerPre P) : TowerHilbert P))
  have hc (w : TowerHilbert P) : x (rTowerPi P b w) = rTowerPi P b (x w) := by
    exact (congrArg (fun T : TowerHilbert P →L[ℂ] TowerHilbert P => T w)
      (hx (rTowerPi P b) ⟨N, b, rfl⟩)).symm
  rw [← rTowerPi_omega, factor_right_apply (expectation_mem_factor _ _),
    hc, project_right, expectation_omega]

/-- The analogous finite compression of a left-commuting operator is right multiplication. -/
theorem left_commutant_compression (N : ℕ)
    (y : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hy : y ∈ commutantSet (towerImage P))
    {v : TowerHilbert P} (hv : v ∈ levelSpace P N) :
    rTowerPi P (expectationMatrix P N y) v = levelProject P N (y v) := by
  obtain ⟨b, rfl⟩ := hv
  change rTowerPi P (expectationMatrix P N y)
      ((tof P N b : TowerPre P) : TowerHilbert P) =
    levelProject P N (y ((tof P N b : TowerPre P) : TowerHilbert P))
  have hc (w : TowerHilbert P) : y (towerPi P b w) = towerPi P b (y w) := by
    exact (congrArg (fun T : TowerHilbert P →L[ℂ] TowerHilbert P => T w)
      (hy (towerPi P b) ⟨N, b, rfl⟩)).symm
  rw [← towerPi_omega, rTowerPi_comm_towerPi, hc, project_left, rTowerPi_omega]
  congr 1
  exact levelDecode_embedding N _

def compressed (P : SiteProfile) (N : ℕ)
    (T : TowerHilbert P →L[ℂ] TowerHilbert P) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  levelProject P N * T * levelProject P N

theorem compressed_apply (N : ℕ)
    (T : TowerHilbert P →L[ℂ] TowerHilbert P) (v : TowerHilbert P) :
    compressed P N T v = levelProject P N (T (levelProject P N v)) := rfl

#print axioms right_commutant_compression
#print axioms left_commutant_compression
end
end TGLV350
