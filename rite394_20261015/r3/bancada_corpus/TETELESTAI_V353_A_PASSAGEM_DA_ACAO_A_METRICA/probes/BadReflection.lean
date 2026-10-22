import TGLExt.TheSameBetaReadsThreeFaces
set_option autoImplicit false

-- Deliberately false: omission of the geometric cost from the reflected weight.
example (c : TGLExt.TGLCoupling) :
    Complex.normSq ((TGLExt.Smat (TGLExt.thetaMiguel c.beta)).mulVec TGLExt.e1 1)
      = c.alpha := by
  exact c.reflection_weight
