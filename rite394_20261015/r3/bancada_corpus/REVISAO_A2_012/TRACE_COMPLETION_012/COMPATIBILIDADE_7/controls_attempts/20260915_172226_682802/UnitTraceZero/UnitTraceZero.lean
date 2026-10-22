import IndependentCompatibilityControls

example (P : TGLExt.SiteProfile) :
  TGLV354.TraceCompletion.cyclicTraceCandidate P
    (1 : (TGLV350.Regular.regularCoreAlgebra P).toStarSubalgebra) = 0 := by
  exact IndependentTraceCompatibility.unit_read_exact P
