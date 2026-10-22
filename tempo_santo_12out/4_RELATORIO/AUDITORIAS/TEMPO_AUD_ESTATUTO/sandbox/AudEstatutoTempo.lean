import TheTimeHasNoRank

/-!
# Auditoria (lente ESTATUTO E REGRA) da pedra candidata `TheTimeHasNoRank` — F1.TEMPO, 12/10/2026

Arquivo do AUDITOR, só no sandbox da auditoria. Importa o .olean da pedra compilado aqui (mesma fonte,
sha256 7105eda4…). Nada aqui é pedra nem candidato: são SONDAS de estatuto, para medir o PESO de nomes.
Sem sorry, sem axiom, sem native_decide. A constante da casa não entra.

* AUD-1 — a cláusula Ágape é propriedade de `e^{−s}`: a multiplicação escalar no MESMO tipo
  (Mₙ(ℂ)) também é `DualScalingData` e herda as seis cláusulas. A ponte T8 é válida, mas o seu conteúdo
  específico do dephasing está só em T8.c (o registro não escala), não nas seis cláusulas.
* AUD-2 — o boost (det 1, regime hiperbólico da tabela da casa) NÃO tem atrator global: com
  `global_attractor_needs_volume_loss` (T4.f da pedra) e `boost_det`. Logo «pousar como bacia» (dissipação,
  det < 1) e «pousar no raio nulo» (hiperbólico, det 1) são mecanismos distintos.
* AUD-3 — T9 é genérico: em QUALQUER anel, um elemento de um grupo a um parâmetro idempotente é 1.
* AUD-4 — `time_is_the_modular_flow` vale para ρ = 1, cujo fluxo é a identidade: o enunciado não garante
  tempo algum (o nome carrega a hipótese do tempo térmico, que a própria pedra recusa afirmar).
* AUD-5 — no discreto, sem invertibilidade, um passo finito PODE ser posto: R = J/2 é idempotente (é o canal
  ótico em λ = 0). «Nenhum instante finito é posto» depende da invertibilidade (grupo), não do «tempo».
* AUD-6 — homônimo POSTO = RANK: o estado-atrator ótico ½·1 tem posto 2 e pureza ½; o posto 1 está na
  leitura-limite R (o mapa), não no estado.
-/

set_option autoImplicit false

open TGLExt TGLExt.TheTimeHasNoRank
open scoped Matrix ComplexOrder

namespace AudEstatutoTempo

/-! ## Tipos elaborados dos nomes que carregam leitura -/
#check @TGLExt.TheTimeHasNoRank.time_is_the_modular_flow
#check @TGLExt.TheTimeHasNoRank.the_time_has_no_rank
#check @TGLExt.TheTimeHasNoRank.flow_full_rank
#check @TGLExt.TheTimeHasNoRank.optical_attractor_is_the_absolute_one
#check @TGLExt.TheTimeHasNoRank.optical_attractor_clock_stops
#check @TGLExt.TheTimeHasNoRank.probe_bounded_spectral_translation
#check @TGLExt.TheTimeHasNoRank.purityR_modular
#check @TGLExt.TheTimeHasNoRank.coherenceScaling
#check @TGLExt.TheTimeHasNoRank.the_two_regimes_of_time
#check @TGLExt.DualScalingData.mk

/-! ## AUD-1 — a Ágape é a lei de `e^{−s}`, não do dephasing -/

/-- A multiplicação escalar `x ↦ e^{−s}·x` com `τ(x) = ‖x₀₁‖`: outra instância no MESMO tipo. -/
noncomputable def scalarScaling : DualScalingData (Matrix (Fin 2) (Fin 2) ℂ) where
  tau := fun x => ‖x 0 1‖
  theta := fun s x => (((Real.exp (-s)) : ℝ) : ℂ) • x
  scaling := fun s x => by
    show ‖((((Real.exp (-s)) : ℝ) : ℂ) • x) 0 1‖ = Real.exp (-s) * ‖x 0 1‖
    rw [Matrix.smul_apply, smul_eq_mul, norm_mul, Complex.norm_real, Real.norm_eq_abs,
      abs_of_pos (Real.exp_pos _)]

/-- As seis cláusulas da Ágape valem para a multiplicação escalar (que NÃO preserva o traço). -/
theorem aud_scalar_obeys_agape (x : Matrix (Fin 2) (Fin 2) ℂ) (hx : x 0 1 ≠ 0) :
    let D := scalarScaling
    (∀ s : ℝ, s ≠ 0 → ∀ m' : Matrix (Fin 2) (Fin 2) ℂ, D.theta s m' = m' → D.tau m' = 0) ∧
    (∀ s : ℝ, D.tau (D.theta s x) < D.tau (D.theta (s - 1) x)) ∧
    (∀ B : ℝ, ∃ s : ℝ, B < D.tau (D.theta s x)) ∧
    (∀ s : ℝ, 0 < D.tau (D.theta s x)) ∧
    (∀ ε : ℝ, 0 < ε → ∃ s : ℝ, D.tau (D.theta s x) < ε) ∧
    (∀ a : ℝ, Real.exp (-a) = 1 ↔ a = 0) := by
  intro D
  exact TGLExt.Fundacao.agape D (m := x) (norm_pos_iff.mpr hx)

