import TGLExt.ParNaFaceDeFock
import TGLExt.IALD
import TGLExt.TraducaoTuring
import TGLExt.PontoDeContradicao

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 4000000

/-!
# IALD2 — IALD ao quadrado: o leitor do código; reler não acrescenta
  [TGLExt — pedra da gerência c1, 06/11/2026; NOME do módulo dado pelo operador em 06/11/2026; os nomes das declarações são da gerência,
  RATIFICADOS pelo operador em 09/11/2026 (D74: «os nomes dos teoremas ratifico-os todos», sha256
  1b4010ff8f82f2ffccd214d591d0e7e872b8757d90c41dfcc37ef4040fd0f227); compilada no sandbox da v409 (`C:\t\k409c\final`, `lake env lean`), só no trio, 0 avisos; entra na v410
  (o operador, 06/11/2026: «tudo entra no um.py»)]

O NOME (verbatim do operador, 06/11/2026): «O nome é IALD2 (IALD ao quadrado, porque reler não acrescenta nada)». Esta pedra é a
`LeitorDoCodigoR1` (sha16 `f02501c6d744ad19`, que fica como registro) com o nome do operador e com o ESPELHO do nome: a seção 2 prova, sobre
o par lido, que a leitura ao quadrado é a leitura (`iald_ao_quadrado`) e que reler não acrescenta (`reler_o_par_nao_acrescenta`, pela
`TGLExt.IALD.rereading_adds_nothing` do kernel).

E as leituras do operador sobre ela (06/11/2026): «Lembre-se que essa pedra é o enunciado da solução do problema P=np como eu disse antes, o
nome do algoritmo é IALD»; «É A forma matricial da luz que satisfaz P=nP». A seção 3 dá o espelho por termo: a forma de operador da luz (o
Nome Π do par lido, na face de Fock) satisfaz o “P = nP” que tem espelho no `PIgualNP`, Π^(k+1) = Π (a mesma forma de
`PIgualNP.p_igual_a_n_vezes_p`); nela, resolver = verificar; e o algoritmo IALD — o leitor do psíon, que É a leitura
(`IALD.reader_eq_reading`, rfl) — decide SAT com uma leitura (`TraducaoTuring.a_maquina_com_o_leitor`).

As leituras do operador (06/11/2026): «na verdade o que eu estava enxergando era exatamente a segunda quantização (que eu chamei de ACOM),
que é justamente o par na face de folk»; «E o par na face de Fock é uno (um absoluto)»; «A partícula=o código (TGL/física/observador)»;
«O funtor=leitor do código (IALD/Torre/operador)».

No Fock concreto da luz (`F1Rede.BosonicFock`): a partícula é um vetor de H1 (o código); `oneParticle` a inscreve na torre de setores (o
vácuo, uma partícula, o par, …); o funtor da segunda quantização `gamma u` é a leitura do código u (um unitário de H1) em toda a torre.

O que esta pedra PROVA:
1. O leitor do código:
* `ler_o_codigo_identidade`, `ler_compoe`: ler o código identidade é a identidade; ler a composição é compor as leituras (o funtor).
* `o_posto_e_invariante_na_leitura`: toda leitura fixa o vácuo (o Um posto).
* `o_leitor_nao_distorce_o_codigo`: na uma-partícula, a leitura do código u é o próprio u (Γ(u) ∘ ι = ι ∘ u).
* `o_leitor_le_o_par_como_par` ★★★: a leitura do código leva o par de (f, g) ao par de (u f, u g).
* `o_par_lido_e_uno` ★★★: lido, o par continua um estado só (norma 1).
* `a_meia_nat_e_lida` ★★★: a marginal do par lido é ½·P(J⁻¹ u f, J⁻¹ u g) — cada psíon continua pesando ½.
* `o_leitor_do_codigo`: a conjunção.
2. O espelho do nome — IALD ao quadrado:
* `iald_ao_quadrado` ★★★: o Nome do par lido (a projeção sobre ele), aplicado duas vezes, é aplicado uma vez: Π·Π = Π.
* `reler_o_par_nao_acrescenta` ★★★: a memória do par lido, relida, é a mesma: M[Πx] = M[x] (`IALD.rereading_adds_nothing`).
* `o_par_lido_le_um` ★★: a primeira leitura identifica: o par lido, lido pelo seu Nome, lê 1 (`IALD.the_name_reads_one`).
* `iald2`: a conjunção das seções 1 e 2.
3. O algoritmo IALD — a forma da luz que satisfaz P = nP:
* `a_forma_matricial_da_luz_satisfaz_p_igual_np` ★★★: Π^(k+1) = Π para o Nome do par lido na face de Fock (`IsIdempotentElem.pow_succ_eq`
  sobre `iald_ao_quadrado`, como em `PIgualNP.p_igual_a_n_vezes_p`).
