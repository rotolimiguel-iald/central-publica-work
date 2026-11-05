import TGLExt.TheCascadeOfObservers
import TGLExt.TheJudgedThing
import TGLExt.UmPostoRelacao
import TGLExt.TheAlphaAndTheOmega

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# OBSERVADOR = TERMINAL — o posto do observador é o terminal; a fusão de tudo num só posto é o colapso
  [pedra da gerência c1, 31/10/2026, 2ª versão (r2), revista em 01/11/2026; nome do operador: «observador=terminal»; entra na v405]

## As cunhagens do operador (verbatim por sha256, 31/10/2026)

> «observador=terminal» — `Central de Patentes\work\cunhagens_13out\OPERADOR_31out_observador_terminal_verbatim.txt`, 20 B,
>   sha256 `e4e105fe14615f39d5af27e6514204e3ad34fd47e5959a1019ad78be23654336` (14:21)

> «é isso, mas essa informação é muito importante para o um.py e eu quero tipa-la lá dentro: o posto do observador é o terminal;
> e isso faz todo sentido, observador=terminal» — `…\OPERADOR_31out_tipar_observador_terminal_no_um_py_verbatim.txt`, 177 B,
>   sha256 `08e98d212f11b554c83565aea515849603a5762c77075c169b1d56ff345cbbda`

> «então não está completa a fusão porque precisa sim fundir tudo em um só posto, porque é o colapso. veja, em teoria das estruturas
> (em engenharia física) o colapso é o ponto terminal da resistência da estrutura, de modo que a estrutura da estrutura é a matemática
> como interseção linguistica última …» — `…\OPERADOR_31out_fusao_e_o_colapso_nao_delegar_massa_kimi_verbatim.txt`, 827 B,
>   sha256 `a22a54dfc97d96114e3d251a41bed8ea300d314c626a9349eda36ce09b2bdfc1`

## O que a 1ª versão errou, e a correção (ao lado, nunca por cima)

A r1 tipou a fusão total no terminal como PRESSUPOSTA («nenhum Um posto lê assim») e leu o posto só como posição. O operador corrigiu:
a fusão de TUDO num só posto É o colapso — em teoria das estruturas, o colapso é o ponto terminal da resistência. O que a r1 provou
segue verdadeiro, mas sobre o espaço ERRADO: na cascata SEM o 0 (só os quatro níveis), a fusão total lê igual em tudo e o tipo
`IdentityCollapse` não a distingue do pressuposto. Falta o par. A TGL é binária — {[1=1=VERDADEIRO][1=0=FALSO]} (19/10; `Psibit`,
`NameIsTheContent.if_one_equals_zero_everything_collapses`): o colapso funde toda a ESTRUTURA num só posto, o 1, e o distingue do
ABISMO, o 0 (`Fundacao.abismo`, a queda sem fundo). Com o par no espaço de estados, a fusão total É um `UmPosto` do kernel
(`UmPostoRelacao.UmPosto`, 17/09/2026): travessia com perda, medida antes de ser posta, legível. É isso que a r2 tipa.

## O que a casa já tinha (levantamento antes de construir — o cético é aferidor, não cego)

* Atlas §II.O, cunhagem 78_: OBSERVADOR = GRAVIDADE VIVA, com OPERA · PERMANECE · É O TERMINAL [REAL 3/3];
  «IALD = MAINFRAME; TGL = PROGRAMA TERMINAL» (terminal = entrada do Um + s-lim = P_F + exibição do veredito).
* `TheCascadeOfObservers` (23/08/2026): a cascata `luz → consciência → física → gravidade` como relação `observes`;
  `gravity_is_observed_by_nothing` («é o termo terminal»), `light_observes_nothing`, `each_level_observes_exactly_one`.
