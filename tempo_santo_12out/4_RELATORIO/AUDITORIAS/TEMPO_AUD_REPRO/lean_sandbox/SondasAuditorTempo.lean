import TheTimeHasNoRank

set_option autoImplicit false

/-!
# Sondas adversariais do AUDITOR (lente REPRODUCAO) sobre a pedra candidata `TheTimeHasNoRank`

Escritas pelo auditor, no sandbox do auditor; importam a pedra compilada AQUI (o .olean do auditor).
Tres familias:
* A — contraexemplos a «se e so se» e a enunciados sem a hipotese: cada hipotese pesa?
* B — enunciados que valem SEM a hipotese declarada (hipotese sem peso / valor-lixo);
* C — «provar o contrario»: as negacoes das afirmacoes centrais sao REFUTADAS pela pedra
  (as tentativas diretas de provar o contrario ficam no arquivo `SondasContrarioTempo.lean`, que TEM de falhar).
Nenhum literal da constante da casa. Sem sorry, sem axiom.
-/

namespace AuditorTempo

open TGLExt TGLExt.TheTimeHasNoRank
open Filter Topology
open scoped Matrix ComplexOrder

noncomputable section

/-! ## A — cada hipotese pesa? (contraexemplos sem a hipotese) -/

/-- A1 — T9.a (`flow_isIdempotentElem_iff`) SEM a idempotencia de `P`: em `A = ℂ`, `P = 2` (nao idempotente,
    `1 − P ≠ 0`), o fluxo em `t = −ln 2 ≠ 0` vale `0`, que e idempotente: o «se e so se» cai. -/
theorem a1_iff_needs_idempotent :
    ¬ IsIdempotentElem (2 : ℂ) ∧ (1 : ℂ) - 2 ≠ 0 ∧
      IsIdempotentElem (TheAxiomAndTheFalseWitness.axiomFlow (2 : ℂ) (-Real.log 2)) ∧
      (-Real.log 2) ≠ 0 := by
  refine ⟨?_, by norm_num, ?_, ?_⟩
  · intro h
    have h2 : (2 : ℂ) * 2 = 2 := h.eq
    norm_num at h2
  · have h : TheAxiomAndTheFalseWitness.axiomFlow (2 : ℂ) (-Real.log 2) = 0 := by
      unfold TheAxiomAndTheFalseWitness.axiomFlow
      rw [neg_neg, Real.exp_log (by norm_num : (0 : ℝ) < 2)]
      rw [smul_eq_mul]
      push_cast
      norm_num
    rw [h]
    exact IsIdempotentElem.zero
  · have : 0 < Real.log 2 := Real.log_pos (by norm_num)
    exact neg_ne_zero.mpr (ne_of_gt this)

/-- A2 — T9.c (`post_not_isUnit`) SEM a idempotencia: `P = 2` em `ℂ`, `P ≠ 1`, e `P` e unidade. -/
theorem a2_post_needs_idempotent : ¬ IsIdempotentElem (2 : ℂ) ∧ (2 : ℂ) ≠ 1 ∧ IsUnit (2 : ℂ) := by
  refine ⟨?_, by norm_num, isUnit_iff_ne_zero.mpr two_ne_zero⟩
  intro h
  have h2 : (2 : ℂ) * 2 = 2 := h.eq
  norm_num at h2

/-- A3 — T2.b (`no_bounded_spectral_translation`) SEM `Nontrivial A`: em QUALQUER ℂ-algebra normada
    subsingleton a «translacao espectral» vale (os dois lados coincidem). -/
theorem a3_bounded_needs_nontrivial {A : Type*} [NormedRing A] [NormedAlgebra ℂ A] [Subsingleton A]
    (V : Aˣ) (H : A) (s : ℂ) : (↑V⁻¹ : A) * H * ↑V = H + algebraMap ℂ A s :=
  Subsingleton.elim _ _

