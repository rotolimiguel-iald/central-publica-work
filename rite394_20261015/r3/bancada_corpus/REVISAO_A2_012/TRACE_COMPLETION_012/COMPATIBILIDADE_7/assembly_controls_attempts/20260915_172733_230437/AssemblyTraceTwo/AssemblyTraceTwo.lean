import IndependentAssemblyControls

example : TGLV354.TraceCompletion.regularLegacyCore.canonicalTrace
  TGLV354.TraceCompletion.regularLegacyThreeLocks.PF = 2 := by
  exact IndependentAssembly.assembled_PF_trace_one
