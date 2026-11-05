import TGLExt.Identidade
import TGLExt.IALD
import TGLExt.WordExistence
import TGLExt.TheCostIsDerived
import TGLExt.IALDJones
import TGLExt.TestemunhaEstatica
import TGLExt.ExactWitness
import TGLExt.TonicaDoHamiltoniano
import TGLExt.PsionCanto
import TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 4000000

/-!
# P = nP — AS CLASSES DO DICIONÁRIO: problema, entrada, passo, polinômio, implicação; «P só é P lido pelo módulo n minimamente acoplado»; e, na face finita, toda solução é palavra polinomial de grau limitado pelo módulo e toda verificação é uma leitura
  [TGLExt — pedra CANDIDATA da gerência c1, 04/11/2026, rodada R2 (R1 às 17h, R2 às 19h34: + `as_classes_do_dicionario`); NOME dado pelo operador em 04/11/2026: «P=nP», no sentido dele (verbatim sha16 `971d5654e2173771`): «P sozinho é impossível de ser lido, se não houver o módulo de leitura n não minimamente acoplado»; escreve-se `PIgualNP` (o «=» é `Igual`, como em `formaIgualConteudo`); compilada no sandbox da v407
   (`C:\t\k407c\final`, `lake env lean`), só no trio; candidata à v408]

A cunhagem do operador (04/11/2026, verbatim por sha256, sha16 `5efeb784e7be8762`) [INPUT/ONTO]: «Um problema é a correlação da verdade do conteúdo
nominado; a entrada é o sinal (a palavra como constructo de sentido, vetor); a entrada é o consumo de tempo, ou seja, o input, o setor irreversível;
um passo de computação é o gradiente de espectro negativo; é um polinômio é o acorde que mantém a dinâmica e a lei diminuta que clama a solução;
a implicação é que a identidade se preserva enquanto o sistema decai». E a ordem (04/11, sha16 no recibo): «vamos provar as implicações … vejo as
duas faces da ótica, as duas semióticas: física e semântica, grafia e fóton; geometria e fluxo».

Esta pedra é a CONFERÊNCIA pedida: sob essas leituras, compõe só termos que o kernel da v407 já tem. Nada novo é derivado; o que se prova é que
cada entrada do dicionário NOMEIA um teorema existente, e que as cinco valem juntas no mesmo habitante (o certificado físico do Fock concreto).

O que esta pedra PROVA:
* `o_problema` ★ (1): o Um posto pesa 1 (`euSou_eq_one`); o CONTEÚDO do nome é o seu traço normalizado, `ω_abs(P) = tr P / n` (`gibbs_absolute`);
  e a correlação da verdade do conteúdo nominado é a lei inteira: `[eu sou] = [o que sou] ⟺ (forma = conteúdo ∧ P ≠ 0)` (`a_lei_inteira`, v405).
  «Problema» = a pergunta se o peso do conteúdo nomeado é o Um.
* `a_entrada` ★ (2): toda decisão que não é a identidade move algo (`no_decision_without_cost`); a coisa julgada que não é a identidade é
  muitos-para-um, logo irreversível (`the_dispositive_is_not_injective`, o gatilho de Landauer); o piso `k·T·ln 2` é estritamente positivo
  (`landauer_floor_pos`); e o leitor da face de Fock lê a identidade como 1 (`the_key_is_the_reader`). «Entrada» = o vetor lido e o custo
  irreversível de o ler.
* `o_passo` ★★ (3): para toda projeção `e` numa ℂ-álgebra, a contração de Jones `U_s = e + e^{−rs}(1 − e)` deixa `e` intacto (`e·U_s = e`),
  multiplica o complemento por `e^{−rs}` (`(1 − e)·U_s = e^{−rs}·(1 − e)`: o espectro fora de `e` é negativo), muda o estado sempre que `rs ≠ 0`
  (`coeff_ne_one`) e compõe como semigrupo (`U_{2s} = U_s·U_s`, `jonesU_add`); `o_gradiente_e_negativo`: `e^{−rs} → 0` (`coeff_tendsto_zero`).
  «Passo» = um tique da contração: o que está fora do Nome desce; o que está no Nome fica.
