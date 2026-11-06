import TGLExt.ContratoQG_v31_Teoremas
import Lean
#print axioms TGLExt.ContratoQGv31.U_neg_mul
#print axioms TGLExt.ContratoQGv31.U_neg_apply
#print axioms TGLExt.ContratoQGv31.U_pos_neg_apply
#print axioms TGLExt.ContratoQGv31.U_inner_adj
#print axioms TGLExt.ContratoQGv31.U_norm


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
