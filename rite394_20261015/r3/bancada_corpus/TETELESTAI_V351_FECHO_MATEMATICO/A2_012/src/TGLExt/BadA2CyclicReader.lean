import TGLExt.V354TraceReaderWall
open TGLExt TGLV350.Regular
example (P : SiteProfile) :
    ∀ x y : (regularCoreAlgebra P).toStarSubalgebra,
      positiveTraceReader P (x*y) = positiveTraceReader P (y*x) := by
  exact positiveTraceReader_not_cyclic P
