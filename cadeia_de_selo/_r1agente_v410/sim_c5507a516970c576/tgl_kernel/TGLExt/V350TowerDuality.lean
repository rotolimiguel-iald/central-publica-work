import TGLExt.V350TowerCommutation
import TGLExt.V350CompressionLimit

set_option autoImplicit false
set_option maxHeartbeats 2000000
namespace TGLV350
open TGLExt ChatgptAudit Filter Topology
noncomputable section
variable {P : SiteProfile}

theorem compressed_right (N : ℕ) (x : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hx : x ∈ commutantSet (rTowerImage P)) (v : TowerHilbert P) :
    compressed P N x v = towerPi P (expectationMatrix P N x) (levelProject P N v) := by
  rw [compressed_apply, ← right_commutant_compression N x hx (levelProject_mem N v)]
  rfl

theorem compressed_left (N : ℕ) (y : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hy : y ∈ commutantSet (towerImage P)) (v : TowerHilbert P) :
    compressed P N y v = rTowerPi P (expectationMatrix P N y) (levelProject P N v) := by
  rw [compressed_apply, ← left_commutant_compression N y hy (levelProject_mem N v)]

/-- On each finite reducing level the two compressions commute exactly. -/
theorem finite_compressions_commute (N : ℕ)
    (x y : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hx : x ∈ commutantSet (rTowerImage P))
    (hy : y ∈ commutantSet (towerImage P)) :
    compressed P N x * compressed P N y = compressed P N y * compressed P N x := by
  ext v
  simp only [mul_apply_eq_comp]
  rw [compressed_right N x hx, compressed_left N y hy,
      compressed_left N y hy, compressed_right N x hx]
  rw [levelProject_fixed (right_preserves_level _ (levelProject_mem N v)),
      levelProject_fixed (left_preserves_level _ (levelProject_mem N v))]
  exact (rTowerPi_comm_towerPi P _ _ _).symm

theorem compressed_strong_limit
    (T : TowerHilbert P →L[ℂ] TowerHilbert P) (v : TowerHilbert P) :
    Tendsto (fun n => compressed P n T v) atTop (𝓝 (T v)) :=
  compression_variable_tendsto T (fun _ => v) v tendsto_const_nhds

/-- The finite commutation relations pass to the strong limit by contraction of the projections. -/
theorem tower_commutants_commute
    (x y : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hx : x ∈ commutantSet (rTowerImage P))
    (hy : y ∈ commutantSet (towerImage P)) : x * y = y * x := by
  ext v
  have hxy : Tendsto (fun n => compressed P n x (compressed P n y v))
      atTop (𝓝 (x (y v))) :=
    compression_variable_tendsto x (fun n => compressed P n y v) (y v)
      (compressed_strong_limit y v)
  have hyx : Tendsto (fun n => compressed P n y (compressed P n x v))
      atTop (𝓝 (y (x v))) :=
    compression_variable_tendsto y (fun n => compressed P n x v) (x v)
      (compressed_strong_limit x v)
  have he : (fun n => compressed P n x (compressed P n y v)) =
      (fun n => compressed P n y (compressed P n x v)) := by
    funext n
    exact congrArg (fun T : TowerHilbert P →L[ℂ] TowerHilbert P => T v)
      (finite_compressions_commute n x y hx hy)
  rw [he] at hxy
  exact tendsto_nhds_unique hxy hyx

/-- The previously reserved converse inclusion, on every product profile. -/
theorem right_commutant_subset_left_bicommutant (P : SiteProfile) :
    commutantSet (rTowerImage P) ⊆ commutantSet (commutantSet (towerImage P)) := by
  intro x hx y hy
  exact (tower_commutants_commute x y hx hy).symm

theorem tower_commutation_equality (P : SiteProfile) :
    commutantSet (rTowerImage P) = commutantSet (commutantSet (towerImage P)) :=
  Set.Subset.antisymm (right_commutant_subset_left_bicommutant P) (the_easy_half_without_J P)

#print axioms finite_compressions_commute
#print axioms tower_commutants_commute
#print axioms right_commutant_subset_left_bicommutant
#print axioms tower_commutation_equality
end
end TGLV350
