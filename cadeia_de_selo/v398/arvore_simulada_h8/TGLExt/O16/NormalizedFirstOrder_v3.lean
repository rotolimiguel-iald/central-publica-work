import Lean
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Tactic

set_option autoImplicit false
namespace ChatgptAudit.NormalizedFirstOrder016
noncomputable section

def reading (a b c r ε : ℝ) : ℝ := (a + 2*b*ε + c*ε^2)/(1+r*ε^2)

theorem reading_hasDerivAt (a b c r : ℝ) :
    HasDerivAt (reading a b c r) (2*b) 0 := by
  have hu : HasDerivAt (fun ε : ℝ => a+2*b*ε+c*ε^2) (2*b) 0 := by
    have h := ((hasDerivAt_const (0:ℝ) a).add
      ((hasDerivAt_id (0:ℝ)).const_mul (2*b))).add
      (((hasDerivAt_id (0:ℝ)).pow 2).const_mul c)
    exact h.congr_deriv (by norm_num)
  have hv : HasDerivAt (fun ε : ℝ => 1+r*ε^2) 0 0 := by
    have h := (hasDerivAt_const (0:ℝ) (1:ℝ)).add
      (((hasDerivAt_id (0:ℝ)).pow 2).const_mul r)
    exact h.congr_deriv (by norm_num)
  exact (hu.div hv (by norm_num)).congr_deriv (by norm_num)

theorem reading_deriv (a b c r : ℝ) : deriv (reading a b c r) 0 = 2*b :=
  (reading_hasDerivAt a b c r).deriv

theorem no_linear_term_iff (a b c r : ℝ) :
    deriv (reading a b c r) 0 = 0 ↔ b = 0 := by
  rw [reading_deriv]
  constructor
  · intro h
    linarith
  · rintro rfl
    ring

theorem normalized_bilateral_hasDerivAt (k r : ℝ) :
    HasDerivAt (fun ε : ℝ => k*ε^2/(1+r*ε^2)) 0 0 := by
  have hf : reading 0 0 k r = (fun ε : ℝ => k*ε^2/(1+r*ε^2)) := by
    funext ε
    simp [reading]
  rw [← hf]
  exact (reading_hasDerivAt 0 0 k r).congr_deriv (by ring)

theorem pair_example_derivative :
    deriv (reading 0 (-(Real.sqrt 2)/3) 4 1) 0 = -(2*Real.sqrt 2)/3 := by
  rw [reading_deriv]
  ring

theorem pair_example_derivative_ne_zero :
    deriv (reading 0 (-(Real.sqrt 2)/3) 4 1) 0 ≠ 0 := by
  rw [pair_example_derivative]
  have hp : 0 < Real.sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
  apply ne_of_lt
  nlinarith

#print axioms reading_hasDerivAt
#print axioms reading_deriv
#print axioms no_linear_term_iff
#print axioms normalized_bilateral_hasDerivAt
#print axioms pair_example_derivative
#print axioms pair_example_derivative_ne_zero
end
end ChatgptAudit.NormalizedFirstOrder016


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