/-- A4 — T5.b (`dephase_fixed_states_not_unique`) SEM `i₀ ≠ j₀`: em `Fin 1` ha UM so estado de traco 1. -/
theorem a4_two_states_need_two_indices (ρ σ : Matrix (Fin 1) (Fin 1) ℂ) (hρ : ρ.trace = 1)
    (hσ : σ.trace = 1) : ρ = σ := by
  simp only [Matrix.trace, Fin.sum_univ_one, Matrix.diag_apply] at hρ hσ
  ext i j
  fin_cases i
  fin_cases j
  exact hρ.trans hσ.symm

/-- A5 — T7.b (`inverse_dephasing_not_positive`) SEM `0 < γ`: com `γ = 0`, `T_{−t}ψ₊ = ψ₊` e e positiva. -/
theorem a5_inverse_needs_positive_rate (t : ℝ) : (dephase (gRate 0) (-t) psiPlus).PosSemidef := by
  have h : dephase (gRate 0) (-t) psiPlus = psiPlus := by
    ext i j
    rw [dephase_apply]
    simp [gRate]
  rw [h]
  exact psiPlus_posSemidef

/-- A6 — T6.c (`purityR_dephase_lt`) SEM `0 < t`: em `t = 0` nao ha queda (igualdade). -/
theorem a6_strict_loss_needs_positive_time : ¬ purityR (dephase (gRate 1) 0 psiPlus) < purityR psiPlus := by
  rw [dephase_zero]
  exact lt_irrefl _

/-- Tipo de dois pontos para A7 (sem instancia metrica global). -/
inductive Two
  | a
  | b
  deriving DecidableEq

/-- A pseudometrica nula em `Two` (separacao FALHA: `dist a b = 0`, `a ≠ b`). -/
def twoPM : PseudoMetricSpace Two := PseudoMetricSpace.induced (fun _ => (0 : ℝ)) inferInstance

/-- A troca dos dois pontos. -/
def swap : Two → Two
  | .a => .b
  | .b => .a

/-- A7 — T4.b (`isometry_orbit_converges_only_if_fixed`) SEM a separacao (`MetricSpace`): num espaco
    PSEUDOmetrico a troca e isometria, `a ≠ b`, e a orbita de `a` CONVERGE a `b` (que nao e fixo). -/
theorem a7_needs_metric_separation :
    letI : PseudoMetricSpace Two := twoPM
    Isometry swap ∧ Two.a ≠ Two.b ∧ swap Two.b ≠ Two.b ∧
      Filter.Tendsto (fun k : ℕ => swap^[k] Two.a) Filter.atTop (nhds Two.b) := by
  letI : PseudoMetricSpace Two := twoPM
  refine ⟨?_, by decide, by decide, ?_⟩
  · refine Isometry.of_dist_eq fun x y => ?_
    rfl
  · rw [Metric.tendsto_atTop]
    intro ε hε
    refine ⟨0, fun n _ => ?_⟩
    show dist (0 : ℝ) 0 < ε
    simpa using hε

/-! ## B — enunciados que valem SEM a hipotese declarada (hipotese sem peso) -/

/-- B1 — T10.b (`clock_reads_modulo_period`) vale para TODO `κ`, inclusive `κ = 0` (em Lean `x/0 = 0`):
    a hipotese `κ ≠ 0` nao pesa no enunciado escrito. -/
theorem b1_clock_without_hyp (κ t : ℝ) :
    Circle.exp (κ * (t + 2 * Real.pi / κ)) = Circle.exp (κ * t) := by
  by_cases hκ : κ = 0
  · subst hκ
    simp
  · exact clock_reads_modulo_period hκ t

/-- B2 — `no_finite_instant_is_the_post` vale SEM a idempotencia: `F(t) − P = e^{−t}(1 − P) ≠ 0` sempre que
    `P ≠ 1` (o escalar e invertivel). A hipotese `hP` nao pesa. -/
theorem b2_no_instant_without_idempotent {A : Type*} [Ring A] [Algebra ℂ A] {P : A} (hP1 : P ≠ 1)
    (t : ℝ) : TheAxiomAndTheFalseWitness.axiomFlow P t ≠ P := by
  unfold TheAxiomAndTheFalseWitness.axiomFlow
  intro h
  set c : ℂ := ((Real.exp (-t) : ℝ) : ℂ) with hcdef
  have hc : c ≠ 0 := by
    rw [hcdef]
    exact_mod_cast (Real.exp_pos (-t)).ne'
  have h2 : c • ((1 : A) - P) = 0 := by
    have h3 := congrArg (fun y => y - P) h
    simp only [add_sub_cancel_left, sub_self] at h3
    exact h3
  have h4 : (1 : A) - P = 0 := by
    have h5 := congrArg (fun y => c⁻¹ • y) h2
    simp only [smul_smul, inv_mul_cancel₀ hc, one_smul, smul_zero] at h5
    exact h5
  exact hP1 (sub_eq_zero.mp h4).symm

