import Mathlib.Analysis.InnerProductSpace.JointEigenspace
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Tactic
/-! A finite-dimensional common eigenvector lemma for the no-fixed-vector
construction. No Fock ergodicity is claimed by this auxiliary theorem. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
namespace F1Fecho.FiniteCommonEigen
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
  [CompleteSpace H] [FiniteDimensional ℂ H] [Nontrivial H]

def part (A : ℝ → H →L[ℂ] H) (i : ℝ × Bool) : H →L[ℂ] H :=
  if i.2 then (-Complex.I / 2) • (A i.1 - A (-i.1))
  else (1 / 2 : ℂ) • (A i.1 + A (-i.1))

theorem part_selfadjoint (A : ℝ → H →L[ℂ] H)
    (hA : ∀ s, star (A s) = A (-s)) (i : ℝ × Bool) :
    IsSelfAdjoint (part A i) := by
  rcases i with ⟨s,b⟩
  cases b
  · simp only [part,Bool.false_eq_true,if_false,isSelfAdjoint_iff,
      star_smul,star_add,hA,neg_neg]
    norm_num [Complex.star_def,add_comm]
  · simp only [part,if_true,isSelfAdjoint_iff,star_smul,star_sub,hA,neg_neg]
    have hc : star (-Complex.I / 2) = -(-Complex.I / 2) := by simp [Complex.star_def]; ring
    rw [hc,neg_smul,← smul_neg,neg_sub]

theorem part_commute (A : ℝ → H →L[ℂ] H)
    (hA : ∀ s t, Commute (A s) (A t)) (i j : ℝ × Bool) :
    Commute (part A i) (part A j) := by
  rcases i with ⟨s,b⟩
  rcases j with ⟨t,c⟩
  cases b <;> cases c <;> simp only [part,Bool.false_eq_true,if_false,if_true]
  · exact ((hA s t).add_right (hA s (-t))).add_left
      ((hA (-s) t).add_right (hA (-s) (-t))) |>.smul_left _ |>.smul_right _
  · exact ((hA s t).sub_right (hA s (-t))).add_left
      ((hA (-s) t).sub_right (hA (-s) (-t))) |>.smul_left _ |>.smul_right _
  · exact ((hA s t).add_right (hA s (-t))).sub_left
      ((hA (-s) t).add_right (hA (-s) (-t))) |>.smul_left _ |>.smul_right _
  · exact ((hA s t).sub_right (hA s (-t))).sub_left
      ((hA (-s) t).sub_right (hA (-s) (-t))) |>.smul_left _ |>.smul_right _

theorem parts_reconstruct (A : ℝ → H →L[ℂ] H) (s : ℝ) :
    part A (s,false) + Complex.I • part A (s,true) = A s := by
  simp only [part,Bool.false_eq_true,if_false,if_true,smul_smul]
  have hc : Complex.I * (-Complex.I / 2) = (1/2:ℂ) := by
    field_simp
    simp
  rw [hc,← smul_add]
  module

theorem exists_common_eigenvector (A : ℝ → H →L[ℂ] H)
    (hstar : ∀ s, star (A s) = A (-s))
    (hcomm : ∀ s t, Commute (A s) (A t)) :
    ∃ x : H, x ≠ 0 ∧ ∀ s : ℝ, ∃ c : ℂ, A s x = c • x := by
  let T : ℝ × Bool → H →ₗ[ℂ] H := fun i => (part A i).toLinearMap
  have hs (i) : (T i).IsSymmetric := (part_selfadjoint A hstar i).isSymmetric
  have hc : Pairwise (fun i j => Commute (T i) (T j)) := by
    intro i j hij
    exact congrArg ContinuousLinearMap.toLinearMap (part_commute A hcomm i j).eq
  have htop := LinearMap.IsSymmetric.iSup_iInf_eq_top_of_commute hs hc
  have hn : ∃ χ : (ℝ × Bool) → ℂ,
      (⨅ i, Module.End.eigenspace (T i) (χ i)) ≠ ⊥ := by
    by_contra! hn
    simp only [hn,iSup_bot] at htop
    exact bot_ne_top htop
  obtain ⟨χ,hχ⟩ := hn
  obtain ⟨x,hx,hx0⟩ := (Submodule.ne_bot_iff _).mp hχ
  refine ⟨x,hx0,fun s => ⟨χ (s,false) + Complex.I * χ (s,true),?_⟩⟩
  have h0 := Module.End.mem_eigenspace_iff.mp
    ((Submodule.mem_iInf _).mp hx (s,false))
  have h1 := Module.End.mem_eigenspace_iff.mp
    ((Submodule.mem_iInf _).mp hx (s,true))
  have he := congrArg (fun L : H →L[ℂ] H => L x) (parts_reconstruct A s)
  change part A (s,false) x + Complex.I • part A (s,true) x = A s x at he
  change part A (s,false) x = _ at h0
  change part A (s,true) x = _ at h1
  rw [h0,h1] at he
  rw [← he,smul_smul,add_smul]

end F1Fecho.FiniteCommonEigen
#print axioms F1Fecho.FiniteCommonEigen.exists_common_eigenvector
