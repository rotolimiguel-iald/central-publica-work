-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_028 (06/09/2026), transposta em 06/09/2026
-- Lote 027..028: EQUIVALENCIA UNITARIA entre os GNS de perfis com afinidade positiva e o TRANSPORTE
--   MODULAR com dominios — Tomita do estado global Phi no Hilbert original (grafo fechado, S, J, Delta,
--   JS = Delta^{1/2} positivo auto-adjunto), grupo modular fortemente continuo que preserva fator e
--   estado, instancia nao trivial (perfil gradual: autovalor transportado 5/7); RESPOSTA GLOBAL finita
--   sem corte (familia de amplitude somavel, fiel), limite conjunto corte/tempo, contraexemplo
--   HARMONICO (entropia relativa finita com incremento modular e entropia DIVERGENTES);
--   einstein_from_summable_area_matching (condicional). Estatuto [REAL / INPUT / OPEN]: a lei de area
--   microscopica NAO foi derivada da torre (controle plano o impede); selecao fisica, H3 dinamico,
--   assinatura e globalizacao seguem INPUT/OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 20/20 + 20/20; manifestos 231/238;
--   2/2 auditores da bancada exit 0; recompilacao INDEPENDENTE 16/16, axiomas no trio; guarda de
--   colisao estatica no ROOT; enunciados lidos. Transposicao MECANICA (cabecalho + prefixo TGLExt.).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.SummableStateThermodynamics

set_option autoImplicit false
set_option maxHeartbeats 4000000
namespace ChatgptAudit.Response028
open Matrix Filter Topology Set TGLExt ChatgptAudit.Micro021
  ChatgptAudit.Profile026 ChatgptAudit.Transport027 ChatgptAudit.Thermal025
noncomputable section

def amplitudeResponse (b : SummableAmplitude) (frequency : ℝ) : ℝ :=
  -Real.log 2*amplitudeMass b*frequency^2

theorem regular_parameter_ratio (frequency t : ℝ) (ht : t≠0) :
    regularParameter (frequency*t)/t^2=frequency^2/(1+(frequency*t)^2) := by
  unfold regularParameter
  field_simp

theorem amplitude_relative_scaled_bound (b : SummableAmplitude) (frequency t : ℝ) :
    0 ≤ amplitudeRelativeEntropy b (frequency*t)/t^2 ∧
      amplitudeRelativeEntropy b (frequency*t)/t^2≤
        (9/2)*frequency^4*t^2*amplitudeSquareMass b := by
  constructor
  · exact div_nonneg (amplitude_relative_nonnegative b _) (sq_nonneg t)
  · by_cases ht : t=0
    · simp [ht]
    have hp : (regularParameter (frequency*t))^2≤(frequency*t)^4 := by
      have hn := regular_parameter_nonnegative (frequency*t)
      have hb := regular_parameter_le_square (frequency*t)
      nlinarith only [mul_nonneg (sub_nonneg.mpr hb) (add_nonneg (sq_nonneg (frequency*t)) hn)]
    have hc := mul_le_mul_of_nonneg_right
      (mul_le_mul_of_nonneg_left hp (by norm_num : (0:ℝ)≤9/2)) (amplitude_square_mass_nonnegative b)
    have h := div_le_div_of_nonneg_right ((amplitude_relative_bound b _).trans hc) (sq_nonneg t)
    have he : ((9/2)*(frequency*t)^4*amplitudeSquareMass b)/t^2=
        (9/2)*frequency^4*t^2*amplitudeSquareMass b := by
      field_simp
    rwa [he] at h

theorem amplitude_prefix_relative_scaled_bound (b : SummableAmplitude) (frequency t : ℝ) (N : ℕ) :
    0 ≤ prefixRelativeEntropy thirdThermalReference (amplitudeProfile b (frequency*t)) N/t^2 ∧
      prefixRelativeEntropy thirdThermalReference (amplitudeProfile b (frequency*t)) N/t^2≤
        (9/2)*frequency^4*t^2*amplitudeSquareMass b :=
  ⟨div_nonneg (prefix_relative_nonnegative _ _ _) (sq_nonneg t),
    (div_le_div_of_nonneg_right
      (prefix_relative_le_total _ _ (amplitude_relative_summable b _) N) (sq_nonneg t)).trans
      (amplitude_relative_scaled_bound b frequency t).2⟩

variable {α : Type} {l : Filter α}

