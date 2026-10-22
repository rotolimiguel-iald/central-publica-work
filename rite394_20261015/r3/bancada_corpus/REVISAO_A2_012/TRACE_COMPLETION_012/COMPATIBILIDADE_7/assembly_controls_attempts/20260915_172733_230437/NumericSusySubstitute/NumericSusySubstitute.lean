import IndependentAssemblyControls

example (P : TGLExt.SiteProfile) : TGLExt.SusyRelativeData
  (TGLV354.CoreProjection (TGLV350.Regular.regularCoreAlgebra P))
  (TGLV354.coreProjectionTraceSubadditive P) := by
  exact TGLExt.modelSusy
