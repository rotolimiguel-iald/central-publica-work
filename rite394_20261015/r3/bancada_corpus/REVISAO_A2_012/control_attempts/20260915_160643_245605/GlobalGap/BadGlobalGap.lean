import IndependentA2Controls
set_option autoImplicit false
open TGLExt TGLV350.Regular TGLV351 TGL.ContinuousCorner IndependentA2
example (P : SiteProfile) : ∀ x : RegularHilbert (TowerHilbert P), ‖regularMinimalLock P x‖ = ‖x‖ := by
  intro x
  exact regularMinimalLock_relative_gap P x
