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
import TGLExt.ProfileEntropyLimits

set_option autoImplicit false
set_option maxHeartbeats 4000000
namespace ChatgptAudit.Response028
open Matrix Filter Topology Set TGLExt ChatgptAudit.Micro021
  ChatgptAudit.Profile026 ChatgptAudit.Transport027 ChatgptAudit.Thermal025
noncomputable section

theorem harmonic_shift_square_summable :
    Summable (fun n => (gradualProfile.w n-1/3)^2) := by
  apply gradual_profile_square_summable.congr
  intro n
  change (1/3-gradualProfile.w n)^2=(gradualProfile.w n-1/3)^2
  ring

theorem harmonic_relative_summable :
    Summable (siteRelativeEntropy thirdThermalReference gradualProfile) :=
  third_relative_sites_summable gradualProfile harmonic_shift_square_summable

theorem harmonic_relative_limit :
    Tendsto (prefixRelativeEntropy thirdThermalReference gradualProfile) atTop
      (𝓝 (profileRelativeTotal thirdThermalReference gradualProfile)) :=
  prefix_relative_tendsto _ _ harmonic_relative_summable

theorem harmonic_shift_diverges :
    Tendsto (fun N => ∑ n∈Finset.range (N+1), (gradualProfile.w n-1/3)) atTop atTop := by
  have hn : ¬Summable (fun n => gradualProfile.w n-1/3) := gradual_profile_diff_not_summable
  have hp : ∀ n, 0 ≤ gradualProfile.w n-1/3 := by
    intro n
    change 0 ≤ gradualProfile.w n-thirdThermalReference.w n
    rw [gradual_profile_diff]
    positivity
  exact ((not_summable_iff_tendsto_nat_atTop_of_nonneg hp).mp hn).comp (tendsto_add_atTop_nat 1)

theorem harmonic_modular_diverges :
    Tendsto (prefixModularIncrement thirdThermalReference gradualProfile) atTop atTop := by
  have h := Tendsto.const_mul_atTop (Real.log_pos (by norm_num : (1:ℝ)<2)) harmonic_shift_diverges
  change Tendsto (fun N => prefixModularIncrement thirdThermalReference gradualProfile N) _ _
  simpa only [third_prefix_modular_formula] using h

theorem harmonic_entropy_diverges :
    Tendsto (prefixEntropyIncrement thirdThermalReference gradualProfile) atTop atTop := by
  apply tendsto_atTop.mpr
  intro b
  filter_upwards [(tendsto_atTop.mp harmonic_modular_diverges)
    (b+profileRelativeTotal thirdThermalReference gradualProfile)] with N hN
  have hD := prefix_relative_le_total _ _ harmonic_relative_summable N
  rw [prefix_entropy_identity]
  linarith only [hN,hD]

theorem harmonic_modular_no_finite_limit (K : ℝ) :
    ¬Tendsto (prefixModularIncrement thirdThermalReference gradualProfile) atTop (𝓝 K) :=
  not_tendsto_nhds_of_tendsto_atTop harmonic_modular_diverges K

theorem harmonic_entropy_no_finite_limit (S : ℝ) :
    ¬Tendsto (prefixEntropyIncrement thirdThermalReference gradualProfile) atTop (𝓝 S) :=
  not_tendsto_nhds_of_tendsto_atTop harmonic_entropy_diverges S

theorem positive_affinity_not_finite_modular :
    ¬(∀ Q : SiteProfile, 0<profileAffinityLimit thirdThermalReference Q →
      ∃ K : ℝ, Tendsto (prefixModularIncrement thirdThermalReference Q) atTop (𝓝 K)) := by
  intro h
  obtain ⟨K,hK⟩ := h gradualProfile gradual_profile_affinity_positive
  exact harmonic_modular_no_finite_limit K hK

theorem finite_relative_not_finite_entropy :
    ∃ Q : SiteProfile, 0<profileAffinityLimit thirdThermalReference Q ∧
      Summable (siteRelativeEntropy thirdThermalReference Q) ∧
      (∀ S : ℝ, ¬Tendsto (prefixEntropyIncrement thirdThermalReference Q) atTop (𝓝 S)) :=
  ⟨gradualProfile,gradual_profile_affinity_positive,harmonic_relative_summable,harmonic_entropy_no_finite_limit⟩

#print axioms harmonic_shift_square_summable
#print axioms harmonic_relative_summable
#print axioms harmonic_relative_limit
#print axioms harmonic_shift_diverges
#print axioms harmonic_modular_diverges
#print axioms harmonic_entropy_diverges
#print axioms harmonic_modular_no_finite_limit
#print axioms harmonic_entropy_no_finite_limit
#print axioms positive_affinity_not_finite_modular
#print axioms finite_relative_not_finite_entropy
end
end ChatgptAudit.Response028
