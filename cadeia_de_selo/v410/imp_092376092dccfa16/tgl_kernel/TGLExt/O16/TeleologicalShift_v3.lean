import Lean
import TGLExt.O16.TeleologicalTail_v3
import Mathlib.MeasureTheory.Group.Integral

set_option autoImplicit false
noncomputable section
open MeasureTheory Set
namespace ChatgptAudit.Teleological016

theorem tail_shift (f : ℝ → ℝ) (l : ℝ) :
    (∫ u : ℝ in Ioi 0, f (l+u))=tail f l := by
  have h := integral_add_left_eq_self (μ := volume) ((Ioi l).indicator f) l
  have heq : (fun u => (Ioi l).indicator f (l+u)) =
      (Ioi (0:ℝ)).indicator (fun u => f (l+u)) := by
    funext u
    by_cases hu : 0 < u
    · rw [indicator_of_mem (by exact show l < l+u by linarith),indicator_of_mem (show u ∈ Ioi (0:ℝ) from hu)]
    · rw [indicator_of_notMem (by exact show ¬ l < l+u by linarith),indicator_of_notMem (show u ∉ Ioi (0:ℝ) from hu)]
  rw [heq,integral_indicator measurableSet_Ioi,integral_indicator measurableSet_Ioi] at h
  exact h

theorem weighted_tail_shift (f : ℝ → ℝ) (l : ℝ) :
    (∫ u : ℝ in Ioi 0, u*f (l+u))=weightedTail f l := by
  have h := tail_shift (fun v => (v-l)*f v) l
  simpa only [add_sub_cancel_left,tail,weightedTail] using h

#print axioms tail_shift
#print axioms weighted_tail_shift
end ChatgptAudit.Teleological016


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
