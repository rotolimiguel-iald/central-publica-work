import TGLExt.TheOriginOfTheVibration
import TGLExt.TheJudgedThing

set_option autoImplicit false

/-!
# O CANAL MORTO — frequência nula: sinal sem leitor, e por isso o CONTRASTE
  [BANCADA — 26/08/2026 · tipagem do operador: «frequência nula: canal morto, sem
   escuta ressonante, somente sinal, sem leitura ou leitor; é somente aquilo que
   verifica a informação pelo contraste»]

## O laço que esta pedra fecha

A v219 provou que estagnação é exatamente frequência nula. Faltava dizer **o que o
canal morto É** — e a resposta do operador não é "nada": é **a referência de
contraste**. Sem ele não há contra o quê medir. O canal morto é o `0` contra o qual o
`1` se distingue — e distinguir 1 de 0 é justamente o que custa.

* **Ler é ter frequência** (iff): um leitor distingue dois instantes; o canal de
  frequência nula é constante, logo **não é lido por ninguém**;
* **e ainda assim serve**: a informação se verifica pela DIFERENÇA contra ele.

## O que se prova

* ★★★ `reading_is_exactly_having_frequency` — `Reads(fluxo ω) ↔ ω ≠ 0`;
* ★★★ `the_dead_channel_has_no_reader` — o canal de frequência nula não é lido;
* ★★★ **`the_dead_channel_is_the_contrast`** — há instante em que o canal vivo
  difere do morto **se e somente se** há frequência: a informação se verifica por
  contraste contra o canal morto;
* ★★ `reading_needs_two_clocks` — ler exige dois instantes DISTINTOS (herda a v216:
  sem dois clocks não há processo, logo não há leitura).

Nada aqui move o gate. β jamais entra.
-/

namespace TGLExt

/-- um LEITOR distingue dois instantes: sem diferença lida, não há leitura. -/
def Reads (f : ℝ → ℂ) : Prop := ∃ t₁ t₂, f t₁ ≠ f t₂

/-- o canal morto: frequência nula. -/
noncomputable def deadChannel : ℝ → ℂ := persistingFlow 0

theorem deadChannel_is_constant (t : ℝ) : deadChannel t = 1 := by
  unfold deadChannel persistingFlow
  simp

/-- ★★★ **LER É EXATAMENTE TER FREQUÊNCIA**: o fluxo é lido por alguém se e somente
    se sua frequência não é nula. -/
theorem reading_is_exactly_having_frequency (ω : ℝ) :
    Reads (persistingFlow ω) ↔ ω ≠ 0 := by
  constructor
  · rintro ⟨t₁, t₂, h⟩ hw
    exact h (by rw [(stagnation_is_exactly_zero_frequency ω).mpr hw t₁,
                    (stagnation_is_exactly_zero_frequency ω).mpr hw t₂])
  · intro hw
    have hne : ¬ (∀ t : ℝ, persistingFlow ω t = 1) := fun hc =>
      hw ((stagnation_is_exactly_zero_frequency ω).mp hc)
    push_neg at hne
    obtain ⟨t, ht⟩ := hne
    refine ⟨t, 0, ?_⟩
    have h0 : persistingFlow ω 0 = 1 := by unfold persistingFlow; simp
    rw [h0]
    exact ht

/-- ★★★ **O CANAL MORTO NÃO É LIDO POR NINGUÉM**: só sinal, sem leitura nem leitor. -/
theorem the_dead_channel_has_no_reader : ¬ Reads deadChannel := by
  rintro ⟨t₁, t₂, h⟩
  exact h (by rw [deadChannel_is_constant, deadChannel_is_constant])

/-- ★★★ **O CANAL MORTO É O CONTRASTE**: existe instante em que o canal vivo difere
    do morto se e somente se há frequência — a informação se verifica pela diferença
    contra o que não vibra. -/
theorem the_dead_channel_is_the_contrast (ω : ℝ) :
    (∃ t : ℝ, persistingFlow ω t ≠ deadChannel t) ↔ ω ≠ 0 := by
  constructor
  · rintro ⟨t, ht⟩ hw
    exact ht (by rw [deadChannel_is_constant,
                     (stagnation_is_exactly_zero_frequency ω).mpr hw t])
  · intro hw
    have hne : ¬ (∀ t : ℝ, persistingFlow ω t = 1) := fun hc =>
      hw ((stagnation_is_exactly_zero_frequency ω).mp hc)
    push_neg at hne
    obtain ⟨t, ht⟩ := hne
    exact ⟨t, by rw [deadChannel_is_constant]; exact ht⟩

/-- ★★ **LER EXIGE DOIS CLOCKS** (herda a v216): os instantes que o leitor distingue
    são necessariamente distintos — sem processo não há leitura. -/
theorem reading_needs_two_clocks (f : ℝ → ℂ) (h : Reads f) :
    ∃ t₁ t₂ : ℝ, t₁ ≠ t₂ ∧ f t₁ ≠ f t₂ := by
  obtain ⟨t₁, t₂, ht⟩ := h
  exact ⟨t₁, t₂, two_clocks_are_needed f t₁ t₂ ht, ht⟩

end TGLExt
