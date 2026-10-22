import TheUnitIsTheRank

/-!
# SONDA S2 (auditor REPRO r2) — CONTRAEXEMPLO A UM «SE E SÓ SE».
Cada ⟺ da pedra vale sob as SUAS hipóteses (compilado). Aqui se busca o contraexemplo quando uma hipótese cai:
se o ⟺ continuasse valendo sem ela, a hipótese seria decorativa. Esperado: compila, 0 erros (cada teorema abaixo
é a NEGAÇÃO do ⟺ sem a hipótese, com testemunha explícita).
-/

open TGLExt TGLExt.TheUnitIsTheRank Matrix Filter Topology

/-- S2.1 — B9.b sem taxas positivas (g = 0): θ = π/4 transmite E vaza, mas D não atua. -/
theorem s2_1 :
    ¬ ∀ (g : Fin 2 → Fin 2 → ℝ) (θ : ℝ), (∀ i, g i i = 0) →
      (dephasingActs g θ ↔
        (0 < Complex.normSq ((Smat θ).mulVec e1 0) ∧ 0 < Complex.normSq ((Smat θ).mulVec e1 1))) := by
  intro h
  have h1 := (h (fun _ _ => 0) (Real.pi / 4) (fun _ => rfl)).mpr (by
    rw [normSq_transmission, normSq_reflection, Real.cos_pi_div_four, Real.sin_pi_div_four]
    constructor <;> positivity)
  obtain ⟨t, ht⟩ := h1
  apply ht
  ext i j
  simp [dephase]

/-- S2.2 — B5.c sem t > 0: em t = 0, θ = π/4, posto 1 mas sin 2θ ≠ 0. -/
theorem s2_2 :
    ¬ ∀ t : ℝ, ((dephase unitRates t (rhoOut (Real.pi / 4))).rank = 2 ↔ Real.sin (2 * (Real.pi / 4)) ≠ 0) := by
  intro h
  have h0 := (h 0).mpr probe_angles.1
  rw [dephased_rank_at_zero] at h0
  exact absurd h0 (by norm_num)

/-- S2.3 — P1.b sem Tr M = 1: M = 2ρ* tem posto 1 e Tr M² = 4. -/
theorem s2_3 : ¬ ∀ M : Matrix (Fin 2) (Fin 2) ℂ, ((M ^ 2).trace = 1 ↔ M.rank = 1) := by
  intro h
  have hr : ((2 : ℂ) • rhoStar).rank = 1 := by
    rw [rank_one_iff_fin_two]
    refine ⟨fun h0 => ?_, ?_⟩
    · have := congrFun (congrFun h0 0) 0
      simp [rhoStar] at this
    · rw [Matrix.det_smul, rhoStar_det]
      simp
  have htr : (((2 : ℂ) • rhoStar) ^ 2).trace = 4 := by
    rw [smul_pow, Matrix.trace_smul, sq rhoStar, rhoStar_idem, rhoStar_trace]
    norm_num
  have := (h ((2 : ℂ) • rhoStar)).mpr hr
  rw [htr] at this
  norm_num at this

/-- S2.4 — B5.b sem b ∈ [0, 1]: b = 2 dá posto 2 sem 0 < b < 1. -/
theorem s2_4 : ¬ ∀ b : ℝ, ((diagonal ![((1 - b : ℝ) : ℂ), (b : ℂ)]).rank = 2 ↔ (0 < b ∧ b < 1)) := by
  intro h
  have hr : (diagonal ![((1 - 2 : ℝ) : ℂ), ((2 : ℝ) : ℂ)]).rank = 2 := by
    rw [rank_two_iff, det_diagonal, Fin.prod_univ_two]
    simp only [Matrix.cons_val_zero, Matrix.cons_val_one]
    norm_num
  have := ((h 2).mp hr).2
  norm_num at this

/-- S2.5 — B8.b em θ_M(b) sem b ≤ 1: b = 2 (arcsin satura em π/2) dá sin 2θ = 0 sem b ∈ {0, 1}. -/
theorem s2_5 : ¬ ∀ b : ℝ, 0 ≤ b → (Real.sin (2 * thetaMiguel b) = 0 ↔ b = 0 ∨ b = 1) := by
  intro h
  have hθ : thetaMiguel 2 = Real.pi / 2 := by
    unfold thetaMiguel
    exact Real.arcsin_of_one_le (Real.one_le_sqrt.mpr (by norm_num))
  have hs : Real.sin (2 * thetaMiguel 2) = 0 := by
    rw [hθ, show 2 * (Real.pi / 2) = Real.pi by ring, Real.sin_pi]
  rcases (h 2 (by norm_num)).mp hs with h2 | h2 <;> norm_num at h2

/-- S2.6 — B8.b em θ_M(b) sem 0 ≤ b: b = −1 (√ de negativo = 0) dá sin 2θ = 0 sem b ∈ {0, 1}. -/
theorem s2_6 : ¬ ∀ b : ℝ, b ≤ 1 → (Real.sin (2 * thetaMiguel b) = 0 ↔ b = 0 ∨ b = 1) := by
  intro h
  have hθ : thetaMiguel (-1) = 0 := by
    unfold thetaMiguel
    rw [Real.sqrt_eq_zero_of_nonpos (by norm_num), Real.arcsin_zero]
  have hs : Real.sin (2 * thetaMiguel (-1)) = 0 := by
    rw [hθ, mul_zero, Real.sin_zero]
  rcases (h (-1) (by norm_num)).mp hs with h2 | h2 <;> norm_num at h2

/-- S2.7 — os dois polos do ⟺ de B2.a computados nos pontos de borda θ = π (sin = 0: nulo) e θ = π/2 (não nulo). -/
theorem s2_7 : anticomm (Qtheta Real.pi) rhoStar = 0 ∧ anticomm (Qtheta (Real.pi / 2)) rhoStar ≠ 0 :=
  ⟨(anticomm_zero_iff _).mpr Real.sin_pi,
   fun h => by
     have := (anticomm_zero_iff _).mp h
     rw [Real.sin_pi_div_two] at this
     norm_num at this⟩

/-- S2.8 — o polo θ = π/2 de B5.a (reflexão total): posto 1 do ponto final, sem defasagem. -/
theorem s2_8 : (diagExpect (rhoOut (Real.pi / 2))).rank = 1 ∧ ¬ dephasingActs unitRates (Real.pi / 2) :=
  ⟨(endpoint_rank_one_at_poles).2.2, (leak_without_dephasing_at_half_pi unitRates unitRates_spec.1).2⟩
