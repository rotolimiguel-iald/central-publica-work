import Lean
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Data.ENNReal.Basic
import Mathlib.Tactic

set_option autoImplicit false
namespace ChatgptAudit.TraceInfinity016
open Matrix
noncomputable section

abbrev M := Matrix (Fin 2) (Fin 2) ℝ
def X : M := !![1,1;0,1]
def P : M := !![1,0;0,0]
def Positive (A : M) : Prop :=
  A.transpose = A ∧ ∀ v : Fin 2 → ℝ, 0 ≤ dotProduct v (A.mulVec v)
def tau (A : M) : ENNReal := by
  classical
  exact if Positive A then ENNReal.ofReal (Matrix.trace A) else ⊤

theorem xp_eq_p : X * P = P := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [X,P,Matrix.mul_apply,Fin.sum_univ_two]

theorem px_not_symmetric : (P * X).transpose ≠ P * X := by
  intro h
  have he := congrArg (fun A : M => A 0 1) h
  norm_num [X,P,Matrix.mul_apply,Fin.sum_univ_two,Matrix.transpose_apply] at he

theorem p_positive : Positive P := by
  constructor
  · ext i j
    fin_cases i <;> fin_cases j <;> norm_num [P,Matrix.transpose_apply]
  · intro v
    simpa [P,dotProduct,Matrix.mulVec,Fin.sum_univ_two,pow_two] using sq_nonneg (v 0)

theorem tau_xp : tau (X*P) = 1 := by
  rw [xp_eq_p]
  unfold tau
  rw [if_pos p_positive]
  norm_num [Matrix.trace,P,Fin.sum_univ_two]

theorem tau_px : tau (P*X) = ⊤ := by
  have hn : ¬ Positive (P*X) := fun h => px_not_symmetric h.1
  simp [tau,hn]

theorem infinity_extension_not_cyclic : ¬ ∀ A B : M, tau (A*B) = tau (B*A) := by
  intro h
  have ht := h X P
  rw [tau_xp,tau_px] at ht
  exact ENNReal.one_ne_top ht

#print axioms xp_eq_p
#print axioms px_not_symmetric
#print axioms p_positive
#print axioms tau_xp
#print axioms tau_px
#print axioms infinity_extension_not_cyclic
end
end ChatgptAudit.TraceInfinity016


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
