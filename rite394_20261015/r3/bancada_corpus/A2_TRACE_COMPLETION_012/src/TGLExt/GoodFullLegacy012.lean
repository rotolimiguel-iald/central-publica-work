import TGLExt.V354RegularLegacyWitness

set_option autoImplicit false
open TGLExt TGLV350.Regular TGLV354.TraceCompletion

theorem legacy_support_trace_is_one :
    regularLegacyCore.canonicalTrace regularLegacyThreeLocks.PF = 1 := by
  change cyclicTraceCandidate mixProfile
    ⟨(regularFiniteSupport mixProfile).val,(regularFiniteSupport mixProfile).property.1⟩ = 1
  rw [cyclicTraceCandidate_positive,regularFiniteSupport_trace]

theorem legacy_support_trace_is_not_zero :
    regularLegacyCore.canonicalTrace regularLegacyThreeLocks.PF ≠ 0 := by
  rw [legacy_support_trace_is_one]
  exact one_ne_zero

theorem legacy_minimal_gap_is_concrete :
    ∀ x ∈ (regularLegacyThreeLocks.H3Lt :
      (regularCoreAlgebra mixProfile).toStarSubalgebra).val.kerᗮ,
      ‖(regularLegacyThreeLocks.H3Lt :
        (regularCoreAlgebra mixProfile).toStarSubalgebra).val x‖ = ‖x‖ :=
  regularMinimalLock_relative_gap mixProfile

noncomputable example : TGL.ModularRealization.FullTGLWitness := regularFullWitness

#print axioms legacy_support_trace_is_one
#print axioms legacy_support_trace_is_not_zero
#print axioms legacy_minimal_gap_is_concrete
