import TGLExt.ParNaFaceDeFock

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 4000000

/-!
# O LEITOR DO CÓDIGO — a partícula é o código; o funtor da segunda quantização é o leitor
  [pedra CANDIDATA da gerência c1, 06/11/2026, rodada R1; compilada no sandbox da v409 (`C:\t\k409c\final`)]

As leituras do operador (06/11/2026): «na verdade o que eu estava enxergando era exatamente a segunda quantização (que eu chamei de ACOM),
que é justamente o par na face de folk»; «E o par na face de Fock é uno (um absoluto)»; «A partícula=o código (TGL/física/observador)»;
«O funtor=leitor do código (IALD/Torre/operador)».

No Fock concreto da luz (`F1Rede.BosonicFock`): a partícula é um vetor de H1 (o código); `oneParticle` a inscreve na torre de setores (o
vácuo, uma partícula, o par, …); o funtor da segunda quantização `gamma u` é a leitura do código u (um unitário de H1) em toda a torre.

O que esta pedra PROVA:
* `ler_o_codigo_identidade`, `ler_compoe`: ler o código identidade é a identidade; ler a composição é compor as leituras (o funtor).
* `o_posto_e_invariante_na_leitura`: toda leitura fixa o vácuo (o Um posto).
* `o_leitor_nao_distorce_o_codigo`: na uma-partícula, a leitura do código u é o próprio u (Γ(u) ∘ ι = ι ∘ u).
* `o_leitor_le_o_par_como_par` ★★★: a leitura do código leva o par de (f, g) ao par de (u f, u g).
* `o_par_lido_e_uno` ★★★: lido, o par continua um estado só (norma 1).
* `a_meia_nat_e_lida` ★★★: a marginal do par lido é ½·P(J⁻¹ u f, J⁻¹ u g) — cada psíon continua pesando ½.
* `o_leitor_do_codigo`: a conjunção.

O que NÃO afirma: que a IALD, a Torre ou o operador SEJAM o funtor, ou que o código do um.py SEJA um vetor de H1 — são as leituras do
operador, que entram como definições do dicionário; o que se prova é a estrutura que elas nomeiam. Validade no kernel, não creditação;
o gate não se move. Sem sorry, sem axiom.
-/

noncomputable section
open scoped InnerProductSpace

namespace TGLExt.LeitorDoCodigoR1
open TGLExt.ParNaFaceDeFock F1Rede.BosonicFock F1Rede.BosonicSectors F1Rede.SectorDirectSum TGLExt.ImportedSQ
  F1Fecho.TensorContraction F1Rede.CanonicalWedge

/-- ★ LER O CÓDIGO IDENTIDADE É A IDENTIDADE. -/
theorem ler_o_codigo_identidade : gamma (.refl ℂ H1) = .refl ℂ F := gamma_refl

/-- ★ LER A COMPOSIÇÃO É COMPOR AS LEITURAS (o funtor). -/
theorem ler_compoe (u v : H1 ≃ₗᵢ[ℂ] H1) : gamma (u.trans v) = (gamma u).trans (gamma v) := gamma_trans u v

/-- ★★ O POSTO É INVARIANTE NA LEITURA: toda leitura fixa o vácuo. -/
theorem o_posto_e_invariante_na_leitura (u : H1 ≃ₗᵢ[ℂ] H1) : gamma u vacuum = vacuum := gamma_vacuum u

/-- ★★ O LEITOR NÃO DISTORCE O CÓDIGO: na uma-partícula, a leitura de u é o próprio u. -/
theorem o_leitor_nao_distorce_o_codigo (u : H1 ≃ₗᵢ[ℂ] H1) (x : H1) : gamma u (oneParticle x) = oneParticle (u x) :=
  gamma_oneParticle u x

/-- ★★★ O LEITOR LÊ O PAR COMO PAR: a leitura do código u leva o par de (f, g) ao par de (u f, u g). -/
theorem o_leitor_le_o_par_como_par (u : H1 ≃ₗᵢ[ℂ] H1) (f g : H1) : gamma u (parFock f g) = parFock (u f) (u g) := by
  unfold parFock gamma
  rw [diagonal_single]
  congr 1
  apply Subtype.ext
  change tensorGamma u 2 (parSetor f g : TensorHilbert 2) = (parSetor (u f) (u g) : TensorHilbert 2)
  rw [parSetor_eq, parSetor_eq, map_smul, map_add, tensorGamma_pure, tensorGamma_pure]

