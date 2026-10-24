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
import TGLExt.BinaryRelativeQuartic
import Mathlib.Analysis.Calculus.LHopital
set_option autoImplicit false
set_option maxHeartbeats 2500000
namespace ChatgptAudit.Clock040
open Filter Set TGLExt ChatgptAudit.Micro021 ChatgptAudit.Response028
  ChatgptAudit.Quartic037 ChatgptAudit.Flow020
open scoped Topology
noncomputable section

/-- A cubic primitive limit from an actual derivative on the negative half-neighbourhood. -/
theorem primitive_cubic_limit (flux primitive : ℝ → ℝ) (coefficient : ℝ)
    (hderiv : ∀ᶠ t in 𝓝[<] (0:ℝ), HasDerivAt primitive (flux t) t)
    (hcontinuous : ContinuousAt primitive 0) (hzero : primitive 0 = 0)
    (hflux : Tendsto (fun t => flux t / t^2) (𝓝[<] 0) (𝓝 coefficient)) :
    Tendsto (fun t => primitive t / t^3) (𝓝[<] 0) (𝓝 (coefficient / 3)) := by
  have hg : ∀ᶠ t in 𝓝[<] (0:ℝ),
      HasDerivAt (fun s : ℝ => s^3) (3*t^2) t :=
    Filter.Eventually.of_forall (fun t => by
      have h := (hasDerivAt_id t).pow 3
      have he : (id ^ 3 : ℝ → ℝ) = (fun s : ℝ => s^3) := by funext s; rfl
      rw [he] at h
      simpa using h)
  have hgn : ∀ᶠ t in 𝓝[<] (0:ℝ), 3*t^2 ≠ 0 := by
    filter_upwards [self_mem_nhdsWithin] with t ht
    exact mul_ne_zero (by norm_num) (pow_ne_zero _ (ne_of_lt ht))
  have hfzero : Tendsto primitive (𝓝[<] 0) (𝓝 0) := by
    simpa only [hzero] using hcontinuous.tendsto.mono_left nhdsWithin_le_nhds
  have hgzero : Tendsto (fun t : ℝ => t^3) (𝓝[<] 0) (𝓝 0) := by
    simpa using ((continuousAt_id : ContinuousAt (fun t : ℝ => t) 0).pow 3).tendsto.mono_left nhdsWithin_le_nhds
  have hratio : Tendsto (fun t => flux t/(3*t^2)) (𝓝[<] 0) (𝓝 (coefficient/3)) := by
    simpa only [mul_comm (3:ℝ), div_mul_eq_div_div] using hflux.div_const (3:ℝ)
  exact HasDerivAt.lhopital_zero_nhdsLT hderiv hg hgn hfzero hgzero hratio

def binaryEntropySlope (k y : ℝ) : ℝ :=
  k*(Real.log (1/3+k*y)-Real.log (1/3)) -
    k*(Real.log (1-(1/3+k*y))-Real.log (1-(1/3)))

def binaryEntropyCurvature (k y : ℝ) : ℝ :=
  k^2/(1/3+k*y)+k^2/(1-(1/3+k*y))

theorem binary_entropy_slope_zero (k : ℝ) : binaryEntropySlope k 0 = 0 := by
  simp [binaryEntropySlope]

theorem binary_entropy_curvature_zero (k : ℝ) :
    binaryEntropyCurvature k 0 = (9/2)*k^2 := by
  norm_num [binaryEntropyCurvature]; ring

theorem binary_entropy_curvature_derivative_zero (k : ℝ) :
    HasDerivAt (binaryEntropyCurvature k) (-(27/4)*k^3) 0 := by
  have hp := ((hasDerivAt_id (0:ℝ)).const_mul k).const_add (1/3:ℝ)
  have hq := hp.const_sub 1
  have h := ((hasDerivAt_const (0:ℝ) (k^2)).div hp (by norm_num)).add
    ((hasDerivAt_const (0:ℝ) (k^2)).div hq (by norm_num))
  convert h using 1
  all_goals first | rfl | (norm_num; ring)

theorem binary_entropy_positive_near (k : ℝ) :
    ∀ᶠ y in 𝓝 (0:ℝ), 0 < 1/3+k*y ∧ 0 < 1-(1/3+k*y) := by
  have hp := ((hasDerivAt_id (0:ℝ)).const_mul k).const_add (1/3:ℝ)
  have hq := hp.const_sub 1
  have ha := hp.continuousAt.eventually (Ioi_mem_nhds (by norm_num : (0:ℝ)<1/3+k*0))
  have hb := hq.continuousAt.eventually (Ioi_mem_nhds (by norm_num : (0:ℝ)<1-(1/3+k*0)))
  exact ha.and hb

