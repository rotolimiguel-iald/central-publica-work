import TGLExt.V351ScalarRightActionAlgebra
import TGLExt.V350ContractionAdjointLimit

set_option autoImplicit false
set_option maxHeartbeats 2200000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt Filter MeasureTheory
open scoped Topology BigOperators
noncomputable section

private theorem average_commutes_regular (P : SiteProfile) (h t : ℝ) :
    regularUnitary P t * regularAverage P h =
      regularAverage P h * regularUnitary P t := by
  ext1 v
  change regularUnitary P t (regularAverage P h v) =
    regularAverage P h (regularUnitary P t v)
  rw [regularAverage_apply,regularAverage_apply]
  change regularUnitary P t (((h⁻¹ : ℝ) : ℂ) •
    ∫ s in 0..h, regularUnitary P s v) =
    ((h⁻¹ : ℝ) : ℂ) • ∫ s in 0..h, regularUnitary P s (regularUnitary P t v)
  rw [map_smul]
  congr 1
  rw [← (regularUnitary P t).intervalIntegral_comp_comm
    ((regular_strongly_continuous P v).intervalIntegrable 0 h)]
  apply intervalIntegral.integral_congr
  intro s _
  change regularUnitary P t (regularUnitary P s v) =
    regularUnitary P s (regularUnitary P t v)
  rw [← mul_apply_eq_comp,regular_mul,← mul_apply_eq_comp,regular_mul,add_comm t s]

/-- Exact partition of the existing strong integral, not a new integral. -/
private theorem average_partition (P : SiteProfile) (h : ℝ) (N : ℕ) :
    ((((N : ℝ)⁻¹ : ℝ) : ℂ) • ∑ k ∈ Finset.range N, regularUnitary P ((k : ℝ)*h)) *
      regularAverage P h = regularAverage P ((N : ℝ)*h) := by
  have hi (v : RegularHilbert (TowerHilbert P)) :
      (∑ k ∈ Finset.range N, regularUnitary P ((k : ℝ)*h))
        (∫ t in 0..h, regularUnitary P t v) =
      ∫ t in 0..((N : ℝ)*h), regularUnitary P t v := by
    rw [sum_apply]
    have he (k : ℕ) :
        regularUnitary P ((k : ℝ)*h) (∫ t in 0..h, regularUnitary P t v) =
          ∫ t in (k : ℝ)*h..((k+1 : ℕ) : ℝ)*h, regularUnitary P t v := by
      rw [← (regularUnitary P ((k : ℝ)*h)).intervalIntegral_comp_comm
        ((regular_strongly_continuous P v).intervalIntegrable 0 h)]
      have hp (t : ℝ) :
          regularUnitary P ((k : ℝ)*h) (regularUnitary P t v) =
            regularUnitary P (t+(k : ℝ)*h) v := by
        rw [← mul_apply_eq_comp,regular_mul,add_comm]
      simp_rw [hp]
      rw [intervalIntegral.integral_comp_add_right (fun s => regularUnitary P s v)]
      congr 1 <;> push_cast <;> ring
    simp_rw [he]
    have hs := intervalIntegral.sum_integral_adjacent_intervals
      (μ := volume) (f := fun s => regularUnitary P s v)
      (a := fun k : ℕ => (k : ℝ)*h) (n := N)
      (fun k _ => (regular_strongly_continuous P v).intervalIntegrable _ _)
    simpa only [Nat.cast_zero,zero_mul] using hs
  ext1 v
  change (((N : ℝ)⁻¹ : ℝ) : ℂ) •
    (∑ k ∈ Finset.range N, regularUnitary P ((k : ℝ)*h))
      (((h⁻¹ : ℝ) : ℂ) • (∫ t in 0..h, regularUnitary P t v)) =
    ((((N : ℝ)*h)⁻¹ : ℝ) : ℂ) •
      (∫ t in 0..((N : ℝ)*h), regularUnitary P t v)
  rw [map_smul,hi,smul_smul]
  congr 1
  simp only [mul_inv_rev,Complex.ofReal_mul,mul_comm]

