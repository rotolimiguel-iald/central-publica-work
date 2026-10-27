import TGLExt.V350ScalarRightMultiplicationGraph
import TGLExt.V350HilbertProjectionBlocks
import TGLExt.V350ScalarRightPairVector

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt WithLp
noncomputable section

/-- The off-diagonal block is an actual bounded right-adjoint pair,
constructed from a fixed vector of the original maximal F. -/
def scalarRightProjectionPair (P : SiteProfile)
    (η : scalarTomitaAdjointDomain P)
    (hη : scalarTomitaAdjoint P η = (η : ScalarGNSHilbert P)) :
    ScalarRightAdjointPair P
      (hilbertBlockB (scalarRightMultiplicationGraph P η).starProjection) where
  vector := hilbertBlockA (scalarRightMultiplicationGraph P η).starProjection η
  adjointVector := (η : ScalarGNSHilbert P) -
    hilbertBlockD (scalarRightMultiplicationGraph P η).starProjection η
  right a := by
    have hA := hilbertBlockA_commutes
      (scalarRightMultiplicationGraph P η).starProjection (scalarGNSRepresentation P a.val)
      (scalarRightMultiplicationGraph_projection_commutes P η a.val)
    exact (hilbertBlockB_from_rotated _ _ _
      (scalarRightMultiplicationGraph_rotated_zero P η hη a)).trans
        (congrArg (fun T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P => T η) hA.eq)
  adjoint a := by
    have hD := hilbertBlockD_commutes
      (scalarRightMultiplicationGraph P η).starProjection (scalarGNSRepresentation P a.val)
      (scalarRightMultiplicationGraph_projection_commutes P η a.val)
    have hp : (scalarRightMultiplicationGraph P η).starProjection
        (toLp 2 (scalarWeightGNSEmbedding P a,scalarGNSRepresentation P a.val η)) =
          toLp 2 (scalarWeightGNSEmbedding P a,scalarGNSRepresentation P a.val η) :=
      Submodule.starProjection_eq_self_iff.mpr
        (complexGraphEmbedding_mem (scalarWeightGNSEmbedding P)
          (scalarRightMultiplicationVector P η) a)
    change (hilbertBlockB (scalarRightMultiplicationGraph P η).starProjection).adjoint
      (scalarWeightGNSEmbedding P a) = _
    exact (hilbertBlockBadjoint_from_fixed _ _ _ hp).trans
      ((congrArg (fun z : ScalarGNSHilbert P => scalarGNSRepresentation P a.val η - z)
        (congrArg (fun T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P => T η) hD.eq)).trans
          (map_sub (scalarGNSRepresentation P a.val) _ _).symm)

private theorem adjointSumSelfAdjoint {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (B : H →L[ℂ] H) :
    star (B + star B) = B + star B := by
  rw [star_add,star_star,add_comm]

def scalarRightProjectionElement (P : SiteProfile)
    (η : scalarTomitaAdjointDomain P)
    (hη : scalarTomitaAdjoint P η = (η : ScalarGNSHilbert P)) : scalarPairedRightAlgebra P :=
  let B := hilbertBlockB (scalarRightMultiplicationGraph P η).starProjection
  let d := scalarRightProjectionPair P η hη
  ⟨B + star B,⟨scalarRightAdjointPair_add d (scalarRightAdjointPair_star d)⟩⟩

theorem scalarRightProjectionElement_selfadjoint (P : SiteProfile)
    (η : scalarTomitaAdjointDomain P)
    (hη : scalarTomitaAdjoint P η = (η : ScalarGNSHilbert P)) :
    star (scalarRightProjectionElement P η hη) = scalarRightProjectionElement P η hη := by
  apply Subtype.ext
  exact adjointSumSelfAdjoint _

private theorem projectionWitness_reassociate {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (S : Submodule ℂ (WithLp 2 (H × H))) [CompleteSpace S] (v : H) :
    hilbertBlockA S.starProjection v + (v - hilbertBlockD S.starProjection v) =
      hilbertProjectionWitness S v := by
  unfold hilbertProjectionWitness
  abel

theorem scalarRightProjectionElement_vector (P : SiteProfile)
    (η : scalarTomitaAdjointDomain P)
    (hη : scalarTomitaAdjoint P η = (η : ScalarGNSHilbert P)) :
    scalarRightPairVector P (scalarRightProjectionElement P η hη) =
      hilbertProjectionWitness (scalarRightMultiplicationGraph P η) η :=
  (scalarRightPairVector_of_pair P _
    (scalarRightAdjointPair_add (scalarRightProjectionPair P η hη)
      (scalarRightAdjointPair_star (scalarRightProjectionPair P η hη)))).trans
        (projectionWitness_reassociate _ _)

theorem scalarRightProjectionElement_positive (P : SiteProfile)
    (η : scalarTomitaAdjointDomain P)
    (hη : scalarTomitaAdjoint P η = (η : ScalarGNSHilbert P))
    (hne : (η : ScalarGNSHilbert P) ≠ 0) :
    0 < (inner ℂ (η : ScalarGNSHilbert P)
      (scalarRightPairVector P (scalarRightProjectionElement P η hη))).re := by
  have hpos := complexGraph_witness_positive (scalarWeightGNSEmbedding P)
    (scalarRightMultiplicationVector P η) (scalarWeightGNSEmbedding_denseRange P) η hne
  exact (congrArg (fun z : ScalarGNSHilbert P =>
    0 < (inner ℂ (η : ScalarGNSHilbert P) z).re)
      (scalarRightProjectionElement_vector P η hη)).mpr hpos

/-- Every nonzero original F-fixed vector is detected by a genuine
self-adjoint element of the previously constructed right algebra. -/
theorem scalarRight_selfadjoint_detects_fixed (P : SiteProfile)
    (η : scalarTomitaAdjointDomain P)
    (hη : scalarTomitaAdjoint P η = (η : ScalarGNSHilbert P))
    (hne : (η : ScalarGNSHilbert P) ≠ 0) :
    ∃ a : scalarPairedRightAlgebra P, star a = a ∧
      0 < (inner ℂ (η : ScalarGNSHilbert P) (scalarRightPairVector P a)).re :=
  ⟨scalarRightProjectionElement P η hη,
    scalarRightProjectionElement_selfadjoint P η hη,
    scalarRightProjectionElement_positive P η hη hne⟩

#print axioms scalarRightProjectionPair
#print axioms scalarRightProjectionElement
#print axioms scalarRightProjectionElement_selfadjoint
#print axioms scalarRightProjectionElement_vector
#print axioms scalarRightProjectionElement_positive
#print axioms scalarRight_selfadjoint_detects_fixed
end
end TGLV350.Regular
