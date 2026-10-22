/- SONDAS ADVERSARIAIS do auditor REPRO (sandbox; nao e pedra; nenhum literal de beta).
   (I)  contraexemplos aos «se e so se» quando se TIRA uma hipotese da pedra (a hipotese tem peso);
   (II) o CONTRARIO das afirmacoes centrais, refutado positivamente com os termos da pedra;
   (III) os dois lados de cada ⟺ central realizados com testemunhas NOVAS (nao as das sondas da pedra). -/
import TheUnitIsTheRank

set_option autoImplicit false

open Matrix Filter Topology
open scoped ComplexOrder

namespace TGLExt.TheUnitIsTheRank

namespace SondaRepro

noncomputable section

/-! ## (I) tirar uma hipotese quebra o ⟺ -/

/-- diag(3/5, 4/5): ⪰ 0, Tr ρ² = 1, posto 2, Tr ρ = 7/5. -/
def D35 : Matrix (Fin 2) (Fin 2) ℂ := diagonal ![((3 / 5 : ℝ) : ℂ), ((4 / 5 : ℝ) : ℂ)]

/-- [I.1 — P1.a] sem Tr ρ = 1, «ρ ⪰ 0 ⟹ (Tr ρ² = 1 ⟺ posto 1)» e FALSO (testemunha diag(3/5, 4/5)). -/
theorem P1a_sem_traco_falha :
    ¬ ∀ ρ : Matrix (Fin 2) (Fin 2) ℂ, ρ.PosSemidef → ((ρ ^ 2).trace = 1 ↔ ρ.rank = 1) := by
  intro h
  have hpsd : D35.PosSemidef := by
    refine Matrix.posSemidef_diagonal_iff.mpr ?_
    intro i
    fin_cases i
    · exact Complex.zero_le_real.mpr (by norm_num)
    · exact Complex.zero_le_real.mpr (by norm_num)
  have htr2 : (D35 ^ 2).trace = 1 := by
    rw [D35, sq, diagonal_mul_diagonal, trace_diagonal, Fin.sum_univ_two]
    simp only [Matrix.cons_val_zero, Matrix.cons_val_one]
    push_cast
    norm_num
  have hrk : D35.rank = 2 := by
    rw [rank_two_iff, D35, det_diagonal, Fin.prod_univ_two]
    simp only [Matrix.cons_val_zero, Matrix.cons_val_one]
    push_cast
    norm_num
  have h1 := (h D35 hpsd).mp htr2
  rw [hrk] at h1
  norm_num at h1

/-- [I.2 — B9.b] sem taxas positivas (g = 0), «D atua ⟺ transmite E vaza» e FALSO (θ = π/4). -/
theorem B9b_sem_taxas_positivas_falha :
    ¬ ∀ (g : Fin 2 → Fin 2 → ℝ) (θ : ℝ), (∀ i, g i i = 0) →
      (dephasingActs g θ ↔ (0 < Complex.normSq ((Smat θ).mulVec e1 0)
        ∧ 0 < Complex.normSq ((Smat θ).mulVec e1 1))) := by
  intro h
  have hT : 0 < Complex.normSq ((Smat (Real.pi / 4)).mulVec e1 0) := by
    rw [normSq_transmission, Real.cos_pi_div_four]
    positivity
  have hR : 0 < Complex.normSq ((Smat (Real.pi / 4)).mulVec e1 1) := by
    rw [normSq_reflection, Real.sin_pi_div_four]
    positivity
  obtain ⟨t, ht⟩ := (h (fun _ _ => (0 : ℝ)) (Real.pi / 4) (fun _ => rfl)).mpr ⟨hT, hR⟩
  exact ht (zero_rate_no_dephasing.1 t _)

