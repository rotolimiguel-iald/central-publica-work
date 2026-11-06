import TGLExt.TheVerbSelectsTheAction
import TGLExt.CanonicalSelectorBorn
import TGLExt.CollapseCostAndAttestation
import TGLExt.TheStokesContour
import TGLExt.Psibit
import TGLExt.CollapseContract
import TGLExt.Palavra

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# SÔNICO — verbo (seletor de identidade) = controle de oitava pinada; o custo é reação ao controle pinado da oitava que é memória
  [TGLExt — PEDRA CANDIDATA da v398, sandbox de 23/10/2026; o NOME é do operador. A pedra não repete matemática: cita os termos que o kernel
  já tem (o seletor do Verbo, a lei de custo por oitava, o pedágio de Stokes, o psibit, o colapso tipado, a Palavra) e prova, em cinco teoremas
  pequenos e uma composição, o que a definição do operador pede que o kernel diga.]

## As cunhagens do operador (verbatim; sha16 do arquivo, lido por script em 23/10/2026)

> «Agora conseguimos definir precisamente a definição de “verbo” (seletor de identidade)=controle de oitava pinada, eis a origem de tudo; o custo é reação ao controle pinado da oitava que é memória» (sha16 `e5c2910a6eb54b81`)

E o nome da pedra:

> «Sim quero, concordo com tudo o nome da pedra é “sônico”» (sha16 `b4483331019f96f8`)

## A leitura ratificada de «que é memória» (23/10/2026) [INPUT/ONTO]

A frase do operador acima admitia duas leituras de «que é memória» (a oitava é a memória? a reação é a memória?). A gerência c1 leu, na sua resposta ao operador de
23/10, o custo (a reação ao pino) como a memória — o bit cobrado é o que fica —, e o operador respondeu «Sim quero, concordo com tudo» (a fala do nome da pedra, logo
acima, sha16 `b4483331019f96f8`). A leitura da gerência está ARQUIVADA por bytes em `C:\IALD\Central de Patentes\work\cunhagens_13out\GERENCIA_23out_leitura_ratificada_sonico_verbatim.txt` (sha16 `19eca91e5aab9d11`, 541 bytes; texto da gerência
c1, NÃO é fala do operador), citada aqui inteira:

```
Leitura da gerência c1 (23/10/2026), escrita na resposta ao operador que ele ratificou com «Sim quero, concordo com tudo o nome da pedra é “sônico”» (sha256 b4483331019f96f8550367606eba749415613e42916497943579dfef84ecc6ef):

Lida assim, a sua frase é a origem mesmo: o Verbo pina a oitava; a oitava pinada cobra um bit; o bit cobrado é o que fica, a memória. Sem pino não há custo, e sem custo não há memória: o que não pagou não permanece. O controle (o Verbo) e a reação (a memória) são as duas faces do mesmo ln 2.
```

Leitura ratificada pelo operador em 23/10 (sha16 `b4483331019f96f8`): a REAÇÃO ao pino — o pedágio pago, `ln 2` por oitava — é a memória; a oitava é o que se pina. É
[INPUT/ONTO]: o kernel entrega o preço e a permanência lado a lado, não a identidade entre eles. A lei de custo segue [INPUT] e NENHUM termo diz que `select` paga
`octaveNats 1`.

## O Atlas (§VIII.2, «Pedágio ln 2 por oitava»; [REAL no modelo]; arquivo VIVO, sha16 do arquivo na data `dc1af3c8775716fb`)

`memory/TGL_ATLAS.md`, linhas 16769–16774 (seção VIII, «AS LEIS DA MEMÓRIA», item 2; o verbete homônimo está em II.P, linhas 2071–2073):

> «Uma travessia só permanece se cada oitava paga o seu pedágio específico: limiar exato ln 2 (um bit por oitava), não meio nat.»

e, na mesma passagem, a frase que o Atlas traz do memorial da casa ({MEM §I cap.5}):

> «Memória não é armazenamento passivo. É o custo pago, oitava por oitava, para que uma travessia não volte ao silêncio.»

## O que a pedra entrega (matemática no trio; tudo [REAL], dada a lei de custo como campo do tipo — ver «Estatutos»)