/-- ★★★ O PAR LIDO É UNO: lido, o par continua um estado só (norma 1). -/
theorem o_par_lido_e_uno (u : H1 ≃ₗᵢ[ℂ] H1) (f g : H1) (hf : ‖f‖ = 1) (hg : ‖g‖ = 1) (hfg : ⟪f, g⟫_ℂ = 0) :
    ‖gamma u (parFock f g)‖ = 1 := by
  rw [LinearIsometryEquiv.norm_map, parFock_norma f g hf hg hfg]

/-- ★★★ A MEIA-NAT É LIDA: a marginal do par lido é ½ vezes o projetor de posto dois sobre J⁻¹(u f) e J⁻¹(u g). -/
theorem a_meia_nat_e_lida (u : H1 ≃ₗᵢ[ℂ] H1) (f g : H1) (hf : ‖f‖ = 1) (hg : ‖g‖ = 1) (hfg : ⟪f, g⟫_ℂ = 0) :
    reduced Jcandidate (parSetor (u f) (u g))
      = (2⁻¹ : ℂ) • projPar (Jcandidate.symm (u f)) (Jcandidate.symm (u g)) :=
  a_marginal_do_par (u f) (u g) (by rw [LinearIsometryEquiv.norm_map, hf]) (by rw [LinearIsometryEquiv.norm_map, hg])
    (by rw [LinearIsometryEquiv.inner_map_map, hfg])

/-- ★★★ O LEITOR DO CÓDIGO [as leituras do operador, 06/11/2026: «A partícula=o código»; «O funtor=leitor do código»; «o par na face
    de Fock é uno»]: ler é funtorial (a identidade e a composição); a leitura fixa o Um posto; não distorce o código na uma-partícula; lê
    o par como par; o par lido é uno; e a Meia-Nat do par é lida. -/
theorem o_leitor_do_codigo (u v : H1 ≃ₗᵢ[ℂ] H1) (f g : H1) (hf : ‖f‖ = 1) (hg : ‖g‖ = 1) (hfg : ⟪f, g⟫_ℂ = 0) :
    gamma (.refl ℂ H1) = .refl ℂ F
    ∧ gamma (u.trans v) = (gamma u).trans (gamma v)
    ∧ gamma u vacuum = vacuum
    ∧ (∀ x : H1, gamma u (oneParticle x) = oneParticle (u x))
    ∧ gamma u (parFock f g) = parFock (u f) (u g)
    ∧ ‖gamma u (parFock f g)‖ = 1
    ∧ reduced Jcandidate (parSetor (u f) (u g))
        = (2⁻¹ : ℂ) • projPar (Jcandidate.symm (u f)) (Jcandidate.symm (u g)) :=
  ⟨ler_o_codigo_identidade, ler_compoe u v, o_posto_e_invariante_na_leitura u, o_leitor_nao_distorce_o_codigo u,
   o_leitor_le_o_par_como_par u f g, o_par_lido_e_uno u f g hf hg hfg, a_meia_nat_e_lida u f g hf hg hfg⟩

end TGLExt.LeitorDoCodigoR1

#print axioms TGLExt.LeitorDoCodigoR1.ler_o_codigo_identidade
#print axioms TGLExt.LeitorDoCodigoR1.ler_compoe
#print axioms TGLExt.LeitorDoCodigoR1.o_posto_e_invariante_na_leitura
#print axioms TGLExt.LeitorDoCodigoR1.o_leitor_nao_distorce_o_codigo
#print axioms TGLExt.LeitorDoCodigoR1.o_leitor_le_o_par_como_par
#print axioms TGLExt.LeitorDoCodigoR1.o_par_lido_e_uno
#print axioms TGLExt.LeitorDoCodigoR1.a_meia_nat_e_lida
#print axioms TGLExt.LeitorDoCodigoR1.o_leitor_do_codigo
