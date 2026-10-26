import TGLExt.LocalTowerProjections

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace TGLV350
open TGLExt ChatgptAudit Filter Topology
noncomputable section
variable {P : SiteProfile}

/-- Orthogonal compression preserves limits even when the input vector varies. -/
theorem project_variable_tendsto (v : ℕ → TowerHilbert P) (z : TowerHilbert P)
    (hv : Tendsto v atTop (𝓝 z)) :
    Tendsto (fun n => levelProject P n (v n)) atTop (𝓝 z) := by
  rw [Metric.tendsto_nhds] at hv ⊢
  intro ε hε
  have hz := Metric.tendsto_nhds.mp (levelProject_tendsto z) (ε / 2) (half_pos hε)
  filter_upwards [hv (ε / 2) (half_pos hε), hz] with n hn hnz
  have hcon : dist (levelProject P n (v n)) (levelProject P n z) ≤ dist (v n) z := by
    rw [dist_eq_norm, dist_eq_norm, ← map_sub]
    exact (levelSpace P n).norm_starProjection_apply_le (v n - z)
  have htri := dist_triangle (levelProject P n (v n)) (levelProject P n z) z
  linarith

/-- Nested compressions and a fixed bounded operator converge strongly. -/
theorem compression_variable_tendsto
    (T : TowerHilbert P →L[ℂ] TowerHilbert P)
    (v : ℕ → TowerHilbert P) (z : TowerHilbert P)
    (hv : Tendsto v atTop (𝓝 z)) :
    Tendsto (fun n => levelProject P n (T (levelProject P n (v n))))
      atTop (𝓝 (T z)) := by
  apply project_variable_tendsto
  exact (T.continuous.tendsto z).comp (project_variable_tendsto v z hv)

#print axioms project_variable_tendsto
#print axioms compression_variable_tendsto
end
end TGLV350
