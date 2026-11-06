-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_007 (05-06/09/2026), transposta em 06/09/2026
-- Lote 007..023: habitante GLOBAL periodico da esperanca do centralizador; cauda nao ciclica;
--   obstrucoes de Borchers e da assinatura; e a camada GEOMETRICA GERAL em carta: tensores,
--   conexao de Levi-Civita, curvatura, Bianchi, Einstein geometrico + conservacao, Raychaudhuri,
--   Clausius local <=> balanco nulo de Ricci, telas/congruencias nulas construidas, area e calor,
--   entropia relativa, dinamica unitaria, covetor de materia. Estatuto [REAL / INPUT / OPEN]:
--   Clausius, a metrica lorentziana, H3 dinamico, assinatura e globalizacao seguem INPUT/OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100% nas 17 entregas; 17/17
--   auditores da bancada exit 0; recompilacao INDEPENDENTE 116/116 exit 0, todos os axiomas no
--   trio [propext, Classical.choice, Quot.sound]; zero sorry/warning; enunciados lidos.
-- Transposicao MECANICA: este cabecalho + prefixo TGLExt. nos imports; nada mais.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.PeriodAveragePrefix
import TGLExt.TracialCentralizerExpectation

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit
open TGLExt Filter Topology
noncomputable section
variable {P : SiteProfile}

theorem period_average_into (T : ℝ) (hT : 0<T) (hp : LocalPhasePeriod P T)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) (hx : x ∈ theFactorObject P) :
    periodAverage P T hT x ∈ omegaCentralizer P := by
  apply centralizer_from_expectations _ (period_average_mem_factor T hT x hx)
  intro N
  rw [period_average_prefix T hT hp]
  exact pinching_into_global_centralizer _ _

theorem period_average_fixes (T : ℝ) (hT : 0<T) (hp : LocalPhasePeriod P T)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) (hx : x ∈ omegaCentralizer P) :
    periodAverage P T hT x = x := by
  have he (N : ℕ) : towerExpectation P N (periodAverage P T hT x) = towerExpectation P N x := by
    rw [period_average_prefix T hT hp,
      pinching_fixes_global_local N _ (expectation_of_centralizer_is_centralizer N x hx)]
    rfl
  apply factor_eq_of_omega (period_average_mem_factor T hT x hx.1) hx.1
  have ht := expectation_omega_limit (periodAverage P T hT x)
  simp only [he] at ht
  exact tendsto_nhds_unique ht (expectation_omega_limit x)

theorem period_average_ortho (T : ℝ) (hT : 0<T) (hp : LocalPhasePeriod P T)
    (x b : TowerHilbert P →L[ℂ] TowerHilbert P) (hb : b ∈ omegaCentralizer P) :
    omegaState P (star b*(x-periodAverage P T hT x)) = 0 := by
  have hn (N : ℕ) : inner ℂ (towerExpectation P N b (hOmega P))
      (towerExpectation P N x (hOmega P)-towerExpectation P N (periodAverage P T hT x) (hOmega P)) = 0 := by
    have h := pinching_global_ortho N (expectationMatrix P N x) (towerExpectation P N b)
      (expectation_of_centralizer_is_centralizer N b hb)
    rw [omega_product_inner,star_star] at h
    rw [period_average_prefix T hT hp]
    exact h
  have ht : Tendsto (fun N => inner ℂ (towerExpectation P N b (hOmega P))
      (towerExpectation P N x (hOmega P)-towerExpectation P N (periodAverage P T hT x) (hOmega P)))
      atTop (𝓝 (inner ℂ (b (hOmega P)) (x (hOmega P)-periodAverage P T hT x (hOmega P)))) :=
    (expectation_omega_limit b).inner
      ((expectation_omega_limit x).sub (expectation_omega_limit (periodAverage P T hT x)))
  have he : (fun N => inner ℂ (towerExpectation P N b (hOmega P))
    (towerExpectation P N x (hOmega P)-towerExpectation P N (periodAverage P T hT x) (hOmega P))) =
    (fun _ : ℕ => (0:ℂ)) := funext hn
  rw [he] at ht
  have hz := tendsto_nhds_unique ht tendsto_const_nhds
  rw [omega_product_inner,star_star]
  exact hz

def periodicExpectationInput (P : SiteProfile) (T : ℝ) (hT : 0<T)
    (hp : LocalPhasePeriod P T) : ExpectationInput P where
  E := periodAverage P T hT
  into := period_average_into T hT hp
  fixes := period_average_fixes T hT hp
  ortho := fun x _ b hb => period_average_ortho T hT hp x b hb

def stationaryExpectationInput (P : SiteProfile) (p : ℝ) (hp : ∀ n, P.w n=p)
    (hne : p ≠ 1/2) : ExpectationInput P :=
  periodicExpectationInput P (2*Real.pi/|Real.log p-Real.log (1-p)|)
    (div_pos (mul_pos (by norm_num) Real.pi_pos)
      (abs_pos.mpr (stationary_log_gap_ne_zero hp hne)))
    (lattice_local_phase_period (stationary_log_gap_ne_zero hp hne) (stationary_site_log_lattice hp))

theorem half_profile_has_period (hp : ∀ n, P.w n=1/2) (T : ℝ) : LocalPhasePeriod P T := by
  intro N i j
  rw [half_profile_weights hp N i j,sub_self]
  simp [modularPhase]

theorem periodic_half_agrees (hp : ∀ n, P.w n=1/2) (T : ℝ) (hT : 0<T)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) (hx : x ∈ theFactorObject P) :
    (periodicExpectationInput P T hT (half_profile_has_period hp T)).E x =
      (tracialExpectationInput P hp).E x := by
  exact period_average_fixes T hT (half_profile_has_period hp T) x
    ((half_profile_centralizer_is_factor hp x).mpr hx)

#print axioms period_average_into
#print axioms period_average_fixes
#print axioms period_average_ortho
#print axioms periodicExpectationInput
#print axioms stationaryExpectationInput
#print axioms half_profile_has_period
#print axioms periodic_half_agrees
end
end ChatgptAudit
