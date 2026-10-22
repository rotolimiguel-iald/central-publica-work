import IndependentA2Controls
set_option autoImplicit false
open TGLExt TGLV350.Regular TGLV351 TGL.ContinuousCorner IndependentA2
example (P : SiteProfile) : 0 < scalarInverseLimitWeight P (PositiveCoreInput.zero P) := by
  exact (support_trace_positive_finite P).1
