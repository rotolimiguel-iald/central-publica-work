import IndependentCompatibilityControls

example : ((0 : ℂ →L[ℂ] ℂ) ^ 0) 1 = 0 := by
  exact IndependentTraceCompatibility.zero_operator_at_one
