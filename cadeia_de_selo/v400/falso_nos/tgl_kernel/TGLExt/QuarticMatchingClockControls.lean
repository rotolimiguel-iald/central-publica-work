-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_037 (06/09/2026), transposta em 06/09/2026
-- Lote 035..037 (processo da ORDEM_008 cumprido pela bancada: zero instancias anonimas, lote compilado junto
--   num diretorio limpo). 035: DEFORMACOES OBSERVAVEIS e AREA DE FISHER — derivadas da conjugacao unitaria e
--   do estado, observaveis de Pauli por sitio na torre real, duas leituras independentes (jacobiano nao
--   degenerado), medicao conjunta efetiva (sitios distintos), probabilidades normalizadas e suas derivadas,
--   matriz de Fisher na origem, densidade de area de Fisher (4/9 como area de coordenadas). 036: AREA OPTICA e
--   LIBERDADE RADIATIVA — a area induzida dos campos de Jacobi da metrica 029 ligada a curvatura real
--   (A2(0) = -Ric(d,d); A4(0) = 2(tr K)^2 - 2 tr(K_TF^T K_TF)); germes de area distintos para shears
--   distintos. 037: QUARTA ORDEM, AREA e RELOGIO — limites entropicos e de area em 4a ordem; NEGATIVO
--   MEDIDO: o casamento adicional em 4a ordem com parametro comum fixo FALHA (delta4 >= (7/48) B > 0);
--   a reparametrizacao do relogio t + lambda t^3 cancela o defeito ate 4a ordem (controle do relogio relativo).
--   Estatuto [REAL / DERIVED / INPUT / OPEN]: X, Y, sitios e normalizacao sao INPUT; a familia optica
--   lorentziana e INPUT; identificacao da inscricao angular com area fisica, retorno estabilizador, ponte
--   regiao-algebra, escala, assinatura, dinamica gravitacional e H3 geral NAO pagos.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 14/14, 8/8 (via manifesto), 10/10; manifestos
--   1051/977; 3/3 auditores exit 0; recompilacao INDEPENDENTE 15/15, axiomas no trio; guarda de colisao;
--   enunciados lidos. Transposicao: cabecalho + prefixo TGLExt. (+ regra 3, sem efeito: zero anonimas).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.QuarticClockTransport
import TGLExt.FourthOrderMatchingControls
import TGLExt.LikelihoodCocycleControls

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace ChatgptAudit.Quartic037
open Filter ChatgptAudit.Response028 ChatgptAudit.Optical036
open scoped Topology
noncomputable section

/-- The new quartic coefficient reads the same L already constructed in 030. -/
theorem likelihood_reading_quartic_limit (b : SummableAmplitude) :
    Tendsto (fun t : ℝ =>
      (amplitudeState b t (ChatgptAudit.Cocycle030.likelihoodGenerator b t)).re / t^4)
      (𝓝[≠] 0) (𝓝 ((9/4) * amplitudeSquareMass b)) := by
  simpa only [ChatgptAudit.Cocycle030.likelihood_generator_entropy, Complex.ofReal_re] using
    amplitude_relative_quartic_limit b

/-- A change of the state parameter, with the optical parameter held fixed. -/
def retimedQuarticStateAreaDefect (b : SummableAmplitude) (eta s lam t : ℝ) : ℝ :=
  amplitudeEntropyIncrement b (cubicClock lam t) -
    eta * (geometricJacobiArea
      (quarticMatchedRicci b eta / 2 + s) (quarticMatchedRicci b eta / 2 - s) t - 1)

def cancellingStateClock (b : SummableAmplitude) (eta s : ℝ) : ℝ :=
  quarticMatchingCoefficient b eta s / (2 * Real.log 2 * amplitudeMass b)

theorem retimed_entropy_quartic_limit (b : SummableAmplitude) (lam : ℝ) :
    Tendsto (fun t : ℝ => (amplitudeEntropyIncrement b (cubicClock lam t) +
        Real.log 2 * amplitudeMass b * t^2) / t^4)
      (𝓝[≠] 0)
      (𝓝 (entropyQuarticCoefficient b - 2 * lam * Real.log 2 * amplitudeMass b)) := by
  have hf : Tendsto
      (fun t : ℝ => (amplitudeEntropyIncrement b t -
        (-(Real.log 2 * amplitudeMass b)) * t^2) / t^4)
      (𝓝[≠] 0) (𝓝 (entropyQuarticCoefficient b)) := by
    simpa only [neg_mul, sub_neg_eq_add, entropyQuarticCoefficient] using
      amplitude_entropy_quartic_limit b
  have h := quartic_remainder_clock_transport (amplitudeEntropyIncrement b)
    (-(Real.log 2 * amplitudeMass b)) (entropyQuarticCoefficient b) lam hf
  have hv : entropyQuarticCoefficient b +
      2 * (-(Real.log 2 * amplitudeMass b)) * lam =
        entropyQuarticCoefficient b - 2 * lam * Real.log 2 * amplitudeMass b := by ring
  rw [hv] at h
  simpa only [neg_mul, sub_neg_eq_add] using h

