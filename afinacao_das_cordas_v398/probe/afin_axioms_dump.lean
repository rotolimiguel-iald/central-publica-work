import TGLExt.AfinacaoDasCordas

open Lean Meta Elab

run_meta do
  let env ← getEnv
  let some idx := env.getModuleIdx? `TGLExt.AfinacaoDasCordas | throwError "modulo ausente"
  let mut raw : Array Name := #[]
  for (n, _) in env.constants.map₁.toList do
    if env.getModuleIdxFor? n == some idx then
      raw := raw.push n
  let sorted := raw.qsort (fun a b => a.toString < b.toString)
  for n in sorted do
    let some ci := env.find? n | continue
    let kind := match ci with
      | .axiomInfo _ => "axiom"
      | .defnInfo _ => "def"
      | .thmInfo _ => "theorem"
      | .opaqueInfo _ => "opaque"
      | .quotInfo _ => "quot"
      | .inductInfo _ => "inductive"
      | .ctorInfo _ => "ctor"
      | .recInfo _ => "rec"
    let axs ← collectAxioms n
    let axStr := String.intercalate "," (axs.toList.map toString)
    logInfo m!"DECL|{n}|{kind}|{n.isInternal}|{axStr}"
