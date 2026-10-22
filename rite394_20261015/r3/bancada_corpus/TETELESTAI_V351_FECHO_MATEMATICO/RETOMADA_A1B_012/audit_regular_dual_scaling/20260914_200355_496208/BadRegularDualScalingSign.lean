import TGLExt.V351RegularGeneratorDualScaling
open TGLExt TGLV350.Regular
example (P : SiteProfile) (s : ℝ)
    (x y : RegularHilbert (TowerHilbert P)) :
    (x,y) ∈ (regularPositiveGenerator P).graph ↔
      (characterMultiplier s x,(Real.exp (-s) : ℂ) • characterMultiplier s y) ∈
        (regularPositiveGenerator P).graph := by
  exact regularPositiveGenerator_dual_scaling P s x y
