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
import TGLExt.UniformQuadraticResponse
import TGLExt.RelativeEntropyFisherLimit

set_option autoImplicit false
set_option maxHeartbeats 1400000

namespace ChatgptAudit.Quartic037

open Filter Topology Set TGLExt ChatgptAudit.Micro021 ChatgptAudit.Response028

noncomputable section

/- The affine variable y is used only to instantiate the verified finite-state
relative-entropy theorem. Physical time enters through y = -regularParameter t.
No global positivity of the auxiliary affine curve is postulated. -/

theorem binary_affine_derivative (k y : ℝ) (i : Fin 2) :
    HasDerivAt (fun z : ℝ => siteW (1 / 3 + k * z) i)
      (if i = 0 then k else -k) y := by
  have h := ((hasDerivAt_id y).const_mul k).const_add (1 / 3 : ℝ)
  fin_cases i
  · simpa [siteW] using h
  · simpa [siteW] using h.const_sub 1

def binaryAffineCurve (k : ℝ) : DiagonalStateCurve (siteW (1 / 3)) where
  weights y := siteW (1 / 3 + k * y)
  tangent _ i := if i = 0 then k else -k
  at_zero i := by simp only [mul_zero, add_zero]
  trace_one y := siteW_sum _
  derivative_zero i := binary_affine_derivative k 0 i
  derivative_past := Filter.Eventually.of_forall (fun y i => binary_affine_derivative k y i)
  tangent_continuous i := continuousAt_const

theorem binary_affine_relative_quadratic_limit (k : ℝ) :
    Tendsto
      (fun y : ℝ => diagonalRelativeEntropy (siteW (1 / 3 + k * y))
        (siteW (1 / 3)) / y ^ 2)
      (𝓝[<] 0) (𝓝 ((9 / 4) * k ^ 2)) := by
  have h := relative_entropy_curve_quadratic_limit (binaryAffineCurve k)
    (siteW_pos (by norm_num) (by norm_num))
  have hc : diagonalFisher (siteW (1 / 3)) ((binaryAffineCurve k).tangent 0) / 2 =
      (9 / 4) * k ^ 2 := by
    norm_num [diagonalFisher, binaryAffineCurve, siteW, Fin.sum_univ_two]
    ring
  rw [hc] at h
  exact h

def binaryRelativeAt (k t : ℝ) : ℝ :=
  diagonalRelativeEntropy (siteW (1 / 3 - k * regularParameter t)) (siteW (1 / 3))

theorem quartic_punctured_time_nonzero : ∀ᶠ t : ℝ in 𝓝[≠] 0, t ≠ 0 := by
  filter_upwards [self_mem_nhdsWithin] with t ht
  simpa only [Set.mem_compl_iff, Set.mem_singleton_iff] using ht

theorem quartic_time_tendsto_zero :
    Tendsto (fun t : ℝ => t) (𝓝[≠] 0) (𝓝 0) :=
  tendsto_id'.mpr nhdsWithin_le_nhds

theorem quartic_regular_parameter_tendsto_zero :
    Tendsto regularParameter (𝓝[≠] (0 : ℝ)) (𝓝 0) := by
  apply squeeze_zero regular_parameter_nonnegative regular_parameter_le_square
  simpa using quartic_time_tendsto_zero.pow 2

theorem quartic_negative_regular_parameter_tendsto :
    Tendsto (fun t : ℝ => -regularParameter t) (𝓝[≠] 0) (𝓝[<] 0) := by
  apply tendsto_nhdsWithin_iff.mpr
  constructor
  · simpa only [neg_zero] using quartic_regular_parameter_tendsto_zero.neg
  · filter_upwards [quartic_punctured_time_nonzero] with t ht
    change -regularParameter t < 0
    linarith [regular_parameter_positive t ht]

theorem quartic_regular_parameter_ratio :
    Tendsto (fun t : ℝ => regularParameter t / t ^ 2) (𝓝[≠] 0) (𝓝 1) := by
  simpa only [one_mul, one_pow, id_eq] using
    regular_parameter_ratio_along 1 id quartic_time_tendsto_zero
      quartic_punctured_time_nonzero

theorem binary_relative_quartic_identity (k t : ℝ) (ht : t ≠ 0) :
    binaryRelativeAt k t / t ^ 4 =
      (diagonalRelativeEntropy (siteW (1 / 3 + k * (-regularParameter t)))
        (siteW (1 / 3)) / (-regularParameter t) ^ 2) *
      (regularParameter t / t ^ 2) ^ 2 := by
  have hh : regularParameter t ≠ 0 := ne_of_gt (regular_parameter_positive t ht)
  have hq : 1 / 3 + k * (-regularParameter t) = 1 / 3 - k * regularParameter t := by
    ring
  unfold binaryRelativeAt
  rw [hq]
  field_simp [ht, hh]