theorem retimed_quartic_defect_identity (b : SummableAmplitude) (eta s lam t : ℝ)
    (heta : eta ≠ 0) :
    (amplitudeEntropyIncrement b (cubicClock lam t) +
        Real.log 2 * amplitudeMass b * t^2) / t^4 -
      eta * ((geometricJacobiArea
        (quarticMatchedRicci b eta / 2 + s) (quarticMatchedRicci b eta / 2 - s) t -
          1 + quarticMatchedRicci b eta * t^2 / 2) / t^4) =
      retimedQuarticStateAreaDefect b eta s lam t / t^4 := by
  unfold retimedQuarticStateAreaDefect
  rw [← mul_div_assoc, ← sub_div]
  congr 1
  rw [← quartic_matched_ricci_cancellation b eta heta]
  ring

theorem retimed_quartic_state_area_defect_limit (b : SummableAmplitude) (eta s lam : ℝ)
    (heta : eta ≠ 0) (hs : |s| < quarticMatchedRicci b eta / 2) :
    Tendsto (fun t : ℝ => retimedQuarticStateAreaDefect b eta s lam t / t^4)
      (𝓝[≠] 0)
      (𝓝 (quarticMatchingCoefficient b eta s -
        2 * lam * Real.log 2 * amplitudeMass b)) := by
  have h := (retimed_entropy_quartic_limit b lam).sub
    ((geometric_jacobi_area_rs_quartic_limit (quarticMatchedRicci b eta) s hs).const_mul eta)
  have hvalue :
      (entropyQuarticCoefficient b - 2 * lam * Real.log 2 * amplitudeMass b) -
          eta * ((quarticMatchedRicci b eta)^2 / 12 - s^2 / 6) =
        quarticMatchingCoefficient b eta s - 2 * lam * Real.log 2 * amplitudeMass b := by
    unfold quarticMatchingCoefficient
    ring
  rw [hvalue] at h
  apply h.congr'
  exact Filter.Eventually.of_forall (fun t => retimed_quartic_defect_identity b eta s lam t heta)

theorem cancelling_state_clock_identity (b : SummableAmplitude) (eta s : ℝ)
    (hB : 0 < amplitudeMass b) :
    quarticMatchingCoefficient b eta s -
      2 * cancellingStateClock b eta s * Real.log 2 * amplitudeMass b = 0 := by
  have hlog : Real.log 2 ≠ 0 := ne_of_gt (Real.log_pos (by norm_num))
  unfold cancellingStateClock
  field_simp [hlog, ne_of_gt hB]
  simp only [sub_self, mul_zero]

/-- This is a mathematical control of the still unselected relative clock.
    It is not a derivation of the physical relation between state and beam time. -/
theorem retimed_quartic_matching (b : SummableAmplitude) (eta s : ℝ)
    (heta : eta ≠ 0) (hB : 0 < amplitudeMass b)
    (hs : |s| < quarticMatchedRicci b eta / 2) :
    Tendsto
      (fun t : ℝ => retimedQuarticStateAreaDefect b eta s
        (cancellingStateClock b eta s) t / t^4)
      (𝓝[≠] 0) (𝓝 0) := by
  have h := retimed_quartic_state_area_defect_limit b eta s
    (cancellingStateClock b eta s) heta hs
  simpa only [cancelling_state_clock_identity b eta s hB] using h

theorem cancelling_clock_same_initial_calibration (b : SummableAmplitude) (eta s : ℝ) :
    cubicClock (cancellingStateClock b eta s) 0 = 0 ∧
      HasDerivAt (cubicClock (cancellingStateClock b eta s)) 1 0 :=
  ⟨cubic_clock_zero _, cubic_clock_hasDerivAt_zero _⟩

theorem common_state_area_clock_limit (b : SummableAmplitude) (eta s lam : ℝ)
    (heta : eta ≠ 0) (hs : |s| < quarticMatchedRicci b eta / 2) :
    Tendsto (fun t : ℝ => quarticStateAreaDefect b eta s (cubicClock lam t) / t^4)
      (𝓝[≠] 0) (𝓝 (quarticMatchingCoefficient b eta s)) :=
  quartic_coefficient_clock_invariant (quarticStateAreaDefect b eta s)
    (quarticMatchingCoefficient b eta s) lam
    (quartic_state_area_defect_limit b eta s heta hs)