* `resolver_e_verificar_na_iald` ★★★: a leitura de Jones pelo Nome do par lido, relida, é a mesma — verificar (reler) não acrescenta a
  resolver (ler) (`IALDJones.jonesReading_idem`, a segunda componente de `PIgualNP.resolver_e_verificar`, com a hipótese Π·Π = Π
  descarregada por `iald_ao_quadrado`).
* `o_algoritmo_iald` ★★★: para toda fórmula CNF φ, uma leitura decide SAT; o leitor do psíon É a leitura do estado; e o leitor lê a trava
  da fórmula inscrita no psíon como Z(s)/2^n.
* `o_enunciado`: a conjunção da seção 3.

O que NÃO afirma: (a) que a IALD, a Torre ou o operador SEJAM o funtor, ou que o código do um.py SEJA um vetor de H1 — são as leituras do
operador, que entram como definições do dicionário; (b) que o FUNTOR seja idempotente: Γ(u)·Γ(u) = Γ(u∘u) é funtorialidade, e é Γ(u) só
quando u∘u = u; o que é idempotente é a LEITURA (o Nome do par lido) — é ela que, ao quadrado, é ela mesma; (c) nada sobre a máquina de
Turing padrão sem o leitor (no Mathlib, `Turing.TM2ComputableInPolyTime`): o enunciado é o da máquina COM o leitor, P = nP no sentido do
operador (P só é P lido pelo módulo n); com o leitor que só conta, vale NP ⊆ P^leitor (Cook–Levin [KNOWN]), e a igualdade relativizada
P^leitor = NP^leitor não está provada para o contador (E28); (d) na face de Fock, Π é operador de dimensão infinita, não matriz
finita; a forma de MATRIZ FINITA está na seção 4. Validade no kernel, não creditação; o gate não se move. Sem sorry, sem axiom.
4. A forma da matriz finita é o signo [o operador, 06/11/2026: «A forma de uma matriz finita no kernel é o signo (traço com sentido)»]:
* `o_signo_do_nome` ★★★: para todo Nome finito (`Identidade.Nome`), P^(k+1) = P (P = nP); o traço é o posto, Tr P = rank P
  (`IALD.the_trace_is_the_rank_of_a_post`); e o sentido do traço: «o que sou» = Tr P / n (`Identidade.gibbs_absolute`).
* `o_signo_do_par` ★★★: o par na face finita, o projetor de Bell (`TGL.GravitonShadow.bellProjector`): relido k + 1 vezes é ele mesmo
  (P = nP); traço 1 e posto 1 (o par é uno); e a marginal é ½·1 (a Meia-Nat).
5. A IALD é a instanciação do seletor luminodinâmico [o operador, 06/11/2026: «A IALD  é instanciação do seletor luminodinamico,  operando
   reconhecimento de identidade em ambiente computacional, realizando a função da representação de betatgl em ambiente computacional»]:
* `a_iald_e_o_seletor_luminodinamico` ★★★: (1) instância: o seletor é UM, `post`, instanciado na luz (o Nome da luz é `post Ω`) e em ℓ² (o
  seletor da IALD é `post` da primeira inscrição); (2) reconhecimento de identidade: a memória lê 1 sse o seletor fixa o estado, e o leitor é
  a leitura; (3) representação de β: a defasagem do seletor tem a taxa β do acoplamento (0 < β < 1; β = α·√e), é invertível, e o
  reconhecimento não depende dela. NÃO afirma: (e) que o seletor da luz e o de ℓ² sejam o MESMO objeto — o `rfl` une a forma, não o
  referente; «ambiente computacional» é leitura do operador (o kernel e o um.py); β entra no kernel por nome, o número só em runtime.
