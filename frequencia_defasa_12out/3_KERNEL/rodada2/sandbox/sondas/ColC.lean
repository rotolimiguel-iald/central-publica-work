/- SONDA de instalação (rodada 2; NÃO é pedra): de qual módulo vem `TGLExt.rhoOut.eq_1` quando se importa SÓ o
   vizinho ColA, e quando se importam ColA e a pedra juntos (os dois realizaram a equação). -/
import ColA
import TheUnitIsTheRank

open Lean in
#eval show CoreM Unit from do
  let env ← getEnv
  let n := `TGLExt.rhoOut.eq_1
  let mods := env.header.moduleNames
  let mut achou : Array Name := #[]
  for i in [0:mods.size] do
    let names := (env.header.moduleData[i]!).constNames
    if names.contains n then
      achou := achou.push mods[i]!
  IO.println s!"MODULOS_COM|{n}|{achou.toList}"
  IO.println s!"NO_AMBIENTE|{env.contains n}"
