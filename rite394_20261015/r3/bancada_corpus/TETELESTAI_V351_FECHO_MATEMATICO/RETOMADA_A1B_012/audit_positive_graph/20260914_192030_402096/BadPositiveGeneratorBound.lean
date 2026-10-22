import TGLExt.V351RegularPositiveGraph
open TGLExt TGLV350.Regular
example (P : SiteProfile) : regularSpectralResolvent P ≤ 0 := by
  exact regularSpectralResolvent_le_one P
