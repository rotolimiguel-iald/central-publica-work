import TGLExt.F1Fecho394.CanonicalFockRegularRightGNSR11
import TGLExt.F1Fecho394.RegularConjugationContinuityR1
import TGLExt.F1Fecho394.CanonicalFockWeightSandwichR5
/-! The actual regular left-right action on the full weight GNS, with its
coefficient formula. The same product as RegularGNSR8 is used, but the graph
consumer does not require its separate Star algebra instance elaboration. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockConjugation
open TGLExt.ImportedSQ F1Rede.BosonicFock
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockWeightDomain F1Fecho.CanonicalFockWeightCompletion F1Fecho.CanonicalFockWeightSandwich
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockRegularRightGNS
def regularConjugationGNS (t : ℝ) : GNSHilbert →L[ℂ] GNSHilbert :=
  scalarGNSRepresentation (regularRightCoreElement t) * regularRightGNS (-t)

theorem regularConjugationGNS_intertwines (t : ℝ) (A : scalarWeightLeftIdeal) :
    regularConjugationGNS t (scalarWeightGNSEmbedding A) =
      scalarWeightGNSEmbedding (scalarWeightLeftProduct (regularRightCoreElement t)
        (scalarRegularRightProduct (-t) A)) := by
  change scalarGNSRepresentation (regularRightCoreElement t)
    (regularRightGNS (-t) (scalarWeightGNSEmbedding A)) = _
  exact (congrArg (scalarGNSRepresentation (regularRightCoreElement t))
    (regularRightGNS_intertwines (-t) A)).trans
      (scalarWeightGNSAction_intertwines (regularRightCoreElement t) (scalarRegularRightProduct (-t) A))

theorem regularConjugationGNS_ambient (t : ℝ) (z : GNSHilbert) :
    (regularConjugationGNS t z).val =
      TGLV350.Regular.fibre (TGLV350.Regular.fibre
        (F1Fecho.RegularCovariantCore.boostCLM fockFlow t)) z.val := by
  change (TGLV350.Regular.dualOrbitRepresentation (regularUnitary t) *
    F1Fecho.RegularRightAction.ambient (H:=F) (-t)) z.val = _
  exact congrArg (fun T => T z.val)
    (F1Fecho.RegularConjugationAmbient.regular_conjugation_is_base_fibre fockFlow t)

theorem regularConjugationGNS_strongly_continuous (z : GNSHilbert) :
    Continuous (fun t : ℝ => regularConjugationGNS t z) := by
  apply continuous_induced_rng.mpr
  exact (F1Fecho.RegularConjugationAmbient.base_fibre_strongly_continuous fockFlow z.val).congr
    (fun t => (regularConjugationGNS_ambient t z).symm)

end F1Fecho.CanonicalFockConjugation
#print axioms F1Fecho.CanonicalFockConjugation.regularConjugationGNS
#print axioms F1Fecho.CanonicalFockConjugation.regularConjugationGNS_intertwines
#print axioms F1Fecho.CanonicalFockConjugation.regularConjugationGNS_ambient
#print axioms F1Fecho.CanonicalFockConjugation.regularConjugationGNS_strongly_continuous
