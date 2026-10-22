import TGLExt.V351AllPositiveWeightOrder
open TGLExt TGLV350.Regular
example (P : SiteProfile) (b c : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (hc : c ∈ scalarPolarRightAlgebra P)
    (hbc : b * star b ≤ c * star c)
    (hbe : ∀ δ : ℝ, Commute b.val (regularAverage P δ))
    (hce : ∀ δ : ℝ, Commute c.val (regularAverage P δ)) (X : PositiveCoreInput P) :
    dualQuadraticIntegral (star c.val * X.val * c.val) (regularVacuum P) ≤
      dualQuadraticIntegral (star b.val * X.val * b.val) (regularVacuum P) := by
  exact scalarWeight_right_perturbed_mono_all_positive P b c hb hc hbc hbe hce X
