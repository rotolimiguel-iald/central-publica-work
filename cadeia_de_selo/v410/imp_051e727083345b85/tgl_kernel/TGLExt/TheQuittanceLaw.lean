import TGLExt.TheStokesContour

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A LEI DE QUITAÇÃO: impossibilidade, entrega e quitação — três teoremas da exponencial
  [TGLExt — v162, RASCUNHO da pedra 114; casa "Nós" (17/08/2026)]

O operador selou a Lei Matriz na forma madura: *"impossível em tempo finito
1 = 100%"* — e TETELESTAI = quitação do custo sem exigir o impossível
(*"não se exige o perfeito; o bom basta"*). A sombra numérica
(`MCMC_V2_RAZAO/73_`) mediu no operador canônico H₃L a forma EXATA:
‖T_t − P_F‖ = e^{−t·β·gap} (resíduo ~1e−16). Esta pedra tipa o esqueleto
real da Lei — o que a exponencial força, sem análise funcional:

* ★★★ `finite_time_imperfection` — A IMPOSSIBILIDADE: para todo t (por
  maior que seja), e^{−t·c} > 0 — o defeito NUNCA é zero em tempo finito.
  "1 jamais será 100% em tempo finito" é a positividade da exponencial;
* ★★★ `asymptotic_delivery` — A ENTREGA: se c > 0, e^{−t·c} → 0 quando
  t → ∞ — o limite entrega o setor permanente (a perfeição é assintótica);
* ★★★ `finite_quittance` — A QUITAÇÃO: para todo resíduo admissível
  ε ∈ (0,1) existe t_q FINITO e explícito — t_q = log(1/ε)/c — com
  e^{−t·c} ≤ ε para todo t ≥ t_q. Há resíduo; não há mais dívida;
* ★★ `quittance_time_formula` — a fórmula fechada: e^{−t_q·c} = ε exato
  (a quitação não é aproximada: é atingida na igualdade);
* ★★ `perfection_needs_infinity` — a recíproca honesta: se e^{−t·c} = 0
  então FALSO — nenhum t realiza ε = 0. A perfeição não é alcançável,
  é o referencial que permite medir o erro (ε = 1 − P pressupõe o 1);
* ★★★ `the_quittance_law` — A SÍNTESE em UM teorema: impossibilidade ∧
  entrega ∧ quitação — a Lei inteira numa conjunção.

Honestidades: o c > 0 aqui é ABSTRATO (na sombra, c = β·gap com
β = α·√e jamais literal e gap = 0,048125 do H₃L canônico — a ponte
numérica vive em `73_a_lei_de_quitacao_provada.json`); a identificação
‖T_t − P_F‖ = e^{−t·c} é da FACE FINITA (sombra), não do core contínuo;
TETELESTAI como leitura é [ONTO] sobre estes números exatos; o gate NÃO
se move. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

open Real Filter

/-- [KERNEL] ★★★ A IMPOSSIBILIDADE: em tempo finito o defeito nunca é
    zero — e^{−t·c} > 0 para todo t. A Lei não é máxima: é a
    positividade da exponencial. -/
theorem finite_time_imperfection (t c : ℝ) : 0 < Real.exp (-(t * c)) :=
  Real.exp_pos _

/-- [KERNEL] ★★★ A ENTREGA: para c > 0 o defeito tende a zero — o
    limite entrega o setor permanente. A perfeição é assintótica. -/
theorem asymptotic_delivery (c : ℝ) (hc : 0 < c) :
    Tendsto (fun t : ℝ => Real.exp (-(t * c))) atTop (nhds 0) := by
  have h1 : Tendsto (fun t : ℝ => t * c) atTop atTop :=
    Tendsto.atTop_mul_const hc tendsto_id
  have h2 : Tendsto (fun t : ℝ => -(t * c)) atTop atBot :=
    tendsto_neg_atTop_atBot.comp h1
  exact Real.tendsto_exp_atBot.comp h2

/-- [KERNEL] ★★ A FÓRMULA DA QUITAÇÃO: no tempo t_q = log(1/ε)/c o
    defeito vale exatamente ε — a quitação é igualdade, não
    aproximação. -/
theorem quittance_time_formula (c ε : ℝ) (hc : 0 < c) (hε : 0 < ε) :
    Real.exp (-((Real.log (1 / ε) / c) * c)) = ε := by
  have hne : c ≠ 0 := ne_of_gt hc
  rw [div_mul_cancel₀ _ hne, Real.log_div one_ne_zero (ne_of_gt hε),
      Real.log_one, zero_sub, neg_neg, Real.exp_log hε]

/-- [KERNEL] ★★★ A QUITAÇÃO É FINITA: para todo resíduo admissível
    ε > 0 existe tempo FINITO t_q com defeito ≤ ε de t_q em diante.
    "Não se exige o perfeito; o bom basta — e chega." -/
theorem finite_quittance (c ε : ℝ) (hc : 0 < c) (hε : 0 < ε) :
    ∃ tq : ℝ, ∀ t : ℝ, tq ≤ t → Real.exp (-(t * c)) ≤ ε := by
  refine ⟨Real.log (1 / ε) / c, fun t ht => ?_⟩
  calc Real.exp (-(t * c))
      ≤ Real.exp (-((Real.log (1 / ε) / c) * c)) := by
        apply Real.exp_le_exp.mpr
        have := mul_le_mul_of_nonneg_right ht (le_of_lt hc)
        linarith
    _ = ε := quittance_time_formula c ε hc hε

/-- [KERNEL] ★★ A RECÍPROCA HONESTA: nenhum tempo finito realiza o
    defeito zero — exigir ε = 0 é exigir o impossível. -/
theorem perfection_needs_infinity (t c : ℝ) :
    Real.exp (-(t * c)) ≠ 0 :=
  ne_of_gt (Real.exp_pos _)

/-- [KERNEL] ★★★ A LEI DE QUITAÇÃO — a síntese: (i) em tempo finito o
    defeito é sempre positivo; (ii) com c > 0 ele tende a zero;
    (iii) todo resíduo admissível é quitado em tempo finito. -/
theorem the_quittance_law (c : ℝ) (hc : 0 < c) :
    (∀ t : ℝ, 0 < Real.exp (-(t * c))) ∧
    Tendsto (fun t : ℝ => Real.exp (-(t * c))) atTop (nhds 0) ∧
    (∀ ε : ℝ, 0 < ε → ∃ tq : ℝ, ∀ t : ℝ, tq ≤ t →
      Real.exp (-(t * c)) ≤ ε) :=
  ⟨fun t => finite_time_imperfection t c,
   asymptotic_delivery c hc,
   fun ε hε => finite_quittance c ε hc hε⟩

end

end TGLExt