theorem binary_entropy_slope_derivative (k y : ℝ)
    (hp : 1/3+k*y ≠ 0) (hq : 1-(1/3+k*y) ≠ 0) :
    HasDerivAt (binaryEntropySlope k) (binaryEntropyCurvature k y) y := by
  have ha := ((hasDerivAt_id y).const_mul k).const_add (1/3:ℝ)
  have hb := ha.const_sub 1
  have h := (((ha.log hp).sub_const (Real.log (1/3))).const_mul k).sub
    (((hb.log hq).sub_const (Real.log (1-(1/3)))).const_mul k)
  convert h using 1 <;> first | rfl | dsimp [binaryEntropyCurvature]; ring

theorem binary_entropy_actual_derivative (k : ℝ) :
    ∀ᶠ y in 𝓝[<] (0:ℝ),
      HasDerivAt
        (fun z => diagonalRelativeEntropy (siteW (1/3+k*z)) (siteW (1/3)))
        (binaryEntropySlope k y) y := by
  have h := relative_curve_derivative_past (binaryAffineCurve k)
    (siteW_pos (by norm_num) (by norm_num))
  filter_upwards [h] with y hy
  convert hy using 1
  · rfl
  · simp [relativeEntropyRate, binaryAffineCurve, binaryEntropySlope, siteW,
      Fin.sum_univ_two]
    ring

theorem binary_entropy_slope_quadratic_limit (k : ℝ) :
    Tendsto (fun y => (binaryEntropySlope k y-(9/2)*k^2*y)/y^2)
      (𝓝[<] 0) (𝓝 (-(27/8)*k^3)) := by
  have hc := binary_entropy_curvature_derivative_zero k
  have hs : Tendsto (fun y => (binaryEntropyCurvature k y-(9/2)*k^2)/y)
      (𝓝[<] 0) (𝓝 (-(27/4)*k^3)) := by
    simpa only [zero_add, binary_entropy_curvature_zero, sub_zero,
      smul_eq_mul, div_eq_mul_inv, mul_comm] using hc.tendsto_slope_zero_left
  have h := primitive_quadratic_limit
    (fun y => binaryEntropyCurvature k y-(9/2)*k^2)
    (fun y => binaryEntropySlope k y-(9/2)*k^2*y) (-(27/4)*k^3) ?_ ?_ ?_ hs
  · convert h using 1
    ring
  · filter_upwards [(binary_entropy_positive_near k).filter_mono nhdsWithin_le_nhds] with y hy
    convert (binary_entropy_slope_derivative k y (ne_of_gt hy.1) (ne_of_gt hy.2)).sub
      ((hasDerivAt_id y).const_mul ((9/2)*k^2)) using 1
    all_goals first | rfl | simp only [mul_one]
  · exact ((binary_entropy_slope_derivative k 0 (by norm_num) (by norm_num)).continuousAt).sub
      (continuousAt_const.mul continuousAt_id)
  · simp [binary_entropy_slope_zero]

theorem binary_entropy_cubic_limit (k : ℝ) :
    Tendsto (fun y => (diagonalRelativeEntropy (siteW (1/3+k*y)) (siteW (1/3)) -
        (9/4)*k^2*y^2)/y^3)
      (𝓝[<] 0) (𝓝 (-(9/8)*k^3)) := by
  have h := primitive_cubic_limit
    (fun y => binaryEntropySlope k y-(9/2)*k^2*y)
    (fun y => diagonalRelativeEntropy (siteW (1/3+k*y)) (siteW (1/3)) -
      (9/4)*k^2*y^2) (-(27/8)*k^3) ?_ ?_ ?_
    (binary_entropy_slope_quadratic_limit k)
  · convert h using 1
    ring
  · filter_upwards [binary_entropy_actual_derivative k] with y hy
    have hd := ((hasDerivAt_id y).pow 2).const_mul ((9/4)*k^2)
    simp only [id_eq] at hd
    convert hy.sub hd using 1 <;> first | rfl | ring
  · exact (relative_curve_continuous_zero (binaryAffineCurve k)
      (siteW_pos (by norm_num) (by norm_num))).sub
        (continuousAt_const.mul (continuousAt_id.pow 2))
  · simp only [mul_zero, add_zero, relative_entropy_self, zero_pow (by norm_num : 2 ≠ 0), sub_zero]

theorem regular_parameter_square_sixth_limit :
    Tendsto (fun t : ℝ => (regularParameter t ^ 2 - t^4)/t^6)
      (𝓝[≠] 0) (𝓝 (-2)) := by
  have ht := quartic_time_tendsto_zero
  have h := ((ht.pow 2).const_add 2).neg.div (((ht.pow 2).const_add 1).pow 2) (by norm_num)
  norm_num at h
  apply h.congr'
  filter_upwards [quartic_punctured_time_nonzero] with t ht0
  dsimp [regularParameter]
  field_simp [ht0]
  ring

