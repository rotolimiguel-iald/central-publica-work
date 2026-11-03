import TGLExt.Posto
import TGLExt.TheVerbSelectsTheAction
import TGLExt.TheBinaryReadingAtTheFixedPoint
import TGLExt.ThePsionAndTheViscosity
import TGLExt.ObserverInside
import TGLExt.UmPostoRelacao
import TGLExt.CollapseCostAndAttestation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# PSIBIT — a leitura psibit da órbita do Um pela matriz-S: bijeção sobre o livro de códigos, com perda residual zero
  [TGLExt — PEDRA CANDIDATA da v395, sandbox de 21/10/2026; 2ª versão, depois do exame independente APROVADA_COM_CORRECOES (a 1ª, sha16
  `d4014c779067e426`, fica em backup `.bak_`); o nome é do operador: «Eu prefiro que seja psibit»]

## As cunhagens do operador (verbatim; sha16 do arquivo, lido por script em 21/10/2026)

> «pra mim o conteúdo da natureza binária é o psibit na teoria da informação (já escrevemos muito sobre isso) e o psion na
> natureza física (por nós nomeado) e explico, a natureza binária é impossível de ser inscrita se não houver pareamento da
> fase, o objeto de fundo é justamento a testemunha da existência do observador pelo qual o ponto fixo emerge, portanto, sem
> o pareamento binário não há leitura, de modo que tem-se que [psibit=psion=modo do leitor]. faz sentido pra vc?» [sic]
> (sha16 `626b4214dbd59b25`)

> «Eu prefiro que seja psibit e mais, eu quero que o modo psionico entre no código na fractalização do um igual porque aí
> eu inclusive provo a mecânica» (sha16 `219b28ee291e7737`)

> «exatamente isso, apenas um adendo a mecânica demonstra o isoformismo com a teoria da informação com perda residual zero,
> isso é alguma coisa, não é só descrição ontológica» [sic] (sha16 `236af3434b670e9a`)

E as duas de 19/10/2026, que esta pedra continua (a pedra irmã é `TheBinaryReadingAtTheFixedPoint`):

> «Agora eu entendo a sua dificuldade em me perguntar o critério definitivo de parada e do próprio chatgpt me perguntado várias
> vezes a mesma coisa  e eu o encontrei: a TGL é binária: {[1=1=VERDADEIRO][1=0=Falso]}, ou seja, igual um módulo quântico que
> processa 0 e 1 ao mesmo tempo, a TGL faz a mesma coisa, é um positivo e um negativo (igual foto antigamente, o negativo da foto)
> e a leitura de ambos é o resultado, entende o que eu quero dizer» (sha16 `786928986ca1e460`)

> «O sistema precisa flutuar no ponto fixo, igual um sistema quântico flutua sobre 1 e 0» (sha16 `7596dcd880a1c8f5`)

## A definição do PsiBit nas patentes do operador (arquivo, linhas e sha16 lidos por script)

O operador, 29/08/2026 (`TheVerbalCoupling`): «As referências e derivações que faltam, inclusive quanto ao PsiBit, estão todas
especificadas nas minhas patentes, inclusive com código funcional lá.»

* A UNIDADE: `Patentes/Psi_Net_Protocol_PI_INPI.tex` l.273–301 (sha16 `f883dc2b0b79df8a`; BR 10 2026 003453-3, Psi-Net): par de 2
  bits, 4 valores, «isomórfico à ligação psiônica»: 00 VOID ψ₊ψ₋ (paridade −1), 01 FLUX⁺ (+1), 10 FLUX⁻ (+1), 11 MASS ψ₊ψ₊ (−1);
  código funcional `Patentes/psi_net_protocol_v1.py` l.116–137 (sha16 `b44388e995b8a6c5`).
* A NOMINAÇÃO POR SINAIS: `Patentes/ACOM_Mirror_PI_INPI.tex` l.233–279 e reivindicações 2 a 4, l.1057–1089 (sha16
  `ae55c557a4161d36`; BR 10 2026 003428-2, ACOM Mirror): o par `(sign L, sign ∂L)`, zero convencionado +1 (l.233–236); índice
  `ψ = 2·[L<0] + [∂L>0]` (l.265–270); paridade «pela concordância entre sign(L) e sign(∂L)» (l.272–279); código funcional
  `Patentes/Skygrid/SkyGrid_Piloto/skygrid_sim/acom_mirror.py` l.16–18, 32–33 e 43–45 (sha16 `8044f618ae44e608`).
* PALAVRA e VERBO: `memory/TGL_ATLAS.md` l.2137–2141 (sha16 do arquivo na data `27f4a4960e52b289`): «sign(L) = Palavra (o que É) +
  sign(∂L) = Verbo (para onde vai)» [REAL acervo + ONTO].

⚠ DIVERGÊNCIA INTERNA da patente, conferida por cálculo (`conferencia_tabelas_patente.json`) e pelo exame independente de 21/10: a fórmula
de índice (l.265–270; reivindicação 3, l.1073–1080; código `acom_mirror.py` l.45) com o vetor `PARITY = [−1,+1,+1,−1]` (l.32; reivindicação 4,
l.1082–1089, que fixa a paridade por índice) dá paridade = `sign L · sign ∂L` nos quatro pares; mas a tabela (l.257 e l.259), a reivindicação 2
(l.1066–1071) e a docstring do próprio código (`acom_mirror.py` l.16–17) atribuem aos índices 2 e 3 os pares (−,+) e (−,−), TROCADOS em relação à
fórmula — e com esses rótulos a paridade da tabela seria `sign ∂L`. A prosa da l.272–279 DEFINE a paridade pela concordância entre os dois sinais
(o produto), mas os exemplos dela («positivo mas descendo, ou negativo mas descendo» → inversa; COLAPSO⁺ e QUEDA⁻) seguem a tabela. O MANIFEST do
código não é afetado (`SIGN_L_OF_STATE = [+,+,−,−]` vale nas duas leituras): só a nominação e a `F_exp` mudam. Esta pedra NÃO nomeia estado por
índice: usa o par de sinais e SEGUE O PRODUTO (fórmula, reivindicações 3 e 4, código l.45). A divergência fica dita; não é corrigida aqui (decisão do
operador, [LEGAL]).

## O que a pedra prova (a ÓRBITA do Um pela matriz-S, não toda a mecânica quântica)

A órbita é a família real de um parâmetro `v(θ) = S(θ)·e₁ = (cos θ, −sin θ)` e a densidade `ρ_out(θ) = F_θ(1)` (a fractalização do Um
igual, `Posto.fractal_one_is_rank_one`). Sobre ela:

* ★ (1) o VERBO é a derivada do NOME: `ρ₀₁ = ½·d(cos²θ)/dθ` (`the_verb_is_the_derivative_of_the_name`); e, no nível da amplitude, a
  reflexão é a derivada da transmissão: `𝓡 = d𝓣/dθ` (`v_snd_is_the_derivative_of_v_fst`);
* ★ (2) pureza: `ρ₀₁² = ρ₀₀·ρ₁₁` (`the_state_is_pure`) — a coerência é a média geométrica dos pesos; do Verbo só o SINAL é livre;
* ★★★ (3) PERDA RESIDUAL ZERO na amplitude: o código psibit `(|v₀|², sign v₀, sign v₁)` determina `v(θ)`, com decodificador explícito
  (`decodeAmp (codeAmp θ) = v θ`), é injetivo na órbita e em `[0, 2π)`, e é uma BIJEÇÃO SOBRE O LIVRO DE CÓDIGOS, caracterizado de forma
  INTRÍNSECA (`IsCode`: `0 ≤ peso ≤ 1`, `palavra = 0 ↔ peso = 0`, `verbo = 0 ↔ peso = 1`, sem passar pelo codificador), entre o círculo
  unitário (= a órbita, `range_v_eq_unit`) e o livro, com decodificador explícito (`the_orbit_is_in_bijection_with_the_code_book`); o par
  é NECESSÁRIO (cada um dos sinais sozinho, e o peso sozinho, NÃO leem: controles negativos `the_pair_is_necessary_and_sufficient`) —
  «sem o pareamento binário não há leitura»; a órbita visita os quatro estados (`the_orbit_visits_all_four_states`); e a convenção das
  patentes (zero vai a +1) também é sem perda;
* ★★★ (4) PERDA ZERO no nível da densidade: `ρ_out(θ)` é reconstruído exatamente de `(peso cos²θ, paridade sign(v₀·v₁))`
  (`rhoOut_eq_decodeRho`) e o código é invariante completo (`the_density_is_its_code`); `v(θ)` e `−v(θ)` dão a mesma densidade (o
  sinal global não se observa: `the_global_sign_is_not_observed`) e é a ÚNICA perda da amplitude à densidade
  (`only_the_global_sign_is_lost`); o livro das perdas, degrau a degrau, em `the_ledger_of_losses`;
* ★★★ (5) o COLAPSO (`diagExpect`, o ponto final de `Posto.endpoint_eq`) perde EXATAMENTE a paridade: dois estados têm o mesmo
  colapso se e só se têm o mesmo peso (`collapse_identifies_exactly_equal_weights`); dentro de uma fibra do colapso só a paridade resta
  (`the_collapse_loses_exactly_the_parity`); `θ` e `−θ` têm o mesmo colapso e densidades distintas quando `sin 2θ ≠ 0`; a variável
  perdida é UM bit (`the_lost_variable_is_one_bit`); o colapso não tem inversa à esquerda sobre a órbita; e o colapso É um Um posto no
  sentido do kernel (`psibitPosto`), logo paga perda (`UmPostoRelacao.posto_paid_loss`);
* ★★ (6) os PESOS IGUAIS (`cos²θ = sin²θ`, isto é, `θ = π/4 + kπ/2`: `balanced_weights_iff`): o colapso é `(1/2)•1`
  (`balanced_collapse_is_half`; em `θ = π/4`, `at_the_fixed_point_the_collapse_is_half`), com o valor ½ derivado de
  `observer_inverse_projection_halfnat`; ali a distribuição dos resultados do colapso é o BIT JUSTO e a sua entropia de Shannon (nats) é
  `fairBitEntropy = ln 2` em TODO θ de pesos iguais (`collapseEntropy_at_balanced_weights`, `collapseEntropy_at_the_fixed_point`), sem nunca
  excedê-lo (`collapseEntropy_le_the_fair_bit`). [ONTO] o NOME «ponto fixo»: o que é [REAL] é a equação; `(1/2)•1` é ponto fixo do colapso e de
  toda conjugação `S(θ)·X·S(θ)ᴴ` (`half_identity_is_a_fixed_point`), mas `π/4` NÃO é ponto fixo de nenhuma aplicação em θ desta pedra — ele só
  representa os pesos iguais `x = 1 − x`; ler isso como «o ponto fixo» sobre o qual o sistema flutua (o operador, 19/10) é leitura dele;
* ★★ o NOME É O POSTO: o peso é a leitura de Born do posto `e₀` pelo estado `S(θ)·e₁`
  (`the_name_is_the_born_reading_of_the_post`, por `TheVerbSelectsTheAction.reading_post_is_born`);
