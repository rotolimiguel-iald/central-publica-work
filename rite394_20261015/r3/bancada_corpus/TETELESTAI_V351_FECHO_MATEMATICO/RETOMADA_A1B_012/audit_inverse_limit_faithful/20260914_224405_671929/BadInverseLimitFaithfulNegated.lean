import TGLExt.V351InverseLimitFaithful
open TGLExt TGLV350.Regular
example (P : SiteProfile) (X : PositiveCoreInput P) :
    scalarInverseLimitWeight P X = 0 ↔ X ≠ PositiveCoreInput.zero P := by
  exact scalarInverseLimitWeight_faithful P X
