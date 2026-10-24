import Lean
import TGLExt.O16.BoostHomonymBridge
import TGLExt.ApproximateBoostFlow
import TGLExt.BisognanoWichmann

set_option autoImplicit false
set_option maxHeartbeats 2000000

/-! A-2.1.2--4. Bridges between the actual imported declarations.
No new definition is substituted for a pre-existing boost.
The 0--3 boost has an inverse rapidity and a coordinate permutation.
Equality of entries of the 2x2 block does not identify all metric conventions.
-/
namespace ChatgptAudit.BoostBridges016
open Matrix TGLExt ChatgptAudit.Boost044
noncomputable section

def swap13 : Matrix (Fin 4) (Fin 4) ℝ :=
  !![1,0,0,0; 0,0,0,1; 0,0,1,0; 0,1,0,0]

theorem swap13_involutive : swap13 * swap13 = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [swap13, Matrix.mul_apply, Fin.sum_univ_four]

theorem even_is_cosh (rate s : ℝ) : boostEven rate s = Real.cosh (-(rate*s)) := by
  simp [boostEven, Real.cosh_eq, neg_mul]

theorem odd_is_sinh (rate s : ℝ) : boostOdd rate s = Real.sinh (-(rate*s)) := by
  simp [boostOdd, Real.sinh_eq, neg_mul]

theorem boostMatrix_eq_conjugated_boostMat (rate s : ℝ) :
    boostMatrix rate s = swap13 * boostMat (-(rate*s)) * swap13 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [boostMatrix, swap13, boostMat, Matrix.mul_apply, Fin.sum_univ_four,
      even_is_cosh, odd_is_sinh]

theorem boost_is_first_block (s : ℝ) (i j : Fin 2) :
    boost s i j = boostMat s (Fin.castLE (by decide : 2 ≤ 4) i)
      (Fin.castLE (by decide : 2 ≤ 4) j) := by
  fin_cases i <;> fin_cases j <;> simp [boost,boostMat]

theorem boost4_group (s t : ℝ) : boost4 (s+t) = boost4 s * boost4 t := by
  simp only [W5Final.boost4_eq_boostMat]
  exact (congrArg Subtype.val (theBoost_add s t)).symm

theorem boost4_identity : boost4 0 = 1 := by
  rw [W5Final.boost4_eq_boostMat]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [boostMat]

#print axioms swap13_involutive
#print axioms even_is_cosh
#print axioms odd_is_sinh
#print axioms boostMatrix_eq_conjugated_boostMat
#print axioms boost_is_first_block
#print axioms boost4_group
#print axioms boost4_identity
end
end ChatgptAudit.BoostBridges016


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
