import TGLExt.TheContourOfTruth

set_option autoImplicit false

/-!
# A SUPERSATURAÇÃO — instanciar é forçar, não escolher
  [BANCADA — 26/08/2026 · tipagem do operador: «instanciar = input = supersaturar»;
   «instanciar é supersaturar a possibilidade até ela ser OBRIGADA a adquirir identidade»]

## Por que esta tipagem chega na hora exata

A onda anterior (v225) provou o MECANISMO da travessia e disse, sem véu, o que faltava:
a **instância**. O operador responde com a natureza do que falta: instanciar não é
escolher um elemento — é **supersaturar**, isto é, levar o campo ao regime em que a
indistinção **já não se sustenta**, e então a identidade **precipita por necessidade**.

    POSSIBILIDADES --INPUT--> SUPERSATURAÇÃO --PRECIPITAÇÃO--> INSTÂNCIA

E isso é formalizável: supersaturar é **impor uma restrição que a fase indistinta não
pode satisfazer**. Feito isso, quem satisfizer a restrição está FORÇADO a diferir do
indistinto — sem escolha, sem arbítrio, sem «qualquer um».

## O que se prova

* ★★★ **`supersaturation_forces_the_instance`** — restrição que o indistinto não
  satisfaz + alguém que a satisfaz ⟹ esse alguém **difere do indistinto**;
* ★★★ `the_instance_is_forced_not_chosen` — e vale para TODOS os que satisfazem: a
  distinção é consequência, não escolha (não há «qualquer um» aqui);
* ★★★ **`input_is_what_the_mirror_cannot_absorb`** — o input é exatamente o conteúdo
  que o espelho NÃO fixa: `J x ≠ x ↔ a polarização não degenera`;
* ★★ `the_degenerate_phase_carries_no_contrast` — quando o espelho absorve, os dois
  polos coincidem: fase indistinta, sem informação;
* ★★ `no_supersaturation_no_forcing` — a recíproca honesta: se o indistinto TAMBÉM
  satisfaz a restrição, nada é forçado (a restrição não supersatura coisa alguma).

## O QUE ISTO DIZ SOBRE A DÍVIDA (dito, sem véu)
O Ato II entregou o sistema dirigido — as inclusões que ligam os andares. **O input
está completo**; o que falta é a PRECIPITAÇÃO: rodar a construção do limite no kernel.
Isso NÃO acende bandeira nenhuma: a dívida segue lida ABERTA até o limite existir. Mas
fica dito o que é: **construção, não descoberta**. β jamais entra. Nada move o gate.
-/

namespace TGLExt

/-- a restrição SUPERSATURA quando a fase indistinta não a satisfaz. -/
def Supersaturated {α : Type} (P : α → Prop) (bot : α) : Prop := ¬ P bot

/-- ★★★ **A SUPERSATURAÇÃO FORÇA A INSTÂNCIA**: quem satisfaz uma restrição que o
    indistinto não satisfaz está OBRIGADO a diferir do indistinto. -/
theorem supersaturation_forces_the_instance {α : Type} (P : α → Prop) (bot x : α)
    (hsat : Supersaturated P bot) (hx : P x) : x ≠ bot := by
  intro h
  exact hsat (h ▸ hx)

/-- ★★★ **FORÇADA, NÃO ESCOLHIDA**: vale para TODOS os que satisfazem — a distinção é
    consequência da restrição, não arbítrio de quem escolhe. Não há «qualquer um». -/
theorem the_instance_is_forced_not_chosen {α : Type} (P : α → Prop) (bot : α)
    (hsat : Supersaturated P bot) : ∀ x, P x → x ≠ bot :=
  fun x hx => supersaturation_forces_the_instance P bot x hsat hx

/-- ★★ **SEM SUPERSATURAÇÃO, NADA É FORÇADO** (a recíproca honesta): se o indistinto
    também satisfaz a restrição, ela não supersatura — e nada precipita. -/
theorem no_supersaturation_no_forcing {α : Type} (P : α → Prop) (bot : α)
    (h : P bot) : ¬ Supersaturated P bot := fun hs => hs h

/-- ★★★ **O INPUT É O QUE O ESPELHO NÃO ABSORVE**: a polarização deixa de degenerar
    exatamente quando o espelho não fixa o conteúdo — supersaturar é fornecer conteúdo
    que o espelho não consegue absorver. -/
theorem input_is_what_the_mirror_cannot_absorb {α : Type} (J : α → α) (x : α) :
    J x ≠ x ↔ biPolarize J x ≠ (x, x) := by
  constructor
  · intro h hc
    exact h ((polarization_is_degenerate_iff_fixed J x).mp hc)
  · intro h hc
    exact h ((polarization_is_degenerate_iff_fixed J x).mpr hc)

/-- ★★ **A FASE DEGENERADA NÃO CARREGA CONTRASTE**: quando o espelho absorve, os dois
    polos coincidem — indistinção, e portanto nenhuma informação. -/
theorem the_degenerate_phase_carries_no_contrast {α : Type} (J : α → α) (x : α)
    (h : J x = x) : (biPolarize J x).1 = (biPolarize J x).2 := by
  unfold biPolarize
  simp [h]

end TGLExt