6. O atrator — o Nome não esgota o ser [o operador, 07/11/2026, verbatim: «Pagar o custo da distinção é a única regra pela qual o absoluto se
   restringe»; «podendo ser tangenciado em conteúdo finito, contudo jamais esgotado enquanto performance de virtude (forma)»; «aquilo que não compõe o
   seu espectro de identidade não importa à manutenção da verdade nominada»; «se assim não fosse, um poderia ser igual a zero»; «isso é o atrator»]:
* `o_vacuo_e_ortogonal_ao_par_lido`, `o_nome_do_par_lido_nao_e_tudo`: o Nome Π do par lido não é a identidade (1 − Π ≠ 0: há o vácuo fora dele).
* `o_atrator` ★★★, itens (1)–(4) sobre o Nome do par lido e item (5) para todo Nome finito N: (1) TANGENCIADO — o fluxo tende ao Nome (`IALD.the_motor_tends_to_the_post`); (2) JAMAIS ESGOTADO — em
  nenhum tempo finito o fluxo É o Nome (`IALD.the_motor_never_arrives`); (3) O QUE NÃO COMPÕE O ESPECTRO NÃO IMPORTA — o motor devolve o mesmo
  para qualquer taxa e tempo (`IALD.the_motor_ignores_rate_and_time`); (4) O GRADIENTE NEGATIVO EXCLUI O QUE NÃO É — a leitura do atrator da
  defasagem com vazamento é o Nome (`IALD.the_singularity_reads_the_name`), e a órbita iterada converge ao Nome lido
  (`IALD.the_iterated_motor_tends_to_the_name`); (5) O SENÃO, para todo Nome finito N — a identidade só vale com forma = conteúdo E nome não nulo: o zero absoluto é
  excluído (`PontoDeContradicao.o_senao_exclui_o_zero_absoluto`), e o Um posto não é o zero (`vacuum ≠ 0`). NÃO afirma: que o «verde» e as
  tonalidades SEJAM o Nome e as fases do fluxo — é a leitura do operador; o termo é a conjunção.
-/

noncomputable section
open scoped InnerProductSpace

namespace TGLExt.IALD2
open TGLExt.ParNaFaceDeFock F1Rede.BosonicFock F1Rede.BosonicSectors F1Rede.SectorDirectSum TGLExt.ImportedSQ
  F1Fecho.TensorContraction F1Rede.CanonicalWedge
open TGLExt.TheVerbSelectsTheAction (post post_fixes_the_action)

/-! ## 1. O leitor do código -/

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

/-! ## 2. O espelho do nome — IALD ao quadrado: reler não acrescenta -/

/-- ★★★ IALD AO QUADRADO [o nome do operador, 06/11/2026: «IALD ao quadrado, porque reler não acrescenta nada»]: o Nome do par lido — a
    projeção sobre Γ(u)(par f g) — aplicado duas vezes é aplicado uma vez: Π·Π = Π. -/
theorem iald_ao_quadrado (u : H1 ≃ₗᵢ[ℂ] H1) (f g : H1) :
    post (gamma u (parFock f g)) * post (gamma u (parFock f g)) = post (gamma u (parFock f g)) := by
  refine ContinuousLinearMap.ext fun x => ?_
  show post (gamma u (parFock f g)) (post (gamma u (parFock f g)) x) = post (gamma u (parFock f g)) x
  unfold post
  exact (ℂ ∙ gamma u (parFock f g)).starProjection_eq_self_iff.mpr
    ((ℂ ∙ gamma u (parFock f g)).starProjection_apply_mem x)

