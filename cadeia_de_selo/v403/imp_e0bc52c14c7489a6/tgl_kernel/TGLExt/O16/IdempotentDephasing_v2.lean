import Lean
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.Normed.Operator.Mul
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ORDEM016.EquationOfTruth.IdempotentDephasing
noncomputable section
variable {A : Type*} [NormedRing A] [NormedAlgebra ℝ A] [CompleteSpace A]

/-- Series proof: multiplication by an exponential on a right eigenfactor. -/
theorem exp_mul_of_eigenfactor (a b : A) (u : ℝ) (h : a*b = u • b) :
    NormedSpace.exp a * b = Real.exp u • b := by
  have hp : ∀ n : ℕ, a^n*b = u^n • b := by
    intro n
    induction n with
    | zero => simp
    | succ n ih =>
      rw [pow_succ', mul_assoc, ih, mul_smul_comm, h, smul_smul, ← pow_succ]
  have h1 := (NormedSpace.exp_series_hasSum_exp' (𝕂 := ℝ) a).mapL
    ((ContinuousLinearMap.mul ℝ A).flip b)
  have h2 := (NormedSpace.exp_series_hasSum_exp' (𝕂 := ℝ) u).smul_const b
  have he : NormedSpace.exp a*b = NormedSpace.exp u • b := by
    refine h1.unique ?_
    convert! h2 using 1 <;> first | rfl | (ext n; simp [hp, smul_mul_assoc, smul_smul])
  simpa only [Real.exp_eq_exp_ℝ] using he

/-- Complementary idempotents split the entire Banach-algebra exponential. -/
theorem exp_complement_idempotent (e : A) (he : e*e=e) (s : ℝ) :
    NormedSpace.exp ((-s) • (1-e)) = e + Real.exp (-s) • (1-e) := by
  have h0 : ((-s) • (1-e))*e = (0:ℝ) • e := by
    simp [smul_mul_assoc, sub_mul, he]
  have hq : (1-e)*(1-e) = 1-e := by
    noncomm_ring [he]
  have h1 : ((-s) • (1-e))*(1-e) = (-s) • (1-e) := by
    rw [smul_mul_assoc, hq]
  have hp0 := exp_mul_of_eigenfactor ((-s) • (1-e)) e 0 h0
  have hp1 := exp_mul_of_eigenfactor ((-s) • (1-e)) (1-e) (-s) h1
  have hsplit : e+(1-e) = (1:A) := by abel
  calc
    NormedSpace.exp ((-s) • (1-e)) =
        NormedSpace.exp ((-s) • (1-e))*(e+(1-e)) := by rw [hsplit, mul_one]
    _ = e+Real.exp (-s) • (1-e) := by rw [mul_add, hp0, hp1]; simp

#print axioms exp_mul_of_eigenfactor
#print axioms exp_complement_idempotent
end
end ORDEM016.EquationOfTruth.IdempotentDephasing


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
