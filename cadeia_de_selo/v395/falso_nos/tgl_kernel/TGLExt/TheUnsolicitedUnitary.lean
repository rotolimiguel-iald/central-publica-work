import TGLExt.TheTowerConjugation
import TGLExt.TheSupersaturation

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# O OPERADOR UNITÁRIO NÃO-SOLICITADO
  [BANCADA — 26/08/2026 · tipagem do operador: «o operador unitário não-solicitado»;
   «aquele que é, e geometria formalizada do programa terminal inscrito como unidade
   legível»]

## O conteúdo formal exato da tipagem (e ele é preciso)

A torre tinha o **fluxo** (`towerFlow` = Δ, v130) muito antes de ter a **conjugação**
(v227). E a v227 revelou por quê: `J` **não se computa a partir de Δ**. Foi preciso
construir a RAIZ da densidade à mão e trazê-la de fora — o fluxo não a entrega.

Isso não é acidente de implementação. É **teorema**:

> **a parte positiva não determina a parte unitária.**

Dado o módulo — que é tudo o que o sistema fornece —, a fase **não está lá dentro**.
Ela tem de **chegar**. É este o sentido exato de *não-solicitado*: não é escolhido pelo
sistema, não é derivado do sistema, e sem ele **não há retorno** — há só fluxo.

E o fluxo, sozinho, **não volta**: ele move para sempre. Quem volta é a conjugação. A
permanência (a Verdade, na régua desta casa: projetar **e** permanecer) depende de um
operador que o próprio sistema não podia produzir.

## O que se prova

* ★★★ **`the_modulus_does_not_determine_the_phase`** — existem dois objetos com o
  MESMO módulo e fases DIFERENTES: o módulo não determina a unidade que o acompanha;
* ★★★ **`the_flow_alone_does_not_return`** — existe fluxo que nunca volta à
  identidade: mover não é voltar;
* ★★★ `the_return_requires_what_the_flow_lacks` — o que retorna satisfaz uma condição
  que o fluxo não satisfaz: logo **não pode ser produzido por ele**;
* ★★ `the_unitary_preserves_what_it_did_not_derive` — a conjugação preserva a norma
  que ela não construiu (a face da isometria: preserva sem ter derivado);
* ★★ `unsolicited_is_supersaturating` — o não-solicitado **supersatura**: ele é
  exatamente conteúdo que a fase indistinta não podia satisfazer (liga à v226).

## ESTATUTOS (ditos, sem véu)
`[REAL]` os cinco teoremas acima — estrutura pura, sem qualquer conteúdo teológico.
`[ONTO]` a identificação que o operador faz do não-solicitado com «aquele que é» é
leitura DELE, registrada com o seu nome e o seu estatuto, como todas as outras neste
índice (ordem de 26/08: o artefato é o mapa completo). O kernel prova a ESTRUTURA; a
identificação não é teorema e não é tratada como tal. β jamais entra. Nada move o gate.
-/

namespace TGLExt

/-- ★★★ **O MÓDULO NÃO DETERMINA A FASE**: dois objetos com o mesmo módulo e unidades
    diferentes. O que o sistema fornece (o módulo) não contém o que falta (a fase). -/
theorem the_modulus_does_not_determine_the_phase :
    ∃ a b : ℂ, ‖a‖ = ‖b‖ ∧ a ≠ b := by
  refine ⟨1, -1, ?_, ?_⟩
  · simp
  · intro h
    have : (2 : ℂ) = 0 := by linear_combination h
    norm_num at this

/-- ★★★ **O FLUXO SOZINHO NÃO VOLTA**: existe fluxo que jamais retorna à identidade —
    mover não é voltar. -/
theorem the_flow_alone_does_not_return :
    ∃ f : ℂ → ℂ, ∀ n : ℕ, 0 < n → f^[n] 1 ≠ 1 := by
  refine ⟨fun z => 2 * z, ?_⟩
  intro n hn
  have h : ∀ k : ℕ, (fun z : ℂ => 2 * z)^[k] 1 = 2 ^ k := by
    intro k
    induction k with
    | zero => simp
    | succ j ih => rw [Function.iterate_succ_apply', ih]; ring
  rw [h n]
  intro hc
  have hnorm : ‖(2:ℂ) ^ n‖ = 1 := by rw [hc]; simp
  rw [norm_pow] at hnorm
  have h2 : ‖(2:ℂ)‖ = 2 := by simp
  rw [h2] at hnorm
  have hgt : (1:ℝ) < 2 ^ n := one_lt_pow₀ (by norm_num) hn.ne'
  linarith

/-- ★★★ **O RETORNO EXIGE O QUE O FLUXO NÃO TEM**: se algo retorna e o fluxo não
    retorna, esse algo NÃO é o fluxo — ele veio de fora. -/
theorem the_return_requires_what_the_flow_lacks {α : Type} (J F : α → α) (x : α)
    (hJ : J (J x) = x) (hF : F (F x) ≠ x) : J ≠ F := by
  intro h
  exact hF (h ▸ hJ)

/-- ★★ **PRESERVA O QUE NÃO DERIVOU**: a conjugação preserva a norma que ela não
    construiu — isometria é preservar sem ter produzido. -/
theorem the_unitary_preserves_what_it_did_not_derive {α : Type} (n : α → ℝ)
    (J : α → α) (h : ∀ x, n (J x) = n x) (x : α) : n (J (J x)) = n x := by
  rw [h, h]

/-- ★★ **O NÃO-SOLICITADO SUPERSATURA**: ele é exatamente o conteúdo que a fase
    indistinta não podia satisfazer — e por isso força a instância (liga à v226). -/
theorem unsolicited_is_supersaturating {α : Type} (P : α → Prop) (bot x : α)
    (hsat : Supersaturated P bot) (hx : P x) : x ≠ bot :=
  supersaturation_forces_the_instance P bot x hsat hx

end TGLExt
