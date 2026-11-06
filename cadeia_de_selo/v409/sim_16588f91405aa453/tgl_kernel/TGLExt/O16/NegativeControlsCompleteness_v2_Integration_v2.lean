import Lean
import TGLExt.O16.TheEquationOfTruth_T20_controles_v3_Integration_v2

set_option autoImplicit false
namespace ORDEM016.EquationOfTruth.NegativeControls
open Matrix
open scoped ComplexOrder
noncomputable section

theorem constant_reader_always_conserved
    (F : ℝ → (Fin 2 → ℝ) → (Fin 2 → ℝ)) (s : ℝ) (x : Fin 2 → ℝ) :
    (fun _ : Fin 2 → ℝ => (1:ℝ)) (F s x) = (fun _ : Fin 2 → ℝ => (1:ℝ)) x := rfl

def invalidDensity : Matrix (Fin 2) (Fin 2) ℂ := !![1/2,3/5;3/5,1/2]

theorem invalidDensity_trace_one : Matrix.trace invalidDensity=1 := by
  norm_num [invalidDensity,Matrix.trace,Fin.sum_univ_two]

theorem invalidDensity_determinant : Matrix.det invalidDensity = -(11/100:ℂ) := by
  norm_num [invalidDensity,Matrix.det_fin_two]

theorem invalidDensity_not_positive : ¬ invalidDensity.PosSemidef := by
  intro hp
  have hq := hp.dotProduct_mulVec_nonneg (![1,-1] : Fin 2 → ℂ)
  norm_num [invalidDensity,Matrix.mulVec,dotProduct,Fin.sum_univ_two] at hq
  norm_num [Complex.le_def] at hq

#print axioms constant_reader_always_conserved
#print axioms invalidDensity_trace_one
#print axioms invalidDensity_determinant
#print axioms invalidDensity_not_positive
end
end ORDEM016.EquationOfTruth.NegativeControls


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
