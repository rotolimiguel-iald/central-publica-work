import TGLExt.TheSameBetaReadsThreeFaces
set_option autoImplicit false

-- Deliberately false: the multiplicative cost has been removed.
example (c : TGLExt.TGLCoupling) : c.beta = c.alpha := by
  exact c.beta_eq_alpha_exp
