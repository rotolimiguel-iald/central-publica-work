import TGLExt.F1Fecho394.FiniteCommutingEigenR3
import Mathlib.Analysis.InnerProductSpace.Spectrum
/-! Absence of common one-dimensional eigenspaces excludes finite invariant
subspaces and compact symmetric operators in the commutant. This is an
intermediate step toward the Fock no-fixed-vector field, not that field. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
namespace F1Fecho.NoFiniteInvariant
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem finite_invariant_eq_bot (A : ℝ → H →L[ℂ] H)
    (hstar : ∀ s, star (A s) = A (-s))
    (hcomm : ∀ s t, Commute (A s) (A t))
    (hnorm : ∀ s x, ‖A s x‖ = ‖x‖)
    (hno : ∀ x : H, (∀ s : ℝ, ∃ c : ℂ, ‖c‖ = 1 ∧ A s x = c • x) → x = 0)
    (S : Submodule ℂ H) [FiniteDimensional ℂ S]
    (hInv : ∀ s x, x ∈ S → A s x ∈ S) : S = ⊥ := by
  by_contra hn
  letI : Nontrivial S := Submodule.nontrivial_iff_ne_bot.mpr hn
  letI : CompleteSpace S := FiniteDimensional.complete ℂ S
  let L (s : ℝ) : S →L[ℂ] S := (A s).restrict (hInv s)
  have hLs (s) : star (L s) = L (-s) := by
    change (L s).adjoint = L (-s)
    symm
    apply (ContinuousLinearMap.eq_adjoint_iff _ _).mpr
    intro x y
    change inner ℂ (A (-s) (x:H)) (y:H) = inner ℂ (x:H) (A s (y:H))
    rw [← hstar s]
    exact ContinuousLinearMap.adjoint_inner_left _ _ _
  have hLc (s t) : Commute (L s) (L t) := by
    apply ContinuousLinearMap.ext
    intro x
    apply Subtype.ext
    exact congrArg (fun B : H →L[ℂ] H => B (x:H)) (hcomm s t).eq
  obtain ⟨x,hx,hxe⟩ := FiniteCommonEigen.exists_common_eigenvector L hLs hLc
  have hxH : (x:H) ≠ 0 := fun h => hx (Subtype.ext h)
  apply hxH
  apply hno
  intro s
  obtain ⟨c,hc⟩ := hxe s
  have hcH : A s (x:H) = c • (x:H) := congrArg Subtype.val hc
  refine ⟨c,?_,hcH⟩
  have h := congrArg norm hcH
  rw [hnorm,norm_smul] at h
  have hp : 0 < ‖(x:H)‖ := norm_pos_iff.mpr hxH
  nlinarith

theorem compact_symmetric_commutant_eq_zero (A : ℝ → H →L[ℂ] H)
    (hstar : ∀ s, star (A s) = A (-s))
    (hcomm : ∀ s t, Commute (A s) (A t))
    (hnorm : ∀ s x, ‖A s x‖ = ‖x‖)
    (hno : ∀ x : H, (∀ s : ℝ, ∃ c : ℂ, ‖c‖ = 1 ∧ A s x = c • x) → x = 0)
    (B : H →L[ℂ] H) (hB : IsCompactOperator B) (hs : B.IsSymmetric)
    (hBA : ∀ s, Commute B (A s)) : B = 0 := by
  apply (ContinuousLinearMap.eq_zero_of_forall_hasEigenvalue_eq_zero hB hs).mp
  intro μ hμ
  by_contra hμ0
  let S := Module.End.eigenspace B.toLinearMap μ
  letI : FiniteDimensional ℂ S := ContinuousLinearMap.finite_dimensional_eigenspace hB μ hμ0
  have hInv (s : ℝ) (x : H) (hx : x ∈ S) : A s x ∈ S := by
    apply Module.End.mem_eigenspace_iff.mpr
    have hx' := Module.End.mem_eigenspace_iff.mp hx
    have hc := congrArg (fun L : H →L[ℂ] H => L x) (hBA s).eq
    change B (A s x) = A s (B x) at hc
    change B x = μ • x at hx'
    change B (A s x) = μ • A s x
    rw [hc,hx',map_smul]
  have hS := finite_invariant_eq_bot A hstar hcomm hnorm hno S hInv
  exact hμ (by exact hS)

end F1Fecho.NoFiniteInvariant
#print axioms F1Fecho.NoFiniteInvariant.finite_invariant_eq_bot
#print axioms F1Fecho.NoFiniteInvariant.compact_symmetric_commutant_eq_zero