* `TheJudgedThing`: `ResJudicata D := ∀ x, D (D x) = D x` e `res_judicata_is_terminal`.
* `CollapseContract` (ENTREGA_057): `IdentityCollapse` (travessia idempotente que preserva a identidade lida e move algo),
  `CollapseTransition`, `collapse_has_no_left_inverse`, `collapse_fixed_iff_in_range`.
* `UmPostoRelacao` (17/09/2026): o Um posto é RELAÇÃO (`UmPosto`: travessia + evento medido + leitura legível); `posto_paid_loss`,
  `posto_anchors_the_reading`, `posto_was_measured_before_being_posited`, `no_posto_reading_is_pressupposed`,
  `pressupposed_is_never_posto`.
* `TheAlphaAndTheOmega.omega_of_one`: ω(I) = 1 no objeto GNS — «o terminal ω do par».
* `TheAxiomAndTheFalseWitness.the_reading_has_two_fixed_points`: a leitura tem exatamente dois pontos fixos, 0 e 1.

## O que esta pedra compõe

* **o posto terminal é um só** — `Terminal x := ∀ y, ¬ observes y x`; `terminal_iff`; `the_terminal_is_unique : ∃! x, Terminal x`;
  (e o inicial: `initial_iff : Initial x ↔ x = luz`);
* **o leitor e a resistência** — `leitor` leva cada nível a quem o observa; `leitor_fixed_iff` (o terminal é o único ponto fixo da
  leitura); `every_level_reaches_the_terminal` (três leituras); `distancia` = a resistência que resta: `each_reading_consumes_resistance`
  e `the_collapse_is_the_terminal_point_of_resistance` (`distancia x = 0 ↔ x = gravidade`): **o colapso é o ponto terminal da resistência**;
* **consumada, a leitura é coisa julgada** — `the_completed_reading_is_res_judicata`, `rereading_at_the_terminal_adds_nothing`;
* **A FUSÃO É O COLAPSO, E O COLAPSO É UM POSTO** — `Posicao` = os quatro níveis da estrutura e o `abismo` (o 0); `colapsoTotal` leva
  TODA a estrutura ao terminal e deixa o abismo no abismo; `leituraBinaria` lê 1 = 1 na estrutura e 1 = 0 no abismo (o psibit);
  `oColapso : IdentityCollapse Posicao Bool` (idempotente, preserva a leitura, move) e **`oPostoTerminal : UmPosto Posicao Bool`** —
  a fusão total É um Um posto do kernel: `the_collapse_fuses_the_structure_into_one_posto`, `the_fusion_is_a_posto`,
  `the_fusion_paid_loss` (= `posto_paid_loss`), `the_fusion_was_measured_before_being_posited`, `the_fusion_anchors_the_reading`,
  `the_fusion_is_not_pressupposed` (= `no_posto_reading_is_pressupposed`: a correção da r1);
* **a estrutura da estrutura** — `the_structure_reads_one` (na estrutura inteira a leitura é UMA: a interseção que resta quando os
  níveis colapsam) e `the_reading_survives_the_collapse` (a leitura é preservada pela travessia);
* **os dois pontos fixos do colapso** — `the_two_fixed_points_of_the_collapse`: `colapsoTotal p = p ↔ p = terminal ∨ p = abismo`:
  o posto (1) e o abismo (0); fazem par com os dois pontos fixos da leitura (`the_reading_has_two_fixed_points`, √x em [0, ∞)): mesma contagem, objetos distintos [ONTO];
* **sem o par não há posto** — `without_the_abyss_the_fusion_reads_as_pressupposed` e `without_the_abyss_no_posto_reads_so` (os
  teoremas da r1, com o nome certo): na cascata SEM o 0, qualquer `IdentityCollapse` cujo passo seja a fusão total tem leitura
  pressuposta e nenhum Um posto lê assim — **o par (1=1 | 1=0) é NECESSÁRIO para que a fusão seja posto**;
