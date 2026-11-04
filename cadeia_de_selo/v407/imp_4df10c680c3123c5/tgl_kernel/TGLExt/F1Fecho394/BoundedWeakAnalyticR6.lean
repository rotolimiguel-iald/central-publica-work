import Mathlib.Analysis.Complex.LocallyUniformLimit
import Mathlib.Analysis.Calculus.DiffContOnCl
import Mathlib.Analysis.InnerProductSpace.Projection.Basic
import Mathlib.Tactic
/-! A uniformly bounded operator family is weakly analytic if all coefficients
on a total family are analytic. Closure follows from a uniform coefficient
estimate, not from a new analyticity premise for arbitrary vectors. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open Filter Set
open scoped Topology
namespace F1Fecho.BoundedWeakAnalytic
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

theorem coefficient_uniform_left (B : ℂ → H →L[ℂ] H) (U : Set ℂ)
    (hB : ∀ z ∈ U, ‖B z‖ ≤ 1) (v : H) (u : ℕ → H) (x : H)
    (hu : Tendsto u atTop (𝓝 x)) :
    TendstoUniformlyOn (fun n z => inner ℂ (u n) (B z v))
      (fun z => inner ℂ x (B z v)) atTop U := by
  apply Metric.tendstoUniformlyOn_iff.mpr
  intro ε hε
  have ht : Tendsto (fun n => ‖u n-x‖*‖v‖) atTop (𝓝 0) := by
    simpa using (hu.sub (tendsto_const_nhds (x := x))).norm.mul_const ‖v‖
  filter_upwards [ht.eventually (gt_mem_nhds hε)] with n hn
  intro z hz
  rw [dist_comm,dist_eq_norm,← inner_sub_left]
  calc
    _ ≤ ‖u n-x‖*‖B z v‖ := norm_inner_le_norm _ _
    _ ≤ ‖u n-x‖*‖v‖ := mul_le_mul_of_nonneg_left
      ((B z).le_opNorm v |>.trans (by nlinarith [hB z hz,norm_nonneg v])) (norm_nonneg _)
    _ < ε := hn

theorem coefficient_uniform_right (B : ℂ → H →L[ℂ] H) (U : Set ℂ)
    (hB : ∀ z ∈ U, ‖B z‖ ≤ 1) (v : H) (u : ℕ → H) (x : H)
    (hu : Tendsto u atTop (𝓝 x)) :
    TendstoUniformlyOn (fun n z => inner ℂ v (B z (u n)))
      (fun z => inner ℂ v (B z x)) atTop U := by
  apply Metric.tendstoUniformlyOn_iff.mpr
  intro ε hε
  have ht : Tendsto (fun n => ‖v‖*‖u n-x‖) atTop (𝓝 0) := by
    simpa using (hu.sub (tendsto_const_nhds (x := x))).norm.const_mul ‖v‖
  filter_upwards [ht.eventually (gt_mem_nhds hε)] with n hn
  intro z hz
  rw [dist_comm,dist_eq_norm,← inner_sub_right,← map_sub]
  calc
    _ ≤ ‖v‖*‖B z (u n-x)‖ := norm_inner_le_norm _ _
    _ ≤ ‖v‖*‖u n-x‖ := mul_le_mul_of_nonneg_left
      ((B z).le_opNorm _ |>.trans (by nlinarith [hB z hz,norm_nonneg (u n-x)])) (norm_nonneg _)
    _ < ε := hn

theorem closed_left (B : ℂ → H →L[ℂ] H) (U : Set ℂ) (hU : IsOpen U)
    (hB : ∀ z ∈ closure U, ‖B z‖ ≤ 1) (y : H) :
    IsClosed {x | DiffContOnCl ℂ (fun z => inner ℂ x (B z y)) U} := by
  apply isSeqClosed_iff_isClosed.mp
  intro u x hu hx
  have ht := coefficient_uniform_left B (closure U) hB y u x hx
  exact ⟨(ht.mono subset_closure).tendstoLocallyUniformlyOn.differentiableOn
    (Eventually.of_forall fun n => (hu n).differentiableOn) hU,
    ht.continuousOn (Filter.Eventually.frequently (Eventually.of_forall fun n => (hu n).continuousOn))⟩

