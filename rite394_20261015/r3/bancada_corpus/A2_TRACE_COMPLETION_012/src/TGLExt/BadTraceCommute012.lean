import TGLExt.GoodTraceCompletion012

-- Intended semantic rejection: an equality of cyclic readings is not xy=yx.
example (x y : Matrix (Fin 2) (Fin 2) ℝ) : x*y = y*x := by
  exact TGLV354.TraceCompletion.ShiftRelated.cyclic x y