theorem regular_parameter_ratio_along (frequency : ℝ) (time : α → ℝ)
    (ht : Tendsto time l (𝓝 0)) (hne : ∀ᶠ x in l, time x≠0) :
    Tendsto (fun x => regularParameter (frequency*time x)/(time x)^2) l (𝓝 (frequency^2)) := by
  have hd := ((ht.const_mul frequency).pow 2).const_add 1
  have h : Tendsto (fun x => frequency^2/(1+(frequency*time x)^2)) l (𝓝 (frequency^2)) := by
    have hc : Tendsto (fun _ : α => frequency^2) l (𝓝 (frequency^2)) := tendsto_const_nhds
    have hr := hc.div hd (by norm_num : (1:ℝ)+(frequency*0)^2≠0)
    change Tendsto (fun x => frequency^2/(1+(frequency*time x)^2)) l
      (𝓝 (frequency^2/(1+(frequency*0)^2))) at hr
    simpa only [mul_zero,zero_pow (by decide : 2≠0),add_zero,div_one] using hr
  apply h.congr'
  filter_upwards [hne] with x hx
  exact (regular_parameter_ratio frequency (time x) hx).symm

theorem quadratic_error_bound_tendsto (b : SummableAmplitude) (frequency : ℝ) (time : α → ℝ)
    (ht : Tendsto time l (𝓝 0)) :
    Tendsto (fun x => (9/2)*frequency^4*(time x)^2*amplitudeSquareMass b) l (𝓝 0) := by
  simpa only [zero_pow (by decide : 2≠0),mul_zero,zero_mul] using
    (((ht.pow 2).const_mul ((9/2)*frequency^4)).mul_const (amplitudeSquareMass b))

theorem amplitude_relative_quadratic_along (b : SummableAmplitude) (frequency : ℝ) (time : α → ℝ)
    (ht : Tendsto time l (𝓝 0)) :
    Tendsto (fun x => amplitudeRelativeEntropy b (frequency*time x)/(time x)^2) l (𝓝 0) :=
  squeeze_zero (fun x => (amplitude_relative_scaled_bound b frequency (time x)).1)
    (fun x => (amplitude_relative_scaled_bound b frequency (time x)).2)
    (quadratic_error_bound_tendsto b frequency time ht)

theorem amplitude_prefix_relative_quadratic_along (b : SummableAmplitude) (frequency : ℝ)
    (cutoff : α → ℕ) (time : α → ℝ) (ht : Tendsto time l (𝓝 0)) :
    Tendsto (fun x => prefixRelativeEntropy thirdThermalReference
      (amplitudeProfile b (frequency*time x)) (cutoff x)/(time x)^2) l (𝓝 0) :=
  squeeze_zero (fun x => (amplitude_prefix_relative_scaled_bound b frequency (time x) (cutoff x)).1)
    (fun x => (amplitude_prefix_relative_scaled_bound b frequency (time x) (cutoff x)).2)
    (quadratic_error_bound_tendsto b frequency time ht)

theorem amplitude_modular_quadratic_along (b : SummableAmplitude) (frequency : ℝ) (time : α → ℝ)
    (ht : Tendsto time l (𝓝 0)) (hne : ∀ᶠ x in l, time x≠0) :
    Tendsto (fun x => amplitudeModularIncrement b (frequency*time x)/(time x)^2) l
      (𝓝 (amplitudeResponse b frequency)) := by
  have h := (regular_parameter_ratio_along frequency time ht hne).const_mul (-Real.log 2*amplitudeMass b)
  have he : (fun x => amplitudeModularIncrement b (frequency*time x)/(time x)^2)=
      (fun x => (-Real.log 2*amplitudeMass b)*(regularParameter (frequency*time x)/(time x)^2)) := by
    funext x
    unfold amplitudeModularIncrement
    ring
  rw [he]
  exact h

theorem amplitude_entropy_quadratic_along (b : SummableAmplitude) (frequency : ℝ) (time : α → ℝ)
    (ht : Tendsto time l (𝓝 0)) (hne : ∀ᶠ x in l, time x≠0) :
    Tendsto (fun x => amplitudeEntropyIncrement b (frequency*time x)/(time x)^2) l
      (𝓝 (amplitudeResponse b frequency)) := by
  have h := (amplitude_modular_quadratic_along b frequency time ht hne).sub
    (amplitude_relative_quadratic_along b frequency time ht)
  have he : (fun x => amplitudeEntropyIncrement b (frequency*time x)/(time x)^2)=
      (fun x => amplitudeModularIncrement b (frequency*time x)/(time x)^2-
        amplitudeRelativeEntropy b (frequency*time x)/(time x)^2) := by
    funext x
    unfold amplitudeEntropyIncrement
    ring
  rw [he]
  simpa only [sub_zero] using h

