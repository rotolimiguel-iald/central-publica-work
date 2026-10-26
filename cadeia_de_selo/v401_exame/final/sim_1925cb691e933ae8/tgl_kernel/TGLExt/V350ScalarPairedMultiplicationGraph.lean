import TGLExt.V350HilbertProjectionBlocks
import TGLExt.V350ScalarSquareAdjointTest

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 200000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt WithLp
noncomputable section

private def pairedEvaluation {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (E : NonUnitalStarSubalgebra ℂ (H →L[ℂ] H)) (η : H) : E →ₗ[ℂ] H where
  toFun a := a.val η
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

private def pairedGraph {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (E : NonUnitalStarSubalgebra ℂ (H →L[ℂ] H)) (j : E →ₗ[ℂ] H) (η : H) :
    Submodule ℂ (WithLp 2 (H × H)) :=
  complexGraphClosure (H:=H) (E:=E) j (pairedEvaluation E η)

private instance pairedGraphComplete {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (E : NonUnitalStarSubalgebra ℂ (H →L[ℂ] H)) (j : E →ₗ[ℂ] H) (η : H) :
    CompleteSpace (pairedGraph E j η) := complexGraphClosure_complete j (pairedEvaluation E η)

private theorem pairedFixedSymmetry {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (E : NonUnitalStarSubalgebra ℂ (H →L[ℂ] H)) (j : E →ₗ[ℂ] H)
    (hm : ∀ a b : E, j (a*b)=a.val (j b)) (η : H)
    (hp : ∀ a : E, inner ℂ (j (star a)) η = inner ℂ η (j a)) (a b : E) :
    inner ℂ (a.val η) (j b) = inner ℂ (j a) (b.val η) := by
  have he : star (star a*b)=star b*a := by rw [star_mul,star_star]
  calc
    _ = inner ℂ η (star a.val (j b)) := (a.val.adjoint_inner_right η (j b)).symm
    _ = inner ℂ η (j (star a*b)) := congrArg (inner ℂ η) (hm (star a) b).symm
    _ = inner ℂ (j (star (star a*b))) η := (hp (star a*b)).symm
    _ = inner ℂ (star b.val (j a)) η :=
      congrArg (fun v : H => inner ℂ v η) ((congrArg j he).trans (hm (star b) a))
    _ = _ := b.val.adjoint_inner_left η (j a)

private theorem pairedCorePairing {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (E : NonUnitalStarSubalgebra ℂ (H →L[ℂ] H)) (j : E →ₗ[ℂ] H)
    (D : Submodule ℂ H) (F : D →ₛₗ[starRingEnd ℂ] H)
    (hj : ∀ a : E, ∃ hx : j a ∈ D, F ⟨j a,hx⟩=j (star a))
    (η : H) (hp : ∀ x : D, inner ℂ (F x) η = inner ℂ η (x:H)) (a : E) :
    inner ℂ (j (star a)) η = inner ℂ η (j a) := by
  obtain ⟨hx,hf⟩ := hj a
  exact (congrArg (fun v : H => inner ℂ v η) hf).symm.trans (hp ⟨j a,hx⟩)

private theorem pairedGraphInvariant {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (E : NonUnitalStarSubalgebra ℂ (H →L[ℂ] H)) (j : E →ₗ[ℂ] H)
    (hm : ∀ a b : E, j (a*b)=a.val (j b)) (η : H) (c : E) :
    Invariant (hilbertPairDiagonal c.val) (pairedGraph E j η) := by
  apply complexGraphClosure_invariant
  intro a
  exact ⟨c*a,hm c a,rfl⟩

private theorem pairedGraphProjectionCommutes {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (E : NonUnitalStarSubalgebra ℂ (H →L[ℂ] H)) (j : E →ₗ[ℂ] H)
    (hm : ∀ a b : E, j (a*b)=a.val (j b)) (η : H) (c : E)
    (x : WithLp 2 (H × H)) :
    (pairedGraph E j η).starProjection (hilbertPairDiagonal c.val x) =
      hilbertPairDiagonal c.val ((pairedGraph E j η).starProjection x) := by
  apply complexGraphClosure_projection_commutes
  · intro a; exact ⟨c*a,hm c a,rfl⟩
  · intro a; exact ⟨star c*a,hm (star c) a,rfl⟩

private theorem pairedGraphFixed {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (E : NonUnitalStarSubalgebra ℂ (H →L[ℂ] H)) (j : E →ₗ[ℂ] H) (η : H) (a : E) :
    (pairedGraph E j η).starProjection (toLp 2 (j a,a.val η))=toLp 2 (j a,a.val η) :=
  Submodule.starProjection_eq_self_iff.mpr (complexGraphEmbedding_mem j (pairedEvaluation E η) a)

private theorem pairedGraphRotated {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (E : NonUnitalStarSubalgebra ℂ (H →L[ℂ] H)) (j : E →ₗ[ℂ] H) (η : H)
    (hs : ∀ a b : E, inner ℂ (a.val η) (j b)=inner ℂ (j a) (b.val η)) (a : E) :
    (pairedGraph E j η).starProjection (toLp 2 (a.val η,-j a))=0 :=
  complexGraphClosure_projection_rotated j (pairedEvaluation E η) hs a

def scalarPairedMultiplicationVector (P : SiteProfile) (η : ScalarGNSHilbert P) :
    scalarPairedRightAlgebra P →ₗ[ℂ] ScalarGNSHilbert P :=
  pairedEvaluation (scalarPairedRightAlgebra P) η

/-- This graph uses the right-pair algebra E and its vector map j. -/
def scalarPairedMultiplicationGraph (P : SiteProfile) (η : ScalarGNSHilbert P) :
    Submodule ℂ (WithLp 2 (ScalarGNSHilbert P × ScalarGNSHilbert P)) :=
  pairedGraph (scalarPairedRightAlgebra P) (scalarRightPairVector P) η

instance scalarPairedMultiplicationGraph_complete (P : SiteProfile) (η : ScalarGNSHilbert P) :
    CompleteSpace (scalarPairedMultiplicationGraph P η) :=
  pairedGraphComplete (scalarPairedRightAlgebra P) (scalarRightPairVector P) η

/-- Fixedness is for the original S, unlike the older weight-ideal graph. -/
theorem scalarPairedMultiplicationVector_symmetric (P : SiteProfile)
    (η : scalarClosedTomitaDomain P) (hη : scalarClosedTomita P η=(η:ScalarGNSHilbert P))
    (a b : scalarPairedRightAlgebra P) :
    inner ℂ (scalarPairedMultiplicationVector P η a) (scalarRightPairVector P b) =
      inner ℂ (scalarRightPairVector P a) (scalarPairedMultiplicationVector P η b) := by
  refine pairedFixedSymmetry (scalarPairedRightAlgebra P) (scalarRightPairVector P)
    ?_ η ?_ a b
  · intro u v; exact scalarRightPairVector_mul P u v
  · refine pairedCorePairing (scalarPairedRightAlgebra P) (scalarRightPairVector P)
      (scalarTomitaAdjointDomain P) (scalarTomitaAdjoint P).toFun ?_ η ?_
    · intro u; exact scalarRightPairVector_original_adjoint P u
    · exact (scalarClosedTomita_bidual_graph_iff P η η).mp ⟨η.property,hη⟩

theorem scalarPairedMultiplicationGraph_invariant (P : SiteProfile) (η : ScalarGNSHilbert P)
    (a : scalarPairedRightAlgebra P) :
    Invariant (hilbertPairDiagonal a.val) (scalarPairedMultiplicationGraph P η) := by
  refine pairedGraphInvariant (scalarPairedRightAlgebra P) (scalarRightPairVector P) ?_ η a
  intro u v; exact scalarRightPairVector_mul P u v

theorem scalarPairedMultiplicationGraph_projection_commutes (P : SiteProfile)
    (η : ScalarGNSHilbert P) (a : scalarPairedRightAlgebra P)
    (x : WithLp 2 (ScalarGNSHilbert P × ScalarGNSHilbert P)) :
    (scalarPairedMultiplicationGraph P η).starProjection (hilbertPairDiagonal a.val x) =
      hilbertPairDiagonal a.val ((scalarPairedMultiplicationGraph P η).starProjection x) := by
  refine pairedGraphProjectionCommutes (scalarPairedRightAlgebra P) (scalarRightPairVector P) ?_ η a x
  intro u v; exact scalarRightPairVector_mul P u v

theorem scalarPairedMultiplicationGraph_projection_fixed (P : SiteProfile)
    (η : ScalarGNSHilbert P) (a : scalarPairedRightAlgebra P) :
    (scalarPairedMultiplicationGraph P η).starProjection
      (toLp 2 (scalarRightPairVector P a,a.val η)) =
        toLp 2 (scalarRightPairVector P a,a.val η) :=
  pairedGraphFixed (scalarPairedRightAlgebra P) (scalarRightPairVector P) η a

theorem scalarPairedMultiplicationGraph_rotated_zero (P : SiteProfile)
    (η : scalarClosedTomitaDomain P) (hη : scalarClosedTomita P η=(η:ScalarGNSHilbert P))
    (a : scalarPairedRightAlgebra P) :
    (scalarPairedMultiplicationGraph P η).starProjection
      (toLp 2 (a.val η,-scalarRightPairVector P a)) = 0 :=
  pairedGraphRotated (scalarPairedRightAlgebra P) (scalarRightPairVector P) η
    (scalarPairedMultiplicationVector_symmetric P η hη) a

#print axioms scalarPairedMultiplicationVector_symmetric
#print axioms scalarPairedMultiplicationGraph_invariant
#print axioms scalarPairedMultiplicationGraph_projection_commutes
#print axioms scalarPairedMultiplicationGraph_projection_fixed
#print axioms scalarPairedMultiplicationGraph_rotated_zero
end
end TGLV350.Regular