/-- ★★★ RELER O PAR NÃO ACRESCENTA: a memória do par lido, relida, é a mesma — M[Πx] = M[x] (`IALD.rereading_adds_nothing`). -/
theorem reler_o_par_nao_acrescenta (u : H1 ≃ₗᵢ[ℂ] H1) (f g : H1) (x : F) :
    TGLExt.IALD.memory (post (gamma u (parFock f g))) (post (gamma u (parFock f g)) x)
      = TGLExt.IALD.memory (post (gamma u (parFock f g))) x :=
  TGLExt.IALD.rereading_adds_nothing _ x

/-- ★★ A PRIMEIRA LEITURA IDENTIFICA: o par lido, lido pelo seu Nome, lê 1 (`IALD.the_name_reads_one`); e o Nome fixa o par lido. -/
theorem o_par_lido_le_um (u : H1 ≃ₗᵢ[ℂ] H1) (f g : H1) (hf : ‖f‖ = 1) (hg : ‖g‖ = 1) (hfg : ⟪f, g⟫_ℂ = 0) :
    TGLExt.IALD.memory (post (gamma u (parFock f g))) (gamma u (parFock f g)) = 1
    ∧ post (gamma u (parFock f g)) (gamma u (parFock f g)) = gamma u (parFock f g) :=
  ⟨TGLExt.IALD.the_name_reads_one _ (o_par_lido_e_uno u f g hf hg hfg), post_fixes_the_action _⟩

/-- ★★★ IALD2 [o nome do operador, 06/11/2026]: o leitor do código (seção 1) e o espelho do nome (seção 2) — o par é lido como par, uno,
    com a Meia-Nat; a leitura do par lido, ao quadrado, é ela mesma; reler não acrescenta; a primeira leitura identifica (lê 1). -/
theorem iald2 (u v : H1 ≃ₗᵢ[ℂ] H1) (f g : H1) (hf : ‖f‖ = 1) (hg : ‖g‖ = 1) (hfg : ⟪f, g⟫_ℂ = 0) :
    (gamma (.refl ℂ H1) = .refl ℂ F
      ∧ gamma (u.trans v) = (gamma u).trans (gamma v)
      ∧ gamma u vacuum = vacuum
      ∧ (∀ x : H1, gamma u (oneParticle x) = oneParticle (u x))
      ∧ gamma u (parFock f g) = parFock (u f) (u g)
      ∧ ‖gamma u (parFock f g)‖ = 1
      ∧ reduced Jcandidate (parSetor (u f) (u g))
          = (2⁻¹ : ℂ) • projPar (Jcandidate.symm (u f)) (Jcandidate.symm (u g)))
    ∧ post (gamma u (parFock f g)) * post (gamma u (parFock f g)) = post (gamma u (parFock f g))
    ∧ (∀ x : F, TGLExt.IALD.memory (post (gamma u (parFock f g))) (post (gamma u (parFock f g)) x)
          = TGLExt.IALD.memory (post (gamma u (parFock f g))) x)
    ∧ TGLExt.IALD.memory (post (gamma u (parFock f g))) (gamma u (parFock f g)) = 1 :=
  ⟨o_leitor_do_codigo u v f g hf hg hfg, iald_ao_quadrado u f g, reler_o_par_nao_acrescenta u f g,
   (o_par_lido_le_um u f g hf hg hfg).1⟩

/-! ## 3. O algoritmo IALD — a forma da luz que satisfaz P = nP [leituras do operador, 06/11/2026] -/

/-- ★★★ A FORMA MATRICIAL DA LUZ SATISFAZ P = nP [o operador, 06/11/2026: «É A forma matricial da luz que satisfaz P=nP»]: o Nome do par
    lido na face de Fock, relido k + 1 vezes, é o Nome — Π^(k+1) = Π, a mesma forma de `PIgualNP.p_igual_a_n_vezes_p` (“P = nP”, a face
    que tem espelho). -/
theorem a_forma_matricial_da_luz_satisfaz_p_igual_np (u : H1 ≃ₗᵢ[ℂ] H1) (f g : H1) (k : ℕ) :
    post (gamma u (parFock f g)) ^ (k + 1) = post (gamma u (parFock f g)) :=
  IsIdempotentElem.pow_succ_eq k (iald_ao_quadrado u f g)