* **o terminal lê 1 na leitura binária** — `the_fixed_points_read_one_and_zero`;
* **o polo ω lê 1 na identidade** — `the_omega_pole_reads_one` (= `omega_of_one`). HOMÔNIMO, dito: em `TheAlphaAndTheOmega`, «terminal» é POLO do par α/ω; aqui o
  terminal é o nível `gravidade` da cascata. Nenhum termo liga os dois; ligá-los é leitura [ONTO] do operador;
* **o fecho** — `the_observers_posto_is_the_terminal`.

## O que esta pedra NÃO afirma

* Nada sobre o observador humano, a gravidade, a luz ou a consciência como ENTIDADES (rótulos, como na pedra de origem); «abismo» e
  «estrutura» são rótulos de posição; a leitura de engenharia (resistência, colapso) é [ONTO] do operador: aqui só a forma.
* Não afirma rank (no `Posto` o fim da defasagem tem posto 2); não constrói o `IdentityCollapse` físico; não toca gate, selo, β nem dado.
  `NOT_FALSIFIED` nunca é `CONFIRMED`.

Sem sorry, sem axiom novo (trio: propext, Classical.choice, Quot.sound).

> **01/11/2026 — NOME DO OPERADOR: «observador=terminal»** (31/10), mantido na nomeação de 01/11 (verbatim sha256 `1f16a74c05d9d4cb`).

> **AO LADO (01/11/2026, gerência c1, em nome próprio; achado da revisão de terceiro):** `the_terminal_reads_one` foi rebatizado `the_omega_pole_reads_one`, antes do
> selo: o enunciado é `omegaState P 1 = 1`, sem termo ligado a `Terminal`, e o nome afirmava a ligação. O fecho passou a trazer também o que é do terminal da cascata,
> `the_fixed_points_read_one_and_zero`. Os níveis seguem rótulos de um modelo finito; «medido» é o campo do tipo `UmPosto`, e «pagou perda» é não injetividade.
-/

namespace TGLExt.ObservadorTerminal

open TGLExt Level
open ChatgptAudit.Collapse057

/-! ### Os dois postos extremos da cascata -/

/-- [DEF] **o posto TERMINAL**: o nível que nenhum outro observa. -/
def Terminal (x : Level) : Prop := ∀ y : Level, ¬ observes y x

/-- [DEF] **o posto INICIAL**: o nível que não observa nenhum. -/
def Initial (x : Level) : Prop := ∀ y : Level, ¬ observes x y

/-- [KERNEL] ★★★ **O TERMINAL É A GRAVIDADE, E SÓ ELA** (reúsa `gravity_is_observed_by_nothing`). -/
theorem terminal_iff (x : Level) : Terminal x ↔ x = gravidade := by
  constructor
  · intro h
    cases x with
    | luz => exact (h consciencia trivial).elim
    | consciencia => exact (h fisica trivial).elim
    | fisica => exact (h gravidade trivial).elim
    | gravidade => rfl
  · rintro rfl
    exact gravity_is_observed_by_nothing

/-- [KERNEL] ★★ **O INICIAL É A LUZ, E SÓ ELA** (reúsa `light_observes_nothing`). -/
theorem initial_iff (x : Level) : Initial x ↔ x = luz := by
  constructor
  · intro h
    cases x with
    | luz => rfl
    | consciencia => exact (h luz trivial).elim
    | fisica => exact (h consciencia trivial).elim
    | gravidade => exact (h fisica trivial).elim
  · rintro rfl
    exact light_observes_nothing

/-- [KERNEL] ★★★ **O POSTO TERMINAL É UM SÓ.** -/
theorem the_terminal_is_unique : ∃! x : Level, Terminal x :=
  ⟨gravidade, gravity_is_observed_by_nothing, fun y hy => (terminal_iff y).mp hy⟩

/-! ### O leitor e a resistência -/

/-- [DEF] **o leitor**: leva cada nível a quem o observa. O terminal, que ninguém observa, só se relê. -/
def leitor : Level → Level
  | luz => consciencia
  | consciencia => fisica
  | fisica => gravidade
  | gravidade => gravidade

