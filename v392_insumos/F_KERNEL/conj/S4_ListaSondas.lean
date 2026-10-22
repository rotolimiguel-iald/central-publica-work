-- SONDA 4: o que os modulos-sonda exportam (constantes por modulo de origem)
import TGLExt.Sonda.EqRealizada
import TGLExt.Sonda.EqRealizada2
open Lean Elab Command
run_cmd do
  let env ← getEnv
  for (n, _) in env.constants.map₁.toList do
    match env.getModuleIdxFor? n with
    | none => pure ()
    | some idx =>
      let m := env.header.moduleNames[idx.toNat]!
      if m == `TGLExt.Sonda.EqRealizada || m == `TGLExt.Sonda.EqRealizada2 then
        IO.println ("SONDA_LISTA\t" ++ m.toString ++ "\t" ++ n.toString)