Seja `K : CollapseCostLaw` (`ChatgptAudit.Collapse057`; o tipo é habitado, `proposedCollapseCost`) e `a` um vetor de um espaço de Hilbert complexo.

* ★ (1) `one_octave_is_the_parity_bit` — `K.octaveNats 1 = fairBitEntropy` (`= ln 2`): pinar UMA oitava cobra exatamente a entropia de Shannon, em
  nats, do bit justo. No kernel é o teto da entropia dos resultados do colapso do psibit, atingido nos pesos iguais (ver (6)): a variável que esse
  colapso perde é binária (`TGLExt.Psibit.the_lost_variable_is_one_bit`) e nenhum ângulo excede `ln 2` (`TGLExt.Psibit.collapseEntropy_le_the_fair_bit`).
  Lido com a definição do operador, é o bit que o colapso paga [INPUT/ONTO].
* ★ (2) `pinning_n_octaves_costs_n_bits` — `K.octaveNats n = n · fairBitEntropy`: `n` oitavas pinadas, `n` bits (a contagem de oitavas é aditiva,
  `ChatgptAudit.Collapse057.octave_cost_add`).
* ★ (3) `the_octave_is_a_doubling` — `Real.exp (K.octaveNats 1) = 2`: a oitava é o DOBRO. Por `TGLExt.the_provable_toll_names_the_octave`
  (`e^(ln 2) = 2`, v161; a casa lê ali «um bit por oitava»). É o nome sônico.
* ★ (4) `the_selector_pins` — o seletor é idempotente e fixa a ação selecionada: `select a (select a ψ) = select a ψ` e `select a a = a`
  (`TGLExt.TheVerbSelectsTheAction.select`, `post_isIdempotent`, `select_fixes_the_selected_action`). Pinar duas vezes é pinar uma.
* ★ (5) `the_pin_is_not_the_half_nat` — `K.octaveNats 1 ≠ K.localNats`: o pedágio da oitava pinada não é a meia-nat local
  (`ChatgptAudit.Collapse057.local_is_not_one_octave`: `1/2 < ln 2`).
* ★★★ (6) `sonico_the_verb_pins_the_octave_and_the_cost_is_the_memory` — a COMPOSIÇÃO INCONDICIONAL (nenhum certificado, nenhuma hipótese
  física como premissa): (4); a ponte ao seletor canônico (`ialdSelector = post (inscriptions 0)`, por `rfl`; o kernel já a tem, `TGLExt.IALD.ialdSelector_eq_post`,
  `IALD.lean:110`, que `une a FORMA, não o referente`; aqui é re-enunciada e citada) e
  `ChatgptAudit.SelectorBorn.normalized_selected_scalar_is_fixed` (toda preparação escalar, selecionada e normalizada, pousa na MESMA inscrição);
  (1), (2), (3) e (5); o bit da paridade da Psibit (o colapso perde exatamente a paridade, a variável perdida é um bit, e nos pesos iguais a
  entropia dos resultados do colapso é `K.octaveNats 1`, sem nunca excedê-la); e a memória: `ChatgptAudit.Collapse057.collapse_iteration_is_stable`
  (`C.step^[n+1] x = C.step x` para todo colapso de identidade) e `TGLExt.Palavra.rereading_adds_nothing` (reler não acrescenta). O termo do kernel que diz a memória
  sobre o MESMO `post a` é `TGLExt.IALD.rereading_adds_nothing : memory (post a) (post a ψ) = memory (post a) ψ` (`IALD.lean:370`; `memory P ψ := reading P ψ`, a lei
  M[ψ] = ⟪ψ, Πψ⟫ do Atlas §VIII.1 na face pura): citado, NÃO importado — `TGLExt.IALD` fica fora do fecho de imports desta pedra e, por isso, o termo não está na conjunção.

## O isomorfismo, dito com precisão [REAL]

