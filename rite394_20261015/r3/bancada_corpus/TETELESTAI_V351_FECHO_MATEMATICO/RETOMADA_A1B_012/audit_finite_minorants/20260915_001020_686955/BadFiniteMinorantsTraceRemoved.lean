import TGLExt.V351InverseLimitFiniteMinorants
open TGLExt TGLV350.Regular TGLV351
open scoped ENNReal
example (P : SiteProfile) : ∀ X : PositiveCoreInput P,
    scalarInverseLimitWeight P X =
      ⨆ (Y : PositiveCoreInput P) (_ : Y ≤ X)
        (_ : scalarInverseLimitWeight P Y < ⊤), scalarInverseLimitWeight P Y :=
  scalarInverseLimitWeight_finite_minorants P
