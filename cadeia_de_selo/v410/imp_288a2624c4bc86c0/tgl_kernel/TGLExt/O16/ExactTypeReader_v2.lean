import Lean
import Lean

open Lean Elab Command Term Meta

/- Engineering prototype. The caller must pin the contract, closed indices,
candidate declaration and this checker. Success is not ratification. -/
elab "#assert_exact_type " candidate:ident " : " expected:term : command => do
  liftTermElabM do
    let name ← realizeGlobalConstNoOverloadWithInfo candidate
    let value ← mkConstWithFreshMVarLevels name
    let actual ← inferType value
    let target ← elabType expected
    synthesizeSyntheticMVarsNoPostponing
    let actual ← instantiateMVars actual
    let target ← instantiateMVars target
    if actual.hasFVar || target.hasFVar || actual.hasMVar || target.hasMVar then
      throwError "EXACT_TYPE_OPEN_CONTEXT: closed indices and a closed declaration are required"
    unless ← isDefEq actual target do
      throwError "EXACT_TYPE_MISMATCH: {name} has type {actual}, expected {target}"
    logInfo m!"EXACT_TYPE_ACCEPTED: {name} : {target}"


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
