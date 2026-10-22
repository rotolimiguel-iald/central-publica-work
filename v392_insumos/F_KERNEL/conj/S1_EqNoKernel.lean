-- SONDA: o kernel v391 inteiro ja contem TGLExt.conjJ.eq_1 / TGLExt.adU.eq_1 (sem realizar agora)?
import TGL
import TGLExt
open Lean Elab Command
run_cmd do
  let env ← getEnv
  for n in [`TGLExt.conjJ.eq_1, `TGLExt.adU.eq_1, `TGLExt.conjJ, `TGLExt.adU] do
    let m := match env.getModuleIdxFor? n with
      | some idx => (env.header.moduleNames[idx.toNat]!).toString
      | none => "-"
    IO.println ("SONDA_EQ\t" ++ n.toString ++ "\tcontem=" ++ toString (env.contains n) ++ "\tmodulo=" ++ m)
