import TGLExt.F1Fecho394.TensorContractionPropertiesR3
import TGLExt.F1Fecho394.UnitaryNoFiniteInvariantR1
/-! A unitary representation without common projective eigenvectors has no
invariant vector in its tensor product with any unitary family. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open UniformSpace
open scoped TensorProduct
namespace F1Fecho.TensorNoFixed
open F1Fecho.TensorContraction
variable {E G : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
  [NormedAddCommGroup G] [InnerProductSpace ℂ G]

theorem conjugate_no_eigen (J : E ≃ₗᵢ⋆[ℂ] E) (u : ℝ → E ≃ₗᵢ[ℂ] E)
    (hno : ∀ x : E, (∀ s : ℝ, ∃ c : ℂ, ‖c‖ = 1 ∧ u s x = c • x) → x = 0)
    (x : E) (hx : ∀ s : ℝ, ∃ c : ℂ, ‖c‖ = 1 ∧ conjugate J (u s) x = c • x) : x = 0 := by
  apply J.injective
  rw [map_zero]
  apply hno
  intro s
  obtain ⟨c,hc,he⟩ := hx s
  refine ⟨star c,by simpa using hc,?_⟩
  have h := congrArg J he
  simpa only [J_conjugate,J.map_smulₛₗ,starRingEnd_apply] using h

theorem tensor_fixed_eq_zero (J : E ≃ₗᵢ⋆[ℂ] E) (u : ℝ → E ≃ₗᵢ[ℂ] E)
    (h0 : u 0 = LinearIsometryEquiv.refl ℂ E)
    (hadd : ∀ s t, u (s+t) = (u t).trans (u s))
    (hno : ∀ x : E, (∀ s : ℝ, ∃ c : ℂ, ‖c‖ = 1 ∧ u s x = c • x) → x = 0)
    (v : ℝ → G ≃ₗᵢ[ℂ] G) (z : Completion (E ⊗[ℂ] G))
    (hz : ∀ s, tensorAction (u s) (v s) z = z) : z = 0 := by
  apply eq_zero_of_reduced_eq_zero J z
  apply F1Fecho.UnitaryNoFiniteInvariant.compact_symmetric_commutant_eq_zero
    (fun s => conjugate J (u s)) ?_ ?_ (conjugate_no_eigen J u hno)
    (reduced J z) (reduced_compact J z) (reduced_symmetric J z)
    (fun s => reduced_commutes J (u s) (v s) z (hz s))
  · ext x
    simp [conjugate,h0]
  · intro s t
    ext x
    simp [conjugate,hadd]

end F1Fecho.TensorNoFixed
#print axioms F1Fecho.TensorNoFixed.conjugate_no_eigen
#print axioms F1Fecho.TensorNoFixed.tensor_fixed_eq_zero
