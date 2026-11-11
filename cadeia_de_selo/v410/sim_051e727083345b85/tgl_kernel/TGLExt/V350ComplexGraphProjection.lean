import TGLExt.V350ScalarRightAdjointPair
import Mathlib.Analysis.InnerProductSpace.ProdL2

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt WithLp
noncomputable section
variable {H E : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [AddCommGroup E] [Module ℂ E]

def hilbertPairInl : H →L[ℂ] WithLp 2 (H × H) :=
  (WithLp.prodContinuousLinearEquiv 2 ℂ H H).symm.toContinuousLinearMap.comp
    ((ContinuousLinearMap.id ℂ H).prod (0 : H →L[ℂ] H))

def hilbertPairInr : H →L[ℂ] WithLp 2 (H × H) :=
  (WithLp.prodContinuousLinearEquiv 2 ℂ H H).symm.toContinuousLinearMap.comp
    ((0 : H →L[ℂ] H).prod (ContinuousLinearMap.id ℂ H))

def hilbertPairDiagonal (T : H →L[ℂ] H) : WithLp 2 (H × H) →L[ℂ] WithLp 2 (H × H) :=
  (WithLp.prodContinuousLinearEquiv 2 ℂ H H).symm.toContinuousLinearMap.comp
    ((T.prodMap T).comp (WithLp.prodContinuousLinearEquiv 2 ℂ H H).toContinuousLinearMap)

theorem hilbertPairDiagonal_adjoint (T : H →L[ℂ] H) :
    (hilbertPairDiagonal T).adjoint = hilbertPairDiagonal T.adjoint := by
  symm
  apply (ContinuousLinearMap.eq_adjoint_iff _ _).mpr
  intro x y
  simp only [WithLp.prod_inner_apply]
  change inner ℂ (T.adjoint (ofLp x).1) (ofLp y).1 +
      inner ℂ (T.adjoint (ofLp x).2) (ofLp y).2 =
    inner ℂ (ofLp x).1 (T (ofLp y).1) + inner ℂ (ofLp x).2 (T (ofLp y).2)
  rw [T.adjoint_inner_left,T.adjoint_inner_left]

def complexGraphEmbedding (e f : E →ₗ[ℂ] H) : E →ₗ[ℂ] WithLp 2 (H × H) :=
  (WithLp.linearEquiv 2 ℂ (H × H)).symm.toLinearMap.comp (e.prod f)

/-- Closed complex graph relation; single-valuedness is not assumed. -/
def complexGraphClosure (e f : E →ₗ[ℂ] H) : Submodule ℂ (WithLp 2 (H × H)) :=
  (complexGraphEmbedding e f).range.topologicalClosure

instance complexGraphClosure_complete (e f : E →ₗ[ℂ] H) :
    CompleteSpace (complexGraphClosure e f) :=
  Submodule.topologicalClosure.completeSpace (complexGraphEmbedding e f).range

theorem complexGraphEmbedding_mem (e f : E →ₗ[ℂ] H) (a : E) :
    toLp 2 (e a,f a) ∈ complexGraphClosure e f :=
  (complexGraphEmbedding e f).range.le_topologicalClosure ⟨a,rfl⟩

theorem complexGraphClosure_invariant (e f : E →ₗ[ℂ] H) (T : H →L[ℂ] H)
    (h : ∀ a, ∃ b, e b = T (e a) ∧ f b = T (f a)) :
    Invariant (hilbertPairDiagonal T) (complexGraphClosure e f) := by
  have ht : Set.MapsTo (hilbertPairDiagonal T)
      ((complexGraphEmbedding e f).range : Set (WithLp 2 (H × H)))
      ((complexGraphEmbedding e f).range : Set (WithLp 2 (H × H))) := by
    rintro _ ⟨a,rfl⟩
    obtain ⟨b,hb1,hb2⟩ := h a
    refine ⟨b,?_⟩
    change toLp 2 (e b,f b) = toLp 2 (T (e a),T (f a))
    rw [hb1,hb2]
  exact ht.closure (hilbertPairDiagonal T).continuous

theorem complexGraphClosure_rotated_orthogonal (e f : E →ₗ[ℂ] H)
    (hs : ∀ a b, inner ℂ (f a) (e b) = inner ℂ (e a) (f b)) (a : E) :
    toLp 2 (f a,-e a) ∈ (complexGraphClosure e f).orthogonal := by
  intro p hp
  have hc : IsClosed {q : WithLp 2 (H × H) | inner ℂ q (toLp 2 (f a,-e a)) = 0} :=
    isClosed_eq (by fun_prop) continuous_const
  apply closure_minimal (s := ((complexGraphEmbedding e f).range : Set (WithLp 2 (H × H)))) ?_ hc hp
  rintro _ ⟨b,rfl⟩
  change inner ℂ (toLp 2 (e b,f b)) (toLp 2 (f a,-e a)) = 0
  rw [WithLp.prod_inner_apply]
  change inner ℂ (e b) (f a) + inner ℂ (f b) (-e a) = 0
  rw [inner_neg_right,hs b a,add_neg_cancel]

theorem complexGraphClosure_projection_rotated (e f : E →ₗ[ℂ] H)
    (hs : ∀ a b, inner ℂ (f a) (e b) = inner ℂ (e a) (f b)) (a : E) :
    (complexGraphClosure e f).starProjection (toLp 2 (f a,-e a)) = 0 :=
  starProjection_eq_zero_of_mem_orthogonal (complexGraphClosure e f)
    (complexGraphClosure_rotated_orthogonal e f hs a)

theorem complexGraphClosure_projection_commutes (e f : E →ₗ[ℂ] H) (T : H →L[ℂ] H)
    (h : ∀ a, ∃ b, e b = T (e a) ∧ f b = T (f a))
    (ha : ∀ a, ∃ b, e b = T.adjoint (e a) ∧ f b = T.adjoint (f a))
    (x : WithLp 2 (H × H)) :
    (complexGraphClosure e f).starProjection (hilbertPairDiagonal T x) =
      hilbertPairDiagonal T ((complexGraphClosure e f).starProjection x) := by
  apply starProjection_commutes_of_invariant
  · exact complexGraphClosure_invariant e f T h
  · rw [hilbertPairDiagonal_adjoint]
    exact complexGraphClosure_invariant e f T.adjoint ha

#print axioms hilbertPairInl
#print axioms hilbertPairInr
#print axioms hilbertPairDiagonal
#print axioms hilbertPairDiagonal_adjoint
#print axioms complexGraphEmbedding
#print axioms complexGraphClosure
#print axioms complexGraphClosure_complete
#print axioms complexGraphEmbedding_mem
#print axioms complexGraphClosure_invariant
#print axioms complexGraphClosure_rotated_orthogonal
#print axioms complexGraphClosure_projection_rotated
#print axioms complexGraphClosure_projection_commutes
end
end TGLV350.Regular
