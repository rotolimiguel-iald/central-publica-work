import TGLExt.V354PositiveShiftCompatibility
import TGLExt.V354PositiveTraceReader
import TGLExt.V350WedgeModularData
import TGLExt.WitnessV3

set_option autoImplicit false

namespace TGLV354.TraceCompletion
open TGLExt TGLV350.Regular TGLExt.V350Continuous
open TGL.ModularRealization TGL.CoreSupport
noncomputable section

/-- The old signature is inhabited without weakening its cyclicity field.
The total ENNReal reader restricts exactly to the previously constructed A1
trace on the positive cone; global complex linearity is not asserted. -/
def regularLegacyCore : ContinuousCoreData theSpecificAQFTWitness towerWedgeData where
  Core := (regularCoreAlgebra mixProfile).toStarSubalgebra
  embedding := regularCoreEmbedding mixProfile
  embedding_injective := regularCoreEmbedding_injective mixProfile
  dualAction := regularDualAction mixProfile
  dualAction_zero := regularDualAction_zero mixProfile
  dualAction_add := regularDualAction_add mixProfile
  canonicalTrace := cyclicTraceCandidate mixProfile
  trace_zero := cyclicTraceCandidate_zero mixProfile
  trace_tracial := cyclicTraceCandidate_cyclic mixProfile
  trace_star := cyclicTraceCandidate_star mixProfile
  trace_dual_scaling := cyclicTraceCandidate_dual mixProfile

/-- Existing CoreSupport constructor, applied to the already constructed
finite support and equal faces on this same core and A1 trace. -/
def regularLegacyThreeLocks :
    ThreeLocksCoreData theSpecificAQFTWitness towerWedgeData regularLegacyCore := by
  let F := regularContinuousCorner mixProfile
  letI : Ring F.Core := F.instRing
  letI : StarRing F.Core := F.instStar
  have hne : (F.P : (regularCoreAlgebra mixProfile).toStarSubalgebra) ≠ 0 := by
    intro h
    exact regularFiniteSupport_ne_zero mixProfile
      (congrArg (fun x : (regularCoreAlgebra mixProfile).toStarSubalgebra => x.val) h)
  have htr : regularLegacyCore.canonicalTrace F.P = 1 := by
    change cyclicTraceCandidate mixProfile
      ⟨(regularFiniteSupport mixProfile).val,(regularFiniteSupport mixProfile).property.1⟩ = 1
    rw [cyclicTraceCandidate_positive,regularFiniteSupport_trace]
  have hadd : regularLegacyCore.canonicalTrace F.P =
      regularLegacyCore.canonicalTrace F.Pplus + regularLegacyCore.canonicalTrace F.Pminus := by
    change cyclicTraceCandidate mixProfile
      ⟨(regularFiniteSupport mixProfile).val,(regularFiniteSupport mixProfile).property.1⟩ =
      cyclicTraceCandidate mixProfile
        ⟨(regularNormalizedFaces mixProfile).val.1.val,(regularNormalizedFaces mixProfile).val.1.property.1⟩ +
      cyclicTraceCandidate mixProfile
        ⟨(regularNormalizedFaces mixProfile).val.2.val,(regularNormalizedFaces mixProfile).val.2.property.1⟩
    rw [cyclicTraceCandidate_positive,cyclicTraceCandidate_positive,cyclicTraceCandidate_positive]
    exact scalarInverseLimitWeight_add mixProfile _ _
  have hequal : regularLegacyCore.canonicalTrace F.Pplus =
      regularLegacyCore.canonicalTrace F.Pminus := by
    change cyclicTraceCandidate mixProfile
        ⟨(regularNormalizedFaces mixProfile).val.1.val,(regularNormalizedFaces mixProfile).val.1.property.1⟩ =
      cyclicTraceCandidate mixProfile
        ⟨(regularNormalizedFaces mixProfile).val.2.val,(regularNormalizedFaces mixProfile).val.2.property.1⟩
    rw [cyclicTraceCandidate_positive,cyclicTraceCandidate_positive]
    exact (regularNormalizedFaces mixProfile).property.2.2.2.2
  exact threeLocksFromSupport regularLegacyCore F.P F.Pplus F.Pminus
    F.P_idempotent F.P_selfAdjoint hne htr
    F.Pplus_idempotent F.Pplus_selfAdjoint F.Pminus_idempotent F.Pminus_selfAdjoint
    F.split F.orthogonal hadd hequal

/-- The packaged fields are literally the support and bounded minimal operator
whose graph affiliation and relative gap were already proved in A2. -/
theorem regularLegacyThreeLocks_concrete :
    (regularLegacyThreeLocks.PF : (regularCoreAlgebra mixProfile).toStarSubalgebra).val =
      (regularFiniteSupport mixProfile).val ∧
    (regularLegacyThreeLocks.H3Lt : (regularCoreAlgebra mixProfile).toStarSubalgebra).val =
      regularMinimalLock mixProfile := ⟨rfl,rfl⟩

/-- The exact dependent legacy realization. The wedge and infinite-Hilbert
suppliers are reused unchanged; this is not a new Bisognano-Wichmann theorem. -/
def regularModularRealization : TGLModularRealization theSpecificAQFTWitness where
  infiniteHilbert := witnessV3_infinite
  modular := towerWedgeData
  core := regularLegacyCore
  threeLocks := regularLegacyThreeLocks

/-- A term of the existing dependent-sum type, not merely Nonempty or a flag.
Its scope is the constructed minimal lock and the existing formal wedge data. -/
def regularFullWitness : FullTGLWitness :=
  ⟨theSpecificAQFTWitness,regularModularRealization⟩

#print axioms regularLegacyCore
#print axioms regularLegacyThreeLocks
#print axioms regularLegacyThreeLocks_concrete
#print axioms regularModularRealization
#print axioms regularFullWitness
end
end TGLV354.TraceCompletion
