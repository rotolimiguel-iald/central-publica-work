import TGLExt.V351AntiunitaryResolventPhase

open TGLV350.Regular

example (t x : ℝ) :
    star (resolventPhaseFunction t (1-x)) = 2 * resolventPhaseFunction t x := by
  exact resolventPhaseFunction_reflection t x
