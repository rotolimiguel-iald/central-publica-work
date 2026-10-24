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
import Mathlib.Analysis.Calculus.Taylor
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv

set_option autoImplicit false
set_option maxHeartbeats 5000000

namespace ChatgptAudit.Clock040
open Filter Set TGLExt ChatgptAudit.Micro021 ChatgptAudit.Response028
open scoped Topology
noncomputable section

/- A single-site Fisher path, with an explicit orientation and square-clock
normalization. No uniqueness or spacetime interpretation of this clock is assumed. -/

def fisherAngularRate (k : ℝ) : ℝ :=
  k / (2 * Real.sqrt (1 / 3 : ℝ) * Real.sqrt (2 / 3 : ℝ))

def fisherSineCoordinate (k x : ℝ) : ℝ :=
  Real.sqrt (1 / 3 : ℝ) * Real.cos (fisherAngularRate k * x) -
    Real.sqrt (2 / 3 : ℝ) * Real.sin (fisherAngularRate k * x)

def fisherCosineCoordinate (k x : ℝ) : ℝ :=
  Real.sqrt (2 / 3 : ℝ) * Real.cos (fisherAngularRate k * x) +
    Real.sqrt (1 / 3 : ℝ) * Real.sin (fisherAngularRate k * x)

def fisherAffineWeight (k x : ℝ) : ℝ := (fisherSineCoordinate k x)^2

def fisherAffineTangent (k x : ℝ) : ℝ :=
  -2 * fisherAngularRate k * fisherSineCoordinate k x * fisherCosineCoordinate k x

def fisherWeight (k u : ℝ) : ℝ := fisherAffineWeight k (u^2)

def fisherWeightTangent (k u : ℝ) : ℝ := fisherAffineTangent k (u^2) * (2*u)

def fisherLengthPrimitive (k u : ℝ) : ℝ := 2 * fisherAngularRate k * u^2

/-- The square of the original parameter, obtained by solving h(t)=(p-q)/k. -/
def fisherClockSquare (k u : ℝ) : ℝ :=
  ((1 / 3 : ℝ) - fisherWeight k u) / (k - 1 / 3 + fisherWeight k u)

/-- The oriented inverse clock. Its normalizing quotient is used only near zero. -/
def fisherOriginalTime (k u : ℝ) : ℝ :=
  u * Real.sqrt (fisherClockSquare k u / u^2)

theorem fisher_angular_rate_square (k : ℝ) :
    (fisherAngularRate k)^2 = (9 / 8 : ℝ)*k^2 := by
  simp only [fisherAngularRate, div_pow, mul_pow,
    Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 1/3),
    Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2/3)]
  ring

theorem fisher_angular_rate_positive (k : ℝ) (hk : 0<k) :
    0<fisherAngularRate k := by
  unfold fisherAngularRate
  positivity

theorem fisher_coordinates_normalized (k x : ℝ) :
    (fisherSineCoordinate k x)^2+(fisherCosineCoordinate k x)^2=1 := by
  have ha := Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 1/3)
  have hc := Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2/3)
  have ht := Real.sin_sq_add_cos_sq (fisherAngularRate k*x)
  calc
    (fisherSineCoordinate k x)^2+(fisherCosineCoordinate k x)^2 =
        ((Real.sqrt (1/3 : ℝ))^2+(Real.sqrt (2/3 : ℝ))^2) *
          ((Real.sin (fisherAngularRate k*x))^2+(Real.cos (fisherAngularRate k*x))^2) := by
      dsimp [fisherSineCoordinate, fisherCosineCoordinate]
      ring
    _ = 1 := by rw [ha, hc, ht]; norm_num

theorem fisher_sine_derivative (k x : ℝ) :
    HasDerivAt (fisherSineCoordinate k)
      (-fisherAngularRate k * fisherCosineCoordinate k x) x := by
  have hd := (hasDerivAt_id x).const_mul (fisherAngularRate k)
  have hh := (hd.cos.const_mul (Real.sqrt (1/3 : ℝ))).sub
    (hd.sin.const_mul (Real.sqrt (2/3 : ℝ)))
  exact hh.congr_deriv (by dsimp [fisherCosineCoordinate]; ring)

theorem fisher_cosine_derivative (k x : ℝ) :
    HasDerivAt (fisherCosineCoordinate k)
      (fisherAngularRate k * fisherSineCoordinate k x) x := by
  have hd := (hasDerivAt_id x).const_mul (fisherAngularRate k)
  have hh := (hd.cos.const_mul (Real.sqrt (2/3 : ℝ))).add
    (hd.sin.const_mul (Real.sqrt (1/3 : ℝ)))
  exact hh.congr_deriv (by dsimp [fisherSineCoordinate]; ring)

