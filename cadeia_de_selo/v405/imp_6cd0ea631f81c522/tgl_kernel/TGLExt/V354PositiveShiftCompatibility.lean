import TGLExt.V354PolarIntertwining
import TGLExt.V354PositiveTraceTransport
import TGLExt.V354CyclicTraceCompletion

set_option autoImplicit false

namespace TGLV354.TraceCompletion
open TGLExt TGLV350.Regular TGLV351
noncomputable section

/-- Positive compatibility is discharged by the constructed polar in N and
the existing A1 quadratic trace. No cyclic total trace is assumed. -/
theorem positiveShift_trace_compatible (P : SiteProfile) (p q : PositiveCoreInput P)
    (h : ShiftRelated (⟨p.val,p.property.1⟩ : (regularCoreAlgebra P).toStarSubalgebra)
      ⟨q.val,q.property.1⟩) :
    scalarInverseLimitWeight P p = scalarInverseLimitWeight P q := by
  obtain ⟨n,hn,r,s,hr,_,hp,hq⟩ := h
  have hr' : p.val*r.val=r.val*q.val :=
    congrArg (fun x : (regularCoreAlgebra P).toStarSubalgebra => x.val) hr
  have hp' : p.val ^ n=r.val*s.val := by
    simpa using congrArg (fun x : (regularCoreAlgebra P).toStarSubalgebra => x.val) hp
  have hq' : q.val ^ n=s.val*r.val := by
    simpa using congrArg (fun x : (regularCoreAlgebra P).toStarSubalgebra => x.val) hq
  have hpol := boundedPolar_transports_shift_factors p.val q.val r.val s.val
    p.property.2.isSelfAdjoint q.property.2.isSelfAdjoint n hn hr' hp' hq'
  let u : (regularCoreAlgebra P).toStarSubalgebra :=
    ⟨boundedPolar r.val,boundedPolar_mem (regularCoreAlgebra P) r.val r.property⟩
  exact scalarTrace_transport_of_support P p q u hpol.1 hpol.2

/-- The completion reads the exact A1 value on every positive operator.
This includes infinite values; no finite-dimensional approximation is used. -/
theorem cyclicTraceCandidate_positive (P : SiteProfile) (p : PositiveCoreInput P) :
    cyclicTraceCandidate P ⟨p.val,p.property.1⟩ = scalarInverseLimitWeight P p := by
  apply cyclicTraceCandidate_positive_of_compatibility P
  exact positiveShift_trace_compatible P

#print axioms positiveShift_trace_compatible
#print axioms cyclicTraceCandidate_positive
end
end TGLV354.TraceCompletion
