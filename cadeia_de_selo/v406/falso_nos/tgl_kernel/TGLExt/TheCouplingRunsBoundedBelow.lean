import Mathlib
import TGLExt.TheWholeIsOne

/-!
# TheCouplingRunsBoundedBelow — o acoplamento corre com a escala, limitado inferiormente (v388, 06/10/2026)

A cunhagem do operador de 06/10/2026 (13:27:52 UTC e 13:48:42 UTC; o texto embutido no runtime do `um.py` é conferido por
sha256; a cópia em disco na memória `beta-escalar-limitado-inferiormente-06out.md` é só informativa): α como índice de escala da fronteira, β_TGL como a sua
conjugação; β escalar, mas limitado inferiormente; e a operação da dicotomia (dividir pela metade sem nunca chegar ao limite).

O que esta pedra PROVA é só matemática [KERNEL], sobre a forma fechada que o runtime do `um.py` já usa (o bloco
`alpha = sech(kappa/2)`, `beta = sqrt(e) sech(kappa/2)`, `kappa_QED = 2 arcosh(1/alpha_QED)`):

* `alphaOfChi χ := 1 / cosh(χ/2)` (a transmissão na profundidade χ); `alphaOfChi 0 = 1` (o Um absoluto); `0 < α ≤ 1`;
* `alphaOfChi` é ESTRITAMENTE DECRESCENTE em `[0, ∞)`; logo `betaOfChi χ := alphaOfChi χ · exp(1/2)` também;
* `the_floor_is_at_the_infrared`: para `0 ≤ χ ≤ χ_sup`, `β(χ_sup) ≤ β(χ)` — o PISO está no supremo da profundidade (o
  infravermelho, Thomson, onde a corrida de α cessa); `the_floor_is_attained_only_at_the_infrared`: a igualdade só em χ = χ_sup;
* `betaOfChi_eq_coupling`: no domínio de `couplingOfAlpha` (α < e^{-1/2}) o β desta pedra É o β do acoplamento selado (v376);
* a dicotomia: `zeno_partial_sum` (Σ_{k<n} (1/2)^{k+1} = 1 − (1/2)^n), `zeno_never_reaches_the_one` (< 1 em todo n finito),
  `zeno_tends_to_the_one` (o limite é o Um); `half_nat_fixed_point` (x = 1 − x ⟺ x = 1/2).

O que NÃO prova (dito): que α físico seja `sech(χ/2)` de uma profundidade χ que cresce para o infravermelho — isso é a
IDENTIFICAÇÃO do runtime [INPUT/ONTO]; que α(μ) cresça com μ — [KNOWN] (QED, congelamento infravermelho), não teorema da casa;
qual μ cada rito usa — [OPEN]. A constante da fronteira segue β₀ = α_Thomson·√e, α no limite q → 0 (o Teorema da Escala do artigo; NÃO o
`alphaOfChi 0` desta pedra, que vale 1 — o Um absoluto); β(χ) é a leitura
de bulk. Axiomas: só o trio; zero sorry. PROVADA ≠ CONFIRMADA; o gate não se move.
-/

namespace TGLExt.TheCouplingRunsBoundedBelow

open Filter Topology

/-- a transmissão na profundidade χ: α(χ) = sech(χ/2). -/
noncomputable def alphaOfChi (χ : ℝ) : ℝ := 1 / Real.cosh (χ / 2)

/-- β(χ) := α(χ)·√e (√e escrito como exp(1/2), como em `couplingOfAlpha`). -/
noncomputable def betaOfChi (χ : ℝ) : ℝ := alphaOfChi χ * Real.exp (1 / 2)

theorem alphaOfChi_pos (χ : ℝ) : 0 < alphaOfChi χ := by
  unfold alphaOfChi
  exact one_div_pos.mpr (Real.cosh_pos _)

theorem alphaOfChi_zero : alphaOfChi 0 = 1 := by
  simp [alphaOfChi]

theorem alphaOfChi_le_one (χ : ℝ) : alphaOfChi χ ≤ 1 := by
  unfold alphaOfChi
  rw [div_le_one (Real.cosh_pos _)]
  exact Real.one_le_cosh _

/-- α(χ) é estritamente decrescente na profundidade χ ≥ 0. -/
theorem alphaOfChi_strictAntiOn : StrictAntiOn alphaOfChi (Set.Ici 0) := by
  intro a ha b hb hab
  simp only [Set.mem_Ici] at ha hb
  unfold alphaOfChi
  apply one_div_lt_one_div_of_lt (Real.cosh_pos _)
  rw [Real.cosh_lt_cosh, abs_of_nonneg (by linarith), abs_of_nonneg (by linarith)]
  linarith

