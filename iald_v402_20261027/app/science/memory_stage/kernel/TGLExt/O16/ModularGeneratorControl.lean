import Lean
import TGLExt.ContinuousModularZero
import Mathlib.LinearAlgebra.Matrix.Notation

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ORDEM016.EquationOfTruth.ModularGeneratorControl
open Matrix NormedSpace
open scoped ComplexOrder MatrixOrder
noncomputable section
variable {n : Type} [Fintype n] [DecidableEq n]

/-- Vanishing of the generator on y is commutation with rho for a positive definite rho. -/
theorem modularGen_zero_iff_commute (ρ y : Matrix n n ℂ) (hρ : ρ.PosDef) :
    TGLExt.modularGen ρ y = 0 ↔ Commute ρ y := by
  constructor
  · intro h
    have hc : Commute (TGLExt.logRho ρ) y := by
      show TGLExt.logRho ρ*y = y*TGLExt.logRho ρ
      exact (sub_eq_zero.mp h).symm
    have he := hc.exp_left
    rwa [TGLExt.exp_logRho ρ hρ] at he
  · intro hc
    have hl := hc.cfc_real Real.log
    unfold TGLExt.modularGen TGLExt.logRho
    rw [hl.eq, sub_self]

theorem scalar_modularGen_zero (c : ℂ) (y : Matrix n n ℂ) :
    TGLExt.modularGen (c • (1:Matrix n n ℂ)) y = 0 := by
  have hc : Commute (c • (1:Matrix n n ℂ)) y := by
    show (c • (1:Matrix n n ℂ))*y = y*(c • (1:Matrix n n ℂ))
    simp [smul_mul_assoc, mul_smul_comm]
  have hl := hc.cfc_real Real.log
  unfold TGLExt.modularGen TGLExt.logRho
  rw [hl.eq, sub_self]

def rhoExample : Matrix (Fin 2) (Fin 2) ℂ := diagonal ![1/3,2/3]
def matrixUnit : Matrix (Fin 2) (Fin 2) ℂ := !![0,1;0,0]

theorem rhoExample_posDef : rhoExample.PosDef := by
  rw [rhoExample, Matrix.posDef_diagonal_iff]
  intro i
  fin_cases i <;> norm_num

theorem rhoExample_trace : Matrix.trace rhoExample = 1 := by
  norm_num [rhoExample, Matrix.trace, Fin.sum_univ_two]

theorem example_generator_nonzero : TGLExt.modularGen rhoExample matrixUnit ≠ 0 := by
  intro hz
  have hc := (modularGen_zero_iff_commute rhoExample matrixUnit rhoExample_posDef).mp hz
  have he := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℂ => M 0 1) hc.eq
  norm_num [rhoExample, matrixUnit, Matrix.mul_apply, Fin.sum_univ_two] at he

theorem exists_normalized_nonzero_generator :
    ∃ ρ : Matrix (Fin 2) (Fin 2) ℂ, ρ.PosDef ∧ Matrix.trace ρ=1 ∧ TGLExt.modularGen ρ ≠ 0 := by
  refine ⟨rhoExample, rhoExample_posDef, rhoExample_trace, ?_⟩
  intro h
  apply example_generator_nonzero
  exact congrFun h matrixUnit

#print axioms modularGen_zero_iff_commute
#print axioms scalar_modularGen_zero
#print axioms rhoExample_posDef
#print axioms rhoExample_trace
#print axioms example_generator_nonzero
#print axioms exists_normalized_nonzero_generator
end
end ORDEM016.EquationOfTruth.ModularGeneratorControl


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
