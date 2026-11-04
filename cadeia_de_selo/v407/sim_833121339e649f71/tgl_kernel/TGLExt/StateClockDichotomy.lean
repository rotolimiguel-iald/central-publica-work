-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_045 (06/09/2026), transposta em 06/09/2026
-- Lote 044..045 (ORDEM_008 cumprida). 044: BOOST APROXIMADO e orientacao do calor — o peso -kappa t realizado
--   por um campo de boost chi = -kappa u d_u + kappa v d_v e seu fluxo (grupo, inversa, jacobiano); pullback da
--   metrica e defeito de Lie -2kappa(aX^2+cY^2)du^2 (zera com o 1o jato na central); controle negativo: nao e
--   Killing em aberto se kappa != 0 e (a,c) != 0; T(chi,d) = -kappa t T(d,d); Q_boost = opticalHeat041 globalmente,
--   = opticalScreenHeat043 como germe; orientacao do passado certificada (calor e area invertem sinal juntos).
--   045 (resposta a ORDEM_010): swapHorizon P p hp i j — troca de sitios no perfil estacionario e um TowerHorizon
--   por prova (unitario, normaliza M, preserva omega); permutacoes finitas com lei de grupo e covariancia das
--   esperancas estacionaria/tracial (horizontes algebricos; identificacao fisica OPEN); shift unilateral NAO
--   construido; aperiodico OPEN (rota Cesaro nomeada); StateClock: classe cinematica (origem, derivada 1, jato) —
--   DICOTOMIA: para todo relogio comum g alguma tela falha (duas telas sigma = 0, r/4, mesmo estado e Ricci:
--   diferenca dos residuos/t^4 -> +eta r^2/96), cada tela isolada admite relogio que cancela a 4a ordem;
--   area: covariancia por horizontes NAO fixa a normalizacao (h e alpha h ambos invariantes; area x alpha).
--   Estatuto [REAL / DERIVED / INPUT / OPEN]: familia, carta e kappa sao INPUT; kappa/(2pi) e normalizacao
--   herdada (sem Unruh/KMS); H3 fisico, lei finita geral, ponte regiao-algebra, shift e aperiodico OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 10/10 + 8/8; 2/2 auditores exit 0;
--   recompilacao INDEPENDENTE 8/8, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3, sem efeito). As fontes v329 (gerencia) NAO sao
--   reincorporadas: a bancada as recompilou como dependencia, sem novidade contada.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.StateClockMatchingControls
import TGLExt.StateClockObstruction

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace ChatgptAudit.Clock045

open Filter TGLExt ChatgptAudit.Response028 ChatgptAudit.Quartic037
  ChatgptAudit.Clock040 ChatgptAudit.Optical036 ChatgptAudit.Thermal025
  ChatgptAudit.Profile026 ChatgptAudit.Transport027
open scoped Topology

noncomputable section

/-- An oriented reparametrization of a state curve, with a reference at zero.
This structure does not assert that the clock is determined by an instantaneous
state. Its cubic jet is a regularity hypothesis, not a matching conclusion. -/
structure StateClock where
  time : ℝ → ℝ
  coefficient : ℝ
  origin : time 0 = 0
  normalized : HasDerivAt time 1 0
  cubic_jet : Tendsto (fun t => (time t - t) / t^3)
    (𝓝[≠] 0) (𝓝 coefficient)

theorem cubic_clock_jet_limit (lam : ℝ) :
    Tendsto (fun t => (cubicClock lam t - t) / t^3)
      (𝓝[≠] 0) (𝓝 lam) := by
  have h : Tendsto (fun _ : ℝ => lam) (𝓝[≠] 0) (𝓝 lam) := tendsto_const_nhds
  apply h.congr'
  filter_upwards [quartic_punctured_time_nonzero] with t ht
  dsimp [cubicClock]
  field_simp [ht]
  ring

/-- A nonempty class of normalized clocks, independent of any optical screen. -/
def cubicStateClock (lam : ℝ) : StateClock where
  time := cubicClock lam
  coefficient := lam
  origin := cubic_clock_zero lam
  normalized := cubic_clock_hasDerivAt_zero lam
  cubic_jet := cubic_clock_jet_limit lam