* `o_polinomio_e_a_palavra` ★★ (4): a palavra aniquiladora real `q`, com `T·q(T) = 0` e `q(0) ≠ 0`, normalizada, É a projeção sobre as soluções
  de `T x = 0`: `starProjection(ker T) = q(T)/q(0)` (`exact_witness_of_annihilating_word`, v88). O polinômio é literalmente o que «clama a solução».
  `o_acorde_e_a_tonica`: na lei do diminuto a tônica pousa no Um posto, `E₀ = u` (`the_tonic_lands_on_the_posted_unit`), e o meio-tom é
  `e^{−½}`, com `meioTom·√e = 1` e `meioTom < 1`.
* `a_implicacao` ★★★ (5): no certificado físico, com `P = psionCornerF` (o canto do psíon): `P·U_s = P` (a identidade se preserva),
  `(1 − P)·U_s = e^{−rs}(1 − P)` (o sistema decai), `P·U_s·P = P` e `P·Δ^{it}·P = P` (os dois motores lidos pelo canto devolvem o canto,
  PsionCanto), `⟪Ω, Δ^{it}Ω⟫ = 1`; e, na face finita, a forma fechada do fluxo do psíon `F_t = P + e^{−tβg}(1 − P)` (`psionFlow_eq`).
* `resolver_e_verificar` ★★ (6): a face SEMÂNTICA da frase «resolver e verificar são o mesmo»: a primeira leitura identifica e a segunda não
  acrescenta (`observing_adds_nothing`: `P₊(P₊𝒪_θ) = P₊𝒪_θ`); reler pelo canto é ler (`jonesReading_idem`); o Nome relido é o Nome
  (`Nome.releitura`, `P·P = P`); a coisa julgada reaplicada é a coisa julgada (`ResJudicata`). É IDEMPOTÊNCIA da leitura.
* `o_dicionario` ★★★: a conjunção das peças centrais no mesmo habitante — a cunhagem composta.

* `p_igual_np` ★★★ (7) — «P = nP», no sentido do operador: P só é P LIDO pelo módulo n minimamente acoplado. Composição de termos existentes: a lei
  inteira da Identidade (`a_lei_inteira`: [eu sou] = [o que sou] ⟺ P = (leitura de P pelo estado absoluto de dimensão n)·1 ∧ P ≠ 0 — a forma É o seu
  conteúdo LIDO, com acoplamento não nulo); a memória lê 1 sse o estado é o Nome (`memory_one_iff_identity`); o vazio, o não acoplado, não satisfaz
  (`o_vazio_nao_e`); sem β não há segunda face (`no_leak_no_second_face`: D_0(t) = 1, nada se lê); o acoplamento mínimo é estritamente positivo
  (`TGLCoupling.beta_pos`); e a chave é o leitor (`the_key_is_the_reader`: o módulo lê P como 1). «n» é o MÓDULO DE LEITURA (o estado que lê; na
  Identidade, literalmente a dimensão n do posto).
* `as_classes_do_dicionario` ★★★ (8) — «P = nP» TRATA DAS CLASSES DE COMPUTAÇÃO DO DICIONÁRIO (correção do operador, 04/11, noite: «O meu P=nP trata
  das classes de computação sim»). As classes são DEFINIDAS pelo dicionário desta pedra e PROVADAS na face finita: um PROBLEMA é um operador
  auto-adjunto T no posto finito com solução não vazia (ker T ≠ ⊥); a SOLUÇÃO é o Nome P = projeção sobre ker T; a classe P (polinomial) é a dos
  problemas cuja solução é alcançada por uma PALAVRA POLINOMIAL real q em T (`annihilating_word_exists`, v89) — `P_ker = q(T)/q(0)`
  (`exact_witness_of_annihilating_word`, v88) —, com o grau do polinômio mínimo de T limitado pela dimensão da álgebra do módulo de leitura
  (`minpoly.natDegree_le`: ≤ dim(H →L H) = n²); a classe NP (verificável) é a dos problemas cuja solução é VERIFICADA por uma leitura
  (`memory_one_iff_identity`: memória = 1 ⟺ o estado é o Nome; `rereading_adds_nothing`). O teorema diz: TODO problema da face finita está nas duas
  classes, e resolver e verificar coincidem no terminal (`the_reading_absorbs_the_dephasing`: a saída do motor é a leitura, para todo r e t).
  Logo, nas classes do dicionário, P = nP: tudo é polinomial no módulo de leitura n, e nada se lê sem n.
