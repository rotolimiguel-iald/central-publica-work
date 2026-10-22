import TGLExt.Ergodicity
import TGLExt.AbsoluteOne

/-!
# Auditoria (lente ESTATUTO E REGRA) da F1.TEMPO — sonda AUD-7 (só sandbox do auditor)

«para que a vida pudesse ter um lugar onde REPOUSAR e SER LEMBRADA» (S50.1). O pré-registro ancora
«repousar» em T11 (no atrator tracial ½·1 o relógio modular para) e «ser lembrada» em T5 (o dephasing guarda
a diagonal do estado inicial). AUD-7 mede a compatibilidade das duas âncoras NO MESMO ESTADO, na face finita
2×2: um estado diagonal fiel com populações DISTINTAS (o que guarda um registro distinguível) tem relógio
modular que GIRA (a coerência E₀₁ não é fixa); o relógio só para se as populações forem iguais.
Sem sorry, sem axiom, sem native_decide; a constante da casa não entra.
-/

set_option autoImplicit false

open TGLExt
open scoped Matrix ComplexOrder

namespace AudEstatutoTempo2

/-- AUD-7: populações distintas (a ≠ b, ambas > 0) ⟹ o relógio modular NÃO para (E₀₁ não é fixo por todo σ_t). -/
theorem aud_clock_runs_unless_equal_populations (a b : ℝ) (ha : 0 < a) (hb : 0 < b) (hab : a ≠ b) :
    ¬ ∀ t : ℝ, sigma (rhoD ![a, b]) t (!![0, 1; 0, 0] : Matrix (Fin 2) (Fin 2) ℂ) = !![0, 1; 0, 0] := by
  intro h
  have hd : ∀ i, 0 < (![a, b] : Fin 2 → ℝ) i := by
    intro i; fin_cases i <;> simp [ha, hb]
  have hinj : Function.Injective (![a, b] : Fin 2 → ℝ) := by
    intro i j hij
    fin_cases i <;> fin_cases j <;> simp_all
  have hfix := (sigma_fixed_iff_diag ![a, b] hd hinj _).mp h
  have h01 := congrFun (congrFun hfix 0) 1
  simp [diagExpect] at h01

/-- … e com populações iguais o relógio para (borda: é o estado tracial, ½·1 após normalizar). -/
theorem aud_clock_stops_when_equal_populations (a : ℝ) (t : ℝ) (x : Matrix (Fin 2) (Fin 2) ℂ) :
    sigma (rhoD ![a, a]) t x = x := by
  have hc : rhoD ![a, a] = (a : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [rhoD]
  exact sigma_fixed_of_commute _ _ (by rw [hc]; exact (Commute.one_left x).smul_left (a : ℂ)) t

end AudEstatutoTempo2

#print axioms AudEstatutoTempo2.aud_clock_runs_unless_equal_populations
#print axioms AudEstatutoTempo2.aud_clock_stops_when_equal_populations
