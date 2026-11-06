import TGLExt.F1Fecho394.CanonicalFockCyclicTraceCompletionR3
import TGLExt.F1Fecho394.CanonicalFockNormalizedSplitR5
import TGLExt.F1Fecho394.PhysicalFockNetRealizationR2

/-! DECLARADO / UNCOMPILED CANDIDATE, R52, 2026-10-16.
All 21 fields of the unchanged RemainingModularCoreInput are assembled from
the existing cyclic ENNReal completion and the normalized positive split on
the SAME regular Fock core. D stays explicit in the generic factory; the
physical specialization reuses the already constructed physicalCanonicalNet.
No trace, PF, corner, type-II, net inhabitance or equal-halves premise is added.
The positive reading agrees exactly with the existing inverse-supremum value.
This ENNReal cyclic completion does not assert complex linearity on the whole
algebra or a factor-type classification. Device and geometric-source contracts
remain separate. SplitR5 is a candidate dependency and must compile first.
Require EXIT0 and all eleven public reports before integration. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 10
noncomputable section
namespace F1Fecho.CanonicalFockModularCoreInputR1
open TGLExt.ImportedSQ TGLV350.Regular
open F1Fecho.NetworkReuse (CanonicalNetInput)
open F1Fecho.NetworkModularCore (RepresentedCore RemainingModularCoreInput coreEmbedding)
open F1Fecho.CanonicalFockRegular (core dualAction)
open F1Fecho.CanonicalFockWeight (PositiveInput add)
open F1Fecho.CanonicalFockInverseSupremum (value)
open F1Fecho.CanonicalFockActualInverseAdditivityR2 (value_add)
open F1Fecho.CanonicalFockPositiveShiftTransportR2 (positiveAsCore)
open F1Fecho.CanonicalFockCyclicTraceCompletionR3
open F1Fecho.CanonicalFockNormalizedSplitR5 (normalized_split_exists)
open F1Fecho.MaxwellLocalization (physicalCanonicalNet)
open scoped ENNReal

private abbrev AmbientHilbert := RegularHilbert F1Rede.BosonicFock.F
private abbrev ambientNormedAddCommGroup : NormedAddCommGroup AmbientHilbert := inferInstance
private abbrev ambientInnerProductSpace : InnerProductSpace ℂ AmbientHilbert := inferInstance
private abbrev ambientNormedSpace : NormedSpace ℂ AmbientHilbert := inferInstance
private abbrev ambientModule : Module ℂ AmbientHilbert := inferInstance
private abbrev ambientTopologicalSpace : TopologicalSpace AmbientHilbert := inferInstance
private abbrev ambientUniformSpace : UniformSpace AmbientHilbert := inferInstance
private abbrev ambientCompleteSpace : CompleteSpace AmbientHilbert := inferInstance
private abbrev ambientStar : Star (AmbientHilbert →L[ℂ] AmbientHilbert) := inferInstance
private abbrev ambientOrder : PartialOrder (AmbientHilbert →L[ℂ] AmbientHilbert) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := AmbientHilbert)
attribute [local instance] ambientNormedAddCommGroup ambientInnerProductSpace
  ambientNormedSpace ambientModule ambientTopologicalSpace ambientUniformSpace
  ambientCompleteSpace ambientStar ambientOrder

private def leftPositive : PositiveInput := Classical.choose normalized_split_exists
private def rightPositive : PositiveInput :=
  Classical.choose (Classical.choose_spec normalized_split_exists)

private theorem chosen_split :
    IsStarProjection leftPositive.val ∧ IsStarProjection rightPositive.val ∧
      leftPositive.val*rightPositive.val=0 ∧
      value (add leftPositive rightPositive)=1 ∧ value leftPositive=value rightPositive :=
  Classical.choose_spec (Classical.choose_spec normalized_split_exists)

private theorem chosen_sum_projection :
    IsStarProjection (add leftPositive rightPositive).val :=
  chosen_split.1.add chosen_split.2.1 chosen_split.2.2.1

private theorem chosen_sum_trace :
    cyclicTraceCandidate (positiveAsCore (add leftPositive rightPositive))=1 :=
  (cyclicTraceCandidate_positive _).trans chosen_split.2.2.2.1

