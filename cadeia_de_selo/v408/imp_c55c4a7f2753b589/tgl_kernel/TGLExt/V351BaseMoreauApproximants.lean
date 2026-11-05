import TGLExt.V351ExtendedBaseDualWeight
import TGLExt.V350DualEnergyOnResolvent

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV351
open TGLExt TGLV350.Regular Filter
open scoped Topology ENNReal NNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The minimum energy is the bounded quadratic form of I-R. -/
theorem dualResolvent_minimum_energy_value
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (v : RegularHilbert H) :
    dualEnergy A v (R v) = ENNReal.ofReal (inner ℂ v ((1-R) v)).re := by
  have hf : dualQuadraticIntegral A (R v) ≠ ⊤ :=
    ne_of_lt (dualResolvent_limit_range_finite A R hA hlim v)
  have he := dualResolvent_limit_energy_identity A R hA hlim v
  have hq : dualQuadraticIntegral A (R v) =
      ENNReal.ofReal (inner ℂ (R v) (v-R v)).re := by
    rw [← he]
    exact (ENNReal.ofReal_toReal hf).symm
  have hp : 0 ≤ (inner ℂ (R v) (v-R v)).re := by
    rw [← he]
    exact ENNReal.toReal_nonneg
  unfold dualEnergy
  rw [hq, ← ENNReal.ofReal_add (sq_nonneg _) hp]
  congr 1
  simp only [sub_apply, one_apply_eq_self, inner_sub_right,
    Complex.sub_re, norm_sub_sq (𝕜 := ℂ)]
  have hr : (inner ℂ (R v) (R v)).re = ‖R v‖^2 := inner_self_eq_norm_sq (𝕜 := ℂ) (R v)
  have hv : (inner ℂ v v).re = ‖v‖^2 := inner_self_eq_norm_sq (𝕜 := ℂ) v
  have hs : (inner ℂ v (R v)).re = (inner ℂ (R v) v).re :=
    inner_re_symm (𝕜 := ℂ) v (R v)
  rw [hr,hv,hs]
  change ‖R v‖^2 - 2*(inner ℂ (R v) v).re + ‖v‖^2 +
    ((inner ℂ (R v) v).re - ‖R v‖^2) = ‖v‖^2 - (inner ℂ (R v) v).re
  ring

