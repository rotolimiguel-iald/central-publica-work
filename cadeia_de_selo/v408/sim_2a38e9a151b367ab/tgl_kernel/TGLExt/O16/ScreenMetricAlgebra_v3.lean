import Lean
import Mathlib.Data.Matrix.Mul
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Ring

set_option autoImplicit false
namespace ChatgptAudit.ScreenMetric016

def screenMetric (a : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  Matrix.diagonal ![0,0,-a,-a]

theorem screenMetric_zero : screenMetric 0 = 0 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [screenMetric,Matrix.diagonal]

theorem screenMetric_symmetric (a : ℝ) : Matrix.transpose (screenMetric a)=screenMetric a := by
  simp [screenMetric]

theorem screenMetric_gauge (a : ℝ) : (screenMetric a).mulVec ![1,1,0,0]=0 := by
  ext i
  rw [screenMetric,Matrix.mulVec_diagonal]
  fin_cases i <;> simp

theorem screenMetric_area (a : ℝ) :
    -((screenMetric a) 2 2+(screenMetric a) 3 3)/2=a := by
  change -(-a + -a)/2=a
  ring

#print axioms screenMetric_zero
#print axioms screenMetric_symmetric
#print axioms screenMetric_gauge
#print axioms screenMetric_area
end ChatgptAudit.ScreenMetric016


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
