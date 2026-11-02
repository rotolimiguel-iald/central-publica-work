-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_040 (06/09/2026), transposta em 06/09/2026
-- Lote 039..041 (ORDEM_008 cumprida: zero instancias anonimas; lote compilado junto em diretorio limpo).
--   039: CONE LOCAL E FILTRO — coordenadas de Herm2, produtos externos positivos singulares, rigidez
--   quadratica condicional, filtro e fase dos logaritmos locais (fatores, sinais, det, nao unitalidade),
--   reducao global ao bloco 0 (igualdade de operadores, compressao GNS). NAO pago: Delta^(it) como boost
--   sobre a tetrade (a obstrucao finita anterior segue). 040 (resposta a ORDEM_009): OBSTRUCAO PRECISA —
--   o fluxo modular do estado fixo nao percorre a curva de estados; o relogio de Fisher (lambda_F = 1/2 - 3k/16)
--   e toda inversa normalizada do relogio entropico (lambda_D = 1/2 - k/8) FALHAM no casamento quartico da
--   familia de um sitio (excedem lambda* = 1/2 - 9B2/(8 log2 B) - eta O/(2 log2 B)) embora preservem o
--   quadratico; o relogio afim da lambda = 0; a rede A(I) <= A(J) sse I <= J com representacao local fiel;
--   NEGATIVO: a area NAO e escalar so da algebra e do estado (dois protocolos de tangentes, duas densidades).
--   H3 (habitante) segue OPEN — o tipo canonico foi usado para PROVAR o negativo. 041: FLUXO DE CALOR efetivo
--   Q(t) = int_0^t -kappa u m A(u) du ligado por teorema a metrica/geodesica/waveMatter/Jacobi; a igualdade
--   FINITA exata Q = kappa eta (A-1)/(2 pi) FALHA (C/t^4 -> kappa eta (a^2+c^2)/(24 pi) > 0); a relacao
--   infinitesimal segue compativel. Estatuto [REAL / DERIVED / INPUT / OPEN]: familia especificada; area
--   fisica, EquilibriumScreenData compativel, materia/geometria/normalizacao e reconstrucao geral OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 16/16, 18/18, 8/8; 3/3 auditores exit 0;
--   recompilacao INDEPENDENTE 11/11, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3, sem efeito: zero anonimas).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.SummableGravityControls
import TGLExt.ProfileFlowTransport
import TGLExt.ChainVolume
import Mathlib.Analysis.Calculus.Deriv.Comp
import Mathlib.Analysis.Calculus.Deriv.Add

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace ChatgptAudit.Clock040
open Matrix Filter Topology TGLExt ChatgptAudit
  ChatgptAudit.Response028 ChatgptAudit.Profile026
  ChatgptAudit.Transport027 ChatgptAudit.Thermal025
noncomputable section

/-- The profile is unchanged by reversing the external state parameter. -/
theorem amplitude_profile_even (b : SummableAmplitude) (t : ℝ) :
    amplitudeProfile b (-t) = amplitudeProfile b t := by
  apply site_profiles_eq_of_weights
  funext n
  simp only [amplitudeProfile, regularParameter, neg_sq]

/-- Equality concerns the entire actual global vector state, not just its local weights. -/
theorem amplitude_state_even (b : SummableAmplitude) (t : ℝ) :
    amplitudeState b (-t) = amplitudeState b t := by
  have hstate :
      ∀ (Q₁ Q₂ : SiteProfile)
        (h₁ : 0 < profileAffinityLimit thirdThermalReference Q₁)
        (h₂ : 0 < profileAffinityLimit thirdThermalReference Q₂),
        Q₁ = Q₂ →
        globalProfileState thirdThermalReference Q₁ h₁ =
          globalProfileState thirdThermalReference Q₂ h₂ := by
    intro Q₁ Q₂ h₁ h₂ hQ
    subst Q₂
    rfl
  exact hstate _ _ _ _ (amplitude_profile_even b t)

/-- An instantaneous scalar reading of an even curve has zero bilateral derivative,
    whenever that derivative exists. No separate regularity of the reading is assumed. -/
