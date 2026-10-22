import TGLExt.V354RegularLegacyWitness
import TGLExt.V354RegularSusy

set_option autoImplicit false

namespace IndependentAssembly
open TGLExt TGLV350.Regular TGLV354 TGLV354.TraceCompletion
open TGL.ModularRealization
noncomputable section

def actualSigmaTerm : FullTGLWitness := regularFullWitness

theorem old_U_is_trivial : theSpecificAQFTWitness.U = (fun _ => 1) := rfl

theorem assembled_H_is_minimal :
    regularLegacyThreeLocks.H3Lt = 1 - regularLegacyThreeLocks.PF := rfl

theorem assembled_PF_trace_one :
    regularLegacyCore.canonicalTrace regularLegacyThreeLocks.PF = 1 := by
  change cyclicTraceCandidate mixProfile
    ⟨(regularFiniteSupport mixProfile).val, (regularFiniteSupport mixProfile).property.1⟩ = 1
  rw [cyclicTraceCandidate_positive, regularFiniteSupport_trace]

theorem assembled_PF_trace_not_two :
    regularLegacyCore.canonicalTrace regularLegacyThreeLocks.PF ≠ 2 := by
  rw [assembled_PF_trace_one]
  norm_num

theorem assembled_PF_nonzero : regularLegacyThreeLocks.PF ≠ 0 :=
  regularLegacyThreeLocks.PF_nonzero

theorem susy_gap_equals_PF (P : SiteProfile) :
    (regularSusyData P).gapD.operator = (regularFiniteSupport P).val :=
  (regularSusy_operator_identifications P).2.1.trans (regularMinimalLock_spectral_zero P)

theorem susy_gap_nonzero (P : SiteProfile) : (regularSusyData P).gapD.operator ≠ 0 := by
  rw [susy_gap_equals_PF]
  exact regularFiniteSupport_ne_zero P

def actualSusy (P : SiteProfile) :
    SusyRelativeData (CoreProjection (regularCoreAlgebra P)) (coreProjectionTraceSubadditive P) :=
  regularSusyData P

end
end IndependentAssembly