/-- Sixth order of the actual existing one-site relative entropy. -/
theorem binary_relative_sixth_limit (k : ℝ) :
    Tendsto (fun t : ℝ => (binaryRelativeAt k t-(9/4)*k^2*t^4)/t^6)
      (𝓝[≠] 0) (𝓝 (-(9/2)*k^2+(9/8)*k^3)) := by
  have hbase := (binary_entropy_cubic_limit k).comp quartic_negative_regular_parameter_tendsto
  have hratio : Tendsto (fun t : ℝ => (-regularParameter t)^3/t^6)
      (𝓝[≠] 0) (𝓝 (-1)) := by
    have h := quartic_regular_parameter_ratio.neg.pow 3
    norm_num at h
    apply h.congr'
    filter_upwards [quartic_punctured_time_nonzero] with t ht0
    field_simp [ht0]
  have h := (hbase.mul hratio).add
    (regular_parameter_square_sixth_limit.const_mul ((9/4)*k^2))
  have hvalue : (-(9/8)*k^3)*(-1)+((9/4)*k^2)*(-2) =
      -(9/2)*k^2+(9/8)*k^3 := by ring
  rw [hvalue] at h
  apply h.congr'
  filter_upwards [quartic_punctured_time_nonzero] with t ht0
  have hh : regularParameter t ≠ 0 := ne_of_gt (regular_parameter_positive t ht0)
  have he : 1/3+k*(-regularParameter t)=1/3-k*regularParameter t := by ring
  simp only [Function.comp_def, he, binaryRelativeAt]
  field_simp [ht0, hh]
  ring

/-- The normalized relative entropy, extended by the field convention at zero. -/
def entropyClockRatio (k t : ℝ) : ℝ :=
  binaryRelativeAt k t / ((9/4)*k^2*t^4)

/-- An oriented fourth-root reading; orientation and normalization are explicit. -/
def entropyReadClock (k t : ℝ) : ℝ :=
  t * Real.sqrt (Real.sqrt (entropyClockRatio k t))

theorem entropy_read_clock_zero (k : ℝ) : entropyReadClock k 0 = 0 := by
  simp [entropyReadClock]

theorem entropy_clock_ratio_limit (k : ℝ) (hk : k ≠ 0) :
    Tendsto (entropyClockRatio k) (𝓝[≠] 0) (𝓝 1) := by
  have h := (binary_relative_quartic_limit k).div_const ((9/4)*k^2)
  have ha : (9/4:ℝ)*k^2 ≠ 0 := mul_ne_zero (by norm_num) (pow_ne_zero _ hk)
  have hv : ((9/4:ℝ)*k^2)/((9/4)*k^2) = 1 := div_self ha
  rw [hv] at h
  apply h.congr'
  exact Filter.Eventually.of_forall (fun t => by
    dsimp [entropyClockRatio]
    ring)

theorem entropy_clock_ratio_correction (k : ℝ) (hk : k ≠ 0) :
    Tendsto (fun t => (entropyClockRatio k t-1)/t^2)
      (𝓝[≠] 0) (𝓝 (-2+k/2)) := by
  have h := (binary_relative_sixth_limit k).div_const ((9/4)*k^2)
  have hv : (-(9/2:ℝ)*k^2+(9/8)*k^3)/((9/4)*k^2) = -2+k/2 := by
    field_simp [hk]; ring
  rw [hv] at h
  apply h.congr'
  filter_upwards [quartic_punctured_time_nonzero] with t ht
  dsimp [entropyClockRatio]
  field_simp [hk, ht]

theorem entropy_clock_root_limit (k : ℝ) (hk : k ≠ 0) :
    Tendsto (fun t => Real.sqrt (Real.sqrt (entropyClockRatio k t)))
      (𝓝[≠] 0) (𝓝 1) := by
  simpa only [Real.sqrt_one] using (entropy_clock_ratio_limit k hk).sqrt.sqrt