theorem even_curve_reading_derivative_zero {α : Type*}
    (E : ℝ → α) (hE : ∀ t : ℝ, E (-t) = E t) (F : α → ℝ)
    {d : ℝ} (hd : HasDerivAt (fun t : ℝ => F (E t)) d 0) : d = 0 := by
  have houter : HasDerivAt (fun t : ℝ => F (E t)) d (-(0 : ℝ)) := by
    simpa only [neg_zero] using hd
  have hneg : HasDerivAt (fun t : ℝ => F (E (-t))) (d * (-1)) 0 :=
    houter.comp 0 (hasDerivAt_neg (0 : ℝ))
  have hsame : HasDerivAt (fun t : ℝ => F (E t)) (-d) 0 := by
    simpa only [hE, mul_neg_one] using hneg
  have heq := hd.unique hsame
  linarith

theorem instantaneous_state_clock_derivative_zero (b : SummableAmplitude)
    (F : ((TowerHilbert thirdThermalReference →L[ℂ]
      TowerHilbert thirdThermalReference) → ℂ) → ℝ)
    {d : ℝ} (hd : HasDerivAt (fun t : ℝ => F (amplitudeState b t)) d 0) :
    d = 0 :=
  even_curve_reading_derivative_zero (amplitudeState b) (amplitude_state_even b) F hd

/-- This excludes a bilateral normalized clock of the instantaneous state alone.
    It does not exclude an oriented branch or a reading of an entire history. -/
theorem no_normalized_instantaneous_state_clock (b : SummableAmplitude)
    (F : ((TowerHilbert thirdThermalReference →L[ℂ]
      TowerHilbert thirdThermalReference) → ℂ) → ℝ) :
    ¬ HasDerivAt (fun t : ℝ => F (amplitudeState b t)) 1 0 := by
  intro hd
  have h := instantaneous_state_clock_derivative_zero b F hd
  norm_num at h

/-- The modular group of a fixed prepared profile fixes its prepared vector. -/
theorem amplitude_profile_flow_fixes_vector (b : SummableAmplitude) (u s : ℝ) :
    profileModularFlow thirdThermalReference (amplitudeProfile b u)
      (amplitude_profile_affinity_positive b u) s (amplitudeVector b u) =
      amplitudeVector b u :=
  profile_flow_fixes_vector thirdThermalReference (amplitudeProfile b u)
    (amplitude_profile_affinity_positive b u) s

/-- Modular time evolves observables while preserving the state of the fixed profile. -/
theorem amplitude_profile_flow_stationary (b : SummableAmplitude) (u s : ℝ)
    (A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference) :
    amplitudeState b u
      (profileFlowConjugation thirdThermalReference (amplitudeProfile b u)
        (amplitude_profile_affinity_positive b u) s A) =
      amplitudeState b u A :=
  profile_flow_preserves_state thirdThermalReference (amplitudeProfile b u)
    (amplitude_profile_affinity_positive b u) s A

/-- A site observable reads the changing weight of the already constructed state. -/
theorem amplitude_state_site_mark (b : SummableAmplitude) (t : ℝ) (n : ℕ) :
    amplitudeState b t (siteMark thirdThermalReference n) =
      ((1/3 - b.value n * regularParameter t : ℝ) : ℂ) := by
  have h := siteMark_state (P := amplitudeProfile b t) n
  change omegaState (amplitudeProfile b t)
      (towerPi (amplitudeProfile b t) (N := n)
        (lastSiteMatrix n (Matrix.single (0 : Fin 2) 0 (1 : ℂ)))) = _ at h
  rw [omegaState_pi] at h
  change amplitudeState b t
      (towerPi thirdThermalReference (N := n)
        (lastSiteMatrix n (Matrix.single (0 : Fin 2) 0 (1 : ℂ)))) = _
  rw [amplitude_state_local b t n]
  exact h

/-- Any positive site amplitude distinguishes every nonzero state time from time zero. -/
theorem amplitude_state_not_initial (b : SummableAmplitude) (n : ℕ)
    (hn : 0 < b.value n) (t : ℝ) (ht : t ≠ 0) :
    amplitudeState b t ≠ amplitudeState b 0 := by
  intro heq
  have h := congrArg Complex.re (congrFun heq (siteMark thirdThermalReference n))
  rw [amplitude_state_site_mark b t n, amplitude_state_site_mark b 0 n] at h
  simp only [Complex.ofReal_re, regular_parameter_zero, mul_zero, sub_zero] at h
  have hp := mul_pos hn (regular_parameter_positive t ht)
  linarith

