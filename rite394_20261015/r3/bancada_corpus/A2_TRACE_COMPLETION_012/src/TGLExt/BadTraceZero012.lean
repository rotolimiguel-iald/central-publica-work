import TGLExt.GoodTraceCompletion012
open TGLV354.TraceCompletion TGLExt TGLV350.Regular

-- Intended semantic rejection: the zero law cannot erase a nonzero positive input.
example (P : SiteProfile) (p : PositiveCoreInput P)
    (hp : p ≠ PositiveCoreInput.zero P) :
    cyclicTraceCandidate P ⟨p.val,p.property.1⟩ = 0 := by
  exact cyclicTraceCandidate_zero P
