import TGLExt.V351RegularSpectralGraph
open TGLExt TGLV350.Regular MeasureTheory
example (P : SiteProfile) (x y : RegularHilbert (TowerHilbert P)) :
    (x,y) ∈ (regularPositiveGenerator P).graph ↔
      ∀ᵐ ξ ∂volume, ((regularSpectralCoordinates P).symm y) ξ =
        (Real.exp (2*Real.pi*ξ) : ℂ) • ((regularSpectralCoordinates P).symm x) ξ := by
  exact regularPositiveGenerator_graph_iff P x y
