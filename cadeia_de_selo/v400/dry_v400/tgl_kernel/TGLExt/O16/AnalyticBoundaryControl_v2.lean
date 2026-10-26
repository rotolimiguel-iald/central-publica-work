import Lean
import Mathlib.Analysis.Complex.Hadamard
import Mathlib.Tactic

/-! Shared analytic control for A-1.b3/b4; no physical witness is assumed here. -/
namespace ChatgptAudit.AnalyticBoundary
open Complex Complex.HadamardThreeLines Set
noncomputable section

theorem vertical_zero_of_zero_edge {f : ℂ → ℂ} {b : ℝ} (hb : 0 < b)
    (hd : DiffContOnCl ℂ f (verticalStrip 0 b))
    (hbound : ∃ M : ℝ, ∀ z : ℂ, 0 ≤ z.re → z.re ≤ b → ‖f z‖ ≤ M)
    (hedge : ∀ z : ℂ, z.re = 0 → f z = 0)
    {z : ℂ} (hz0 : 0 ≤ z.re) (hzb : z.re < b) : f z = 0 := by
  obtain ⟨M, hM⟩ := hbound
  have hbdd : BddAbove ((norm ∘ f) '' verticalClosedStrip 0 b) := by
    refine ⟨M, ?_⟩
    rintro y ⟨w, hw, rfl⟩
    exact hM w hw.1 hw.2
  have he : 0 < 1 - z.re / b := by
    have : z.re / b < 1 := (div_lt_one hb).2 hzb
    linarith
  have hn := norm_le_interp_of_mem_verticalClosedStrip' (f := f)
    (a := 0) (b := M) hb ⟨hz0, hzb.le⟩ hd hbdd
    (fun w hw => by simp [hedge w hw])
    (fun w hw => hM w (by change w.re = b at hw; linarith) (by change w.re = b at hw; exact hw.le))
  simp only [sub_zero, Real.zero_rpow (ne_of_gt he), zero_mul] at hn
  exact norm_le_zero_iff.mp hn

theorem horizontal_zero_of_zero_edge {f : ℂ → ℂ} {b : ℝ} (hb : 0 < b)
    (hd : DiffContOnCl ℂ f {z : ℂ | 0 < z.im ∧ z.im < b})
    (hbound : ∃ M : ℝ, ∀ z : ℂ, 0 ≤ z.im → z.im ≤ b → ‖f z‖ ≤ M)
    (hedge : ∀ z : ℂ, z.im = 0 → f z = 0)
    {z : ℂ} (hz0 : 0 ≤ z.im) (hzb : z.im < b) : f z = 0 := by
  let g : ℂ → ℂ := fun w => f (I * w)
  have hdg : DiffContOnCl ℂ g (verticalStrip 0 b) := by
    apply hd.comp (differentiable_id.const_mul I).diffContOnCl
    intro w hw
    simpa [verticalStrip, mul_im] using hw
  have hbg : ∃ M : ℝ, ∀ w : ℂ, 0 ≤ w.re → w.re ≤ b → ‖g w‖ ≤ M := by
    obtain ⟨M, hM⟩ := hbound
    exact ⟨M, fun w h0 h1 => hM (I * w) (by simpa using h0) (by simpa using h1)⟩
  have hzg : ∀ w : ℂ, w.re = 0 → g w = 0 := by
    intro w hw
    exact hedge (I * w) (by simpa using hw)
  have h := vertical_zero_of_zero_edge hb hdg hbg hzg
    (z := -I * z) (by simpa using hz0) (by simpa using hzb)
  simpa [g, ← mul_assoc] using h

#print axioms vertical_zero_of_zero_edge
#print axioms horizontal_zero_of_zero_edge
end
end ChatgptAudit.AnalyticBoundary


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
