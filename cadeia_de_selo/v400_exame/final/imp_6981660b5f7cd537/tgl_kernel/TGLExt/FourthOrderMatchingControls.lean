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
import TGLExt.JacobiAreaQuarticLimit
import TGLExt.SummableRelativeQuartic

set_option autoImplicit false
set_option maxHeartbeats 4000000

namespace ChatgptAudit.Quartic037

open Filter ChatgptAudit.Response028 ChatgptAudit.Optical036
open scoped Topology

noncomputable section

/-- Ricci trace selected by the already established quadratic matching. -/
def quarticMatchedRicci (b : SummableAmplitude) (eta : ℝ) : ℝ :=
  2*Real.log 2*amplitudeMass b/eta

def entropyQuarticCoefficient (b : SummableAmplitude) : ℝ :=
  Real.log 2*amplitudeMass b-(9/4)*amplitudeSquareMass b

/-- The fourth-order coefficient, with the same parameter on both sides. -/
def quarticMatchingCoefficient (b : SummableAmplitude) (eta s : ℝ) : ℝ :=
  entropyQuarticCoefficient b-
    eta*((quarticMatchedRicci b eta)^2/12-s^2/6)

def quarticStateAreaDefect (b : SummableAmplitude) (eta s t : ℝ) : ℝ :=
  amplitudeEntropyIncrement b t-
    eta*(geometricJacobiArea
      (quarticMatchedRicci b eta/2+s) (quarticMatchedRicci b eta/2-s) t-1)

theorem quartic_matched_ricci_cancellation (b : SummableAmplitude) (eta : ℝ)
    (heta : eta≠0) :
    eta*quarticMatchedRicci b eta/2=Real.log 2*amplitudeMass b := by
  unfold quarticMatchedRicci
  field_simp [heta]

theorem quartic_state_area_defect_identity (b : SummableAmplitude) (eta s : ℝ)
    (heta : eta≠0) (t : ℝ) :
    (amplitudeEntropyIncrement b t+Real.log 2*amplitudeMass b*t^2)/t^4-
      eta*((geometricJacobiArea
        (quarticMatchedRicci b eta/2+s) (quarticMatchedRicci b eta/2-s) t-1+
        quarticMatchedRicci b eta*t^2/2)/t^4)=
      quarticStateAreaDefect b eta s t/t^4 := by
  unfold quarticStateAreaDefect
  rw [← mul_div_assoc, ← sub_div]
  congr 1
  rw [← quartic_matched_ricci_cancellation b eta heta]
  ring

/-- A genuine punctured limit, obtained from the two proved Taylor remainders. -/
theorem quartic_state_area_defect_limit (b : SummableAmplitude) (eta s : ℝ)
    (heta : eta≠0) (hs : |s|<quarticMatchedRicci b eta/2) :
    Tendsto (fun t : ℝ => quarticStateAreaDefect b eta s t/t^4)
      (𝓝[≠] 0) (𝓝 (quarticMatchingCoefficient b eta s)) := by
  have h := (amplitude_entropy_quartic_limit b).sub
    ((geometric_jacobi_area_rs_quartic_limit (quarticMatchedRicci b eta) s hs).const_mul eta)
  apply h.congr'
  exact Filter.Eventually.of_forall
    (fun t => quartic_state_area_defect_identity b eta s heta t)

theorem quartic_state_area_matching_iff (b : SummableAmplitude) (eta s : ℝ)
    (heta : eta≠0) (hs : |s|<quarticMatchedRicci b eta/2) :
    Tendsto (fun t : ℝ => quarticStateAreaDefect b eta s t/t^4)
      (𝓝[≠] 0) (𝓝 0) ↔
      entropyQuarticCoefficient b=
        eta*((quarticMatchedRicci b eta)^2/12-s^2/6) := by
  have h := quartic_state_area_defect_limit b eta s heta hs
  constructor
  · intro hz
    have he : quarticMatchingCoefficient b eta s=0 :=
      tendsto_nhds_unique h hz
    exact sub_eq_zero.mp he
  · intro hm
    have he : quarticMatchingCoefficient b eta s=0 := sub_eq_zero.mpr hm
    simpa only [he] using h

theorem quartic_log_two_bounds : (1/2 : ℝ)≤Real.log 2 ∧ Real.log 2≤1 := by
  constructor
  · have h := Real.one_sub_inv_le_log_of_pos (by norm_num : (0 : ℝ)<2)
    norm_num at h
    exact h
  · have h := Real.log_le_sub_one_of_pos (by norm_num : (0 : ℝ)<2)
    norm_num at h
    exact h

/-- Algebraic obstruction valid for every anisotropy parameter, before geometric
    admissibility is imposed. The bound concerns fourth-order matching only. -/
