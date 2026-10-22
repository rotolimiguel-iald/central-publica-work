import TGLExt.ActionCouplingControls
set_option autoImplicit false
open TGLExt TGLExt.ActionCouplingControls
example {X : Type*} (D : ActionCouplingData X) (c : TGLCoupling) (psi : X → ℂ) (hEOM : D.EOM c psi) (b : ℝ) : D.fieldOperator psi = b • D.K_boundary psi := by
  exact hEOM