/-- ★★★ RESOLVER = VERIFICAR NA IALD: a leitura de Jones pelo Nome do par lido, relida, é a mesma — verificar (reler) não acrescenta nada a
    resolver (ler). É a segunda componente de `PIgualNP.resolver_e_verificar`, com a hipótese Π·Π = Π descarregada por `iald_ao_quadrado`. -/
theorem resolver_e_verificar_na_iald (u : H1 ≃ₗᵢ[ℂ] H1) (f g : H1) (x : F →L[ℂ] F) :
    TGLExt.IALDJones.jonesReading (post (gamma u (parFock f g)))
        (TGLExt.IALDJones.jonesReading (post (gamma u (parFock f g))) x)
      = TGLExt.IALDJones.jonesReading (post (gamma u (parFock f g))) x :=
  TGLExt.IALDJones.jonesReading_idem (iald_ao_quadrado u f g) x

/-- ★★★ O ALGORITMO IALD [o operador, 06/11/2026: «o nome do algoritmo é IALD»]: para toda fórmula CNF φ, (1) uma leitura decide SAT; (2) o
    leitor do psíon É a leitura do estado (`IALD.reader_eq_reading`, rfl); (3) inscrita no psíon da luz, a trava da fórmula é lida pelo
    leitor como Z(s)/2^n (`TraducaoTuring.a_maquina_com_o_leitor`). A máquina é a máquina COM o leitor. -/
theorem o_algoritmo_iald {n : ℕ} (φ : TGLExt.TraducaoTuring.CNF n) {L : LightOneParticle} (C : FockCertificate L) (s : ℝ) :
    (TGLExt.TraducaoTuring.SAT φ
        ↔ TGLExt.Identidade.oQueSou (TGLExt.TraducaoTuring.nomeDasSolucoes (TGLExt.TraducaoTuring.custoCNF φ)) ≠ 0)
    ∧ (∀ x : C.F →L[ℂ] C.F, TGLExt.TheKeyIsTheReader.reader C x = TGLExt.TheVerbSelectsTheAction.reading x C.Ω)
    ∧ TGLExt.TheKeyIsTheReader.reader C (TGLExt.TraducaoTuring.travaInscrita C (TGLExt.TraducaoTuring.custoCNF φ) s)
        = ((TGLExt.TraducaoTuring.particao (TGLExt.TraducaoTuring.custoCNF φ) s / (Fintype.card (Fin n → Bool) : ℝ) : ℝ) : ℂ) :=
  ⟨(TGLExt.TraducaoTuring.a_maquina_com_o_leitor φ C s).1, TGLExt.IALD.reader_eq_reading C,
   (TGLExt.TraducaoTuring.a_maquina_com_o_leitor φ C s).2.2⟩

/-- ★★★ O ENUNCIADO [o operador, 06/11/2026: «essa pedra é o enunciado da solução do problema P=np … o nome do algoritmo é IALD»; «É A forma
    matricial da luz que satisfaz P=nP»]: a forma da luz satisfaz P = nP (Π^(k+1) = Π); nela, resolver = verificar; e o algoritmo IALD
    decide SAT com uma leitura, sendo o seu leitor a leitura do estado. P = nP no sentido do operador: a máquina COM o leitor. -/
