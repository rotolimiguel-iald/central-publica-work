import TGLExt.V351CutoffAverageCommutation
open TGLExt TGLV350.Regular
example (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) (δ : ℝ) :
    hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) * regularAverage P δ =
      -(regularAverage P δ * hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) := by
  exact (regularInverseCutoffSqrt_commutes_average P ε hε δ).eq
