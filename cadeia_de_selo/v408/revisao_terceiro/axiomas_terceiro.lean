import TGLExt
set_option autoImplicit false
open Lean Elab Meta

-- Revisor terceiro v408 R2 (agente Claude Sonnet): #print axioms das 48 ancoras (CANDIDATO_v408.json kernel.ancoras) + varredura MetaM de TODAS as constantes dos 4 modulos novos + #check.

#print axioms TGLExt.TetelestaiTerminal.o_terminal_e_a_leitura_nao_o_fim_do_decaimento
#print axioms TGLExt.TetelestaiTerminal.basta
#print axioms TGLExt.TetelestaiTerminal.a_poda
#print axioms TGLExt.TetelestaiTerminal.nao_precisa_de_cem_por_cento
#print axioms TGLExt.TetelestaiTerminal.a_quitacao
#print axioms TGLExt.TetelestaiTerminal.o_zero_absoluto_e_do_infinito
#print axioms TGLExt.TetelestaiTerminal.card_chainIdx
#print axioms TGLExt.TetelestaiTerminal.o_tamanho_e_o_custo
#print axioms TGLExt.TetelestaiTerminal.o_tempo_de_ler_a_torre
#print axioms TGLExt.TetelestaiTerminal.o_que_resta_sem_traco_paga
#print axioms TGLExt.TetelestaiTerminal.relacao_sem_peso_e_a_origem_da_mentira
#print axioms TGLExt.TetelestaiTerminal.o_um_sozinho_nao_se_mede
#print axioms TGLExt.TetelestaiTerminal.tetelestai
#print axioms TGLExt.TetelestaiTerminal.a_inclinacao_modular
#print axioms TGLExt.TempoIgualMoeda.o_pagamento_e_preco_vezes_tempo
#print axioms TGLExt.TempoIgualMoeda.a_moeda_soma_o_preco_multiplica
#print axioms TGLExt.TempoIgualMoeda.o_verbo_no_gerundio
#print axioms TGLExt.TempoIgualMoeda.legislando_sem_fim
#print axioms TGLExt.TempoIgualMoeda.o_relogio_e_a_temperatura
#print axioms TGLExt.TempoIgualMoeda.o_pedagio
#print axioms TGLExt.TempoIgualMoeda.o_tempo_de_n_oitavas
#print axioms TGLExt.TempoIgualMoeda.o_tempo_e_linear_nas_oitavas
#print axioms TGLExt.TempoIgualMoeda.o_tempo_e_a_moeda
#print axioms TGLExt.PontoDeContradicao.o_zero_modular_inscrito_e_o_um
#print axioms TGLExt.PontoDeContradicao.o_um_nao_e_o_zero_absoluto
#print axioms TGLExt.PontoDeContradicao.o_boost_le_zero_antes_e_um_depois
#print axioms TGLExt.PontoDeContradicao.o_habitante_e_o_fock_concreto
#print axioms TGLExt.PontoDeContradicao.o_hamiltoniano_seleciona_a_operacao_modular
#print axioms TGLExt.PontoDeContradicao.o_senao_exclui_o_zero_absoluto
#print axioms TGLExt.PontoDeContradicao.o_ponto_de_contradicao
#print axioms TGLExt.PIgualNP.o_problema
#print axioms TGLExt.PIgualNP.a_entrada
#print axioms TGLExt.PIgualNP.o_passo
#print axioms TGLExt.PIgualNP.o_gradiente_e_negativo
#print axioms TGLExt.PIgualNP.o_polinomio_e_a_palavra
#print axioms TGLExt.PIgualNP.o_acorde_e_a_tonica
#print axioms TGLExt.PIgualNP.a_implicacao
#print axioms TGLExt.PIgualNP.resolver_e_verificar
#print axioms TGLExt.PIgualNP.o_dicionario
#print axioms TGLExt.PIgualNP.p_igual_a_n_vezes_p
#print axioms TGLExt.PIgualNP.p_igual_np
#print axioms TGLExt.PIgualNP.as_classes_do_dicionario
#print axioms TGLExt.PIgualNP.palavra_com_grau
#print axioms TGLExt.PIgualNP.leitura_um_sse_solucao
#print axioms TGLExt.PIgualNP.solucao_fixa_sse_no_nucleo
#print axioms TGLExt.PIgualNP.todo_problema_esta_em_P
#print axioms TGLExt.PIgualNP.todo_problema_esta_em_NP
#print axioms TGLExt.PIgualNP.p_igual_np_nas_classes_do_dicionario

