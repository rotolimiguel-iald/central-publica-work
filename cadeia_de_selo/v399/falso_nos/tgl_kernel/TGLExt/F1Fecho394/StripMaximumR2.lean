import Mathlib.Analysis.Complex.Hadamard
import Mathlib.Analysis.Complex.LocallyUniformLimit
import Mathlib.Tactic
/-! A common bound on both horizontal edges controls the whole closed strip.
The global boundedness premise is essential to the three-lines argument. -/
set_option autoImplicit false
noncomputable section
open Complex Complex.HadamardThreeLines Set
namespace F1Fecho.StripMaximum

def strip : Set ℂ := {z | 0<z.im ∧ z.im<1}
def closedStrip : Set ℂ := {z | 0≤z.im ∧ z.im≤1}

theorem norm_le_edge_bound {f : ℂ→ℂ} {C : ℝ} (hC : 0≤C)
    (hd : DiffContOnCl ℂ f strip)
    (hbound : ∃ M : ℝ, ∀ z ∈ closedStrip, ‖f z‖≤M)
    (hleft : ∀ z : ℂ, z.im=0 → ‖f z‖≤C)
    (hright : ∀ z : ℂ, z.im=1 → ‖f z‖≤C)
    {z : ℂ} (hz : z∈closedStrip) : ‖f z‖≤C := by
  let g : ℂ→ℂ := fun w => f (I*w)
  have hdg : DiffContOnCl ℂ g (verticalStrip 0 1) := by
    apply hd.comp (differentiable_id.const_mul I).diffContOnCl
    intro w hw
    simpa [strip,verticalStrip,mul_im] using hw
  have hbg : BddAbove ((norm ∘ g) '' verticalClosedStrip 0 1) := by
    obtain ⟨M,hM⟩ := hbound
    refine ⟨M,?_⟩
    rintro a ⟨w,hw,rfl⟩
    exact hM (I*w) (by simpa [closedStrip,verticalClosedStrip] using hw)
  have hn := norm_le_interp_of_mem_verticalClosedStrip' (f:=g)
    (a:=C) (b:=C) (by norm_num : (0:ℝ)<1)
    (z:=-I*z) (by simpa [verticalClosedStrip,closedStrip] using hz) hdg hbg
    (fun w hw => hleft (I*w) (by simpa using hw))
    (fun w hw => hright (I*w) (by simpa using hw))
  have hp (x : ℝ) : C^(1-x)*C^x=C := by
    rw [← Real.rpow_add' hC (by ring_nf; norm_num : 1-x+x≠0)]
    simp
  have hzid : I * (-I*z)=z := by rw [←mul_assoc]; simp
  dsimp only [g] at hn
  rw [hzid] at hn
  simpa only [sub_zero,div_one,hp] using hn

end F1Fecho.StripMaximum
#print axioms F1Fecho.StripMaximum.norm_le_edge_bound