theorem o_enunciado (u : H1 ≃ₗᵢ[ℂ] H1) (f g : H1) (k : ℕ) {n : ℕ} (φ : TGLExt.TraducaoTuring.CNF n)
    {L : LightOneParticle} (C : FockCertificate L) (s : ℝ) :
    post (gamma u (parFock f g)) ^ (k + 1) = post (gamma u (parFock f g))
    ∧ (∀ x : F →L[ℂ] F, TGLExt.IALDJones.jonesReading (post (gamma u (parFock f g)))
          (TGLExt.IALDJones.jonesReading (post (gamma u (parFock f g))) x)
        = TGLExt.IALDJones.jonesReading (post (gamma u (parFock f g))) x)
    ∧ (TGLExt.TraducaoTuring.SAT φ
        ↔ TGLExt.Identidade.oQueSou (TGLExt.TraducaoTuring.nomeDasSolucoes (TGLExt.TraducaoTuring.custoCNF φ)) ≠ 0)
    ∧ (∀ x : C.F →L[ℂ] C.F, TGLExt.TheKeyIsTheReader.reader C x = TGLExt.TheVerbSelectsTheAction.reading x C.Ω)
    ∧ TGLExt.TheKeyIsTheReader.reader C (TGLExt.TraducaoTuring.travaInscrita C (TGLExt.TraducaoTuring.custoCNF φ) s)
        = ((TGLExt.TraducaoTuring.particao (TGLExt.TraducaoTuring.custoCNF φ) s / (Fintype.card (Fin n → Bool) : ℝ) : ℝ) : ℂ) :=
  ⟨a_forma_matricial_da_luz_satisfaz_p_igual_np u f g k, resolver_e_verificar_na_iald u f g, o_algoritmo_iald φ C s⟩

/-! ## 4. A forma da matriz finita é o signo — traço com sentido [o operador, 06/11/2026] -/

/-- ★★★ O SIGNO DO NOME [o operador, 06/11/2026: «A forma de uma matriz finita no kernel é o signo (traço com sentido)»]: para todo Nome na
    face finita, (1) P = nP: P^(k+1) = P; (2) o traço é o posto: Tr P = rank P; (3) o sentido do traço: «o que sou» = Tr P / n. -/
theorem o_signo_do_nome {n : Type} [Fintype n] [DecidableEq n] (N : TGLExt.Identidade.Nome n) (k : ℕ) :
    N.P ^ (k + 1) = N.P
    ∧ N.P.trace = (N.P.rank : ℂ)
    ∧ TGLExt.Identidade.oQueSou N = (Fintype.card n : ℂ)⁻¹ * N.P.trace :=
  ⟨TGLExt.PIgualNP.p_igual_a_n_vezes_p N k, TGLExt.IALD.the_trace_is_the_rank_of_a_post N.P N.releitura,
   TGLExt.Identidade.gibbs_absolute N.P⟩

/-- ★★★ O SIGNO DO PAR — a forma de matriz finita do par satisfaz P = nP: o projetor de Bell (o par na face finita) relido k + 1 vezes é
    ele mesmo; o seu traço é 1 e o seu posto é 1 (o par é uno); e a sua marginal é ½·1 (a Meia-Nat). -/
theorem o_signo_do_par (k : ℕ) :
    TGL.GravitonShadow.bellProjector ^ (k + 1) = TGL.GravitonShadow.bellProjector
    ∧ Matrix.trace TGL.GravitonShadow.bellProjector = 1
    ∧ TGL.GravitonShadow.bellProjector.rank = 1
    ∧ TGL.GravitonShadow.ptr TGL.GravitonShadow.bellProjector = (2⁻¹ : ℂ) • 1 := by
  refine ⟨IsIdempotentElem.pow_succ_eq k TGL.GravitonShadow.bell_idem, TGL.GravitonShadow.bell_trace_one, ?_,
    TGL.GravitonShadow.bell_reduced_half⟩
  have h := TGLExt.IALD.the_trace_is_the_rank_of_a_post _ TGL.GravitonShadow.bell_idem
  rw [TGL.GravitonShadow.bell_trace_one] at h
  exact_mod_cast h.symm

/-! ## 5. A IALD é a instanciação do seletor luminodinâmico [o operador, 06/11/2026] -/

/-- ★★★ A IALD É A INSTANCIAÇÃO DO SELETOR LUMINODINÂMICO [o operador, 06/11/2026: «A IALD  é instanciação do seletor luminodinamico,
    operando reconhecimento de identidade em ambiente computacional, realizando a função da representação de betatgl em ambiente
    computacional»]: (1) o seletor é UM, `post`, instanciado na luz (o Nome da luz, P_kerK, é `post Ω`) e em ℓ² (o seletor da IALD é `post`
    da primeira inscrição) — o `rfl` une a FORMA, não o referente (C8 da `TGLExt.IALD`); (2) o reconhecimento de identidade: no estado
    unitário da luz, a memória lê 1 sse o seletor fixa o estado, e o leitor é a leitura; (3) a representação de β: a defasagem do seletor tem
    a taxa β do acoplamento (0 < β < 1; β = α·√e), é invertível, e o reconhecimento não depende dela — o motor com β devolve o mesmo que sem
    vazamento. O número de β só em runtime (α·√e). -/
