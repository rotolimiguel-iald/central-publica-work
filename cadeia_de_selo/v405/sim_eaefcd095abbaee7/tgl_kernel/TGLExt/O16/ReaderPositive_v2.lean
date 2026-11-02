import Lean
import TGLExt.O16.ExactTypeReader_v2
set_option autoImplicit false
namespace ChatgptAudit.ReaderControl
def identityWitness : Nat := 1
#assert_exact_type identityWitness : Nat
def preserve (n : Nat) : n = n := rfl
#assert_exact_type preserve : (n : Nat) → n = n
#print axioms identityWitness
#print axioms preserve
end ChatgptAudit.ReaderControl


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
