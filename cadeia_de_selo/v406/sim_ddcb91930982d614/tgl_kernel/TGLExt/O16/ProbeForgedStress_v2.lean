import Lean
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.Data.Fin.VecNotation
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/-!
A-1.b2: independent algebraic control, NOT an inhabitant of ContratoH3 v3.1.
The full contract reproduction hit the prescribed memory limit. These lemmas
isolate the transverse ambiguity in the actual null contraction n=(1,1,0,0).
No assertion of locality/nonlocality follows solely from a matrix of expectations.
-/
namespace ChatgptAudit.ForgedStress
noncomputable section
abbrev Tensor := Matrix (Fin 4) (Fin 4) ℝ
def nullVector : Fin 4 → ℝ := ![1, 1, 0, 0]
def nullRead (T : Tensor) : ℝ := dotProduct nullVector (T.mulVec nullVector)
def transverseSkew (a : ℝ) : Tensor := fun i j =>
  if i = 2 ∧ j = 3 then a else if i = 3 ∧ j = 2 then -a else 0
def forge (T : Tensor) (a : ℝ) : Tensor := T + transverseSkew a
def symmetrize (T : Tensor) : Tensor := fun i j => (T i j + T j i) / 2

theorem nullRead_entries (T : Tensor) :
    nullRead T = T 0 0 + T 0 1 + T 1 0 + T 1 1 := by
  simp [nullRead, nullVector, Matrix.mulVec, dotProduct, Fin.sum_univ_four]
  <;> ring

theorem forge_preserves_nullRead (T : Tensor) (a : ℝ) :
    nullRead (forge T a) = nullRead T := by
  simp [nullRead_entries, forge, transverseSkew, Matrix.add_apply]

theorem symmetrize_forge (T : Tensor) (a : ℝ) :
    symmetrize (forge T a) = symmetrize T := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [symmetrize, forge, transverseSkew, Matrix.add_apply] <;> ring

theorem symmetrize_of_symmetric (T : Tensor) (h : T.transpose = T) :
    symmetrize T = T := by
  ext i j
  have hij : T j i = T i j := congrFun (congrFun h i) j
  simp [symmetrize, hij]

theorem forge_not_symmetric (T : Tensor) (h : T.transpose = T)
    (a : ℝ) (ha : a ≠ 0) : (forge T a).transpose ≠ forge T a := by
  intro hf
  have hT : T 3 2 = T 2 3 := congrFun (congrFun h 2) 3
  have hF : forge T a 3 2 = forge T a 2 3 := congrFun (congrFun hf 2) 3
  simp [forge, transverseSkew, Matrix.add_apply] at hF
  apply ha
  linarith

theorem charge_unchanged {X : Type} (T : X → Tensor) (a : X → ℝ)
    (charge : (X → ℝ) → ℝ) :
    charge (fun x => nullRead (forge (T x) (a x))) =
      charge (fun x => nullRead (T x)) := by
  congr 1
  funext x
  exact forge_preserves_nullRead (T x) (a x)

#print axioms nullRead_entries
#print axioms forge_preserves_nullRead
#print axioms symmetrize_forge
#print axioms symmetrize_of_symmetric
#print axioms forge_not_symmetric
#print axioms charge_unchanged
end
end ChatgptAudit.ForgedStress


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
