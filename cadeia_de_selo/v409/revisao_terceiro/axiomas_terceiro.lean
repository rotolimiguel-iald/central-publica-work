import TGLExt
set_option autoImplicit false
open Lean Elab Meta

-- Revisor terceiro v409 R1 (agente Claude Sonnet): #print axioms das 82 ancoras (CANDIDATO_v409.json kernel.ancoras) + varredura MetaM de TODAS as constantes dos 2 modulos novos + #check/#print.

#print axioms TGLExt.TraducaoTuring.opDaInstancia_autoadjunto
#print axioms TGLExt.TraducaoTuring.nucleo_nao_nulo_sse
#print axioms TGLExt.TraducaoTuring.verificacao_np
#print axioms TGLExt.TraducaoTuring.grau_da_palavra_da_instancia
#print axioms TGLExt.TraducaoTuring.bits_sao_oitavas
#print axioms TGLExt.TraducaoTuring.o_fluxo_conserva_o_peso
#print axioms TGLExt.TraducaoTuring.solucao_por_coordenadas
#print axioms TGLExt.TraducaoTuring.leitura_da_solucao_por_coordenadas
#print axioms TGLExt.TraducaoTuring.peso_da_solucao_no_uniforme
#print axioms TGLExt.TraducaoTuring.a_instancia_nao_e_o_vazio
#print axioms TGLExt.TraducaoTuring.o_pedagio_da_selecao
#print axioms TGLExt.TraducaoTuring.a_traducao
#print axioms TGLExt.TraducaoTuring.selecao_no_nome
#print axioms TGLExt.TraducaoTuring.o_decaimento_converge_a_selecao
#print axioms TGLExt.TraducaoTuring.uniforme_tem_solucao
#print axioms TGLExt.TraducaoTuring.a_selecao_acha
#print axioms TGLExt.TraducaoTuring.o_custo_da_selecao_em_nats
#print axioms TGLExt.TraducaoTuring.p_igual_np_no_modo_selecao
#print axioms TGLExt.TraducaoTuring.a_selecao_esquece
#print axioms TGLExt.TraducaoTuring.a_selecao_perde
#print axioms TGLExt.TraducaoTuring.norma_do_normalizado
#print axioms TGLExt.TraducaoTuring.a_fotografia_sem_leitor
#print axioms TGLExt.TraducaoTuring.o_par_quebra_a_simetria
#print axioms TGLExt.TraducaoTuring.a_trava_fatora
#print axioms TGLExt.TraducaoTuring.o_nome_fica_travado
#print axioms TGLExt.TraducaoTuring.norma_por_coordenadas
#print axioms TGLExt.TraducaoTuring.a_trava_sem_conhecer_o_nome
#print axioms TGLExt.TraducaoTuring.negar_o_zero
#print axioms TGLExt.TraducaoTuring.norma_do_uniforme
#print axioms TGLExt.TraducaoTuring.norma_sq_do_nome_no_uniforme
#print axioms TGLExt.TraducaoTuring.a_trava_em_tempo_linear
#print axioms TGLExt.TraducaoTuring.a_trava_converge_a_selecao
#print axioms TGLExt.TraducaoTuring.a_trava_no_nome
#print axioms TGLExt.TraducaoTuring.a_regra_reconstroi_o_todo
#print axioms TGLExt.TraducaoTuring.o_hamiltoniano_gera_a_trava
#print axioms TGLExt.TraducaoTuring.a_norma_da_trava_e_a_particao
#print axioms TGLExt.TraducaoTuring.a_particao_conta_o_nome
#print axioms TGLExt.TraducaoTuring.a_particao_cobre_o_nome
#print axioms TGLExt.TraducaoTuring.a_fita_e_o_hamiltoniano_oculto
#print axioms TGLExt.TraducaoTuring.trava_smul
#print axioms TGLExt.TraducaoTuring.cada_pixel_e_lido
#print axioms TGLExt.TraducaoTuring.z_le_os_pixels
#print axioms TGLExt.TraducaoTuring.o_psion_le_os_pixels
#print axioms TGLExt.TraducaoTuring.o_canto_do_psion_escalariza_a_trava
#print axioms TGLExt.TraducaoTuring.z_e_o_modo_leitor
#print axioms TGLExt.TraducaoTuring.o_que_sou_das_solucoes
#print axioms TGLExt.TraducaoTuring.eu_sou_no_instante_zero
#print axioms TGLExt.TraducaoTuring.eu_sou_eu_mesmo
#print axioms TGLExt.TraducaoTuring.o_que_sou_no_limite
#print axioms TGLExt.TraducaoTuring.o_tempo_cria_a_medida
#print axioms TGLExt.TraducaoTuring.eu_sou_o_que_sou_so_na_instancia_trivial
#print axioms TGLExt.TraducaoTuring.a_fita_sem_escala
#print axioms TGLExt.TraducaoTuring.a_leitura_sem_escala_afirma_o_que_nao_e
#print axioms TGLExt.TraducaoTuring.sem_escala_a_mentira_e_a_verdade_leem_igual
#print axioms TGLExt.TraducaoTuring.o_pai_da_mentira
#print axioms TGLExt.TraducaoTuring.leituraPerformada_e_a_leitura
#print axioms TGLExt.TraducaoTuring.a_performance_comeca_em_eu_sou
#print axioms TGLExt.TraducaoTuring.a_performance_decai
#print axioms TGLExt.TraducaoTuring.a_identidade_se_preserva_enquanto_decai
#print axioms TGLExt.TraducaoTuring.a_performance_chega_ao_conteudo
#print axioms TGLExt.TraducaoTuring.o_conteudo_e_o_que_sou
#print axioms TGLExt.TraducaoTuring.a_identidade_performada
#print axioms TGLExt.TraducaoTuring.travaOp_apply
#print axioms TGLExt.TraducaoTuring.inscricao_do_uniforme
#print axioms TGLExt.TraducaoTuring.adjunta_da_inscricao_no_psion
#print axioms TGLExt.TraducaoTuring.o_psion_le_z
#print axioms TGLExt.TraducaoTuring.o_canto_do_psion_da_luz_le_z
#print axioms TGLExt.TraducaoTuring.custoCNF_cons
#print axioms TGLExt.TraducaoTuring.custoCNF_zero_sse
#print axioms TGLExt.TraducaoTuring.uma_leitura_decide_SAT
#print axioms TGLExt.TraducaoTuring.a_trava_da_formula_fatora_na_clausula
#print axioms TGLExt.TraducaoTuring.a_maquina_com_o_leitor
#print axioms TGLExt.ParNaFaceDeFock.inner_espelho
#print axioms TGLExt.ParNaFaceDeFock.reduzido_do_par
#print axioms TGLExt.ParNaFaceDeFock.norma_do_par
#print axioms TGLExt.ParNaFaceDeFock.meia_nat_do_projetor
#print axioms TGLExt.ParNaFaceDeFock.par_ortonormal_das_polarizacoes
#print axioms TGLExt.ParNaFaceDeFock.existe_par_ortonormal_em_H1
#print axioms TGLExt.ParNaFaceDeFock.parFock_norma
#print axioms TGLExt.ParNaFaceDeFock.parFock_ortogonal_ao_vacuo
#print axioms TGLExt.ParNaFaceDeFock.a_marginal_do_par
#print axioms TGLExt.ParNaFaceDeFock.o_par_na_face_de_fock

