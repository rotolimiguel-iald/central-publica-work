import Mathlib.Analysis.InnerProductSpace.Positive
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Order
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic
import Mathlib.Analysis.Normed.Operator.Completeness
import Mathlib.Topology.Order.MonotoneConvergence
import Mathlib.Topology.MetricSpace.Cauchy
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

set_option autoImplicit false
set_option maxHeartbeats 1600000

namespace ChatgptAudit.Expectation047

open Filter Set
open scoped Topology ComplexOrder

noncomputable section

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The scalar quadratic reading of a bounded operator. -/
def operatorQuadratic (A : H →L[ℂ] H) (v : H) : ℝ :=
  (inner ℂ v (A v)).re

/-- A positive operator satisfies the quadratic order estimate. -/
theorem positive_square_le_norm_smul (D : H →L[ℂ] H) (hD : 0 ≤ D) :
    D * D ≤ ‖D‖ • D := by
  let S := CFC.sqrt D
  have hS : S * S = D := CFC.sqrt_mul_sqrt_self D hD
  have hSstar : star S = S := (IsSelfAdjoint.of_nonneg (CFC.sqrt_nonneg D)).star_eq
  have hc := CStarAlgebra.star_left_conjugate_le_norm_smul
    (a := S) (b := D) (IsSelfAdjoint.of_nonneg hD)
  rw [hSstar, hS] at hc
  have he : S * D * S = D * D := by
    rw [← hS]
    simp only [mul_assoc]
  rwa [he] at hc

/-- The estimate that converts scalar monotone convergence to strong Cauchy convergence. -/
theorem positive_apply_norm_sq_le (D : H →L[ℂ] H) (hD : 0 ≤ D) (v : H) :
    ‖D v‖ ^ 2 ≤ ‖D‖ * operatorQuadratic D v := by
  have hp := (ContinuousLinearMap.nonneg_iff_isPositive D).mp hD
  have hi := ((ContinuousLinearMap.le_def (D * D) (‖D‖ • D)).mp
    (positive_square_le_norm_smul D hD)).re_inner_nonneg_right v
  have he : (inner ℂ v ((D * D) v)).re = ‖D v‖ ^ 2 := by
    change (inner ℂ v (D (D v))).re = _
    rw [← hp.inner_left_eq_inner_right v (D v), inner_self_eq_norm_sq]
  simp only [ContinuousLinearMap.sub_apply, inner_sub_right, map_sub,
    ContinuousLinearMap.smul_apply, inner_smul_real_right] at hi
  rw [he] at hi
  change 0 ≤ ‖D‖ * operatorQuadratic D v - ‖D v‖ ^ 2 at hi
  linarith

/-- Ordered positive increments have their norms controlled by their quadratic readings. -/
theorem positive_increment_norm_sq_le (A B : H →L[ℂ] H)
    (hA : 0 ≤ A) (hAB : A ≤ B) (C : ℝ) (hB : ‖B‖ ≤ C) (v : H) :
    ‖(B - A) v‖ ^ 2 ≤ C * (operatorQuadratic B v - operatorQuadratic A v) := by
  have hd : 0 ≤ B - A := sub_nonneg.mpr hAB
  have hn : ‖B - A‖ ≤ C :=
    (CStarAlgebra.norm_le_norm_of_nonneg_of_le hd (sub_le_self B hA)).trans hB
  have hq := ((ContinuousLinearMap.nonneg_iff_isPositive (B - A)).mp hd).re_inner_nonneg_right v
  calc
    ‖(B - A) v‖ ^ 2 ≤ ‖B - A‖ * operatorQuadratic (B - A) v :=
      positive_apply_norm_sq_le (B - A) hd v
    _ ≤ C * operatorQuadratic (B - A) v := mul_le_mul_of_nonneg_right hn hq
    _ = C * (operatorQuadratic B v - operatorQuadratic A v) := by
      simp only [operatorQuadratic, ContinuousLinearMap.sub_apply, inner_sub_right, map_sub]

