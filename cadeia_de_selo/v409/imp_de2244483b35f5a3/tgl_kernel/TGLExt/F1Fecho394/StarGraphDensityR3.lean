import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.InnerProductSpace.Dual
import Mathlib.Algebra.Star.Subalgebra
import Mathlib.Analysis.LocallyConvex.SeparatingDual
import Mathlib.Analysis.Normed.Group.Quotient
import Mathlib.Topology.Algebra.Module.ContinuousLinearMap.Quotient
/-! Real graph closure of an algebra-vector pair from simultaneous two-vector
approximation. The two-vector premise remains explicit here; a separate
bicommutant theorem must discharge it. No equality of Tomita operators is
asserted by this generic module. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open Filter Topology
namespace F1Fecho.StarGraphDensity

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
local instance : InnerProductSpace ℝ H := InnerProductSpace.rclikeToReal ℂ H

def starGraph (A : StarSubalgebra ℂ (H →L[ℂ] H)) (Ω : H) : Submodule ℝ (H × H) where
  carrier := {p | ∃ b ∈ A, p = (b Ω, (star b) Ω)}
  zero_mem' := by
    refine ⟨0,A.zero_mem,?_⟩
    simp only [star_zero,ContinuousLinearMap.zero_apply]
    rfl
  add_mem' := by
    rintro p q ⟨b,hb,rfl⟩ ⟨c,hc,rfl⟩
    refine ⟨b+c,A.add_mem hb hc,?_⟩
    simp
  smul_mem' := by
    rintro t p ⟨b,hb,rfl⟩
    refine ⟨(t:ℂ) • b,A.smul_mem hb (t:ℂ),?_⟩
    change ((t:ℂ) • b Ω,(t:ℂ) • (star b) Ω) = _
    simp

theorem mem_starGraph (A : StarSubalgebra ℂ (H →L[ℂ] H)) (Ω : H) (p : H × H) :
    p ∈ starGraph A Ω ↔ ∃ b ∈ A, p = (b Ω,(star b) Ω) := Iff.rfl

private theorem mem_closed_of_real_functionals {E : Type*}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    (L : Submodule ℝ E) (hL : IsClosed (L : Set E)) (x : E)
    (hx : ∀ l : E →L[ℝ] ℝ, (∀ y ∈ L, l y = 0) → l x = 0) : x ∈ L := by
  letI : IsClosed (L : Set E) := hL
  by_contra hn
  have hq : L.mkQL x ≠ 0 := by
    intro h
    exact hn ((Submodule.Quotient.mk_eq_zero L).mp h)
  obtain ⟨l,hl⟩ := SeparatingDual.exists_ne_zero (R := ℝ) hq
  apply hl
  apply hx (l.comp L.mkQL)
  intro y hy
  change l (L.mkQL y) = 0
  have h : L.mkQL y = 0 := (Submodule.Quotient.mk_eq_zero L).mpr hy
  rw [h,map_zero]

private theorem real_functional_pair (l : (H × H) →L[ℝ] ℝ) :
    ∃ v w : H, ∀ x y : H, l (x,y) = inner ℝ v x + inner ℝ w y := by
  let v := (InnerProductSpace.toDual ℝ H).symm (l.comp (ContinuousLinearMap.inl ℝ H H))
  let w := (InnerProductSpace.toDual ℝ H).symm (l.comp (ContinuousLinearMap.inr ℝ H H))
  refine ⟨v,w,?_⟩
  intro x y
  change l (x,y) = inner ℝ ((InnerProductSpace.toDual ℝ H).symm _) x +
    inner ℝ ((InnerProductSpace.toDual ℝ H).symm _) y
  rw [InnerProductSpace.toDual_symm_apply,InnerProductSpace.toDual_symm_apply]
  change l (x,y) = l (x,0) + l (0,y)
  rw [← map_add]
  congr 1
  exact Prod.ext (add_zero x).symm (zero_add y).symm

theorem real_inner_star_swap (b : H →L[ℂ] H) (Ω w : H) :
    inner ℝ w ((star b) Ω) = inner ℝ Ω (b w) := by
  change (inner ℂ w ((star b) Ω)).re = (inner ℂ Ω (b w)).re
  rw [ContinuousLinearMap.star_eq_adjoint,ContinuousLinearMap.adjoint_inner_right]
  exact inner_re_symm (𝕜 := ℂ) (b w) Ω

/-- Density is required only for the simultaneous images of two vectors.
The conclusion is closure in the real graph topology on both coordinates. -/
theorem star_pair_mem_real_closure_of_two_vector_density
    (A : StarSubalgebra ℂ (H →L[ℂ] H)) (a : H →L[ℂ] H) (Ω : H)
    (h_two : ∀ x y : H, (a x,a y) ∈
      closure {p : H × H | ∃ b ∈ A, p = (b x,b y)}) :
    (a Ω,(star a) Ω) ∈ (starGraph A Ω).topologicalClosure := by
  apply mem_closed_of_real_functionals _ (starGraph A Ω).isClosed_topologicalClosure
  intro l hl
  obtain ⟨v,w,hvw⟩ := real_functional_pair l
  let g : H × H → ℝ := fun p => inner ℝ v p.1 + inner ℝ Ω p.2
  have hg : Continuous g := by fun_prop
  have hzero : ∀ b ∈ A, g (b Ω,b w) = 0 := by
    intro b hb
    have h := hl (b Ω,(star b) Ω) ((starGraph A Ω).le_topologicalClosure ⟨b,hb,rfl⟩)
    rw [hvw,real_inner_star_swap] at h
    exact h
  have hcl : closure {p : H × H | ∃ b ∈ A, p = (b Ω,b w)} ⊆ {p | g p = 0} := by
    apply closure_minimal
    · rintro p ⟨b,hb,rfl⟩
      exact hzero b hb
    · exact isClosed_eq hg continuous_const
  have ha := hcl (h_two Ω w)
  rw [hvw,real_inner_star_swap]
  exact ha

theorem star_pair_mem_set_closure_of_two_vector_density
    (A : StarSubalgebra ℂ (H →L[ℂ] H)) (a : H →L[ℂ] H) (Ω : H)
    (h_two : ∀ x y : H, (a x,a y) ∈
      closure {p : H × H | ∃ b ∈ A, p = (b x,b y)}) :
    (a Ω,(star a) Ω) ∈ closure {p : H × H | ∃ b ∈ A, p = (b Ω,(star b) Ω)} := by
  have h := star_pair_mem_real_closure_of_two_vector_density A a Ω h_two
  change (a Ω,(star a) Ω) ∈ (starGraph A Ω).topologicalClosure at h
  change (a Ω,(star a) Ω) ∈ closure (starGraph A Ω : Set (H × H))
  rw [← Submodule.topologicalClosure_coe]
  exact h

end F1Fecho.StarGraphDensity
#print axioms F1Fecho.StarGraphDensity.star_pair_mem_real_closure_of_two_vector_density
#print axioms F1Fecho.StarGraphDensity.star_pair_mem_set_closure_of_two_vector_density