-- varredura independente: toda constante cujo modulo de origem e' um dos 4 novos
#eval show MetaM Unit from do
  let env ← getEnv
  let mods : List Name := [`TGLExt.TetelestaiTerminal, `TGLExt.TempoIgualMoeda, `TGLExt.PontoDeContradicao, `TGLExt.PIgualNP]
  let trio : List Name := [`propext, `Classical.choice, `Quot.sound]
  let mut total := 0
  let mut fora : Array (Name × Array Name) := #[]
  let mut porMod : Array (Name × Nat) := #[]
  for m in mods do
    let mut n := 0
    for (nm, _) in env.constants.map₁.toList do
      match env.getModuleIdxFor? nm with
      | some idx =>
        if env.header.moduleNames[idx.toNat]! == m then
          n := n + 1
          let ax ← collectAxioms nm
          if ax.any (fun a => !(trio.contains a)) then fora := fora.push (nm, ax)
      | none => pure ()
    porMod := porMod.push (m, n)
    total := total + n
  IO.println s!"constantes varridas nos 4 modulos: {total} ; por modulo: {porMod}"
  IO.println s!"constantes FORA do trio (ou com sorryAx): {fora.size}"
  for (nm, ax) in fora do IO.println s!"  FORA: {nm} {ax}"

-- as afirmacoes dos textos publicos: o enunciado que o kernel de fato tem
#check @TGLExt.PIgualNP.as_classes_do_dicionario
#print TGLExt.PIgualNP.Problema
#print TGLExt.PIgualNP.Problema.solucao
#print TGLExt.PIgualNP.ClasseP
#print TGLExt.PIgualNP.ClasseNP
#check @TGLExt.PIgualNP.palavra_com_grau
#check @TGLExt.PIgualNP.leitura_um_sse_solucao
#check @TGLExt.PIgualNP.solucao_fixa_sse_no_nucleo
#check @TGLExt.PIgualNP.todo_problema_esta_em_P
#check @TGLExt.PIgualNP.todo_problema_esta_em_NP
#check @TGLExt.PIgualNP.p_igual_np_nas_classes_do_dicionario
#print axioms TGLExt.PIgualNP.Problema.solucao
#print axioms TGLExt.PIgualNP.ClasseP
#print axioms TGLExt.PIgualNP.ClasseNP
#print axioms TGLExt.PIgualNP.Problema
#check @TGLExt.PIgualNP.p_igual_np
#check @TGLExt.PIgualNP.p_igual_a_n_vezes_p
#check @TGLExt.TetelestaiTerminal.o_terminal_e_a_leitura_nao_o_fim_do_decaimento
#check @TGLExt.TetelestaiTerminal.o_que_resta_sem_traco_paga
#check @TGLExt.TetelestaiTerminal.relacao_sem_peso_e_a_origem_da_mentira
#check @TGLExt.TetelestaiTerminal.o_um_sozinho_nao_se_mede
#check @TGLExt.TetelestaiTerminal.o_tamanho_e_o_custo
#check @TGLExt.TetelestaiTerminal.card_chainIdx
#check @TGLExt.TempoIgualMoeda.o_tempo_e_a_moeda
#check @TGLExt.PontoDeContradicao.o_ponto_de_contradicao