theorem amplitude_prefix_modular_joint (b : SummableAmplitude) (frequency : ℝ)
    (cutoff : α → ℕ) (time : α → ℝ) (hN : Tendsto cutoff l atTop)
    (ht : Tendsto time l (𝓝 0)) (hne : ∀ᶠ x in l, time x≠0) :
    Tendsto (fun x => prefixModularIncrement thirdThermalReference
      (amplitudeProfile b (frequency*time x)) (cutoff x)/(time x)^2) l
      (𝓝 (amplitudeResponse b frequency)) := by
  have h := (((amplitude_prefix_tendsto b).comp hN).const_mul (-Real.log 2)).mul
    (regular_parameter_ratio_along frequency time ht hne)
  have he : (fun x => prefixModularIncrement thirdThermalReference
      (amplitudeProfile b (frequency*time x)) (cutoff x)/(time x)^2)=
      (fun x => (-Real.log 2*(∑ n∈Finset.range (cutoff x+1), b.value n))*
        (regularParameter (frequency*time x)/(time x)^2)) := by
    funext x
    rw [amplitude_prefix_modular_formula]
    ring
  rw [he]
  exact h

theorem amplitude_prefix_entropy_joint (b : SummableAmplitude) (frequency : ℝ)
    (cutoff : α → ℕ) (time : α → ℝ) (hN : Tendsto cutoff l atTop)
    (ht : Tendsto time l (𝓝 0)) (hne : ∀ᶠ x in l, time x≠0) :
    Tendsto (fun x => prefixEntropyIncrement thirdThermalReference
      (amplitudeProfile b (frequency*time x)) (cutoff x)/(time x)^2) l
      (𝓝 (amplitudeResponse b frequency)) := by
  have h := (amplitude_prefix_modular_joint b frequency cutoff time hN ht hne).sub
    (amplitude_prefix_relative_quadratic_along b frequency cutoff time ht)
  have he : (fun x => prefixEntropyIncrement thirdThermalReference
      (amplitudeProfile b (frequency*time x)) (cutoff x)/(time x)^2)=
      (fun x => prefixModularIncrement thirdThermalReference
        (amplitudeProfile b (frequency*time x)) (cutoff x)/(time x)^2-
        prefixRelativeEntropy thirdThermalReference
          (amplitudeProfile b (frequency*time x)) (cutoff x)/(time x)^2) := by
    funext x
    rw [prefix_entropy_identity]
    ring
  rw [he]
  simpa only [sub_zero] using h

theorem past_time_nonzero : ∀ᶠ t : ℝ in 𝓝[<] 0, t≠0 := by
  filter_upwards [self_mem_nhdsWithin] with t ht
  exact ne_of_lt ht

theorem amplitude_modular_quadratic_limit (b : SummableAmplitude) (frequency : ℝ) :
    Tendsto (fun t => amplitudeModularIncrement b (frequency*t)/t^2) (𝓝[<] 0)
      (𝓝 (amplitudeResponse b frequency)) :=
  amplitude_modular_quadratic_along b frequency id
    (tendsto_id'.mpr nhdsWithin_le_nhds) past_time_nonzero

theorem amplitude_relative_quadratic_limit (b : SummableAmplitude) (frequency : ℝ) :
    Tendsto (fun t => amplitudeRelativeEntropy b (frequency*t)/t^2) (𝓝[<] 0) (𝓝 0) :=
  amplitude_relative_quadratic_along b frequency id (tendsto_id'.mpr nhdsWithin_le_nhds)

theorem amplitude_entropy_quadratic_limit (b : SummableAmplitude) (frequency : ℝ) :
    Tendsto (fun t => amplitudeEntropyIncrement b (frequency*t)/t^2) (𝓝[<] 0)
      (𝓝 (amplitudeResponse b frequency)) :=
  amplitude_entropy_quadratic_along b frequency id
    (tendsto_id'.mpr nhdsWithin_le_nhds) past_time_nonzero

#print axioms regular_parameter_ratio
#print axioms amplitude_relative_scaled_bound
#print axioms amplitude_prefix_relative_scaled_bound
#print axioms regular_parameter_ratio_along
#print axioms quadratic_error_bound_tendsto
#print axioms amplitude_relative_quadratic_along
#print axioms amplitude_prefix_relative_quadratic_along
#print axioms amplitude_modular_quadratic_along
#print axioms amplitude_entropy_quadratic_along
#print axioms amplitude_prefix_modular_joint
#print axioms amplitude_prefix_entropy_joint
#print axioms past_time_nonzero
#print axioms amplitude_modular_quadratic_limit
#print axioms amplitude_relative_quadratic_limit
#print axioms amplitude_entropy_quadratic_limit
end
end ChatgptAudit.Response028
