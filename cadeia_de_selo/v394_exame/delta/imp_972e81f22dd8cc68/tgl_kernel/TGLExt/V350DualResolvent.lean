import TGLExt.V350PositiveResolvent
import TGLExt.V350DualClosedForm

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1600000

namespace TGLV350.Regular
open Filter
open scoped Topology ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem normalizedDualCut_mono_radius {R S : ℝ} (hR : 0 ≤ R) (hRS : R ≤ S)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) :
    normalizedDualCut R A ≤ normalizedDualCut S A := by
  rw [← sub_nonneg]
  change 0 ≤ (dualHaarFactor : ℂ) • dualWeightCut S A -
    (dualHaarFactor : ℂ) • dualWeightCut R A
  rw [← smul_sub, ContinuousLinearMap.nonneg_iff_isPositive]
  exact ((ContinuousLinearMap.nonneg_iff_isPositive _).mp
    (sub_nonneg.mpr (dualWeightCut_mono_radius hR hRS A hA))).smul_of_nonneg
    (by exact_mod_cast dualHaarFactor_pos.le)

theorem normalizedDualCut_quadratic (R : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    (inner ℂ v (normalizedDualCut R A v)).re =
      dualHaarFactor * (inner ℂ v (dualWeightCut R A v)).re := by
  change (inner ℂ v ((dualHaarFactor : ℂ) • dualWeightCut R A v)).re = _
  simp only [inner_smul_right, Complex.mul_re, Complex.ofReal_re,
    Complex.ofReal_im, zero_mul, sub_zero]

theorem dualQuadraticIntegral_eq_iSup_normalized_cuts
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (v : RegularHilbert H) :
    dualQuadraticIntegral A v = ⨆ n : ℕ,
      ENNReal.ofReal (inner ℂ v (normalizedDualCut (n : ℝ) A v)).re := by
  simp only [normalizedDualCut_quadratic, ENNReal.ofReal_mul dualHaarFactor_pos.le]
  exact dualQuadraticIntegral_eq_iSup_cuts A hA v

/-- Actual normalized dual cuts, not an arbitrary increasing surrogate. -/
def dualCutResolvent (n : ℕ) (A : RegularHilbert H →L[ℂ] RegularHilbert H) :=
  positiveResolvent (normalizedDualCut (n : ℝ) A)

theorem dualCutResolvent_antitone
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) :
    Antitone (fun n => dualCutResolvent n A) := by
  intro n m hnm
  exact positiveResolvent_antitone (normalizedDualCut_nonneg _ (Nat.cast_nonneg n) A hA)
    (normalizedDualCut_mono_radius (Nat.cast_nonneg n) (by exact_mod_cast hnm) A hA)

theorem exists_dualResolvent_limit (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P)) (hmem : A ∈ regularCoreAlgebra P)
    (hA : 0 ≤ A) :
    ∃ R : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P),
      R ∈ regularCoreAlgebra P ∧ 0 ≤ R ∧ R ≤ 1 ∧
      (∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) ∧
      IsGLB (Set.range (fun n => dualCutResolvent n A)) R := by
  apply vonNeumann_antitone_contraction_limit (regularCoreAlgebra P)
    (fun n => dualCutResolvent n A)
  · intro n
    exact positiveResolvent_mem _ _ (normalizedDualCut_mem P _ A hmem)
      (normalizedDualCut_nonneg _ (Nat.cast_nonneg n) A hA)
  · intro n
    exact positiveResolvent_nonneg _ (normalizedDualCut_nonneg _ (Nat.cast_nonneg n) A hA)
  · intro n
    exact positiveResolvent_le_one _ (normalizedDualCut_nonneg _ (Nat.cast_nonneg n) A hA)
  · exact dualCutResolvent_antitone A hA

/-- A uniform energy bound, derived from (I+C)r=v and Cauchy--Schwarz.
The constant is independent of the cutoff norm. -/
theorem positiveResolvent_energy_bound (C : H →L[ℂ] H) (hC : 0 ≤ C) (v : H) :
    (inner ℂ (positiveResolvent C v) (C (positiveResolvent C v))).re ≤ ‖v‖^2 / 4 := by
  let r := positiveResolvent C v
  have heq := congrArg (fun B : H →L[ℂ] H => B v) (positiveResolvent_right_inverse C hC)
  change r + C r = v at heq
  have hCr : C r = v-r := by rw [← heq]; abel
  change (inner ℂ r (C r)).re ≤ _
  rw [hCr, inner_sub_right, Complex.sub_re]
  have hr : (inner ℂ r r).re = ‖r‖^2 := inner_self_eq_norm_sq (𝕜 := ℂ) r
  rw [hr]
  have hcs : (inner ℂ r v).re ≤ ‖r‖ * ‖v‖ := re_inner_le_norm (𝕜 := ℂ) r v
  nlinarith [sq_nonneg (‖r‖ - ‖v‖ / 2)]