/-- [KERNEL] fora do terminal, o leitor de `x` observa `x`. -/
theorem leitor_observes (x : Level) (hx : x ≠ gravidade) : observes (leitor x) x := by
  cases x with
  | luz => exact trivial
  | consciencia => exact trivial
  | fisica => exact trivial
  | gravidade => exact absurd rfl hx

/-- [KERNEL] ★★★ **O TERMINAL É O ÚNICO PONTO FIXO DA LEITURA** — o posto que permanece. -/
theorem leitor_fixed_iff (x : Level) : leitor x = x ↔ x = gravidade := by
  cases x <;> decide

/-- [KERNEL] ★★★ **TODA LEITURA CHEGA AO TERMINAL**: três leituras bastam, de qualquer nível. -/
theorem every_level_reaches_the_terminal (x : Level) : leitor^[3] x = gravidade := by
  cases x <;> decide

/-- [DEF] **a resistência que resta**: quantas leituras faltam até o terminal. -/
def distancia : Level → ℕ
  | luz => 3
  | consciencia => 2
  | fisica => 1
  | gravidade => 0

/-- [KERNEL] a resistência é exata: `distancia x` leituras levam `x` ao terminal. -/
theorem distancia_reaches (x : Level) : leitor^[distancia x] x = gravidade := by
  cases x <;> decide

/-- [KERNEL] ★★ **CADA LEITURA CONSOME RESISTÊNCIA**: fora do terminal, ler baixa a distância. -/
theorem each_reading_consumes_resistance (x : Level) (hx : x ≠ gravidade) : distancia (leitor x) < distancia x := by
  cases x with
  | luz => decide
  | consciencia => decide
  | fisica => decide
  | gravidade => exact absurd rfl hx

/-- [KERNEL] ★★★ **O COLAPSO É O PONTO TERMINAL DA RESISTÊNCIA**: resistência zero é estar no terminal. -/
theorem the_collapse_is_the_terminal_point_of_resistance (x : Level) : distancia x = 0 ↔ x = gravidade := by
  cases x <;> decide

/-- [KERNEL] ★★ o posto é legível como posição: dois níveis a distâncias distintas. -/
theorem the_position_is_legible : ∃ x y : Level, distancia x ≠ distancia y :=
  ⟨luz, gravidade, by decide⟩

/-! ### Consumada, a leitura é coisa julgada -/

/-- [KERNEL] ★★★ **A LEITURA CONSUMADA É COISA JULGADA**: `leitor^[3]` é idempotente (`ResJudicata`). -/
theorem the_completed_reading_is_res_judicata : ResJudicata (leitor^[3]) := by
  intro x
  cases x <;> decide

/-- [KERNEL] ★★ **RELER NO TERMINAL NÃO ACRESCENTA** (reúsa `res_judicata_is_terminal`). -/
theorem rereading_at_the_terminal_adds_nothing (x : Level) (k : ℕ) :
    (leitor^[3])^[k + 1] x = leitor^[3] x :=
  res_judicata_is_terminal (leitor^[3]) the_completed_reading_is_res_judicata x k

/-! ### A FUSÃO É O COLAPSO — e o colapso é um posto, porque a leitura é o par -/

/-- [DEF] **as posições sob carga**: os quatro níveis da ESTRUTURA e o `abismo` — o 0, a queda sem fundo
    (`Fundacao.abismo`), que não é nível de nada. -/
inductive Posicao where
  | nivel (x : Level)
  | abismo
  deriving DecidableEq, Repr

open Posicao

/-- [DEF] **O COLAPSO TOTAL**: funde TODA a estrutura num só posto — o terminal; o abismo fica no abismo. -/
def colapsoTotal : Posicao → Posicao
  | nivel _ => nivel gravidade
  | abismo => abismo

