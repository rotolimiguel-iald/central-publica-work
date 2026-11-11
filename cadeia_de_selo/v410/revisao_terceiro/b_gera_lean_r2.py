# -*- coding: utf-8 -*-
"""Revisor v410 R2: gera axiomas_terceiro_r2.lean: #print axioms das ancoras LIDAS de insumos/IALD2.lean e insumos/AEscala.lean (R3/R4) + varredura MetaM dos 2 modulos + #check dos enunciados novos
+ SONDAS: (1) a minha sonda da R1 (leitor constante) tem de NAO compilar mais; (2) o decisor constante nao e' leitura de leitor do fundo; (3) instancias das hipoteses (nao vacuidade). So escreve nesta pasta."""
import re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
anc = []
for rel in ("IALD2.lean", "AEscala.lean"):
    src = open(R + "insumos/" + rel, "rb").read().decode("utf-8")
    nomes = re.findall(r"^#print axioms\s+(\S+)", src, re.M)
    print(rel, len(nomes)); anc += nomes
L = ["import TGLExt", "set_option autoImplicit false", "open Lean Elab Meta", "",
     "-- Revisor terceiro v410 R2 (Claude Sonnet): %d ancoras + varredura MetaM + #check + sondas." % len(anc), ""]
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
      "#check @TGLExt.AEscala.o_leitor_do_fundo_e_a_iald",
      "#check @TGLExt.AEscala.o_decisor_sem_escala_nao_e_leitor_do_fundo",
      "#check @TGLExt.AEscala.os_passos_sao_o_ciclo_ate_o_tetelestai",
      "#check @TGLExt.AEscala.cada_ciclo_aplica_a_mesma_regra",
      "#check @TGLExt.AEscala.o_leitor_e_a_escala",
      "#check @TGLExt.AEscala.a_escala_e_meio_por_oitava",
      "#check @TGLExt.AEscala.em_n_oitavas_o_fundo_pesa_um_pixel",
      "#check @TGLExt.AEscala.a_mentira_lida_como_mentira_e_verdade",
      "#check @TGLExt.AEscala.o_pai_da_mentira_so_nao_reconhece",
      "#check @TGLExt.AEscala.a_pergunta_do_clay_tem_resposta",
      "#check @TGLExt.AEscala.a_escala",
      "#check @TGLExt.AEscala.existe_o_algoritmo_e_e_a_iald",
      "#print TGLExt.AEscala.LeitorDoFundo",
      "#print TGLExt.AEscala.aPerguntaDoClay",
      "#print TGLExt.AEscala.LeitorDoFundo.leitura",
      "#print TGLExt.AEscala.LeitorDoFundo.limite",
      "",
      "-- SONDA 1: a minha sonda da R1 (leitor constante) NAO compila contra a estrutura nova: erros esperados nas linhas desta secao",
      "section SondaR1_DEVE_FALHAR",
      "open Classical in",
      "noncomputable def leitorTrivialR1 (X : Type) [Fintype X] [DecidableEq X] : TGLExt.AEscala.LeitorDoFundo X where",
      "  leitura := fun c _ => if ∃ x, c x = 0 then 1 else 0",
      "  limite := fun c => if ∃ x, c x = 0 then 1 else 0",
      "  le_como_dissipacao := fun c => tendsto_const_nhds",
      "  diz_a_face_sem_leitura := fun c => by",
      "    by_cases h : ∃ x, c x = 0",
      "    · simp [h]",
      "    · simp [h]",
      "end SondaR1_DEVE_FALHAR",
      "",
      "-- SONDA 2: nenhuma leitura constante no tempo, nula nas instancias sem solucao, e' a leitura de um leitor do fundo (o enunciado do controle negativo, usado por mim)",
      "example (X : Type) [Fintype X] [DecidableEq X] [Nonempty X] (L : TGLExt.AEscala.LeitorDoFundo X) :",
      "    L.leitura ≠ (fun (c : X → ℕ) (_ : ℝ) => if (∃ x, c x = 0) then (1 : ℂ) else 0) :=",
      "  (TGLExt.AEscala.o_decisor_sem_escala_nao_e_leitor_do_fundo L).2.2",
      "",
      "-- SONDA 3: as hipoteses do teorema do Tetelestai sao satisfazíveis (n = 1, custo constante 0, s = 1 > ln 2): a conclusao (iii) vale e a instancia e' nao vazia",
      "example : ((∃ x : Fin 1 → Bool, (fun _ : Fin 1 → Bool => (0 : ℕ)) x = 0) ↔ 1 ≤ TGLExt.TraducaoTuring.particao (fun _ : Fin 1 → Bool => (0 : ℕ)) 1) :=",
      "  (TGLExt.AEscala.os_passos_sao_o_ciclo_ate_o_tetelestai 1 (fun _ => 0) (s := 1)",
      "    (by have h := Real.log_two_lt_d9; push_cast; linarith) TGLExt.AEscala.iald).2.2.1",
      "",
      "-- SONDA 4: o limiar e' mesmo n ln 2 e nao menos: com n = 1 e s = 0,1 (< ln 2) a desigualdade (ii) da prova (Z < #sol + 1) pode falhar; exibir um custo em que Z(s) >= #sol + 1",
      "-- (informativo: c = (fun x => if x 0 then 1 else 0) em Fin 1 -> Bool: um pixel de custo 0 e um de custo 1; Z(s) = 1 + e^(-s); #sol = 1; Z >= #sol + 1 sse e^(-s) >= 1, i.e. s <= 0: o limiar real e' menor; so' registramos a #check abaixo)",
      "#check @TGLExt.TraducaoTuring.particao",
      ""]
open(R + "revisao_terceiro/axiomas_terceiro_r2.lean", "w", encoding="utf-8", newline="\n").write("\n".join(L))
print("escrito", len(anc), "ancoras")
