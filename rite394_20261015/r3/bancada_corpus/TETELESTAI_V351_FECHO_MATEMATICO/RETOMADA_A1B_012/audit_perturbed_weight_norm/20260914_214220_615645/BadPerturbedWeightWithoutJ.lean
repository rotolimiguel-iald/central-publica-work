import TGLExt.V351PerturbedWeightNorm
open TGLExt TGLV350.Regular
example (P : SiteProfile)
    (b : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (A : scalarWeightLeftIdeal P) :
    dualQuadraticIntegral (star b.val * (star A.val.val*A.val.val) * b.val)
      (regularVacuum P) =
    ENNReal.ofReal (‖scalarGNSRepresentation P (star b)
      (scalarWeightGNSEmbedding P A)‖^2) := by
  exact scalarWeight_right_perturbed_norm P b hb A