theorem closed_right (B : ℂ → H →L[ℂ] H) (U : Set ℂ) (hU : IsOpen U)
    (hB : ∀ z ∈ closure U, ‖B z‖ ≤ 1) (y : H) :
    IsClosed {x | DiffContOnCl ℂ (fun z => inner ℂ y (B z x)) U} := by
  apply isSeqClosed_iff_isClosed.mp
  intro u x hu hx
  have ht := coefficient_uniform_right B (closure U) hB y u x hx
  exact ⟨(ht.mono subset_closure).tendstoLocallyUniformlyOn.differentiableOn
    (Eventually.of_forall fun n => (hu n).differentiableOn) hU,
    ht.continuousOn (Filter.Eventually.frequently (Eventually.of_forall fun n => (hu n).continuousOn))⟩

theorem of_total {I : Type*} (e : I → H)
    (he : (Submodule.span ℂ (range e)).topologicalClosure = ⊤)
    (B : ℂ → H →L[ℂ] H) (U : Set ℂ) (hU : IsOpen U)
    (hB : ∀ z ∈ closure U, ‖B z‖ ≤ 1)
    (ha : ∀ i j, DiffContOnCl ℂ (fun z => inner ℂ (e i) (B z (e j))) U) :
    ∀ x y : H, DiffContOnCl ℂ (fun z => inner ℂ x (B z y)) U := by
  have hd : Dense (Submodule.span ℂ (range e) : Set H) :=
    Submodule.dense_iff_topologicalClosure_eq_top.mpr he
  have hfirst (i : I) (y : H) : DiffContOnCl ℂ (fun z => inner ℂ (e i) (B z y)) U := by
    apply (closed_right B U hU hB (e i)).closure_subset_iff.mpr ?_ (hd y)
    intro y hy
    induction hy using Submodule.span_induction with
    | mem y hy => obtain ⟨j,rfl⟩ := hy; exact ha i j
    | zero => simpa only [Set.mem_setOf_eq,map_zero,inner_zero_right] using (diffContOnCl_const (𝕜 := ℂ) (s := U) (c := (0:ℂ)))
    | add y z hy hz ihy ihz => simpa only [Set.mem_setOf_eq,map_add,inner_add_right,Pi.add_def] using ihy.add ihz
    | smul c y hy ih => simpa only [Set.mem_setOf_eq,map_smul,inner_smul_right,Pi.smul_def,smul_eq_mul] using ih.const_smul c
  intro x y
  apply (closed_left B U hU hB y).closure_subset_iff.mpr ?_ (hd x)
  intro x hx
  induction hx using Submodule.span_induction with
  | mem x hx => obtain ⟨i,rfl⟩ := hx; exact hfirst i y
  | zero => simpa only [Set.mem_setOf_eq,inner_zero_left] using (diffContOnCl_const (𝕜 := ℂ) (s := U) (c := (0:ℂ)))
  | add x z hx hz ihx ihz => simpa only [Set.mem_setOf_eq,inner_add_left,Pi.add_def] using ihx.add ihz
  | smul c x hx ih => simpa only [Set.mem_setOf_eq,inner_smul_left,Pi.smul_def,smul_eq_mul] using ih.const_smul ((starRingEnd ℂ) c)

end F1Fecho.BoundedWeakAnalytic
#print axioms F1Fecho.BoundedWeakAnalytic.coefficient_uniform_left
#print axioms F1Fecho.BoundedWeakAnalytic.coefficient_uniform_right
#print axioms F1Fecho.BoundedWeakAnalytic.of_total
