import TGLExt.V351RegularGeneratorAffiliation
open TGLExt TGLV350.Regular
example (P : SiteProfile)
    (B : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hB : B ∈ (regularCoreAlgebra P).commutant)
    (x y : RegularHilbert (TowerHilbert P))
    (hxy : (x,y) ∈ (regularPositiveGenerator P).graph) :
    (B x,2 • B y) ∈ (regularPositiveGenerator P).graph := by
  exact regularPositiveGenerator_commutant_graph P B hB x y hxy
