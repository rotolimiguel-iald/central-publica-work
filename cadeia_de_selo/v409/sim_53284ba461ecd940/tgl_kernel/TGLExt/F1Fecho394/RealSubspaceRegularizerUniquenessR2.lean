import Mathlib.Analysis.InnerProductSpace.Projection.Submodule
import Mathlib.Topology.Algebra.Module.Basic
import Mathlib.Tactic

/-! A closed real subspace is determined by a dense complex span and genuine
bounded regularizers of its antilinear fixed-point equation. Ordinary complex
density alone is not used to infer equality. All regularizer obligations are
explicit; physical localization must supply them by separate terms. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open Filter
open scoped Topology
namespace F1Fecho.RealSubspaceRegularizerUniqueness
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem symmetrized_range_mem
    (M : Submodule ℝ H) (hM : IsClosed (M : Set H))
    (hd : (Submodule.span ℂ (M : Set H)).topologicalClosure=⊤)
    (R : H →L[ℂ] H) (B : H →SL[starRingEnd ℂ] H)
    (hR : ∀x∈M,R x∈M) (hB : ∀x∈M,B x=R x) (x : H) :
    R x+B x∈M := by
  have hs : ∀v∈Submodule.span ℂ (M : Set H),∀c:ℂ,R (c • v)+B (c • v)∈M := by
    intro v hv
    induction hv using Submodule.span_induction with
    | mem v hv =>
      intro c
      rw [map_smul,map_smulₛₗ,hB v hv,←add_smul]
      change (c+star c) • R v∈M
      rw [Complex.star_def,Complex.add_conj]
      exact M.smul_mem (2*c.re) (hR v hv)
    | zero => intro c; simp
    | add v w hv hw ihv ihw =>
      intro c
      simpa only [smul_add,map_add,add_add_add_comm] using M.add_mem (ihv c) (ihw c)
    | smul a v hv ih =>
      intro c
      simpa only [smul_smul] using ih (c*a)
  have hc : IsClosed {v : H | R v+B v∈M} := hM.preimage (R.continuous.add B.continuous)
  have hsub : (Submodule.span ℂ (M : Set H)).topologicalClosure ≤
      ({v : H | R v+B v∈M} : Set H) := by
    exact closure_minimal (fun v hv => by simpa using hs v hv 1) hc
  apply hsub
  rw [hd]
  trivial

theorem eq_of_regularizers
    (M K : Submodule ℝ H) (hM : IsClosed (M : Set H)) (hMK : M≤K)
    (hd : (Submodule.span ℂ (M : Set H)).topologicalClosure=⊤)
    (R : ℕ → H →L[ℂ] H) (B : ℕ → H →SL[starRingEnd ℂ] H)
    (hR : ∀n x,x∈M→R n x∈M)
    (hB : ∀n x,x∈K→B n x=R n x)
    (hlim : ∀x,Tendsto (fun n=>R n x) atTop (𝓝 x)) : M=K := by
  apply le_antisymm hMK
  intro x hx
  apply hM.mem_of_tendsto (hlim x)
  apply Filter.Eventually.of_forall
  intro n
  have hs := symmetrized_range_mem M hM hd (R n) (B n) (hR n)
    (fun y hy=>hB n y (hMK hy)) x
  rw [hB n x hx] at hs
  have hh := M.smul_mem (1/2:ℝ) hs
  have he : (1/2:ℝ) • (R n x+R n x)=R n x := by
    rw [←two_smul ℝ (R n x),smul_smul]
    norm_num
  rw [he] at hh
  exact hh

end F1Fecho.RealSubspaceRegularizerUniqueness
#print axioms F1Fecho.RealSubspaceRegularizerUniqueness.symmetrized_range_mem
#print axioms F1Fecho.RealSubspaceRegularizerUniqueness.eq_of_regularizers
