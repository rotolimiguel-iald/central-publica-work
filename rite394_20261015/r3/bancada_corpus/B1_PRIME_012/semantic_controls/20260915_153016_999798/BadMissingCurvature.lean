import TGLExt.ActionCouplingControls
set_option autoImplicit false
open TGLExt TGLExt.ActionCouplingControls
example {X : Type*} (D : ActionCouplingData X) (c : TGLCoupling) (psi : X → ℂ) (hEOM : D.EOM c psi) : D.boxOperator psi - D.mass^2 • psi = D.modularSource c psi := by
  exact hEOM