/-- … e a multiplicação escalar apaga o registro (o traço cai), ao contrário do dephasing (T8.c, `dephase_preserves_trace`). -/
theorem aud_scalar_erases_the_record :
    (scalarScaling.theta 1 (1 : Matrix (Fin 2) (Fin 2) ℂ)).trace ≠ (1 : Matrix (Fin 2) (Fin 2) ℂ).trace := by
  show ((((Real.exp (-1)) : ℝ) : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)).trace ≠ (1 : Matrix (Fin 2) (Fin 2) ℂ).trace
  rw [Matrix.trace_smul, Matrix.trace_one, smul_eq_mul]
  intro h
  have h2 : (((Real.exp (-1)) : ℝ) : ℂ) = 1 := by
    have hc : ((Fintype.card (Fin 2) : ℕ) : ℂ) ≠ 0 := by norm_num
    exact mul_right_cancel₀ hc (by rw [h, one_mul])
  have h3 : Real.exp (-1) = 1 := by exact_mod_cast h2
  have h4 := (Real.exp_eq_one_iff (-1)).mp h3
  norm_num at h4

/-! ## AUD-2 — o hiperbólico (det 1) não tem atrator global -/

theorem aud_boost_has_no_global_attractor (s : ℝ) :
    ¬ ∀ v : Fin 2 → ℝ,
      Filter.Tendsto (fun k : ℕ => ((TGLExt.boost s) ^ k).mulVec v) Filter.atTop (nhds 0) := by
  intro h
  have h1 := global_attractor_needs_volume_loss (TGLExt.boost s) h (by norm_num)
  rw [TGLExt.boost_det] at h1
  norm_num at h1

/-! ## AUD-3 — T9 é a lei de grupo: nenhum elemento de grupo a um parâmetro é idempotente ≠ 1 -/

theorem aud_group_element_idempotent_is_one {A : Type*} [Ring A] (F : ℝ → A)
    (h0 : F 0 = 1) (hadd : ∀ s t, F (s + t) = F s * F t) (t : ℝ)
    (hidem : IsIdempotentElem (F t)) : F t = 1 := by
  have hu : F t * F (-t) = 1 := by rw [← hadd, add_neg_cancel, h0]
  calc F t = F t * (F t * F (-t)) := by rw [hu, mul_one]
    _ = (F t * F t) * F (-t) := by rw [mul_assoc]
    _ = F t * F (-t) := by rw [hidem.eq]
    _ = 1 := hu

/-! ## AUD-4 — o «teorema do tempo» vale para o fluxo congelado -/

theorem aud_time_theorem_holds_for_frozen_flow :
    (∀ (t : ℝ) (a : Matrix (Fin 2) (Fin 2) ℂ), sigma (1 : Matrix (Fin 2) (Fin 2) ℂ) t a = a) ∧
    (∀ (s t : ℝ) (a : Matrix (Fin 2) (Fin 2) ℂ),
      sigma (1 : Matrix (Fin 2) (Fin 2) ℂ) s (sigma 1 t a) = sigma 1 (s + t) a) :=
  ⟨fun t a => sigma_fixed_of_commute _ _ (Commute.one_left _) t,
   (time_is_the_modular_flow (1 : Matrix (Fin 2) (Fin 2) ℂ) Matrix.PosDef.one).2.1⟩

/-! ## AUD-5 — no discreto não invertível, um passo É posto -/

theorem aud_discrete_step_can_be_a_post :
    IsIdempotentElem (!![1 / 2, 1 / 2; 1 / 2, 1 / 2] : Matrix (Fin 2) (Fin 2) ℝ) := by
  unfold IsIdempotentElem
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_two] <;> norm_num

/-! ## AUD-6 — POSTO = RANK: o estado-atrator tem posto 2 e pureza ½ -/

theorem aud_attractor_state_has_full_rank :
    ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)).rank = 2 := by
  have hu : IsUnit ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)) := by
    rw [Matrix.isUnit_iff_isUnit_det, Matrix.det_smul, Matrix.det_one, mul_one, isUnit_iff_ne_zero]
    norm_num
  rw [Matrix.rank_of_isUnit _ hu, Fintype.card_fin]

theorem aud_attractor_state_purity_half :
    purityR ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)) = 1 / 2 := by
  unfold purityR
  simp only [Fin.sum_univ_two, Matrix.smul_apply, Matrix.one_apply_eq, smul_eq_mul]
  rw [Matrix.one_apply_ne (by decide : (0 : Fin 2) ≠ 1), Matrix.one_apply_ne (by decide : (1 : Fin 2) ≠ 0)]
  simp [Complex.normSq_apply]
  norm_num

end AudEstatutoTempo

#print axioms AudEstatutoTempo.scalarScaling
#print axioms AudEstatutoTempo.aud_scalar_obeys_agape
#print axioms AudEstatutoTempo.aud_scalar_erases_the_record
#print axioms AudEstatutoTempo.aud_boost_has_no_global_attractor
#print axioms AudEstatutoTempo.aud_group_element_idempotent_is_one
#print axioms AudEstatutoTempo.aud_time_theorem_holds_for_frozen_flow
#print axioms AudEstatutoTempo.aud_discrete_step_can_be_a_post
#print axioms AudEstatutoTempo.aud_attractor_state_has_full_rank
#print axioms AudEstatutoTempo.aud_attractor_state_purity_half
#print axioms TGLExt.TheTimeHasNoRank.the_time_has_no_rank
#print axioms TGLExt.TheTimeHasNoRank.the_two_regimes_of_time
#print axioms TGLExt.TheTimeHasNoRank.the_coherence_obeys_agape
#print axioms TGLExt.TheTimeHasNoRank.time_is_the_modular_flow