/-- A real fourth-root correction, with the nonnegative branch displayed. -/
theorem fourth_root_correction_identity (r t : ℝ) (hr : 0 ≤ r) (ht : t ≠ 0) :
    (t*Real.sqrt (Real.sqrt r)-t)/t^3 =
      ((r-1)/t^2) /
        ((Real.sqrt (Real.sqrt r))^3 + (Real.sqrt (Real.sqrt r))^2 +
          Real.sqrt (Real.sqrt r) + 1) := by
  let z := Real.sqrt (Real.sqrt r)
  have hz : 0 ≤ z := Real.sqrt_nonneg _
  have hz4 : z^4 = r := by
    calc
      z^4 = (z^2)^2 := by ring
      _ = (Real.sqrt r)^2 := by rw [Real.sq_sqrt (Real.sqrt_nonneg r)]
      _ = r := Real.sq_sqrt hr
  have hpoly : (z-1)*(z^3+z^2+z+1)=r-1 := by
    rw [← hz4]
    ring
  have hp : 0 < z^3+z^2+z+1 := by positivity
  change (t*z-t)/t^3 = ((r-1)/t^2)/(z^3+z^2+z+1)
  calc
    (t*z-t)/t^3 = (z-1)/t^2 := by field_simp [ht]
    _ = ((r-1)/t^2)/(z^3+z^2+z+1) := by
      apply (eq_div_iff (ne_of_gt hp)).mpr
      rw [div_mul_eq_mul_div, hpoly]

/-- The cubic coefficient of the actual entropy reading, before inversion. -/
theorem entropy_read_clock_cubic_limit (k : ℝ) (hk : k ≠ 0) :
    Tendsto (fun t => (entropyReadClock k t-t)/t^3)
      (𝓝[≠] 0) (𝓝 (-(1/2)+k/8)) := by
  have hz := entropy_clock_root_limit k hk
  have hd := ((hz.pow 3).add (hz.pow 2)).add hz |>.add_const 1
  have h := (entropy_clock_ratio_correction k hk).div hd (by norm_num)
  have hv : (-2+k/2)/((1:ℝ)^3+1^2+1+1)=-(1/2)+k/8 := by ring
  rw [hv] at h
  apply h.congr'
  have hp : ∀ᶠ t in 𝓝[≠] (0:ℝ), 0 < entropyClockRatio k t :=
    (entropy_clock_ratio_limit k hk).eventually (lt_mem_nhds (by norm_num : (0:ℝ)<1))
  filter_upwards [hp, quartic_punctured_time_nonzero] with t ht ht0
  exact (fourth_root_correction_identity (entropyClockRatio k t) t ht.le ht0).symm

theorem entropy_read_clock_ratio_limit (k : ℝ) (hk : k ≠ 0) :
    Tendsto (fun t => entropyReadClock k t/t) (𝓝[≠] 0) (𝓝 1) := by
  apply (entropy_clock_root_limit k hk).congr'
  filter_upwards [quartic_punctured_time_nonzero] with t ht
  dsimp [entropyReadClock]
  field_simp

/-- At nonzero time the fourth power is exactly the existing relative entropy. -/
theorem entropy_read_clock_fourth_power (k t : ℝ)
    (hk : 0 < k) (hb : k ≤ 1/12) (ht : t ≠ 0) :
    ((9/4)*k^2) * (entropyReadClock k t)^4 = binaryRelativeAt k t := by
  have hr : 0 ≤ entropyClockRatio k t := by
    exact div_nonneg (binary_relative_nonnegative k t hk.le hb) (by positivity)
  have hroot : (Real.sqrt (Real.sqrt (entropyClockRatio k t)))^4 =
      entropyClockRatio k t := by
    calc
      _ = ((Real.sqrt (Real.sqrt (entropyClockRatio k t)))^2)^2 := by ring
      _ = (Real.sqrt (entropyClockRatio k t))^2 := by
        rw [Real.sq_sqrt (Real.sqrt_nonneg _)]
      _ = _ := Real.sq_sqrt hr
  rw [entropyReadClock, mul_pow, hroot]
  unfold entropyClockRatio
  field_simp [ne_of_gt hk, ht]

#print axioms entropyClockRatio
#print axioms entropyReadClock
#print axioms entropy_read_clock_zero
#print axioms entropy_clock_ratio_limit
#print axioms entropy_clock_ratio_correction
#print axioms entropy_clock_root_limit
#print axioms fourth_root_correction_identity
#print axioms entropy_read_clock_cubic_limit
#print axioms entropy_read_clock_ratio_limit
#print axioms entropy_read_clock_fourth_power

#print axioms primitive_cubic_limit
#print axioms binaryEntropySlope
#print axioms binaryEntropyCurvature
#print axioms binary_entropy_slope_zero
#print axioms binary_entropy_curvature_zero
#print axioms binary_entropy_curvature_derivative_zero
#print axioms binary_entropy_positive_near
#print axioms binary_entropy_slope_derivative
#print axioms binary_entropy_actual_derivative
#print axioms binary_entropy_slope_quadratic_limit
#print axioms binary_entropy_cubic_limit
#print axioms regular_parameter_square_sixth_limit
#print axioms binary_relative_sixth_limit
end
end ChatgptAudit.Clock040
