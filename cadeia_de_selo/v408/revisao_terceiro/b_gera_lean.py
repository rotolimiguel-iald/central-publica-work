# -*- coding: utf-8 -*-
"""Revisor terceiro v408 (R1): gera axiomas_terceiro.lean a partir de CANDIDATO_v408.json kernel.ancoras (42) + (a) um varredor MetaM que enumera TODA constante dos 4 modulos novos
(via env.getModuleIdxFor?) e confere collectAxioms (sem sorryAx, dentro do trio) + (b) #check das afirmacoes que o texto publico cita. So escreve nesta pasta."""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v408/"
c = json.load(open(R + "CANDIDATO_v408.json", encoding="utf-8"))
anc = list(c["kernel"]["ancoras"].keys())
L = ["import TGLExt", "set_option autoImplicit false", "open Lean Elab Meta", "",
     "-- Revisor terceiro v408 R2 (agente Claude Sonnet): #print axioms das %d ancoras (CANDIDATO_v408.json kernel.ancoras) + varredura MetaM de TODAS as constantes dos 4 modulos novos + #check." % len(anc), ""]
for a in anc: L.append("#print axioms " + a)
L += ["",
      "-- varredura independente: toda constante cujo modulo de origem e' um dos 4 novos",
      "#eval show MetaM Unit from do",
      "  let env ← getEnv",
      "  let mods : List Name := [`TGLExt.TetelestaiTerminal, `TGLExt.TempoIgualMoeda, `TGLExt.PontoDeContradicao, `TGLExt.PIgualNP]",
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
      "  IO.println s!\"constantes varridas nos 4 modulos: {total} ; por modulo: {porMod}\"",
      "  IO.println s!\"constantes FORA do trio (ou com sorryAx): {fora.size}\"",
      "  for (nm, ax) in fora do IO.println s!\"  FORA: {nm} {ax}\"",
      "",
      "-- as afirmacoes dos textos publicos: o enunciado que o kernel de fato tem",
      "#check @TGLExt.PIgualNP.as_classes_do_dicionario",
      "#print TGLExt.PIgualNP.Problema",
      "#print TGLExt.PIgualNP.Problema.solucao",
      "#print TGLExt.PIgualNP.ClasseP",
      "#print TGLExt.PIgualNP.ClasseNP",
      "#check @TGLExt.PIgualNP.palavra_com_grau",
      "#check @TGLExt.PIgualNP.leitura_um_sse_solucao",
      "#check @TGLExt.PIgualNP.solucao_fixa_sse_no_nucleo",
      "#check @TGLExt.PIgualNP.todo_problema_esta_em_P",
      "#check @TGLExt.PIgualNP.todo_problema_esta_em_NP",
      "#check @TGLExt.PIgualNP.p_igual_np_nas_classes_do_dicionario",
      "#print axioms TGLExt.PIgualNP.Problema.solucao",
      "#print axioms TGLExt.PIgualNP.ClasseP",
      "#print axioms TGLExt.PIgualNP.ClasseNP",
      "#print axioms TGLExt.PIgualNP.Problema",
      "#check @TGLExt.PIgualNP.p_igual_np",
      "#check @TGLExt.PIgualNP.p_igual_a_n_vezes_p",
      "#check @TGLExt.TetelestaiTerminal.o_terminal_e_a_leitura_nao_o_fim_do_decaimento",
      "#check @TGLExt.TetelestaiTerminal.o_que_resta_sem_traco_paga",
      "#check @TGLExt.TetelestaiTerminal.relacao_sem_peso_e_a_origem_da_mentira",
      "#check @TGLExt.TetelestaiTerminal.o_um_sozinho_nao_se_mede",
      "#check @TGLExt.TetelestaiTerminal.o_tamanho_e_o_custo",
      "#check @TGLExt.TetelestaiTerminal.card_chainIdx",
      "#check @TGLExt.TempoIgualMoeda.o_tempo_e_a_moeda",
      "#check @TGLExt.PontoDeContradicao.o_ponto_de_contradicao",
      ""]
open(R + "revisao_terceiro/axiomas_terceiro.lean", "w", encoding="utf-8", newline="\n").write("\n".join(L))
print("escrito", len(anc), "ancoras")