theorem amplitude_state_eq_initial_time_zero (b : SummableAmplitude) (n : ℕ)
    (hn : 0 < b.value n) (t : ℝ)
    (heq : amplitudeState b t = amplitudeState b 0) : t = 0 := by
  by_contra ht
  exact amplitude_state_not_initial b n hn t ht heq

/-- A noninitial state is not on the modular orbit of the initial state. -/
theorem amplitude_modular_orbit_not_state (b : SummableAmplitude) (n : ℕ)
    (hn : 0 < b.value n) (t : ℝ) (ht : t ≠ 0) (s : ℝ) :
    amplitudeState b t ≠
      (fun A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference =>
        amplitudeState b 0
          (profileFlowConjugation thirdThermalReference (amplitudeProfile b 0)
            (amplitude_profile_affinity_positive b 0) s A)) := by
  intro heq
  apply amplitude_state_not_initial b n hn t ht
  exact heq.trans (funext (amplitude_profile_flow_stationary b 0 s))

/-- No time change with derivative one can turn the stationary modular orbit into
    the nonzero amplitude curve, even when agreement is required only near zero.
    Modular time is arbitrary here; stationarity does not select a cubic coefficient. -/
theorem no_normalized_modular_reparametrization (b : SummableAmplitude) (n : ℕ)
    (hn : 0 < b.value n) (tau sigma : ℝ → ℝ)
    (htau : HasDerivAt tau 1 0) :
    ¬ (∀ᶠ t : ℝ in 𝓝 0,
      amplitudeState b (tau t) =
        (fun A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference =>
          amplitudeState b 0
            (profileFlowConjugation thirdThermalReference (amplitudeProfile b 0)
              (amplitude_profile_affinity_positive b 0) (sigma t) A))) := by
  intro horbit
  have hevent : tau =ᶠ[𝓝 0] (fun _ : ℝ => 0) := by
    filter_upwards [horbit] with t ht
    apply amplitude_state_eq_initial_time_zero b n hn (tau t)
    exact ht.trans (funext (amplitude_profile_flow_stationary b 0 (sigma t)))
  have hzero : HasDerivAt tau 0 0 :=
    (hasDerivAt_const (0 : ℝ) (0 : ℝ)).congr_of_eventuallyEq hevent
  have hbad := htau.unique hzero
  norm_num at hbad

/-- The zero-amplitude curve is constant. Its reference remains the nonuniform
    one-third profile, so this is not a tracial-limit assertion. -/
theorem zero_amplitude_curve_constant (t u : ℝ) :
    amplitudeState zeroAmplitude t = amplitudeState zeroAmplitude u := by
  funext A
  rw [zero_amplitude_state, zero_amplitude_state]

theorem zero_amplitude_site_weight (t : ℝ) (n : ℕ) :
    amplitudeState zeroAmplitude t (siteMark thirdThermalReference n) = (1/3 : ℂ) := by
  rw [zero_amplitude_state, siteMark_state]
  norm_num [thirdThermalReference]

theorem zero_amplitude_site_weight_ne_half (t : ℝ) (n : ℕ) :
    amplitudeState zeroAmplitude t (siteMark thirdThermalReference n) ≠ (1/2 : ℂ) := by
  rw [zero_amplitude_site_weight]
  norm_num

#print axioms amplitude_profile_even
#print axioms amplitude_state_even
#print axioms even_curve_reading_derivative_zero
#print axioms instantaneous_state_clock_derivative_zero
#print axioms no_normalized_instantaneous_state_clock
#print axioms amplitude_profile_flow_fixes_vector
#print axioms amplitude_profile_flow_stationary
#print axioms amplitude_state_site_mark
#print axioms amplitude_state_not_initial
#print axioms amplitude_state_eq_initial_time_zero
#print axioms amplitude_modular_orbit_not_state
#print axioms no_normalized_modular_reparametrization
#print axioms zero_amplitude_curve_constant
#print axioms zero_amplitude_site_weight
#print axioms zero_amplitude_site_weight_ne_half

end
end ChatgptAudit.Clock040
