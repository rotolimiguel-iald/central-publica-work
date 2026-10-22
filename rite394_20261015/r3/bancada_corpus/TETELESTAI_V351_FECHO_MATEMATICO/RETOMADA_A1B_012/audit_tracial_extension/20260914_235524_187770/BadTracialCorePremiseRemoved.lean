import TGLExt.V351InverseLimitTracialExtension
open TGLExt TGLV350.Regular TGLV351
example (P : SiteProfile) :
    ∀ A : (regularCoreAlgebra P).toStarSubalgebra,
      scalarInverseLimitWeight P (positiveSquare P A) =
        scalarInverseLimitWeight P (positiveSquare P (star A)) :=
  scalarInverseLimitWeight_tracial_iff_core P