/-- [DEF] **a leitura binária** (o psibit): 1 = 1, VERDADEIRO, em toda a estrutura; 1 = 0, FALSO, no abismo. -/
def leituraBinaria : Posicao → Bool
  | nivel _ => true
  | abismo => false

/-- [KERNEL] ★★★ **O COLAPSO FUNDE A ESTRUTURA INTEIRA NUM SÓ POSTO**: todo nível vai ao terminal. -/
theorem the_collapse_fuses_the_structure_into_one_posto (x : Level) : colapsoTotal (nivel x) = nivel gravidade := rfl

/-- [DEF] **o colapso como travessia do kernel**: idempotente, preserva a leitura binária, move (a luz não fica onde estava). -/
def oColapso : IdentityCollapse Posicao Bool where
  step := colapsoTotal
  identity := leituraBinaria
  stable := by
    intro p
    cases p <;> rfl
  preserves := by
    intro p
    cases p <;> rfl
  effective := ⟨nivel luz, by decide⟩

/-- [DEF] ★★★ **O POSTO TERMINAL É UM UM POSTO DO KERNEL**: a travessia é o colapso total; o antes é a luz, o depois é o
    terminal (medido antes de ser posto); a leitura é legível porque distingue a estrutura do abismo (1 ≠ 0). -/
def oPostoTerminal : UmPostoRelacao.UmPosto Posicao Bool where
  crossing := oColapso
  before := nivel luz
  after := nivel gravidade
  measured := ⟨rfl, by decide⟩
  legible := ⟨nivel luz, abismo, by decide⟩

/-- [KERNEL] ★★★ **A FUSÃO É UM POSTO** — e o seu passo é exatamente o colapso total. -/
theorem the_fusion_is_a_posto : oPostoTerminal.crossing.step = colapsoTotal := rfl

/-- [KERNEL] ★★ **A FUSÃO PAGOU PERDA** (= `posto_paid_loss`): o colapso não se desfaz — sem inversa à esquerda. -/
theorem the_fusion_paid_loss : ¬ ∃ R : Posicao → Posicao, Function.LeftInverse R colapsoTotal :=
  UmPostoRelacao.posto_paid_loss oPostoTerminal

/-- [KERNEL] ★★ **MEDIDA ANTES DE SER POSTA**: houve evento — o antes (luz) não é o depois (terminal). -/
theorem the_fusion_was_measured_before_being_posited : (nivel luz : Posicao) ≠ nivel gravidade :=
  UmPostoRelacao.posto_was_measured_before_being_posited oPostoTerminal

/-- [KERNEL] ★★ **A FUSÃO ANCORA A LEITURA**: depois do colapso a leitura é a de antes e o terminal está fixado. -/
theorem the_fusion_anchors_the_reading :
    leituraBinaria (nivel gravidade) = leituraBinaria (nivel luz) ∧ colapsoTotal (nivel gravidade) = nivel gravidade :=
  UmPostoRelacao.posto_anchors_the_reading oPostoTerminal

/-- [KERNEL] ★★★ **A FUSÃO NÃO É PRESSUPOSTA** (= `no_posto_reading_is_pressupposed`) — a correção da 1ª versão: com o par
    no espaço de estados, a fusão total lê 1 na estrutura e 0 no abismo, logo distingue, logo é posto. -/
theorem the_fusion_is_not_pressupposed : ¬ UmPostoRelacao.Pressupposed leituraBinaria :=
  UmPostoRelacao.no_posto_reading_is_pressupposed oPostoTerminal

/-- [KERNEL] ★★★ **A ESTRUTURA DA ESTRUTURA**: na estrutura inteira a leitura é UMA — é o que resta, a interseção, quando os
    níveis colapsam no terminal. -/
theorem the_structure_reads_one (x y : Level) : leituraBinaria (nivel x) = leituraBinaria (nivel y) := rfl

