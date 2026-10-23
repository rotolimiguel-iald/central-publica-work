-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_041 (06/09/2026), transposta em 06/09/2026
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
import TGLExt.JacobiAreaQuarticLimit
import TGLExt.PlaneWaveEntropyMatching
import Mathlib.Analysis.Calculus.LHopital
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

set_option autoImplicit false
set_option maxHeartbeats 2500000
namespace ChatgptAudit.Heat041
open Filter Set TGLExt ChatgptAudit ChatgptAudit.Optical036
  ChatgptAudit.Quartic037 ChatgptAudit.Wave029 ChatgptAudit.Coherent023
open scoped Topology
noncomputable section

/-- A fourth-order primitive limit from an actual derivative, on both sides of zero. -/
theorem primitive_quartic_limit (flux primitive : ℝ → ℝ) (coefficient : ℝ)
    (hderiv : ∀ᶠ t in 𝓝[≠] (0:ℝ), HasDerivAt primitive (flux t) t)
    (hcontinuous : ContinuousAt primitive 0) (hzero : primitive 0 = 0)
    (hflux : Tendsto (fun t => flux t / t^3) (𝓝[≠] 0) (𝓝 coefficient)) :
    Tendsto (fun t => primitive t / t^4) (𝓝[≠] 0) (𝓝 (coefficient / 4)) := by
  have hg : ∀ᶠ t in 𝓝[≠] (0:ℝ),
      HasDerivAt (fun s : ℝ => s^4) (4*t^3) t :=
    Filter.Eventually.of_forall (fun t => by
      have h := (hasDerivAt_id t).pow 4
      have he : (id ^ 4 : ℝ → ℝ) = (fun s : ℝ => s^4) := by funext s; rfl
      rw [he] at h
      simpa using h)
  have hgn : ∀ᶠ t in 𝓝[≠] (0:ℝ), 4*t^3 ≠ 0 := by
    filter_upwards [self_mem_nhdsWithin] with t ht
    exact mul_ne_zero (by norm_num) (pow_ne_zero _ ht)
  have hfzero : Tendsto primitive (𝓝[≠] 0) (𝓝 0) := by
    simpa only [hzero] using hcontinuous.tendsto.mono_left nhdsWithin_le_nhds
  have hgzero : Tendsto (fun t : ℝ => t^4) (𝓝[≠] 0) (𝓝 0) := by
    simpa using ((continuousAt_id : ContinuousAt (fun t : ℝ => t) 0).pow 4).tendsto.mono_left nhdsWithin_le_nhds
  have hratio : Tendsto (fun t => flux t/(4*t^3)) (𝓝[≠] 0) (𝓝 (coefficient/4)) := by
    simpa only [mul_comm (4:ℝ), div_mul_eq_div_div] using hflux.div_const (4:ℝ)
  exact HasDerivAt.lhopital_zero_nhdsNE hderiv hg hgn hfzero hgzero hratio

theorem geometric_area_continuous (a c : ℝ) : Continuous (geometricJacobiArea a c) := by
  have he : geometricJacobiArea a c = fun t => |opticalJacobiArea a c t| :=
    funext (geometric_jacobi_area_abs a c)
  rw [he]
  exact (optical_jacobi_area_contDiff a c).continuous.abs

/-- Flux evaluated on the actual Jacobi screen. This does not construct EquilibriumScreenData. -/
def opticalHeatFlux (a c rate mass t : ℝ) : ℝ :=
  -rate*t*mass*geometricJacobiArea a c t

theorem optical_heat_flux_geometric (a c rate mass t : ℝ) :
    opticalHeatFlux a c rate mass t =
      -rate*t*tensorQuad (waveMatter a c mass (centralNullCurve t)) centralNullDirection *
        inducedArea (frameMetricField (waveSolder a c)) centralNullCurve
          (geometricJacobiColumns a c) t := by
  rw [wave_matter_quad]
  have hw : covectorRead waveCovector centralNullDirection = 1 :=
    central_direction_frequency
  rw [hw, one_pow, mul_one]
  rfl

theorem optical_heat_flux_continuous (a c rate mass : ℝ) :
    Continuous (opticalHeatFlux a c rate mass) := by
  exact ((continuous_const.mul continuous_id).mul continuous_const).mul
    (geometric_area_continuous a c)

def opticalHeat (a c rate mass t : ℝ) : ℝ :=
  ∫ u in (0:ℝ)..t, opticalHeatFlux a c rate mass u

theorem optical_heat_derivative (a c rate mass t : ℝ) :
    HasDerivAt (opticalHeat a c rate mass) (opticalHeatFlux a c rate mass t) t :=
  ((optical_heat_flux_continuous a c rate mass).integral_hasStrictDerivAt 0 t).hasDerivAt

theorem optical_heat_continuous (a c rate mass : ℝ) :
    Continuous (opticalHeat a c rate mass) :=
  continuous_iff_continuousAt.mpr (fun t =>
    (optical_heat_derivative a c rate mass t).continuousAt)