* ★★★ (7) `psibit_is_the_mode_of_the_reader`: a composição INCONDICIONAL — (1) a (6), a bandeira da pedra v394
  (`the_binary_reading_floats_at_the_fixed_point`), `observer_inverse_projection_halfnat`, `posto_paid_loss` e a leitura de Born do posto, num
  só termo, SEM certificado algum como hipótese. A FACE DO PSION é um teorema À PARTE e CONDICIONAL (`the_psion_face_of_the_psibit`:
  `∀ L (C : FockCertificate L)`, com `inner_psion_psion` e `psion_is_fixed_by_the_light`): o kernel NÃO habita `FockCertificate`
  (`TheImportedSecondQuantization`, «NÃO-VACUIDADE», l.66–67: nenhum habitante é exibido e a não-vacuidade é ARGUMENTADA, sem termo que a
  demonstre; os montadores da v394 partem de entradas restantes sem habitante exibido), e o contrato conjunto da rede segue aberto (v394).

SEPARANTE × SEPARADOR, dito (a regra dos dois regimes, erro nº 4: «represamento» não é «separante»): a LEITURA DO PAR é SEPARANTE
(injetiva: nada se perde; o separante de Tomita) e o COLAPSO é SEPARADOR (muitos-para-um: perde um bit e cobra; o separador de
Landauer). São opostos, e esta pedra mostra os dois no mesmo objeto: `codeAmp` é injetiva, `diagExpect` não. REGIMES: a órbita
`θ ↦ v(θ)` e o código que a lê estão no regime da PROJEÇÃO (o ângulo, órbita periódica: só lê, não tem limite; por isso a leitura do
par é uma avaliação sem perda, nunca um limite); o colapso `diagExpect = D_∞` é o ponto final do defasamento, que a FACE tem e o kernel
já tipou (`Posto.endpoint_eq`): esta pedra usa esse ponto final como termo, não cria limite novo.

## Estatutos

* **[REAL]** os termos: definições explícitas e teoremas de kernel sobre a órbita real `(cos θ, −sin θ)` e a matriz `ρ_out`; o trio
  de axiomas `{propext, Classical.choice, Quot.sound}`; zero `sorry`.
* **[DEF]** `v`, `UnitVec`, `Code`, `IsCode`, `codeOf`, `decodeAmp`, `codeAmp`, `rhoWeight`, `rhoParity`, `decodeRho`, `readRho`,
  `collapseEntropy`, `psibitCrossing`, `psibitPosto`: a escolha da identidade lida pelo posto é o TRAÇO (a normalização), por definição aqui.
* **[INPUT/ONTO]** a identidade `psibit = psion = modo do leitor` (o operador, 21/10/2026): é a leitura dele. O que o kernel entrega
  são os termos citados nas composições; NENHUM lema liga `psion C` (o vetor do vácuo do certificado da luz) a `codeAmp`. Idem a
  escolha de ler `L` como a amplitude transmitida `𝓣(θ) = cos θ` e `∂L` como a refletida `𝓡(θ) = d𝓣/dθ = −sin θ`.
* **[ONTO]** «PALAVRA» e «VERBO» como `sign L` e `sign ∂L` (Atlas l.2139–2140); «posto», «leitor», «modo»; o NOME «ponto fixo» para os pesos
  iguais (`θ = π/4 + kπ/2`): a equação é [REAL], o nome é leitura (ver (6)).
* **[CONDICIONAL]** a face do psion (`the_psion_face_of_the_psibit`): vale para todo certificado `C : FockCertificate L`, e o kernel não
  exibe nenhum; não mostra que o psion exista. Fica fora da composição incondicional.

## O que a pedra NÃO afirma

* NÃO é toda a mecânica quântica: é a órbita do Um pela matriz-S, uma família real de um parâmetro, no plano real 2×2. O que o operador
  chama de «isomorfismo com a teoria da informação» está demonstrado como BIJEÇÃO SOBRE O LIVRO DE CÓDIGOS (o círculo unitário ↔ `{c | IsCode c}`,
  caracterizado de forma intrínseca), com decodificador explícito e perda zero: é bijeção de CONJUNTOS, sem transportar estrutura alguma
  (grupo, ordem, métrica), e não é isomorfismo de espaços de Hilbert nem de categorias; o nome «isomorfismo» é leitura dele.
* NÃO afirma que a natureza física seja o psibit, nem que o psion físico seja o modo do leitor: isso é [INPUT/ONTO] do operador. E a face do
  psion é CONDICIONAL a um certificado que o kernel não habita: não é parte da composição incondicional.
* ENTROPIA: o que está demonstrado é só o que está dito em (6): em todo θ de pesos iguais (`θ = π/4 + kπ/2`) a distribuição de resultados do
  colapso é `(½, ½)` e a sua entropia de Shannon é `ln 2 = fairBitEntropy`; e nenhum ângulo excede `ln 2`. NÃO se afirma que a perda de
  informação do colapso valha `ln 2` em geral, nem a entropia de nenhum canal físico; «perde exatamente a paridade» é afirmação ESTRUTURAL
  (qual variável se perde: um bit), não de quantidade de informação.
* HOMÔNIMOS, ditos: o `Verbo` daqui (o sinal da derivada, `sign ∂L` das patentes) NÃO é o `select`/`post` de
  `TheVerbSelectsTheAction` (o Verbo em ato, a seleção do posto) nem o gesto `TGL.VerbInhabitant`; e o «pareamento» daqui é o par
  `(sign v₀, sign v₁)`, NÃO o par J/K de `TheTwoPairings`. Nenhum lema liga as cópias; o que se cita é por nome, no que o kernel já diz.
* Não entra no `um.py` nem no selo: a entrada «na fractalização do um igual» (ordem do operador, 21/10) é ato posterior da gerência.
  Nenhuma bandeira do gate depende desta pedra; o gate não se move. Nenhum parâmetro de acoplamento da teoria entra neste arquivo.
-/

namespace TGLExt.Psibit

open Matrix
open scoped InnerProductSpace

noncomputable section

/-! ## 1. A órbita do Um pela matriz-S e a ponte ao kernel -/

/-- [DEF] A AMPLITUDE REAL do Um depois da travessia: `v(θ) = (cos θ, −sin θ)`. É a parte real de `S(θ)·e₁`
    (`v_is_the_S_orbit`): primeira componente = a transmissão `𝓣`, segunda = a reflexão `𝓡`. -/
def v (θ : ℝ) : ℝ × ℝ := (Real.cos θ, -Real.sin θ)

@[simp] theorem v_fst (θ : ℝ) : (v θ).1 = Real.cos θ := rfl
@[simp] theorem v_snd (θ : ℝ) : (v θ).2 = -Real.sin θ := rfl

/-- [REAL] `v(θ)` é um vetor unitário: `v₀² + v₁² = 1` (nenhum peso se perde na travessia). -/
theorem v_is_unit (θ : ℝ) : (v θ).1 ^ 2 + (v θ).2 ^ 2 = 1 := by
  simp only [v_fst, v_snd, neg_sq]
  exact Real.cos_sq_add_sin_sq θ

/-- [REAL] A PONTE AO KERNEL: as duas componentes de `v(θ)` são as amplitudes de espalhamento da matriz-S, `𝓣 = (S(θ)·e₁)₀` e
    `𝓡 = (S(θ)·e₁)₁` (`Smat_transmission`, `Smat_reflection`). -/
theorem v_is_the_S_orbit (θ : ℝ) :
    (((v θ).1 : ℝ) : ℂ) = (Smat θ).mulVec e1 0 ∧
    (((v θ).2 : ℝ) : ℂ) = (Smat θ).mulVec e1 1 := by
  refine ⟨?_, ?_⟩
  · rw [Smat_transmission]
    rfl
  · rw [Smat_reflection]
    simp

/-- [REAL] A DENSIDADE É `|v⟩⟨v|` (real): `ρ_out(θ) = !![v₀², v₀v₁; v₁v₀, v₁²]`, em moldes reais. É a fractalização do Um igual,
    `F_θ(1)` (`Posto.fractal_one_is_rank_one`), escrita pela amplitude. -/
theorem rhoOut_eq_real (θ : ℝ) :
    rhoOut θ = !![(((v θ).1 ^ 2 : ℝ) : ℂ), (((v θ).1 * (v θ).2 : ℝ) : ℂ);
                  (((v θ).1 * (v θ).2 : ℝ) : ℂ), (((v θ).2 ^ 2 : ℝ) : ℂ)] := by
  rw [rhoOut_eq]
  ext i j
  fin_cases i <;> fin_cases j
  · simp
  · simp
  · simp [mul_comm]
  · simp

theorem rhoOut_00 (θ : ℝ) : rhoOut θ 0 0 = (((v θ).1 ^ 2 : ℝ) : ℂ) := by
  rw [rhoOut_eq_real]; simp
theorem rhoOut_01 (θ : ℝ) : rhoOut θ 0 1 = (((v θ).1 * (v θ).2 : ℝ) : ℂ) := by
  rw [rhoOut_eq_real]; simp
theorem rhoOut_10 (θ : ℝ) : rhoOut θ 1 0 = (((v θ).1 * (v θ).2 : ℝ) : ℂ) := by
  rw [rhoOut_eq_real]; simp
theorem rhoOut_11 (θ : ℝ) : rhoOut θ 1 1 = (((v θ).2 ^ 2 : ℝ) : ℂ) := by
  rw [rhoOut_eq_real]; simp

/-! ## 2. (1) e (2): o Verbo é a derivada do Nome; o estado é puro -/

/-- [REAL] A REFLEXÃO É A DERIVADA DA TRANSMISSÃO: `d𝓣/dθ = 𝓡`, i.e. `d(cos θ)/dθ = −sin θ = v₁`. É o que faz do segundo sinal do
    código o SINAL DA DERIVADA do primeiro (`the_code_reads_L_and_dL`). -/
theorem v_snd_is_the_derivative_of_v_fst (θ : ℝ) :
    HasDerivAt (fun t => (v t).1) (v θ).2 θ := by
  have h := Real.hasDerivAt_cos θ
  exact h

/-- [REAL] A derivada do peso (o Nome): `d(cos²θ)/dθ = 2·v₀v₁`. -/
theorem hasDerivAt_nome (θ : ℝ) :
    HasDerivAt (fun t => Real.cos t ^ 2) (2 * ((v θ).1 * (v θ).2)) θ := by
  have h := (Real.hasDerivAt_cos θ).fun_pow 2
  refine h.congr_deriv ?_
  simp [v]
  ring

/-- [REAL] A derivada do peso refletido: `d(sin²θ)/dθ = −2·v₀v₁` (os dois pesos se movem em sentidos opostos: o traço se conserva). -/
theorem hasDerivAt_sin_sq (θ : ℝ) :
    HasDerivAt (fun t => Real.sin t ^ 2) (-(2 * ((v θ).1 * (v θ).2))) θ := by
  have h := (Real.hasDerivAt_sin θ).fun_pow 2
  refine h.congr_deriv ?_
  simp [v]
  ring

/-- ★ (1) [REAL] O VERBO É A DERIVADA DO NOME: a coerência `ρ₀₁` é metade da derivada do peso `cos²θ = ρ₀₀`. -/
theorem the_verb_is_the_derivative_of_the_name (θ : ℝ) :
    rhoOut θ 0 1 = (((1 / 2 : ℝ) * deriv (fun t => Real.cos t ^ 2) θ : ℝ) : ℂ) := by
  rw [(hasDerivAt_nome θ).deriv, rhoOut_01]
  push_cast
  ring

