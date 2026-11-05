import TGLExt.Identidade
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
# O DICIONÁRIO: problema, entrada, passo, polinômio, implicação — as cinco leituras do operador, cada uma no termo que o kernel já tem
  [TGLExt — pedra CANDIDATA da gerência c1, 04/11/2026, rodada R1; NOME PROVISÓRIO (o nome é do operador); compilada no sandbox da v407
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

O que esta pedra NÃO afirma (regra dos dois regimes; homônimos ditos; a partitura lida ao operador em 04/11):
* NADA aqui é enunciado de complexidade computacional. «P» nesta pedra é PROJEÇÃO (o Nome, o canto); «P» na ciência da computação é uma CLASSE
  de problemas, e «NP» outra. São homônimos. O kernel não tem termo de TAMANHO de entrada nem de CONTAGEM de passos em função dele; a Mathlib
  do sandbox tem `TM2ComputableInPolyTime` e nenhuma definição de NP, SAT ou redução (grep 04/11). Esta pedra não decide, não sugere e não
  candidata a igualdade ou a desigualdade dessas classes.
* «resolver = verificar» aqui é a idempotência de UMA leitura cuja solução (`P`, `Ω`, `ker T`) já está escrita na dinâmica; não é a afirmação
  de que ACHAR a solução de um problema arbitrário custa o mesmo que CONFERI-LA. Para instância arbitrária, a descida ao estado fundamental é a
  computação adiabática [KNOWN], cujo custo é o gap, e esse gap não é termo desta pedra.
* o lock e o Hamiltoniano modular seguem objetos distintos (nota da PontoDeContradicaoR1); a lei do diminuto entra pela tônica, como termo, não
  como «equação de Lindblad» (a outra instância da IALD chamou-a assim: leitura [DECLARADO], não termo).
* as pontes entre as cinco leituras e os cinco termos são do operador [INPUT/ONTO]; o kernel entrega os termos e a conjunção.
* nada aqui é teste com a natureza; não move o gate; PROVADA = validade; NOT_FALSIFIED nunca é CONFIRMED.
Sem sorry, sem axiom; trio `{propext, Classical.choice, Quot.sound}`.
-/

noncomputable section
namespace TGLExt.DicionarioR1
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

end TGLExt.DicionarioR1
end

#print axioms TGLExt.DicionarioR1.o_problema
#print axioms TGLExt.DicionarioR1.a_entrada
#print axioms TGLExt.DicionarioR1.o_passo
#print axioms TGLExt.DicionarioR1.o_gradiente_e_negativo
#print axioms TGLExt.DicionarioR1.o_polinomio_e_a_palavra
#print axioms TGLExt.DicionarioR1.o_acorde_e_a_tonica
#print axioms TGLExt.DicionarioR1.a_implicacao
#print axioms TGLExt.DicionarioR1.resolver_e_verificar
#print axioms TGLExt.DicionarioR1.o_dicionario