/-- [I.3 — B5.c] sem t > 0, «posto D_t F_θ(1) = 2 ⟺ sin 2θ ≠ 0» e FALSO (t = 0, θ = π/4). -/
theorem B5c_sem_tempo_positivo_falha :
    ¬ ∀ t : ℝ, ((dephase unitRates t (rhoOut (Real.pi / 4))).rank = 2 ↔ Real.sin (2 * (Real.pi / 4)) ≠ 0) := by
  intro h
  have h0 := (h 0).mpr probe_angles.1
  rw [dephased_rank_at_zero] at h0
  norm_num at h0

/-- [I.4 — B6.a] sem g_ii = 0 (taxas todas 1), «Tr(ρ*·D_t Q_θ) = sin²θ» e FALSO (θ = π/2, t = 1). -/
theorem B6a_sem_diagonal_nula_falha :
    ¬ ∀ (g : Fin 2 → Fin 2 → ℝ) (θ t : ℝ), (rhoStar * dephase g t (Qtheta θ)).trace = (Real.sin θ : ℂ) ^ 2 := by
  intro h
  have h1 := h (fun _ _ => (1 : ℝ)) (Real.pi / 2) 1
  rw [rhoStar_eq, Matrix.trace_fin_two, dephased_Qtheta_eq, Real.sin_pi_div_two] at h1
  simp [Matrix.mul_apply, Fin.sum_univ_two] at h1
  have h2 : ((Real.exp (-1) : ℝ) : ℂ) = 1 := by
    rw [Complex.ofReal_exp]
    push_cast
    exact h1
  have h3 : Real.exp (-1) = 1 := by exact_mod_cast h2
  rw [Real.exp_eq_one_iff] at h3
  norm_num at h3

/-- [I.5 — B1.b] sem P² = P, «Tr P = posto P» e FALSO (I/2: Tr 1, posto 2). -/
theorem B1b_sem_idempotencia_falha : ¬ ∀ P : Matrix (Fin 2) (Fin 2) ℂ, P.trace = (P.rank : ℂ) := by
  intro h
  have h1 := h halfId
  rw [trace_one_not_rank_one.1, halfId_rank] at h1
  norm_num at h1

/-- [I.6 — θ_M] sem 0 ≤ β ≤ 1 (TGLCoupling), «sin² θ_M(b) = b» e FALSO (b = 4: arcsin 2 = π/2). -/
theorem thetaM_sem_limites_falha : ¬ ∀ b : ℝ, Real.sin (thetaMiguel b) ^ 2 = b := by
  intro h
  have h4 := h 4
  have hs : Real.sqrt 4 = 2 := by
    rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  rw [thetaMiguel, hs, Real.arcsin_of_one_le (by norm_num), Real.sin_pi_div_two] at h4
  norm_num at h4

/-- [I.7 — B2.a] um ⟺ ERRADO e refutado: «{Q_θ, ρ*} = 0 ⟺ cos θ = 0» falha em θ = 0. -/
theorem B2a_iff_errado_refutado : ¬ ∀ θ : ℝ, (anticomm (Qtheta θ) rhoStar = 0 ↔ Real.cos θ = 0) := by
  intro h
  have h1 := (h 0).mp anticomm_zero_at_zero
  simp at h1

/-! ## (II) o CONTRARIO, refutado com os termos da pedra -/

/-- [II.1 — B5.a] o contrario «posto D_∞ F_{π/4}(1) = 1» e falso. -/
theorem contrario_B5a_refutado : ¬ (diagExpect (rhoOut (Real.pi / 4))).rank = 1 := by
  rw [(endpoint_rank_two_iff _).mpr probe_angles.1]
  norm_num

/-- [II.2 — B2.b] o contrario «{Q_θM, ρ*} = 0» e falso para TODO acoplamento 0 < β < 1. -/
theorem contrario_B2b_refutado (c : TGLCoupling) : ¬ anticomm (Qtheta (thetaMiguel c.beta)) rhoStar = 0 :=
  (anticomm_at_thetaMiguel c).1