theorem binary_relative_quartic_limit (k : ℝ) :
    Tendsto (fun t : ℝ => binaryRelativeAt k t / t ^ 4)
      (𝓝[≠] 0) (𝓝 ((9 / 4) * k ^ 2)) := by
  have hlocal := (binary_affine_relative_quadratic_limit k).comp
    quartic_negative_regular_parameter_tendsto
  have h := hlocal.mul (quartic_regular_parameter_ratio.pow 2)
  have h' : Tendsto
      (fun t : ℝ =>
        (diagonalRelativeEntropy (siteW (1 / 3 + k * (-regularParameter t)))
          (siteW (1 / 3)) / (-regularParameter t) ^ 2) *
        (regularParameter t / t ^ 2) ^ 2)
      (𝓝[≠] 0) (𝓝 ((9 / 4) * k ^ 2)) := by
    simpa only [Function.comp_def, one_pow, mul_one] using h
  apply h'.congr'
  filter_upwards [quartic_punctured_time_nonzero] with t ht
  exact (binary_relative_quartic_identity k t ht).symm

theorem binary_relative_admissible (k t : ℝ) (hk : 0 ≤ k) (hb : k ≤ 1 / 12) :
    0 < 1 / 3 - k * regularParameter t ∧ 1 / 3 - k * regularParameter t < 1 := by
  have hl := mul_nonneg hk (regular_parameter_nonnegative t)
  have hu := (mul_le_of_le_one_right hk (regular_parameter_lt_one t).le).trans hb
  constructor <;> linarith

theorem binary_relative_nonnegative (k t : ℝ) (hk : 0 ≤ k) (hb : k ≤ 1 / 12) :
    0 ≤ binaryRelativeAt k t := by
  obtain ⟨h0, h1⟩ := binary_relative_admissible k t hk hb
  exact (third_binary_relative_bound (1 / 3 - k * regularParameter t) h0 h1).1

theorem binary_relative_quartic_bound (k : ℝ) (hk : 0 ≤ k) (hb : k ≤ 1 / 12)
    (t : ℝ) :
    0 ≤ binaryRelativeAt k t / t ^ 4 ∧
      binaryRelativeAt k t / t ^ 4 ≤ (9 / 2) * k ^ 2 := by
  constructor
  · exact div_nonneg (binary_relative_nonnegative k t hk hb) (by positivity)
  · by_cases ht : t = 0
    · simp only [ht, zero_pow (by decide : 4 ≠ 0), div_zero]
      positivity
    have hh : (regularParameter t) ^ 2 ≤ t ^ 4 := by
      have hn := regular_parameter_nonnegative t
      have hu := regular_parameter_le_square t
      nlinarith [mul_nonneg (sub_nonneg.mpr hu) (add_nonneg (sq_nonneg t) hn)]
    obtain ⟨h0, h1⟩ := binary_relative_admissible k t hk hb
    have hbound := (third_binary_relative_bound (1 / 3 - k * regularParameter t) h0 h1).2
    have hnum : binaryRelativeAt k t ≤ ((9 / 2) * k ^ 2) * t ^ 4 := by
      calc
        binaryRelativeAt k t ≤ (9 / 2) * (1 / 3 - k * regularParameter t - 1 / 3) ^ 2 :=
          hbound
        _ = ((9 / 2) * k ^ 2) * (regularParameter t) ^ 2 := by ring
        _ ≤ ((9 / 2) * k ^ 2) * t ^ 4 := mul_le_mul_of_nonneg_left hh (by positivity)
    have ht4 : 0 < t ^ 4 := by
      simpa only [← pow_mul] using sq_pos_of_ne_zero (pow_ne_zero 2 ht)
    exact (div_le_iff₀ ht4).mpr hnum

#print axioms binary_affine_derivative
#print axioms binaryAffineCurve
#print axioms binary_affine_relative_quadratic_limit
#print axioms binaryRelativeAt
#print axioms quartic_punctured_time_nonzero
#print axioms quartic_time_tendsto_zero
#print axioms quartic_regular_parameter_tendsto_zero
#print axioms quartic_negative_regular_parameter_tendsto
#print axioms quartic_regular_parameter_ratio
#print axioms binary_relative_quartic_identity
#print axioms binary_relative_quartic_limit
#print axioms binary_relative_admissible
#print axioms binary_relative_nonnegative
#print axioms binary_relative_quartic_bound

end

end ChatgptAudit.Quartic037
