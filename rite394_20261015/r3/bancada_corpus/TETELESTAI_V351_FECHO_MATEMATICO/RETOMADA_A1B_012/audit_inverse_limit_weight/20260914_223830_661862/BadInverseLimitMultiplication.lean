import TGLExt.V351InverseLimitWeight
open TGLExt TGLV350.Regular
example (P : SiteProfile) (X Y : PositiveCoreInput P) :
    scalarInverseLimitWeight P (X.add Y) = scalarInverseLimitWeight P X * scalarInverseLimitWeight P Y := by
  exact scalarInverseLimitWeight_add P X Y