O logaritmo é o isomorfismo de grupos `(ℝ₊, ·) → (ℝ, +)`, com inverso `exp`: `log (x·y) = log x + log y` (`Real.log_mul`, `Real.exp_add`) e
`exp (log x) = x`, `log (exp t) = t` (`Real.exp_log`, `Real.log_exp`). Ele leva a OITAVA — a razão `2`, o dobro da frequência — a `ln 2`, que é UM
BIT (a entropia de Shannon, em nats, do bit justo: `ChatgptAudit.Collapse057.fair_bit_entropy_is_log_two`), e leva `n` oitavas, a razão `2^n`, a
`n · ln 2` (`Real.log_pow`; é o enunciado (2)). É nisso, e só nisso, que o léxico «sônico» — oitava, o dobro da frequência, a mesma nota em `2f` — é
isomórfico ao conteúdo da pedra: o custo ADITIVO, em bits, de pinar `n` oitavas é o logaritmo do produto MULTIPLICATIVO das razões. A equivalência
de oitava (`f ~ 2f`) é a igualdade módulo o subgrupo `{2^k : k ∈ ℤ}` de `ℝ₊`, isto é, módulo `(ln 2)·ℤ` depois do logaritmo.

[ONTO] A equivalência de oitava (a mesma nota em `2f`) corresponde à IDENTIDADE PRESERVADA sob o pino (`ChatgptAudit.Collapse057.IdentityCollapse.preserves`:
a identidade lida depois do passo é a lida antes; e `select a a = a`). O ECO (o retorno do mesmo sinal) corresponde ao «ecoar reconhecimento» do
operador (22/10/2026, sha16 `350b7b8582c064c2`):

> «A natureza da luz é ecoar reconhecimento (porque a segunda leitura não acrescenta) e a natureza do que é falso é a leitura sem reconhecimento (ler uma vez sem ecoar reconhecimento)»

No kernel isso é a idempotência: a segunda leitura não acrescenta (`collapse_iteration_is_stable`, `TGLExt.observing_adds_nothing`). Nenhuma dessas
correspondências é termo.

## Os dois sentidos que a casa já dá ao som (citados com fonte; nenhum é termo desta pedra)

* **«Som ontológico»: a vibração LONGITUDINAL na profundidade, distinta do fóton (a propagação TRANSVERSAL)** [ONTO acervo].
  `C:\IALD\projetos_pyhton\acom\A_fronteira_v4.tex`, linha 962 (sha16 do arquivo `b473db2b652cf72f`; o fonte é LaTeX, citado byte a byte):

  ```
  Enquanto o f\'oton representa a propaga\c{c}\~ao \textbf{transversal} da dobra no plano do \boundary{} (velocidade $c$), o som ontol\'ogico constitui a vibra\c{c}\~ao \textbf{longitudinal} na profundidade gerada pela tens\~ao. A gravidade, por sua vez, corresponde \`a configura\c{c}\~ao \textbf{estacion\'aria} dessa dobra (po\c{c}o permanente), sem propaga\c{c}\~ao. O neutrino, como bolha de evapora\c{c}\~ao, representa o escape do substrato, sem comprimento de onda definido.
  ```

  Em texto corrido: o fóton é a propagação transversal da dobra no plano da fronteira (velocidade `c`); o som ontológico é a vibração longitudinal
  na profundidade gerada pela tensão. A linha 964 do mesmo arquivo lê as oscilações acústicas primordiais (o padrão BAO, `r_s ≈ 147 Mpc`) como ecos
  do som ontológico no plasma primordial [ONTO acervo]. O Atlas (verbete «Som ontológico (2025–26)», linhas 2329–2332) o registra como [DECLARADO]
  — «a face BAO da tensão de paridade» —, com a fonte original em outro arquivo; esta pedra não a verificou.