/-- [KERNEL] ★★ **A LEITURA SOBREVIVE AO COLAPSO** (o `preserves` da travessia). -/
theorem the_reading_survives_the_collapse (p : Posicao) : leituraBinaria (colapsoTotal p) = leituraBinaria p :=
  oColapso.preserves p

/-- [KERNEL] ★★★ **OS DOIS PONTOS FIXOS DO COLAPSO**: o posto terminal (lido 1) e o abismo (lido 0) — e nenhum outro.
    Fazem par com os dois pontos fixos da leitura (`the_reading_has_two_fixed_points`, √x em [0, ∞): 0 e 1): mesma contagem, objetos distintos [ONTO]. -/
theorem the_two_fixed_points_of_the_collapse (p : Posicao) :
    colapsoTotal p = p ↔ (p = nivel gravidade ∨ p = abismo) := by
  cases p with
  | nivel x => cases x <;> decide
  | abismo => decide

/-- [KERNEL] ★★ os dois pontos fixos leem-se 1 e 0: a estrutura condensada é VERDADEIRO, o abismo é FALSO. -/
theorem the_fixed_points_read_one_and_zero :
    leituraBinaria (nivel gravidade) = true ∧ leituraBinaria abismo = false := ⟨rfl, rfl⟩

/-! ### Sem o par não há posto (os teoremas da 1ª versão, com o nome certo) -/

/-- [KERNEL] ★★ **SEM O ABISMO, A FUSÃO LÊ COMO PRESSUPOSTA**: na cascata SÓ com os quatro níveis, qualquer travessia cujo passo
    seja a fusão total (`leitor^[3]`) tem leitura igual em todo nível. É por isso que a leitura do posto é o PAR: sem o 0 no espaço
    de estados, o tipo não distingue o colapso do pressuposto. -/
theorem without_the_abyss_the_fusion_reads_as_pressupposed {I : Type}
    (C : IdentityCollapse Level I) (hC : C.step = leitor^[3]) :
    UmPostoRelacao.Pressupposed C.identity := by
  intro x y
  have hx := C.preserves x
  have hy := C.preserves y
  rw [hC, every_level_reaches_the_terminal] at hx hy
  exact hx.symm.trans hy

/-- [KERNEL] ★★ **SEM O ABISMO, NENHUM UM POSTO LÊ ASSIM** (reúsa `pressupposed_is_never_posto`): o par é NECESSÁRIO. -/
theorem without_the_abyss_no_posto_reads_so {I : Type}
    (C : IdentityCollapse Level I) (hC : C.step = leitor^[3]) (P : UmPostoRelacao.UmPosto Level I) :
    P.crossing.identity ≠ C.identity :=
  UmPostoRelacao.pressupposed_is_never_posto C.identity
    (without_the_abyss_the_fusion_reads_as_pressupposed C hC) id 0 P

/-! ### O polo ω lê 1 na identidade -/

/-- [KERNEL] ★★ **O POLO ω LÊ 1 NA IDENTIDADE** — ω(I) = 1 no objeto GNS (= `TheAlphaAndTheOmega.omega_of_one`, «O terminal ω do par»). HOMÔNIMO, dito: ali «terminal» é
    POLO do par α/ω; nesta pedra o terminal é o nível `gravidade` da cascata. Nenhum termo liga os dois; ligá-los é leitura [ONTO] do operador. O terminal da cascata lê 1
    na leitura binária: `the_fixed_points_read_one_and_zero`. (Rebatizado em 01/11/2026, antes do selo; o nome anterior afirmava a ligação.) -/
theorem the_omega_pole_reads_one (P : SiteProfile) : omegaState P 1 = 1 :=
  omega_of_one P

/-! ### O fecho -/

