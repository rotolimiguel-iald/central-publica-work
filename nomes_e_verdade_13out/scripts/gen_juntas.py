# -*- coding: utf-8 -*-
"""Gera, em C:/t/nm1/meta: CtlSorry.lean (controle positivo do contador de sorry), Colisoes.lean (varredura no kernel dos nomes
curtos das quatro pedras nos regimes de open), Juntas_A.lean (import das quatro + `open TGLExt` + #check de cada nome publico
qualificado) e AmbControle.lean (controle positivo: `open TGLExt TGLExt.IALD` + `#check @dephase` TEM de dar ambiguidade)."""
import re
M = "C:/t/nm1/meta/"
MODS = {"Posto": "posto_new", "Santo": "santo_new", "IALD": "iald_new", "Verdade": "verdade_new"}
IMPORTS = "".join("import TGLExt.%s\n" % m for m in MODS)
open(M + "CtlSorry.lean", "w", encoding="utf-8", newline="\n").write(
    "theorem ctl_sorry : (1 : Nat) = 2 := sorry\n#print axioms ctl_sorry\n")
col = IMPORTS + r'''import Lean
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
'''
open(M + "Colisoes.lean", "w", encoding="utf-8", newline="\n").write(col)
pub = []
for m, tag in MODS.items():
    for ln in open(M + "meta_%s.txt" % tag, encoding="utf-8"):
        if not ln.startswith("DECL\t"):
            continue
        parts = ln.rstrip("\n").split("\t")
        n, internal = parts[1], parts[3] == "true"
        if internal or re.search(r"\.eq_\d+$", n) or "._" in n:
            continue
        short = n[len("TGLExt." + m + "."):]
        if not n.startswith("TGLExt." + m + "."):
            continue
        # evita rec/casesOn/recOn/noConfusion de estruturas (geradores) e abbreviations nao chec aveis sem ajuda
        pub.append(m + "." + short)
open(M + "Juntas_A.lean", "w", encoding="utf-8", newline="\n").write(
    IMPORTS + "\nopen TGLExt\n\n" + "".join("#check @%s\n" % p for p in pub))
open(M + "AmbControle.lean", "w", encoding="utf-8", newline="\n").write(
    IMPORTS + "\nopen TGLExt TGLExt.IALD\n\n#check @dephase\n")
print("ok", len(pub), "nomes publicos")
