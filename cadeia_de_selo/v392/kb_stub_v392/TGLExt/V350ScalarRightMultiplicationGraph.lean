import TGLExt.V350ComplexGraphProjection

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt WithLp
noncomputable section

def scalarRightMultiplicationVector (P : SiteProfile) (η : ScalarGNSHilbert P) :
    scalarWeightLeftIdeal P →ₗ[ℂ] ScalarGNSHilbert P where
  toFun a := scalarGNSRepresentation P a.val η
  map_add' a b := by
    change scalarGNSRepresentation P (a.val+b.val) η = _
    rw [map_add]
    rfl
  map_smul' c a := by
    change scalarGNSRepresentation P (c • a.val) η = _
    rw [map_smul]
    rfl

def scalarWeightPairProduct (P : SiteProfile) (a b : scalarWeightLeftIdeal P) :
    scalarWeightStarCore P :=
  ⟨star a.val * b.val,scalarWeightLeftIdeal_left_mul P (star a.val) b.val b.property,by
    change HasFiniteScalarSquare P (star (star a.val.val * b.val.val))
    rw [star_mul,star_star]
    exact HasFiniteScalarSquare.left_mul P (star b.val.val) a.val.val a.property⟩

theorem scalarWeightPairProduct_star (P : SiteProfile) (a b : scalarWeightLeftIdeal P) :
    star (scalarWeightPairProduct P a b) = scalarWeightPairProduct P b a := by
  apply Subtype.ext
  change star (star a.val * b.val) = star b.val * a.val
  rw [star_mul,star_star]

theorem scalarWeightPairProduct_embedding (P : SiteProfile) (a b : scalarWeightLeftIdeal P) :
    scalarWeightStarEmbedding P (scalarWeightPairProduct P a b) =
      scalarGNSRepresentation P (star a.val) (scalarWeightGNSEmbedding P b) :=
  (scalarWeightGNSAction_intertwines P (star a.val) b).symm

/-- A vector fixed by the original maximal adjoint makes right multiplication
symmetric on the full scalar weight ideal. -/
theorem scalarRightMultiplicationVector_symmetric (P : SiteProfile)
    (η : scalarTomitaAdjointDomain P) (hη : scalarTomitaAdjoint P η = (η : ScalarGNSHilbert P))
    (a b : scalarWeightLeftIdeal P) :
    inner ℂ (scalarRightMultiplicationVector P η a) (scalarWeightGNSEmbedding P b) =
      inner ℂ (scalarWeightGNSEmbedding P a) (scalarRightMultiplicationVector P η b) := by
  let c := scalarWeightPairProduct P a b
  let x : scalarClosedTomitaDomain P :=
    ⟨scalarWeightStarEmbedding P c,scalarWeightStar_mem_closedTomitaDomain P c⟩
  have hp : inner ℂ (scalarWeightStarEmbedding P (star c)) (η : ScalarGNSHilbert P) =
      inner ℂ (η : ScalarGNSHilbert P) (scalarWeightStarEmbedding P c) := by
    calc
      _ = inner ℂ (scalarClosedTomita P x) (η : ScalarGNSHilbert P) :=
        congrArg (fun z : ScalarGNSHilbert P => inner ℂ z (η : ScalarGNSHilbert P))
          (scalarClosedTomita_extends_weight_star P c).symm
      _ = inner ℂ (scalarTomitaAdjoint P η) (x : ScalarGNSHilbert P) :=
        scalarTomitaAdjoint_pairing P η x
      _ = _ := congrArg (fun z : ScalarGNSHilbert P => inner ℂ z (x : ScalarGNSHilbert P)) hη
  have ha : (scalarGNSRepresentation P a.val).adjoint = scalarGNSRepresentation P (star a.val) :=
    (map_star (scalarGNSRepresentation P) a.val).symm
  have hb : (scalarGNSRepresentation P b.val).adjoint = scalarGNSRepresentation P (star b.val) :=
    (map_star (scalarGNSRepresentation P) b.val).symm
  calc
    _ = inner ℂ (η : ScalarGNSHilbert P)
        ((scalarGNSRepresentation P a.val).adjoint (scalarWeightGNSEmbedding P b)) :=
      ((scalarGNSRepresentation P a.val).adjoint_inner_right _ _).symm
    _ = inner ℂ (η : ScalarGNSHilbert P) (scalarWeightStarEmbedding P c) := by
      exact congrArg (inner ℂ (η : ScalarGNSHilbert P))
        ((congrArg (fun T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
          T (scalarWeightGNSEmbedding P b)) ha).trans (scalarWeightPairProduct_embedding P a b).symm)
    _ = inner ℂ (scalarWeightStarEmbedding P (star c)) (η : ScalarGNSHilbert P) := hp.symm
    _ = inner ℂ ((scalarGNSRepresentation P b.val).adjoint (scalarWeightGNSEmbedding P a))
        (η : ScalarGNSHilbert P) := by
      apply congrArg (fun z : ScalarGNSHilbert P => inner ℂ z (η : ScalarGNSHilbert P))
      exact (congrArg (scalarWeightStarEmbedding P) (scalarWeightPairProduct_star P a b)).trans
        ((scalarWeightPairProduct_embedding P b a).trans
          (congrArg (fun T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
            T (scalarWeightGNSEmbedding P a)) hb.symm))
    _ = _ := (scalarGNSRepresentation P b.val).adjoint_inner_left _ _

