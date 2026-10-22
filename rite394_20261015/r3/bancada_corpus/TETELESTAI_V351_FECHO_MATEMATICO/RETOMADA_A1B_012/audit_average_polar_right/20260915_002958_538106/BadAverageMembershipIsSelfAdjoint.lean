import TGLExt.V351AveragePolarRight
open TGLExt TGLV350.Regular
example (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ) :
    star (regularAverage P δ) = regularAverage P δ :=
  regularAverage_mem_scalarPolarRightAlgebra P δ hδ