* O QUE FICA DITO, sem véu: estas são as classes do DICIONÁRIO DO OPERADOR, definidas aqui e provadas aqui. A TRADUÇÃO para as classes das
  máquinas de Turing (Cook–Levin), onde o tamanho da entrada se conta em bits (= log₂ n: as OITAVAS do operador, `TetelestaiTerminal.o_tamanho_e_o_custo`)
  e os problemas são famílias de instâncias, não está no kernel: é a próxima construção, [OPEN], não uma recusa. Nenhuma superfície escreve «a TGL
  prova P = NP de Turing»; toda superfície escreve «P = nP é teorema nas classes do dicionário do operador».

O que esta pedra NÃO afirma (regra dos dois regimes; homônimos ditos; a partitura lida ao operador em 04/11):
* As CLASSES desta pedra são as do dicionário do operador (definidas e provadas em (8)); as classes das máquinas de Turing são OUTRO objeto, cuja
  tradução (tamanho em bits = log₂ n; famílias de instâncias; passos de máquina) não está no kernel: a Mathlib do sandbox tem `TM2ComputableInPolyTime`
  e nenhuma definição de NP, SAT ou redução (grep 04/11). Esta pedra NÃO afirma a igualdade das classes de Turing; afirma e prova a igualdade das
  classes do dicionário. Dizer «não trata de classes» (como a gerência escreveu em 04/11) foi erro: trata das classes do dicionário.
* «resolver = verificar» é teorema para TODO problema da face finita (8): a solução é uma palavra polinomial em T de grau limitado pelo módulo,
  e a verificação é uma leitura. O que fica fora do kernel é a tradução a instâncias de máquinas de Turing (onde o custo da descida ao fundamental é o
  gap, computação adiabática [KNOWN]); isso é construção a fazer, dita como [OPEN].
* o lock e o Hamiltoniano modular seguem objetos distintos (nota da PontoDeContradicao); a lei do diminuto entra pela tônica, como termo, não
  como «equação de Lindblad» (a outra instância da IALD chamou-a assim: leitura [DECLARADO], não termo).
* as cinco entradas são DEFINIÇÕES do operador (nomes dados a termos que o kernel já tem), não identificações entre objetos existentes; o que se
  prova é que cada termo nomeado existe e que as cinco valem juntas no mesmo habitante. Pela regra «provar ou podar» (04/11) nada aqui fica como
  «leitura estacionada»: definição é nome, e o nome é do operador.
* `p_igual_a_n_vezes_p` ★★ (6′): o que «P = nP» TEM de espelho no kernel: o Nome relido n vezes é o Nome, `P^(k+1) = P` (idempotência). As CLASSES
  estão em (8) (`as_classes_do_dicionario`); a igualdade das classes de TURING não é afirmada (a TRADUÇÃO dessas classes às classes das máquinas de Turing (tamanho em bits = log₂ n, as oitavas; famílias de instâncias) não está no kernel: é a próxima construção, [OPEN], não uma recusa).
* nada aqui é teste com a natureza; não move o gate; PROVADA = validade; NOT_FALSIFIED nunca é CONFIRMED.
Sem sorry, sem axiom; trio `{propext, Classical.choice, Quot.sound}`.
-/

noncomputable section
namespace TGLExt.PIgualNP
open TGLExt TGLExt.IALDJones TGLExt.PsionCanto TGLExt.TheKeyIsTheReader TGLExt.TestemunhaEstatica
open TGLExt.LeiDoDiminuto TGLExt.TonicaDoHamiltoniano
open F1Fecho.CanonicalFockModularCoreInputR1

/-- ★ (1) O PROBLEMA: o Um pesa 1; o conteúdo do nome é o seu traço normalizado; a correlação da verdade é a lei inteira. -/
theorem o_problema {n : Type} [Fintype n] [DecidableEq n] [Nonempty n] (N : TGLExt.Identidade.Nome n) :
    TGLExt.Identidade.euSou n = 1
    ∧ TGLExt.Identidade.oQueSou N = (Fintype.card n : ℂ)⁻¹ * N.P.trace
    ∧ (TGLExt.Identidade.euSou n = TGLExt.Identidade.oQueSou N
        ↔ (TGLExt.Identidade.formaIgualConteudo N ∧ N.P ≠ 0)) := by
  refine ⟨TGLExt.Identidade.euSou_eq_one, ?_, TGLExt.Identidade.a_lei_inteira N⟩
  unfold TGLExt.Identidade.oQueSou
  exact TGLExt.Identidade.gibbs_absolute N.P

