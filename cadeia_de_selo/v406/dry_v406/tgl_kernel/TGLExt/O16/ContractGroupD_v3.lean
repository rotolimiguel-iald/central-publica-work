import TGLExt.ContratoQG_v31_Teoremas
import Lean
#print axioms TGLExt.ContratoQGv31.translate_null_subset
#print axioms TGLExt.ContratoQGv31.halfsided_inclusion
#print axioms TGLExt.ContratoQGv31.ContratoH2.contract_borchers_form
#print axioms TGLExt.ContratoQGv31.positiveEnergy_orientation
#print axioms TGLExt.ContratoQGv31.KMSAt.rescale


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