def scalarRightMultiplicationGraph (P : SiteProfile) (η : ScalarGNSHilbert P) :
    Submodule ℂ (WithLp 2 (ScalarGNSHilbert P × ScalarGNSHilbert P)) :=
  complexGraphClosure (scalarWeightGNSEmbedding P) (scalarRightMultiplicationVector P η)

instance scalarRightMultiplicationGraph_complete (P : SiteProfile) (η : ScalarGNSHilbert P) :
    CompleteSpace (scalarRightMultiplicationGraph P η) := complexGraphClosure_complete _ _

theorem scalarRightMultiplicationGraph_invariant (P : SiteProfile) (η : ScalarGNSHilbert P)
    (c : (regularCoreAlgebra P).toStarSubalgebra) :
    Invariant (hilbertPairDiagonal (scalarGNSRepresentation P c)) (scalarRightMultiplicationGraph P η) := by
  apply complexGraphClosure_invariant
  intro a
  refine ⟨scalarWeightLeftProduct P c a,(scalarWeightGNSAction_intertwines P c a).symm,?_⟩
  change scalarGNSRepresentation P (c * a.val) η = _
  rw [map_mul]
  rfl

theorem scalarRightMultiplicationGraph_projection_commutes (P : SiteProfile) (η : ScalarGNSHilbert P)
    (c : (regularCoreAlgebra P).toStarSubalgebra)
    (x : WithLp 2 (ScalarGNSHilbert P × ScalarGNSHilbert P)) :
    (scalarRightMultiplicationGraph P η).starProjection
        (hilbertPairDiagonal (scalarGNSRepresentation P c) x) =
      hilbertPairDiagonal (scalarGNSRepresentation P c)
        ((scalarRightMultiplicationGraph P η).starProjection x) := by
  apply starProjection_commutes_of_invariant
  · exact scalarRightMultiplicationGraph_invariant P η c
  · rw [hilbertPairDiagonal_adjoint,← ContinuousLinearMap.star_eq_adjoint,← map_star]
    exact scalarRightMultiplicationGraph_invariant P η (star c)

theorem scalarRightMultiplicationGraph_rotated_zero (P : SiteProfile)
    (η : scalarTomitaAdjointDomain P) (hη : scalarTomitaAdjoint P η = (η : ScalarGNSHilbert P))
    (a : scalarWeightLeftIdeal P) :
    (scalarRightMultiplicationGraph P η).starProjection
      (toLp 2 (scalarGNSRepresentation P a.val η,-scalarWeightGNSEmbedding P a)) = 0 :=
  complexGraphClosure_projection_rotated (scalarWeightGNSEmbedding P)
    (scalarRightMultiplicationVector P η) (scalarRightMultiplicationVector_symmetric P η hη) a

#print axioms scalarRightMultiplicationVector
#print axioms scalarWeightPairProduct
#print axioms scalarWeightPairProduct_star
#print axioms scalarWeightPairProduct_embedding
#print axioms scalarRightMultiplicationVector_symmetric
#print axioms scalarRightMultiplicationGraph
#print axioms scalarRightMultiplicationGraph_complete
#print axioms scalarRightMultiplicationGraph_invariant
#print axioms scalarRightMultiplicationGraph_projection_commutes
#print axioms scalarRightMultiplicationGraph_rotated_zero
end
end TGLV350.Regular
