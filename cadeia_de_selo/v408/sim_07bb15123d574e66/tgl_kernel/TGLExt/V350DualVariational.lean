import TGLExt.V350DualResolvent

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open Filter
open scoped Topology ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The actual extended form plus the squared distance to the given vector. -/
def dualEnergy (A : RegularHilbert H →L[ℂ] RegularHilbert H)
    (v w : RegularHilbert H) : ℝ≥0∞ :=
  ENNReal.ofReal (‖w-v‖^2) + dualQuadraticIntegral A w

theorem positiveResolvent_energy_identity (C : H →L[ℂ] H) (hC : 0 ≤ C) (v w : H) :
    ‖w-v‖^2 + (inner ℂ w (C w)).re =
      ‖positiveResolvent C v-v‖^2 +
      (inner ℂ (positiveResolvent C v) (C (positiveResolvent C v))).re +
      ‖w-positiveResolvent C v‖^2 +
      (inner ℂ (w-positiveResolvent C v) (C (w-positiveResolvent C v))).re := by
  let r := positiveResolvent C v
  have heq := congrArg (fun B : H →L[ℂ] H => B v) (positiveResolvent_right_inverse C hC)
  change r + C r = v at heq
  have hCr : C r = v-r := by rw [← heq]; abel
  have hp := (ContinuousLinearMap.nonneg_iff_isPositive C).mp hC
  have hsym : (inner ℂ r (C w)).re = (inner ℂ w (C r)).re := by
    rw [← hp.inner_left_eq_inner_right]
    exact inner_re_symm (𝕜 := ℂ) (C r) w
  change ‖w-v‖^2 + (inner ℂ w (C w)).re =
    ‖r-v‖^2 + (inner ℂ r (C r)).re + ‖w-r‖^2 +
      (inner ℂ (w-r) (C (w-r))).re
  rw [map_sub, inner_sub_left, inner_sub_right, inner_sub_right]
  simp only [Complex.sub_re]
  rw [hsym, hCr, inner_sub_right, inner_sub_right]
  simp only [Complex.sub_re]
  rw [norm_sub_sq (𝕜 := ℂ), norm_sub_sq (𝕜 := ℂ), norm_sub_sq (𝕜 := ℂ)]
  have hr : (inner ℂ r r).re = ‖r‖^2 := inner_self_eq_norm_sq (𝕜 := ℂ) r
  change ‖w‖^2 - 2*(inner ℂ w v).re + ‖v‖^2 + (inner ℂ w (C w)).re = _
  change _ = (‖r‖^2 - 2*(inner ℂ r v).re + ‖v‖^2) +
    ((inner ℂ r v).re - (inner ℂ r r).re) +
    (‖w‖^2 - 2*(inner ℂ w r).re + ‖r‖^2) +
    ((inner ℂ w (C w)).re - ((inner ℂ w v).re - (inner ℂ w r).re) -
      (((inner ℂ w v).re - (inner ℂ w r).re) -
        ((inner ℂ r v).re - (inner ℂ r r).re)))
  rw [hr]
  ring

theorem positiveResolvent_minimizes_energy (C : H →L[ℂ] H) (hC : 0 ≤ C) (v w : H) :
    ‖positiveResolvent C v-v‖^2 +
      (inner ℂ (positiveResolvent C v) (C (positiveResolvent C v))).re ≤
    ‖w-v‖^2 + (inner ℂ w (C w)).re := by
  rw [positiveResolvent_energy_identity C hC v w]
  have hq := ((ContinuousLinearMap.nonneg_iff_isPositive C).mp hC).re_inner_nonneg_right
    (w-positiveResolvent C v)
  change 0 ≤ (inner ℂ (w-positiveResolvent C v) (C (w-positiveResolvent C v))).re at hq
  linarith [sq_nonneg ‖w-positiveResolvent C v‖]

theorem dualEnergy_eq_iSup_cuts
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (v w : RegularHilbert H) :
    dualEnergy A v w = ⨆ n : ℕ, ENNReal.ofReal
      (‖w-v‖^2 + (inner ℂ w (normalizedDualCut (n : ℝ) A w)).re) := by
  unfold dualEnergy
  rw [dualQuadraticIntegral_eq_iSup_normalized_cuts A hA, ENNReal.add_iSup]
  congr 1
  funext n
  exact (ENNReal.ofReal_add (sq_nonneg _)
    (((ContinuousLinearMap.nonneg_iff_isPositive _).mp
      (normalizedDualCut_nonneg _ (Nat.cast_nonneg n) A hA)).re_inner_nonneg_right w)).symm

/-- The actual dual form is minimized by the strong resolvent limit. Values at
competitors may be infinite; no subtraction of extended values is used. -/
theorem dualResolvent_limit_minimizes_energy
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (v w : RegularHilbert H) : dualEnergy A v (R v) ≤ dualEnergy A v w := by
  rw [dualEnergy_eq_iSup_cuts A hA]
  apply iSup_le
  intro m
  have hc : Continuous (fun z : RegularHilbert H => ENNReal.ofReal
      (‖z-v‖^2 + (inner ℂ z (normalizedDualCut (m : ℝ) A z)).re)) :=
    ENNReal.continuous_ofReal.comp
      (((continuous_id.sub continuous_const).norm.pow 2).add
        (Complex.continuous_re.comp (continuous_id.inner
          (normalizedDualCut (m : ℝ) A).continuous)))
  apply le_of_tendsto (hc.continuousAt.tendsto.comp (hlim v))
  filter_upwards [eventually_ge_atTop m] with n hmn
  have horder := normalizedDualCut_mono_radius (Nat.cast_nonneg m)
    (show (m : ℝ) ≤ (n : ℝ) by exact_mod_cast hmn) A hA
  have hnonneg := ((ContinuousLinearMap.nonneg_iff_isPositive _).mp
    (sub_nonneg.mpr horder)).re_inner_nonneg_right (dualCutResolvent n A v)
  simp only [sub_apply, inner_sub_right] at hnonneg
  have hcut :
      ‖dualCutResolvent n A v-v‖^2 +
        (inner ℂ (dualCutResolvent n A v)
          (normalizedDualCut (m : ℝ) A (dualCutResolvent n A v))).re ≤
      ‖w-v‖^2 + (inner ℂ w (normalizedDualCut (n : ℝ) A w)).re :=
    (add_le_add le_rfl (sub_nonneg.mp hnonneg)).trans
      (positiveResolvent_minimizes_energy _
        (normalizedDualCut_nonneg _ (Nat.cast_nonneg n) A hA) v w)
  refine (ENNReal.ofReal_le_ofReal hcut).trans ?_
  rw [dualEnergy_eq_iSup_cuts A hA]
  exact le_iSup (fun k : ℕ => ENNReal.ofReal
    (‖w-v‖^2 + (inner ℂ w (normalizedDualCut (k : ℝ) A w)).re)) n

#print axioms positiveResolvent_energy_identity
#print axioms positiveResolvent_minimizes_energy
#print axioms dualEnergy_eq_iSup_cuts
#print axioms dualResolvent_limit_minimizes_energy
end
end TGLV350.Regular
