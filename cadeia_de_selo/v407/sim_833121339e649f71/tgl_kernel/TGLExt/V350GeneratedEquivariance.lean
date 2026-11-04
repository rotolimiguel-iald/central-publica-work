import TGLExt.V350RegularGeneratedAlgebra

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- An actual star-algebra equivalence transports the star commutant. -/
theorem centralizer_transport (e : (H →L[ℂ] H) ≃⋆ₐ[ℂ] (H →L[ℂ] H))
    (S : Set (H →L[ℂ] H)) (B : H →L[ℂ] H) :
    e B ∈ StarSubalgebra.centralizer ℂ (e '' S) ↔ B ∈ StarSubalgebra.centralizer ℂ S := by
  rw [StarSubalgebra.mem_centralizer_iff, StarSubalgebra.mem_centralizer_iff]
  constructor
  · intro h A hA
    have hh := h (e A) ⟨A, hA, rfl⟩
    constructor
    · apply e.injective
      change e (A * B) = e (B * A)
      simpa only [map_mul] using hh.1
    · apply e.injective
      change e (star A * B) = e (B * star A)
      simpa only [map_mul, map_star] using hh.2
  · intro h A hA
    rcases hA with ⟨C, hC, rfl⟩
    have hh := h C hC
    constructor
    · simpa only [map_mul] using congrArg e hh.1
    · simpa only [map_mul, map_star] using congrArg e hh.2

theorem centralizer_image (e : (H →L[ℂ] H) ≃⋆ₐ[ℂ] (H →L[ℂ] H))
    (S : Set (H →L[ℂ] H)) :
    e '' ((StarSubalgebra.centralizer ℂ S) : Set (H →L[ℂ] H)) =
      ((StarSubalgebra.centralizer ℂ (e '' S)) : Set (H →L[ℂ] H)) := by
  ext B
  constructor
  · rintro ⟨A, hA, rfl⟩
    exact (centralizer_transport e S A).mpr hA
  · intro hB
    change B ∈ StarSubalgebra.centralizer ℂ (e '' S) at hB
    refine ⟨e.symm B, ?_, e.apply_symm_apply B⟩
    apply (centralizer_transport e S (e.symm B)).mp
    simpa only [e.apply_symm_apply] using hB

/-- Bicommutant generation is preserved, with no topological closure assumption. -/
theorem generated_transport (e : (H →L[ℂ] H) ≃⋆ₐ[ℂ] (H →L[ℂ] H))
    (S : Set (H →L[ℂ] H)) (A : H →L[ℂ] H) :
    e A ∈ generatedAlgebra (e '' S) ↔ A ∈ generatedAlgebra S := by
  change e A ∈ StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ (e '' S)) : Set (H →L[ℂ] H)) ↔ _
  rw [← centralizer_image e S]
  exact centralizer_transport e _ A

theorem generated_maps_into (e : (H →L[ℂ] H) ≃⋆ₐ[ℂ] (H →L[ℂ] H))
    (S : Set (H →L[ℂ] H)) (hS : ∀ A ∈ S, e A ∈ generatedAlgebra S)
    {A : H →L[ℂ] H} (hA : A ∈ generatedAlgebra S) : e A ∈ generatedAlgebra S := by
  have hmin : generatedAlgebra (e '' S) ≤ generatedAlgebra S := by
    apply generated_minimal
    rintro _ ⟨B, hB, rfl⟩
    exact hS B hB
  exact hmin ((generated_transport e S A).mpr hA)

/-- Restrictions require both forward and inverse preservation of the generators. -/
def generatedAutomorphism (e : (H →L[ℂ] H) ≃⋆ₐ[ℂ] (H →L[ℂ] H))
    (S : Set (H →L[ℂ] H))
    (hS : ∀ A ∈ S, e A ∈ generatedAlgebra S)
    (hSi : ∀ A ∈ S, e.symm A ∈ generatedAlgebra S) :
    (generatedAlgebra S).toStarSubalgebra ≃⋆ₐ[ℂ] (generatedAlgebra S).toStarSubalgebra where
  toFun A := ⟨e A, generated_maps_into e S hS A.property⟩
  invFun A := ⟨e.symm A, generated_maps_into e.symm S hSi A.property⟩
  left_inv A := Subtype.ext (e.symm_apply_apply A)
  right_inv A := Subtype.ext (e.apply_symm_apply A)
  map_mul' A B := Subtype.ext (e.map_mul A B)
  map_add' A B := Subtype.ext (e.map_add A B)
  map_smul' c A := Subtype.ext (e.map_smul' c (A : H →L[ℂ] H))
  map_star' A := Subtype.ext (map_star e (A : H →L[ℂ] H))

theorem generatedAutomorphism_apply (e : (H →L[ℂ] H) ≃⋆ₐ[ℂ] (H →L[ℂ] H))
    (S : Set (H →L[ℂ] H))
    (hS : ∀ A ∈ S, e A ∈ generatedAlgebra S)
    (hSi : ∀ A ∈ S, e.symm A ∈ generatedAlgebra S)
    (A : (generatedAlgebra S).toStarSubalgebra) :
    ((generatedAutomorphism e S hS hSi A) : H →L[ℂ] H) = e A := rfl

#print axioms generated_transport
#print axioms generatedAutomorphism
end
end TGLV350.Regular
