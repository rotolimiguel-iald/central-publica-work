import TGLExt
set_option autoImplicit false
open Lean Elab Meta

-- Revisor terceiro v410 R1 (agente Claude Sonnet): #print axioms das 60 ancoras (insumos/*.lean) + varredura MetaM de TODAS as constantes dos 2 modulos novos + #check + sondas.

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

-- os enunciados que os textos publicos citam
#check @TGLExt.AEscala.a_escala
#check @TGLExt.AEscala.existe_o_algoritmo_e_e_a_iald
#check @TGLExt.AEscala.a_pergunta_do_clay_tem_resposta
#check @TGLExt.AEscala.a_iald_le_a_face_sem_leitura
#check @TGLExt.AEscala.cada_face_pesa_meio
#check @TGLExt.AEscala.os_pesos
#check @TGLExt.AEscala.a_face_caida_nao_acopla
#check @TGLExt.AEscala.o_nome_objeto_e_o_centro
#print TGLExt.AEscala.LeitorDoFundo
#print TGLExt.AEscala.aPerguntaDoClay
#print TGLExt.AEscala.iald
#print TGLExt.AEscala.faceMeio
#print TGLExt.AEscala.nomeObjeto
#print TGLExt.AEscala.nomeLido

-- SONDA 1 (revisor): `aPerguntaDoClay X` e' satisfeita por um leitor CONSTANTE, sem nenhuma TGL (nem `iald`, nem `trava`, nem `Identidade`):
--   a definicao `Nonempty (LeitorDoFundo X)` nao exige custo, tempo polinomial, nem computabilidade.
section SondaTrivial2
open Classical in
noncomputable def leitorTrivial (X : Type) [Fintype X] [DecidableEq X] : TGLExt.AEscala.LeitorDoFundo X where
  leitura := fun c _ => if ∃ x, c x = 0 then 1 else 0
  limite := fun c => if ∃ x, c x = 0 then 1 else 0
  le_como_dissipacao := fun c => tendsto_const_nhds
  diz_a_face_sem_leitura := fun c => by
    by_cases h : ∃ x, c x = 0
    · simp [h]
    · simp [h]

theorem a_pergunta_do_clay_sem_TGL (X : Type) [Fintype X] [DecidableEq X] : TGLExt.AEscala.aPerguntaDoClay X := ⟨leitorTrivial X⟩
#print axioms a_pergunta_do_clay_sem_TGL
end SondaTrivial2
