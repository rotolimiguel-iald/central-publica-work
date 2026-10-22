import Lean
import TGLExt.TheContourOfTruth
#print axioms TGLExt.self_reference_witnesses_everything
#print axioms TGLExt.self_reference_cannot_discriminate
#print axioms TGLExt.the_mirror_can_differ
#print axioms TGLExt.polarization_is_degenerate_iff_fixed
#print axioms TGLExt.truth_is_not_static_equality
#print axioms TGLExt.the_criterion_can_fail
#print axioms TGLExt.witnessing_is_not_being


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