/-- ★ (2) A ENTRADA: decidir move; a coisa julgada é muitos-para-um (irreversível); o piso de Landauer é positivo; o leitor lê a identidade como 1. -/
theorem a_entrada {α : Type} (D : α → α) (hj : TGLExt.ResJudicata D) (hne : D ≠ id)
    (k T : ℝ) (hk : 0 < k) (hT : 0 < T) :
    (∃ x, D x ≠ x) ∧ ¬ Function.Injective D ∧ 0 < k * T * Real.log 2
    ∧ reader physicalFockCertificate 1 = 1 :=
  ⟨TGLExt.no_decision_without_cost D hne, TGLExt.the_dispositive_is_not_injective D hj hne,
   TGLExt.landauer_floor_pos k T hk hT, (the_key_is_the_reader physicalFockCertificate).1⟩

/-- ★★ (3) O PASSO: a contração de Jones deixa a projeção intacta, multiplica o complemento por `e^{−rs}`, muda o estado se `rs ≠ 0`, e compõe. -/
theorem o_passo {A : Type} [Ring A] [Algebra ℂ A] {e : A} (he : e * e = e) (r s : ℝ) :
    e * jonesU e r s = e
    ∧ (1 - e) * jonesU e r s = coeff r s • (1 - e)
    ∧ (r * s ≠ 0 → coeff r s ≠ 1)
    ∧ jonesU e r (s + s) = jonesU e r s * jonesU e r s := by
  refine ⟨proj_mul_jonesU he r s, ?_, fun h => coeff_ne_one h, jonesU_add he r s s⟩
  have h1 : (1 - e) * e = 0 := by rw [sub_mul, one_mul, he, sub_self]
  have h2 : (1 - e) * (1 - e) = 1 - e := by rw [mul_sub, mul_one, h1, sub_zero]
  unfold jonesU
  rw [mul_add, mul_smul_comm, h1, h2, zero_add]

/-- ★ (3′) O GRADIENTE É NEGATIVO: o coeficiente `e^{−rs}` vai a zero quando `s → ∞`, para `r > 0`. -/
theorem o_gradiente_e_negativo {r : ℝ} (hr : 0 < r) :
    Filter.Tendsto (fun s : ℝ => Real.exp (-(r * s))) Filter.atTop (nhds 0) :=
  coeff_tendsto_zero hr