-- varredura independente: toda constante cujo modulo de origem e' um dos 2 novos
#eval show MetaM Unit from do
  let env ← getEnv
  let mods : List Name := [`TGLExt.TraducaoTuring, `TGLExt.ParNaFaceDeFock]
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
  IO.println s!"constantes varridas nos 2 modulos: {total} ; por modulo: {porMod}"
  IO.println s!"constantes FORA do trio (ou com sorryAx): {fora.size}"
  for (nm, ax) in fora do IO.println s!"  FORA: {nm} {ax}"

-- as afirmacoes dos textos publicos: o enunciado que o kernel de fato tem
#check @TGLExt.TraducaoTuring.p_igual_np_no_modo_selecao
#check @TGLExt.TraducaoTuring.a_selecao_acha
#check @TGLExt.TraducaoTuring.uniforme_tem_solucao
#check @TGLExt.TraducaoTuring.o_custo_da_selecao_em_nats
#check @TGLExt.TraducaoTuring.a_trava_no_nome
#check @TGLExt.TraducaoTuring.a_trava_em_tempo_linear
#check @TGLExt.TraducaoTuring.a_trava_converge_a_selecao
#check @TGLExt.TraducaoTuring.negar_o_zero
#check @TGLExt.TraducaoTuring.z_e_o_modo_leitor
#check @TGLExt.TraducaoTuring.a_fita_e_o_hamiltoniano_oculto
#check @TGLExt.TraducaoTuring.a_fita_sem_escala
#check @TGLExt.TraducaoTuring.o_pai_da_mentira
#check @TGLExt.TraducaoTuring.a_identidade_performada
#check @TGLExt.TraducaoTuring.eu_sou_o_que_sou_so_na_instancia_trivial
#check @TGLExt.TraducaoTuring.inscricao_do_uniforme
#check @TGLExt.TraducaoTuring.adjunta_da_inscricao_no_psion
#check @TGLExt.TraducaoTuring.o_psion_le_z
#check @TGLExt.TraducaoTuring.o_canto_do_psion_da_luz_le_z
#check @TGLExt.TraducaoTuring.custoCNF_zero_sse
#check @TGLExt.TraducaoTuring.uma_leitura_decide_SAT
#check @TGLExt.TraducaoTuring.a_trava_da_formula_fatora_na_clausula
#check @TGLExt.TraducaoTuring.a_maquina_com_o_leitor
#check @TGLExt.TraducaoTuring.a_traducao
#check @TGLExt.TraducaoTuring.bits_sao_oitavas
#print TGLExt.TraducaoTuring.SAT
#print TGLExt.TraducaoTuring.custoCNF
#print TGLExt.TraducaoTuring.inscricao
#print TGLExt.TraducaoTuring.selecao
#check @TGLExt.ParNaFaceDeFock.o_par_na_face_de_fock
#check @TGLExt.ParNaFaceDeFock.a_marginal_do_par
#check @TGLExt.ParNaFaceDeFock.meia_nat_do_projetor
#check @TGLExt.ParNaFaceDeFock.reduzido_do_par
#check @TGLExt.ParNaFaceDeFock.parFock_norma
#check @TGLExt.ParNaFaceDeFock.parFock_ortogonal_ao_vacuo
#check @TGLExt.ParNaFaceDeFock.existe_par_ortonormal_em_H1
#check @TGLExt.ParNaFaceDeFock.par_ortonormal_das_polarizacoes

-- as ancoras herdadas que os textos citam (conferencia de existencia)
#check @TGLExt.PIgualNP.p_igual_np_nas_classes_do_dicionario
#check @TGLExt.TetelestaiTerminal.o_terminal_e_a_leitura_nao_o_fim_do_decaimento