theorem state_clock_ratio (clock : StateClock) :
    Tendsto (fun t => clock.time t / t) (𝓝[≠] 0) (𝓝 1) :=
  clock_jet_ratio clock.cubic_jet

/-- Positive ratio fixes the local orientation on both punctured branches. -/
theorem state_clock_positive_ratio (clock : StateClock) :
    ∀ᶠ t : ℝ in 𝓝[≠] 0, 0 < clock.time t / t :=
  (state_clock_ratio clock).eventually (lt_mem_nhds (by norm_num))

/-- Actual entropy and Jacobi-area increments, using the already defined residual. -/
def FourthOrderMatch (b : SummableAmplitude) (eta sigma : ℝ)
    (g : ℝ → ℝ) : Prop :=
  Tendsto (fun t => actualClockStateAreaDefect b eta sigma g t / t^4)
    (𝓝[≠] 0) (𝓝 0)

theorem two_screen_anisotropies_admissible (b : SummableAmplitude) (eta : ℝ)
    (heta : 0 < eta) (hB : 0 < amplitudeMass b) :
    |(0 : ℝ)| < quarticMatchedRicci b eta / 2 ∧
      |quarticMatchedRicci b eta / 4| < quarticMatchedRicci b eta / 2 := by
  have hr := quartic_matched_ricci_positive b eta heta hB
  constructor
  · rw [abs_zero]
    linarith
  · rw [abs_of_pos (by positivity)]
    linarith

theorem tidal_quartic_coefficient_gap (b : SummableAmplitude) (eta : ℝ) :
    quarticMatchingCoefficient b eta (quarticMatchedRicci b eta / 4) -
      quarticMatchingCoefficient b eta 0 = eta * (quarticMatchedRicci b eta)^2 / 96 := by
  unfold quarticMatchingCoefficient
  ring

/-- The state contribution cancels for every function g, including clocks without
continuity or a cubic jet. The optical parameter is the same t in both tests. -/
theorem common_clock_residual_difference (b : SummableAmplitude) (eta sigma : ℝ)
    (g : ℝ → ℝ) (t : ℝ) :
    actualClockStateAreaDefect b eta sigma g t / t^4 -
      actualClockStateAreaDefect b eta 0 g t / t^4 =
    quarticStateAreaDefect b eta sigma t / t^4 -
      quarticStateAreaDefect b eta 0 t / t^4 := by
  unfold actualClockStateAreaDefect quarticStateAreaDefect
  ring

theorem common_clock_residual_gap_limit (b : SummableAmplitude) (eta : ℝ)
    (g : ℝ → ℝ) (heta : 0 < eta) (hB : 0 < amplitudeMass b) :
    Tendsto (fun t =>
      actualClockStateAreaDefect b eta (quarticMatchedRicci b eta / 4) g t / t^4 -
        actualClockStateAreaDefect b eta 0 g t / t^4)
      (𝓝[≠] 0) (𝓝 (eta * (quarticMatchedRicci b eta)^2 / 96)) := by
  obtain ⟨hs0, hs1⟩ := two_screen_anisotropies_admissible b eta heta hB
  have h := (quartic_state_area_defect_limit b eta (quarticMatchedRicci b eta / 4)
    (ne_of_gt heta) hs1).sub
      (quartic_state_area_defect_limit b eta 0 (ne_of_gt heta) hs0)
  rw [tidal_quartic_coefficient_gap] at h
  apply h.congr'
  exact Filter.Eventually.of_forall (fun t =>
    (common_clock_residual_difference b eta (quarticMatchedRicci b eta / 4) g t).symm)

/-- Stronger than the cubic-jet obstruction in 040: no regularity of g is needed. -/
theorem arbitrary_common_clock_pair_incompatible (b : SummableAmplitude) (eta : ℝ)
    (g : ℝ → ℝ) (heta : 0 < eta) (hB : 0 < amplitudeMass b) :
    ¬ (FourthOrderMatch b eta 0 g ∧
      FourthOrderMatch b eta (quarticMatchedRicci b eta / 4) g) := by
  rintro ⟨h0, h1⟩
  unfold FourthOrderMatch at h0 h1
  have hz : Tendsto (fun t =>
      actualClockStateAreaDefect b eta (quarticMatchedRicci b eta / 4) g t / t^4 -
        actualClockStateAreaDefect b eta 0 g t / t^4)
      (𝓝[≠] 0) (𝓝 0) := by
    simpa only [sub_self] using h1.sub h0
  have he := tendsto_nhds_unique (common_clock_residual_gap_limit b eta g heta hB) hz
  have hr := quartic_matched_ricci_positive b eta heta hB
  have hp : 0 < eta * (quarticMatchedRicci b eta)^2 / 96 := by positivity
  linarith

