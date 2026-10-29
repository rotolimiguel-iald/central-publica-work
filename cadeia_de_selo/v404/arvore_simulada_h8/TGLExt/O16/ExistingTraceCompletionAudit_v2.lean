import Lean
import TGLExt.V354RegularLegacyWitness

/- Read-only audit of existing declarations. No replacement trace or new theorem. -/
#check TGLV354.TraceCompletion.cyclicTraceCandidate_cyclic
#check TGLV354.TraceCompletion.cyclicTraceCandidate_positive
#check TGLV354.TraceCompletion.regularLegacyCore
#print axioms TGLV354.TraceCompletion.cyclicTraceCandidate_cyclic
#print axioms TGLV354.TraceCompletion.cyclicTraceCandidate_positive
#print axioms TGLV354.TraceCompletion.regularLegacyCore


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
