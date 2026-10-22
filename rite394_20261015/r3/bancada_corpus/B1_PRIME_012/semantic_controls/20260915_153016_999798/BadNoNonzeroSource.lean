import TGLExt.ActionCouplingControls
set_option autoImplicit false
open TGLExt TGLExt.ActionCouplingControls
example {X : Type*} (D : ActionCouplingData X) (c : TGLCoupling) (psi : X → ℂ) (hK : D.K_boundary psi = 0) : (-c.beta) = c.beta := by
  exact D.zero_source_hides_coefficient c psi hK (-c.beta)
