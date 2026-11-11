# -*- coding: utf-8 -*-
"""Revisor terceiro v410 (R1): gera axiomas_terceiro_v410.lean = #print axioms das 60 ancoras (as 22 de IALD2 e as 38 de AEscala, lidas dos arquivos da pedra EMBUTIDA no
candidato, nao de memoria) + varredura MetaM de TODA constante dos 2 modulos novos (collectAxioms: sem sorryAx, dentro do trio) + #check das afirmacoes que os textos citam
+ SONDAS do revisor (demonstracoes Lean de que um enunciado e' trivial / de que uma hipotese e' satisfazivel). So escreve nesta pasta."""
import ast, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
s = open(R + "um_v410_candidato.py", "rb").read().decode("utf-8")
tr = ast.parse(s)
E = None
for n in tr.body:
    if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_EMBEDDED_KERNEL_FILES":
        E = ast.literal_eval(n.value)
anc = []
for rel, ns in (("TGLExt/IALD2.lean", "TGLExt.IALD2"), ("TGLExt/AEscala.lean", "TGLExt.AEscala")):
    src = open(R + "insumos/" + rel.split("/")[1], "rb").read().decode("utf-8")
    nomes = re.findall(r"^#print axioms\s+(\S+)", src, re.M)
    print(rel, len(nomes))
    anc += nomes
print("total ancoras", len(anc))
L = ["import TGLExt", "set_option autoImplicit false", "open Lean Elab Meta", "",
     "-- Revisor terceiro v410 R1 (agente Claude Sonnet): #print axioms das %d ancoras (insumos/*.lean) + varredura MetaM de TODAS as constantes dos 2 modulos novos + #check + sondas." % len(anc), ""]
for a in anc: L.append("#print axioms " + a)
L += ["",
      "#eval show MetaM Unit from do",
      "  let env ← getEnv",
      "  let mods : List Name := [`TGLExt.IALD2, `TGLExt.AEscala]",
      "  let trio : List Name := [`propext, `Classical.choice, `Quot.sound]",
      "  let mut total := 0",
      "  let mut fora : Array (Name × Array Name) := #[]",
      "  let mut porMod : Array (Name × Nat) := #[]",
      "  for m in mods do",
      "    let mut n := 0",
      "    for (nm, _) in env.constants.map₁.toList do",
      "      match env.getModuleIdxFor? nm with",
      "      | some idx =>",
      "        if env.header.moduleNames[idx.toNat]! == m then",
      "          n := n + 1",
      "          let ax ← collectAxioms nm",
      "          if ax.any (fun a => !(trio.contains a)) then fora := fora.push (nm, ax)",
      "      | none => pure ()",
      "    porMod := porMod.push (m, n)",
      "    total := total + n",
      "  IO.println s!\"constantes varridas nos 2 modulos: {total} ; por modulo: {porMod}\"",
      "  IO.println s!\"constantes FORA do trio (ou com sorryAx): {fora.size}\"",
      "  for (nm, ax) in fora do IO.println s!\"  FORA: {nm} {ax}\"",
      "",
      "-- os enunciados que os textos publicos citam",
      "#check @TGLExt.AEscala.a_escala",
      "#check @TGLExt.AEscala.existe_o_algoritmo_e_e_a_iald",
      "#check @TGLExt.AEscala.a_pergunta_do_clay_tem_resposta",
      "#check @TGLExt.AEscala.a_iald_le_a_face_sem_leitura",
      "#check @TGLExt.AEscala.cada_face_pesa_meio",
      "#check @TGLExt.AEscala.os_pesos",
      "#check @TGLExt.AEscala.a_face_caida_nao_acopla",
      "#check @TGLExt.AEscala.o_nome_objeto_e_o_centro",
      "#print TGLExt.AEscala.LeitorDoFundo",
      "#print TGLExt.AEscala.aPerguntaDoClay",
      "#print TGLExt.AEscala.iald",
      "#print TGLExt.AEscala.faceMeio",
      "#print TGLExt.AEscala.nomeObjeto",
      "#print TGLExt.AEscala.nomeLido",
      "",
      "-- SONDA 1 (revisor): `aPerguntaDoClay X` e' satisfeita por um leitor CONSTANTE, sem nenhuma TGL (nem `iald`, nem `trava`, nem `Identidade`):",
      "--   a definicao `Nonempty (LeitorDoFundo X)` nao exige custo, tempo polinomial, nem computabilidade.",
      "section SondaTrivial2",
      "open Classical in",
      "noncomputable def leitorTrivial (X : Type) [Fintype X] [DecidableEq X] : TGLExt.AEscala.LeitorDoFundo X where",
      "  leitura := fun c _ => if ∃ x, c x = 0 then 1 else 0",
      "  limite := fun c => if ∃ x, c x = 0 then 1 else 0",
      "  le_como_dissipacao := fun c => tendsto_const_nhds",
      "  diz_a_face_sem_leitura := fun c => by",
      "    by_cases h : ∃ x, c x = 0",
      "    · simp [h]",
      "    · simp [h]",
      "",
      "theorem a_pergunta_do_clay_sem_TGL (X : Type) [Fintype X] [DecidableEq X] : TGLExt.AEscala.aPerguntaDoClay X := ⟨leitorTrivial X⟩",
      "#print axioms a_pergunta_do_clay_sem_TGL",
      "end SondaTrivial2",
      ""]
open(R + "revisao_terceiro/axiomas_terceiro_v410.lean", "w", encoding="utf-8", newline="\n").write("\n".join(L))
print("escrito")
