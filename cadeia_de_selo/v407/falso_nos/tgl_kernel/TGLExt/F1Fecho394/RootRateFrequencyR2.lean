import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic
/-! Exact two-level consequence of the already stated root law, on the SAME
positive energy spectrum and clock. beta is a parameter; no numerical value
is inserted. A device identification, its measured rates and its energy zero
are not consequences of this scalar algebra. -/
set_option autoImplicit false
set_option maxHeartbeats 500000
namespace F1Fecho.RootRateFrequency
noncomputable def rootRate (beta hbar high low : ℝ) : ℝ :=
  beta * (Real.sqrt high-Real.sqrt low)^2 / (2*hbar)
noncomputable def phaseFrequency (hbar high low : ℝ) : ℝ := (high-low)/hbar

theorem phase_pos (hbar high low : ℝ) (hh : 0<hbar) (he : low<high) :
    0 < phaseFrequency hbar high low := div_pos (sub_pos.mpr he) hh

theorem ratio_factor (beta hbar high low : ℝ) (hh : 0<hbar)
    (hl : 0≤low) (he : low<high) :
    rootRate beta hbar high low / phaseFrequency hbar high low =
      (beta/2) * ((Real.sqrt high-Real.sqrt low)/(Real.sqrt high+Real.sqrt low)) := by
  have hhigh : 0<high := lt_of_le_of_lt hl he
  have hs : Real.sqrt low<Real.sqrt high := Real.sqrt_lt_sqrt hl he
  have hp : 0<Real.sqrt high+Real.sqrt low :=
    add_pos_of_pos_of_nonneg (Real.sqrt_pos.mpr hhigh) (Real.sqrt_nonneg _)
  have hd : high-low=(Real.sqrt high-Real.sqrt low)*(Real.sqrt high+Real.sqrt low) := by
    nlinarith [Real.sq_sqrt hl, Real.sq_sqrt hhigh.le]
  unfold rootRate phaseFrequency
  rw [hd]
  field_simp [ne_of_gt hh,ne_of_gt hp,sub_ne_zero.mpr hs.ne']
  <;> ring

theorem ratio_bounds (beta hbar high low : ℝ) (hb : 0<beta) (hh : 0<hbar)
    (hl : 0≤low) (he : low<high) :
    0 < rootRate beta hbar high low / phaseFrequency hbar high low ∧
    rootRate beta hbar high low / phaseFrequency hbar high low ≤ beta/2 := by
  rw [ratio_factor beta hbar high low hh hl he]
  have hs := Real.sqrt_lt_sqrt hl he
  have hp : 0<Real.sqrt high+Real.sqrt low :=
    add_pos_of_pos_of_nonneg (Real.sqrt_pos.mpr (lt_of_le_of_lt hl he)) (Real.sqrt_nonneg _)
  have hratio : (Real.sqrt high-Real.sqrt low)/(Real.sqrt high+Real.sqrt low) ≤ 1 := by
    apply (div_le_one hp).mpr
    linarith [Real.sqrt_nonneg low]
  constructor
  · exact mul_pos (div_pos hb (by norm_num)) (div_pos (sub_pos.mpr hs) hp)
  · nlinarith [div_pos hb (show (0:ℝ)<2 by norm_num)]

theorem upper_bound_iff_ground_zero (beta hbar high low : ℝ)
    (hb : 0<beta) (hh : 0<hbar) (hl : 0≤low) (he : low<high) :
    rootRate beta hbar high low / phaseFrequency hbar high low = beta/2 ↔ low=0 := by
  rw [ratio_factor beta hbar high low hh hl he]
  have hp : 0<Real.sqrt high+Real.sqrt low :=
    add_pos_of_pos_of_nonneg (Real.sqrt_pos.mpr (lt_of_le_of_lt hl he)) (Real.sqrt_nonneg _)
  constructor
  · intro h
    have hr : (Real.sqrt high-Real.sqrt low)/(Real.sqrt high+Real.sqrt low)=1 := by
      nlinarith [div_pos hb (show (0:ℝ)<2 by norm_num)]
    have hs : Real.sqrt high-Real.sqrt low=Real.sqrt high+Real.sqrt low :=
      (div_eq_one_iff_eq (ne_of_gt hp)).mp hr
    have hz : Real.sqrt low=0 := by linarith
    nlinarith [Real.sq_sqrt hl]
  · intro h
    subst low
    simp [ne_of_gt (Real.sqrt_pos.mpr he)]

theorem ratio_less_than_one (beta hbar high low : ℝ)
    (hb : 0<beta) (hb2 : beta<2) (hh : 0<hbar) (hl : 0≤low) (he : low<high) :
    rootRate beta hbar high low / phaseFrequency hbar high low < 1 := by
  have h := (ratio_bounds beta hbar high low hb hh hl he).2
  linarith

end F1Fecho.RootRateFrequency
#print axioms F1Fecho.RootRateFrequency.ratio_factor
#print axioms F1Fecho.RootRateFrequency.ratio_bounds
#print axioms F1Fecho.RootRateFrequency.upper_bound_iff_ground_zero
#print axioms F1Fecho.RootRateFrequency.ratio_less_than_one