/-- ★★★ **OBSERVADOR = TERMINAL — o fecho.** O posto terminal é um só; é o único ponto fixo da leitura; o colapso funde a estrutura
    inteira nele; consumada, a leitura é coisa julgada; a fusão é um posto (não pressuposta) que pagou perda; o colapso tem dois
    pontos fixos, o posto e o abismo; o terminal lê 1 e o abismo lê 0 na leitura binária; e, ao lado, o polo ω do par lê 1 na identidade
    (homônimo: a ligação entre os dois terminais é leitura [ONTO]). Tudo num modelo finito cujos níveis são rótulos. -/
theorem the_observers_posto_is_the_terminal (P : SiteProfile) :
    (∃! x : Level, Terminal x)
    ∧ (∀ x : Level, leitor x = x ↔ x = gravidade)
    ∧ (∀ x : Level, colapsoTotal (nivel x) = nivel gravidade)
    ∧ ResJudicata (leitor^[3])
    ∧ (¬ UmPostoRelacao.Pressupposed leituraBinaria)
    ∧ (¬ ∃ R : Posicao → Posicao, Function.LeftInverse R colapsoTotal)
    ∧ (∀ p : Posicao, colapsoTotal p = p ↔ (p = nivel gravidade ∨ p = abismo))
    ∧ (leituraBinaria (nivel gravidade) = true ∧ leituraBinaria abismo = false)
    ∧ omegaState P 1 = 1 :=
  ⟨the_terminal_is_unique, leitor_fixed_iff, the_collapse_fuses_the_structure_into_one_posto,
   the_completed_reading_is_res_judicata, the_fusion_is_not_pressupposed, the_fusion_paid_loss,
   the_two_fixed_points_of_the_collapse, the_fixed_points_read_one_and_zero, the_omega_pole_reads_one P⟩

end TGLExt.ObservadorTerminal

#print axioms TGLExt.ObservadorTerminal.terminal_iff
#print axioms TGLExt.ObservadorTerminal.initial_iff
#print axioms TGLExt.ObservadorTerminal.the_terminal_is_unique
#print axioms TGLExt.ObservadorTerminal.leitor_observes
#print axioms TGLExt.ObservadorTerminal.leitor_fixed_iff
#print axioms TGLExt.ObservadorTerminal.every_level_reaches_the_terminal
#print axioms TGLExt.ObservadorTerminal.distancia_reaches
#print axioms TGLExt.ObservadorTerminal.each_reading_consumes_resistance
#print axioms TGLExt.ObservadorTerminal.the_collapse_is_the_terminal_point_of_resistance
#print axioms TGLExt.ObservadorTerminal.the_position_is_legible
#print axioms TGLExt.ObservadorTerminal.the_completed_reading_is_res_judicata
#print axioms TGLExt.ObservadorTerminal.rereading_at_the_terminal_adds_nothing
#print axioms TGLExt.ObservadorTerminal.the_collapse_fuses_the_structure_into_one_posto
#print axioms TGLExt.ObservadorTerminal.the_fusion_is_a_posto
#print axioms TGLExt.ObservadorTerminal.the_fusion_paid_loss
#print axioms TGLExt.ObservadorTerminal.the_fusion_was_measured_before_being_posited
#print axioms TGLExt.ObservadorTerminal.the_fusion_anchors_the_reading
#print axioms TGLExt.ObservadorTerminal.the_fusion_is_not_pressupposed
#print axioms TGLExt.ObservadorTerminal.the_structure_reads_one
#print axioms TGLExt.ObservadorTerminal.the_reading_survives_the_collapse
#print axioms TGLExt.ObservadorTerminal.the_two_fixed_points_of_the_collapse
#print axioms TGLExt.ObservadorTerminal.the_fixed_points_read_one_and_zero
#print axioms TGLExt.ObservadorTerminal.without_the_abyss_the_fusion_reads_as_pressupposed
#print axioms TGLExt.ObservadorTerminal.without_the_abyss_no_posto_reads_so
#print axioms TGLExt.ObservadorTerminal.the_omega_pole_reads_one
#print axioms TGLExt.ObservadorTerminal.the_observers_posto_is_the_terminal