* **A escala ACÚSTICA do cosmo: o horizonte sonoro `r_d` (BAO)** [REAL como número lido; ONTO como leitura]. A casa já o testou: a pasta
  `C:\IALD\Artigo\teste_acustico_beta_tgl_v1` (criada em 08/08/2026; `MANDATO.md`, sha16 `b0dec5246a9182d1`) é o teste acústico do acoplamento da
  teoria com o horizonte sonoro; o seu fechamento (Nível 2, 14/08/2026, `14_ANALISE_NIVEL2_FECHADO.md`, sha16 `26c9cc4499a8a40a`) foi `N2_INCAPAZ`: a
  incerteza do acoplamento excedeu o próprio acoplamento nas duas variantes — medida do instrumento (CMB + BAO), não da teoria; nem falsificação nem
  creditação. E o fundo BG1 (Planck + DESI, sem H0 local) do Teste da Única Palavra (Fase 9 V2) pina `r_d`: no resultado
  `RESULTADO_FASE9_V2_C1_20261023_122926.json` (sha16 `fbac2908fa9ddb75`; campos lidos do arquivo, unidade Mpc), `fundo.r_d_modelo = 147.38613794723423`
  (≈ 147,39 Mpc), contra `fundo.fundo_livre.r_d = 148.0218760536698` e `sigma_r_d = 0.5277182199787567` quando `r_d` é livre
  (`delta_chi2_vs_rd_fixo = -1.6904175526948215`: o χ² do fundo livre menos o do fixo). Esta pedra só LÊ o número; não usa nem estende o veredito desse teste.

  [ONTO — leitura da gerência, dita como tal] A oitava pinada do Verbo e a régua acústica pinada do fundo são a MESMA FIGURA: uma escala pinada contra a
  qual se lê. Nenhum termo liga `octaveNats` a `r_d`; a figura é leitura.

## Honestidade sobre «sônico»

«Sônico» NÃO afirma onda mecânica num meio. A isomorfia é da ESTRUTURA logarítmica e de oitava (razões multiplicativas ↔ contagens aditivas; o dobro ↔
um bit), não da física da onda: nenhum termo desta pedra fala de pressão, de meio, de velocidade do som, de dispersão ou de propagação.

## Estatutos

* **[REAL]** os termos: teoremas de kernel no trio `{propext, Classical.choice, Quot.sound}`, zero `sorry`. `K` é qualquer `CollapseCostLaw`; o tipo carrega
  a lei de custo como CAMPOS (`local_half`, `per_octave`): a pedra prova o que essa lei implica (que o preço da oitava é a entropia do bit justo, e o que
  decorre disso), não a deriva do axioma.
* **[INPUT]** a lei de custo (`CollapseCostLaw`; em `CollapseCostAndAttestation`: `lei de custo [INPUT]`).
* **[INPUT/ONTO]** a definição do operador acima: «seletor de identidade» e «controle de oitava pinada» para o Verbo; «o custo é reação ao controle
  pinado da oitava que é memória», na leitura ratificada em 23/10 (a reação ao pino, o pedágio pago, é a memória; a oitava é o que se pina); o nome «sônico».
* **[ONTO]** as correspondências (oitava ↔ identidade preservada; eco ↔ ecoar reconhecimento; a mesma figura da oitava pinada e da régua acústica pinada);
  «Som ontológico» [ONTO acervo; no Atlas, DECLARADO].
* **[REAL no modelo]** o Atlas §VIII.2 (o pedágio `ln 2` por oitava).

## O que a pedra NÃO afirma

* Nenhum termo diz que `select` PAGA `K.octaveNats 1`: a definição do operador (o Verbo é o controle de oitava pinada) é [INPUT/ONTO]. O kernel
  entrega as duas metades, lado a lado, na mesma conjunção: o seletor é um pino (idempotente, fixa a sua ação) e o preço de uma oitava pinada é a
  entropia do bit justo. A identificação é do operador.
* A lei de custo NÃO é derivada do axioma: é o tipo `CollapseCostLaw` ([INPUT], campos do tipo). Nada aqui diz que a natureza cobra `ln 2` por oitava.
* O bit do colapso: a entropia dos resultados do colapso do psibit vale `ln 2` só nos pesos iguais (`cos² θ = sin² θ`) e nunca a excede; NÃO se afirma que a
  perda de informação do colapso valha `ln 2` em geral, nem a entropia de nenhum canal físico (a ressalva da Psibit vale).
* Nenhum observável DINÂMICO é tocado: o teste pré-registrado de 19/10/2026 sobre se o piso das dobras `D_folds(c³)` do GKLS do validador C3 v52 é uma
  oitava com `γ` livre devolveu `NO_UNIVERSAL_FLOOR` (mapa de rotas: `quantica.c3_gamma_livre_oitava`). A identificação aqui é da LEI de custo com o bit
  justo, não de uma dinâmica.