/-- For each common clock, at least one of the two screens fails fourth-order
matching. This does not say that each clock fails for every screen. -/
theorem arbitrary_common_clock_dichotomy (b : SummableAmplitude) (eta : ℝ)
    (g : ℝ → ℝ) (heta : 0 < eta) (hB : 0 < amplitudeMass b) :
    ¬ FourthOrderMatch b eta 0 g ∨
      ¬ FourthOrderMatch b eta (quarticMatchedRicci b eta / 4) g := by
  classical
  by_cases h0 : FourthOrderMatch b eta 0 g
  · exact Or.inr (fun h1 => arbitrary_common_clock_pair_incompatible b eta g heta hB ⟨h0, h1⟩)
  · exact Or.inl h0

theorem state_clock_dichotomy (b : SummableAmplitude) (eta : ℝ)
    (clock : StateClock) (heta : 0 < eta) (hB : 0 < amplitudeMass b) :
    ¬ FourthOrderMatch b eta 0 clock.time ∨
      ¬ FourthOrderMatch b eta (quarticMatchedRicci b eta / 4) clock.time :=
  arbitrary_common_clock_dichotomy b eta clock.time heta hB

/-- A rule may read the entire parametrized state history, including a fixed
reference and orientation. It receives no geometry argument; both screens use
the very same state history. No regularity of the rule is assumed. -/
theorem state_history_rule_dichotomy (b : SummableAmplitude) (eta : ℝ)
    (rule : (ℝ → ((TowerHilbert thirdThermalReference →L[ℂ]
      TowerHilbert thirdThermalReference) → ℂ)) → ℝ → ℝ)
    (heta : 0 < eta) (hB : 0 < amplitudeMass b) :
    ¬ FourthOrderMatch b eta 0 (rule (amplitudeState b)) ∨
      ¬ FourthOrderMatch b eta (quarticMatchedRicci b eta / 4)
        (rule (amplitudeState b)) :=
  arbitrary_common_clock_dichotomy b eta (rule (amplitudeState b)) heta hB

/-- A normalized bilateral clock cannot factor through the instantaneous state
of the even amplitude curve. Oriented branch/history readings are not excluded. -/
theorem state_clock_not_instantaneous (b : SummableAmplitude) (clock : StateClock) :
    ¬ ∃ reading : ((TowerHilbert thirdThermalReference →L[ℂ]
      TowerHilbert thirdThermalReference) → ℂ) → ℝ,
      ∀ t : ℝ, clock.time t = reading (amplitudeState b t) := by
  rintro ⟨reading, hreading⟩
  have he : clock.time = (fun t => reading (amplitudeState b t)) := funext hreading
  apply no_normalized_instantaneous_state_clock b reading
  rw [← he]
  exact clock.normalized

/-- Stationary modular evolution does not instantiate a normalized clock for
the nonconstant amplitude curve. Modular and state-curve parameters stay distinct. -/
theorem state_clock_not_modular_reparametrization (b : SummableAmplitude) (n : ℕ)
    (hn : 0 < b.value n) (clock : StateClock) (sigma : ℝ → ℝ) :
    ¬ (∀ᶠ t : ℝ in 𝓝 0,
      amplitudeState b (clock.time t) =
        (fun A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference =>
          amplitudeState b 0
            (profileFlowConjugation thirdThermalReference (amplitudeProfile b 0)
              (amplitude_profile_affinity_positive b 0) (sigma t) A))) :=
  no_normalized_modular_reparametrization b n hn clock.time sigma clock.normalized

