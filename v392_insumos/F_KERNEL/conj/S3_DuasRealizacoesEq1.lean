-- SONDA 3: dois modulos que realizaram TGLExt.conjJ.eq_1 (TheLightReadsItself e Sonda.EqRealizada2), juntos
import TGLExt.TheLightReadsItself
import TGLExt.Sonda.EqRealizada2
open Lean Elab Command
run_cmd do
  let env ← getEnv
  for n in [`TGLExt.conjJ.eq_1, `TGLExt.conjJ.eq_def] do
    let m := match env.getModuleIdxFor? n with
      | some idx => (env.header.moduleNames[idx.toNat]!).toString
      | none => "-"
    IO.println ("SONDA_DUAS\t" ++ n.toString ++ "\tcontem=" ++ toString (env.contains n) ++ "\tmodulo=" ++ m)