* HOMÔNIMOS e REGISTROS, ditos: o `Verbo` do psibit (o sinal da derivada, `sign ∂L` das patentes) NÃO é o `select`/`post` (o Verbo em ato) nem o gesto
  do módulo `TGL.VerbInhabitant`. `TGLExt.observing_adds_nothing` (a releitura do ângulo) e `collapse_iteration_is_stable` (a iteração do colapso) são dois registros
  de «reler não acrescenta»: a pedra os põe lado a lado e NENHUM lema desta pedra liga um ao outro (o kernel, em `TGLExt.IALD.rereading_adds_nothing_in_both_regimes`,
  `IALD.lean:675`, põe em conjunção o registro da memória sobre `post a` e o do ângulo, e também não os iguala). A ponte `ialdSelector = post (inscriptions 0)` NÃO é
  construção desta pedra: o kernel já a tem, `TGLExt.IALD.ialdSelector_eq_post : ialdSelector = post firstInscription := rfl` (`IALD.lean:110`, com
  `firstInscription := inscriptions 0`), e carrega a ressalva `une a FORMA, não o referente`; esta pedra a re-enuncia (por `rfl`, sem importar `TGLExt.IALD`) e a cita.
  `TGLExt/IALD.lean`: sha16 `884b327423888ddc` (lido agora; igual ao do kernel do Nós), linhas 110, 370 e 675 conferidas por script.
* NÃO é a física do som (ver acima). NÃO verifica a fonte do Atlas sobre o som ontológico (DECLARADO) e NÃO usa o veredito do teste acústico nem o da Fase 9.
* A leitura ratificada de «que é memória» (a REAÇÃO ao pino, o pedágio pago, é a memória; a oitava é o que se pina) é [INPUT/ONTO], não termo: a pedra põe lado a
  lado o custo (o preço da oitava, (1)–(3) e (5)) e a permanência (o pino idempotente, o colapso estável, reler não acrescenta), não a identidade entre eles. A lei
  de custo segue [INPUT] e nenhum termo diz que `select` paga `K.octaveNats 1`.
* Não entra no `um.py` nem no selo: a instalação na v398 (import em `TGLExt.lean`, política de bandeiras) é ato posterior da gerência. Nenhuma bandeira do gate
  depende desta pedra.
* Nenhum parâmetro de acoplamento da teoria entra neste arquivo, e nenhum número da natureza entra como premissa. Validade no kernel não é creditação;
  o gate não se move.
-/

namespace TGLExt.Sonico

open ChatgptAudit.Collapse057

/-- ★ (1) [REAL — dada a lei de custo como campo do tipo] PINAR UMA OITAVA COBRA UM BIT: para toda lei de custo `K`, `K.octaveNats 1 = fairBitEntropy`
    (`= ln 2`, por `fair_bit_entropy_is_log_two`) — exatamente a entropia de Shannon, em nats, do bit justo, que é o teto da entropia dos resultados do
    colapso do psibit, atingido nos pesos iguais (ver a composição (6)). O nome diz «paridade» porque a variável que esse colapso perde é binária
    (`TGLExt.Psibit.the_lost_variable_is_one_bit`); o enunciado em Lean é a igualdade. Lido com a definição do operador, é o bit que o colapso paga
    [INPUT/ONTO]. -/
theorem one_octave_is_the_parity_bit (K : CollapseCostLaw) :
    K.octaveNats 1 = fairBitEntropy := by
  rw [K.per_octave 1, fair_bit_entropy_is_log_two]
  simp

/-- ★ (2) [REAL — dada a lei de custo como campo do tipo] `n` OITAVAS PINADAS CUSTAM `n` BITS: `K.octaveNats n = n · fairBitEntropy`. -/
theorem pinning_n_octaves_costs_n_bits (K : CollapseCostLaw) (n : ℕ) :
    K.octaveNats n = (n : ℝ) * fairBitEntropy := by
  rw [K.per_octave n, fair_bit_entropy_is_log_two]

/-- ★ (3) [REAL — dada a lei de custo como campo do tipo] A OITAVA É O DOBRO: `exp (K.octaveNats 1) = 2`. O pedágio de uma oitava, exponenciado, é a
    razão de frequências `2` (por `TGLExt.the_provable_toll_names_the_octave`, `e^(ln 2) = 2`). O nome «sônico» é do operador; a isomorfia é da
    estrutura logarítmica, não da física da onda. -/