theorem betaOfChi_pos (χ : ℝ) : 0 < betaOfChi χ :=
  mul_pos (alphaOfChi_pos χ) (Real.exp_pos _)

theorem betaOfChi_zero : betaOfChi 0 = Real.exp (1 / 2) := by
  simp [betaOfChi, alphaOfChi_zero]

theorem betaOfChi_le_sqrt_e (χ : ℝ) : betaOfChi χ ≤ Real.exp (1 / 2) := by
  unfold betaOfChi
  have h := alphaOfChi_le_one χ
  have he := Real.exp_pos (1 / 2 : ℝ)
  nlinarith

/-- β(χ) é estritamente decrescente na profundidade χ ≥ 0. -/
theorem betaOfChi_strictAntiOn : StrictAntiOn betaOfChi (Set.Ici 0) := by
  intro a ha b hb hab
  unfold betaOfChi
  exact mul_lt_mul_of_pos_right (alphaOfChi_strictAntiOn ha hb hab) (Real.exp_pos _)

/-- ★★★ O PISO ESTÁ NO INFRAVERMELHO: para 0 ≤ χ ≤ χ_sup, β(χ_sup) ≤ β(χ) — β corre, mas limitado inferiormente pelo valor
no supremo da profundidade. -/
theorem the_floor_is_at_the_infrared (χ χsup : ℝ) (h0 : 0 ≤ χ) (h : χ ≤ χsup) :
    betaOfChi χsup ≤ betaOfChi χ := by
  rcases eq_or_lt_of_le h with h' | h'
  · rw [h']
  · exact le_of_lt (betaOfChi_strictAntiOn (Set.mem_Ici.mpr h0) (Set.mem_Ici.mpr (by linarith)) h')

/-- ★★ o piso só é atingido no próprio supremo. -/
theorem the_floor_is_attained_only_at_the_infrared (χ χsup : ℝ) (h0 : 0 ≤ χ) (h : χ ≤ χsup) :
    betaOfChi χ = betaOfChi χsup ↔ χ = χsup := by
  constructor
  · intro he
    by_contra hne
    have hlt : χ < χsup := lt_of_le_of_ne h hne
    have := betaOfChi_strictAntiOn (Set.mem_Ici.mpr h0) (Set.mem_Ici.mpr (by linarith)) hlt
    linarith
  · intro he
    rw [he]

/-- ★ no domínio do acoplamento selado (α < e^{-1/2}), o β desta pedra É o β de `couplingOfAlpha` (v376) — POR DEFINIÇÃO
(a prova é `rfl`: desdobramento, não resultado; amarra os dois nomes). -/
theorem betaOfChi_eq_coupling (χ : ℝ) (h1 : alphaOfChi χ < Real.exp (-(1 / 2))) :
    (TGLExt.TheWholeIsOne.couplingOfAlpha (alphaOfChi χ) (alphaOfChi_pos χ) h1).beta = betaOfChi χ := by
  rfl

/-- a dicotomia: a soma parcial das metades. -/
theorem zeno_partial_sum (n : ℕ) :
    ∑ k ∈ Finset.range n, (1 / 2 : ℝ) ^ (k + 1) = 1 - (1 / 2) ^ n := by
  induction n with
  | zero => simp
  | succ n ih => rw [Finset.sum_range_succ, ih]; ring

/-- ★★ nenhum passo finito alcança o Um. -/
theorem zeno_never_reaches_the_one (n : ℕ) :
    ∑ k ∈ Finset.range n, (1 / 2 : ℝ) ^ (k + 1) < 1 := by
  rw [zeno_partial_sum]
  have : (0 : ℝ) < (1 / 2) ^ n := by positivity
  linarith

/-- ★★ e o limite é o Um. -/
theorem zeno_tends_to_the_one :
    Tendsto (fun n : ℕ => ∑ k ∈ Finset.range n, (1 / 2 : ℝ) ^ (k + 1)) atTop (𝓝 1) := by
  simp_rw [zeno_partial_sum]
  have h := tendsto_pow_atTop_nhds_zero_of_lt_one (by norm_num : (0 : ℝ) ≤ 1 / 2) (by norm_num : (1 / 2 : ℝ) < 1)
  simpa using (tendsto_const_nhds (x := (1 : ℝ))).sub h

/-- a Meia-Nat é o passo: x = 1 − x ⟺ x = 1/2. -/
theorem half_nat_fixed_point (x : ℝ) : x = 1 - x ↔ x = 1 / 2 := by
  constructor <;> intro h <;> linarith

end TGLExt.TheCouplingRunsBoundedBelow