theorem optical_heat_zero (a c rate mass : ℝ) : opticalHeat a c rate mass 0 = 0 := by
  simp [opticalHeat]

theorem geometric_area_quadratic_limit (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    Tendsto (fun t : ℝ => (geometricJacobiArea a c t-1)/t^2)
      (𝓝[≠] 0) (𝓝 (-(a+c)/2)) := by
  have ht : Tendsto (fun t : ℝ => t^2) (𝓝[≠] 0) (𝓝 0) := by
    simpa using ((continuousAt_id : ContinuousAt (fun t : ℝ => t) 0).pow 2).tendsto.mono_left nhdsWithin_le_nhds
  have h := ((geometric_jacobi_area_quartic_limit a c ha hc).mul ht).sub_const ((a+c)/2)
  have he : (fun t : ℝ => (geometricJacobiArea a c t-1)/t^2) =ᶠ[𝓝[≠] 0]
      (fun t => ((geometricJacobiArea a c t-1+(a+c)*t^2/2)/t^4)*t^2-(a+c)/2) := by
    filter_upwards [self_mem_nhdsWithin] with t ht0
    have hn : t≠0 := ht0
    field_simp [hn]
    ring
  apply (tendsto_congr' he).2
  simpa only [mul_zero,zero_sub,neg_div] using h

theorem optical_corrected_heat_derivative (a c rate mass t : ℝ) :
    HasDerivAt (fun u => opticalHeat a c rate mass u+rate*mass*u^2/2)
      (-rate*mass*t*(geometricJacobiArea a c t-1)) t := by
  have h := (optical_heat_derivative a c rate mass t).add
    ((((hasDerivAt_id t).pow 2).const_mul (rate*mass)).div_const 2)
  have he : opticalHeatFlux a c rate mass t + rate*mass*((2:ℝ)*t^(2-1)*1)/2 =
      -rate*mass*t*(geometricJacobiArea a c t-1) := by
    norm_num [opticalHeatFlux]
    ring
  have hh := h.congr_deriv he
  convert hh using 1 <;> rfl

theorem optical_corrected_flux_cubic_limit (a c rate mass : ℝ)
    (ha : 0≤a) (hc : 0≤c) :
    Tendsto (fun t : ℝ => (-rate*mass*t*(geometricJacobiArea a c t-1))/t^3)
      (𝓝[≠] 0) (𝓝 (rate*mass*(a+c)/2)) := by
  have h := (geometric_area_quadratic_limit a c ha hc).const_mul (-rate*mass)
  have he : (fun t : ℝ => (-rate*mass*t*(geometricJacobiArea a c t-1))/t^3) =ᶠ[𝓝[≠] 0]
      (fun t => (-rate*mass)*((geometricJacobiArea a c t-1)/t^2)) := by
    filter_upwards [self_mem_nhdsWithin] with t ht0
    have hn : t≠0 := ht0
    field_simp [hn]
  have hscalar : -rate*mass*(-(a+c)/2)=rate*mass*(a+c)/2 := by ring
  rw [hscalar] at h
  exact (tendsto_congr' he).2 h

/-- Effective fourth-order coefficient of the integral, without prescribing heat by Clausius. -/
theorem optical_heat_quartic_limit (a c rate mass : ℝ) (ha : 0≤a) (hc : 0≤c) :
    Tendsto (fun t : ℝ => (opticalHeat a c rate mass t+rate*mass*t^2/2)/t^4)
      (𝓝[≠] 0) (𝓝 (rate*mass*(a+c)/8)) := by
  have h := primitive_quartic_limit
    (fun t => -rate*mass*t*(geometricJacobiArea a c t-1))
    (fun t => opticalHeat a c rate mass t+rate*mass*t^2/2)
    (rate*mass*(a+c)/2)
    (Filter.Eventually.of_forall (optical_corrected_heat_derivative a c rate mass))
    ((optical_heat_continuous a c rate mass).continuousAt.add
      ((((continuousAt_id : ContinuousAt (fun t : ℝ => t) 0).pow 2).const_mul
        (rate*mass)).div_const 2))
    (by simp [optical_heat_zero])
    (optical_corrected_flux_cubic_limit a c rate mass ha hc)
  have hscalar : rate*mass*(a+c)/2/4=rate*mass*(a+c)/8 := by ring
  rw [hscalar] at h
  exact h

theorem optical_heat_zero_mass (a c rate t : ℝ) :
    opticalHeat a c rate 0 t = 0 := by
  simp [opticalHeat, opticalHeatFlux]

#print axioms primitive_quartic_limit
#print axioms geometric_area_continuous
#print axioms opticalHeatFlux
#print axioms optical_heat_flux_geometric
#print axioms optical_heat_flux_continuous
#print axioms opticalHeat
#print axioms optical_heat_derivative
#print axioms optical_heat_continuous
#print axioms optical_heat_zero
#print axioms geometric_area_quadratic_limit
#print axioms optical_corrected_heat_derivative
#print axioms optical_corrected_flux_cubic_limit
#print axioms optical_heat_quartic_limit
#print axioms optical_heat_zero_mass
end
end ChatgptAudit.Heat041