theorem quartic_coefficient_lower_bound_algebra (ell B B2 eta s : ℝ)
    (hell_lower : 1/2≤ell) (hell_upper : ell≤1)
    (hB : 0≤B) (hBeta : B≤eta) (hB2 : B2≤B/12) (heta : 0<eta) :
    (7/48)*B≤ell*B-(9/4)*B2-
      eta*((2*ell*B/eta)^2/12-s^2/6) := by
  have hell : 0≤ell := by linarith
  have hEB : 0≤eta*B := mul_nonneg heta.le hB
  have hellsq : ell^2≤ell := by
    nlinarith [mul_nonneg hell (sub_nonneg.mpr hell_upper)]
  have hBB : B^2≤eta*B := by
    nlinarith [mul_nonneg hB (sub_nonneg.mpr hBeta)]
  have hterm : ell^2*B^2≤ell*(eta*B) :=
    (mul_le_mul_of_nonneg_left hBB (sq_nonneg ell)).trans
      (mul_le_mul_of_nonneg_right hellsq hEB)
  have hB2scaled := mul_le_mul_of_nonneg_left hB2 heta.le
  have hellscaled := mul_le_mul_of_nonneg_right hell_lower hEB
  have hsnonnegative := mul_nonneg (sq_nonneg eta) (sq_nonneg s)
  have hproduct :
      eta*(ell*B-(9/4)*B2-eta*((2*ell*B/eta)^2/12-s^2/6))=
        eta*ell*B-(9/4)*eta*B2-ell^2*B^2/3+eta^2*s^2/6 := by
    field_simp [ne_of_gt heta]
    ring
  apply (mul_le_mul_iff_right₀ heta).mp
  rw [hproduct]
  nlinarith

theorem quartic_matching_coefficient_lower_bound (b : SummableAmplitude)
    (eta s : ℝ) (heta : 0<eta) (hsmall : amplitudeMass b≤eta) :
    (7/48)*amplitudeMass b≤quarticMatchingCoefficient b eta s := by
  obtain ⟨hlower,hupper⟩ := quartic_log_two_bounds
  exact quartic_coefficient_lower_bound_algebra
    (Real.log 2) (amplitudeMass b) (amplitudeSquareMass b) eta s
    hlower hupper (amplitude_mass_nonnegative b) hsmall
    (amplitude_square_mass_le_mass_twelfth b) heta

theorem quartic_matching_coefficient_positive (b : SummableAmplitude)
    (eta s : ℝ) (heta : 0<eta) (hB : 0<amplitudeMass b)
    (hsmall : amplitudeMass b≤eta) :
    0<quarticMatchingCoefficient b eta s := by
  have h := quartic_matching_coefficient_lower_bound b eta s heta hsmall
  linarith

/-- This excludes an additional quartic matching in the fixed clock; it does not
    contradict the earlier second-order relation. -/
theorem quartic_state_area_small_amplitude_no_go (b : SummableAmplitude)
    (eta s : ℝ) (heta : 0<eta) (hB : 0<amplitudeMass b)
    (hsmall : amplitudeMass b≤eta) (hs : |s|<quarticMatchedRicci b eta/2) :
    ¬Tendsto (fun t : ℝ => quarticStateAreaDefect b eta s t/t^4)
      (𝓝[≠] 0) (𝓝 0) := by
  intro hz
  have he : quarticMatchingCoefficient b eta s=0 :=
    tendsto_nhds_unique
      (quartic_state_area_defect_limit b eta s (ne_of_gt heta) hs) hz
  have hp := quartic_matching_coefficient_positive b eta s heta hB hsmall
  linarith

theorem quartic_matching_square_criterion (C eta r s : ℝ) (heta : eta≠0) :
    C=eta*(r^2/12-s^2/6) ↔ s^2=r^2/2-6*C/eta := by
  constructor
  · intro hm
    rw [hm]
    field_simp [heta]; ring
  · intro he
    rw [he]
    field_simp [heta]; ring

theorem quartic_optical_coefficient_admissible_bounds (eta r s : ℝ)
    (heta : 0<eta) (hs : |s|<r/2) :
    eta*r^2/24<eta*(r^2/12-s^2/6) ∧
      eta*(r^2/12-s^2/6)≤eta*r^2/12 := by
  have hr : 0<r/2 := lt_of_le_of_lt (abs_nonneg s) hs
  have hplus : 0<r/2+|s| := add_pos_of_pos_of_nonneg hr (abs_nonneg s)
  have hproduct := mul_pos (sub_pos.mpr hs) hplus
  have hsquare : s^2<r^2/4 := by nlinarith [sq_abs s]
  have hscaled := mul_lt_mul_of_pos_left hsquare heta
  have hnonnegative := mul_nonneg heta.le (sq_nonneg s)
  constructor <;> nlinarith

#print axioms quarticMatchedRicci
#print axioms entropyQuarticCoefficient
#print axioms quarticMatchingCoefficient
#print axioms quarticStateAreaDefect
#print axioms quartic_matched_ricci_cancellation
#print axioms quartic_state_area_defect_identity
#print axioms quartic_state_area_defect_limit
#print axioms quartic_state_area_matching_iff
#print axioms quartic_log_two_bounds
#print axioms quartic_coefficient_lower_bound_algebra
#print axioms quartic_matching_coefficient_lower_bound
#print axioms quartic_matching_coefficient_positive
#print axioms quartic_state_area_small_amplitude_no_go
#print axioms quartic_matching_square_criterion
#print axioms quartic_optical_coefficient_admissible_bounds

end

end ChatgptAudit.Quartic037