/-- A positive bounded operator in the original base represents each Moreau
minimum of the actual dual form. The minimizing vector remains in the same
regular Hilbert space. No bounded-output assumption is imposed on q_A. -/
theorem exists_base_moreau_approximant (P : SiteProfile) (A : PositiveCoreInput P)
    (c : ℝ) (hc : 0 < c) :
    ∃ D : TowerHilbert P →L[ℂ] TowerHilbert P,
      D ∈ theFactorObject P ∧ 0 ≤ D ∧ D ≤ (c : ℂ) • 1 ∧
      ∀ v : RegularHilbert (TowerHilbert P), ∃ w : RegularHilbert (TowerHilbert P),
        ENNReal.ofReal (inner ℂ v (fibre D v)).re =
          ENNReal.ofReal (c * ‖w-v‖^2) + dualQuadraticIntegral A.val w ∧
        ∀ z : RegularHilbert (TowerHilbert P),
          ENNReal.ofReal (inner ℂ v (fibre D v)).re ≤
            ENNReal.ofReal (c * ‖z-v‖^2) + dualQuadraticIntegral A.val z := by
  let A' := A.scale ⟨c⁻¹, (inv_pos.mpr hc).le⟩
  obtain ⟨R, hmR, hR, hone, hlim, hfix⟩ :=
    exists_dualResolvent_fixed P A'.val A'.property.1 A'.property.2
  let B : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P) :=
    (c : ℂ) • (1-R)
  have hRF : R ∈ dualFixedCore P := (dualFixedCore_mem_iff P R).mpr ⟨hmR,hfix⟩
  have hBF : B ∈ dualFixedCore P :=
    (dualFixedCore P).toStarSubalgebra.smul_mem
      ((dualFixedCore P).sub_mem (dualFixedCore P).one_mem hRF) (c : ℂ)
  have hB : 0 ≤ B := by
    rw [ContinuousLinearMap.nonneg_iff_isPositive]
    exact ((ContinuousLinearMap.nonneg_iff_isPositive _).mp
      (sub_nonneg.mpr hone)).smul_of_nonneg (by exact_mod_cast hc.le)
  have hBbound : B ≤ (c : ℂ) • 1 := by
    rw [← sub_nonneg]
    have he : (c : ℂ) • (1 : RegularHilbert (TowerHilbert P) →L[ℂ] _) - B = (c : ℂ) • R := by
      apply ContinuousLinearMap.ext
      intro v
      change (c : ℂ) • v - (c : ℂ) • (v-R v) = (c : ℂ) • R v
      rw [smul_sub]
      abel
    rw [he, ContinuousLinearMap.nonneg_iff_isPositive]
    exact ((ContinuousLinearMap.nonneg_iff_isPositive _).mp hR).smul_of_nonneg
      (by exact_mod_cast hc.le)
  obtain ⟨D, hD, hBD⟩ := (dualFixedCore_eq_amplified_base P B).mp hBF
  refine ⟨D,hD,(fibre_nonneg_iff D).mp (hBD ▸ hB),?_,?_⟩
  · apply (fibre_le_iff D ((c : ℂ) • 1)).mp
    have hf : fibre ((c : ℂ) • (1 : TowerHilbert P →L[ℂ] _)) = (c : ℂ) • 1 := by
      rw [fibre_smul, fibre_one]
    rw [hf, ← hBD]
    exact hBbound
  · intro v
    have he : ENNReal.ofReal (inner ℂ v (fibre D v)).re =
        ENNReal.ofReal c * dualEnergy A'.val v (R v) := by
      rw [dualResolvent_minimum_energy_value A'.val R A'.property.2 hlim v, ← hBD]
      change ENNReal.ofReal (inner ℂ v ((c : ℂ) • ((1-R) v))).re = _
      simp only [inner_smul_right, Complex.mul_re, Complex.ofReal_re,
        Complex.ofReal_im, zero_mul, sub_zero]
      exact ENNReal.ofReal_mul hc.le
    have hscale : ∀ z : RegularHilbert (TowerHilbert P),
        ENNReal.ofReal c * dualEnergy A'.val v z =
          ENNReal.ofReal (c * ‖z-v‖^2) + dualQuadraticIntegral A.val z := by
      intro z
      change ENNReal.ofReal c *
        (ENNReal.ofReal (‖z-v‖^2) + dualQuadraticIntegral (c⁻¹ • A.val) z) = _
      rw [dualQuadraticIntegral_smul_operator _ (inv_pos.mpr hc).le,
        mul_add, ← mul_assoc, ← ENNReal.ofReal_mul hc.le,
        ← ENNReal.ofReal_mul hc.le, mul_inv_cancel₀ hc.ne',
        ENNReal.ofReal_one, one_mul]
    refine ⟨R v, he.trans (hscale (R v)), ?_⟩
    intro z
    rw [he, ← hscale z]
    exact mul_le_mul_right
      (dualResolvent_limit_minimizes_energy A'.val R A'.property.2 hlim v z)
      (ENNReal.ofReal c)

