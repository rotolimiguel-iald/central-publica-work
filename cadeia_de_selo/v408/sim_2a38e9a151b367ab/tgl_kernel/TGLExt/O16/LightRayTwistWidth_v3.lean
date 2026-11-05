import Lean
import TGLExt.O16.LightRayAnalyticCore_v3

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open Complex

namespace ChatgptAudit.LightRayCore016

theorem multiplier_real_norm_one (a x : ℝ) : ‖multiplier a (x : ℂ)‖ = 1 := by
  simpa using multiplier_strip_norm a x 0

theorem sine_zero_unique_in_first_period (w : ℝ) (hw0 : 0 < w)
    (hw2 : w < 2*Real.pi) (hsin : Real.sin w = 0) : w = Real.pi := by
  rcases lt_trichotomy w Real.pi with h | h | h
  · have hp := Real.sin_pos_of_pos_of_lt_pi hw0 h
    rw [hsin] at hp
    exact False.elim (lt_irrefl _ hp)
  · exact h
  · have hp := Real.sin_pos_of_pos_of_lt_pi (show 0 < w-Real.pi by linarith)
      (show w-Real.pi < Real.pi by linarith)
    rw [Real.sin_sub_pi, hsin, neg_zero] at hp
    exact False.elim (lt_irrefl _ hp)

/-- Even one boundary point's norm forces the width within the first open period. -/
theorem twist_at_zero_forces_width (a w : ℝ) (ha : 0 < a)
    (hw0 : 0 < w) (hw2 : w < 2*Real.pi)
    (ht : multiplier a ((0 : ℂ)+I*(w : ℂ)) = star (multiplier a (0 : ℂ))) :
    w = Real.pi := by
  have hn := congrArg norm ht
  have hm := multiplier_strip_norm a 0 w
  simp only [Complex.ofReal_zero] at hm
  have hzero := multiplier_real_norm_one a 0
  simp only [Complex.ofReal_zero] at hzero
  rw [hm, norm_star, hzero] at hn
  have he : Real.exp (-a * Real.sin w) = Real.exp 0 := by simpa using hn
  have hz : -a * Real.sin w = 0 := Real.exp_injective he
  have hs : Real.sin w = 0 := (mul_eq_zero.mp hz).resolve_left (neg_ne_zero.mpr ha.ne')
  exact sine_zero_unique_in_first_period w hw0 hw2 hs

theorem twist_preserved_iff (a w : ℝ) (ha : 0 < a) (hw0 : 0 < w)
    (hw2 : w < 2*Real.pi) :
    (∀ x : ℝ, multiplier a ((x : ℂ)+I*(w : ℂ)) = star (multiplier a (x : ℂ))) ↔
      w = Real.pi := by
  constructor
  · intro h
    exact twist_at_zero_forces_width a w ha hw0 hw2 (h 0)
  · rintro rfl
    exact multiplier_twist a

theorem twist_fails_at_half_width (a : ℝ) (ha : 0 < a) :
    multiplier a ((0 : ℂ)+I*(Real.pi/2 : ℝ)) ≠ star (multiplier a (0 : ℂ)) := by
  intro h
  have hw := twist_at_zero_forces_width a (Real.pi/2) ha (by positivity)
    (by nlinarith [Real.pi_pos]) h
  nlinarith [Real.pi_pos]

theorem twist_fails_at_three_half_width (a : ℝ) (ha : 0 < a) :
    multiplier a ((0 : ℂ)+I*(3*Real.pi/2 : ℝ)) ≠ star (multiplier a (0 : ℂ)) := by
  intro h
  have hw := twist_at_zero_forces_width a (3*Real.pi/2) ha (by positivity)
    (by nlinarith [Real.pi_pos]) h
  nlinarith [Real.pi_pos]

/-- A concrete failure of contraction for negative a, not a claim of failed isotony. -/
theorem negative_translation_breaks_strip_contraction (a : ℝ) (ha : a < 0) :
    1 < ‖multiplier a ((0 : ℂ)+I*(Real.pi/2 : ℝ))‖ := by
  have hm := multiplier_strip_norm a 0 (Real.pi/2)
  simp only [Complex.ofReal_zero] at hm
  rw [hm]
  simp only [Real.exp_zero, mul_one, Real.sin_pi_div_two]
  exact Real.one_lt_exp_iff.mpr (neg_pos.mpr ha)

theorem zero_translation_twist_all_widths (w x : ℝ) :
    multiplier 0 ((x : ℂ)+I*(w : ℂ)) = star (multiplier 0 (x : ℂ)) := by
  simp [multiplier]

#print axioms multiplier_real_norm_one
#print axioms sine_zero_unique_in_first_period
#print axioms twist_at_zero_forces_width
#print axioms twist_preserved_iff
#print axioms twist_fails_at_half_width
#print axioms twist_fails_at_three_half_width
#print axioms negative_translation_breaks_strip_contraction
#print axioms zero_translation_twist_all_widths
end ChatgptAudit.LightRayCore016


-- Engineering audit: all declarations introduced by this compilation unit.
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    let kind := match ci with
      | .axiomInfo _ => "axiom"
      | .thmInfo _ => "theorem"
      | .defnInfo _ => "definition"
      | _ => "generated_or_type"
    IO.println ("BENCH_DECL\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++
      String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    if kind == "axiom" then throwError "NEW_AXIOM_REFUSED: {n}"
