import TGLExt.ActionCouplingControls
set_option autoImplicit false
open TGLExt TGLExt.ActionCouplingControls
example (c : TGLCoupling) (xi : ℝ) : (scalarModel xi c.beta).xi = (1/6 : ℝ) := by
  exact (nonzero_model_for_every_xi c xi).1