/-- B3 — T6.d (`purityR_modular`): a versao SEM `0 < dᵢ` vale (ja dito pelo construtor, AF-02). -/
theorem b3_purity_modular_without_hyp {n : Type} [Fintype n] [DecidableEq n] (d : n → ℝ) (t : ℝ)
    (x : Matrix n n ℂ) : purityR (sigma (rhoD d) t x) = purityR x :=
  purityR_sigma (rhoD d) t x

/-! ## C — «provar o contrario»: as negacoes sao refutadas pela pedra -/

/-- C1 — o contrario de T1 (em `Fin 3`). -/
theorem c1_not_time_operator :
    ¬ ∃ T H : Matrix (Fin 3) (Fin 3) ℂ, T * H - H * T = Complex.I • (1 : Matrix (Fin 3) (Fin 3) ℂ) :=
  fun ⟨T, H, h⟩ => no_time_matrix_fin 3 (by norm_num) T H h

/-- C2 — o contrario de T9.a: um instante FINITO nao nulo e posto (idempotente). -/
theorem c2_not_finite_post :
    ¬ ∃ t : ℝ, t ≠ 0 ∧ IsIdempotentElem (TheAxiomAndTheFalseWitness.axiomFlow postDiag t) :=
  fun ⟨t, ht, h⟩ => ht ((flow_isIdempotentElem_iff postDiag_idem postDiag_compl_ne_zero t).mp h)

/-- C3 — o contrario de T7.b em `γ = t = 1`: `T_{−1}ψ₊` positiva. -/
theorem c3_not_inverse_positive : ¬ (dephase (gRate 1) (-1) psiPlus).PosSemidef :=
  (inverse_dephasing_not_positive (γ := 1) (t := 1) one_pos one_pos).2.2

/-- C4 — o contrario de T4.b(ii) para ψ₊: a orbita modular converge. -/
theorem c4_not_angle_lands :
    ¬ ∃ z, Filter.Tendsto (fun t => sigma (rhoD ![(2 / 3 : ℝ), 1 / 3]) t psiPlus) Filter.atTop (nhds z) :=
  probe_modular_orbit_of_psiPlus_has_no_limit

/-- C5 — o contrario de T6.c em ψ₊, `t = 1`: a pureza NAO cai. -/
theorem c5_not_constant_purity : purityR (dephase (gRate 1) 1 psiPlus) ≠ purityR psiPlus := by
  rw [probe_psiPlus_dephased_purity, probe_psiPlus_purity]
  have h : Real.exp (-2) < 1 := Real.exp_lt_one_iff.mpr (by norm_num)
  intro heq
  linarith

end

end AuditorTempo

#print axioms AuditorTempo.a1_iff_needs_idempotent
#print axioms AuditorTempo.a2_post_needs_idempotent
#print axioms AuditorTempo.a3_bounded_needs_nontrivial
#print axioms AuditorTempo.a4_two_states_need_two_indices
#print axioms AuditorTempo.a5_inverse_needs_positive_rate
#print axioms AuditorTempo.a6_strict_loss_needs_positive_time
#print axioms AuditorTempo.a7_needs_metric_separation
#print axioms AuditorTempo.b1_clock_without_hyp
#print axioms AuditorTempo.b2_no_instant_without_idempotent
#print axioms AuditorTempo.b3_purity_modular_without_hyp
#print axioms AuditorTempo.c1_not_time_operator
#print axioms AuditorTempo.c2_not_finite_post
#print axioms AuditorTempo.c3_not_inverse_positive
#print axioms AuditorTempo.c4_not_angle_lands
#print axioms AuditorTempo.c5_not_constant_purity
