import TGLExt.V351InverseCutoffCFC
open TGLExt TGLV350.Regular
example (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    regularInverseGeneratorCutoff P ε =
      cfc (inverseCutoffFunction ε) (1-regularSpectralResolvent P) := by
  exact regularInverseGeneratorCutoff_cfc P ε hε
