import TGLExt.F1Fecho394.StarGraphDensityR3
import TGLExt.F1Fecho394.BicommutantTwoVectorR2
/-! The two-vector premise is discharged by the finite-amplification theorem.
The remaining premise is explicit membership in the operator bicommutant.
This module does not assert a Tomita identification for a concrete Fock net. -/
set_option autoImplicit false
noncomputable section
open Filter Topology
namespace F1Fecho.StarGraphDensity
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
local instance : InnerProductSpace ℝ H := InnerProductSpace.rclikeToReal ℂ H

theorem star_pair_mem_real_closure_of_bicommutant
    (A : StarSubalgebra ℂ (H →L[ℂ] H)) (a : H →L[ℂ] H) (Ω : H)
    (ha : ∀ b : H →L[ℂ] H, (∀ c ∈ A,b*c=c*b) → a*b=b*a) :
    (a Ω,(star a) Ω) ∈ (starGraph A Ω).topologicalClosure :=
  star_pair_mem_real_closure_of_two_vector_density A a Ω
    (fun x y => BicommutantTwoVector.two_vector_density A a ha x y)

theorem star_pair_mem_set_closure_of_bicommutant
    (A : StarSubalgebra ℂ (H →L[ℂ] H)) (a : H →L[ℂ] H) (Ω : H)
    (ha : ∀ b : H →L[ℂ] H, (∀ c ∈ A,b*c=c*b) → a*b=b*a) :
    (a Ω,(star a) Ω) ∈ closure {p : H × H | ∃ b ∈ A,p=(b Ω,(star b) Ω)} :=
  star_pair_mem_set_closure_of_two_vector_density A a Ω
    (fun x y => BicommutantTwoVector.two_vector_density A a ha x y)

/-- Any closed real graph containing the algebra-vector pairs also contains
the bicommutant-vector pair. No boundedness of the approximating operators is
claimed; the topology controls the two graph coordinates. -/
theorem closed_real_submodule_contains_bicommutant_pair
    (A : StarSubalgebra ℂ (H →L[ℂ] H)) (a : H →L[ℂ] H) (Ω : H)
    (ha : ∀ b : H →L[ℂ] H, (∀ c ∈ A,b*c=c*b) → a*b=b*a)
    (L : Submodule ℝ (H × H)) (hL : IsClosed (L : Set (H × H)))
    (hA : ∀ b ∈ A,(b Ω,(star b) Ω) ∈ L) : (a Ω,(star a) Ω) ∈ L := by
  have h := star_pair_mem_set_closure_of_bicommutant A a Ω ha
  apply (closure_minimal (t := (L : Set (H × H))) ?_ hL) h
  rintro p ⟨b,hb,rfl⟩
  exact hA b hb

end F1Fecho.StarGraphDensity
#print axioms F1Fecho.StarGraphDensity.star_pair_mem_real_closure_of_bicommutant
#print axioms F1Fecho.StarGraphDensity.star_pair_mem_set_closure_of_bicommutant
#print axioms F1Fecho.StarGraphDensity.closed_real_submodule_contains_bicommutant_pair
