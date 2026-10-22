import IndependentA2Controls
set_option autoImplicit false
open TGLExt TGLV350.Regular TGLV351 TGL.ContinuousCorner IndependentA2
example (P : SiteProfile) : (regularContinuousCorner P).normalizedTrace (regularContinuousCorner P).Pplus = 1 := by
  exact plus_half P
