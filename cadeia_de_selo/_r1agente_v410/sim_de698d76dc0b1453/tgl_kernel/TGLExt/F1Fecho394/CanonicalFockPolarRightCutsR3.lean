import TGLExt.F1Fecho394.GenericCutRecognitionR1
import TGLExt.F1Fecho394.CanonicalFockPolarRightAlgebraR6
import TGLExt.F1Fecho394.CanonicalFockGNSClosednessR5

-- BEGIN SOURCE CanonicalFockPolarRightClosureR4
/-! Closure, strong-star transport and cutoff consequences on the SAME Fock
GNS. The regular-unitary polar identity remains explicit until its separate
actual polar consumer. Reuses V351 modules as incorporated in v393. -/
/-! Norm closure and ambient functional calculus for the actual polar-right
identity algebra. The antiunitary remains explicit until its concrete polar
consumer; the full-weight embedding is identified by proven cut maps. -/
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option maxErrors 3
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
local instance : CompleteSpace F1Fecho.CanonicalFockGNS.GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
open TGLExt.ImportedSQ F1Rede.BosonicFock MeasureTheory Filter
open TGLV350.Regular (RegularHilbert dualOrbitRepresentation operatorFieldLift dualIntegralFamily operatorFieldLift_norm_le antiunitaryConjugate antiunitaryConjugate_apply)
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockWeightOrbit F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockGNSCuts F1Fecho.CanonicalFockGNSClosedness
open scoped Topology
variable (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
theorem scalarPolarRight_iff_cuts 
    (b : core.toStarSubalgebra) :
    ScalarPolarRight J b ↔ ∀ A : scalarWeightLeftIdeal, ∀ n : ℕ,
      scalarGNSCutMap (n : ℝ)
        (antiunitaryConjugate (H := GNSHilbert) J
          (scalarGNSRepresentation (star b)) (scalarWeightGNSEmbedding A)) =
        dualOrbitRepresentation (A.val.val*b.val) (scalarCutVacuum (n : ℝ)) := by
  unfold ScalarPolarRight
  exact GenericCutRecognition.forall_embedding_iff_cuts
    (A := core.toStarSubalgebra) (B := scalarWeightLeftIdeal)
    (H := GNSHilbert) (E := RegularHilbert (RegularHilbert F))
    (fun a => a ∈ scalarWeightLeftIdeal) scalarWeightGNSEmbedding
    (fun n => scalarGNSCutMap (n : ℝ))
    (fun n a => dualOrbitRepresentation a.val (scalarCutVacuum (n : ℝ)))
    (fun n A => scalarGNSCutMap_weight_embedding (n : ℝ) A)
    scalarWeightGNSEmbedding_of_cut_actions
    (fun A => A.val*b)
    (fun A => antiunitaryConjugate (H := GNSHilbert) J
      (scalarGNSRepresentation (star b)) (scalarWeightGNSEmbedding A))




end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRight_iff_cuts
