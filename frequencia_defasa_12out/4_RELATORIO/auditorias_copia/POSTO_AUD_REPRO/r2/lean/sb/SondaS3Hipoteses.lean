import TheUnitIsTheRank

/-!
# SONDA S3 (auditor REPRO r2) — PROVA QUE NÃO USA AS HIPÓTESES.
(a) as hipóteses declaradas SEM PESO (`_ha`, `_hH`): a conclusão vale sem elas (vetor NÃO normalizado; idempotente
    OBLÍQUO, não hermitiano);
(b) parâmetro logicamente supérfluo: a conclusão de `rank_not_preserved_by_dephasing` vale sem `c : TGLCoupling`;
(c) hipóteses que CARREGAM PESO: sem `g i i = 0` o negativo honesto B9.a e o B6.a deixam de valer (g ≡ 1).
Esperado: compila, 0 erros.
-/

open TGLExt TGLExt.TheUnitIsTheRank Matrix Filter Topology

/-- S3.1 (= S1'.2) — sem `c`: θ = π/4 é testemunha. -/
theorem s3_1 : ¬ ∀ θ : ℝ, (diagExpect (rhoOut θ)).rank = (rhoOut θ).rank := by
  intro h
  have h1 := h (Real.pi / 4)
  rw [(endpoint_rank_two_iff _).mpr probe_angles.1, (fractal_one_is_rank_one _).1] at h1
  exact absurd h1 (by norm_num)

/-- S3.2 — `_ha` sem peso: a = 2·e₁ (⟨a, a⟩ = 4 ≠ 1) e a compressão e a leitura valem igual. -/
theorem s3_2 (X : Matrix (Fin 2) (Fin 2) ℂ) :
    star ((2 : ℂ) • e1) ⬝ᵥ ((2 : ℂ) • e1) ≠ 1
    ∧ vecMulVec ((2 : ℂ) • e1) (star ((2 : ℂ) • e1)) * X * vecMulVec ((2 : ℂ) • e1) (star ((2 : ℂ) • e1))
        = (star ((2 : ℂ) • e1) ⬝ᵥ (X *ᵥ ((2 : ℂ) • e1))) • vecMulVec ((2 : ℂ) • e1) (star ((2 : ℂ) • e1)) := by
  refine ⟨?_, (compression_by_rank_one _ X).1⟩
  have hc : (starRingEnd ℂ) (2 : ℂ) = 2 := map_ofNat _ 2
  simp [e1, dotProduct, Fin.sum_univ_two, hc] <;> norm_num

/-- O idempotente oblíquo !![1, 1; 0, 0]. -/
def Pobl : Matrix (Fin 2) (Fin 2) ℂ := !![1, 1; 0, 0]

/-- S3.3 — `_hH` sem peso: Pobl² = Pobl, Pobl ≠ Poblᴴ, e Tr = posto = 1 vale (P4/B1.b sem hermiticidade). -/
theorem s3_3 : Pobl * Pobl = Pobl ∧ Poblᴴ ≠ Pobl ∧ Pobl.trace = (Pobl.rank : ℂ) ∧ Pobl.trace = 1 := by
  have hid : Pobl * Pobl = Pobl := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [Pobl, Matrix.mul_apply, Fin.sum_univ_two]
  refine ⟨hid, fun h => ?_, trace_eq_rank_of_projection Pobl hid, ?_⟩
  · have := congrFun (congrFun h 1) 0
    simp [Pobl, Matrix.conjTranspose_apply] at this
  · rw [Matrix.trace_fin_two]
    simp [Pobl]

/-- S3.4 — `hg0` CARREGA PESO em B9.a: com g ≡ 1 (populações também decaem) a leitura literal VALE. -/
theorem s3_4_aux (θ : ℝ) (h : 0 < Complex.normSq ((Smat θ).mulVec e1 0)) :
    dephasingActs (fun _ _ => (1 : ℝ)) θ := by
  rw [normSq_transmission] at h
  refine ⟨1, fun he => ?_⟩
  have h00 : dephase (fun _ _ => (1 : ℝ)) 1 (rhoOut θ) 0 0 = rhoOut θ 0 0 := by rw [he]
  have hF : rhoOut θ 0 0 = (Real.cos θ : ℂ) ^ 2 := by
    rw [rhoOut_eq]
    simp
  have hD : dephase (fun _ _ => (1 : ℝ)) 1 (rhoOut θ) 0 0 = (Real.exp (-1) : ℂ) * rhoOut θ 0 0 := by
    simp [dephase]
  rw [hD, hF] at h00
  have hc : (Real.cos θ : ℂ) ^ 2 ≠ 0 := by
    have : Real.cos θ ^ 2 ≠ 0 := ne_of_gt h
    exact_mod_cast this
  have hE : (Real.exp (-1) : ℂ) ≠ 1 := by
    intro h1
    have h2 : Real.exp (-1) = 1 := by exact_mod_cast h1
    rw [Real.exp_eq_one_iff] at h2
    norm_num at h2
  have h3 : ((Real.exp (-1) : ℂ) - 1) * (Real.cos θ : ℂ) ^ 2 = 0 := by linear_combination h00
  rcases mul_eq_zero.mp h3 with h4 | h4
  · exact hE (by linear_combination h4)
  · exact hc h4

theorem s3_4 :
    ¬ ∀ g : Fin 2 → Fin 2 → ℝ,
      ¬ ∀ θ : ℝ, 0 < Complex.normSq ((Smat θ).mulVec e1 0) → dephasingActs g θ :=
  fun h => h (fun _ _ => 1) (fun θ hθ => s3_4_aux θ hθ)

/-- S3.5 — `hg0` CARREGA PESO em B6.a: com g ≡ 1, θ = π/2, t = 1, Tr(ρ*·D_t Q_θ) = e^{−1} ≠ 1 = sin²θ. -/
theorem s3_5 :
    ¬ ∀ (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ) (t : ℝ), (rhoStar * dephase g t (Qtheta θ)).trace = (Real.sin θ : ℂ) ^ 2 := by
  intro h
  have hT : ∀ X : Matrix (Fin 2) (Fin 2) ℂ, (rhoStar * X).trace = X 0 0 := by
    intro X
    rw [rhoStar_eq, Matrix.trace_fin_two]
    simp [Matrix.mul_apply, Fin.sum_univ_two]
  have h1 := h (Real.pi / 2) (fun _ _ => 1) 1
  rw [hT, dephased_Qtheta_eq] at h1
  simp only [Matrix.of_apply, Matrix.cons_val', Matrix.cons_val_zero, Matrix.empty_val',
    Matrix.cons_val_fin_one, Real.sin_pi_div_two] at h1
  have h2 : Real.exp (-(1 * 1)) = 1 := by
    have : (Real.exp (-(1 * 1)) : ℂ) = 1 := by simpa using h1
    exact_mod_cast this
  rw [Real.exp_eq_one_iff] at h2
  norm_num at h2