/-- The strong limit has range in the finite domain of the actual dual form.
This is a connection to q_A, not yet the spectral representation theorem. -/
theorem dualResolvent_limit_energy_bound
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (v : RegularHilbert H) :
    dualQuadraticIntegral A (R v) ≤ ENNReal.ofReal (‖v‖^2 / 4) := by
  rw [dualQuadraticIntegral_eq_iSup_normalized_cuts A hA]
  apply iSup_le
  intro m
  have hcontinuous : Continuous (fun w : RegularHilbert H =>
      (inner ℂ w (normalizedDualCut (m : ℝ) A w)).re) :=
    Complex.continuous_re.comp (continuous_id.inner (normalizedDualCut (m : ℝ) A).continuous)
  have hbound : ∀ᶠ n : ℕ in atTop,
      (inner ℂ (dualCutResolvent n A v)
        (normalizedDualCut (m : ℝ) A (dualCutResolvent n A v))).re ≤ ‖v‖^2 / 4 := by
    filter_upwards [eventually_ge_atTop m] with n hmn
    have horder := normalizedDualCut_mono_radius (Nat.cast_nonneg m)
      (show (m : ℝ) ≤ (n : ℝ) by exact_mod_cast hmn) A hA
    have hnonneg := ((ContinuousLinearMap.nonneg_iff_isPositive _).mp
      (sub_nonneg.mpr horder)).re_inner_nonneg_right (dualCutResolvent n A v)
    simp only [sub_apply, inner_sub_right] at hnonneg
    exact (sub_nonneg.mp hnonneg).trans (positiveResolvent_energy_bound _
      (normalizedDualCut_nonneg _ (Nat.cast_nonneg n) A hA) v)
  exact ENNReal.ofReal_le_ofReal (le_of_tendsto
    (hcontinuous.continuousAt.tendsto.comp (hlim v)) hbound)

theorem dualResolvent_limit_range_finite
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (v : RegularHilbert H) : R v ∈ (dualClosedPositiveForm A hA).finiteDomain :=
  lt_of_le_of_lt (dualResolvent_limit_energy_bound A R hA hlim v) ENNReal.ofReal_lt_top

/-- The limit for the unit is zero. Invertibility of every finite resolvent does
not imply invertibility of its strong limit; the infinite part is retained. -/
theorem dualResolvent_limit_one_eq_zero (R : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n 1 v) atTop (𝓝 (R v))) : R = 0 := by
  apply ContinuousLinearMap.ext
  intro v
  have hfin := dualResolvent_limit_range_finite 1 R zero_le_one hlim v
  rw [dualClosedPositiveForm_one_domain] at hfin
  exact hfin

theorem dualCutResolvent_zero (n : ℕ) :
    dualCutResolvent n (0 : RegularHilbert H →L[ℂ] RegularHilbert H) = 1 := by
  have hf : fibre (0 : H →L[ℂ] H) = 0 := map_zero fibreRepresentation
  have hcut : dualWeightCut (n : ℝ) (0 : RegularHilbert H →L[ℂ] RegularHilbert H) = 0 := by
    simpa only [hf, smul_zero] using dualWeightCut_fibre (n : ℝ) (0 : H →L[ℂ] H)
  simp only [dualCutResolvent, normalizedDualCut, hcut, smul_zero, positiveResolvent,
    add_zero, Ring.inverse_one]

/-- The opposite endpoint retains the entire Hilbert space. -/
theorem dualResolvent_limit_zero_eq_one (R : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n 0 v) atTop (𝓝 (R v))) : R = 1 := by
  apply ContinuousLinearMap.ext
  intro v
  have ht := hlim v
  simp only [dualCutResolvent_zero, one_apply_eq_self] at ht
  exact (tendsto_nhds_unique ht tendsto_const_nhds)

#print axioms normalizedDualCut_mono_radius
#print axioms normalizedDualCut_quadratic
#print axioms dualQuadraticIntegral_eq_iSup_normalized_cuts
#print axioms dualCutResolvent_antitone
#print axioms exists_dualResolvent_limit
#print axioms positiveResolvent_energy_bound
#print axioms dualResolvent_limit_energy_bound
#print axioms dualResolvent_limit_range_finite
#print axioms dualResolvent_limit_one_eq_zero
#print axioms dualCutResolvent_zero
#print axioms dualResolvent_limit_zero_eq_one
end
end TGLV350.Regular
