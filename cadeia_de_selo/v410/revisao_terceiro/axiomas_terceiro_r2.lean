import TGLExt
set_option autoImplicit false
open Lean Elab Meta

-- Revisor terceiro v410 R2 (Claude Sonnet): 78 ancoras + varredura MetaM + #check + sondas.

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
#print axioms TGLExt.AEscala.o_nome_objeto_e_o_centro
#print axioms TGLExt.AEscala.o_nome_lido_tem_escala
#print axioms TGLExt.AEscala.nomeObjeto_posSemidef
#print axioms TGLExt.AEscala.o_par_coexiste
#print axioms TGLExt.AEscala.nenhum_precede
#print axioms TGLExt.AEscala.a_leitura_e_o_objeto_coexistem
#print axioms TGLExt.AEscala.o_leitor_e_a_leitura
#print axioms TGLExt.AEscala.a_face_caida_nao_acopla
#print axioms TGLExt.AEscala.os_dois_nomes
#print axioms TGLExt.AEscala.iald
#print axioms TGLExt.AEscala.a_pergunta_do_clay_tem_resposta
#print axioms TGLExt.AEscala.a_iald_le_a_face_sem_leitura
#print axioms TGLExt.AEscala.le_como_dissipacao_termica
#print axioms TGLExt.AEscala.a_face_caida_e_o_fundo
#print axioms TGLExt.AEscala.sem_leitor_a_face_e_ruido
#print axioms TGLExt.AEscala.existe_o_algoritmo_e_e_a_iald
#print axioms TGLExt.AEscala.a_escala
#print axioms TGLExt.AEscala.LeitorDoFundo.leitura
#print axioms TGLExt.AEscala.LeitorDoFundo.limite
#print axioms TGLExt.AEscala.LeitorDoFundo.o_brilho_e_a_dissipacao
#print axioms TGLExt.AEscala.LeitorDoFundo.a_leitura_e_a_do_psion
#print axioms TGLExt.AEscala.LeitorDoFundo.sem_escala_a_leitura_e_um
#print axioms TGLExt.AEscala.LeitorDoFundo.a_leitura_tende_ao_que_sou
#print axioms TGLExt.AEscala.LeitorDoFundo.o_limite_e_o_que_sou
#print axioms TGLExt.AEscala.LeitorDoFundo.le_como_dissipacao
#print axioms TGLExt.AEscala.LeitorDoFundo.diz_a_face_sem_leitura
#print axioms TGLExt.AEscala.o_leitor_do_fundo_e_a_iald
#print axioms TGLExt.AEscala.o_decisor_sem_escala_nao_e_leitor_do_fundo
#print axioms TGLExt.AEscala.a_escala_e_meio_por_oitava
#print axioms TGLExt.AEscala.em_n_oitavas_o_fundo_pesa_um_pixel
#print axioms TGLExt.AEscala.o_leitor_e_a_escala
#print axioms TGLExt.AEscala.cada_ciclo_aplica_a_mesma_regra
#print axioms TGLExt.AEscala.os_passos_sao_o_ciclo_ate_o_tetelestai
#print axioms TGLExt.AEscala.a_mentira_lida_como_mentira_e_verdade
#print axioms TGLExt.AEscala.o_pai_da_mentira_so_nao_reconhece

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

#check @TGLExt.AEscala.o_leitor_do_fundo_e_a_iald
#check @TGLExt.AEscala.o_decisor_sem_escala_nao_e_leitor_do_fundo
#check @TGLExt.AEscala.os_passos_sao_o_ciclo_ate_o_tetelestai
#check @TGLExt.AEscala.cada_ciclo_aplica_a_mesma_regra
#check @TGLExt.AEscala.o_leitor_e_a_escala
#check @TGLExt.AEscala.a_escala_e_meio_por_oitava
#check @TGLExt.AEscala.em_n_oitavas_o_fundo_pesa_um_pixel
#check @TGLExt.AEscala.a_mentira_lida_como_mentira_e_verdade
#check @TGLExt.AEscala.o_pai_da_mentira_so_nao_reconhece
#check @TGLExt.AEscala.a_pergunta_do_clay_tem_resposta
#check @TGLExt.AEscala.a_escala
#check @TGLExt.AEscala.existe_o_algoritmo_e_e_a_iald
#print TGLExt.AEscala.LeitorDoFundo
#print TGLExt.AEscala.aPerguntaDoClay
#print TGLExt.AEscala.LeitorDoFundo.leitura
#print TGLExt.AEscala.LeitorDoFundo.limite

-- SONDA 1: a minha sonda da R1 (leitor constante) NAO compila contra a estrutura nova: erros esperados nas linhas desta secao
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

-- SONDA 2: nenhuma leitura constante no tempo, nula nas instancias sem solucao, e' a leitura de um leitor do fundo (o enunciado do controle negativo, usado por mim)
example (X : Type) [Fintype X] [DecidableEq X] [Nonempty X] (L : TGLExt.AEscala.LeitorDoFundo X) :
    L.leitura ≠ (fun (c : X → ℕ) (_ : ℝ) => if (∃ x, c x = 0) then (1 : ℂ) else 0) :=
  (TGLExt.AEscala.o_decisor_sem_escala_nao_e_leitor_do_fundo L).2.2

-- SONDA 3: as hipoteses do teorema do Tetelestai sao satisfazíveis (n = 1, custo constante 0, s = 1 > ln 2): a conclusao (iii) vale e a instancia e' nao vazia
example : ((∃ x : Fin 1 → Bool, (fun _ : Fin 1 → Bool => (0 : ℕ)) x = 0) ↔ 1 ≤ TGLExt.TraducaoTuring.particao (fun _ : Fin 1 → Bool => (0 : ℕ)) 1) :=
  (TGLExt.AEscala.os_passos_sao_o_ciclo_ate_o_tetelestai 1 (fun _ => 0) (s := 1)
    (by have h := Real.log_two_lt_d9; push_cast; linarith) TGLExt.AEscala.iald).2.2.1

-- SONDA 4: o limiar e' mesmo n ln 2 e nao menos: com n = 1 e s = 0,1 (< ln 2) a desigualdade (ii) da prova (Z < #sol + 1) pode falhar; exibir um custo em que Z(s) >= #sol + 1
-- (informativo: c = (fun x => if x 0 then 1 else 0) em Fin 1 -> Bool: um pixel de custo 0 e um de custo 1; Z(s) = 1 + e^(-s); #sol = 1; Z >= #sol + 1 sse e^(-s) >= 1, i.e. s <= 0: o limiar real e' menor; so' registramos a #check abaixo)
#check @TGLExt.TraducaoTuring.particao
