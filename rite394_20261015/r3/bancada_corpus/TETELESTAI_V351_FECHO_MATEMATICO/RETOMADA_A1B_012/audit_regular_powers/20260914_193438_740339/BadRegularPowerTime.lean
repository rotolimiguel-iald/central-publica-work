import TGLExt.V351RegularImaginaryPowers
open TGLExt TGLV350.Regular MeasureTheory
example (P : SiteProfile) (t : ℝ) (u : RegularHilbert (TowerHilbert P)) :
    resolventImaginaryPower (regularSpectralResolvent P)
      (regularSpectralResolvent_nonneg P) (regularSpectralResolvent_le_one P)
      (regularSpectralResolvent_injective P) (regularSpectralResolvent_complement_injective P)
      t u = regularUnitary P (-t) u := by
  exact regularPositiveGenerator_imaginaryPower P t u
