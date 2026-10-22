import IndependentSubstitution
set_option autoImplicit false
open TGLExt IndependentB1Prime

example (c : TGLCoupling) (xi b : ℝ) (h : b ≠ c.beta) :
    (fixedData c xi).fieldOperator probe = b • (fixedData c xi).K_boundary probe := by
  exact beta_positive c xi