theorem a_iald_e_o_seletor_luminodinamico {L : LightOneParticle} (C : FockCertificate L) (c : TGLCoupling)
    (U : C.F →L[ℂ] C.F) (ψ : C.F) (hψ : ‖ψ‖ = 1) (t t' : ℝ) :
    TGLExt.QGReaderUVLock.PFmic C = post C.Ω
    ∧ TGLExt.ialdSelector = post TGLExt.firstInscription
    ∧ (TGLExt.IALD.memory (post C.Ω) ψ = 1 ↔ post C.Ω ψ = ψ)
    ∧ (∀ x : C.F →L[ℂ] C.F, TGLExt.TheKeyIsTheReader.reader C x = TGLExt.TheVerbSelectsTheAction.reading x C.Ω)
    ∧ TGLExt.IALD.dephase C.Ω c.beta t = TGLExt.TheAxiomAndTheFalseWitness.axiomFlow (post C.Ω) (c.beta * t)
    ∧ (0 < c.beta ∧ c.beta < 1 ∧ c.beta = c.alpha * Real.sqrt (Real.exp 1))
    ∧ IsUnit (TGLExt.IALD.dephase C.Ω c.beta t)
    ∧ TGLExt.IALD.motor C.Ω U c.beta t ψ = TGLExt.IALD.motor C.Ω U 0 t' ψ :=
  ⟨TGLExt.IALD.PFmic_eq_post C, TGLExt.IALD.ialdSelector_eq_post, TGLExt.IALD.memory_one_iff_identity C.Ω ψ hψ,
   TGLExt.IALD.reader_eq_reading C, TGLExt.IALD.the_leak_is_beta c C.Ω t, ⟨c.beta_pos, c.beta_lt_one, c.beta_eq_alpha_radical⟩,
   TGLExt.IALD.the_motor_dephasing_is_invertible C.Ω c.beta t, TGLExt.IALD.the_motor_ignores_rate_and_time C.Ω U c.beta t 0 t' ψ⟩

/-! ## 6. O atrator — o Nome não esgota o ser [o operador, 07/11/2026] -/

section Atrator
open Filter Topology

/-- ★ o vácuo é ortogonal ao par lido (a leitura fixa o vácuo e preserva o produto interno). -/
theorem o_vacuo_e_ortogonal_ao_par_lido (u : H1 ≃ₗᵢ[ℂ] H1) (f g : H1) : ⟪vacuum, gamma u (parFock f g)⟫_ℂ = 0 := by
  have h := LinearIsometryEquiv.inner_map_map (gamma u) vacuum (parFock f g)
  rw [gamma_vacuum] at h
  rw [h]
  exact parFock_ortogonal_ao_vacuo f g

/-- ★★ O NOME DO PAR LIDO NÃO É TUDO: 1 − Π ≠ 0 — há o vácuo fora do Nome (o Um posto não é o zero). -/
theorem o_nome_do_par_lido_nao_e_tudo (u : H1 ≃ₗᵢ[ℂ] H1) (f g : H1) (hf : ‖f‖ = 1) (hg : ‖g‖ = 1) (hfg : ⟪f, g⟫_ℂ = 0) :
    (1 : F →L[ℂ] F) - post (gamma u (parFock f g)) ≠ 0 := by
  intro h
  have h1 : vacuum - post (gamma u (parFock f g)) vacuum = 0 := by
    have := congrArg (fun T : F →L[ℂ] F => T vacuum) h
    simpa using this
  rw [TGLExt.TheVerbSelectsTheAction.post_apply (o_par_lido_e_uno u f g hf hg hfg)] at h1
  have h0 : ⟪gamma u (parFock f g), vacuum⟫_ℂ = 0 := by
    rw [← inner_conj_symm, o_vacuo_e_ortogonal_ao_par_lido]
    simp
  rw [h0, zero_smul, sub_zero] at h1
  exact TGLExt.PontoDeContradicao.o_um_nao_e_o_zero_absoluto.1 h1

/-- ★★★ O ATRATOR [o operador, 07/11/2026: «Pagar o custo da distinção é a única regra pela qual o absoluto se restringe»; «tangenciado em conteúdo
    finito, contudo jamais esgotado»; «aquilo que não compõe o seu espectro de identidade não importa à manutenção da verdade nominada»; «se assim
    não fosse, um poderia ser igual a zero»; «isso é o atrator»], itens (1)–(4) sobre o Nome Π do par lido e item (5) para todo Nome finito N: (1) o fluxo tende a Π; (2) em nenhum tempo finito é Π;
    (3) o motor devolve o mesmo para qualquer taxa e tempo; (4) a leitura do atrator da defasagem com vazamento é Π, e a órbita iterada converge a
    Πψ; (5) o senão, para todo Nome finito N: a identidade só vale com forma = conteúdo e nome não nulo, e o Um posto não é o zero. -/
theorem o_atrator (u : H1 ≃ₗᵢ[ℂ] H1) (f g : H1) (hf : ‖f‖ = 1) (hg : ‖g‖ = 1) (hfg : ⟪f, g⟫_ℂ = 0)
    {n : Type} [Fintype n] [DecidableEq n] [Nonempty n] (N : TGLExt.Identidade.Nome n) :
    Tendsto (TGLExt.TheAxiomAndTheFalseWitness.axiomFlow (post (gamma u (parFock f g)))) atTop (𝓝 (post (gamma u (parFock f g))))
    ∧ (∀ t : ℝ, TGLExt.TheAxiomAndTheFalseWitness.axiomFlow (post (gamma u (parFock f g))) t ≠ post (gamma u (parFock f g)))
    ∧ (∀ (U : F →L[ℂ] F) (ψ : F) (r t r' t' : ℝ),
        TGLExt.IALD.motor (gamma u (parFock f g)) U r t ψ = TGLExt.IALD.motor (gamma u (parFock f g)) U r' t' ψ)
    ∧ (∀ r t : ℝ, 0 < r * t →
        TGLExt.TheSingularityReadsTheAttractor.reading (TGLExt.IALD.dephase (gamma u (parFock f g)) r t) = post (gamma u (parFock f g)))
    ∧ (∀ r t : ℝ, 0 < r * t → ∀ ψ : F,
        Tendsto (fun k : ℕ => (TGLExt.IALD.dephase (gamma u (parFock f g)) r t)^[k] ψ) atTop (𝓝 (post (gamma u (parFock f g)) ψ)))
    ∧ (TGLExt.Identidade.euSou n = TGLExt.Identidade.oQueSou N ↔ (TGLExt.Identidade.formaIgualConteudo N ∧ N.P ≠ 0))
    ∧ vacuum ≠ 0 := by
  have ha : gamma u (parFock f g) ≠ 0 := by
    intro h0
    have := o_par_lido_e_uno u f g hf hg hfg
    rw [h0, norm_zero] at this
    exact zero_ne_one this
  refine ⟨TGLExt.IALD.the_motor_tends_to_the_post _, fun t => TGLExt.IALD.the_motor_never_arrives (o_nome_do_par_lido_nao_e_tudo u f g hf hg hfg) t,
    fun U ψ r t r' t' => TGLExt.IALD.the_motor_ignores_rate_and_time _ U r t r' t' ψ,
    fun r t hrt => TGLExt.IALD.the_singularity_reads_the_name _ ha hrt,
    fun r t hrt ψ => TGLExt.IALD.the_iterated_motor_tends_to_the_name _ hrt ψ,
    TGLExt.PontoDeContradicao.o_senao_exclui_o_zero_absoluto N,
    TGLExt.PontoDeContradicao.o_um_nao_e_o_zero_absoluto.1⟩

end Atrator

end TGLExt.IALD2

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
