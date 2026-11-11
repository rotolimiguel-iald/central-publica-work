import Lean
import TGLExt.O16.TheEquationOfTruth_T20_v3
import TGL.FiniteThreeLocks
set_option autoImplicit false
noncomputable section
namespace ORDEM016.EquationOfTruth
variable {n : ℕ}
variable (Dc Db Dz : EuclideanSpace ℂ (Fin n) →ₗ[ℂ] EuclideanSpace ℂ (Fin n))

/-- Exact equality of operators; no claim about floating-point runtime operands. -/
theorem penalty_eq_kernel_H3L :
    (penalty ![Dc.toContinuousLinearMap,Db.toContinuousLinearMap,Dz.toContinuousLinearMap]).toLinearMap =
      TGL.FiniteThreeLocks.H3L Dc Db Dz := by
  ext x
  simp [penalty,Fin.sum_univ_three,TGL.FiniteThreeLocks.H3L,
    ← LinearMap.adjoint_toContinuousLinearMap]

theorem reading_eq_kernel_PF :
    reading (penalty ![Dc.toContinuousLinearMap,Db.toContinuousLinearMap,Dz.toContinuousLinearMap]) =
      TGL.FiniteThreeLocks.PF Dc Db Dz := by
  unfold reading TGL.FiniteThreeLocks.PF
  simp only [penalty_eq_kernel_H3L]

#print axioms penalty_eq_kernel_H3L
#print axioms reading_eq_kernel_PF
end ORDEM016.EquationOfTruth


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
