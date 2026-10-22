import TGLExt.V351ScaledResolventFunctions

set_option autoImplicit false
open TGLV350.Regular TGLExt ChatgptAudit
noncomputable section
example (r x : ℝ) (hd : r+(1-r)*x ≠ 0) :
    1-scaledResolventCoordinate r x = r*(1-x)/(r+(1-r)*x) := by
  exact scaledResolventCoordinate_complement r x hd
end
