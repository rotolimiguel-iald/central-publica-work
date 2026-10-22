import TGLExt.V351WeightAverageRecovery
open TGLExt TGLV350.Regular
example (P : SiteProfile) (A : (regularCoreAlgebra P).toStarSubalgebra) :
    dualQuadraticIntegral (star A.val*A.val) (regularVacuum P) =
      dualQuadraticIntegral
        (star (A.val*regularAverage P 1)*(A.val*regularAverage P 1)) (regularVacuum P) := by
  exact scalarWeight_square_eq_iSup_averages P A