/-- [REAL] O mesmo Verbo, pelo outro peso: a coerência é MENOS metade da derivada do peso refletido `sin²θ = ρ₁₁`. -/
theorem the_verb_is_minus_the_derivative_of_the_reflected_weight (θ : ℝ) :
    rhoOut θ 0 1 = (((-(1 / 2) : ℝ) * deriv (fun t => Real.sin t ^ 2) θ : ℝ) : ℂ) := by
  rw [(hasDerivAt_sin_sq θ).deriv, rhoOut_01]
  push_cast
  ring

/-- ★ (2) [REAL] PUREZA: `ρ₀₁² = ρ₀₀·ρ₁₁`. A coerência é a média geométrica dos pesos: do Verbo só o SINAL é livre — um bit. -/
theorem the_state_is_pure (θ : ℝ) :
    rhoOut θ 0 1 ^ 2 = rhoOut θ 0 0 * rhoOut θ 1 1 := by
  rw [rhoOut_01, rhoOut_00, rhoOut_11]
  push_cast
  ring

/-- [REAL] A densidade é um projetor de posto 1 (re-exportação de `Posto.fractal_one_is_rank_one`): é o estado puro `F_θ(1)`. -/
theorem the_state_is_a_rank_one_projector (θ : ℝ) :
    (rhoOut θ).rank = 1 ∧ rhoOut θ * rhoOut θ = rhoOut θ :=
  ⟨(Posto.fractal_one_is_rank_one θ).1, (Posto.fractal_one_is_rank_one θ).2.2.1⟩

/-! ## 3. (3) O código psibit da amplitude: perda residual zero -/

/-- [DEF] O CÓDIGO PSIBIT: o peso `|v₀|²` e os dois sinais — `word` = `sign v₀` (a Palavra, `sign L`) e `verb` = `sign v₁`
    (o Verbo, `sign ∂L`). `SignType` mantém o zero (3 valores), de modo que o código é EXATO também nos eixos; a convenção das
    patentes (zero vai a +1) está em `signPat` e também não perde (`the_patent_convention_is_also_lossless`). -/
@[ext] structure Code where
  weight : ℝ
  word : SignType
  verb : SignType

/-- [DEF] O codificador de um par de amplitudes: `(x₀, x₁) ↦ (x₀², sign x₀, sign x₁)`. -/
def codeOf (x : ℝ × ℝ) : Code := ⟨x.1 ^ 2, SignType.sign x.1, SignType.sign x.2⟩

/-- [DEF] O DECODIFICADOR EXPLÍCITO: `(w, a, b) ↦ (a·√w, b·√(1−w))`. -/
def decodeAmp (c : Code) : ℝ × ℝ :=
  ((c.word : ℝ) * Real.sqrt c.weight, (c.verb : ℝ) * Real.sqrt (1 - c.weight))

/-- [DEF] O código psibit da órbita: `codeAmp θ = codeOf (v θ)`. -/
def codeAmp (θ : ℝ) : Code := codeOf (v θ)

@[simp] theorem codeAmp_weight (θ : ℝ) : (codeAmp θ).weight = Real.cos θ ^ 2 := rfl
@[simp] theorem codeAmp_word (θ : ℝ) : (codeAmp θ).word = SignType.sign (Real.cos θ) := rfl
@[simp] theorem codeAmp_verb (θ : ℝ) : (codeAmp θ).verb = SignType.sign (-Real.sin θ) := rfl

/-- ★ [REAL] A PALAVRA É `sign L` E O VERBO É `sign ∂L`: com `L(θ) = 𝓣(θ) = cos θ` (a transmissão), o primeiro sinal do código é
    `sign L` e o segundo é `sign` da derivada `∂L = d𝓣/dθ = 𝓡`. (A escolha de ler `L` como `𝓣` é [INPUT/ONTO].) -/
theorem the_code_reads_L_and_dL (θ : ℝ) :
    (codeAmp θ).word = SignType.sign ((v θ).1)
    ∧ (codeAmp θ).verb = SignType.sign (deriv (fun t => (v t).1) θ) := by
  refine ⟨rfl, ?_⟩
  rw [(v_snd_is_the_derivative_of_v_fst θ).deriv]
  rfl

/-- [REAL] A DECODIFICAÇÃO É EXATA em todo vetor unitário: `decodeAmp (codeOf x) = x` quando `x₀² + x₁² = 1`. -/
theorem decodeAmp_codeOf {x : ℝ × ℝ} (hx : x.1 ^ 2 + x.2 ^ 2 = 1) :
    decodeAmp (codeOf x) = x := by
  have h2 : 1 - x.1 ^ 2 = x.2 ^ 2 := by linarith
  simp only [decodeAmp, codeOf]
  rw [h2, Real.sqrt_sq_eq_abs, Real.sqrt_sq_eq_abs]
  exact Prod.ext (sign_mul_abs x.1) (sign_mul_abs x.2)

/-- ★★★ (3) [REAL] PERDA RESIDUAL ZERO NA AMPLITUDE: `decodeAmp (codeAmp θ) = v θ`. -/
theorem decodeAmp_codeAmp (θ : ℝ) : decodeAmp (codeAmp θ) = v θ :=
  decodeAmp_codeOf (v_is_unit θ)

