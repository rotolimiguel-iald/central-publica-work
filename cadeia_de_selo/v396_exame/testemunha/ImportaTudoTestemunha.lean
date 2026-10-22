import TGL
import TGLExt
import TGLExt.TestemunhaEstatica

open Lean in
run_meta do
  let env ← getEnv
  let some idx := env.getModuleIdx? `TGLExt.TestemunhaEstatica | throwError "modulo ausente"
  let mut n := 0
  let mut fora : Array Name := #[]
  for (c, _) in env.constants.map₁.toList do
    if env.getModuleIdxFor? c == some idx then
      n := n + 1
      if !((`TGLExt.TestemunhaEstatica).isPrefixOf c) && !c.isInternal then
        fora := fora.push c
  IO.println s!"IMPORTA_TUDO_OK modulos={env.header.moduleNames.size} decls_do_modulo={n}"
  for c in fora do
    IO.println s!"FORA_DO_NAMESPACE {c}"
