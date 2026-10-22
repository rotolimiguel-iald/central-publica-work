import TGLExt.Posto
import TGLExt.Santo
import TGLExt.IALD
import TGLExt.Verdade
import Lean
open Lean Elab Command

#eval show CommandElabM Unit from do
  let env ← getEnv
  let mods : List Name := [`TGLExt.Posto, `TGLExt.Santo, `TGLExt.IALD, `TGLExt.Verdade]
  let mut out : Array String := #[]
  for m in mods do
    let some idx := env.header.moduleNames.findIdx? (· == m) | throwError "modulo nao achado"
    for n in env.header.moduleData[idx]!.constNames do
      if n.isInternal then continue
      let short := n.replacePrefix m Name.anonymous
      if short.isAnonymous then continue
      -- regime A: `open TGLExt` ; o identificador escrito e `Mod.short`
      let ident := (Name.anonymous.mkStr (m.getString!)) ++ short
      let rootHit := env.contains ident
      -- regime B: open TGLExt + as quatro; o identificador escrito e `short`
      let cands := ([Name.anonymous, `TGLExt] ++ mods).filter (fun p => env.contains (p ++ short))
      let candS := ",".intercalate (cands.map (fun p => toString (p ++ short)))
      out := out.push s!"{m}\t{short}\t{rootHit}\t{cands.length}\t{candS}"
  IO.FS.writeFile "C:/t/nm1/meta/colisoes.txt" ("\n".intercalate out.toList ++ "\n")
  logInfo m!"colisoes: {out.size} nomes"