theorem common_clock_small_amplitude_no_go (b : SummableAmplitude) (eta s lam : ℝ)
    (heta : 0 < eta) (hB : 0 < amplitudeMass b) (hsmall : amplitudeMass b ≤ eta)
    (hs : |s| < quarticMatchedRicci b eta / 2) :
    ¬ Tendsto (fun t : ℝ => quarticStateAreaDefect b eta s (cubicClock lam t) / t^4)
      (𝓝[≠] 0) (𝓝 0) := by
  intro hz
  have he := tendsto_nhds_unique (common_state_area_clock_limit b eta s lam
    (ne_of_gt heta) hs) hz
  have hp := quartic_matching_coefficient_positive b eta s heta hB hsmall
  linarith

/-- A nonzero, finitely supported member of the already defined global-state family. -/
def smallSingleAmplitude (eta : ℝ) (heta : 0 < eta) : SummableAmplitude where
  value n := if n = 0 then min (1/24) (eta/2) else 0
  nonnegative n := by
    split_ifs
    · exact le_of_lt (lt_min_iff.mpr ⟨by norm_num, by positivity⟩)
    · exact le_rfl
  bound n := by
    split_ifs
    · exact (min_le_left _ _).trans (by norm_num)
    · norm_num
  summable := (hasSum_ite_eq (0 : ℕ) (min (1/24 : ℝ) (eta/2))).summable

theorem small_single_amplitude_mass (eta : ℝ) (heta : 0 < eta) :
    amplitudeMass (smallSingleAmplitude eta heta) = min (1/24) (eta/2) := by
  simp [amplitudeMass, smallSingleAmplitude]

theorem small_single_amplitude_square_mass (eta : ℝ) (heta : 0 < eta) :
    amplitudeSquareMass (smallSingleAmplitude eta heta) = (min (1/24) (eta/2))^2 := by
  simp [amplitudeSquareMass, smallSingleAmplitude, ite_pow]

theorem small_single_amplitude_bounds (eta : ℝ) (heta : 0 < eta) :
    0 < amplitudeMass (smallSingleAmplitude eta heta) ∧
      amplitudeMass (smallSingleAmplitude eta heta) ≤ eta := by
  rw [small_single_amplitude_mass]
  constructor
  · exact lt_min_iff.mpr ⟨by norm_num, by positivity⟩
  · exact (min_le_right _ _).trans (by linarith)

theorem quartic_matched_ricci_positive (b : SummableAmplitude) (eta : ℝ)
    (heta : 0 < eta) (hB : 0 < amplitudeMass b) :
    0 < quarticMatchedRicci b eta := by
  unfold quarticMatchedRicci
  exact div_pos (mul_pos (mul_pos (by norm_num) (Real.log_pos (by norm_num))) hB) heta

/-- Every positive area conversion admits an actual nonzero state and optical
    screen for which fixed-clock quartic matching fails but a relative retiming
    matches. This does not contradict the established quadratic matching. -/
theorem nonvacuous_quartic_clock_control (eta : ℝ) (heta : 0 < eta) :
    let b := smallSingleAmplitude eta heta
    (¬ Tendsto (fun t : ℝ => quarticStateAreaDefect b eta 0 t / t^4)
        (𝓝[≠] 0) (𝓝 0)) ∧
      Tendsto (fun t : ℝ => retimedQuarticStateAreaDefect b eta 0
          (cancellingStateClock b eta 0) t / t^4)
        (𝓝[≠] 0) (𝓝 0) := by
  dsimp only
  obtain ⟨hB, hsmall⟩ := small_single_amplitude_bounds eta heta
  have hr := quartic_matched_ricci_positive (smallSingleAmplitude eta heta) eta heta hB
  have hs : |(0 : ℝ)| < quarticMatchedRicci (smallSingleAmplitude eta heta) eta / 2 := by
    rw [abs_zero]
    linarith
  exact ⟨quartic_state_area_small_amplitude_no_go _ eta 0 heta hB hsmall hs,
    retimed_quartic_matching _ eta 0 (ne_of_gt heta) hB hs⟩

#print axioms likelihood_reading_quartic_limit
#print axioms retimedQuarticStateAreaDefect
#print axioms cancellingStateClock
#print axioms retimed_entropy_quartic_limit
#print axioms retimed_quartic_defect_identity
#print axioms retimed_quartic_state_area_defect_limit
#print axioms cancelling_state_clock_identity
#print axioms retimed_quartic_matching
#print axioms cancelling_clock_same_initial_calibration
#print axioms common_state_area_clock_limit
#print axioms common_clock_small_amplitude_no_go
#print axioms smallSingleAmplitude
#print axioms small_single_amplitude_mass
#print axioms small_single_amplitude_square_mass
#print axioms small_single_amplitude_bounds
#print axioms quartic_matched_ricci_positive
#print axioms nonvacuous_quartic_clock_control
end
end ChatgptAudit.Quartic037