private theorem finite_regular_average_norm (P : SiteProfile) (N : ℕ) (hN : 0 < N)
    (h : ℝ) :
    ‖((((N : ℝ)⁻¹ : ℝ) : ℂ) • ∑ k ∈ Finset.range N, regularUnitary P ((k : ℝ)*h))‖ ≤ 1 := by
  have hn : (0 : ℝ) < N := by exact_mod_cast hN
  rw [norm_smul,Complex.norm_real,Real.norm_eq_abs,abs_of_pos (inv_pos.mpr hn)]
  calc
    _ ≤ (N : ℝ)⁻¹ * ∑ k ∈ Finset.range N, (1 : ℝ) := by
      apply mul_le_mul_of_nonneg_left _ (inv_nonneg.mpr hn.le)
      exact (norm_sum_le _ _).trans (Finset.sum_le_sum fun k _ =>
        (regularIntegralFamily P).norm_bound ((k : ℝ)*h))
    _ = 1 := by simp [ne_of_gt hn]

/-- The existing average is a bounded strong-star limit of finite combinations
of regular unitaries in the already constructed right-identity algebra. -/
theorem regularAverage_polar_approximants (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ) :
    ∃ b : ℕ → (regularCoreAlgebra P).toStarSubalgebra,
      (∀ n, b n ∈ scalarPolarRightAlgebra P) ∧
      (∀ n, ‖(b n).val‖ ≤ 1) ∧
      (∀ v, Tendsto (fun n => (b n).val v) atTop (𝓝 (regularAverage P δ v))) ∧
      (∀ v, Tendsto (fun n => (star (b n)).val v) atTop
        (𝓝 (star (regularAverage P δ) v))) := by
  let d : ℕ → ℝ := fun n => δ/((n : ℝ)+1)
  let b : ℕ → (regularCoreAlgebra P).toStarSubalgebra := fun n =>
    ((((n : ℝ)+1)⁻¹ : ℝ) : ℂ) • ∑ k ∈ Finset.range (n+1),
      regularRightCoreElement P ((k : ℝ)*d n)
  have hb (n : ℕ) : b n ∈ scalarPolarRightAlgebra P := by
    apply (scalarPolarRightAlgebra P).smul_mem
    apply (scalarPolarRightAlgebra P).sum_mem
    intro k _
    exact scalarPolarRightAlgebra_regular_mem P _
  have hv (n : ℕ) : (b n).val =
      ((((n : ℝ)+1)⁻¹ : ℝ) : ℂ) • ∑ k ∈ Finset.range (n+1),
        regularUnitary P ((k : ℝ)*d n) := by
    change (regularCoreAlgebra P).toStarSubalgebra.subtype
      (((((n : ℝ)+1)⁻¹ : ℝ) : ℂ) • ∑ k ∈ Finset.range (n+1),
        regularRightCoreElement P ((k : ℝ)*d n)) = _
    rw [map_smul,map_sum]
    rfl
  have hn (n : ℕ) : ‖(b n).val‖ ≤ 1 := by
    rw [hv]
    simpa only [Nat.cast_add,Nat.cast_one] using
      finite_regular_average_norm P (n+1) (Nat.succ_pos n) (d n)
  have hdpos (n : ℕ) : 0 < d n := by dsimp [d]; positivity
  have hp (n : ℕ) : (b n).val * regularAverage P (d n) = regularAverage P δ := by
    have hx : ((n+1 : ℕ) : ℝ)*d n = δ := by dsimp [d]; push_cast; field_simp
    have ht := average_partition P (d n) (n+1)
    rw [hx] at ht
    rw [hv]
    simpa only [Nat.cast_add,Nat.cast_one] using ht
  have hc (n : ℕ) : (b n).val * regularAverage P (d n) =
      regularAverage P (d n) * (b n).val := by
    rw [hv,smul_mul_assoc,mul_smul_comm,Finset.sum_mul,Finset.mul_sum]
    congr 1
    exact Finset.sum_congr rfl fun k _ => average_commutes_regular P (d n) _
  have hd : Tendsto d atTop (𝓝[≠] (0 : ℝ)) := by
    apply tendsto_nhdsWithin_iff.mpr
    constructor
    · have ht : Tendsto (fun n : ℕ => δ*(1/((n : ℝ)+1))) atTop (𝓝 (δ*0)) :=
        tendsto_const_nhds.mul tendsto_one_div_add_atTop_nhds_zero_nat
      simpa only [d,mul_zero,div_eq_mul_inv,one_mul] using ht
    · exact Eventually.of_forall fun n => ne_of_gt (hdpos n)
  have hsmall (v : RegularHilbert (TowerHilbert P)) :
      Tendsto (fun n => regularAverage P (d n) v) atTop (𝓝 v) :=
    (regularAverage_tendsto_identity P v).comp hd
  have hsmallstar (v : RegularHilbert (TowerHilbert P)) :
      Tendsto (fun n => star (regularAverage P (d n)) v) atTop (𝓝 v) :=
    (regularAverage_star_tendsto_identity P v).comp hd
  have bound_limit (A C : ℕ → RegularHilbert (TowerHilbert P) →L[ℂ]
      RegularHilbert (TowerHilbert P))
      (B : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
      (hA : ∀ n, ‖A n‖ ≤ 1) (he : ∀ n, A n*C n=B)
      (hC : ∀ v, Tendsto (fun n => C n v) atTop (𝓝 v))
      (v : RegularHilbert (TowerHilbert P)) :
      Tendsto (fun n => A n v) atTop (𝓝 (B v)) := by
    apply tendsto_iff_dist_tendsto_zero.mpr
    have hl : Tendsto (fun n => ‖v-C n v‖) atTop (𝓝 0) := by
      simpa only [sub_self,norm_zero] using
        ((tendsto_const_nhds (x := v)).sub (hC v)).norm
    apply squeeze_zero (fun n => dist_nonneg)
      (fun n => ?_) hl
    rw [dist_eq_norm,← he n]
    change ‖A n v-A n (C n v)‖ ≤ ‖v-C n v‖
    rw [← map_sub]
    simpa only [one_mul] using (A n).le_of_opNorm_le (hA n) (v-C n v)
  refine ⟨b,hb,hn,?_,?_⟩
  · exact bound_limit (fun n => (b n).val) (fun n => regularAverage P (d n))
      (regularAverage P δ) hn hp hsmall
  · intro v
    refine bound_limit (fun n => star (b n).val) (fun n => star (regularAverage P (d n)))
      (star (regularAverage P δ)) ?_ ?_ hsmallstar v
    · intro n
      change ‖star ((b n).val)‖ ≤ 1
      rw [_root_.norm_star]
      exact hn n
    · intro n
      have he := congrArg star ((hc n).symm.trans (hp n))
      simpa only [star_mul] using he

/-- The original one-sided average has the full polar right action.
Selfadjointness of the average is neither asserted nor used. -/
theorem regularAverage_mem_scalarPolarRightAlgebra (P : SiteProfile)
    (δ : ℝ) (hδ : 0 < δ) :
    (⟨regularAverage P δ,regularAverage_mem P δ⟩ :
      (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P := by
  obtain ⟨b,hb,hn,hs,ha⟩ := regularAverage_polar_approximants P δ hδ
  let B : (regularCoreAlgebra P).toStarSubalgebra :=
    ⟨regularAverage P δ,regularAverage_mem P δ⟩
  change ScalarPolarRight P B ∧ ScalarPolarRight P (star B)
  constructor
  · intro A
    exact scalarRightAction_closed_of_bounded_strongStar P b B 1 hn hs ha A
      (fun n => (hb n).1 A)
  · intro A
    apply scalarRightAction_closed_of_bounded_strongStar P (l := atTop)
      (fun n => star (b n)) (star B) 1
    · intro n
      simpa only [StarMemClass.coe_star,_root_.norm_star] using hn n
    · exact ha
    · simpa only [star_star] using hs
    · exact fun n => (hb n).2 A

end
end TGLV350.Regular
