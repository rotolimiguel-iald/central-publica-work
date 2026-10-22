import TGLExt.ActionCouplingControls
set_option autoImplicit false
open TGLExt TGLExt.ActionCouplingControls
example {X : Type*} (D : ActionCouplingData X) (c : TGLCoupling) (psi : X → ℂ) (hEOM : D.EOM c psi) (K : (X → ℂ) →ₗ[ℝ] (X → ℂ)) : D.fieldOperator psi = c.beta • K psi := by
  exact hEOM