/-- Positivity survives pointwise strong limits along any nontrivial filter. -/
theorem positive_of_strong_limit {ι : Type*} {l : Filter ι} [l.NeBot]
    (A : ι → H →L[ℂ] H) (B : H →L[ℂ] H)
    (hpos : ∀ᶠ i in l, 0 ≤ A i)
    (hlim : ∀ v, Tendsto (fun i => A i v) l (𝓝 (B v))) : 0 ≤ B := by
  rw [ContinuousLinearMap.nonneg_iff_isPositive, ContinuousLinearMap.isPositive_def]
  constructor
  · intro v w
    have hl := (hlim v).inner tendsto_const_nhds (g := fun _ => w)
    have hr := tendsto_const_nhds.inner (hlim w) (f := fun _ => v)
    apply tendsto_nhds_unique hl
    apply hr.congr'
    filter_upwards [hpos] with i hi
    exact ((ContinuousLinearMap.nonneg_iff_isPositive (A i)).mp hi).inner_left_eq_inner_right v w
  · intro v
    exact le_of_tendsto ((hlim v).inner tendsto_const_nhds (g := fun _ => v)).re
      (hpos.mono fun i hi =>
        ((ContinuousLinearMap.nonneg_iff_isPositive (A i)).mp hi).re_inner_nonneg_left v)

variable {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]

/-- The scalar readings form bounded monotone nets. -/
theorem monotone_quadratic_limit (A : ι → H →L[ℂ] H)
    (hmono : Monotone A) (C : ℝ) (hbound : ∀ i, ‖A i‖ ≤ C) (v : H) :
    Tendsto (fun i => operatorQuadratic (A i) v) atTop
      (𝓝 (⨆ i, operatorQuadratic (A i) v)) := by
  have hm : Monotone (fun i => operatorQuadratic (A i) v) := by
    intro i j hij
    have h := ((ContinuousLinearMap.le_def (A i) (A j)).mp (hmono hij)).re_inner_nonneg_right v
    simpa only [operatorQuadratic, ContinuousLinearMap.sub_apply, inner_sub_right,
      map_sub, sub_nonneg] using h
  have hb : BddAbove (Set.range (fun i => operatorQuadratic (A i) v)) := by
    refine ⟨C * ‖v‖ ^ 2, ?_⟩
    rintro _ ⟨i, rfl⟩
    calc
      operatorQuadratic (A i) v ≤ ‖inner ℂ v (A i v)‖ := Complex.re_le_norm _
      _ ≤ ‖v‖ * ‖A i v‖ := norm_inner_le_norm _ _
      _ ≤ ‖v‖ * (C * ‖v‖) := mul_le_mul_of_nonneg_left
        ((A i).le_of_opNorm_le (hbound i) v) (norm_nonneg v)
      _ = C * ‖v‖ ^ 2 := by ring
  exact tendsto_atTop_ciSup hm hb

/-- An arbitrary directed positive bounded net is Cauchy on every Hilbert vector. -/
theorem monotone_operator_vector_cauchy (A : ι → H →L[ℂ] H)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A)
    (C : ℝ) (hC : 0 ≤ C) (hbound : ∀ i, ‖A i‖ ≤ C) (v : H) :
    Cauchy (Filter.map (fun i => A i v) atTop) := by
  let q : ι → ℝ := fun i => operatorQuadratic (A i) v
  let qsup : ℝ := ⨆ i, q i
  have hb : BddAbove (Set.range q) := by
    refine ⟨C * ‖v‖ ^ 2, ?_⟩
    rintro _ ⟨i, rfl⟩
    calc
      q i ≤ ‖inner ℂ v (A i v)‖ := Complex.re_le_norm _
      _ ≤ ‖v‖ * ‖A i v‖ := norm_inner_le_norm _ _
      _ ≤ ‖v‖ * (C * ‖v‖) := mul_le_mul_of_nonneg_left
        ((A i).le_of_opNorm_le (hbound i) v) (norm_nonneg v)
      _ = C * ‖v‖ ^ 2 := by ring
  have ht : Tendsto q atTop (𝓝 qsup) := monotone_quadratic_limit A hmono C hbound v
  apply Metric.cauchy_iff.mpr
  refine ⟨inferInstance, ?_⟩
  intro eps heps
  let delta : ℝ := eps ^ 2 / (4 * (C + 1))
  have hden : 0 < 4 * (C + 1) := by positivity
  have hd : 0 < delta := div_pos (sq_pos_of_pos heps) hden
  have hid : delta * (4 * (C + 1)) = eps ^ 2 := div_mul_cancel₀ _ (ne_of_gt hden)
  have hcd : C * delta < (eps / 2) ^ 2 := by nlinarith
  have hn := (Metric.tendsto_nhds.mp ht) delta hd
  obtain ⟨N, hN⟩ := eventually_atTop.mp hn
  have hs (i k : ι) (hi : N ≤ i) (hik : i ≤ k) :
      ‖(A k - A i) v‖ < eps / 2 := by
    have hnear := hN i hi
    rw [Real.dist_eq] at hnear
    have hks : q k ≤ qsup := le_ciSup hb k
    have hdif : q k - q i < delta := by
      have hlo := (abs_lt.mp hnear).1
      linarith
    have hinc := positive_increment_norm_sq_le (A i) (A k) (hpos i) (hmono hik) C (hbound k) v
    have hlast : C * (q k - q i) < (eps / 2) ^ 2 :=
      lt_of_le_of_lt (mul_le_mul_of_nonneg_left hdif.le hC) hcd
    change ‖(A k - A i) v‖ ^ 2 ≤ C * (q k - q i) at hinc
    nlinarith [norm_nonneg ((A k - A i) v)]
  refine ⟨(fun i => A i v) '' Set.Ici N,
    Filter.image_mem_map (show Set.Ici N ∈ (atTop : Filter ι) from eventually_ge_atTop N), ?_⟩
  rintro _ ⟨i, hi, rfl⟩ _ ⟨j, hj, rfl⟩
  obtain ⟨k, hik, hjk⟩ := exists_ge_ge i j
  have h1 : dist (A i v) (A k v) < eps / 2 := by
    rw [dist_comm, dist_eq_norm]
    exact hs i k hi hik
  have h2 : dist (A k v) (A j v) < eps / 2 := by
    rw [dist_eq_norm]
    exact hs j k hj hjk
  exact lt_of_le_of_lt (dist_triangle (A i v) (A k v) (A j v)) (by linarith)