theorem fisher_affine_derivative (k x : ℝ) :
    HasDerivAt (fisherAffineWeight k) (fisherAffineTangent k x) x := by
  exact ((fisher_sine_derivative k x).pow 2).congr_deriv
    (by dsimp [fisherAffineTangent]; ring)

theorem fisher_affine_tangent_derivative (k x : ℝ) :
    HasDerivAt (fisherAffineTangent k)
      (2*(fisherAngularRate k)^2*
        ((fisherCosineCoordinate k x)^2-(fisherSineCoordinate k x)^2)) x := by
  have hh := ((fisher_sine_derivative k x).const_mul
    (-2*fisherAngularRate k)).mul (fisher_cosine_derivative k x)
  exact hh.congr_deriv (by ring)

theorem fisher_affine_deriv (k : ℝ) :
    deriv (fisherAffineWeight k)=fisherAffineTangent k := by
  funext x
  exact (fisher_affine_derivative k x).deriv

theorem fisher_affine_zero (k : ℝ) : fisherAffineWeight k 0=1/3 := by
  simp [fisherAffineWeight, fisherSineCoordinate]

theorem fisher_affine_first_zero (k : ℝ) :
    iteratedDeriv 1 (fisherAffineWeight k) 0 = -k := by
  rw [iteratedDeriv_one, fisher_affine_deriv]
  have ha : Real.sqrt (1/3 : ℝ)≠0 := ne_of_gt (Real.sqrt_pos.mpr (by norm_num))
  have hc : Real.sqrt (2/3 : ℝ)≠0 := ne_of_gt (Real.sqrt_pos.mpr (by norm_num))
  simp only [fisherAffineTangent, fisherSineCoordinate, fisherCosineCoordinate,
    mul_zero, Real.cos_zero, Real.sin_zero, mul_one, sub_zero, add_zero]
  unfold fisherAngularRate
  field_simp [ha, hc]

theorem fisher_affine_second_zero (k : ℝ) :
    iteratedDeriv 2 (fisherAffineWeight k) 0 = (3/4 : ℝ)*k^2 := by
  rw [iteratedDeriv_succ (n := 1), iteratedDeriv_one,
    fisher_affine_deriv, (fisher_affine_tangent_derivative k 0).deriv]
  simp only [fisherSineCoordinate, fisherCosineCoordinate, mul_zero,
    Real.cos_zero, Real.sin_zero, mul_one, sub_zero, add_zero]
  rw [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 1/3),
    Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2/3), fisher_angular_rate_square]
  ring

theorem fisher_affine_contDiff (k : ℝ) : ContDiff ℝ 2 (fisherAffineWeight k) := by
  unfold fisherAffineWeight fisherSineCoordinate
  fun_prop

theorem fisher_affine_taylor_two (k x : ℝ) :
    taylorWithinEval (fisherAffineWeight k) 2 univ 0 x =
      1/3-k*x+(3/8 : ℝ)*k^2*x^2 := by
  norm_num [taylor_within_apply, Finset.sum_range_succ, iteratedDerivWithin_univ,
    iteratedDeriv_zero, fisher_affine_zero, fisher_affine_first_zero,
    fisher_affine_second_zero]
  ring

theorem fisher_affine_taylor_limit (k : ℝ) :
    Tendsto (fun x : ℝ =>
      (fisherAffineWeight k x-(1/3-k*x+(3/8 : ℝ)*k^2*x^2))/x^2)
      (𝓝 0) (𝓝 0) := by
  have hh := Real.taylor_tendsto (f := fisherAffineWeight k)
    (x₀ := 0) (n := 2) (s := univ) convex_univ (mem_univ 0)
    (fisher_affine_contDiff k).contDiffOn
  simpa only [nhdsWithin_univ, sub_zero, fisher_affine_taylor_two] using hh

theorem fisher_weight_derivative (k u : ℝ) :
    HasDerivAt (fisherWeight k) (fisherWeightTangent k u) u := by
  have hh := (fisher_affine_derivative k (u^2)).comp u ((hasDerivAt_id u).pow 2)
  convert hh using 1
  all_goals first | rfl | (simp [fisherWeightTangent])

