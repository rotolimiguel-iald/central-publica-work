import TGLExt.V350ReducingBicommutantLift

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable {H K A : Type}
  [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
  [Semiring A] [StarRing A] [Algebra ℂ A]

theorem starRepresentation_bicommutant_commutes
    (ρ : A →⋆ₐ[ℂ] (H →L[ℂ] H)) (B : H →L[ℂ] H)
    (hB : B ∈ generatedAlgebra (Set.range ρ))
    (Q : H →L[ℂ] H) (hQ : ∀ a, Commute Q (ρ a)) : Commute B Q := by
  have hc : Q ∈ StarSubalgebra.centralizer ℂ (Set.range ρ) := by
    rw [StarSubalgebra.mem_centralizer_iff]
    rintro _ ⟨a,rfl⟩
    refine ⟨(hQ a).eq.symm,?_⟩
    rw [← map_star]
    exact (hQ (star a)).eq.symm
  change B ∈ StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ (Set.range ρ)) : Set (H →L[ℂ] H)) at hB
  exact (((StarSubalgebra.mem_centralizer_iff ℂ).mp hB) Q hc).1.symm

/-- Faithful reducing restriction is proved bicommutant closed through an actual
separating vector and a norm-controlled ambient lift. -/
theorem mem_generated_restriction_iff
    (M : VonNeumannAlgebra H) (S : Submodule ℂ H) [CompleteSpace S]
    (hS : ∀ a : M.toStarSubalgebra, ∀ x ∈ S, a.val x ∈ S)
    (v : S) (hsep : ∀ A ∈ M, A v.val = 0 → A = 0) (B : S →L[ℂ] S) :
    B ∈ generatedAlgebra (Set.range (reducingStarRepresentation M.toStarSubalgebra.subtype S hS)) ↔
      ∃ a : M.toStarSubalgebra,
        B = reducingStarRepresentation M.toStarSubalgebra.subtype S hS a := by
  constructor
  · intro hB
    obtain ⟨a,ha,_⟩ := reducingBicommutant_has_preimage M S hS B
      (starRepresentation_bicommutant_commutes _ B hB) v hsep
    exact ⟨a,ha.symm⟩
  · rintro ⟨a,rfl⟩
    exact generator_mem (Set.mem_range_self a)

/-- Transport between different Hilbert spaces; no same-space identification is implicit. -/
theorem starEquiv_centralizer_transport
    (e : (H →L[ℂ] H) ≃⋆ₐ[ℂ] (K →L[ℂ] K))
    (S : Set (H →L[ℂ] H)) (B : H →L[ℂ] H) :
    e B ∈ StarSubalgebra.centralizer ℂ (e '' S) ↔
      B ∈ StarSubalgebra.centralizer ℂ S := by
  rw [StarSubalgebra.mem_centralizer_iff,StarSubalgebra.mem_centralizer_iff]
  constructor
  · intro h A hA
    have hh := h (e A) ⟨A,hA,rfl⟩
    constructor
    · apply e.injective
      change e (A * B) = e (B * A)
      simpa only [map_mul] using hh.1
    · apply e.injective
      change e (star A * B) = e (B * star A)
      simpa only [map_mul,map_star] using hh.2
  · intro h A hA
    rcases hA with ⟨C,hC,rfl⟩
    have hh := h C hC
    constructor
    · simpa only [map_mul] using congrArg e hh.1
    · simpa only [map_mul,map_star] using congrArg e hh.2

theorem starEquiv_centralizer_image
    (e : (H →L[ℂ] H) ≃⋆ₐ[ℂ] (K →L[ℂ] K)) (S : Set (H →L[ℂ] H)) :
    e '' ((StarSubalgebra.centralizer ℂ S) : Set (H →L[ℂ] H)) =
      ((StarSubalgebra.centralizer ℂ (e '' S)) : Set (K →L[ℂ] K)) := by
  ext B
  constructor
  · rintro ⟨A,hA,rfl⟩
    exact (starEquiv_centralizer_transport e S A).mpr hA
  · intro hB
    change B ∈ StarSubalgebra.centralizer ℂ (e '' S) at hB
    refine ⟨e.symm B,?_,e.apply_symm_apply B⟩
    apply (starEquiv_centralizer_transport e S (e.symm B)).mp
    simpa only [e.apply_symm_apply] using hB

theorem starEquiv_generated_transport
    (e : (H →L[ℂ] H) ≃⋆ₐ[ℂ] (K →L[ℂ] K))
    (S : Set (H →L[ℂ] H)) (B : H →L[ℂ] H) :
    e B ∈ generatedAlgebra (e '' S) ↔ B ∈ generatedAlgebra S := by
  change e B ∈ StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ (e '' S)) : Set (K →L[ℂ] K)) ↔ _
  rw [← starEquiv_centralizer_image e S]
  exact starEquiv_centralizer_transport e _ B

#print axioms starRepresentation_bicommutant_commutes
#print axioms mem_generated_restriction_iff
#print axioms starEquiv_centralizer_transport
#print axioms starEquiv_centralizer_image
#print axioms starEquiv_generated_transport
end
end TGLV350.Regular
