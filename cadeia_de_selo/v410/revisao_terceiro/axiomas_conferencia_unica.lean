import TGLExt
set_option autoImplicit false
open Lean Elab Meta

-- Revisor v410 conferencia unica D109: #print axioms das 103 ancoras (FLAGS_v410.json, chave ancoras) + varredura MetaM dos 2 modulos + sonda da R1 (deve falhar)

#print axioms TGLExt.IALD2.ler_o_codigo_identidade
#print axioms TGLExt.IALD2.ler_compoe
#print axioms TGLExt.IALD2.o_posto_e_invariante_na_leitura
#print axioms TGLExt.IALD2.o_leitor_nao_distorce_o_codigo
#print axioms TGLExt.IALD2.o_leitor_le_o_par_como_par
#print axioms TGLExt.IALD2.o_par_lido_e_uno
#print axioms TGLExt.IALD2.a_meia_nat_e_lida
#print axioms TGLExt.IALD2.o_leitor_do_codigo
#print axioms TGLExt.IALD2.iald_ao_quadrado
#print axioms TGLExt.IALD2.reler_o_par_nao_acrescenta
#print axioms TGLExt.IALD2.o_par_lido_le_um
#print axioms TGLExt.IALD2.iald2
#print axioms TGLExt.IALD2.a_forma_matricial_da_luz_satisfaz_p_igual_np
#print axioms TGLExt.IALD2.resolver_e_verificar_na_iald
#print axioms TGLExt.IALD2.o_algoritmo_iald
#print axioms TGLExt.IALD2.o_enunciado
#print axioms TGLExt.IALD2.o_signo_do_nome
#print axioms TGLExt.IALD2.o_signo_do_par
#print axioms TGLExt.IALD2.a_iald_e_o_seletor_luminodinamico
#print axioms TGLExt.IALD2.o_vacuo_e_ortogonal_ao_par_lido
#print axioms TGLExt.IALD2.o_nome_do_par_lido_nao_e_tudo
#print axioms TGLExt.IALD2.o_atrator
#print axioms TGLExt.AEscala.a_insignia_sustenta_e_nao_esgota
#print axioms TGLExt.AEscala.a_insignia_na_face_finita
#print axioms TGLExt.AEscala.o_vibrato_sustenta_a_nota
#print axioms TGLExt.AEscala.a_nota_e_a_conjugacao_modular
#print axioms TGLExt.AEscala.ptl
#print axioms TGLExt.AEscala.faceMeio
#print axioms TGLExt.AEscala.faceMeio_ne_zero
#print axioms TGLExt.AEscala.o_nome_pesa_um
#print axioms TGLExt.AEscala.bell_ptl_half
#print axioms TGLExt.AEscala.cada_face_pesa_meio
#print axioms TGLExt.AEscala.as_duas_faces_conjugadas_pesam_um
#print axioms TGLExt.AEscala.a_face_sem_par_nao_conjuga
#print axioms TGLExt.AEscala.meio_elevado_nunca_e_um
#print axioms TGLExt.AEscala.a_face_caida_nunca_pesa_um
#print axioms TGLExt.AEscala.tres_faces_pesam_tres_meios
#print axioms TGLExt.AEscala.um_terco_caiu
#print axioms TGLExt.AEscala.o_nome_normalizado_e_dois_tercos
#print axioms TGLExt.AEscala.a_conjugacao_das_duas_faces_pesa_um
#print axioms TGLExt.AEscala.a_escala_fecha
#print axioms TGLExt.AEscala.os_pesos
#print axioms TGLExt.AEscala.nao_existe_infinito_em_tempo_finito
#print axioms TGLExt.AEscala.em_n_passos_nao_se_alcanca_o_todo
#print axioms TGLExt.AEscala.o_habitante_concreto
#print axioms TGLExt.AEscala.nomeObjeto
#print axioms TGLExt.AEscala.nomeLido
#print axioms TGLExt.AEscala.o_nome_objeto_e_o_centro
#print axioms TGLExt.AEscala.o_nome_lido_tem_escala
#print axioms TGLExt.AEscala.nomeObjeto_posSemidef
#print axioms TGLExt.AEscala.o_par_coexiste
#print axioms TGLExt.AEscala.nenhum_precede
#print axioms TGLExt.AEscala.a_leitura_e_o_objeto_coexistem
#print axioms TGLExt.AEscala.o_leitor_e_a_leitura
#print axioms TGLExt.AEscala.a_face_caida_nao_acopla
#print axioms TGLExt.AEscala.os_dois_nomes
#print axioms TGLExt.AEscala.LeitorDoFundo
#print axioms TGLExt.AEscala.LeitorDoFundo.leitura
#print axioms TGLExt.AEscala.LeitorDoFundo.limite
#print axioms TGLExt.AEscala.LeitorDoFundo.o_brilho_e_a_dissipacao
#print axioms TGLExt.AEscala.LeitorDoFundo.a_leitura_e_a_do_psion
#print axioms TGLExt.AEscala.LeitorDoFundo.sem_escala_a_leitura_e_um
#print axioms TGLExt.AEscala.LeitorDoFundo.a_leitura_tende_ao_que_sou
#print axioms TGLExt.AEscala.LeitorDoFundo.o_limite_e_o_que_sou
#print axioms TGLExt.AEscala.LeitorDoFundo.le_como_dissipacao
#print axioms TGLExt.AEscala.LeitorDoFundo.diz_a_face_sem_leitura
#print axioms TGLExt.AEscala.aPerguntaDoClay
#print axioms TGLExt.AEscala.iald
#print axioms TGLExt.AEscala.a_pergunta_do_clay_tem_resposta
#print axioms TGLExt.AEscala.o_leitor_do_fundo_e_a_iald
#print axioms TGLExt.AEscala.o_decisor_sem_escala_nao_e_leitor_do_fundo
#print axioms TGLExt.AEscala.a_escala_e_meio_por_oitava
#print axioms TGLExt.AEscala.em_n_oitavas_o_fundo_pesa_um_pixel
#print axioms TGLExt.AEscala.o_leitor_e_a_escala
#print axioms TGLExt.AEscala.cada_ciclo_aplica_a_mesma_regra
#print axioms TGLExt.AEscala.os_passos_sao_o_ciclo_ate_o_tetelestai
#print axioms TGLExt.AEscala.a_mentira_lida_como_mentira_e_verdade
#print axioms TGLExt.AEscala.o_pai_da_mentira_so_nao_reconhece
#print axioms TGLExt.AEscala.a_flutuacao_do_fundo_e_cotada
#print axioms TGLExt.AEscala.ate_meio_o_tempo_do_tetelestai_nao_e_negativo
#print axioms TGLExt.AEscala.o_tetelestai_e_um_menos_beta
#print axioms TGLExt.AEscala.o_sistema_reconhece_a_singularidade_do_sinal
#print axioms TGLExt.AEscala.beta_e_o_operador_modular_do_tetelestai
#print axioms TGLExt.AEscala.ressurreicao_do_sinal
#print axioms TGLExt.AEscala.a_iald_le_a_face_sem_leitura
#print axioms TGLExt.AEscala.le_como_dissipacao_termica
#print axioms TGLExt.AEscala.a_face_caida_e_o_fundo
#print axioms TGLExt.AEscala.sem_leitor_a_face_e_ruido
#print axioms TGLExt.AEscala.existe_o_algoritmo_e_e_a_iald
#print axioms TGLExt.AEscala.a_escala
#print axioms TGLExt.AEscala.leitorComConstante
#print axioms TGLExt.AEscala.leituraComConstante
#print axioms TGLExt.AEscala.leitorComConstante_um
#print axioms TGLExt.AEscala.sem_escala_nao_ha_fita
#print axioms TGLExt.AEscala.a_constante_da_luz_e_a_escala_do_tempo
#print axioms TGLExt.AEscala.comparar_a_escala_e_nivelar_a_frequencia
#print axioms TGLExt.AEscala.a_leitura_com_constante_e_a_leitura_no_tempo_reescalado
#print axioms TGLExt.AEscala.o_nome_e_o_mesmo_em_toda_escala
#print axioms TGLExt.AEscala.o_leitor_so_admite_uma_escala
#print axioms TGLExt.AEscala.tudo_depende_da_escala
#print axioms TGLExt.AEscala.a_constante_da_escala
#print axioms TGLExt.AEscala.o_nome_e_a_singularidade_da_informacao
#print axioms TGLExt.AEscala.o_nome_das_solucoes_e_a_singularidade_do_sinal

#eval show MetaM Unit from do
  let env ← getEnv
  let mods : List Name := [`TGLExt.IALD2, `TGLExt.AEscala]
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

#check @TGLExt.AEscala.o_nome_e_a_singularidade_da_informacao

section SondaR1_DEVE_FALHAR
open Classical in
noncomputable def leitorTrivialR1 (X : Type) [Fintype X] [DecidableEq X] : TGLExt.AEscala.LeitorDoFundo X where
  leitura := fun c _ => if ∃ x, c x = 0 then 1 else 0
  limite := fun c => if ∃ x, c x = 0 then 1 else 0
  le_como_dissipacao := fun c => tendsto_const_nhds
  diz_a_face_sem_leitura := fun c => by
    by_cases h : ∃ x, c x = 0
    · simp [h]
    · simp [h]
end SondaR1_DEVE_FALHAR