/-- [II.3 — B3.b] o contrario «vazamento em θ_M = 0» e falso (o vazamento e β > 0). -/
theorem contrario_B3b_refutado (c : TGLCoupling) : (rhoStar * Qtheta (thetaMiguel c.beta)).trace ≠ 0 := by
  rw [leak_at_thetaMiguel]
  exact_mod_cast c.beta_pos.ne'

/-- [II.4 — B5.e(ii)] o contrario do negativo («D preserva o posto para todo θ») e falso. -/
theorem contrario_B5e_refutado : ¬ ∀ θ : ℝ, (diagExpect (rhoOut θ)).rank = (rhoOut θ).rank := by
  intro h
  have h1 := h (Real.pi / 4)
  rw [(endpoint_rank_two_iff _).mpr probe_angles.1, (fractal_one_is_rank_one _).1] at h1
  norm_num at h1

/-- [II.5 — B7.a2] o contrario «sin²(n·2) tem limite» e falso (testemunha NOVA θ = 2). -/
theorem contrario_B7a2_refutado : ¬ ∃ L : ℝ, Tendsto (fun k : ℕ => Real.sin (k * 2) ^ 2) atTop (𝓝 L) := by
  apply angular_leak_no_limit
  exact (Real.sin_pos_of_pos_of_lt_pi (by norm_num) (by linarith [Real.pi_gt_three])).ne'

/-- [II.6 — B9.a] o contrario do negativo («transmitir sempre defasa») e falso (taxas unitarias). -/
theorem contrario_B9a_refutado :
    ¬ ∀ θ : ℝ, 0 < Complex.normSq ((Smat θ).mulVec e1 0) → dephasingActs unitRates θ :=
  literal_transmission_does_not_force_dephasing unitRates unitRates_spec.1

/-! ## (III) os dois lados de cada ⟺ central com testemunhas NOVAS -/

/-- [III.1 — B2.a] θ = π: {Q_π, ρ*} = 0; θ = 2: ≠ 0. -/
theorem lados_B2a : anticomm (Qtheta Real.pi) rhoStar = 0 ∧ anticomm (Qtheta 2) rhoStar ≠ 0 := by
  refine ⟨(anticomm_zero_iff _).mpr Real.sin_pi, fun h => ?_⟩
  have := (anticomm_zero_iff 2).mp h
  exact (Real.sin_pos_of_pos_of_lt_pi (by norm_num) (by linarith [Real.pi_gt_three])).ne' this

/-- [III.2 — B5.a/B9.b] θ = π/6: posto 2 e D atua; θ = π: posto 1 e D NAO atua (transmite, nao vaza). -/
theorem lados_B5a_B9b :
    (diagExpect (rhoOut (Real.pi / 6))).rank = 2 ∧ dephasingActs unitRates (Real.pi / 6)
    ∧ (diagExpect (rhoOut Real.pi)).rank = 1 ∧ ¬ dephasingActs unitRates Real.pi := by
  obtain ⟨hg0, h01, h10⟩ := unitRates_spec
  have hq : Real.sin (2 * (Real.pi / 6)) ≠ 0 := by
    rw [show 2 * (Real.pi / 6) = Real.pi / 3 by ring, Real.sin_pi_div_three]
    positivity
  have hz : Real.sin (2 * Real.pi) = 0 := Real.sin_two_pi
  refine ⟨(endpoint_rank_two_iff _).mpr hq, ?_, (endpoint_rank_one_iff _).mpr hz, ?_⟩
  · rw [dephasingActs_iff, dephasing_trivial_iff _ unitRates hg0 h01 h10]
    exact hq
  · rw [dephasingActs_iff, not_not, dephasing_trivial_iff _ unitRates hg0 h01 h10]
    exact hz

/-- [III.3 — P1.a] diag(1/3, 2/3): ⪰ 0, Tr 1, Tr ρ² = 5/9 ≠ 1 e posto 2 (lado falso, testemunha nova). -/
def D13 : Matrix (Fin 2) (Fin 2) ℂ := diagonal ![((1 / 3 : ℝ) : ℂ), ((2 / 3 : ℝ) : ℂ)]

