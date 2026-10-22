-- KH-N1, D2 passo 1 (exame F_KERNEL, 12/10/2026, so sandbox): enumera TODAS as constantes do fecho TGL + TGLExt
-- (modulo de origem, nome, tipo de constante). Nao calcula axiomas.
import TGL
import TGLExt
open Lean Elab Command
run_cmd do
  let env ← getEnv
  let mods := env.header.moduleNames
  let mut nm := 0
  for m in mods do
    if m.getRoot == `TGL || m.getRoot == `TGLExt then
      nm := nm + 1
      IO.println ("MOD\t" ++ m.toString)
  IO.println ("MOD_TOTAL\t" ++ toString nm)
  let mut n := 0
  for (c, ci) in env.constants.map₁.toList do
    match env.getModuleIdxFor? c with
    | none => pure ()
    | some idx =>
      let m := mods[idx.toNat]!
      if m.getRoot == `TGL || m.getRoot == `TGLExt then
        let kind : String := match ci with
          | .thmInfo _ => "thm" | .defnInfo _ => "def" | .axiomInfo _ => "AXIOM"
          | .opaqueInfo _ => "opaque" | .quotInfo _ => "quot" | .inductInfo _ => "induct"
          | .ctorInfo _ => "ctor" | .recInfo _ => "rec"
        n := n + 1
        IO.println ("CONST\t" ++ m.toString ++ "\t" ++ c.toString ++ "\t" ++ kind)
  IO.println ("CONST_TOTAL\t" ++ toString n)
