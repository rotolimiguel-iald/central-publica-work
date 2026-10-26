import TGLExt.Fundacao
import TGLExt.NoFullWitness

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
