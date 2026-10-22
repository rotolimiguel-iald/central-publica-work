import SitePauliObservables
import TGLExt.TheModularFlowIsAHorizon
import Mathlib.Data.Real.Sign
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

set_option autoImplicit false
set_option maxHeartbeats 800000

namespace ChatgptAudit.Orbit052
open TGLExt ChatgptAudit ChatgptAudit.Observable035 Matrix
noncomputable section

def firstSiteModularGap (P : SiteProfile) : ℝ :=
  Real.log (P.w 0) - Real.log (1 - P.w 0)

def modularQuarterTurnTime (P : SiteProfile) : ℝ :=
  -Real.pi / (2 * firstSiteModularGap P)

def modularOrientedQuarterTime (P : SiteProfile) : ℝ :=
  -Real.pi / (2 * |firstSiteModularGap P|)

theorem first_site_modular_gap_ne_zero (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    firstSiteModularGap P ≠ 0 := by
  intro h
  have he := Real.log_injOn_pos (P.pos 0)
    (show 0 < 1 - P.w 0 by linarith [P.lt_one 0])
    (sub_eq_zero.mp h)
  apply hp
  linarith

theorem first_site_modular_gap_pos_iff (P : SiteProfile) :
    0 < firstSiteModularGap P ↔ 0 < 2 * P.w 0 - 1 := by
  rw [firstSiteModularGap, sub_pos,
    Real.log_lt_log_iff (show 0 < 1 - P.w 0 by linarith [P.lt_one 0]) (P.pos 0)]
  constructor <;> intro h <;> linarith

theorem first_site_modular_gap_neg_iff (P : SiteProfile) :
    firstSiteModularGap P < 0 ↔ 2 * P.w 0 - 1 < 0 := by
  rw [firstSiteModularGap, sub_neg,
    Real.log_lt_log_iff (P.pos 0) (show 0 < 1 - P.w 0 by linarith [P.lt_one 0])]
  constructor <;> intro h <;> linarith

theorem first_site_modular_gap_sign (P : SiteProfile) :
    Real.sign (firstSiteModularGap P) = Real.sign (2 * P.w 0 - 1) := by
  rcases lt_trichotomy (firstSiteModularGap P) 0 with h | h | h
  · rw [Real.sign_of_neg h,
      Real.sign_of_neg ((first_site_modular_gap_neg_iff P).mp h)]
  · have hr : 2 * P.w 0 - 1 = 0 := by
      have hn := first_site_modular_gap_neg_iff P
      have hp := first_site_modular_gap_pos_iff P
      rw [h] at hn hp
      linarith
    rw [h, hr]
  · rw [Real.sign_of_pos h,
      Real.sign_of_pos ((first_site_modular_gap_pos_iff P).mp h)]

theorem modular_phase_trigonometric (t r : ℝ) :
    modularPhase t r =
      (Real.cos (t * r) : ℂ) + (Real.sin (t * r) : ℂ) * Complex.I := by
  simp only [modularPhase, Complex.exp_mul_I, Complex.ofReal_cos, Complex.ofReal_sin]

theorem first_site_flow_x (P : SiteProfile) (t : ℝ) :
    flowLevel P t 0 pauliXMatrix =
      (Real.cos (t * firstSiteModularGap P) : ℂ) • pauliXMatrix -
      (Real.sin (t * firstSiteModularGap P) : ℂ) • pauliYMatrix := by
  have hgap : Real.log (P.w 0) - Real.log (1 - P.w 0) =
      firstSiteModularGap P := rfl
  have hneg : Real.log (1 - P.w 0) - Real.log (P.w 0) =
      -(firstSiteModularGap P) := by
    unfold firstSiteModularGap
    ring
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [flowLevel, towerW, siteW, pauliXMatrix, pauliYMatrix,
      modular_phase_trigonometric, hgap, hneg, mul_neg] <;> ring

theorem first_site_flow_y (P : SiteProfile) (t : ℝ) :
    flowLevel P t 0 pauliYMatrix =
      (Real.sin (t * firstSiteModularGap P) : ℂ) • pauliXMatrix +
      (Real.cos (t * firstSiteModularGap P) : ℂ) • pauliYMatrix := by
  have hgap : Real.log (P.w 0) - Real.log (1 - P.w 0) =
      firstSiteModularGap P := rfl
  have hneg : Real.log (1 - P.w 0) - Real.log (P.w 0) =
      -(firstSiteModularGap P) := by
    unfold firstSiteModularGap
    ring
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [flowLevel, towerW, siteW, pauliXMatrix, pauliYMatrix,
      modular_phase_trigonometric, hgap, hneg, mul_neg] <;>
    ring_nf <;> simp [Complex.I_sq]

theorem modular_horizon_pauli_x (P : SiteProfile) (t : ℝ) :
    adT (modularHorizon P t) (sitePauliX P 0) =
      (Real.cos (t * firstSiteModularGap P) : ℂ) • sitePauliX P 0 -
      (Real.sin (t * firstSiteModularGap P) : ℂ) • sitePauliY P 0 := by
  rw [adT_modularHorizon]
  change modularConjugation P t (towerPi P (N := 0) pauliXMatrix) = _
  rw [modularConjugation_local, first_site_flow_x]
  change (towerPiLinear P 0) (_ - _) = _
  rw [map_sub, map_smul, map_smul]
  rfl

theorem modular_horizon_pauli_y (P : SiteProfile) (t : ℝ) :
    adT (modularHorizon P t) (sitePauliY P 0) =
      (Real.sin (t * firstSiteModularGap P) : ℂ) • sitePauliX P 0 +
      (Real.cos (t * firstSiteModularGap P) : ℂ) • sitePauliY P 0 := by
  rw [adT_modularHorizon]
  change modularConjugation P t (towerPi P (N := 0) pauliYMatrix) = _
  rw [modularConjugation_local, first_site_flow_y, towerPi_add, towerPi_smul,
    towerPi_smul]
  rfl

theorem modular_quarter_turn_angle (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    modularQuarterTurnTime P * firstSiteModularGap P = -(Real.pi / 2) := by
  unfold modularQuarterTurnTime
  field_simp [first_site_modular_gap_ne_zero P hp]

theorem modular_quarter_horizon_x (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    adT (modularHorizon P (modularQuarterTurnTime P)) (sitePauliX P 0) =
      sitePauliY P 0 := by
  rw [modular_horizon_pauli_x, modular_quarter_turn_angle P hp]
  simp

theorem modular_quarter_horizon_y (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    adT (modularHorizon P (modularQuarterTurnTime P)) (sitePauliY P 0) =
      -sitePauliX P 0 := by
  rw [modular_horizon_pauli_y, modular_quarter_turn_angle P hp]
  simp

theorem modular_oriented_quarter_time_neg (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    modularOrientedQuarterTime P < 0 := by
  exact div_neg_of_neg_of_pos (neg_lt_zero.mpr Real.pi_pos)
    (mul_pos (by norm_num) (abs_pos.mpr (first_site_modular_gap_ne_zero P hp)))

theorem modular_oriented_angle_of_pos (P : SiteProfile)
    (h : 0 < firstSiteModularGap P) :
    modularOrientedQuarterTime P * firstSiteModularGap P = -(Real.pi / 2) := by
  unfold modularOrientedQuarterTime
  rw [abs_of_pos h]
  field_simp [ne_of_gt h]

theorem modular_oriented_angle_of_neg (P : SiteProfile)
    (h : firstSiteModularGap P < 0) :
    modularOrientedQuarterTime P * firstSiteModularGap P = Real.pi / 2 := by
  unfold modularOrientedQuarterTime
  rw [abs_of_neg h]
  field_simp [ne_of_lt h]
  <;> ring

theorem modular_oriented_horizon_x (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    adT (modularHorizon P (modularOrientedQuarterTime P)) (sitePauliX P 0) =
      (Real.sign (2 * P.w 0 - 1) : ℂ) • sitePauliY P 0 := by
  rw [modular_horizon_pauli_x]
  rcases lt_or_gt_of_ne (first_site_modular_gap_ne_zero P hp) with hn | hp
  · rw [modular_oriented_angle_of_neg P hn,
      Real.sign_of_neg ((first_site_modular_gap_neg_iff P).mp hn)]
    simp
  · rw [modular_oriented_angle_of_pos P hp,
      Real.sign_of_pos ((first_site_modular_gap_pos_iff P).mp hp)]
    simp

theorem modular_oriented_horizon_y (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    adT (modularHorizon P (modularOrientedQuarterTime P)) (sitePauliY P 0) =
      (-Real.sign (2 * P.w 0 - 1) : ℂ) • sitePauliX P 0 := by
  rw [modular_horizon_pauli_y]
  rcases lt_or_gt_of_ne (first_site_modular_gap_ne_zero P hp) with hn | hp
  · rw [modular_oriented_angle_of_neg P hn,
      Real.sign_of_neg ((first_site_modular_gap_neg_iff P).mp hn)]
    simp
  · rw [modular_oriented_angle_of_pos P hp,
      Real.sign_of_pos ((first_site_modular_gap_pos_iff P).mp hp)]
    simp

theorem first_site_modular_gap_tracial (P : SiteProfile) (hp : P.w 0 = 1 / 2) :
    firstSiteModularGap P = 0 := by
  norm_num [firstSiteModularGap, hp]

theorem modular_horizon_pauli_x_tracial (P : SiteProfile) (hp : P.w 0 = 1 / 2)
    (t : ℝ) :
    adT (modularHorizon P t) (sitePauliX P 0) = sitePauliX P 0 := by
  rw [modular_horizon_pauli_x, first_site_modular_gap_tracial P hp]
  simp

theorem modular_horizon_pauli_y_tracial (P : SiteProfile) (hp : P.w 0 = 1 / 2)
    (t : ℝ) :
    adT (modularHorizon P t) (sitePauliY P 0) = sitePauliY P 0 := by
  rw [modular_horizon_pauli_y, first_site_modular_gap_tracial P hp]
  simp

#print axioms firstSiteModularGap
#print axioms modularQuarterTurnTime
#print axioms modularOrientedQuarterTime
#print axioms first_site_modular_gap_ne_zero
#print axioms first_site_modular_gap_pos_iff
#print axioms first_site_modular_gap_neg_iff
#print axioms first_site_modular_gap_sign
#print axioms modular_phase_trigonometric
#print axioms first_site_flow_x
#print axioms first_site_flow_y
#print axioms modular_horizon_pauli_x
#print axioms modular_horizon_pauli_y
#print axioms modular_quarter_turn_angle
#print axioms modular_quarter_horizon_x
#print axioms modular_quarter_horizon_y
#print axioms modular_oriented_quarter_time_neg
#print axioms modular_oriented_angle_of_pos
#print axioms modular_oriented_angle_of_neg
#print axioms modular_oriented_horizon_x
#print axioms modular_oriented_horizon_y
#print axioms first_site_modular_gap_tracial
#print axioms modular_horizon_pauli_x_tracial
#print axioms modular_horizon_pauli_y_tracial

end
end ChatgptAudit.Orbit052