/-- The residual is the one already paid in 040, now applied to an explicit clock. -/
theorem state_clock_quartic_residual (b : SummableAmplitude) (eta sigma : ℝ)
    (clock : StateClock) (heta : eta ≠ 0)
    (hs : |sigma| < quarticMatchedRicci b eta / 2) :
    Tendsto (fun t => actualClockStateAreaDefect b eta sigma clock.time t / t^4)
      (𝓝[≠] 0) (𝓝 (quarticMatchingCoefficient b eta sigma -
        2 * clock.coefficient * Real.log 2 * amplitudeMass b)) :=
  actual_clock_state_area_limit b eta sigma clock.coefficient clock.time heta hs clock.cubic_jet

/-- Failure in fourth order does not remove the already matched quadratic limit. -/
theorem state_clock_preserves_quadratic_matching (b : SummableAmplitude) (eta sigma : ℝ)
    (clock : StateClock) (heta : eta ≠ 0)
    (hs : |sigma| < quarticMatchedRicci b eta / 2) :
    Tendsto (fun t => actualClockStateAreaDefect b eta sigma clock.time t / t^2)
      (𝓝[≠] 0) (𝓝 0) :=
  actual_clock_quadratic_matching b eta sigma clock.coefficient clock.time heta hs clock.cubic_jet

theorem state_clock_matching_iff_coefficient (b : SummableAmplitude) (eta sigma : ℝ)
    (clock : StateClock) (heta : eta ≠ 0) (hB : 0 < amplitudeMass b)
    (hs : |sigma| < quarticMatchedRicci b eta / 2) :
    FourthOrderMatch b eta sigma clock.time ↔
      clock.coefficient = cancellingStateClock b eta sigma := by
  constructor
  · intro hm
    exact actual_clock_matching_requires_coefficient b eta sigma clock.coefficient clock.time
      heta hB hs clock.cubic_jet hm
  · intro he
    have h := state_clock_quartic_residual b eta sigma clock heta hs
    rw [he, cancelling_state_clock_identity b eta sigma hB] at h
    exact h

/-- Separate screen-dependent choices do match; this controls the quantifiers
and does not select a physical clock from the state. -/
theorem each_screen_has_a_matching_state_clock (b : SummableAmplitude) (eta sigma : ℝ)
    (heta : eta ≠ 0) (hB : 0 < amplitudeMass b)
    (hs : |sigma| < quarticMatchedRicci b eta / 2) :
    ∃ clock : StateClock, FourthOrderMatch b eta sigma clock.time := by
  refine ⟨cubicStateClock (cancellingStateClock b eta sigma), ?_⟩
  exact (state_clock_matching_iff_coefficient b eta sigma
    (cubicStateClock (cancellingStateClock b eta sigma)) heta hB hs).2 rfl

theorem required_state_clock_gap_positive (b : SummableAmplitude) (eta : ℝ)
    (heta : 0 < eta) (hB : 0 < amplitudeMass b) :
    cancellingStateClock b eta (quarticMatchedRicci b eta / 4) -
        cancellingStateClock b eta 0 = quarticMatchedRicci b eta / 96 ∧
      0 < cancellingStateClock b eta (quarticMatchedRicci b eta / 4) -
        cancellingStateClock b eta 0 := by
  have he := required_clock_tidal_gap b eta (ne_of_gt heta) hB
  refine ⟨he, ?_⟩
  rw [he]
  have hr := quartic_matched_ricci_positive b eta heta hB
  positivity

#print axioms StateClock
#print axioms cubic_clock_jet_limit
#print axioms cubicStateClock
#print axioms state_clock_ratio
#print axioms state_clock_positive_ratio
#print axioms FourthOrderMatch
#print axioms two_screen_anisotropies_admissible
#print axioms tidal_quartic_coefficient_gap
#print axioms common_clock_residual_difference
#print axioms common_clock_residual_gap_limit
#print axioms arbitrary_common_clock_pair_incompatible
#print axioms arbitrary_common_clock_dichotomy
#print axioms state_clock_dichotomy
#print axioms state_history_rule_dichotomy
#print axioms state_clock_not_instantaneous
#print axioms state_clock_not_modular_reparametrization
#print axioms state_clock_quartic_residual
#print axioms state_clock_preserves_quadratic_matching
#print axioms state_clock_matching_iff_coefficient
#print axioms each_screen_has_a_matching_state_clock
#print axioms required_state_clock_gap_positive

end
end ChatgptAudit.Clock045
