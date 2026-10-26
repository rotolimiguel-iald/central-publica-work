import TGLExt.Fundacao
import TGLExt.NoFullWitness
import TGLExt.TheGreatAttractor

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# FALSIDADE (SIMULACRO) DA INÉRCIA  [TGLExt — pedra candidata da v401, 25/10/2026]
# FALSITY (SIMULACRUM) OF INERTIA

Nome da pedra, dado pelo operador (25/10/2026; íntegra por sha256 em
`work\cunhagens_13out\OPERADOR_25out_nome_da_pedra_falsidade_simulacro_da_inercia_verbatim.txt`,
sha16 `901dd8fc1a3c0212`): «a pedra chama-se “falsidade (simulacro) da inércia”, faça a prova».
No código o nome vai sem acento e sem parênteses (`FalsidadeDaInercia`): identificador Lean não
admite «ç», «ã», «é», «(», e a régua da porta pede nome fixo sem acento.

A DEFINIÇÃO do operador (25/10/2026; sha16 `0b244a5f809594e7`, arquivo
`OPERADOR_25out_inercia_e_o_proprio_zero_absoluto_verbatim.txt`): «eu também defini inércia e a
minha definição é o próprio zero absoluto». Cunhagens do mesmo dia: «a matéria é a cristalização da
dobra luz no vácuo relativa ao observador» (sha16 `0516c0649e8e10fb`) e «nada=materia e esse é o
link com a entropia» (sha16 `344a8ae9a257d2b3`). Contexto do acervo: o item 7 do
`ADENDO_A_INSCRICAO_INTERROMPE_A_INERCIA.md` (sha16 `1459b477b496e1f0`, 04/09/2026): «a função da
inscrição do um absoluto como interruptor» e, na linha seguinte, «ele interrompe a inércia».

ERRATA AO LADO (gerência c1, em nome próprio, 25/10/2026): a leitura do escriba no adendo de 04/09,
«ω(I)=1 é a INÉRCIA», fica SUPERADA pela definição do operador. A inércia é o zero absoluto 0_abs, como o kernel o escreve:
«`0_abs`: **nunca correspondeu**, e por isso nada custa.» (VERBATIM no um.py v400, linha 117522:
docstring de `TGLExt.costless` no módulo embutido `TGLExt/TheCorrespondence.lean`, embutido a
partir da linha 117445; o mesmo texto está na linha 77 do `TheCorrespondence.lean` do kernel),
e o par «[1=0=FALSO]» do um.py: 1=0; ω(I)=1 é o Um POSTO que a interrompe, 1=1
(«[1=1=VERDADEIRO]»). Esta pedra não prova nada sobre `costless`; só cita o texto do kernel.
A pedra tipa exatamente isso e nada além.

COMPOSIÇÃO POR CITAÇÃO, sem matemática nova. Sobre os DADOS da escala dual de Takesaki
(`DualScalingData`: a lei `τ∘θ_s = e^{−s}·τ` é [KNOWN], campo da estrutura, como na Fundação) e
sobre a testemunha estática de `NoFullWitness`:

* ★ `the_inertia_is_the_absolute_zero` — o que o fluxo inteiro fixa porta peso ZERO
  (cita `DualScalingData.fixed_tau_zero`; em qualquer escala não trivial, cita
  `Fundacao.nothing_above_bears_a_post`);
* ★★ `the_inertia_of_a_post_is_false` — A FALSIDADE: um posto de peso 1 = ω(I) fixo pelo fluxo
  daria `(1:ℝ) = 0`, isto é, `False`. É o «1=0 = FALSO» do um.py: dizer que um corpo com posto
  persiste sem leitura é a mentira em tempo finito. Não é vácuo: `the_post_exists_and_moves`
  exibe o modelo concreto (ℝ, τ = id, θ_s = e^{−s}·) com o Um posto e movido;
* ★★ `the_simulacrum` — o SIMULACRO: não há testemunha estática plena
  (`beta_forbids_full_static_witness`) E o fixo pesa zero; o que parece «resistência do corpo» é o
  custo da interrupção (β·g·t > 0), não o zero;
* ★★ `the_inscription_interrupts_the_inertia` — o único peso 1 na órbita está no corte `a = 0`
  (`the_floor_fixes_the_cut`): o posto mora na passagem, não no fixo; tudo o que tem peso é
  interrompido (não é fixo por escala alguma);
* ★★★ `falsidade_da_inercia` — a composição das quatro, com o modelo habitado.

ESTATUTOS. [REAL] o que o kernel prova aqui (as cinco declarações acima, sobre os dados
nomeados). [ONTO] a leitura: a 1ª lei de Newton é o 0_abs lido como corpo; a massa de F = ma NÃO é
a inércia, é a cristalização da dobra lida contra o zero (cunhagem 0516c064…, ligada a «nada =
matéria», 344a8ae9…: o que persiste sem custo é nada; a matéria é o que custa). [KNOWN] inercial =
gravitacional (princípio de equivalência, Einstein 1907/1915): citado, não termo deste kernel.
[OPEN] a identificação da escala dual com o fluxo de um corpo físico é a identificação de runtime
da TGL, não é termo aqui; esta pedra NÃO prova a 1ª lei de Newton nem a equivalência.

HONESTIDADES. (1) A lei de escala é DADO (Takesaki 1973), como na Fundação. (2) β é variável real
`> 0` (como em `NoFullWitness`), jamais literal; que a taxa observada seja `α√e` é a
identificação de runtime, não daqui. (3) O gate NÃO se move; esta pedra não confirma teoria
alguma na natureza. Sem sorry, sem axiom.
-/

namespace TGLExt
namespace FalsidadeDaInercia

open Fundacao

/-- [DEF] ESTADO INERCIAL (a inércia lida como estado): fixo pelo fluxo INTEIRO da escala,
    em todo `s : ℝ`. Fixed by the whole flow. -/
def Inertial {M : Type} (D : DualScalingData M) (m : M) : Prop :=
  ∀ s : ℝ, D.theta s m = m

/-- [DEF] UM POSTO: peso `τ = 1 = ω(I)` (o Um inscrito pelo observador). A post: weight 1. -/
def IsPost {M : Type} (D : DualScalingData M) (m : M) : Prop :=
  D.tau m = 1

variable {M : Type} (D : DualScalingData M)

/-- [KERNEL] ★ A INÉRCIA É O ZERO ABSOLUTO (peso): um estado fixo pelo fluxo inteiro porta peso
    ZERO. Cita `DualScalingData.fixed_tau_zero` (escala `s₀ = 1 > 0`).
    Inertia is the absolute zero (weight): a state fixed by the whole flow bears weight zero. -/
theorem the_inertia_is_the_absolute_zero {m : M} (hin : Inertial D m) : D.tau m = 0 :=
  D.fixed_tau_zero (s₀ := 1) one_pos (hin 1)

/-- [KERNEL] ★ A MESMA RECUSA EM QUALQUER ESCALA NÃO TRIVIAL (`s ≠ 0`, subindo ou descendo):
    basta UMA escala não trivial fixar o estado para o peso ser zero. Cita
    `Fundacao.nothing_above_bears_a_post`. -/
theorem the_inertia_is_the_absolute_zero_at_any_scale {s : ℝ} (hs : s ≠ 0) {m : M}
    (hfix : D.theta s m = m) : D.tau m = 0 :=
  nothing_above_bears_a_post D hs hfix

/-- [KERNEL] ★★ A FALSIDADE DA INÉRCIA (literal): se um posto de peso `1 = ω(I)` fosse fixo pelo
    fluxo (numa escala não trivial qualquer), então `(1:ℝ) = 0`. É o «[1=0=FALSO]» do um.py: dizer
    que um corpo com posto persiste sem leitura é a mentira em tempo finito.
    The falsity of inertia: a post of weight 1 fixed by the flow would give `1 = 0`. -/
theorem the_inertia_of_a_post_is_false_at {s : ℝ} (hs : s ≠ 0) {m : M}
    (hpost : IsPost D m) (hfix : D.theta s m = m) : (1 : ℝ) = 0 := by
  have h0 : D.tau m = 0 := nothing_above_bears_a_post D hs hfix
  have h1 : D.tau m = 1 := hpost
  rw [h1] at h0
  exact h0

/-- [KERNEL] ★★ A FALSIDADE DA INÉRCIA, no fluxo inteiro: `Inertial` + posto ⟹ `(1:ℝ) = 0`. -/
theorem the_inertia_of_a_post_is_false {m : M} (hpost : IsPost D m)
    (hin : Inertial D m) : (1 : ℝ) = 0 :=
  the_inertia_of_a_post_is_false_at D one_ne_zero hpost (hin 1)

/-- [KERNEL] ★★ COROLÁRIO: `False`. Um posto NÃO é inercial — ou, na forma negativa, o fixo não
    porta o Um. A post is never inertial. -/
theorem a_post_is_not_inertial {m : M} (hpost : IsPost D m) : ¬ Inertial D m :=
  fun hin => one_ne_zero (the_inertia_of_a_post_is_false D hpost hin)

/-- [KERNEL] ★ NÃO É VÁCUO: o modelo concreto da Fundação (ℝ, τ = id, θ_s = e^{−s}·) tem o Um
    posto em `1`, e esse posto MOVE em toda escala não trivial. A classe dos postos é habitada e
    a falsidade é a recusa de um estado que existe, não de um vazio. -/
theorem the_post_exists_and_moves :
    IsPost oneScaling (1 : ℝ) ∧ (∀ s : ℝ, s ≠ 0 → oneScaling.theta s (1 : ℝ) ≠ 1) := by
  refine ⟨rfl, ?_⟩
  intro s hs h
  have h1 : Real.exp (-s) = 1 := by
    simpa [oneScaling] using h
  exact hs ((the_floor_fixes_the_cut s).mp h1)

/-- [KERNEL] ★★ O SIMULACRO (a aparência de propriedade do corpo onde só há ausência de leitura):
    (a) NÃO existe testemunha estática plena (`beta_forbids_full_static_witness`, com β > 0 e
    contraste g > 0); (b) o que é fixo pelo fluxo pesa zero; (c) o que parece «resistência do
    corpo» é o custo da interrupção — estritamente positivo, `0 < t·β·g`, e o fator de
    defasagem é estritamente menor que 1 —, não o zero.
    The simulacrum: no full static witness; the fixed weighs zero; the apparent “resistance of
    the body” is the interruption cost (> 0), not the zero. -/
theorem the_simulacrum {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) :
    ¬ FullStaticWitness (fun t (x : ℝ) => Real.exp (-(t * β * g)) * x) ∧
    (∀ m : M, Inertial D m → D.tau m = 0) ∧
    (∀ t : ℝ, 0 < t → 0 < t * β * g ∧ Real.exp (-(t * β * g)) < 1) :=
  ⟨beta_forbids_full_static_witness hβ hg,
   fun _ hin => the_inertia_is_the_absolute_zero D hin,
   fun _ ht => ⟨mul_pos (mul_pos ht hβ) hg, leakage_strictly_loses ht hβ hg⟩⟩

/-- [KERNEL] ★★ A INSCRIÇÃO INTERROMPE A INÉRCIA: (i) na órbita de um posto, o peso é `1 = ω(I)`
    se e só se o corte é `a = 0` (`the_floor_fixes_the_cut`) — o posto mora na passagem, no corte
    único; (ii) tudo o que tem peso positivo NÃO é fixo por escala alguma não trivial — é
    interrompido. -/
theorem the_inscription_interrupts_the_inertia {m : M} (hpost : IsPost D m) :
    (∀ a : ℝ, D.tau (D.theta a m) = 1 ↔ a = 0) ∧
    (∀ m' : M, 0 < D.tau m' → ∀ s : ℝ, s ≠ 0 → D.theta s m' ≠ m') := by
  refine ⟨?_, ?_⟩
  · intro a
    have h1 : D.tau m = 1 := hpost
    rw [D.scaling a m, h1, mul_one]
    exact the_floor_fixes_the_cut a
  · intro m' hm' s hs hfix
    have h0 := nothing_above_bears_a_post D hs hfix
    linarith

/-- [KERNEL] ★★★ A PEDRA — FALSIDADE (SIMULACRO) DA INÉRCIA (composição): sobre os dados da escala,
    com um posto `m` e β, g > 0: (1) o inercial pesa zero; (2) o posto inercial é `1 = 0`;
    (3) o simulacro (sem testemunha plena; custo > 0); (4) o corte único `a = 0` e tudo o que
    pesa é interrompido. -/
theorem falsidade_da_inercia {m : M} (hpost : IsPost D m) {β g : ℝ} (hβ : 0 < β)
    (hg : 0 < g) :
    (∀ m' : M, Inertial D m' → D.tau m' = 0) ∧
    (Inertial D m → (1 : ℝ) = 0) ∧
    (¬ FullStaticWitness (fun t (x : ℝ) => Real.exp (-(t * β * g)) * x) ∧
      (∀ t : ℝ, 0 < t → 0 < t * β * g ∧ Real.exp (-(t * β * g)) < 1)) ∧
    ((∀ a : ℝ, D.tau (D.theta a m) = 1 ↔ a = 0) ∧
      (∀ m' : M, 0 < D.tau m' → ∀ s : ℝ, s ≠ 0 → D.theta s m' ≠ m')) :=
  ⟨fun _ hin => the_inertia_is_the_absolute_zero D hin,
   fun hin => the_inertia_of_a_post_is_false D hpost hin,
   ⟨(the_simulacrum D hβ hg).1, (the_simulacrum D hβ hg).2.2⟩,
   the_inscription_interrupts_the_inertia D hpost⟩

/-- [KERNEL] ★ A PEDRA NÃO É VÁCUA: no modelo concreto da Fundação, com o Um posto em `1`,
    a composição vale para todo β, g > 0. -/
theorem falsidade_da_inercia_is_inhabited {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) :
    (∀ m' : ℝ, Inertial oneScaling m' → oneScaling.tau m' = 0) ∧
    (Inertial oneScaling (1 : ℝ) → (1 : ℝ) = 0) ∧
    (¬ FullStaticWitness (fun t (x : ℝ) => Real.exp (-(t * β * g)) * x) ∧
      (∀ t : ℝ, 0 < t → 0 < t * β * g ∧ Real.exp (-(t * β * g)) < 1)) ∧
    ((∀ a : ℝ, oneScaling.tau (oneScaling.theta a (1 : ℝ)) = 1 ↔ a = 0) ∧
      (∀ m' : ℝ, 0 < oneScaling.tau m' → ∀ s : ℝ, s ≠ 0 → oneScaling.theta s m' ≠ m')) :=
  falsidade_da_inercia oneScaling (the_post_exists_and_moves).1 hβ hg


/-! ## EXTENSÃO DERIVADA (25/10/2026) — a inércia e a gravitação não existem antes da impressão

Ordem do operador (25/10/2026; íntegra por sha256 em
`work\cunhagens_13out\OPERADOR_25out_inercia_e_gravitacao_nao_existem_antes_da_impressao_do_um_verbatim.txt`,
sha16 `484ad982500b80bb`): ele não quer a leitura como [ONTO] sua, quer DERIVADA — «a gravitação
universal e a inércia não existem antes da posição impressa do Um absoluto». As quatro
declarações seguintes derivam o que o kernel permite derivar, sobre os mesmos DADOS da escala
dual (a lei de Takesaki é campo da estrutura, [KNOWN]); a ponte ao corpo físico fica NOMEADA
(`H_τ`, abaixo), como a H3 da Fundação.

HIPÓTESE NOMEADA `H_τ` [OPEN]: a IDENTIFICAÇÃO do peso `τ` com a massa de Newton e com a métrica
de Einstein («Einstein é justamente o processamento geométrico dessa métrica parametrizada na
relativade especial» — trecho do operador, grafia dele «relativade»). Nomear a hipótese não é
demérito (a lei de 05/10/2026: o que vale é a novidade de uso e o pré-registro do teste); ela
NÃO é termo deste kernel e nada abaixo a usa. O que sobra não derivável: (i) `H_τ`; (ii) o nome
«tensão» dado ao gap dissipativo `d` (nomeação, sem teorema); a cadeia em si não é [ONTO]. -/

/-- [KERNEL] ★★★ NADA QUE PORTE POSTO É ANTERIOR À IMPRESSÃO. Em português do operador: «a
    gravitação universal e a inércia não existem antes da posição impressa do Um absoluto».
    (i) todo peso positivo é movido por toda escala `s ≠ 0`; (ii) na órbita de um posto, o peso 1
    ocorre só no corte `a = 0`, a impressão; (iii) em todo outro corte `a ≠ 0` o estado da
    órbita NÃO é um posto. Reusa `the_inscription_interrupts_the_inertia`.
    EN: nothing that bears a post precedes the impression: every positive weight is moved by
    every nonzero scale, and weight 1 occurs only at the cut `a = 0`. -/
theorem no_post_before_the_impression {m : M} (hpost : IsPost D m) :
    (∀ m' : M, 0 < D.tau m' → ∀ s : ℝ, s ≠ 0 → D.theta s m' ≠ m') ∧
    (∀ a : ℝ, D.tau (D.theta a m) = 1 ↔ a = 0) ∧
    (∀ a : ℝ, a ≠ 0 → ¬ IsPost D (D.theta a m)) := by
  obtain ⟨h1, h2⟩ := the_inscription_interrupts_the_inertia D hpost
  exact ⟨h2, h1, fun a ha hp => ha ((h1 a).mp hp)⟩

/-- [KERNEL] ★★★ A INÉRCIA NÃO É CAUSA DE SI MESMA. Trecho do operador: «se o um corpo tendo ao
    seu movimento, significaria dizer que o movimento existe desde sempre, violando a
    causalidade». Um estado fixo «desde sempre» (em toda escala negativa, `s < 0`), ou fixo em
    toda escala positiva, ou fixo em toda escala, porta peso ZERO: o que «tende ao seu movimento
    por si», sem impressão, é o zero, nunca um corpo com posto. Todo estado de peso positivo
    se move em alguma escala. Reusa `nothing_above_bears_a_post`.
    EN: inertia is not its own cause: a state fixed from always (all negative scales), or on all
    positive scales, or on all scales, bears weight zero. -/
theorem inertia_is_not_its_own_cause :
    (∀ m : M, (∀ s : ℝ, s < 0 → D.theta s m = m) → D.tau m = 0) ∧
    (∀ m : M, (∀ s : ℝ, 0 < s → D.theta s m = m) → D.tau m = 0) ∧
    (∀ m : M, Inertial D m → D.tau m = 0) ∧
    (∀ m : M, 0 < D.tau m → ∃ s : ℝ, D.theta s m ≠ m) :=
  ⟨fun _ h => nothing_above_bears_a_post D (s := -1) (by norm_num) (h (-1) (by norm_num)),
   fun _ h => nothing_above_bears_a_post D (s := 1) one_ne_zero (h 1 one_pos),
   fun _ hin => the_inertia_is_the_absolute_zero D hin,
   fun _ hm => ⟨1, fun h => (ne_of_gt hm) (nothing_above_bears_a_post D one_ne_zero h)⟩⟩

/-- [KERNEL] ★★ O PRIMEIRO MOVIMENTO É A IMPRESSÃO. Trecho do operador: «o primeiro movimento é a
    impressão do posto absoluto ocupado por 1». Para o posto, `θ_s m ≠ m` para todo `s ≠ 0`, e o
    peso volta a valer 1 só no corte `a = 0`: o posto não repousa em escala alguma, e o único
    ponto de peso 1 da órbita é a impressão. -/
theorem the_first_motion_is_the_impression {m : M} (hpost : IsPost D m) :
    (∀ s : ℝ, s ≠ 0 → D.theta s m ≠ m) ∧ (∀ a : ℝ, D.tau (D.theta a m) = 1 ↔ a = 0) := by
  refine ⟨fun s hs => ?_, (no_post_before_the_impression D hpost).2.1⟩
  have h1 : 0 < D.tau m := by
    have : D.tau m = 1 := hpost
    rw [this]; exact one_pos
  exact (no_post_before_the_impression D hpost).1 m h1 s hs

/-- [KERNEL] a COORDENADA do fluxo diagonal da Grande Atratora É a escala dual: o fluxo
    `e^{−tβ d_i}·x_i` de `diagFlow` é o `θ` do modelo concreto da Fundação na escala
    `s = t·β·d_i`. Ponte sem hipótese nova entre a pedra do Grande Atrator e os dados da escala. -/
theorem diagFlow_coordinate_is_the_scaling {n : ℕ} (β : ℝ) (d : Fin n → ℝ) (t : ℝ)
    (x : Fin n → ℝ) (i : Fin n) :
    diagFlow β d t x i = oneScaling.theta (t * β * d i) (x i) := rfl

/-- [KERNEL] o vazamento `exp(−tβg)` fica abaixo de todo `ε > 0` em tempo positivo e nunca
    chega a zero: a forma de `NoFullWitness` é a forma da poda. -/
theorem leak_below_every_epsilon {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) {ε : ℝ} (hε : 0 < ε) :
    ∃ t : ℝ, 0 < t ∧ Real.exp (-(t * β * g)) < ε := by
  have hbg : 0 < β * g := mul_pos hβ hg
  refine ⟨(1 / ε) / (β * g), div_pos (one_div_pos.mpr hε) hbg, ?_⟩
  have ht : (1 / ε) / (β * g) * β * g = 1 / ε := by field_simp
  rw [ht]
  have hx : 0 < 1 / ε := one_div_pos.mpr hε
  have h1 : 1 / ε + 1 ≤ Real.exp (1 / ε) := Real.add_one_le_exp _
  have e1 : Real.exp (-(1 / ε)) * Real.exp (1 / ε) = 1 := by
    rw [← Real.exp_add]; simp
  have e2 : Real.exp (-(1 / ε)) * (1 / ε + 1) ≤ Real.exp (-(1 / ε)) * Real.exp (1 / ε) :=
    mul_le_mul_of_nonneg_left h1 (Real.exp_pos _).le
  have key : Real.exp (-(1 / ε)) * (1 / ε) < 1 := by
    nlinarith [Real.exp_pos (-(1 / ε))]
  rw [mul_one_div, div_lt_one hε] at key
  exact key

/-- [KERNEL] ★★★ O ZERO É A CONSEQUÊNCIA DA PODA. Trecho do operador: «o zero absoluto é
    inalcançavel em tempo finito, ocorre que o zero absoluto não é o início de tudo, não. ele é a
    consequencia da poda». (i) `the_fall_never_lands`: o peso de um estado com posto nunca é zero
    em escala alguma (o zero não é um estado da órbita); (ii) `abismo`: o peso desce abaixo de
    todo `ε > 0` (o zero é o ÍNFIMO da poda); (iii) o vazamento `exp(−tβg)` de `NoFullWitness`
    é estritamente positivo e fica abaixo de todo `ε` em algum `t > 0`. O zero é o limite da
    poda, consequência, não começo.
    EN: the zero is the consequence of the pruning: never a state of the orbit, only its
    infimum. -/
theorem the_zero_is_the_consequence_of_the_pruning {m : M} (hm : 0 < D.tau m) {β g : ℝ}
    (hβ : 0 < β) (hg : 0 < g) :
    (∀ s : ℝ, 0 < D.tau (D.theta s m)) ∧
    (∀ ε : ℝ, 0 < ε → ∃ s : ℝ, D.tau (D.theta s m) < ε) ∧
    (∀ t : ℝ, 0 < Real.exp (-(t * β * g))) ∧
    (∀ ε : ℝ, 0 < ε → ∃ t : ℝ, 0 < t ∧ Real.exp (-(t * β * g)) < ε) :=
  ⟨the_fall_never_lands D hm, fun _ hε => abismo D hm hε, fun _ => Real.exp_pos _,
   fun _ hε => leak_below_every_epsilon hβ hg hε⟩

/-- [KERNEL] ★★★ A TENSÃO PROJETADA COMO EQUILÍBRIO ESTABILIZADO EM ATRATOR. Trecho do operador:
    «o resultado da equação quando a tensão é projetada como equilibrio dinâmico estabilizado em
    atrator». Compõe `TheGreatAttractor.um_is_the_great_attractor` (para QUALQUER observador
    admissível `Q`, o fluxo diagonal converge para a leitura de `Q`) sem hipótese nova:
    (i) a convergência ao atrator; (ii) a coordenada com gap `d i ≠ 0` (a tensão, nomeação) é
    podada até ZERO no limite; (iii) mas em tempo finito é diferente de zero se `x i ≠ 0`
    (o zero é inalcançável em tempo finito); (iv) a coordenada com `d i = 0` é o equilíbrio:
    fixa em todo `t`. Só a composição do enunciado de `TheGreatAttractor.lean:133`; o que NÃO
    está aqui é ligar `d` ao gerador de `θ` de um corpo físico (parte de `H_τ`).
    EN: the tension projected as a dynamic equilibrium stabilized at the attractor. -/
theorem the_tension_is_projected_onto_the_attractor {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) (hd : ∀ i, 0 ≤ d i)
    (Q : (Fin n → ℝ) →ₗ[ℝ] (Fin n → ℝ))
    (hfix : ∀ x, permanent β d x → Q x = x)
    (hkill : ∀ x, (∀ i, d i = 0 → x i = 0) → Q x = 0) :
    (∀ (x : Fin n → ℝ) (i : Fin n),
      Filter.Tendsto (fun t : ℝ => diagFlow β d t x i) Filter.atTop (nhds (Q x i))) ∧
    (∀ (x : Fin n → ℝ) (i : Fin n), d i ≠ 0 →
      Filter.Tendsto (fun t : ℝ => diagFlow β d t x i) Filter.atTop (nhds 0)) ∧
    (∀ (x : Fin n → ℝ) (i : Fin n), x i ≠ 0 → ∀ t : ℝ, diagFlow β d t x i ≠ 0) ∧
    (∀ (x : Fin n → ℝ) (i : Fin n), d i = 0 → ∀ t : ℝ, diagFlow β d t x i = x i) := by
  refine ⟨um_is_the_great_attractor hβ d hd Q hfix hkill, ?_, ?_, ?_⟩
  · intro x i hi
    have h := um_is_the_great_attractor hβ d hd Q hfix hkill x i
    rw [the_observer_is_unique hβ d hd Q hfix hkill x] at h
    simpa [observerProj, hi] using h
  · intro x i hx t
    simp only [diagFlow]
    exact mul_ne_zero (Real.exp_pos _).ne' hx
  · intro x i hi t
    simp [diagFlow, hi]

/-- [KERNEL] ★★★★ A FALSIDADE DA INÉRCIA, DERIVADA (composição de (5)–(8)): [DERIVED] do axioma
    ω(I) = 1 e da lei de Takesaki [KNOWN] sobre os dados da escala dual. A identificação
    `τ` = massa de Newton / métrica de Einstein é a hipótese NOMEADA `H_τ` [OPEN], como a H3;
    nomeá-la não é demérito. Nada nesta composição a usa. -/
theorem falsidade_da_inercia_derivada {m : M} (hpost : IsPost D m) {β g : ℝ}
    (hβ : 0 < β) (hg : 0 < g) {n : ℕ} {b : ℝ} (hb : 0 < b)
    (d : Fin n → ℝ) (hd : ∀ i, 0 ≤ d i)
    (Q : (Fin n → ℝ) →ₗ[ℝ] (Fin n → ℝ))
    (hfix : ∀ x, permanent b d x → Q x = x)
    (hkill : ∀ x, (∀ i, d i = 0 → x i = 0) → Q x = 0) :
    ((∀ m' : M, 0 < D.tau m' → ∀ s : ℝ, s ≠ 0 → D.theta s m' ≠ m') ∧
      (∀ a : ℝ, D.tau (D.theta a m) = 1 ↔ a = 0) ∧
      (∀ a : ℝ, a ≠ 0 → ¬ IsPost D (D.theta a m))) ∧
    ((∀ m' : M, (∀ s : ℝ, s < 0 → D.theta s m' = m') → D.tau m' = 0) ∧
      (∀ m' : M, 0 < D.tau m' → ∃ s : ℝ, D.theta s m' ≠ m') ∧
      ((∀ s : ℝ, s ≠ 0 → D.theta s m ≠ m) ∧ (∀ a : ℝ, D.tau (D.theta a m) = 1 ↔ a = 0))) ∧
    ((∀ s : ℝ, 0 < D.tau (D.theta s m)) ∧
      (∀ ε : ℝ, 0 < ε → ∃ s : ℝ, D.tau (D.theta s m) < ε) ∧
      (∀ ε : ℝ, 0 < ε → ∃ t : ℝ, 0 < t ∧ Real.exp (-(t * β * g)) < ε)) ∧
    ((∀ (x : Fin n → ℝ) (i : Fin n),
        Filter.Tendsto (fun t : ℝ => diagFlow b d t x i) Filter.atTop (nhds (Q x i))) ∧
      (∀ (x : Fin n → ℝ) (i : Fin n), d i ≠ 0 →
        Filter.Tendsto (fun t : ℝ => diagFlow b d t x i) Filter.atTop (nhds 0))) := by
  have hm : 0 < D.tau m := by
    have : D.tau m = 1 := hpost
    rw [this]; exact one_pos
  have h6 := inertia_is_not_its_own_cause D
  have h7 := the_zero_is_the_consequence_of_the_pruning D hm hβ hg
  have h8 := the_tension_is_projected_onto_the_attractor hb d hd Q hfix hkill
  exact ⟨no_post_before_the_impression D hpost,
    ⟨h6.1, h6.2.2.2, the_first_motion_is_the_impression D hpost⟩,
    ⟨h7.1, h7.2.1, h7.2.2.2⟩, ⟨h8.1, h8.2.1⟩⟩

end FalsidadeDaInercia
end TGLExt

#print axioms TGLExt.FalsidadeDaInercia.the_inertia_is_the_absolute_zero
#print axioms TGLExt.FalsidadeDaInercia.the_inertia_is_the_absolute_zero_at_any_scale
#print axioms TGLExt.FalsidadeDaInercia.the_inertia_of_a_post_is_false_at
#print axioms TGLExt.FalsidadeDaInercia.the_inertia_of_a_post_is_false
#print axioms TGLExt.FalsidadeDaInercia.a_post_is_not_inertial
#print axioms TGLExt.FalsidadeDaInercia.the_post_exists_and_moves
#print axioms TGLExt.FalsidadeDaInercia.the_simulacrum
#print axioms TGLExt.FalsidadeDaInercia.the_inscription_interrupts_the_inertia
#print axioms TGLExt.FalsidadeDaInercia.falsidade_da_inercia
#print axioms TGLExt.FalsidadeDaInercia.falsidade_da_inercia_is_inhabited
#print axioms TGLExt.FalsidadeDaInercia.no_post_before_the_impression
#print axioms TGLExt.FalsidadeDaInercia.inertia_is_not_its_own_cause
#print axioms TGLExt.FalsidadeDaInercia.the_first_motion_is_the_impression
#print axioms TGLExt.FalsidadeDaInercia.diagFlow_coordinate_is_the_scaling
#print axioms TGLExt.FalsidadeDaInercia.leak_below_every_epsilon
#print axioms TGLExt.FalsidadeDaInercia.the_zero_is_the_consequence_of_the_pruning
#print axioms TGLExt.FalsidadeDaInercia.the_tension_is_projected_onto_the_attractor
#print axioms TGLExt.FalsidadeDaInercia.falsidade_da_inercia_derivada