theorem fisher_weight_zero (k : ℝ) : fisherWeight k 0=1/3 := by
  simpa only [fisherWeight, zero_pow (by decide : 2≠0)] using fisher_affine_zero k

theorem fisher_weight_tendsto (k : ℝ) :
    Tendsto (fisherWeight k) (𝓝 0) (𝓝 (1/3)) := by
  simpa only [fisher_weight_zero] using (fisher_weight_derivative k 0).continuousAt.tendsto

theorem fisher_weight_positive_near_zero (k : ℝ) :
    ∀ᶠ u in 𝓝 (0 : ℝ), 0<fisherWeight k u ∧ fisherWeight k u<1 := by
  exact (fisher_weight_tendsto k).eventually
    (Ioo_mem_nhds (by norm_num : (0 : ℝ)<1/3) (by norm_num : (1/3 : ℝ)<1))

theorem fisher_weight_quartic_limit (k : ℝ) :
    Tendsto (fun u : ℝ => (fisherWeight k u-1/3+k*u^2)/u^4)
      (𝓝[≠] 0) (𝓝 ((3/8 : ℝ)*k^2)) := by
  have hs : Tendsto (fun u : ℝ => u^2) (𝓝[≠] 0) (𝓝 0) := by
    simpa using (ChatgptAudit.Quartic037.quartic_time_tendsto_zero.pow 2)
  have hh := ((fisher_affine_taylor_limit k).comp hs).add_const ((3/8 : ℝ)*k^2)
  have he :
      (fun u : ℝ => (fisherWeight k u-1/3+k*u^2)/u^4) =ᶠ[𝓝[≠] 0]
      (fun u : ℝ =>
        (fisherAffineWeight k (u^2)-
          (1/3-k*(u^2)+(3/8 : ℝ)*k^2*(u^2)^2))/(u^2)^2+(3/8 : ℝ)*k^2) := by
    filter_upwards [self_mem_nhdsWithin] with u hu
    have hu0 : u≠0 := hu
    dsimp [fisherWeight]
    field_simp [hu0]
    ring
  exact (tendsto_congr' he).2 (by simpa only [Function.comp_def, zero_add] using hh)

/-- Fisher is computed from the two differentiated probabilities of this curve. -/
theorem fisher_weight_fisher (k u : ℝ)
    (hp : 0<fisherWeight k u) (hq : fisherWeight k u<1) :
    diagonalFisher (siteW (fisherWeight k u))
      (fun i : Fin 2 => if i=0 then fisherWeightTangent k u else -fisherWeightTangent k u) =
        18*k^2*u^2 := by
  have hp0 : fisherWeight k u≠0 := ne_of_gt hp
  have hq0 : 1-fisherWeight k u≠0 := ne_of_gt (sub_pos.mpr hq)
  have hcomp : 1-(fisherSineCoordinate k (u^2))^2 =
      (fisherCosineCoordinate k (u^2))^2 := by
    linarith [fisher_coordinates_normalized k (u^2)]
  have hs0 : fisherSineCoordinate k (u^2)≠0 := by
    intro hz
    simp [fisherWeight, fisherAffineWeight, hz] at hp0
  have hc0 : fisherCosineCoordinate k (u^2)≠0 := by
    intro hz
    have he : 1-fisherWeight k u=0 := by
      change 1-(fisherSineCoordinate k (u^2))^2=0
      rw [hcomp, hz]
      norm_num
    exact hq0 he
  calc
    diagonalFisher (siteW (fisherWeight k u))
        (fun i : Fin 2 => if i=0 then fisherWeightTangent k u else -fisherWeightTangent k u) =
        (fisherWeightTangent k u)^2/(fisherWeight k u*(1-fisherWeight k u)) := by
      norm_num [diagonalFisher, siteW, Fin.sum_univ_two]
      field_simp [hp0, hq0]
      ring
    _ = 16*(fisherAngularRate k)^2*u^2 := by
      dsimp [fisherWeightTangent, fisherAffineTangent, fisherWeight, fisherAffineWeight]
      rw [hcomp]
      field_simp [hs0, hc0]
      ring
    _ = 18*k^2*u^2 := by rw [fisher_angular_rate_square]; ring

theorem fisher_length_derivative (k u : ℝ) :
    HasDerivAt (fisherLengthPrimitive k) (4*fisherAngularRate k*u) u := by
  exact (((hasDerivAt_id u).pow 2).const_mul (2*fisherAngularRate k)).congr_deriv
    (by simp only [id_eq]; ring)

theorem fisher_length_speed (k u : ℝ) (hk : 0<k) (hu : 0≤u)
    (hp : 0<fisherWeight k u) (hq : fisherWeight k u<1) :
    Real.sqrt (diagonalFisher (siteW (fisherWeight k u))
      (fun i : Fin 2 => if i=0 then fisherWeightTangent k u else -fisherWeightTangent k u)) =
        deriv (fisherLengthPrimitive k) u := by
  rw [fisher_weight_fisher k u hp hq, (fisher_length_derivative k u).deriv]
  have he : 18*k^2*u^2=(4*fisherAngularRate k*u)^2 := by
    rw [mul_pow, mul_pow, fisher_angular_rate_square]
    ring
  have hr := (fisher_angular_rate_positive k hk).le
  rw [he, Real.sqrt_sq_eq_abs, abs_of_nonneg (by positivity : 0≤4*fisherAngularRate k*u)]

theorem fisher_length_normalized (k u : ℝ) (hk : 0<k) :
    fisherLengthPrimitive k u/(2*fisherAngularRate k)=u^2 := by
  have hr : fisherAngularRate k≠0 := ne_of_gt (fisher_angular_rate_positive k hk)
  unfold fisherLengthPrimitive
  field_simp [hr]

theorem fisher_weight_quadratic_limit (k : ℝ) :
    Tendsto (fun u : ℝ => (1/3-fisherWeight k u)/u^2)
      (𝓝[≠] 0) (𝓝 k) := by
  have hs : Tendsto (fun u : ℝ => u^2) (𝓝[≠] 0) (𝓝 0) := by
    simpa using (ChatgptAudit.Quartic037.quartic_time_tendsto_zero.pow 2)
  have hconst : Tendsto (fun _ : ℝ => k) (𝓝[≠] 0) (𝓝 k) := tendsto_const_nhds
  have hh := hconst.sub ((fisher_weight_quartic_limit k).mul hs)
  have he : (fun u : ℝ => (1/3-fisherWeight k u)/u^2) =ᶠ[𝓝[≠] 0]
      (fun u : ℝ => k-((fisherWeight k u-1/3+k*u^2)/u^4)*u^2) := by
    filter_upwards [self_mem_nhdsWithin] with u hu
    have hu0 : u≠0 := hu
    field_simp [hu0]
    ring
  exact (tendsto_congr' he).2 (by simpa only [mul_zero, sub_zero] using hh)

theorem fisher_clock_denominator_limit (k : ℝ) :
    Tendsto (fun u : ℝ => k-1/3+fisherWeight k u) (𝓝[≠] 0) (𝓝 k) := by
  have hh : Tendsto (fisherWeight k) (𝓝[≠] 0) (𝓝 (1/3)) :=
    (fisher_weight_tendsto k).mono_left nhdsWithin_le_nhds
  simpa only [sub_add_cancel] using hh.const_add (k-1/3)

theorem fisher_clock_square_quadratic_limit (k : ℝ) (hk : 0<k) :
    Tendsto (fun u : ℝ => fisherClockSquare k u/u^2)
      (𝓝[≠] 0) (𝓝 1) := by
  have hh := (fisher_weight_quadratic_limit k).div
    (fisher_clock_denominator_limit k) (ne_of_gt hk)
  have he : (fun u : ℝ => fisherClockSquare k u/u^2) =
      (fun u : ℝ => ((1/3-fisherWeight k u)/u^2)/(k-1/3+fisherWeight k u)) := by
    funext u
    unfold fisherClockSquare
    ring
  rw [he]
  rw [div_self (ne_of_gt hk)] at hh
  convert hh using 1
  all_goals rfl

theorem fisher_clock_square_quartic_limit (k : ℝ) (hk : 0<k) :
    Tendsto (fun u : ℝ => (fisherClockSquare k u-u^2)/u^4)
      (𝓝[≠] 0) (𝓝 (1-(3/8 : ℝ)*k)) := by
  have hh := ((fisher_weight_quartic_limit k).neg.add
    (fisher_weight_quadratic_limit k)).div
      (fisher_clock_denominator_limit k) (ne_of_gt hk)
  have hden : ∀ᶠ u in 𝓝[≠] (0 : ℝ), k-1/3+fisherWeight k u≠0 :=
    (fisher_clock_denominator_limit k).eventually_ne (ne_of_gt hk)
  have he : (fun u : ℝ => (fisherClockSquare k u-u^2)/u^4) =ᶠ[𝓝[≠] 0]
      (fun u : ℝ => (-(fisherWeight k u-1/3+k*u^2)/u^4+
        (1/3-fisherWeight k u)/u^2)/(k-1/3+fisherWeight k u)) := by
    filter_upwards [self_mem_nhdsWithin, hden] with u hu hd
    have hu0 : u≠0 := hu
    have hd3 : 3*k-1+3*fisherWeight k u≠0 := by
      intro hz
      apply hd
      linarith
    have hd3' : -1+fisherWeight k u*3+k*3≠0 := by
      intro hz
      apply hd
      linarith
    unfold fisherClockSquare
    field_simp [hu0, hd, hd3, hd3']
    all_goals ring
  have hc : (-((3/8 : ℝ)*k^2)+k)/k=1-(3/8 : ℝ)*k := by
    field_simp [ne_of_gt hk]
    ring
  apply (tendsto_congr' he).2
  rw [hc] at hh
  convert hh using 1
  all_goals first | rfl | (funext u; simp only [Pi.div_apply]; ring)

theorem fisher_clock_ratio_positive (k : ℝ) (hk : 0<k) :
    ∀ᶠ u in 𝓝[≠] (0 : ℝ), 0<fisherClockSquare k u/u^2 :=
  (fisher_clock_square_quadratic_limit k hk).eventually
    (Ioi_mem_nhds (by norm_num : (0 : ℝ)<1))

theorem fisher_original_time_zero (k : ℝ) : fisherOriginalTime k 0=0 := by
  simp [fisherOriginalTime]

theorem fisher_original_time_square (k : ℝ) (hk : 0<k) :
    ∀ᶠ u in 𝓝[≠] (0 : ℝ), (fisherOriginalTime k u)^2=fisherClockSquare k u := by
  filter_upwards [self_mem_nhdsWithin, fisher_clock_ratio_positive k hk] with u hu hp
  have hu0 : u≠0 := hu
  simp only [fisherOriginalTime, mul_pow, Real.sq_sqrt hp.le]
  field_simp [hu0]

/-- Exact equality of probabilities with the existing amplitude parameter h. -/
theorem fisher_original_time_realizes (k : ℝ) (hk : 0<k) :
    ∀ᶠ u in 𝓝[≠] (0 : ℝ),
      1/3-k*regularParameter (fisherOriginalTime k u)=fisherWeight k u := by
  have hden : ∀ᶠ u in 𝓝[≠] (0 : ℝ), k-1/3+fisherWeight k u≠0 :=
    (fisher_clock_denominator_limit k).eventually_ne (ne_of_gt hk)
  filter_upwards [fisher_original_time_square k hk, hden] with u hs hd
  have hd3 : 3*k-1+3*fisherWeight k u≠0 := by
    intro hz
    apply hd
    linarith
  have hd3' : -1+fisherWeight k u*3+k*3≠0 := by
    intro hz
    apply hd
    linarith
  have hsum : 1+fisherClockSquare k u=k/(k-1/3+fisherWeight k u) := by
    unfold fisherClockSquare
    field_simp [hd, hd3, hd3']
    all_goals ring
  unfold regularParameter
  rw [hs, hsum]
  unfold fisherClockSquare
  field_simp [ne_of_gt hk, hd, hd3, hd3']
  all_goals ring

theorem fisher_original_time_ratio_limit (k : ℝ) (hk : 0<k) :
    Tendsto (fun u : ℝ => fisherOriginalTime k u/u)
      (𝓝[≠] 0) (𝓝 1) := by
  have hh := (fisher_clock_square_quadratic_limit k hk).sqrt
  have he : (fun u : ℝ => fisherOriginalTime k u/u) =ᶠ[𝓝[≠] 0]
      (fun u : ℝ => Real.sqrt (fisherClockSquare k u/u^2)) := by
    filter_upwards [self_mem_nhdsWithin] with u hu
    have hu0 : u≠0 := hu
    unfold fisherOriginalTime
    field_simp [hu0]
  exact (tendsto_congr' he).2 (by simpa only [Real.sqrt_one] using hh)

/-- The cubic coefficient is extracted from the constructed inverse clock. -/
theorem fisher_original_time_cubic_limit (k : ℝ) (hk : 0<k) :
    Tendsto (fun u : ℝ => (fisherOriginalTime k u-u)/u^3)
      (𝓝[≠] 0) (𝓝 (1/2-(3/16 : ℝ)*k)) := by
  have hs := (fisher_clock_square_quadratic_limit k hk).sqrt
  have hd := hs.add_const 1
  have hh := (fisher_clock_square_quartic_limit k hk).div hd
    (by norm_num : Real.sqrt (1 : ℝ)+1≠0)
  have he : (fun u : ℝ => (fisherOriginalTime k u-u)/u^3) =ᶠ[𝓝[≠] 0]
      (fun u : ℝ => ((fisherClockSquare k u-u^2)/u^4)/
        (Real.sqrt (fisherClockSquare k u/u^2)+1)) := by
    filter_upwards [self_mem_nhdsWithin, fisher_clock_ratio_positive k hk] with u hu hp
    have hu0 : u≠0 := hu
    have hroot := Real.sq_sqrt hp.le
    have hden : Real.sqrt (fisherClockSquare k u/u^2)+1≠0 := by positivity
    have hnum :
        (Real.sqrt (fisherClockSquare k u/u^2)-1)*
          (Real.sqrt (fisherClockSquare k u/u^2)+1)=
            fisherClockSquare k u/u^2-1 := by nlinarith
    unfold fisherOriginalTime
    calc
      (u*Real.sqrt (fisherClockSquare k u/u^2)-u)/u^3 =
          (Real.sqrt (fisherClockSquare k u/u^2)-1)/u^2 := by
        field_simp [hu0]
      _ = ((Real.sqrt (fisherClockSquare k u/u^2)-1)*
          (Real.sqrt (fisherClockSquare k u/u^2)+1))/
            (u^2*(Real.sqrt (fisherClockSquare k u/u^2)+1)) := by
        field_simp [hu0, hden]
      _ = (fisherClockSquare k u/u^2-1)/
          (u^2*(Real.sqrt (fisherClockSquare k u/u^2)+1)) := by rw [hnum]
      _ = ((fisherClockSquare k u-u^2)/u^4)/
          (Real.sqrt (fisherClockSquare k u/u^2)+1) := by
        field_simp [hu0, hden]
  have hc : (1-(3/8 : ℝ)*k)/(Real.sqrt 1+1)=1/2-(3/16 : ℝ)*k := by
    rw [Real.sqrt_one]
    ring
  apply (tendsto_congr' he).2
  rw [hc] at hh
  convert hh using 1
  all_goals rfl

theorem fisher_one_twenty_fourth_clock :
    Tendsto (fun u : ℝ => (fisherOriginalTime (1/24) u-u)/u^3)
      (𝓝[≠] 0) (𝓝 (63/128 : ℝ)) := by
  convert fisher_original_time_cubic_limit (1/24) (by norm_num) using 1; norm_num

#print axioms fisherAngularRate
#print axioms fisherSineCoordinate
#print axioms fisherCosineCoordinate
#print axioms fisherAffineWeight
#print axioms fisherAffineTangent
#print axioms fisherWeight
#print axioms fisherWeightTangent
#print axioms fisherLengthPrimitive
#print axioms fisherClockSquare
#print axioms fisherOriginalTime
#print axioms fisher_angular_rate_square
#print axioms fisher_angular_rate_positive
#print axioms fisher_coordinates_normalized
#print axioms fisher_sine_derivative
#print axioms fisher_cosine_derivative
#print axioms fisher_affine_derivative
#print axioms fisher_affine_tangent_derivative
#print axioms fisher_affine_deriv
#print axioms fisher_affine_zero
#print axioms fisher_affine_first_zero
#print axioms fisher_affine_second_zero
#print axioms fisher_affine_contDiff
#print axioms fisher_affine_taylor_two
#print axioms fisher_affine_taylor_limit
#print axioms fisher_weight_derivative
#print axioms fisher_weight_zero
#print axioms fisher_weight_tendsto
#print axioms fisher_weight_positive_near_zero
#print axioms fisher_weight_quartic_limit
#print axioms fisher_weight_fisher
#print axioms fisher_length_derivative
#print axioms fisher_length_speed
#print axioms fisher_length_normalized
#print axioms fisher_weight_quadratic_limit
#print axioms fisher_clock_denominator_limit
#print axioms fisher_clock_square_quadratic_limit
#print axioms fisher_clock_square_quartic_limit
#print axioms fisher_clock_ratio_positive
#print axioms fisher_original_time_zero
#print axioms fisher_original_time_square
#print axioms fisher_original_time_realizes
#print axioms fisher_original_time_ratio_limit
#print axioms fisher_original_time_cubic_limit
#print axioms fisher_one_twenty_fourth_clock

end
end ChatgptAudit.Clock040
