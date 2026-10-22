import TGLExt.V351PerturbedWeightOrder
open TGLExt TGLV350.Regular
example (P : SiteProfile)
    (b c : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (hc : c ∈ scalarPolarRightAlgebra P)
    (hbc : b * star b ≤ c * star c) (A : scalarWeightLeftIdeal P) :
    dualQuadraticIntegral (star c.val*(star A.val.val*A.val.val)*c.val) (regularVacuum P) ≤
    dualQuadraticIntegral (star b.val*(star A.val.val*A.val.val)*b.val) (regularVacuum P) := by
  exact scalarWeight_right_perturbed_mono P b c hb hc hbc A
