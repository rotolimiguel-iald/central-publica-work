import Mathlib
import TheTimeHasNoRank

/-!
Sondas adversariais do AUDITOR CÉTICO (lente REPRODUÇÃO), F1.TEMPO — arquivo que DEVE compilar (EXIT 0).
Importa o .olean da pedra recompilado no sandbox do auditor. Nada aqui entra no kernel do Nós.
S1  o contrário de T1 (existe par de Weyl em M₂) é REFUTÁVEL a partir da pedra;
S2  sem `Nonempty ι` o enunciado de T1.a é FALSO (Fin 0): a hipótese pesa, não é peso morto;
S3  CONTRAEXEMPLO ao «se e só se» T9.a quando se retira `IsIdempotentElem P`: com P = 2·1 em ℂ, F(−log 2) = 0
    é idempotente e −log 2 ≠ 0 — a hipótese de idempotência do iff é necessária;
S4  sem `x i₀ j₀ ≠ 0` (x = 0) e sem `0 < t` (t = 0) a queda ESTRITA de T6.c é FALSA: as duas hipóteses pesam;
S5  o contrário de T6.c para ψ₊ (pureza constante) é refutável; o contrário de T11.a é refutável;
S6  sem `∃ i j, 0 < g i j` a contração de T4.c é FALSA (g = 0 dá volume 1).
-/

set_option autoImplicit false
open TGLExt TGLExt.TheTimeHasNoRank

noncomputable section

/-- S1 -/
theorem aud_S1_no_weyl_pair_in_M2 :
    ¬ ∃ T H : Matrix (Fin 2) (Fin 2) ℂ, T * H - H * T = Complex.I • (1 : Matrix (Fin 2) (Fin 2) ℂ) :=
  fun ⟨T, H, h⟩ => no_time_matrix_fin 2 (by norm_num) T H h

/-- S2 -/
theorem aud_S2_nonempty_is_necessary :
    ¬ ∀ {ι : Type} [Fintype ι] [DecidableEq ι] (T H : Matrix ι ι ℂ) {c : ℂ}, c ≠ 0 →
        T * H - H * T ≠ c • (1 : Matrix ι ι ℂ) :=
  fun h => h (ι := Fin 0) 0 0 Complex.I_ne_zero (by ext i; exact i.elim0)

/-- S3 (cálculo): com P = 2 em ℂ, F(−log 2) = 2 + e^{log 2}·(1 − 2) = 0. -/
theorem aud_S3_flow_of_two_at_minus_log_two :
    TheAxiomAndTheFalseWitness.axiomFlow (2 : ℂ) (-(Real.log 2)) = 0 := by
  unfold TheAxiomAndTheFalseWitness.axiomFlow
  rw [neg_neg, Real.exp_log two_pos]
  push_cast
  ring

/-- S3: o «se e só se» de T9.a FALHA sem a idempotência: F(t) idempotente com t ≠ 0. -/
theorem aud_S3_iff_fails_without_idempotence :
    ∃ (P : ℂ) (t : ℝ), (1 : ℂ) - P ≠ 0 ∧
      IsIdempotentElem (TheAxiomAndTheFalseWitness.axiomFlow P t) ∧ t ≠ 0 :=
  ⟨2, -(Real.log 2), by norm_num,
    by rw [aud_S3_flow_of_two_at_minus_log_two]; exact IsIdempotentElem.zero,
    by have := Real.log_pos (show (1 : ℝ) < 2 by norm_num); linarith⟩

/-- S4a: dephase de 0 é 0. -/
theorem aud_S4_dephase_zero_matrix {n : Type} [Fintype n] [DecidableEq n] (g : n → n → ℝ) (t : ℝ) :
    dephase g t (0 : Matrix n n ℂ) = 0 := by
  ext i j; simp [dephase]

/-- S4a: sem `x i₀ j₀ ≠ 0` a queda estrita é FALSA (x = 0). -/
theorem aud_S4_strict_fails_for_zero_state :
    ¬ purityR (dephase (gRate 1) 1 (0 : Matrix (Fin 2) (Fin 2) ℂ)) < purityR (0 : Matrix (Fin 2) (Fin 2) ℂ) := by
  rw [aud_S4_dephase_zero_matrix]; exact lt_irrefl _

/-- S4b: sem `0 < t` a queda estrita é FALSA (t = 0, mesmo com ψ₊). -/
theorem aud_S4_strict_fails_at_time_zero :
    ¬ purityR (dephase (gRate 1) 0 psiPlus) < purityR psiPlus := by
  rw [dephase_zero]; exact lt_irrefl _

/-- S5a: o contrário de T6.c para ψ₊ (pureza constante sob defasagem) é refutável. -/
theorem aud_S5_purity_not_constant_for_psiPlus :
    purityR (dephase (gRate 1) 1 psiPlus) ≠ purityR psiPlus :=
  ne_of_lt (purityR_dephase_lt (gRate 1) (gRate_nonneg zero_le_one) one_pos psiPlus
    (i₀ := 0) (j₀ := 1) (by rw [gRate_01]; exact one_pos) psiPlus_01_ne_zero)

/-- S5b: o contrário de T11.a é refutável. -/
theorem aud_S5_half_identity_contrary_refuted :
    ¬ ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) ≠ absoluteRho (Fin 2)) :=
  fun h => h half_identity_is_absoluteRho_two

/-- S6: sem taxa positiva a contração de volume de T4.c é FALSA (g = 0 ⟹ e^{0} = 1, não < 1). -/
theorem aud_S6_contraction_needs_positive_rate :
    ¬ Real.exp (-((1 : ℝ) * ∑ i : Fin 2, ∑ j : Fin 2, (fun _ _ : Fin 2 => (0 : ℝ)) i j)) < 1 := by
  simp

end

#print axioms aud_S1_no_weyl_pair_in_M2
#print axioms aud_S2_nonempty_is_necessary
#print axioms aud_S3_iff_fails_without_idempotence
#print axioms aud_S4_strict_fails_for_zero_state
#print axioms aud_S4_strict_fails_at_time_zero
#print axioms aud_S5_purity_not_constant_for_psiPlus
#print axioms aud_S5_half_identity_contrary_refuted
#print axioms aud_S6_contraction_needs_positive_rate
