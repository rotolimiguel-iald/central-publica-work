import TGLExt.F1Fecho394.LpIntervalTotalityR3
/-! Interval generators from any total vector family; no separability assumption. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.LpIntervalTotalVectors
open MeasureTheory
open F1Fecho.LpIntervalTotality
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
theorem closed_submodule_eq_top_of_total
    (S : Submodule ℂ (Lp H 2 (volume : Measure ℝ)))
    (hS : IsClosed (S : Set (Lp H 2 (volume : Measure ℝ))))
    (W : Set H) (hW : ∀ v : H, (∀ w∈W, inner ℂ v w=0) → v=0)
    (hi : ∀ a b w, w∈W → intervalVector a b w ∈ S) : S=⊤ := by
  letI : CompleteSpace S := hS.completeSpace_coe
  apply Submodule.orthogonal_eq_bot_iff.mp
  apply le_antisymm ?_ bot_le
  intro f hf
  change f=0
  have hI (a b : ℝ) : (∫ t in Set.Ioc a b, f t)=0 := by
    apply hW
    intro w hw
    have hh := Submodule.inner_right_of_mem_orthogonal (hi a b w hw) hf
    rw [intervalVector_inner] at hh
    exact inner_eq_zero_symm.mp hh
  apply vector_eq_zero_of_intervals f
  intro a b
  simp only [intervalIntegral,hI,sub_self]
end F1Fecho.LpIntervalTotalVectors
#print axioms F1Fecho.LpIntervalTotalVectors.closed_submodule_eq_top_of_total
