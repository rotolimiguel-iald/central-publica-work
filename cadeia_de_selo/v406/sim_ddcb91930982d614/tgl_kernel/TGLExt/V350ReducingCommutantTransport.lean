import TGLExt.V350ReducingStarRepresentation
import TGLExt.InvariantProjection

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable {A H : Type} [Semiring A] [StarRing A] [Algebra ℂ A]
  [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Extension by zero on the orthogonal complement, not an algebra homomorphism. -/
def reducingOperatorExtension (S : Submodule ℂ H) [CompleteSpace S]
    (T : S →L[ℂ] S) : H →L[ℂ] H :=
  S.subtypeL.comp (T.comp S.orthogonalProjectionOnto)

theorem reducing_projection_intertwines
    (ρ : A →⋆ₐ[ℂ] (H →L[ℂ] H)) (S : Submodule ℂ H) [CompleteSpace S]
    (h : ∀ a, ∀ v ∈ S, ρ a v ∈ S) (a : A) (x : H) :
    S.orthogonalProjectionOnto (ρ a x) =
      reducingStarRepresentation ρ S h a (S.orthogonalProjectionOnto x) := by
  apply Subtype.ext
  change S.starProjection (ρ a x) = ρ a (S.starProjection x)
  apply starProjection_commutes_of_invariant
  · exact h a
  · simpa only [Invariant,map_star,ContinuousLinearMap.star_eq_adjoint] using h (star a)

theorem reducingOperatorExtension_commutes_iff
    (ρ : A →⋆ₐ[ℂ] (H →L[ℂ] H)) (S : Submodule ℂ H) [CompleteSpace S]
    (h : ∀ a, ∀ v ∈ S, ρ a v ∈ S) (T : S →L[ℂ] S) (a : A) :
    Commute (reducingOperatorExtension S T) (ρ a) ↔
      Commute T (reducingStarRepresentation ρ S h a) := by
  constructor
  · intro hc
    ext1 v
    apply Subtype.ext
    change (T (reducingStarRepresentation ρ S h a v)).val = ρ a (T v).val
    have he := congrArg (fun B : H →L[ℂ] H => B v.val) hc.eq
    change (T (S.orthogonalProjectionOnto (ρ a v.val))).val =
      ρ a (T (S.orthogonalProjectionOnto v.val)).val at he
    rw [reducing_projection_intertwines ρ S h a] at he
    simpa only [Submodule.orthogonalProjectionOnto_mem_subspace_eq_self] using he
  · intro hc
    ext1 x
    change (T (S.orthogonalProjectionOnto (ρ a x))).val =
      ρ a (T (S.orthogonalProjectionOnto x)).val
    rw [reducing_projection_intertwines ρ S h a]
    exact congrArg Subtype.val
      (congrArg (fun B : S →L[ℂ] S => B (S.orthogonalProjectionOnto x)) hc.eq)

/-- Generator commutation transfers through a reducing restriction.
The ambient generation premise must be discharged for the actual representation. -/
theorem reducing_commutation_from_generators
    (ρ : A →⋆ₐ[ℂ] (H →L[ℂ] H)) (S : Submodule ℂ H) [CompleteSpace S]
    (h : ∀ a, ∀ v ∈ S, ρ a v ∈ S) (G : Set A)
    (hgen : ∀ T : H →L[ℂ] H,
      (∀ g ∈ G, Commute T (ρ g)) → ∀ a, Commute T (ρ a))
    (T : S →L[ℂ] S)
    (hT : ∀ g ∈ G, Commute T (reducingStarRepresentation ρ S h g)) :
    ∀ a, Commute T (reducingStarRepresentation ρ S h a) := by
  intro a
  apply (reducingOperatorExtension_commutes_iff ρ S h T a).mp
  apply hgen
  intro g hg
  exact (reducingOperatorExtension_commutes_iff ρ S h T g).mpr (hT g hg)

#print axioms reducingOperatorExtension
#print axioms reducing_projection_intertwines
#print axioms reducingOperatorExtension_commutes_iff
#print axioms reducing_commutation_from_generators
end
end TGLV350.Regular
