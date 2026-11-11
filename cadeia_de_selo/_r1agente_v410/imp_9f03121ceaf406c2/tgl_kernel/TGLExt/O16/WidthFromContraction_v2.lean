import Lean
import TGLExt.O16.LightRayTwistWidth_v3

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open Complex
namespace ChatgptAudit.LightRayCore016

theorem positive_multiplier_expands_at_three_half_pi (a : ℝ) (ha : 0 < a) :
    1 < ‖multiplier a ((0 : ℂ) + I * (3 * Real.pi / 2 : ℝ))‖ := by
  have hm := multiplier_strip_norm a 0 (3 * Real.pi / 2)
  simp only [Complex.ofReal_zero] at hm
  rw [hm]
  have hs : Real.sin (3 * Real.pi / 2) = -1 := by
    rw [show 3 * Real.pi / 2 = Real.pi / 2 + Real.pi by ring,
      Real.sin_add_pi, Real.sin_pi_div_two]
  simp only [Real.exp_zero, mul_one, hs, mul_neg_one, neg_neg]
  exact Real.one_lt_exp_iff.mpr ha

/-- The first-period restriction is derived from contraction on the whole strip. -/
theorem full_strip_contraction_forces_first_period (a w : ℝ) (ha : 0 < a)
    (hcontract : ∀ y : ℝ, 0 ≤ y → y ≤ w →
      ‖multiplier a ((0 : ℂ) + I * (y : ℂ))‖ ≤ 1) :
    w < 2 * Real.pi := by
  by_contra hn
  have hw : 2 * Real.pi ≤ w := le_of_not_gt hn
  have hp := hcontract (3 * Real.pi / 2) (by positivity) (by linarith [Real.pi_pos])
  exact (not_lt_of_ge hp) (positive_multiplier_expands_at_three_half_pi a ha)

/-- No first-period hypothesis; the conjugate boundary remains essential. -/
theorem contraction_and_twist_force_width (a w : ℝ) (ha : 0 < a) (hw : 0 < w)
    (hcontract : ∀ y : ℝ, 0 ≤ y → y ≤ w →
      ‖multiplier a ((0 : ℂ) + I * (y : ℂ))‖ ≤ 1)
    (htwist : multiplier a ((0 : ℂ) + I * (w : ℂ)) = star (multiplier a (0 : ℂ))) :
    w = Real.pi :=
  twist_at_zero_forces_width a w ha hw
    (full_strip_contraction_forces_first_period a w ha hcontract) htwist

theorem contraction_and_boundary_iff_pi (a w : ℝ) (ha : 0 < a) (hw : 0 < w) :
    ((∀ x y : ℝ, 0 ≤ y → y ≤ w →
        ‖multiplier a ((x : ℂ) + I * (y : ℂ))‖ ≤ 1) ∧
     (∀ x : ℝ, multiplier a ((x : ℂ) + I * (w : ℂ)) =
        star (multiplier a (x : ℂ)))) ↔ w = Real.pi := by
  constructor
  · rintro ⟨hc, ht⟩
    exact contraction_and_twist_force_width a w ha hw (hc 0) (ht 0)
  · rintro rfl
    exact ⟨fun x y hy hp => multiplier_strip_contraction a x y ha.le hy hp,
      multiplier_twist a⟩

/-- Positivity and contraction alone do not determine the width. -/
theorem half_width_contracts_without_boundary (a : ℝ) (ha : 0 < a) :
    (∀ x y : ℝ, 0 ≤ y → y ≤ Real.pi / 2 →
      ‖multiplier a ((x : ℂ) + I * (y : ℂ))‖ ≤ 1) ∧
    multiplier a ((0 : ℂ) + I * (Real.pi / 2 : ℝ)) ≠
      star (multiplier a (0 : ℂ)) := by
  constructor
  · intro x y hy hp
    exact multiplier_strip_contraction a x y ha.le hy (by linarith [Real.pi_pos])
  · exact twist_fails_at_half_width a ha

#print axioms positive_multiplier_expands_at_three_half_pi
#print axioms full_strip_contraction_forces_first_period
#print axioms contraction_and_twist_force_width
#print axioms contraction_and_boundary_iff_pi
#print axioms half_width_contracts_without_boundary
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
