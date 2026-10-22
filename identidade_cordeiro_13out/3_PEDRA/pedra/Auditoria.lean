import TGLExt.TheIdentityHasAName
open Lean Elab Command

/-- Auditoria: TODAS as constantes do namespace TGLExt.TheIdentityHasAName (inclui as geradas), com collectAxioms. -/
elab "#auditar_identidade" : command => do
  let env ← getEnv
  let pre := `TGLExt.TheIdentityHasAName
  let mut nomes : Array Name := #[]
  for (c, _) in env.constants.toList do
    if pre.isPrefixOf c then nomes := nomes.push c
  nomes := nomes.qsort (fun a b => a.toString < b.toString)
  let mut fora : Nat := 0
  for c in nomes do
    let axs ← liftCoreM (Lean.collectAxioms c)
    if axs.isEmpty then
      logInfo m!"'{c}' does not depend on any axioms"
    else
      logInfo m!"'{c}' depends on axioms: {axs.toList}"
    if axs.any (fun a => a != ``propext && a != ``Classical.choice && a != ``Quot.sound) then fora := fora + 1
  logInfo m!"AUDITORIA: {nomes.size} constantes; fora do trio: {fora}"

#auditar_identidade
