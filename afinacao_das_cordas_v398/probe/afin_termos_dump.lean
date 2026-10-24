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
    let th := ci.type.hash
    let vh := match ci with
      | .defnInfo d => toString d.value.hash
      | .thmInfo t => toString t.value.hash
      | .opaqueInfo o => toString o.value.hash
      | _ => "-"
    logInfo m!"TERMO|{n}|{th}|{vh}"
