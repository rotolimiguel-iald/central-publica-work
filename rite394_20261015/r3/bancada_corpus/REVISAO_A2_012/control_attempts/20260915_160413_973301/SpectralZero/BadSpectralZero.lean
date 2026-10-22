import IndependentA2Controls
set_option autoImplicit false
open TGLExt TGLV350.Regular TGLV351 TGL.ContinuousCorner IndependentA2
example (P : SiteProfile) : (regularMinimalLock P).ker.starProjection = 0 := by
  exact spectral_positive P
