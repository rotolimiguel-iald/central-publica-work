import TGLExt.ActionCouplingControls
set_option autoImplicit false
open TGLExt TGLExt.ActionCouplingControls
example (c : TGLCoupling) (xi : ℝ) : (scalarModel xi (-c.beta)).EOM c unitSection := by
  exact scalar_model_eom c xi
