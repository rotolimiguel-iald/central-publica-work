import TGLExt.V351RegularCoreTraceConstruction
open TGLExt TGLV350.Regular TGLV351
example (P : SiteProfile) (A : (regularCoreAlgebra P).toStarSubalgebra) :
    scalarInverseLimitWeight P (positiveSquare P A) = 0 :=
  scalarInverseLimitWeight_tracial P A
