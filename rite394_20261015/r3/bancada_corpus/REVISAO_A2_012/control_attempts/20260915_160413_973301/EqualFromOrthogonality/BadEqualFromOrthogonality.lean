import IndependentA2Controls
set_option autoImplicit false
open TGLExt TGLV350.Regular TGLV351 TGL.ContinuousCorner IndependentA2
example : unequalWeight leftFace = unequalWeight rightFace := by
  exact (show (1 : ℝ) = 1 from rfl)