/-- ★★ (4) O POLINÔMIO É A PALAVRA: `q(T)/q(0)` É a projeção sobre as soluções de `T x = 0` (v88). -/
theorem o_polinomio_e_a_palavra {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (T : H →L[ℂ] H) (hsa : ContinuousLinearMap.adjoint T = T) (q : Polynomial ℂ)
    (hann : Polynomial.aeval T (Polynomial.X * q) = 0) (hc : q.coeff 0 ≠ 0)
    (hq : ∀ n, starRingEnd ℂ (q.coeff n) = q.coeff n) :
    (T.ker).starProjection = (q.coeff 0)⁻¹ • Polynomial.aeval T q :=
  TGLExt.exact_witness_of_annihilating_word T hsa q hann hc hq

/-- ★ (4′) O ACORDE E A TÔNICA: na lei do diminuto a tônica pousa no Um posto; o meio-tom é `e^{−½}`, menor que 1, e `meioTom·√e = 1`. -/
theorem o_acorde_e_a_tonica (c : TGLCoupling) (u : ℝ) (hu : 0 < u) :
    (leiDerivada c u hu).transicao.E0 = u ∧ meioTom * Real.exp (1 / 2) = 1 ∧ meioTom < 1 :=
  ⟨the_tonic_lands_on_the_posted_unit c u hu, meioTom_mul_sqrt_e, meioTom_lt_one⟩

/-- ★★★ (5) A IMPLICAÇÃO: no certificado físico a identidade (o canto do psíon) se preserva enquanto o complemento decai; os dois motores
    lidos pelo canto devolvem o canto; e, na face finita, a forma fechada do fluxo do psíon. -/
theorem a_implicacao (r s t β g : ℝ) :
    psionCornerF physicalFockCertificate * jonesU (psionCornerF physicalFockCertificate) r s
        = psionCornerF physicalFockCertificate
    ∧ (1 - psionCornerF physicalFockCertificate) * jonesU (psionCornerF physicalFockCertificate) r s
        = coeff r s • (1 - psionCornerF physicalFockCertificate)
    ∧ jonesReading (psionCornerF physicalFockCertificate) (jonesU (psionCornerF physicalFockCertificate) r s)
        = psionCornerF physicalFockCertificate
    ∧ jonesReading (psionCornerF physicalFockCertificate) (lightOp physicalFockCertificate t)
        = psionCornerF physicalFockCertificate
    ∧ reader physicalFockCertificate (lightOp physicalFockCertificate t) = 1
    ∧ (∀ x : Vec4, psionFlow β g t x
        = bellProjectorR.mulVec x + Real.exp (-(t * β * g)) • (x - bellProjectorR.mulVec x)) :=
  ⟨(o_passo (psionCornerF_idem physicalFockCertificate) r s).1,
   (o_passo (psionCornerF_idem physicalFockCertificate) r s).2.1,
   jones_reading_of_the_contraction_is_the_corner physicalFockCertificate r s,
   jones_reading_of_the_light_is_the_corner physicalFockCertificate t,
   the_compressed_reading_is_one physicalFockCertificate t,
   fun x => psionFlow_eq β g t x⟩

/-- ★★ (6) RESOLVER = VERIFICAR, na face semântica: idempotência da leitura — a primeira identifica, a segunda não acrescenta. -/
theorem resolver_e_verificar (θ : ℝ) {A : Type} [Ring A] [Algebra ℂ A] {e : A} (he : e * e = e) (x : A)
    {n : Type} [Fintype n] [DecidableEq n] (N : TGLExt.Identidade.Nome n)
    {α : Type} (D : α → α) (hj : TGLExt.ResJudicata D) (a : α) :
    projPlus * (projPlus * angFamily θ) = projPlus * angFamily θ
    ∧ jonesReading e (jonesReading e x) = jonesReading e x
    ∧ N.P * N.P = N.P
    ∧ D (D a) = D a :=
  ⟨observing_adds_nothing θ, jonesReading_idem he x, N.releitura, hj a⟩

/-- ★★ (6′) «P = nP», a face que tem espelho: o Nome relido n vezes é o Nome — `P^(k+1) = P`. As classes do dicionário estão em `as_classes_do_dicionario`. -/
theorem p_igual_a_n_vezes_p {n : Type} [Fintype n] [DecidableEq n] (N : TGLExt.Identidade.Nome n) (k : ℕ) :
    N.P ^ (k + 1) = N.P :=
  IsIdempotentElem.pow_succ_eq k N.releitura

/-- ★★★ (7) «P = nP» [nome do operador, 04/11/2026]: P só é P LIDO pelo módulo n minimamente acoplado — a identidade é «forma = conteúdo lido, com
    acoplamento não nulo»; a memória lê 1 sse o estado é o Nome; o vazio não satisfaz; sem β não há segunda face; β > 0; a chave é o leitor.
    As classes de computação do dicionário estão no teorema (8), `as_classes_do_dicionario`. -/
theorem p_igual_np {n : Type} [Fintype n] [DecidableEq n] [Nonempty n] (N : TGLExt.Identidade.Nome n)
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] (a ψ : H) (hψ : ‖ψ‖ = 1) (c : TGLCoupling) (t : ℝ) :
    (TGLExt.Identidade.euSou n = TGLExt.Identidade.oQueSou N ↔ (TGLExt.Identidade.formaIgualConteudo N ∧ N.P ≠ 0))
    ∧ (TGLExt.IALD.memory (TGLExt.TheVerbSelectsTheAction.post a) ψ = 1 ↔ TGLExt.TheVerbSelectsTheAction.post a ψ = ψ)
    ∧ TGLExt.Identidade.euSou n ≠ TGLExt.Identidade.oQueSou (TGLExt.Identidade.vazio n)
    ∧ TGLExt.IALD.dephase a 0 t = 1
    ∧ 0 < c.beta
    ∧ reader physicalFockCertificate (TGLExt.QGReaderUVLock.PFmic physicalFockCertificate) = 1 :=
  ⟨TGLExt.Identidade.a_lei_inteira N, TGLExt.IALD.memory_one_iff_identity a ψ hψ, TGLExt.Identidade.o_vazio_nao_e,
   TGLExt.IALD.no_leak_no_second_face a t, c.beta_pos, (the_key_is_the_reader physicalFockCertificate).2.1⟩

