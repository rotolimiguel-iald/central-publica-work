import TGLExt.GoodFullLegacy012
open TGLV354.TraceCompletion

-- Intended semantic rejection: PF has the exact A1 value 1, not the value of zero.
example : regularLegacyCore.canonicalTrace regularLegacyThreeLocks.PF = 0 := by
  exact legacy_support_trace_is_one