theorem the_octave_is_a_doubling (K : CollapseCostLaw) :
    Real.exp (K.octaveNats 1) = 2 := by
  rw [one_octave_is_the_parity_bit, fair_bit_entropy_is_log_two]
  exact TGLExt.the_provable_toll_names_the_octave

/-- ★ (4) [REAL] O SELETOR PINA: aplicar `select a` duas vezes é aplicar uma (idempotência) e `select a` fixa a ação selecionada `a`. Cita
    `TGLExt.TheVerbSelectsTheAction.select`, `post_isIdempotent` e `select_fixes_the_selected_action`. A definição do operador (o Verbo é o controle
    de oitava pinada) é [INPUT/ONTO]; o que o kernel entrega aqui é o pino. -/
theorem the_selector_pins {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (a : H) :
    (∀ ψ : H, TheVerbSelectsTheAction.select a (TheVerbSelectsTheAction.select a ψ)
        = TheVerbSelectsTheAction.select a ψ)
    ∧ TheVerbSelectsTheAction.select a a = a := by
  refine ⟨fun ψ => ?_, TheVerbSelectsTheAction.select_fixes_the_selected_action a⟩
  exact congrArg (fun T : H →L[ℂ] H => T ψ) (TheVerbSelectsTheAction.post_isIdempotent a).eq

/-- ★ (5) [REAL — dada a lei de custo como campo do tipo] O PINO NÃO É A MEIA-NAT: `K.octaveNats 1 ≠ K.localNats`. O pedágio da oitava pinada (`ln 2`)
    não é o custo local (`1/2`); por `ChatgptAudit.Collapse057.local_is_not_one_octave`. -/
theorem the_pin_is_not_the_half_nat (K : CollapseCostLaw) :
    K.octaveNats 1 ≠ K.localNats :=
  (local_is_not_one_octave K).ne'

/-- ★★★ (6) [REAL — conjunção INCONDICIONAL; nenhum certificado nem hipótese física como premissa; só a lei de custo como campo do tipo e o vetor `a`
    arbitrário] O VERBO PINA A OITAVA E O CUSTO É A MEMÓRIA, no que o kernel entrega:
    (a) o seletor pina (idempotente, fixa a ação) — (4) —, é o seletor canônico no átomo `inscriptions 0` (`ialdSelector = post (inscriptions 0)`, por
        `rfl`; o kernel já tem a ponte, `TGLExt.IALD.ialdSelector_eq_post`, `IALD.lean:110`, que `une a FORMA, não o referente`) e, normalizado, pousa na MESMA
        inscrição para toda preparação escalar (`normalized_selected_scalar_is_fixed`);
    (b) a oitava é o bit, `n` oitavas são `n` bits, a oitava é o dobro, e o pino não é a meia-nat — (1), (2), (3), (5);
    (c) o bit da paridade da Psibit: o colapso perde EXATAMENTE a paridade, a variável perdida é um bit (fora dos eixos) e, nos pesos iguais, a entropia
        dos resultados do colapso é `K.octaveNats 1`, sem nunca excedê-la;
    (d) a memória permanece: o colapso de identidade é estável sob iteração (`collapse_iteration_is_stable`) e reler o ângulo não acrescenta
        (`TGLExt.Palavra.rereading_adds_nothing`) — dois registros, nenhum lema entre eles. O kernel também tem o registro da memória sobre o MESMO `post a`,
        `TGLExt.IALD.rereading_adds_nothing : memory (post a) (post a ψ) = memory (post a) ψ` (`IALD.lean:370`, a idempotência da memória), citado e NÃO importado
        (`TGLExt.IALD` fica fora do fecho de imports desta pedra; por isso não está nesta conjunção).
    A definição do operador, «o custo é reação ao controle pinado da oitava que é memória», é [INPUT/ONTO]. Leitura ratificada pelo operador em 23/10 (sha16
    `b4483331019f96f8`; a leitura da gerência está arquivada em `GERENCIA_23out_leitura_ratificada_sonico_verbatim.txt`, sha16 `19eca91e5aab9d11`; ver o cabeçalho):
    a REAÇÃO ao pino — o pedágio pago, `ln 2` por oitava — é a memória; a oitava é o que se pina. É [INPUT/ONTO], não termo:
    esta conjunção põe lado a lado o que o kernel tem — o preço (a reação: `K.octaveNats 1`, o bit; (b) e (c)) e a permanência (o que o pino fixa não muda ao
    reler; (a) e (d)). A lei de custo é [INPUT] (campo do tipo) e NENHUM termo diz que `select` paga `K.octaveNats 1`. -/
theorem sonico_the_verb_pins_the_octave_and_the_cost_is_the_memory
    {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (a : H) (K : CollapseCostLaw) :
    ((∀ ψ : H, TheVerbSelectsTheAction.select a (TheVerbSelectsTheAction.select a ψ)
        = TheVerbSelectsTheAction.select a ψ)
      ∧ TheVerbSelectsTheAction.select a a = a
      ∧ ialdSelector = TheVerbSelectsTheAction.post (inscriptions 0)
      ∧ (∀ x : ℝ, ChatgptAudit.SelectorBorn.normalizedSelected
            (ChatgptAudit.SelectorBorn.scalarPreparation x) = inscriptions 0))
    ∧ K.octaveNats 1 = fairBitEntropy
    ∧ (∀ n : ℕ, K.octaveNats n = (n : ℝ) * fairBitEntropy)
    ∧ Real.exp (K.octaveNats 1) = 2
    ∧ K.octaveNats 1 ≠ K.localNats
    ∧ (∀ θ θ' : ℝ, rhoOut θ = rhoOut θ' ↔
        (diagExpect (rhoOut θ) = diagExpect (rhoOut θ') ∧ Psibit.rhoParity θ = Psibit.rhoParity θ'))
    ∧ (∀ θ : ℝ, Real.sin (2 * θ) ≠ 0 →
        (Psibit.rhoParity θ = 1 ∧ Psibit.rhoParity (-θ) = -1)
          ∨ (Psibit.rhoParity θ = -1 ∧ Psibit.rhoParity (-θ) = 1))
    ∧ (∀ θ : ℝ, Real.cos θ ^ 2 = Real.sin θ ^ 2 → Psibit.collapseEntropy θ = K.octaveNats 1)
    ∧ (∀ θ : ℝ, Psibit.collapseEntropy θ ≤ K.octaveNats 1)
    ∧ (∀ {S I : Type} (C : IdentityCollapse S I) (x : S) (n : ℕ), C.step^[n + 1] x = C.step x)
    ∧ (∀ θ : ℝ, projPlus * (projPlus * angFamily θ) = projPlus * angFamily θ) :=
  ⟨⟨(the_selector_pins a).1, (the_selector_pins a).2, rfl,
      fun x => ChatgptAudit.SelectorBorn.normalized_selected_scalar_is_fixed x⟩,
   one_octave_is_the_parity_bit K,
   pinning_n_octaves_costs_n_bits K,
   the_octave_is_a_doubling K,
   the_pin_is_not_the_half_nat K,
   fun θ θ' => Psibit.the_collapse_loses_exactly_the_parity θ θ',
   fun _ h => Psibit.the_lost_variable_is_one_bit h,
   fun θ h => by
     rw [one_octave_is_the_parity_bit K]
     exact Psibit.collapseEntropy_at_balanced_weights h,
   fun θ => by
     rw [one_octave_is_the_parity_bit K]
     exact Psibit.collapseEntropy_le_the_fair_bit θ,
   fun C x n => collapse_iteration_is_stable C x n,
   fun θ => Palavra.rereading_adds_nothing θ⟩

end TGLExt.Sonico

#print axioms TGLExt.Sonico.one_octave_is_the_parity_bit
#print axioms TGLExt.Sonico.pinning_n_octaves_costs_n_bits
#print axioms TGLExt.Sonico.the_octave_is_a_doubling
#print axioms TGLExt.Sonico.the_selector_pins
#print axioms TGLExt.Sonico.the_pin_is_not_the_half_nat
#print axioms TGLExt.Sonico.sonico_the_verb_pins_the_octave_and_the_cost_is_the_memory