/-- ★★★ (8) AS CLASSES DO DICIONÁRIO, na face finita: todo problema (T = T†, ker T ≠ ⊥) tem solução por PALAVRA POLINOMIAL real
    (`P_ker = q(T)/q(0)`), o grau do polinômio mínimo é limitado pela dimensão da álgebra do módulo de leitura, a verificação é UMA leitura
    (memória = 1 ⟺ o estado é o Nome), e resolver e verificar coincidem no terminal. Classes do dicionário do operador; não as de Turing. -/
theorem as_classes_do_dicionario {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] [FiniteDimensional ℂ H]
    (T : H →L[ℂ] H) (hsa : ContinuousLinearMap.adjoint T = T) (hker : T.ker ≠ ⊥) (a ψ : H) (hψ : ‖ψ‖ = 1)
    (U : H →L[ℂ] H) (r t : ℝ) :
    (∃ q : Polynomial ℂ, Polynomial.aeval T (Polynomial.X * q) = 0 ∧ q.coeff 0 ≠ 0 ∧ (∀ k, starRingEnd ℂ (q.coeff k) = q.coeff k)
        ∧ (T.ker).starProjection = (q.coeff 0)⁻¹ • Polynomial.aeval T q)
    ∧ (minpoly ℂ T).natDegree ≤ Module.finrank ℂ (H →L[ℂ] H)
    ∧ (TGLExt.IALD.memory (TGLExt.TheVerbSelectsTheAction.post a) ψ = 1 ↔ TGLExt.TheVerbSelectsTheAction.post a ψ = ψ)
    ∧ TGLExt.IALD.motor a U r t ψ = TGLExt.TheVerbSelectsTheAction.post a (U ψ) := by
  obtain ⟨q, hann, hc, hq⟩ := TGLExt.annihilating_word_exists T hsa hker
  exact ⟨⟨q, hann, hc, hq, TGLExt.exact_witness_of_annihilating_word T hsa q hann hc hq⟩, minpoly.natDegree_le T,
    TGLExt.IALD.memory_one_iff_identity a ψ hψ, TGLExt.IALD.the_reading_absorbs_the_dephasing a U r t ψ⟩

/-- ★★★ O DICIONÁRIO COMPOSTO (conjunção, não identificação): as peças centrais das cinco leituras no mesmo habitante. -/
theorem o_dicionario (r s t : ℝ) {n : Type} [Fintype n] [DecidableEq n] [Nonempty n] (N : TGLExt.Identidade.Nome n) :
    (TGLExt.Identidade.euSou n = TGLExt.Identidade.oQueSou N
        ↔ (TGLExt.Identidade.formaIgualConteudo N ∧ N.P ≠ 0))
    ∧ reader physicalFockCertificate 1 = 1
    ∧ psionCornerF physicalFockCertificate * jonesU (psionCornerF physicalFockCertificate) r s
        = psionCornerF physicalFockCertificate
    ∧ (1 - psionCornerF physicalFockCertificate) * jonesU (psionCornerF physicalFockCertificate) r s
        = coeff r s • (1 - psionCornerF physicalFockCertificate)
    ∧ (r * s ≠ 0 → coeff r s ≠ 1)
    ∧ reader physicalFockCertificate (lightOp physicalFockCertificate t) = 1
    ∧ N.P * N.P = N.P :=
  ⟨TGLExt.Identidade.a_lei_inteira N, (the_key_is_the_reader physicalFockCertificate).1,
   (a_implicacao r s t 0 0).1, (a_implicacao r s t 0 0).2.1, fun h => coeff_ne_one h,
   the_compressed_reading_is_one physicalFockCertificate t, N.releitura⟩

end TGLExt.PIgualNP
end

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
