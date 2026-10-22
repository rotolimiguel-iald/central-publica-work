-- SONDA P1b: o fecho de imports SO da PALAVRA contem os modulos da letra (ExactWitness, WordExistence, InfiniteWord)?
import TGLExt.Palavra
open Lean Elab Command
run_cmd do
  let env ← getEnv
  let ms := env.header.moduleNames
  for m in [`TGLExt.ExactWitness, `TGLExt.WordExistence, `TGLExt.InfiniteWord, `TGLExt.TheObserverReadsTheAngle,
            `TGLExt.O16.PeriodHeatCalibration_v3, `TGLExt.O16.RotationGeneratorBridges] do
    IO.println ("FECHO_PALAVRA\t" ++ m.toString ++ "\t" ++ toString (ms.contains m))
  IO.println ("FECHO_PALAVRA_N_MODULOS\t" ++ toString ms.size)
  for c in [`TGLExt.exact_witness_of_annihilating_word, `TGLExt.annihilating_word_exists] do
    IO.println ("FECHO_PALAVRA_CONST\t" ++ c.toString ++ "\t" ++ toString (env.contains c))
