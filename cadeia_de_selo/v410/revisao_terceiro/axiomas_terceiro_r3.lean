import TGLExt
set_option autoImplicit false
open Lean Elab Meta

-- Revisor terceiro v410 R3 (Claude Sonnet): 84 ancoras + varredura MetaM + #check + sondas.

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
#print axioms TGLExt.AEscala.a_flutuacao_do_fundo_e_cotada
#print axioms TGLExt.AEscala.ate_meio_o_tempo_do_tetelestai_nao_e_negativo
#print axioms TGLExt.AEscala.o_tetelestai_e_um_menos_beta
#print axioms TGLExt.AEscala.o_sistema_reconhece_a_singularidade_do_sinal
#print axioms TGLExt.AEscala.beta_e_o_operador_modular_do_tetelestai
#print axioms TGLExt.AEscala.a_informacao_completa_se_reconstroi

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

#check @TGLExt.AEscala.o_tetelestai_e_um_menos_beta
#check @TGLExt.AEscala.o_sistema_reconhece_a_singularidade_do_sinal
#check @TGLExt.AEscala.beta_e_o_operador_modular_do_tetelestai
#check @TGLExt.AEscala.a_informacao_completa_se_reconstroi
#check @TGLExt.AEscala.a_flutuacao_do_fundo_e_cotada
#check @TGLExt.AEscala.ate_meio_o_tempo_do_tetelestai_nao_e_negativo

-- SONDA 3 (R3): as hipoteses de o_tetelestai_e_um_menos_beta sao satisfazíveis: n = 1, custo (0 em true, 2 em false), b = 1/2, s = ln 2 (= o limiar com b = 1/2)
open TGLExt.AEscala TGLExt.TraducaoTuring in
example : (1 - (1/2 : ℝ)) * particao (fun x : Fin 1 → Bool => if x 0 then 0 else 2) (Real.log 2) ≤ ((Finset.univ.filter (fun y : Fin 1 → Bool => (fun x : Fin 1 → Bool => if x 0 then 0 else 2) y = 0)).card : ℝ) :=
  (o_tetelestai_e_um_menos_beta 1 (fun x : Fin 1 → Bool => if x 0 then 0 else 2) ⟨fun _ => true, by simp⟩ (b := 1/2) (s := Real.log 2) (by norm_num) (by norm_num) (Real.log_nonneg one_le_two) (by simp) iald).1

-- SONDA 4 (R3): a clausula vale para QUALQUER b em (0,1) (nao singulariza beta): b = 1/100 com s = n ln 2 + ln 99
open TGLExt.AEscala TGLExt.TraducaoTuring in
example (n : ℕ) (c : (Fin n → Bool) → ℕ) (h : ∃ x, c x = 0) (L : LeitorDoFundo (Fin n → Bool)) {s : ℝ} (hs0 : 0 ≤ s)
    (hs : (n : ℝ) * Real.log 2 + Real.log ((1 - (1/100 : ℝ)) / (1/100)) ≤ s) :
    (1 - (1/100 : ℝ)) * particao c s ≤ ((Finset.univ.filter (fun y => c y = 0)).card : ℝ) :=
  (o_tetelestai_e_um_menos_beta n c h (b := 1/100) (s := s) (by norm_num) (by norm_num) hs0 hs L).1

-- SONDA 5 (R3): beta_e_o_operador_modular_do_tetelestai e' a instancia b := κ.beta da clausula generica + as identidades da matriz-S: os itens (2) e (3) saem da generica por `.1` e `.2.1`
open TGLExt.AEscala TGLExt.TraducaoTuring in
example (κ : TGLCoupling) (n : ℕ) (c : (Fin n → Bool) → ℕ) (h : ∃ x, c x = 0) {s : ℝ} (hs0 : 0 ≤ s)
    (hs : (n : ℝ) * Real.log 2 + Real.log ((1 - κ.beta) / κ.beta) ≤ s) (L : LeitorDoFundo (Fin n → Bool)) :
    (1 - κ.beta) * particao c s ≤ ((Finset.univ.filter (fun y => c y = 0)).card : ℝ) :=
  (o_tetelestai_e_um_menos_beta n c h κ.beta_pos κ.beta_lt_one hs0 hs L).1

-- SONDA 6 (R3): a hipotese 0 <= s e' dita; sem ela e com b > 1/2 o limiar e' negativo: exibir que o limiar e' negativo para b = 9/10, n = 1 (o contraexemplo numerico esta' no meu script Python, em Fraction)
example : (1 : ℝ) * Real.log 2 + Real.log ((1 - (9/10 : ℝ)) / (9/10)) < 0 := by
  have h1 : Real.log ((1 - (9/10 : ℝ)) / (9/10)) = - Real.log 9 := by
    rw [show ((1 - (9/10 : ℝ)) / (9/10)) = (9 : ℝ)⁻¹ by norm_num, Real.log_inv]
  rw [h1]
  have : Real.log 2 < Real.log 9 := Real.log_lt_log (by norm_num) (by norm_num)
  linarith

#check @TGLExt.TraducaoTuring.particao
