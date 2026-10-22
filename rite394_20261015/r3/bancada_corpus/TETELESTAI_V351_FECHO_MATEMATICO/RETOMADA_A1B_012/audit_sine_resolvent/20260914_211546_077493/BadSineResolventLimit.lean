import TGLExt.V351SineResolventApprox
open TGLExt TGLV350.Regular Filter
open scoped Topology
example (P : SiteProfile) (u : RegularHilbert (TowerHilbert P)) :
    Tendsto (fun n : ℕ => regularSineResolvent P ((n : ℝ)+1) u) atTop
      (𝓝 ((1-regularSpectralResolvent P) u)) := by
  exact regularSineResolvent_tendsto P u