theorem lados_P1a : (D13 ^ 2).trace ≠ 1 ∧ D13.rank ≠ 1 := by
  have hpsd : D13.PosSemidef := by
    refine Matrix.posSemidef_diagonal_iff.mpr ?_
    intro i
    fin_cases i
    · exact Complex.zero_le_real.mpr (by norm_num)
    · exact Complex.zero_le_real.mpr (by norm_num)
  have htr : D13.trace = 1 := by
    rw [D13, trace_diagonal, Fin.sum_univ_two]
    simp only [Matrix.cons_val_zero, Matrix.cons_val_one]
    push_cast
    norm_num
  have hrk : D13.rank = 2 := by
    rw [rank_two_iff, D13, det_diagonal, Fin.prod_univ_two]
    simp only [Matrix.cons_val_zero, Matrix.cons_val_one]
    push_cast
    norm_num
  have hr : D13.rank ≠ 1 := by rw [hrk]; norm_num
  exact ⟨fun h => hr ((pure_iff_rank_one hpsd htr).mp h), hr⟩

/-- [III.4 — θ_M com um acoplamento NOVO b = 1/3 (so satisfatibilidade; nao e β)] o vazamento e b e o ponto final tem posto 2. -/
theorem lados_thetaM_b13 :
    (rhoStar * Qtheta (thetaMiguel (1 / 3))).trace = ((1 / 3 : ℝ) : ℂ)
    ∧ (diagExpect (rhoOut (thetaMiguel (1 / 3)))).rank = 2 := by
  let c : TGLCoupling := ⟨1 / 3, by norm_num, by norm_num⟩
  exact ⟨leak_at_thetaMiguel c, (endpoint_at_thetaMiguel c).2.1⟩

end

end SondaRepro

end TGLExt.TheUnitIsTheRank

#print axioms TGLExt.TheUnitIsTheRank.SondaRepro.D35
#print axioms TGLExt.TheUnitIsTheRank.SondaRepro.P1a_sem_traco_falha
#print axioms TGLExt.TheUnitIsTheRank.SondaRepro.B9b_sem_taxas_positivas_falha
#print axioms TGLExt.TheUnitIsTheRank.SondaRepro.B5c_sem_tempo_positivo_falha
#print axioms TGLExt.TheUnitIsTheRank.SondaRepro.B6a_sem_diagonal_nula_falha
#print axioms TGLExt.TheUnitIsTheRank.SondaRepro.B1b_sem_idempotencia_falha
#print axioms TGLExt.TheUnitIsTheRank.SondaRepro.thetaM_sem_limites_falha
#print axioms TGLExt.TheUnitIsTheRank.SondaRepro.B2a_iff_errado_refutado
#print axioms TGLExt.TheUnitIsTheRank.SondaRepro.contrario_B5a_refutado
#print axioms TGLExt.TheUnitIsTheRank.SondaRepro.contrario_B2b_refutado
#print axioms TGLExt.TheUnitIsTheRank.SondaRepro.contrario_B3b_refutado
#print axioms TGLExt.TheUnitIsTheRank.SondaRepro.contrario_B5e_refutado
#print axioms TGLExt.TheUnitIsTheRank.SondaRepro.contrario_B7a2_refutado
#print axioms TGLExt.TheUnitIsTheRank.SondaRepro.contrario_B9a_refutado
#print axioms TGLExt.TheUnitIsTheRank.SondaRepro.lados_B2a
#print axioms TGLExt.TheUnitIsTheRank.SondaRepro.lados_B5a_B9b
#print axioms TGLExt.TheUnitIsTheRank.SondaRepro.D13
#print axioms TGLExt.TheUnitIsTheRank.SondaRepro.lados_P1a
#print axioms TGLExt.TheUnitIsTheRank.SondaRepro.lados_thetaM_b13