/-- The bounded operators lie in M, increase in its actual operator order,
and recover the extended dual form on every regular vector, including infinity. -/
theorem exists_monotone_base_dual_approximation (P : SiteProfile) (A : PositiveCoreInput P) :
    ∃ D : ℕ → TowerHilbert P →L[ℂ] TowerHilbert P,
      (∀ n, D n ∈ theFactorObject P) ∧ (∀ n, 0 ≤ D n) ∧ Monotone D ∧
      ∀ v : RegularHilbert (TowerHilbert P),
        dualQuadraticIntegral A.val v =
          ⨆ n : ℕ, ENNReal.ofReal (inner ℂ v (fibre (D n) v)).re := by
  have hex := fun n : ℕ => exists_base_moreau_approximant P A ((n : ℝ)+1) (by positivity)
  choose D hmem hpos hbound hmin using hex
  have hmonoQ : ∀ v : RegularHilbert (TowerHilbert P),
      Monotone (fun n : ℕ => ENNReal.ofReal (inner ℂ v (fibre (D n) v)).re) := by
    intro v n m hnm
    obtain ⟨w, hw, _⟩ := hmin m v
    obtain ⟨_, _, hn⟩ := hmin n v
    apply (hn w).trans
    dsimp only
    rw [hw]
    apply add_le_add _ le_rfl
    apply ENNReal.ofReal_le_ofReal
    apply mul_le_mul_of_nonneg_right _ (sq_nonneg _)
    exact_mod_cast Nat.add_le_add_right hnm 1
  refine ⟨D,hmem,hpos,?_,?_⟩
  · intro n m hnm
    rw [← sub_nonneg, ContinuousLinearMap.nonneg_iff_isPositive,
      ContinuousLinearMap.isPositive_def']
    refine ⟨(IsSelfAdjoint.of_nonneg (hpos m)).sub (IsSelfAdjoint.of_nonneg (hpos n)), ?_⟩
    intro v
    have hq := hmonoQ (testVector v) hnm
    simp only [fibre_testVector, testVector_inner] at hq
    have hp : 0 ≤ (inner ℂ v (D m v)).re :=
      ((ContinuousLinearMap.nonneg_iff_isPositive _).mp (hpos m)).re_inner_nonneg_right v
    have hr := (ENNReal.ofReal_le_ofReal_iff hp).mp hq
    change 0 ≤ (inner ℂ ((D m-D n) v) v).re
    have hs : (inner ℂ ((D m-D n) v) v).re = (inner ℂ v ((D m-D n) v)).re :=
      inner_re_symm (𝕜 := ℂ) ((D m-D n) v) v
    rw [hs]
    simp only [sub_apply, inner_sub_right, Complex.sub_re]
    exact sub_nonneg.mpr hr
  · intro v
    let s : ℝ≥0∞ := ⨆ n : ℕ, ENNReal.ofReal (inner ℂ v (fibre (D n) v)).re
    have hu : ∀ n, ENNReal.ofReal (inner ℂ v (fibre (D n) v)).re ≤
        dualQuadraticIntegral A.val v := by
      intro n
      obtain ⟨_, _, hm⟩ := hmin n v
      simpa only [sub_self, norm_zero, zero_pow (by decide : 2 ≠ 0), mul_zero,
        ENNReal.ofReal_zero, zero_add] using hm v
    apply le_antisymm _ (iSup_le hu)
    change dualQuadraticIntegral A.val v ≤ s
    by_cases hs : s = ⊤
    · rw [hs]
      exact le_top
    choose w he _ using (fun n => hmin n v)
    have hwBound : ∀ n : ℕ, ENNReal.ofReal (((n : ℝ)+1) * ‖w n-v‖^2) ≤ s := by
      intro n
      calc
        _ ≤ ENNReal.ofReal (((n : ℝ)+1) * ‖w n-v‖^2) +
            dualQuadraticIntegral A.val (w n) := le_self_add
        _ = ENNReal.ofReal (inner ℂ v (fibre (D n) v)).re := (he n).symm
        _ ≤ s := le_iSup (fun k => ENNReal.ofReal (inner ℂ v (fibre (D k) v)).re) n
    have hqBound : ∀ n, dualQuadraticIntegral A.val (w n) ≤ s := by
      intro n
      calc
        _ ≤ ENNReal.ofReal (((n : ℝ)+1) * ‖w n-v‖^2) +
            dualQuadraticIntegral A.val (w n) := le_add_self
        _ = ENNReal.ofReal (inner ℂ v (fibre (D n) v)).re := (he n).symm
        _ ≤ s := le_iSup (fun k => ENNReal.ofReal (inner ℂ v (fibre (D k) v)).re) n
    have ht : Tendsto w atTop (𝓝 v) := by
      apply Metric.tendsto_atTop.mpr
      intro ε hε
      obtain ⟨N,hN⟩ := exists_nat_gt (s.toReal / ε^2)
      refine ⟨N,fun n hn => ?_⟩
      have hc : s.toReal / ε^2 < (n : ℝ)+1 := by
        have hcast : (N : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
        linarith
      have hε2 : 0 < ε^2 := sq_pos_of_pos hε
      have hc' := (div_lt_iff₀ hε2).mp hc
      have hb := ENNReal.toReal_mono hs (hwBound n)
      rw [ENNReal.toReal_ofReal (mul_nonneg (by positivity) (sq_nonneg _))] at hb
      rw [dist_eq_norm]
      have hnpos : (0 : ℝ) < (n : ℝ)+1 := by positivity
      have hsq : ‖w n-v‖^2 < ε^2 := by nlinarith
      nlinarith [norm_nonneg (w n-v)]
    exact (dualClosedPositiveForm A.val A.property.2).isClosed_sublevel s |>.mem_of_tendsto ht
      (Eventually.of_forall hqBound)

#print axioms dualResolvent_minimum_energy_value
#print axioms exists_base_moreau_approximant
#print axioms exists_monotone_base_dual_approximation
end
end TGLV351
