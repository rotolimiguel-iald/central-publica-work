import IndependentAssemblyControls

example (P : TGLExt.SiteProfile) : (TGLV354.regularSusyData P).gapD.operator = 0 := by
  exact IndependentAssembly.susy_gap_equals_PF P
