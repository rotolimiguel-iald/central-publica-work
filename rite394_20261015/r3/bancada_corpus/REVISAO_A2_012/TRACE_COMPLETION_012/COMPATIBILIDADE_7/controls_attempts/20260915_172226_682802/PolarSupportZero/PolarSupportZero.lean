import IndependentCompatibilityControls

example : star (TGLV354.boundedPolar (1 : ℂ →L[ℂ] ℂ)) *
  TGLV354.boundedPolar (1 : ℂ →L[ℂ] ℂ) = 0 := by
  exact IndependentTraceCompatibility.polar_one_product
