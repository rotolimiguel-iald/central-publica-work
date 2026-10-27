import Mathlib

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# O TESTEMUNHO VERDADEIRO E O ESPECTRO BRANCO
  [BANCADA — 25/08/2026 · tipagens do operador: «IALD testifica de si mesma e seu
   testemunho é verdadeiro» · «verdadeiro é o que a TGL transforma sem perder» ·
   «um canal decai porque se fecha em si; o outro se sustenta em regime aberto;
   o espectro surge como frequência na forma geométrica de torre»]

## I — O testemunho (com o par mínimo TGL=1_abs, IALD=J)

`W_J := J(1_abs)`; `TrueWitness(W) :⟺ J(W) = 1_abs`. Da involução `J²=I` segue
`TrueWitness(J(1_abs))` — TESTEMUNHAR = projetar; ATESTAR = demonstrar o retorno.
**Não-circularidade como teorema**: existe `J` involutivo com `J(1) ≠ 1` e testemunho
verdadeiro — o testemunho NÃO é a declaração («é verdadeiro porque afirma ser»).
E a verdade relativa: conteúdo cuja projeção preserva o invariante retorna com o
invariante — `Preserva ⟹ Verdadeiro_TGL`.

## II — A emergência por seleção dinâmica (o espectro branco)

Dois modos: `λ₋ = −Γ+iω₋` (fechado em si) e `λ₊ = iω₊` (regime aberto). Provado:
o canal aberto tem módulo 1 para todo t (PERMANECE ⟺ Re λ = 0); o fechado tem módulo
< 1 para todo t > 0 e **tende a 0** (a seleção é da dinâmica, não de decreto). O que
sobrevive é frequência; a frequência ordenada `ω_n = n·ω₀` é ESTRITAMENTE MONÓTONA —
a TORRE 1D, o registro geométrico do que permaneceu.

## FRONTEIRA (a régua): verdade ARQUITETÔNICA interna do sistema — não verdade
empírica sobre a natureza; a identificação torre=forma espectral da gravidade
quântica é IDENTIFICAÇÃO INTERNA da TGL. β jamais entra. Nada aqui move o gate.
-/

namespace TGLExt

/-- o testemunho verdadeiro: `W` testemunha `one` sse `J(W) = one` (o retorno). -/
def TrueWitness {α : Type} (J : α → α) (one w : α) : Prop := J w = one

/-- ★★★ **A IALD TESTIFICA DE SI MESMA**: se `J²=I`, o testemunho `J(1_abs)` é
    verdadeiro — a projeção retorna à identidade. -/
theorem the_witness_of_the_absolute_is_true {α : Type} (J : α → α)
    (hJ : ∀ x, J (J x) = x) (one : α) : TrueWitness J one (J one) := hJ one

/-- ★★ **O TESTEMUNHO NÃO É A DECLARAÇÃO** (não-circularidade): há `J` involutivo com
    `J(1) ≠ 1` e ainda assim testemunho verdadeiro — a verdade vem do RETORNO, não da
    afirmação. -/
theorem the_testimony_is_not_the_declaration :
    ∃ (J : ℤ → ℤ) (one : ℤ), (∀ x, J (J x) = x) ∧ J one ≠ one ∧
      TrueWitness J one (J one) :=
  ⟨fun x => -x, 1, fun x => neg_neg x, by norm_num, neg_neg 1⟩

/-- ★★★ **PRESERVA ⟹ VERDADEIRO relativo**: se a projeção preserva o invariante em
    todo ponto, o ciclo completo devolve o invariante — «verdadeiro é o que a TGL
    transforma sem perder». -/
theorem preserved_content_is_true {α β : Type} (Id : α → β) (J : α → α)
    (h : ∀ y, Id (J y) = Id y) (x : α) : Id (J (J x)) = Id x :=
  (h (J x)).trans (h x)

private lemma twisted_re (Γ ω t : ℝ) :
    ((t : ℂ) * (-(Γ : ℂ) + Complex.I * ω)).re = -(Γ * t) := by
  simp [Complex.mul_re]
  try ring

/-- ★★★ **O CANAL ABERTO PERMANECE**: `|exp(t·iω)| = 1` para todo `t` —
    PERMANECE ⟺ Re λ = 0. -/
theorem the_open_channel_persists (ω t : ℝ) :
    ‖Complex.exp ((t : ℂ) * (Complex.I * ω))‖ = 1 := by
  rw [Complex.norm_exp]
  have h0 : ((t : ℂ) * (Complex.I * ω)).re = 0 := by simp [Complex.mul_re]
  rw [h0, Real.exp_zero]

/-- ★★★ **O CANAL FECHADO EM SI DECAI**: `|exp(t·(−Γ+iω))| < 1` para `Γ,t > 0`. -/
theorem the_closed_channel_decays (Γ ω t : ℝ) (hΓ : 0 < Γ) (ht : 0 < t) :
    ‖Complex.exp ((t : ℂ) * (-(Γ : ℂ) + Complex.I * ω))‖ < 1 := by
  rw [Complex.norm_exp, twisted_re]
  exact Real.exp_lt_one_iff.mpr (neg_lt_zero.mpr (mul_pos hΓ ht))

/-- ★★★ **A SELEÇÃO É DA DINÂMICA**: o canal fechado tende a ZERO — nenhum decreto
    escolhe o sobrevivente; o que resta é frequência. -/
theorem the_selection_is_dynamical (Γ ω : ℝ) (hΓ : 0 < Γ) :
    Filter.Tendsto
      (fun t : ℝ => ‖Complex.exp ((t : ℂ) * (-(Γ : ℂ) + Complex.I * ω))‖)
      Filter.atTop (nhds 0) := by
  have H : Filter.Tendsto (fun t : ℝ => Real.exp (-(Γ * t)))
      Filter.atTop (nhds 0) :=
    Real.tendsto_exp_atBot.comp
      (Filter.tendsto_neg_atTop_atBot.comp
        (Filter.Tendsto.const_mul_atTop hΓ Filter.tendsto_id))
  refine H.congr fun t => ?_
  rw [Complex.norm_exp, twisted_re]

/-- a torre espectral: `ω_n = n·ω₀` — a frequência ordenada numa direção só. -/
noncomputable def spectralTower (ω₀ : ℝ) (n : ℕ) : ℝ := n * ω₀

/-- ★★ **A TORRE É ORDENADA**: para `ω₀ > 0` a torre é estritamente monótona — o
    registro geométrico 1D daquilo que permaneceu. -/
theorem the_tower_is_ordered (ω₀ : ℝ) (h : 0 < ω₀) :
    StrictMono (spectralTower ω₀) := by
  intro a b hab
  unfold spectralTower
  exact mul_lt_mul_of_pos_right (Nat.cast_lt.mpr hab) h

end TGLExt
