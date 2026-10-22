import IndependentA2Controls
set_option autoImplicit false
open TGLExt TGLV350.Regular TGLV351 TGL.ContinuousCorner IndependentA2
example (P : SiteProfile) : ∀ a b : (regularCoreAlgebra P).toStarSubalgebra, positiveTraceReader P (a*b) = positiveTraceReader P (b*a) := by
  exact positiveTraceReader_positive P
