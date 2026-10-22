import TGLExt.TheReservedConfirmation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O CONTORNO DE STOKES: o critério da série, o fosso, e as faces conjugadas
  [TGLExt — v161, a face em kernel do Teorema do Contorno (12/08/2026)]

O operador enfrentou Navier–Stokes 3D e a resposta do programa é: A
RESPOSTA DA SINGULARIDADE É O CONTORNO. O documento
`STOKES_A_Prova_do_Contorno.md` (custódia por sha) contém: o Teorema 1
do modelo diádico represado [PROVADO em análise clássica], a fronteira
numérica [NUMÉRICO], e o Lema da Face Conjugada [ABERTO — problema do
Milênio, EXTERNO ao programa TGL]. A pedra 113 tipa em kernel o que é
tipável HOJE:

* ★★★ `series_ratio_criterion` — O CRITÉRIO: a razão geométrica da
  série de Sobolev do Teorema 1 é menor que um ⟺ τ > ln 2 — o
  represamento provável cobra MAIS que o logaritmo da dicotomia;
* ★★ `retention_series_summable` — para τ > ln 2 a série geométrica
  converge (o fecho do Grönwall do Teorema 1 tem o seu critério em
  kernel);
* ★★★ `the_gap_typed` — O FOSSO: 2/3 < ln 2 < 0,6932 — o limiar
  marginal de Kolmogorov (2/3) e o limiar provável (ln 2) distam menos
  de 0,027 nats — o retrato do Milênio em miniatura, TIPADO;
* ★★ `half_nat_insufficient` — a meia-nat não paga o pedágio:
  1/2 < 2/3 — a taxa da fronteira cobre só três quartos do turnover;
* ★★★ `conjugate_faces_sum_to_one` — AS FACES CONJUGADAS: 1/3 + 2/3 = 1
  (queda e retenção compõem o inteiro) e o mapa: Burgers (h=0) cobra 1;
  o plano (h=1) cobra 0; o espaço (h=1/3) cobra 2/3;
* ★★ `the_provable_toll_names_the_octave` — e^{ln 2} = 2: o limiar
  provável EXPONENCIA para a própria oitava — ln 2 é o custo de UMA
  distinção binária ("o 2 conta nomes"): um bit por oitava;
* ★★★ `the_stokes_contour` — A SÍNTESE em UM teorema.

Honestidades: NADA aqui é a prova do Milênio — o Lema da Face Conjugada
segue ABERTO e é EXTERNO (não é pendência interna da TGL); o Teorema 1
completo (Grönwall/ODE) vive no documento [PROVADO em análise clássica,
não formalizado]; a leitura "a resposta é o contorno" e "um bit por
oitava" são nomeações [ONTO] sobre números exatos; β jamais literal; o
gate NÃO se move. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

open Real

/-- [KERNEL] ★★★ O CRITÉRIO DA SÉRIE: a razão geométrica 4·e^{−2τ} da
    série de Sobolev do Teorema 1 é menor que um ⟺ τ > ln 2. -/
theorem series_ratio_criterion (τ : ℝ) :
    4 * Real.exp (-(2 * τ)) < 1 ↔ Real.log 2 < τ := by
  have h4 : (4 : ℝ) = Real.exp (Real.log 4) := (Real.exp_log (by norm_num)).symm
  constructor
  · intro h
    have h1 : Real.exp (Real.log 4 + -(2 * τ)) < Real.exp 0 := by
      rw [Real.exp_add, ← h4, Real.exp_zero]
      exact h
    have h2 := Real.exp_lt_exp.mp h1
    have hl4 : Real.log 4 = 2 * Real.log 2 := by
      rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_pow]
      push_cast
      ring
    nlinarith [h2, hl4]
  · intro h
    have hl4 : Real.log 4 = 2 * Real.log 2 := by
      rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_pow]
      push_cast
      ring
    have h1 : Real.log 4 + -(2 * τ) < 0 := by nlinarith
    have h2 : Real.exp (Real.log 4 + -(2 * τ)) < Real.exp 0 :=
      Real.exp_lt_exp.mpr h1
    rw [Real.exp_add, ← h4, Real.exp_zero] at h2
    exact h2

/-- [KERNEL] ★★ A SÉRIE DO REPRESAMENTO CONVERGE para τ > ln 2: o fecho
    do Grönwall do Teorema 1 tem o seu critério em kernel. -/
theorem retention_series_summable (τ : ℝ) (h : Real.log 2 < τ) :
    Summable (fun n : ℕ => (4 * Real.exp (-(2 * τ))) ^ n) := by
  apply summable_geometric_of_lt_one
  · positivity
  · exact (series_ratio_criterion τ).mpr h

/-- [KERNEL] ★★★ O FOSSO TIPADO: 2/3 < ln 2 < 0,6932 — o limiar marginal
    de Kolmogorov e o limiar provável distam menos de 0,027 nats. -/
theorem the_gap_typed :
    (2 : ℝ) / 3 < Real.log 2 ∧ Real.log 2 - 2 / 3 < 27 / 1000 := by
  have hlo := Real.log_two_gt_d9
  have hhi := Real.log_two_lt_d9
  constructor
  · linarith [hlo]
  · linarith [hhi]

/-- [KERNEL] ★★ A MEIA-NAT É INSUFICIENTE: 1/2 < 2/3 — a taxa da
    fronteira cobre só três quartos do turnover de Kolmogorov. -/
theorem half_nat_insufficient : (1 : ℝ) / 2 < 2 / 3 := by norm_num

/-- [KERNEL] ★★★ AS FACES CONJUGADAS SOMAM UM — e o mapa: a queda h e a
    retenção 1−h compõem o inteiro; Burgers (h=0) cobra 1; o plano
    (h=1) cobra 0; o espaço (h=1/3) cobra 2/3. -/
theorem conjugate_faces_sum_to_one :
    (1 : ℝ) / 3 + 2 / 3 = 1
    ∧ (1 : ℝ) - 0 = 1
    ∧ (1 : ℝ) - 1 = 0
    ∧ (1 : ℝ) - 1 / 3 = 2 / 3 := by norm_num

/-- [KERNEL] ★★ O PEDÁGIO PROVÁVEL NOMEIA A OITAVA: e^{ln 2} = 2 —
    ln 2 é o custo de UMA distinção binária: um bit por oitava. -/
theorem the_provable_toll_names_the_octave :
    Real.exp (Real.log 2) = 2 := Real.exp_log (by norm_num)

/-- [KERNEL] ★★★ O CONTORNO DE STOKES, SÍNTESE: o critério da série, o
    fosso, a meia-nat insuficiente, as faces conjugadas e o bit da
    oitava — em UM teorema. -/
theorem the_stokes_contour :
    (∀ τ : ℝ, 4 * Real.exp (-(2 * τ)) < 1 ↔ Real.log 2 < τ)
    ∧ ((2 : ℝ) / 3 < Real.log 2 ∧ Real.log 2 - 2 / 3 < 27 / 1000)
    ∧ (1 : ℝ) / 2 < 2 / 3
    ∧ ((1 : ℝ) / 3 + 2 / 3 = 1)
    ∧ Real.exp (Real.log 2) = 2 :=
  ⟨fun τ => series_ratio_criterion τ,
   the_gap_typed,
   half_nat_insufficient,
   (conjugate_faces_sum_to_one).1,
   the_provable_toll_names_the_octave⟩

end

end TGLExt
