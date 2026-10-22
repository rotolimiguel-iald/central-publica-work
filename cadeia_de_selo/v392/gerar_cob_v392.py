# -*- coding: utf-8 -*-
"""gerar_cob_v392.py -- escreve Cob_v392.lean (enumeracao COB das declaracoes das pedras de STONES (14 na rodada 2), no formato da F_KERNEL/J1) FORA da arvore do kernel.
O arquivo usa run_cmd: e' instrumento de medida (nao entra no kernel nem no um.py). Uso: python -I -B -X utf8 gerar_cob_v392.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import v392_pedras as P
imps = "".join("import TGLExt.%s\n" % s["mod"] for s in P.STONES)
alvo = ", ".join("`TGLExt.%s" % s["mod"] for s in P.STONES)
lean = f"""-- COB v392 (cadeia v392, 13/10/2026): enumera as declaracoes das pedras de STONES (14 na rodada 2) e a cobertura de axiomas (collectAxioms). Instrumento de medida; so no sandbox.
import TGL
import TGLExt
{imps}
open Lean Elab Command

run_cmd do
  let env ← getEnv
  let alvo : List Name := [{alvo}]
  let mut n_decl := 0
  let mut n_thm := 0
  let mut n_fora := 0
  for (n, ci) in env.constants.map₁.toList do
    match env.getModuleIdxFor? n with
    | none => pure ()
    | some idx =>
      let m := env.header.moduleNames[idx.toNat]!
      if alvo.contains m then
        let axs ← liftCoreM (collectAxioms n)
        let kind : String := match ci with
          | .thmInfo _ => "thm" | .defnInfo _ => "def" | .axiomInfo _ => "AXIOM"
          | .opaqueInfo _ => "opaque" | .quotInfo _ => "quot" | .inductInfo _ => "induct"
          | .ctorInfo _ => "ctor" | .recInfo _ => "rec"
        n_decl := n_decl + 1
        if kind == "thm" then n_thm := n_thm + 1
        let ok := axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound)
        unless ok do n_fora := n_fora + 1
        IO.println ("COB\t" ++ m.toString ++ "\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++ (if ok then "TRIO" else "FORA") ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
  IO.println ("COB_TOTAL\tdecl=" ++ toString n_decl ++ "\tthm=" ++ toString n_thm ++ "\tfora_do_trio=" ++ toString n_fora)
"""
os.makedirs(os.path.join(HERE, "kernel"), exist_ok=True)
open(os.path.join(HERE, "kernel", "Cob_v392.lean"), "w", encoding="utf-8", newline="\n").write(lean)
print("Cob_v392.lean escrito;", len(P.STONES), "modulos")
