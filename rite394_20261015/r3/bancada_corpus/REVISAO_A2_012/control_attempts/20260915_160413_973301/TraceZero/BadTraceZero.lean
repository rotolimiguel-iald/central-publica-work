import IndependentA2Controls
set_option autoImplicit false
open TGLExt TGLV350.Regular TGLV351 TGL.ContinuousCorner IndependentA2
example (P : SiteProfile) : scalarInverseLimitWeight P (regularFiniteSupport P) = 0 := by
  exact trace_positive P
