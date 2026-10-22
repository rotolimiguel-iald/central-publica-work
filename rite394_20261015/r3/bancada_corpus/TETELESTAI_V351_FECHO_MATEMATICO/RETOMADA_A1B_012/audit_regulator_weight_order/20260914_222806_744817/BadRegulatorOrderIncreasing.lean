import TGLExt.V351RegulatorWeightOrder
open TGLExt TGLV350.Regular
example (P : SiteProfile) (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) (hεη : ε ≤ η) :
    regularInverseGeneratorCutoff P ε ≤ regularInverseGeneratorCutoff P η := by
  exact regularInverseGeneratorCutoff_antitone P ε η hε hη hεη