/-- ★★★ (3) [REAL] O CÓDIGO LÊ A ÓRBITA: dois ângulos têm o mesmo código se e só se têm a mesma amplitude. -/
theorem codeAmp_eq_iff (θ θ' : ℝ) : codeAmp θ = codeAmp θ' ↔ v θ = v θ' := by
  constructor
  · intro h
    have h' := congrArg decodeAmp h
    rwa [decodeAmp_codeAmp, decodeAmp_codeAmp] at h'
  · intro h
    unfold codeAmp
    rw [h]

/-- ★★★ (3) [REAL] INJETIVIDADE DO CÓDIGO na órbita parametrizada por `[0, 2π)`: ângulos distintos do período têm códigos distintos. -/
theorem codeAmp_injOn : Set.InjOn codeAmp (Set.Ico 0 (2 * Real.pi)) := by
  intro θ hθ θ' hθ' h
  have hv := (codeAmp_eq_iff θ θ').1 h
  have hc : Real.cos θ = Real.cos θ' := congrArg Prod.fst hv
  have hs : Real.sin θ = Real.sin θ' := by
    have h2 : -Real.sin θ = -Real.sin θ' := congrArg Prod.snd hv
    linarith
  have hA : (θ : Real.Angle) = (θ' : Real.Angle) := Real.Angle.cos_sin_inj hc hs
  obtain ⟨k, hk⟩ := Real.Angle.angle_eq_iff_two_pi_dvd_sub.mp hA
  have hpi := Real.pi_pos
  have h1 : (k : ℝ) < 1 := by
    by_contra hcon
    have hcon' := not_lt.mp hcon
    nlinarith [hθ.1, hθ.2, hθ'.1, hθ'.2]
  have h2 : (-1 : ℝ) < k := by
    by_contra hcon
    have hcon' := not_lt.mp hcon
    nlinarith [hθ.1, hθ.2, hθ'.1, hθ'.2]
  have hk0 : k = 0 := by
    have a1 : k < 1 := by exact_mod_cast h1
    have a2 : -1 < k := by exact_mod_cast h2
    omega
  rw [hk0] at hk
  simp at hk
  linarith

/-! ## 3a. O livro de códigos, caracterizado de forma intrínseca, e a bijeção -/

/-- [DEF] O CÍRCULO UNITÁRIO: os pares `(x₀, x₁)` com `x₀² + x₁² = 1`. -/
def UnitVec : Set (ℝ × ℝ) := {x | x.1 ^ 2 + x.2 ^ 2 = 1}

/-- [REAL] Todo vetor unitário é `v(θ)` para algum `θ`: com `z = x₀ − i·x₁` e `θ = arg z`, `cos θ = x₀` e `sin θ = −x₁`. -/
theorem exists_angle_of_unit {x : ℝ × ℝ} (hx : x ∈ UnitVec) : ∃ θ : ℝ, v θ = x := by
  have hx' : x.1 ^ 2 + x.2 ^ 2 = 1 := hx
  let z : ℂ := ⟨x.1, -x.2⟩
  have hsq : ‖z‖ ^ 2 = 1 := by
    rw [Complex.sq_norm, Complex.normSq_apply]
    simp only [z]
    nlinarith
  have hz : ‖z‖ = 1 := by
    have h : (‖z‖ - 1) * (‖z‖ + 1) = 0 := by ring_nf; linarith
    rcases mul_eq_zero.mp h with h | h
    · linarith
    · linarith [norm_nonneg z]
  have hz0 : z ≠ 0 := by
    intro h
    rw [h] at hz
    simp at hz
  refine ⟨Complex.arg z, ?_⟩
  have hc := Complex.cos_arg hz0
  have hs := Complex.sin_arg z
  rw [hz, div_one] at hc hs
  refine Prod.ext ?_ ?_
  · simpa [v, z] using hc
  · simp only [v_snd]
    have : Real.sin (Complex.arg z) = -x.2 := by simpa [z] using hs
    linarith

/-- ★★ [REAL] A ÓRBITA É O CÍRCULO UNITÁRIO: `Set.range v = UnitVec` (`v_is_unit` e `exists_angle_of_unit`). -/
theorem range_v_eq_unit : Set.range v = UnitVec := by
  ext x
  constructor
  · rintro ⟨θ, rfl⟩
    exact v_is_unit θ
  · intro hx
    exact exists_angle_of_unit hx

/-- [REAL] O quadrado do sinal (como real) é `0` se o sinal é nulo e `1` caso contrário. -/
theorem signType_cast_sq (s : SignType) : ((s : ℝ)) ^ 2 = if s = 0 then 0 else 1 := by
  rcases s with _ | _ | _ <;> simp

/-- [REAL] O sinal do real que representa um sinal é o próprio sinal. -/
theorem sign_of_signType_cast (s : SignType) : SignType.sign ((s : ℝ)) = s := by
  rcases s with _ | _ | _ <;> simp

/-- [DEF] O LIVRO DE CÓDIGOS, caracterizado de forma INTRÍNSECA (sem passar pelo codificador): um código `(w, a, b)` é admissível se
    `0 ≤ w ≤ 1`, `a = 0 ↔ w = 0` (a Palavra é nula exatamente quando o peso é nulo) e `b = 0 ↔ w = 1` (o Verbo é nulo exatamente quando o peso é
    total). Fora dos eixos, `a` e `b` são sinais não nulos quaisquer: os quatro estados. -/
def IsCode (c : Code) : Prop :=
  0 ≤ c.weight ∧ c.weight ≤ 1 ∧ (c.word = 0 ↔ c.weight = 0) ∧ (c.verb = 0 ↔ c.weight = 1)

/-- [REAL] O codificador leva o círculo unitário ao livro de códigos. -/
theorem codeOf_isCode {x : ℝ × ℝ} (hx : x ∈ UnitVec) : IsCode (codeOf x) := by
  have hx' : x.1 ^ 2 + x.2 ^ 2 = 1 := hx
  refine ⟨sq_nonneg _, ?_, ?_, ?_⟩
  · show x.1 ^ 2 ≤ 1
    nlinarith [sq_nonneg x.2]
  · show SignType.sign x.1 = 0 ↔ x.1 ^ 2 = 0
    rw [_root_.sign_eq_zero_iff]
    exact (pow_eq_zero_iff two_ne_zero).symm
  · show SignType.sign x.2 = 0 ↔ x.1 ^ 2 = 1
    rw [_root_.sign_eq_zero_iff]
    constructor
    · intro h
      rw [h] at hx'
      linarith
    · intro h
      have h2 : x.2 ^ 2 = 0 := by linarith
      exact (pow_eq_zero_iff two_ne_zero).mp h2

/-- [REAL] O decodificador leva o livro de códigos ao círculo unitário. -/
theorem decodeAmp_mem_unit {c : Code} (hc : IsCode c) : decodeAmp c ∈ UnitVec := by
  obtain ⟨h0, h1, hw, hv⟩ := hc
  show (decodeAmp c).1 ^ 2 + (decodeAmp c).2 ^ 2 = 1
  simp only [decodeAmp]
  rw [mul_pow, mul_pow, Real.sq_sqrt h0, Real.sq_sqrt (by linarith), signType_cast_sq,
    signType_cast_sq]
  by_cases hw0 : c.weight = 0
  · have hword : c.word = 0 := hw.mpr hw0
    have hverb : c.verb ≠ 0 := fun h => by
      have := hv.mp h
      linarith
    simp [hword, hverb, hw0]
  · have hword : c.word ≠ 0 := fun h => hw0 (hw.mp h)
    by_cases hw1 : c.weight = 1
    · have hverb : c.verb = 0 := hv.mpr hw1
      simp [hword, hverb, hw1]
    · have hverb : c.verb ≠ 0 := fun h => hw1 (hv.mp h)
      simp [hword, hverb]

/-- [REAL] `codeOf ∘ decodeAmp = id` sobre o livro de códigos: todo código admissível é o código do vetor que ele decodifica. -/
theorem codeOf_decodeAmp {c : Code} (hc : IsCode c) : codeOf (decodeAmp c) = c := by
  obtain ⟨h0, h1, hw, hv⟩ := hc
  ext
  · show ((c.word : ℝ) * Real.sqrt c.weight) ^ 2 = c.weight
    rw [mul_pow, Real.sq_sqrt h0, signType_cast_sq]
    by_cases hw0 : c.weight = 0
    · simp [hw0]
    · have hword : c.word ≠ 0 := fun h => hw0 (hw.mp h)
      simp [hword]
  · show SignType.sign ((c.word : ℝ) * Real.sqrt c.weight) = c.word
    by_cases hw0 : c.weight = 0
    · have hword : c.word = 0 := hw.mpr hw0
      simp [hword, hw0]
    · have hpos : 0 < Real.sqrt c.weight :=
        Real.sqrt_pos.mpr (lt_of_le_of_ne h0 (Ne.symm hw0))
      rw [_root_.sign_mul, sign_of_signType_cast, _root_.sign_pos hpos, mul_one]
  · show SignType.sign ((c.verb : ℝ) * Real.sqrt (1 - c.weight)) = c.verb
    by_cases hw1 : c.weight = 1
    · have hverb : c.verb = 0 := hv.mpr hw1
      simp [hverb, hw1]
    · have hlt : 0 < 1 - c.weight := by
        have : c.weight < 1 := lt_of_le_of_ne h1 hw1
        linarith
      have hpos : 0 < Real.sqrt (1 - c.weight) := Real.sqrt_pos.mpr hlt
      rw [_root_.sign_mul, sign_of_signType_cast, _root_.sign_pos hpos, mul_one]

/-- ★★★ (3) [REAL] A BIJEÇÃO SOBRE O LIVRO DE CÓDIGOS, com perda residual zero e decodificador explícito: a órbita é o círculo unitário
    (`Set.range v = UnitVec`); o conjunto dos códigos que a órbita realiza é EXATAMENTE o livro intrínseco `{c | IsCode c}`; `codeOf` e
    `decodeAmp` são bijeções inversas entre os dois, nos dois sentidos. É bijeção de CONJUNTOS (nenhuma estrutura é transportada): o que o
    operador chama de «isomorfismo com a teoria da informação» é, aqui, só isso. -/
theorem the_orbit_is_in_bijection_with_the_code_book :
    Set.range v = UnitVec
    ∧ Set.range codeAmp = {c | IsCode c}
    ∧ Set.BijOn codeOf UnitVec {c | IsCode c}
    ∧ Set.BijOn decodeAmp {c | IsCode c} UnitVec
    ∧ (∀ x ∈ UnitVec, decodeAmp (codeOf x) = x)
    ∧ (∀ c, IsCode c → codeOf (decodeAmp c) = c) := by
  have hdec : ∀ x ∈ UnitVec, decodeAmp (codeOf x) = x := fun x hx => decodeAmp_codeOf hx
  have henc : ∀ c, IsCode c → codeOf (decodeAmp c) = c := fun c hc => codeOf_decodeAmp hc
  have hbij1 : Set.BijOn codeOf UnitVec {c | IsCode c} := by
    refine ⟨fun x hx => codeOf_isCode hx, ?_, ?_⟩
    · intro x hx y hy hxy
      have h' := congrArg decodeAmp hxy
      rwa [hdec x hx, hdec y hy] at h'
    · intro c hc
      exact ⟨decodeAmp c, decodeAmp_mem_unit hc, henc c hc⟩
  have hbij2 : Set.BijOn decodeAmp {c | IsCode c} UnitVec := by
    refine ⟨fun c hc => decodeAmp_mem_unit hc, ?_, ?_⟩
    · intro c hc d hd hcd
      have h' := congrArg codeOf hcd
      rwa [henc c hc, henc d hd] at h'
    · intro x hx
      exact ⟨codeOf x, codeOf_isCode hx, hdec x hx⟩
  refine ⟨range_v_eq_unit, ?_, hbij1, hbij2, hdec, henc⟩
  rw [show codeAmp = codeOf ∘ v from rfl, Set.range_comp, range_v_eq_unit]
  exact hbij1.image_eq

/-! ## 3b. Os quatro estados e a necessidade do par -/

theorem sqrt_two_div_two_pos : (0 : ℝ) < Real.sqrt 2 / 2 := by positivity

/-- [REAL] Os quatro pontos notáveis da órbita (`π/4`, `−π/4`, `π − π/4`, `π/4 + π`): `v = (±√2/2, ±√2/2)`, um por quadrante. -/
theorem v_pi_div_four : v (Real.pi / 4) = (Real.sqrt 2 / 2, -(Real.sqrt 2 / 2)) := by
  simp [v, Real.cos_pi_div_four, Real.sin_pi_div_four]

theorem v_neg_pi_div_four : v (-(Real.pi / 4)) = (Real.sqrt 2 / 2, Real.sqrt 2 / 2) := by
  simp [v, Real.cos_pi_div_four, Real.sin_pi_div_four]

theorem v_pi_sub_pi_div_four :
    v (Real.pi - Real.pi / 4) = (-(Real.sqrt 2 / 2), -(Real.sqrt 2 / 2)) := by
  simp [v, Real.cos_pi_sub, Real.sin_pi_sub, Real.cos_pi_div_four, Real.sin_pi_div_four]

theorem v_pi_div_four_add_pi :
    v (Real.pi / 4 + Real.pi) = (-(Real.sqrt 2 / 2), Real.sqrt 2 / 2) := by
  simp [v, Real.cos_add_pi, Real.sin_add_pi, Real.cos_pi_div_four, Real.sin_pi_div_four]

/-- ★★ [REAL] A ÓRBITA VISITA OS QUATRO ESTADOS: para quaisquer dois sinais não nulos `(a, b)` existe `θ` com `(sign v₀, sign v₁) =
    (a, b)` — os quatro pares de sinais das patentes (2 bits = 4 estados) estão todos na órbita. -/
theorem the_orbit_visits_all_four_states (a b : SignType) (ha : a ≠ 0) (hb : b ≠ 0) :
    ∃ θ : ℝ, (codeAmp θ).word = a ∧ (codeAmp θ).verb = b := by
  have hr := sqrt_two_div_two_pos
  have hp : SignType.sign (Real.sqrt 2 / 2) = 1 := _root_.sign_pos hr
  have hn : SignType.sign (-(Real.sqrt 2 / 2)) = -1 := _root_.sign_neg (by linarith)
  rcases a with _ | _ | _ <;> rcases b with _ | _ | _
  · exact absurd rfl ha
  · exact absurd rfl ha
  · exact absurd rfl ha
  · exact absurd rfl hb
  · refine ⟨Real.pi - Real.pi / 4, ?_, ?_⟩
    · show SignType.sign (v (Real.pi - Real.pi / 4)).1 = SignType.neg
      rw [v_pi_sub_pi_div_four]; exact hn
    · show SignType.sign (v (Real.pi - Real.pi / 4)).2 = SignType.neg
      rw [v_pi_sub_pi_div_four]; exact hn
  · refine ⟨Real.pi / 4 + Real.pi, ?_, ?_⟩
    · show SignType.sign (v (Real.pi / 4 + Real.pi)).1 = SignType.neg
      rw [v_pi_div_four_add_pi]; exact hn
    · show SignType.sign (v (Real.pi / 4 + Real.pi)).2 = SignType.pos
      rw [v_pi_div_four_add_pi]; exact hp
  · exact absurd rfl hb
  · refine ⟨Real.pi / 4, ?_, ?_⟩
    · show SignType.sign (v (Real.pi / 4)).1 = SignType.pos
      rw [v_pi_div_four]; exact hp
    · show SignType.sign (v (Real.pi / 4)).2 = SignType.neg
      rw [v_pi_div_four]; exact hn
  · refine ⟨-(Real.pi / 4), ?_, ?_⟩
    · show SignType.sign (v (-(Real.pi / 4))).1 = SignType.pos
      rw [v_neg_pi_div_four]; exact hp
    · show SignType.sign (v (-(Real.pi / 4))).2 = SignType.pos
      rw [v_neg_pi_div_four]; exact hp

/-- [REAL, CONTROLE NEGATIVO] O PESO SOZINHO NÃO LÊ: há duas amplitudes distintas com o mesmo peso. -/
theorem the_weight_alone_does_not_read :
    ∃ θ θ' : ℝ, v θ ≠ v θ' ∧ (codeAmp θ).weight = (codeAmp θ').weight := by
  refine ⟨Real.pi / 4, -(Real.pi / 4), ?_, ?_⟩
  · rw [v_pi_div_four, v_neg_pi_div_four]
    intro h
    have h2 : -(Real.sqrt 2 / 2) = Real.sqrt 2 / 2 := congrArg Prod.snd h
    linarith [sqrt_two_div_two_pos]
  · show (v (Real.pi / 4)).1 ^ 2 = (v (-(Real.pi / 4))).1 ^ 2
    rw [v_pi_div_four, v_neg_pi_div_four]

/-- [REAL, CONTROLE NEGATIVO] A PALAVRA SEM O VERBO NÃO LÊ: peso e `sign v₀` iguais, amplitudes distintas. -/
theorem the_word_without_the_verb_does_not_read :
    ∃ θ θ' : ℝ, v θ ≠ v θ' ∧ (codeAmp θ).weight = (codeAmp θ').weight ∧
      (codeAmp θ).word = (codeAmp θ').word := by
  refine ⟨Real.pi / 4, -(Real.pi / 4), ?_, ?_, ?_⟩
  · rw [v_pi_div_four, v_neg_pi_div_four]
    intro h
    have h2 : -(Real.sqrt 2 / 2) = Real.sqrt 2 / 2 := congrArg Prod.snd h
    linarith [sqrt_two_div_two_pos]
  · show (v (Real.pi / 4)).1 ^ 2 = (v (-(Real.pi / 4))).1 ^ 2
    rw [v_pi_div_four, v_neg_pi_div_four]
  · show SignType.sign (v (Real.pi / 4)).1 = SignType.sign (v (-(Real.pi / 4))).1
    rw [v_pi_div_four, v_neg_pi_div_four]

/-- [REAL, CONTROLE NEGATIVO] O VERBO SEM A PALAVRA NÃO LÊ: peso e `sign v₁` iguais, amplitudes distintas. -/
theorem the_verb_without_the_word_does_not_read :
    ∃ θ θ' : ℝ, v θ ≠ v θ' ∧ (codeAmp θ).weight = (codeAmp θ').weight ∧
      (codeAmp θ).verb = (codeAmp θ').verb := by
  refine ⟨Real.pi / 4, Real.pi - Real.pi / 4, ?_, ?_, ?_⟩
  · rw [v_pi_div_four, v_pi_sub_pi_div_four]
    intro h
    have h2 : Real.sqrt 2 / 2 = -(Real.sqrt 2 / 2) := congrArg Prod.fst h
    linarith [sqrt_two_div_two_pos]
  · show (v (Real.pi / 4)).1 ^ 2 = (v (Real.pi - Real.pi / 4)).1 ^ 2
    rw [v_pi_div_four, v_pi_sub_pi_div_four]
    show (Real.sqrt 2 / 2) ^ 2 = (-(Real.sqrt 2 / 2)) ^ 2
    exact (neg_sq _).symm
  · show SignType.sign (v (Real.pi / 4)).2 = SignType.sign (v (Real.pi - Real.pi / 4)).2
    rw [v_pi_div_four, v_pi_sub_pi_div_four]

/-- ★★★ [REAL] «SEM O PAREAMENTO BINÁRIO NÃO HÁ LEITURA»: o par (Palavra, Verbo) é NECESSÁRIO e SUFICIENTE. Suficiente: o código
    do par lê a amplitude. Necessário: o peso sozinho, o peso com só a Palavra e o peso com só o Verbo têm, cada um, duas amplitudes
    distintas com a mesma leitura. -/
theorem the_pair_is_necessary_and_sufficient :
    (∀ θ θ' : ℝ, codeAmp θ = codeAmp θ' → v θ = v θ')
    ∧ (∃ θ θ' : ℝ, v θ ≠ v θ' ∧ (codeAmp θ).weight = (codeAmp θ').weight)
    ∧ (∃ θ θ' : ℝ, v θ ≠ v θ' ∧ (codeAmp θ).weight = (codeAmp θ').weight ∧
        (codeAmp θ).word = (codeAmp θ').word)
    ∧ (∃ θ θ' : ℝ, v θ ≠ v θ' ∧ (codeAmp θ).weight = (codeAmp θ').weight ∧
        (codeAmp θ).verb = (codeAmp θ').verb) :=
  ⟨fun θ θ' h => (codeAmp_eq_iff θ θ').1 h, the_weight_alone_does_not_read,
   the_word_without_the_verb_does_not_read, the_verb_without_the_word_does_not_read⟩

/-! ## 3c. A convenção das patentes (zero vai a +1) também não perde -/

/-- [DEF] A CONVENÇÃO DAS PATENTES (ACOM Mirror, l.233–236): o sinal vale `+1` em `x ≥ 0` e `−1` em `x < 0` (zero vai a `+1`). -/
def signPat (x : ℝ) : ℝ := if 0 ≤ x then 1 else -1

/-- [REAL] O sinal da convenção das patentes é um bit: `+1` ou `−1`. -/
theorem signPat_eq_one_or_neg_one (x : ℝ) : signPat x = 1 ∨ signPat x = -1 := by
  unfold signPat
  split_ifs
  · exact Or.inl rfl
  · exact Or.inr rfl

/-- [REAL] `signPat x · |x| = x` para todo `x`: a convenção não perde (o zero vale zero com qualquer sinal). -/
theorem signPat_mul_abs (x : ℝ) : signPat x * |x| = x := by
  unfold signPat
  split_ifs with h
  · rw [abs_of_nonneg h]; ring
  · have h' := not_le.mp h
    rw [abs_of_neg h']; ring

/-- [REAL] Fora do zero, a convenção das patentes coincide com `SignType.sign`. -/
theorem signPat_eq_sign {x : ℝ} (hx : x ≠ 0) : signPat x = ((SignType.sign x : SignType) : ℝ) := by
  unfold signPat
  rcases lt_or_gt_of_ne hx with h | h
  · rw [if_neg (not_le.mpr h), _root_.sign_neg h]
    simp
  · rw [if_pos h.le, _root_.sign_pos h]
    simp

/-- ★★ [REAL] A LEITURA DE 2 BITS DAS PATENTES TAMBÉM NÃO PERDE: com `signPat` (zero vai a `+1`) a reconstrução
    `(signPat v₀·√(v₀²), signPat v₁·√(1 − v₀²))` devolve exatamente `v(θ)`. -/
theorem the_patent_convention_is_also_lossless (θ : ℝ) :
    (signPat (v θ).1 * Real.sqrt ((v θ).1 ^ 2),
     signPat (v θ).2 * Real.sqrt (1 - (v θ).1 ^ 2)) = v θ := by
  have h2 : 1 - (v θ).1 ^ 2 = (v θ).2 ^ 2 := by linarith [v_is_unit θ]
  rw [h2, Real.sqrt_sq_eq_abs, Real.sqrt_sq_eq_abs]
  exact Prod.ext (signPat_mul_abs _) (signPat_mul_abs _)

/-! ## 4. (4) A densidade lida pelo par (peso, paridade) -/

/-- [DEF] O PESO: `ρ₀₀ = v₀² = cos²θ` — o Nome. -/
def rhoWeight (θ : ℝ) : ℝ := (v θ).1 ^ 2

/-- [DEF] A PARIDADE: `sign(v₀·v₁)`, o produto dos dois sinais do código (a leitura que o código executável das patentes faz:
    `acom_mirror.py` l.32 e l.45; ver o ⚠ do cabeçalho). É o sinal da coerência `ρ₀₁`. -/
def rhoParity (θ : ℝ) : SignType := SignType.sign ((v θ).1 * (v θ).2)

theorem rhoWeight_eq (θ : ℝ) : rhoWeight θ = Real.cos θ ^ 2 := rfl

/-- [REAL] A PARIDADE É O PRODUTO DOS DOIS SINAIS: `sign(v₀v₁) = sign v₀ · sign v₁` (= Palavra · Verbo). -/
theorem rhoParity_eq_product (θ : ℝ) :
    rhoParity θ = (codeAmp θ).word * (codeAmp θ).verb := by
  unfold rhoParity
  exact _root_.sign_mul _ _

/-- ★ [REAL] A PARIDADE É O SINAL DA DERIVADA DO NOME: `sign(v₀v₁) = sign (d(cos²θ)/dθ)` — o sinal do Verbo no nível da densidade. -/
theorem the_parity_is_the_sign_of_the_derivative_of_the_name (θ : ℝ) :
    rhoParity θ = SignType.sign (deriv (fun t => Real.cos t ^ 2) θ) := by
  rw [(hasDerivAt_nome θ).deriv]
  unfold rhoParity
  symm
  rw [_root_.sign_mul, _root_.sign_pos (by norm_num : (0 : ℝ) < 2), one_mul]

/-- [DEF] O DECODIFICADOR EXPLÍCITO DA DENSIDADE: `(w, p) ↦ !![w, p·√(w(1−w)); p·√(w(1−w)), 1−w]`. -/
def decodeRho (w : ℝ) (p : SignType) : Matrix (Fin 2) (Fin 2) ℂ :=
  !![(w : ℂ), (((p : ℝ) * Real.sqrt (w * (1 - w)) : ℝ) : ℂ);
     (((p : ℝ) * Real.sqrt (w * (1 - w)) : ℝ) : ℂ), ((1 - w : ℝ) : ℂ)]

/-- ★★★ (4) [REAL] RECONSTRUÇÃO EXATA DA DENSIDADE: `ρ_out(θ) = decodeRho (peso cos²θ) (paridade sign(v₀v₁))`. Perda zero. -/
theorem rhoOut_eq_decodeRho (θ : ℝ) :
    rhoOut θ = decodeRho (rhoWeight θ) (rhoParity θ) := by
  have hw : 1 - rhoWeight θ = (v θ).2 ^ 2 := by
    unfold rhoWeight; linarith [v_is_unit θ]
  have hx : ((rhoParity θ : SignType) : ℝ) * Real.sqrt (rhoWeight θ * (1 - rhoWeight θ))
      = (v θ).1 * (v θ).2 := by
    rw [hw]
    have h : rhoWeight θ * (v θ).2 ^ 2 = ((v θ).1 * (v θ).2) ^ 2 := by
      unfold rhoWeight; ring
    rw [h, Real.sqrt_sq_eq_abs]
    unfold rhoParity
    exact sign_mul_abs ((v θ).1 * (v θ).2)
  rw [rhoOut_eq_real]
  unfold decodeRho
  rw [hx, hw]
  rfl

/-- [DEF] A LEITURA DA DENSIDADE: `ρ ↦ (Re ρ₀₀, sign Re ρ₀₁)`. -/
def readRho (ρ : Matrix (Fin 2) (Fin 2) ℂ) : ℝ × SignType :=
  ((ρ 0 0).re, SignType.sign (ρ 0 1).re)

/-- [REAL] A leitura de `ρ_out(θ)` é o par `(peso, paridade)`. -/
theorem readRho_rhoOut (θ : ℝ) : readRho (rhoOut θ) = (rhoWeight θ, rhoParity θ) := by
  simp only [readRho, rhoOut_00, rhoOut_01, Complex.ofReal_re]
  rfl

/-- ★★★ (4) [REAL] A DENSIDADE SÓ DEPENDE DE (PESO, PARIDADE) E O PAR É UM INVARIANTE COMPLETO: `ρ_out(θ) = ρ_out(θ')` se e só se
    os pesos e as paridades coincidem. -/
theorem the_density_is_its_code (θ θ' : ℝ) :
    rhoOut θ = rhoOut θ' ↔ (rhoWeight θ = rhoWeight θ' ∧ rhoParity θ = rhoParity θ') := by
  constructor
  · intro h
    have h' := congrArg readRho h
    rw [readRho_rhoOut, readRho_rhoOut] at h'
    exact Prod.mk.inj h'
  · rintro ⟨hw, hp⟩
    rw [rhoOut_eq_decodeRho, rhoOut_eq_decodeRho, hw, hp]

/-- [REAL] `decodeRho ∘ readRho = id` sobre a densidade da órbita: a leitura do par devolve a fractalização do Um igual sem perda. -/
theorem decodeRho_readRho (θ : ℝ) :
    decodeRho (readRho (rhoOut θ)).1 (readRho (rhoOut θ)).2 = rhoOut θ := by
  rw [readRho_rhoOut]
  exact (rhoOut_eq_decodeRho θ).symm

theorem v_add_pi (θ : ℝ) : v (θ + Real.pi) = (-(v θ).1, -(v θ).2) := by
  simp [v, Real.cos_add_pi, Real.sin_add_pi]

/-- ★★ (4) [REAL] O SINAL GLOBAL NÃO SE OBSERVA: `v(θ + π) = −v(θ)`; os DOIS sinais do código da amplitude se invertem (Palavra e
    Verbo), mas o peso, a paridade (o produto) e a densidade ficam iguais. Da amplitude à densidade o par de sinais se reduz ao seu
    produto. -/
theorem the_global_sign_is_not_observed (θ : ℝ) :
    v (θ + Real.pi) = (-(v θ).1, -(v θ).2)
    ∧ (codeAmp (θ + Real.pi)).word = -(codeAmp θ).word
    ∧ (codeAmp (θ + Real.pi)).verb = -(codeAmp θ).verb
    ∧ rhoWeight (θ + Real.pi) = rhoWeight θ
    ∧ rhoParity (θ + Real.pi) = rhoParity θ
    ∧ rhoOut (θ + Real.pi) = rhoOut θ := by
  have hv := v_add_pi θ
  have hw : rhoWeight (θ + Real.pi) = rhoWeight θ := by
    unfold rhoWeight
    rw [hv]
    simp
  have hp : rhoParity (θ + Real.pi) = rhoParity θ := by
    unfold rhoParity
    rw [hv]
    simp
  refine ⟨hv, ?_, ?_, hw, hp, ?_⟩
  · show SignType.sign (v (θ + Real.pi)).1 = -SignType.sign (v θ).1
    rw [hv]
    exact Left.sign_neg _
  · show SignType.sign (v (θ + Real.pi)).2 = -SignType.sign (v θ).2
    rw [hv]
    exact Left.sign_neg _
  · exact (the_density_is_its_code _ _).2 ⟨hw, hp⟩

/-- [REAL] ÁLGEBRA DO SINAL: se `a² = a'²`, `b² = b'²` e `ab = a'b'`, então `(a', b') = (a, b)` ou `(a', b') = (−a, −b)`. -/
theorem pair_equal_up_to_the_global_sign {a b a' b' : ℝ}
    (e0 : a ^ 2 = a' ^ 2) (e1 : b ^ 2 = b' ^ 2) (e01 : a * b = a' * b') :
    (a' = a ∧ b' = b) ∨ (a' = -a ∧ b' = -b) := by
  have ha : a' = a ∨ a' = -a := by
    have h : (a' - a) * (a' + a) = 0 := by linear_combination -e0
    rcases mul_eq_zero.mp h with h | h
    · exact Or.inl (by linarith)
    · exact Or.inr (by linarith)
  have hb : b' = b ∨ b' = -b := by
    have h : (b' - b) * (b' + b) = 0 := by linear_combination -e1
    rcases mul_eq_zero.mp h with h | h
    · exact Or.inl (by linarith)
    · exact Or.inr (by linarith)
  rcases ha with ha | ha <;> rcases hb with hb | hb
  · exact Or.inl ⟨ha, hb⟩
  · have hab : a * b = 0 := by
      rw [ha, hb] at e01
      linarith
    rcases mul_eq_zero.mp hab with h0 | h0
    · exact Or.inr ⟨by rw [ha, h0]; ring, hb⟩
    · exact Or.inl ⟨ha, by rw [hb, h0]; ring⟩
  · have hab : a * b = 0 := by
      rw [ha, hb] at e01
      linarith
    rcases mul_eq_zero.mp hab with h0 | h0
    · exact Or.inl ⟨by rw [ha, h0]; ring, hb⟩
    · exact Or.inr ⟨ha, by rw [hb, h0]; ring⟩
  · exact Or.inr ⟨ha, hb⟩

/-- ★★ (4) [REAL] DA AMPLITUDE À DENSIDADE SÓ O SINAL GLOBAL SE PERDE: `ρ_out(θ) = ρ_out(θ')` se e só se `v(θ') = v(θ)` ou
    `v(θ') = −v(θ)`. (Fecha a recíproca de `the_global_sign_is_not_observed`.) -/
theorem only_the_global_sign_is_lost (θ θ' : ℝ) :
    rhoOut θ = rhoOut θ' ↔ (v θ' = v θ ∨ v θ' = (-(v θ).1, -(v θ).2)) := by
  constructor
  · intro h
    have h00 := congrFun (congrFun h 0) 0
    have h01 := congrFun (congrFun h 0) 1
    have h11 := congrFun (congrFun h 1) 1
    rw [rhoOut_00, rhoOut_00] at h00
    rw [rhoOut_01, rhoOut_01] at h01
    rw [rhoOut_11, rhoOut_11] at h11
    have e0 : (v θ).1 ^ 2 = (v θ').1 ^ 2 := by exact_mod_cast h00
    have e01 : (v θ).1 * (v θ).2 = (v θ').1 * (v θ').2 := by exact_mod_cast h01
    have e1 : (v θ).2 ^ 2 = (v θ').2 ^ 2 := by exact_mod_cast h11
    rcases pair_equal_up_to_the_global_sign e0 e1 e01 with ⟨h1, h2⟩ | ⟨h1, h2⟩
    · exact Or.inl (Prod.ext h1 h2)
    · exact Or.inr (Prod.ext h1 h2)
  · intro h
    rw [rhoOut_eq_real θ, rhoOut_eq_real θ']
    rcases h with h | h
    · rw [h]
    · rw [h]
      simp

/-! ## 5. (5) O colapso perde exatamente a paridade -/

/-- [REAL] A reflexão `θ ↦ −θ` mantém o peso e INVERTE a paridade: `sign(v₀v₁)(−θ) = −sign(v₀v₁)(θ)`. -/
theorem parity_neg (θ : ℝ) : rhoParity (-θ) = -rhoParity θ := by
  unfold rhoParity
  simp only [v_fst, v_snd, Real.cos_neg, Real.sin_neg, neg_neg]
  rw [mul_neg, Left.sign_neg, neg_neg]

/-- [REAL] Fora dos eixos (`sin 2θ ≠ 0`) a paridade não é nula: é `+1` ou `−1`. -/
theorem parity_ne_zero_of_generic {θ : ℝ} (h : Real.sin (2 * θ) ≠ 0) : rhoParity θ ≠ 0 := by
  intro h0
  have h3 : (v θ).1 * (v θ).2 = 0 := _root_.sign_eq_zero_iff.mp h0
  apply h
  rw [Real.sin_two_mul]
  have h4 : Real.cos θ * -Real.sin θ = 0 := h3
  linear_combination (-2 : ℝ) * h4

/-- ★★★ (5) [REAL] O COLAPSO NÃO VÊ A PARIDADE: `D_∞F_θ(1) = D_∞F_{−θ}(1)` (`diagExpect` é o ponto final `Posto.endpoint_eq`). -/
theorem collapse_forgets_the_parity (θ : ℝ) :
    diagExpect (rhoOut θ) = diagExpect (rhoOut (-θ)) := by
  rw [Posto.endpoint_eq, Posto.endpoint_eq]
  simp [Real.cos_neg, Real.sin_neg]

/-- ★★★ (5) [REAL] A LEITURA COMPLETA A LEMBRA: se `sin 2θ ≠ 0`, `ρ_out(θ) ≠ ρ_out(−θ)` — as duas densidades têm o mesmo colapso e
    paridades opostas. -/
theorem the_full_reading_remembers_the_parity {θ : ℝ} (h : Real.sin (2 * θ) ≠ 0) :
    rhoOut θ ≠ rhoOut (-θ) := by
  intro heq
  have h1 := ((the_density_is_its_code θ (-θ)).1 heq).2
  have h2 : rhoParity θ = -rhoParity θ := h1.trans (parity_neg θ)
  have h0 : rhoParity θ = 0 := by
    revert h2
    generalize rhoParity θ = s
    revert s
    decide
  exact parity_ne_zero_of_generic h h0

/-- ★★ (5) [REAL] A VARIÁVEL PERDIDA É UM BIT: fora dos eixos as duas paridades `(θ, −θ)` são exatamente `(+1, −1)` ou `(−1, +1)`. -/
theorem the_lost_variable_is_one_bit {θ : ℝ} (h : Real.sin (2 * θ) ≠ 0) :
    (rhoParity θ = 1 ∧ rhoParity (-θ) = -1) ∨ (rhoParity θ = -1 ∧ rhoParity (-θ) = 1) := by
  have hne := parity_ne_zero_of_generic h
  rw [parity_neg]
  revert hne
  generalize rhoParity θ = s
  revert s
  decide

/-- ★★★ (5) [REAL] O COLAPSO IDENTIFICA EXATAMENTE OS ESTADOS DE MESMO PESO: `diagExpect (ρ_out θ) = diagExpect (ρ_out θ')` se e só se
    `cos²θ = cos²θ'`. -/
theorem collapse_identifies_exactly_equal_weights (θ θ' : ℝ) :
    diagExpect (rhoOut θ) = diagExpect (rhoOut θ') ↔ rhoWeight θ = rhoWeight θ' := by
  rw [Posto.endpoint_eq, Posto.endpoint_eq]
  constructor
  · intro h
    have h0 := congrFun (congrFun h 0) 0
    simp only [Matrix.diagonal_apply_eq, Matrix.cons_val_zero] at h0
    show Real.cos θ ^ 2 = Real.cos θ' ^ 2
    exact_mod_cast h0
  · intro hw
    have hw' : Real.cos θ ^ 2 = Real.cos θ' ^ 2 := hw
    have hs : Real.sin θ ^ 2 = Real.sin θ' ^ 2 := by
      have e1 := Real.sin_sq_add_cos_sq θ
      have e2 := Real.sin_sq_add_cos_sq θ'
      linarith
    have hc : ((Real.cos θ : ℝ) : ℂ) ^ 2 = ((Real.cos θ' : ℝ) : ℂ) ^ 2 := by exact_mod_cast hw'
    have hs' : ((Real.sin θ : ℝ) : ℂ) ^ 2 = ((Real.sin θ' : ℝ) : ℂ) ^ 2 := by exact_mod_cast hs
    rw [hc, hs']

/-- ★★★ (5) [REAL] O COLAPSO PERDE EXATAMENTE A PARIDADE: `ρ_out(θ) = ρ_out(θ')` se e só se têm o mesmo colapso E a mesma paridade.
    Dentro de uma fibra do colapso só a paridade resta. -/
theorem the_collapse_loses_exactly_the_parity (θ θ' : ℝ) :
    rhoOut θ = rhoOut θ' ↔
      (diagExpect (rhoOut θ) = diagExpect (rhoOut θ') ∧ rhoParity θ = rhoParity θ') := by
  rw [the_density_is_its_code, collapse_identifies_exactly_equal_weights]

/-- ★★★ O LIVRO DAS PERDAS, nos três níveis da leitura — cada degrau perde exatamente um bit de sinal, e nada além disso:
    (i) a AMPLITUDE (código do par de sinais, 2 bits) é lida sem perda; (ii) a DENSIDADE perde exatamente o sinal global (o par de
    sinais vira o seu produto, 1 bit); (iii) o COLAPSO perde exatamente a paridade (0 bits de sinal, só o peso). Conjunção de
    `codeAmp_eq_iff`, `only_the_global_sign_is_lost` e `collapse_identifies_exactly_equal_weights`. -/
theorem the_ledger_of_losses :
    (∀ θ θ' : ℝ, codeAmp θ = codeAmp θ' ↔ v θ = v θ')
    ∧ (∀ θ θ' : ℝ, rhoOut θ = rhoOut θ' ↔ (v θ' = v θ ∨ v θ' = (-(v θ).1, -(v θ).2)))
    ∧ (∀ θ θ' : ℝ, diagExpect (rhoOut θ) = diagExpect (rhoOut θ') ↔ rhoWeight θ = rhoWeight θ') :=
  ⟨codeAmp_eq_iff, only_the_global_sign_is_lost, collapse_identifies_exactly_equal_weights⟩

/-- ★★ (5) [REAL] O COLAPSO NÃO TEM INVERSA À ESQUERDA SOBRE A ÓRBITA: não existe `R` com `R (diagExpect (ρ_out θ)) = ρ_out θ` para
    todo `θ` (testemunha: `θ = π/4`, `sin(π/2) = 1`). -/
theorem the_collapse_has_no_left_inverse_on_the_orbit :
    ¬ ∃ R : Matrix (Fin 2) (Fin 2) ℂ → Matrix (Fin 2) (Fin 2) ℂ,
        ∀ θ : ℝ, R (diagExpect (rhoOut θ)) = rhoOut θ := by
  rintro ⟨R, hR⟩
  have hsin : Real.sin (2 * (Real.pi / 4)) ≠ 0 := by
    have h : 2 * (Real.pi / 4) = Real.pi / 2 := by ring
    rw [h, Real.sin_pi_div_two]
    exact one_ne_zero
  have h1 := hR (Real.pi / 4)
  have h2 := hR (-(Real.pi / 4))
  rw [collapse_forgets_the_parity] at h1
  exact the_full_reading_remembers_the_parity hsin (h1.symm.trans h2)

/-! ## 6. (6) Os pesos iguais (a leitura «ponto fixo», [ONTO]) e o bit justo -/

/-- [REAL] PESOS TROCÁVEIS SOMAM A MEIA-NAT: se `cos²θ = sin²θ` então `cos²θ = 1/2` (por `observer_inverse_projection_halfnat`). -/
theorem balanced_weights_are_half {θ : ℝ} (h : Real.cos θ ^ 2 = Real.sin θ ^ 2) :
    Real.cos θ ^ 2 = 1 / 2 :=
  observer_inverse_projection_halfnat _ _ h (Real.cos_sq_add_sin_sq θ)

/-- [REAL] OS ÂNGULOS DE PESOS IGUAIS: `cos²θ = sin²θ` se e só se `θ = π/4 + kπ/2` para algum inteiro `k` (`cos 2θ = 0`). -/
theorem balanced_weights_iff {θ : ℝ} :
    Real.cos θ ^ 2 = Real.sin θ ^ 2 ↔ ∃ k : ℤ, θ = Real.pi / 4 + k * (Real.pi / 2) := by
  have h2 : Real.cos (2 * θ) = Real.cos θ ^ 2 - Real.sin θ ^ 2 := by
    rw [Real.cos_two_mul]
    nlinarith [Real.sin_sq_add_cos_sq θ]
  constructor
  · intro h
    have hc : Real.cos (2 * θ) = 0 := by rw [h2]; linarith
    obtain ⟨k, hk⟩ := Real.cos_eq_zero_iff.mp hc
    refine ⟨k, ?_⟩
    linarith
  · rintro ⟨k, hk⟩
    have hc : Real.cos (2 * θ) = 0 := Real.cos_eq_zero_iff.mpr ⟨k, by rw [hk]; ring⟩
    rw [h2] at hc
    linarith

/-- [REAL] `π/4` tem os pesos iguais: `cos²(π/4) = sin²(π/4)`. -/
theorem pi_div_four_weights_are_balanced :
    Real.cos (Real.pi / 4) ^ 2 = Real.sin (Real.pi / 4) ^ 2 := by
  rw [Real.cos_pi_div_four, Real.sin_pi_div_four]

/-- ★★ (6) [REAL] EM TODO θ DE PESOS IGUAIS (`π/4 + kπ/2`) O COLAPSO É `(1/2)•1`: os dois pesos valem ½. -/
theorem balanced_collapse_is_half {θ : ℝ} (h : Real.cos θ ^ 2 = Real.sin θ ^ 2) :
    diagExpect (rhoOut θ) = (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  have hcos : Real.cos θ ^ 2 = 1 / 2 := balanced_weights_are_half h
  have hsin : Real.sin θ ^ 2 = 1 / 2 := by
    have e := Real.sin_sq_add_cos_sq θ
    linarith
  have hc : ((Real.cos θ : ℝ) : ℂ) ^ 2 = 1 / 2 := by
    rw [← Complex.ofReal_pow, hcos]
    norm_num
  have hs : ((Real.sin θ : ℝ) : ℂ) ^ 2 = 1 / 2 := by
    rw [← Complex.ofReal_pow, hsin]
    norm_num
  rw [Posto.endpoint_eq, hc, hs]
  ext i j
  fin_cases i <;> fin_cases j <;> simp

/-- ★★ (6) [REAL; o NOME «ponto fixo» é [ONTO]] EM `θ = π/4` o colapso é `(1/2)•1`. A equação é [REAL]; ler `π/4` como «o ponto fixo» é
    leitura do operador: `π/4` não é ponto fixo de nenhuma aplicação em θ desta pedra, só representa os pesos iguais `x = 1 − x`. -/
theorem at_the_fixed_point_the_collapse_is_half :
    diagExpect (rhoOut (Real.pi / 4)) = (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) :=
  balanced_collapse_is_half pi_div_four_weights_are_balanced

/-- [REAL] O QUE É PONTO FIXO: `(1/2)•1` é fixado pelo colapso (`diagExpect`) e por TODA conjugação pela matriz-S,
    `S(θ)·X·S(θ)ᴴ = X` (unitariedade, `Smat_mul_conjTranspose`). Que este estado seja «o ponto fixo» sobre o qual o sistema flutua é [ONTO]. -/
theorem half_identity_is_a_fixed_point :
    diagExpect ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)) = (1 / 2 : ℂ) • 1
    ∧ ∀ θ : ℝ, Smat θ * ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)) * (Smat θ)ᴴ
        = (1 / 2 : ℂ) • 1 := by
  refine ⟨?_, fun θ => ?_⟩
  · ext i j
    fin_cases i <;> fin_cases j <;> simp [diagExpect]
  · rw [Matrix.mul_smul, Matrix.mul_one, Matrix.smul_mul, Smat_mul_conjTranspose]

/-- [DEF] A entropia de Shannon (em nats) da distribuição dos RESULTADOS do colapso, `(cos²θ, 1 − cos²θ)`. Não é a entropia de
    nenhum canal físico: é a da distribuição de pesos da diagonal. -/
def collapseEntropy (θ : ℝ) : ℝ := Real.binEntropy (Real.cos θ ^ 2)

/-- ★★ (6) [REAL] EM TODO θ DE PESOS IGUAIS OS RESULTADOS DO COLAPSO SÃO O BIT JUSTO: `collapseEntropy θ = fairBitEntropy` (`= ln 2`, por
    `fair_bit_entropy_is_log_two`). -/
theorem collapseEntropy_at_balanced_weights {θ : ℝ} (h : Real.cos θ ^ 2 = Real.sin θ ^ 2) :
    collapseEntropy θ = ChatgptAudit.Collapse057.fairBitEntropy := by
  unfold collapseEntropy
  rw [balanced_weights_are_half h, ChatgptAudit.Collapse057.fair_bit_entropy_is_log_two]
  have h2 : (1 / 2 : ℝ) = 2⁻¹ := by norm_num
  rw [h2]
  exact Real.binEntropy_two_inv

/-- ★★ (6) [REAL] Em `θ = π/4`: `collapseEntropy (π/4) = fairBitEntropy`. (Vale em todo `π/4 + kπ/2`: `collapseEntropy_at_balanced_weights`.) -/
theorem collapseEntropy_at_the_fixed_point :
    collapseEntropy (Real.pi / 4) = ChatgptAudit.Collapse057.fairBitEntropy :=
  collapseEntropy_at_balanced_weights pi_div_four_weights_are_balanced

/-- [REAL] NENHUM ÂNGULO EXCEDE O BIT JUSTO: `collapseEntropy θ ≤ fairBitEntropy`. (O limite da analogia, dito em
    `fair_bit_entropy_is_not_half_nat`: o bit justo é `ln 2`, não a meia-nat.) -/
theorem collapseEntropy_le_the_fair_bit (θ : ℝ) :
    collapseEntropy θ ≤ ChatgptAudit.Collapse057.fairBitEntropy := by
  rw [ChatgptAudit.Collapse057.fair_bit_entropy_is_log_two]
  exact Real.binEntropy_le_log_two

/-! ## 6b. O colapso do psibit é um Um posto no sentido do kernel -/

/-- [REAL] No ponto fixo a fractalização do Um igual NÃO é o seu colapso: `ρ_out(π/4) ≠ (1/2)•1` (a coerência `−1/2` ≠ 0). -/
theorem rho_pi_div_four_ne_half :
    rhoOut (Real.pi / 4) ≠ (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  intro h
  have h' := congrFun (congrFun h 0) 1
  rw [rhoOut_01, v_pi_div_four] at h'
  simp at h'

/-- [DEF] A TRAVESSIA do colapso: `step = diagExpect`, a leitura da identidade é o TRAÇO (a normalização; escolha [DEF] desta pedra),
    idempotente (`diagExpect_idem`), que preserva o traço (`trace_diagExpect`) e é efetiva. -/
def psibitCrossing :
    ChatgptAudit.Collapse057.IdentityCollapse (Matrix (Fin 2) (Fin 2) ℂ) ℂ where
  step := diagExpect
  identity := Matrix.trace
  stable := fun x => diagExpect_idem x
  preserves := fun x => trace_diagExpect x
  effective := ⟨!![0, 1; 0, 0], by
    intro h
    have h' := congrFun (congrFun h 0) 1
    simp [diagExpect] at h'⟩

/-- ★★ [REAL] O COLAPSO DO PSIBIT É UM UM POSTO (`UmPostoRelacao.UmPosto`): a travessia `diagExpect`; medido antes de ser posto (o estado
    puro `ρ_out(π/4)` vira `(1/2)•1`, um evento efetivo); a leitura (o traço) é legível. -/
def psibitPosto : UmPostoRelacao.UmPosto (Matrix (Fin 2) (Fin 2) ℂ) ℂ where
  crossing := psibitCrossing
  before := rhoOut (Real.pi / 4)
  after := (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)
  measured := ⟨at_the_fixed_point_the_collapse_is_half, rho_pi_div_four_ne_half⟩
  legible := ⟨1, 0, by
    show Matrix.trace (1 : Matrix (Fin 2) (Fin 2) ℂ) ≠ Matrix.trace (0 : Matrix (Fin 2) (Fin 2) ℂ)
    simp⟩

/-- ★★ [REAL] A TRAVESSIA PAGA PERDA: o colapso `diagExpect` não tem inversa à esquerda em toda a álgebra (por
    `UmPostoRelacao.posto_paid_loss` aplicado a `psibitPosto`). Contraste: a leitura do par (`codeAmp`) é injetiva. -/
theorem the_psibit_crossing_pays_loss :
    ¬ ∃ R : Matrix (Fin 2) (Fin 2) ℂ → Matrix (Fin 2) (Fin 2) ℂ,
        Function.LeftInverse R diagExpect :=
  UmPostoRelacao.posto_paid_loss psibitPosto

/-! ## 6c. O NOME É O POSTO: o peso é a leitura de Born -/

/-- [DEF] O estado `S(θ)·e₁` como vetor de `ℂ²`. -/
def stateVec (θ : ℝ) : EuclideanSpace ℂ (Fin 2) := WithLp.toLp 2 ((Smat θ).mulVec e1)

/-- [DEF] O vetor unitário `e₀` (o modo incidente). -/
def basis0 : EuclideanSpace ℂ (Fin 2) := EuclideanSpace.single (0 : Fin 2) (1 : ℂ)

theorem basis0_norm : ‖basis0‖ = 1 := by
  simp [basis0]

theorem stateVec_zero (θ : ℝ) : (stateVec θ) 0 = ((Real.cos θ : ℝ) : ℂ) := by
  show ((Smat θ).mulVec e1) 0 = _
  exact Smat_transmission θ

theorem inner_basis0_stateVec (θ : ℝ) : ⟪basis0, stateVec θ⟫_ℂ = ((Real.cos θ : ℝ) : ℂ) := by
  rw [basis0, EuclideanSpace.inner_single_left, stateVec_zero]
  simp

/-- ★★ [REAL] O NOME É O POSTO: a leitura de Born do posto `e₀` (`TheVerbSelectsTheAction.post`, o projetor de posto 1) pelo estado
    `S(θ)·e₁` é `cos²θ`, o peso do código. Por `TheVerbSelectsTheAction.reading_post_is_born`. -/
theorem the_name_is_the_born_reading_of_the_post (θ : ℝ) :
    TheVerbSelectsTheAction.reading (TheVerbSelectsTheAction.post basis0) (stateVec θ)
      = ((rhoWeight θ : ℝ) : ℂ) := by
  rw [TheVerbSelectsTheAction.reading_post_is_born basis0_norm, inner_basis0_stateVec,
    Complex.norm_real, Real.norm_eq_abs, sq_abs]
  rfl

/-! ## 7. (7) A composição INCONDICIONAL e, à parte, a face do psion (CONDICIONAL) -/

/-- ★★★ (7) [REAL — conjunção INCONDICIONAL, sem dedução nova além das provas acima; NENHUM certificado é hipótese] O PSIBIT É O MODO DO LEITOR,
    no que o kernel entrega: (1) o Verbo é a derivada do Nome; (2) o estado é puro, de posto 1; (3) a leitura do par não perde (decodificador
    explícito, injetividade) e é bijeção sobre o livro de códigos; (4) a densidade é reconstruída exatamente do par (peso, paridade), o sinal
    global não se observa, e o livro das perdas (amplitude: nada; densidade: só o sinal global; colapso: exatamente a paridade); (5) o
    colapso não vê a paridade e a leitura completa a lembra fora dos eixos; o bit justo vale `ln 2`; (6) nos pesos iguais (`π/4 + kπ/2`) o
    colapso é `(1/2)•1` e a entropia dos resultados é o bit justo; o Nome é a leitura de Born do posto (`reading_post_is_born`); a bandeira da
    pedra v394 (`the_binary_reading_floats_at_the_fixed_point`); a meia-nat da projeção inversa do observador; e a travessia PAGA PERDA
    (`posto_paid_loss`, geral e no colapso do psibit), ao passo que a leitura do par NÃO perde — o separante (injetivo) e o separador
    (muitos-para-um) no mesmo objeto. A FACE DO PSION NÃO está aqui: é condicional ao certificado e vive em `the_psion_face_of_the_psibit`.
    A identidade `psibit = psion = modo do leitor` NÃO é um termo: é [INPUT/ONTO] do operador (ver o cabeçalho). -/
theorem psibit_is_the_mode_of_the_reader :
    (∀ θ : ℝ, rhoOut θ 0 1 = (((1 / 2 : ℝ) * deriv (fun t => Real.cos t ^ 2) θ : ℝ) : ℂ))
    ∧ (∀ θ : ℝ, rhoOut θ 0 1 ^ 2 = rhoOut θ 0 0 * rhoOut θ 1 1)
    ∧ (∀ θ : ℝ, (rhoOut θ).rank = 1 ∧ rhoOut θ * rhoOut θ = rhoOut θ)
    ∧ (∀ θ : ℝ, decodeAmp (codeAmp θ) = v θ)
    ∧ (∀ θ θ' : ℝ, codeAmp θ = codeAmp θ' → v θ = v θ')
    ∧ (type_of% the_orbit_is_in_bijection_with_the_code_book)
    ∧ (∀ θ : ℝ, rhoOut θ = decodeRho (rhoWeight θ) (rhoParity θ))
    ∧ (∀ θ : ℝ, rhoOut (θ + Real.pi) = rhoOut θ)
    ∧ (type_of% the_ledger_of_losses)
    ∧ (∀ θ : ℝ, diagExpect (rhoOut θ) = diagExpect (rhoOut (-θ)))
    ∧ (∀ θ : ℝ, Real.sin (2 * θ) ≠ 0 → rhoOut θ ≠ rhoOut (-θ))
    ∧ ChatgptAudit.Collapse057.fairBitEntropy = Real.log 2
    ∧ (∀ θ : ℝ, Real.cos θ ^ 2 = Real.sin θ ^ 2 →
        diagExpect (rhoOut θ) = (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)
          ∧ collapseEntropy θ = ChatgptAudit.Collapse057.fairBitEntropy)
    ∧ diagExpect (rhoOut (Real.pi / 4)) = (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)
    ∧ (∀ θ : ℝ, TheVerbSelectsTheAction.reading (TheVerbSelectsTheAction.post basis0) (stateVec θ)
        = ((rhoWeight θ : ℝ) : ℂ))
    ∧ (type_of% the_binary_reading_floats_at_the_fixed_point)
    ∧ (∀ ωP ωQ : ℝ, ωP = ωQ → ωP + ωQ = 1 → ωP = 1 / 2)
    ∧ (∀ {S I : Type} (P : UmPostoRelacao.UmPosto S I),
        ¬ ∃ R : S → S, Function.LeftInverse R P.crossing.step)
    ∧ (¬ ∃ R : Matrix (Fin 2) (Fin 2) ℂ → Matrix (Fin 2) (Fin 2) ℂ,
        Function.LeftInverse R diagExpect) :=
  ⟨the_verb_is_the_derivative_of_the_name,
   the_state_is_pure,
   the_state_is_a_rank_one_projector,
   decodeAmp_codeAmp,
   fun θ θ' h => (codeAmp_eq_iff θ θ').1 h,
   the_orbit_is_in_bijection_with_the_code_book,
   rhoOut_eq_decodeRho,
   fun θ => (the_global_sign_is_not_observed θ).2.2.2.2.2,
   the_ledger_of_losses,
   collapse_forgets_the_parity,
   fun _ h => the_full_reading_remembers_the_parity h,
   ChatgptAudit.Collapse057.fair_bit_entropy_is_log_two,
   fun _ h => ⟨balanced_collapse_is_half h, collapseEntropy_at_balanced_weights h⟩,
   at_the_fixed_point_the_collapse_is_half,
   the_name_is_the_born_reading_of_the_post,
   the_binary_reading_floats_at_the_fixed_point,
   observer_inverse_projection_halfnat,
   fun P => UmPostoRelacao.posto_paid_loss P,
   the_psibit_crossing_pays_loss⟩

/-- ★ [REAL — CONDICIONAL AO CERTIFICADO] A FACE DO PSION: para todo certificado `C : FockCertificate L`, o psion tem `⟨ψ, ψ⟩ = 1`
    (`inner_psion_psion`) e é fixado pela luz, `Δ^{it} ψ = ψ` para todo `t` (`psion_is_fixed_by_the_light`).
    ⚠ O KERNEL NÃO HABITA `FockCertificate`: `TheImportedSecondQuantization` (l.66–67, «NÃO-VACUIDADE») diz que nenhum habitante é exibido e que a
    não-vacuidade é ARGUMENTADA, sem termo que a demonstre; só há o construtor, `TetelestaiOneObject.rescale` (que exige outro certificado) e os
    montadores da v394 (`F1Fecho394/*Assembly*`), que partem de entradas restantes sem habitante exibido («not a claim that the remaining imported
    fields are inhabited»). Logo este enunciado é uma IMPLICAÇÃO sobre um tipo sem habitante conhecido: NÃO mostra que o psion exista; o contrato conjunto da
    rede segue aberto (v394). Por isso NÃO é parte de `psibit_is_the_mode_of_the_reader`, que é incondicional. NENHUM lema liga `psion C` a
    `codeAmp`: `psibit = psion = modo do leitor` é [INPUT/ONTO] do operador. -/
theorem the_psion_face_of_the_psibit :
    ∀ {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L),
      inner ℂ (ThePsionAndTheViscosity.psion C) (ThePsionAndTheViscosity.psion C) = 1
      ∧ (∀ t : ℝ, ImportedSQ.lightDelta C t (ThePsionAndTheViscosity.psion C)
          = ThePsionAndTheViscosity.psion C) :=
  fun C => ⟨ThePsionAndTheViscosity.inner_psion_psion C,
    ThePsionAndTheViscosity.psion_is_fixed_by_the_light C⟩

end

end TGLExt.Psibit

#print axioms TGLExt.Psibit.the_verb_is_the_derivative_of_the_name
#print axioms TGLExt.Psibit.the_state_is_pure
#print axioms TGLExt.Psibit.decodeAmp_codeAmp
#print axioms TGLExt.Psibit.codeAmp_injOn
#print axioms TGLExt.Psibit.the_orbit_is_in_bijection_with_the_code_book
#print axioms TGLExt.Psibit.the_pair_is_necessary_and_sufficient
#print axioms TGLExt.Psibit.rhoOut_eq_decodeRho
#print axioms TGLExt.Psibit.the_density_is_its_code
#print axioms TGLExt.Psibit.the_global_sign_is_not_observed
#print axioms TGLExt.Psibit.only_the_global_sign_is_lost
#print axioms TGLExt.Psibit.the_ledger_of_losses
#print axioms TGLExt.Psibit.collapse_forgets_the_parity
#print axioms TGLExt.Psibit.the_full_reading_remembers_the_parity
#print axioms TGLExt.Psibit.the_collapse_loses_exactly_the_parity
#print axioms TGLExt.Psibit.the_collapse_has_no_left_inverse_on_the_orbit
#print axioms TGLExt.Psibit.balanced_weights_iff
#print axioms TGLExt.Psibit.balanced_collapse_is_half
#print axioms TGLExt.Psibit.at_the_fixed_point_the_collapse_is_half
#print axioms TGLExt.Psibit.half_identity_is_a_fixed_point
#print axioms TGLExt.Psibit.collapseEntropy_at_balanced_weights
#print axioms TGLExt.Psibit.collapseEntropy_at_the_fixed_point
#print axioms TGLExt.Psibit.the_psibit_crossing_pays_loss
#print axioms TGLExt.Psibit.the_name_is_the_born_reading_of_the_post
#print axioms TGLExt.Psibit.psibit_is_the_mode_of_the_reader
#print axioms TGLExt.Psibit.the_psion_face_of_the_psibit