private theorem chosen_sum_ne_zero :
    positiveAsCore (add leftPositive rightPositive) ≠ 0 := by
  intro hz
  exact one_ne_zero (chosen_sum_trace.symm.trans
    ((congrArg cyclicTraceCandidate hz).trans cyclicTraceCandidate_zero))

/-- The full existing modular-core input, with only the global net D explicit. -/
def modularCoreInput (D : CanonicalNetInput) : RemainingModularCoreInput D where
  trace := cyclicTraceCandidate
  trace_zero := cyclicTraceCandidate_zero
  trace_tracial := cyclicTraceCandidate_cyclic
  trace_star := cyclicTraceCandidate_star
  trace_dual_scaling := cyclicTraceCandidate_dual
  PF := positiveAsCore (add leftPositive rightPositive)
  PF_sa := Subtype.ext chosen_sum_projection.isSelfAdjoint.star_eq
  PF_idem := Subtype.ext chosen_sum_projection.isIdempotentElem
  PF_ne := chosen_sum_ne_zero
  PF_pos := chosen_sum_trace.symm ▸ (zero_lt_one : (0 : ℝ≥0∞)<1)
  PF_fin := chosen_sum_trace.symm ▸ ENNReal.one_lt_top
  Pp := positiveAsCore leftPositive
  Pm := positiveAsCore rightPositive
  Pp_sa := Subtype.ext chosen_split.1.isSelfAdjoint.star_eq
  Pp_idem := Subtype.ext chosen_split.1.isIdempotentElem
  Pm_sa := Subtype.ext chosen_split.2.1.isSelfAdjoint.star_eq
  Pm_idem := Subtype.ext chosen_split.2.1.isIdempotentElem
  split := rfl
  orth := Subtype.ext chosen_split.2.2.1
  trace_additive := (cyclicTraceCandidate_positive _).trans
    ((value_add leftPositive rightPositive).trans
      (congrArg₂ (fun x y : ℝ≥0∞ => x+y)
        (cyclicTraceCandidate_positive leftPositive).symm
        (cyclicTraceCandidate_positive rightPositive).symm))
  equal_halves := (cyclicTraceCandidate_positive leftPositive).trans
    (chosen_split.2.2.2.2.trans (cyclicTraceCandidate_positive rightPositive).symm)
#print axioms modularCoreInput

/-- The total reading is the existing shift-related cyclic completion. -/
theorem modularCoreInput_trace (D : CanonicalNetInput) :
    (modularCoreInput D).trace=cyclicTraceCandidate := rfl
#print axioms modularCoreInput_trace

/-- On every positive operator, including infinite values, no value changes. -/
theorem modularCoreInput_trace_positive (D : CanonicalNetInput) (p : PositiveInput) :
    (modularCoreInput D).trace (positiveAsCore p)=value p :=
  cyclicTraceCandidate_positive p
#print axioms modularCoreInput_trace_positive

theorem modularCoreInput_PF_trace (D : CanonicalNetInput) :
    (modularCoreInput D).trace (modularCoreInput D).PF=1 := chosen_sum_trace
#print axioms modularCoreInput_PF_trace

/-- Specialization to the existing compact Maxwell net; no new net is chosen. -/
def physicalModularCoreInput : RemainingModularCoreInput physicalCanonicalNet :=
  modularCoreInput physicalCanonicalNet
#print axioms physicalModularCoreInput

/-- Consume the original full Fock assembly on the existing physical net. -/
def physicalFockCertificate :
    FockCertificate physicalCanonicalNet.toLightNetData.toLightOneParticle :=
  physicalModularCoreInput.toCertificate
#print axioms physicalFockCertificate

theorem physical_core : physicalFockCertificate.Core=RepresentedCore := rfl
#print axioms physical_core

theorem physical_trace : physicalFockCertificate.trace=cyclicTraceCandidate := rfl
#print axioms physical_trace

theorem physical_dual : physicalFockCertificate.dualAction=dualAction := rfl
#print axioms physical_dual

theorem physical_embedding :
    physicalFockCertificate.embedding=coreEmbedding physicalCanonicalNet := rfl
#print axioms physical_embedding

theorem physical_net (O : Set (Fin 4 → ℝ)) :
    physicalFockCertificate.R (physicalCanonicalNet.K O)=F1Fecho.PhysicalFockNet.net O := rfl
#print axioms physical_net

end F1Fecho.CanonicalFockModularCoreInputR1
