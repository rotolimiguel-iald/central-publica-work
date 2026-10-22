import TGLExt.V351InverseGeneratorCutoff
open TGLExt TGLV350.Regular
example (P : SiteProfile) (ε : ℝ) (hε : 0 < ε)
    (x : RegularHilbert (TowerHilbert P)) :
    (regularInverseGeneratorCutoff P ε x,
      x+(ε : ℂ) • regularInverseGeneratorCutoff P ε x) ∈
        (regularPositiveGenerator P).graph := by
  exact regularInverseGeneratorCutoff_graph P ε hε x
