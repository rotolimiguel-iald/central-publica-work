import TGLExt.ContratoQG_v31_Teoremas
import Lean
#print axioms TGLExt.ContratoQGv31.ContratoH2.Δit_vac
#print axioms TGLExt.ContratoQGv31.ContratoH2.bw_covariance
#print axioms TGLExt.ContratoQGv31.ContratoH2.poincare_relation
#print axioms TGLExt.ContratoQGv31.ContratoH2.translates
#print axioms TGLExt.ContratoQGv31.ContratoH2.eigen_null_correlation_dilation
#print axioms TGLExt.ContratoQGv31.ContratoH2.no_point_spectrum


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
