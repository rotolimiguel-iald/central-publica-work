/- SONDA do auditor REPRO (sandbox): a definicao `dephasingActs` da pedra quantifica t em TODO ℝ (o pre-registro diz
   «existe t», sem sinal). Com taxas positivas, isso e EQUIVALENTE a existir t > 0: a escolha nao altera B9.b. -/
import TheUnitIsTheRank

set_option autoImplicit false

open Matrix

namespace TGLExt.TheUnitIsTheRank

namespace SondaRepro2

theorem atua_iff_atua_em_tempo_positivo (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0)
    (h01 : 0 < g 0 1) (h10 : 0 < g 1 0) :
    dephasingActs g θ ↔ ∃ t : ℝ, 0 < t ∧ dephase g t (rhoOut θ) ≠ rhoOut θ := by
  constructor
  · intro h
    rw [dephasingActs_iff, dephasing_trivial_iff θ g hg0 h01 h10, sin_two_mul_eq_zero_iff] at h
    refine ⟨1, one_pos, fun he => ?_⟩
    have hent := congrFun (congrFun he 0) 1
    simp only [dephase, Matrix.of_apply] at hent
    have hE : (Real.exp (-(1 * g 0 1)) : ℂ) ≠ 1 := by
      intro h1
      have h2 : Real.exp (-(1 * g 0 1)) = 1 := by exact_mod_cast h1
      rw [Real.exp_eq_one_iff] at h2
      linarith
    have hz : rhoOut θ 0 1 = 0 := by
      have h3 : ((Real.exp (-(1 * g 0 1)) : ℂ) - 1) * rhoOut θ 0 1 = 0 := by
        linear_combination hent
      rcases mul_eq_zero.mp h3 with h4 | h4
      · exact absurd (sub_eq_zero.mp h4) hE
      · exact h4
    rw [rhoOut_eq] at hz
    simp only [Matrix.of_apply, Matrix.cons_val', Matrix.cons_val_zero, Matrix.cons_val_one,
      Matrix.empty_val', Matrix.cons_val_fin_one, neg_eq_zero, mul_eq_zero,
      Complex.ofReal_eq_zero] at hz
    exact h (by tauto)
  · rintro ⟨t, -, ht⟩
    exact ⟨t, ht⟩

end SondaRepro2

end TGLExt.TheUnitIsTheRank

#print axioms TGLExt.TheUnitIsTheRank.SondaRepro2.atua_iff_atua_em_tempo_positivo