/-- Any existing strong limit of an increasing net is its least upper bound. -/
theorem monotone_strong_limit_isLUB (A : ι → H →L[ℂ] H)
    (hmono : Monotone A) (B : H →L[ℂ] H)
    (hlim : ∀ v, Tendsto (fun i => A i v) atTop (𝓝 (B v))) :
    IsLUB (Set.range A) B := by
  constructor
  · rintro _ ⟨j, rfl⟩
    apply sub_nonneg.mp
    apply positive_of_strong_limit (fun i => A i - A j) (B - A j)
    · exact (eventually_ge_atTop j).mono fun i hi => sub_nonneg.mpr (hmono hi)
    · intro v
      exact (hlim v).sub tendsto_const_nhds
  · intro D hD
    apply sub_nonneg.mp
    apply positive_of_strong_limit (fun i => D - A i) (D - B)
    · exact Eventually.of_forall fun i => sub_nonneg.mpr (hD (Set.mem_range_self i))
    · intro v
      exact tendsto_const_nhds.sub (hlim v)

/-- A positive increasing uniformly bounded net has a constructed strong limit and supremum. -/
theorem monotone_operator_limit (A : ι → H →L[ℂ] H)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A)
    (C : ℝ) (hC : 0 ≤ C) (hbound : ∀ i, ‖A i‖ ≤ C) :
    ∃ B : H →L[ℂ] H, 0 ≤ B ∧ ‖B‖ ≤ C ∧
      (∀ v, Tendsto (fun i => A i v) atTop (𝓝 (B v))) ∧
      IsLUB (Set.range A) B := by
  have hex (v : H) : ∃ z, Tendsto (fun i => A i v) atTop (𝓝 z) :=
    cauchy_map_iff_exists_tendsto.mp (monotone_operator_vector_cauchy A hpos hmono C hC hbound v)
  choose f hf using hex
  have hb : Bornology.IsBounded (Set.range A) := by
    refine isBounded_iff_forall_norm_le.mpr ⟨C, ?_⟩
    rintro _ ⟨i, rfl⟩
    exact hbound i
  let B : H →L[ℂ] H :=
    ContinuousLinearMap.ofTendstoOfBoundedRange f A (tendsto_pi_nhds.mpr hf) hb
  have hlim (v : H) : Tendsto (fun i => A i v) atTop (𝓝 (B v)) := hf v
  have hBpos : 0 ≤ B := positive_of_strong_limit A B (Eventually.of_forall hpos) hlim
  have hBbound : ‖B‖ ≤ C := by
    apply B.opNorm_le_bound hC
    intro v
    exact le_of_tendsto (hlim v).norm
      (Eventually.of_forall fun i => (A i).le_of_opNorm_le (hbound i) v)
  exact ⟨B, hBpos, hBbound, hlim, monotone_strong_limit_isLUB A hmono B hlim⟩

#print axioms operatorQuadratic
#print axioms positive_square_le_norm_smul
#print axioms positive_apply_norm_sq_le
#print axioms positive_increment_norm_sq_le
#print axioms positive_of_strong_limit
#print axioms monotone_quadratic_limit
#print axioms monotone_operator_vector_cauchy
#print axioms monotone_strong_limit_isLUB
#print axioms monotone_operator_limit

end
end ChatgptAudit.Expectation047
