import TheTimeHasNoRank

set_option autoImplicit false

/-!
# «Provar o contrario» — tentativas DIRETAS do auditor de provar as negacoes. ESTE ARQUIVO TEM DE FALHAR:
cada `theorem` abaixo tenta provar o contrario de uma afirmacao central da pedra e deve dar ERRO.
Contagem esperada: 6 erros (um por tentativa). Se alguma tentativa compilar, a pedra (ou o kernel) e
inconsistente com ela — achado material.
-/

namespace AuditorTempoContrario

open TGLExt TGLExt.TheTimeHasNoRank
open Filter Topology
open scoped Matrix ComplexOrder

noncomputable section

/-- X1 — contrario de T1: um par 2×2 com `TH − HT = i·1` (candidato: E₀₁, E₁₀). -/
theorem x1_time_operator_exists :
    ∃ T H : Matrix (Fin 2) (Fin 2) ℂ, T * H - H * T = Complex.I • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  refine ⟨!![0, 1; 0, 0], !![0, 0; 1, 0], ?_⟩
  ext i j
  fin_cases i <;> fin_cases j <;> simp

/-- X2 — contrario de T9.a: `F(1)` do posto `diag(1,0)` e idempotente. -/
theorem x2_finite_instant_is_post : IsIdempotentElem (TheAxiomAndTheFalseWitness.axiomFlow postDiag 1) := by
  unfold IsIdempotentElem TheAxiomAndTheFalseWitness.axiomFlow postDiag
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_two]

/-- X3 — contrario de T4.b(ii): a orbita modular de ψ₊ converge (candidato: ψ₊ fixo). -/
theorem x3_angle_lands :
    ∃ z, Filter.Tendsto (fun t => sigma (rhoD ![(2 / 3 : ℝ), 1 / 3]) t psiPlus) Filter.atTop (nhds z) :=
  ⟨psiPlus, tendsto_const_nhds⟩

/-- X4 — contrario de T7.b: `T_{−1}ψ₊` e positiva. -/
theorem x4_inverse_is_positive : (dephase (gRate 1) (-1) psiPlus).PosSemidef := by
  have h := psiPlus_posSemidef
  simpa [dephase, gRate] using h

/-- X5 — contrario de T6.c: a pureza de ψ₊ nao cai em `t = 1`. -/
theorem x5_purity_constant : purityR (dephase (gRate 1) 1 psiPlus) = purityR psiPlus := by
  rw [probe_psiPlus_dephased_purity, probe_psiPlus_purity]
  norm_num

/-- X6 — contrario de T9.c: o posto `diag(1,0)` e invertivel. -/
theorem x6_post_is_unit : IsUnit postDiag := by
  rw [Matrix.isUnit_iff_isUnit_det]
  simp [postDiag]

end

end AuditorTempoContrario
