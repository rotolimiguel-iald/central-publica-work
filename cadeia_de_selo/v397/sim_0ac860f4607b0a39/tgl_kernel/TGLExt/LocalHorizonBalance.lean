-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_010 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.CoordinateRaychaudhuri
import Mathlib.Analysis.Calculus.Deriv.Slope
import Mathlib.Analysis.Calculus.LHopital

set_option autoImplicit false
set_option maxHeartbeats 3000000
namespace ChatgptAudit
open Matrix Filter Topology
open scoped ContDiff
noncomputable section

def horizonFluxResidual (rate eta : ℝ) (theta area matter : ℝ → ℝ) (t : ℝ) : ℝ :=
  -rate*t*matter t*area t-(rate/(2*Real.pi))*eta*theta t*area t

def LocalClausiusPast (rate eta : ℝ) (theta area matter : ℝ → ℝ) : Prop :=
  Tendsto (fun t => horizonFluxResidual rate eta theta area matter t/t) (𝓝[<] 0) (𝓝 0)

theorem curve_expansion_focusing (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V)
    (ha : Set.EqOn (vectorAcceleration Gamma V) (fun _ => 0) U)
    (x : Coordinate4) (hx : x∈U) (ht : ∀ i j a, Gamma x i a j=Gamma x j a i)
    (hB : covariantVectorGradient Gamma V x=0)
    (curve : ℝ → Coordinate4) (hc : curve 0=x) (hv : HasDerivAt curve (V x) 0) :
    HasDerivAt (fun t => vectorExpansion Gamma V (curve t))
      (-tensorQuad (coordinateRicci Gamma x) (V x)) 0 := by
  have hs : ContDiffOn ℝ ∞ (vectorExpansion Gamma V) U := by
    have hBsm := covariantVectorGradient_smooth U hU Gamma V hG hV
    unfold SmoothMatrixOn at hBsm
    unfold vectorExpansion Matrix.trace Matrix.diag
    fun_prop
  have hd : DifferentiableAt ℝ (vectorExpansion Gamma V) x :=
    (hs.differentiableOn (by simp)).differentiableAt (hU.mem_nhds hx)
  have hcomp := hd.hasFDerivAt.comp_hasDerivAt_of_eq 0 hv hc.symm
  have he := equilibrium_ricci_focusing U hU Gamma V hG hV ha x hx ht hB
  rw [scalarAlong_eq_fderiv] at he
  simpa only [Function.comp_def,he] using hcomp

theorem horizon_flux_residual_limit (rate eta thetaPrime : ℝ) (theta area matter : ℝ → ℝ)
    (htheta : HasDerivAt theta thetaPrime 0) (htheta0 : theta 0=0)
    (harea : ContinuousAt area 0) (hmatter : ContinuousAt matter 0) :
    Tendsto (fun t => horizonFluxResidual rate eta theta area matter t/t) (𝓝[<] 0)
      (𝓝 (-rate*matter 0*area 0-(rate/(2*Real.pi))*eta*thetaPrime*area 0)) := by
  have hs : Tendsto (fun t => theta t/t) (𝓝[<] 0) (𝓝 thetaPrime) := by
    simpa only [zero_add,htheta0,sub_zero,smul_eq_mul,div_eq_mul_inv,mul_comm]
      using htheta.tendsto_slope_zero_left
  have hA : Tendsto area (𝓝[<] 0) (𝓝 (area 0)) := harea.tendsto.mono_left nhdsWithin_le_nhds
  have hM : Tendsto matter (𝓝[<] 0) (𝓝 (matter 0)) := hmatter.tendsto.mono_left nhdsWithin_le_nhds
  have hl : Tendsto (fun t => -rate*matter t*area t-((rate/(2*Real.pi))*eta)*(theta t/t)*area t)
      (𝓝[<] 0) (𝓝 (-rate*matter 0*area 0-(rate/(2*Real.pi))*eta*thetaPrime*area 0)) :=
    ((tendsto_const_nhds.mul hM).mul hA).sub ((tendsto_const_nhds.mul hs).mul hA)
  have he : (fun t => horizonFluxResidual rate eta theta area matter t/t) =ᶠ[𝓝[<] (0:ℝ)]
      (fun t => -rate*matter t*area t-((rate/(2*Real.pi))*eta)*(theta t/t)*area t) := by
    filter_upwards [self_mem_nhdsWithin] with t ht
    have hn : t≠0 := ne_of_lt ht
    unfold horizonFluxResidual
    field_simp [hn]
  exact hl.congr' he.symm

theorem local_clausius_forces_ricci (rate eta ricci : ℝ) (theta area matter : ℝ → ℝ)
    (hrate : rate≠0) (heta : eta≠0) (hA0 : area 0≠0)
    (htheta : HasDerivAt theta (-ricci) 0) (htheta0 : theta 0=0)
    (harea : ContinuousAt area 0) (hmatter : ContinuousAt matter 0)
    (hbalance : LocalClausiusPast rate eta theta area matter) :
    ricci=(2*Real.pi/eta)*matter 0 := by
  have he := tendsto_nhds_unique
    (horizon_flux_residual_limit rate eta (-ricci) theta area matter htheta htheta0 harea hmatter)
    hbalance
  have hp : rate*area 0*(eta*ricci-2*Real.pi*matter 0)=0 := by
    field_simp [Real.pi_ne_zero] at he
    nlinarith only [he]
  have hz : eta*ricci-2*Real.pi*matter 0=0 :=
    (mul_eq_zero.mp hp).resolve_left (mul_ne_zero hrate hA0)
  rw [div_mul_eq_mul_div]
  apply (eq_div_iff heta).mpr
  nlinarith only [hz]

theorem primitive_quadratic_limit (flux primitive : ℝ → ℝ) (coefficient : ℝ)
    (hderiv : ∀ᶠ t in 𝓝[<] (0:ℝ), HasDerivAt primitive (flux t) t)
    (hcontinuous : ContinuousAt primitive 0) (hzero : primitive 0=0)
    (hflux : Tendsto (fun t => flux t/t) (𝓝[<] 0) (𝓝 coefficient)) :
    Tendsto (fun t => primitive t/t^2) (𝓝[<] 0) (𝓝 (coefficient/2)) := by
  have hg : ∀ᶠ t in 𝓝[<] (0:ℝ), HasDerivAt (fun s : ℝ => s^2) (2*t) t := by
    filter_upwards [] with t
    have hd := (hasDerivAt_id t).pow 2
    have he : (id ^ 2 : ℝ → ℝ)=(fun s : ℝ => s^2) := by
      funext s
      rfl
    rw [he] at hd
    simpa using hd
  have hgn : ∀ᶠ t in 𝓝[<] (0:ℝ), 2*t≠0 := by
    filter_upwards [self_mem_nhdsWithin] with t ht
    exact mul_ne_zero (by norm_num) (ne_of_lt ht)
  have hfzero : Tendsto primitive (𝓝[<] 0) (𝓝 0) := by
    simpa only [hzero] using hcontinuous.tendsto.mono_left nhdsWithin_le_nhds
  have hgzero : Tendsto (fun t : ℝ => t^2) (𝓝[<] 0) (𝓝 0) := by
    simpa using ((continuousAt_id : ContinuousAt (fun t : ℝ => t) 0).pow 2).tendsto.mono_left nhdsWithin_le_nhds
  have hratio : Tendsto (fun t => flux t/(2*t)) (𝓝[<] 0) (𝓝 (coefficient/2)) := by
    simpa only [mul_comm (2:ℝ),div_mul_eq_div_div] using hflux.div_const (2:ℝ)
  exact HasDerivAt.lhopital_zero_nhdsLT hderiv hg hgn hfzero hgzero hratio

theorem integrated_clausius_implies_local (rate eta thetaPrime : ℝ) (theta area matter primitive : ℝ → ℝ)
    (htheta : HasDerivAt theta thetaPrime 0) (htheta0 : theta 0=0)
    (harea : ContinuousAt area 0) (hmatter : ContinuousAt matter 0)
    (hderiv : ∀ᶠ t in 𝓝[<] (0:ℝ), HasDerivAt primitive (horizonFluxResidual rate eta theta area matter t) t)
    (hcontinuous : ContinuousAt primitive 0) (hzero : primitive 0=0)
    (hbalance : Tendsto (fun t => primitive t/t^2) (𝓝[<] 0) (𝓝 0)) :
    LocalClausiusPast rate eta theta area matter := by
  have hl := horizon_flux_residual_limit rate eta thetaPrime theta area matter htheta htheta0 harea hmatter
  have hi := primitive_quadratic_limit _ primitive _ hderiv hcontinuous hzero hl
  have he := tendsto_nhds_unique hi hbalance
  have hz : -rate*matter 0*area 0-(rate/(2*Real.pi))*eta*thetaPrime*area 0=0 := by
    linarith
  unfold LocalClausiusPast
  simpa only [hz] using hl


def horizonBalancePrimitive (rate eta : ℝ) (area heat : ℝ → ℝ) (t : ℝ) : ℝ :=
  heat t-((rate/(2*Real.pi))*eta)*(area t-area 0)

theorem horizon_primitive_flux (rate eta t : ℝ) (theta area matter heat : ℝ → ℝ)
    (harea : HasDerivAt area (theta t*area t) t)
    (hheat : HasDerivAt heat (-rate*t*matter t*area t) t) :
    HasDerivAt (horizonBalancePrimitive rate eta area heat)
      (horizonFluxResidual rate eta theta area matter t) t := by
  have hd := hheat.sub ((harea.sub_const (area 0)).const_mul ((rate/(2*Real.pi))*eta))
  have hf : (heat-(fun y => ((rate/(2*Real.pi))*eta)*(area y-area 0)))=
      horizonBalancePrimitive rate eta area heat := by
    funext y
    rfl
  rw [hf] at hd
  have he : horizonFluxResidual rate eta theta area matter t=
      -rate*t*matter t*area t-((rate/(2*Real.pi))*eta)*(theta t*area t) := by
    unfold horizonFluxResidual
    ring
  rw [he]
  exact hd

theorem horizon_primitive_zero (rate eta : ℝ) (area heat : ℝ → ℝ) (hheat : heat 0=0) :
    horizonBalancePrimitive rate eta area heat 0=0 := by
  simp [horizonBalancePrimitive,hheat]

theorem heat_area_clausius_implies_local (rate eta thetaPrime : ℝ) (theta area matter heat : ℝ → ℝ)
    (htheta : HasDerivAt theta thetaPrime 0) (htheta0 : theta 0=0)
    (harea : ContinuousAt area 0) (hmatter : ContinuousAt matter 0)
    (hheat : ContinuousAt heat 0) (hheat0 : heat 0=0)
    (harea_rate : ∀ᶠ t in 𝓝[<] (0:ℝ), HasDerivAt area (theta t*area t) t)
    (hheat_rate : ∀ᶠ t in 𝓝[<] (0:ℝ), HasDerivAt heat (-rate*t*matter t*area t) t)
    (hbalance : Tendsto (fun t => horizonBalancePrimitive rate eta area heat t/t^2)
      (𝓝[<] 0) (𝓝 0)) :
    LocalClausiusPast rate eta theta area matter := by
  apply integrated_clausius_implies_local rate eta thetaPrime theta area matter
    (horizonBalancePrimitive rate eta area heat) htheta htheta0 harea hmatter
  · filter_upwards [harea_rate,hheat_rate] with t hAt hQt
    exact horizon_primitive_flux rate eta t theta area matter heat hAt hQt
  · exact hheat.sub ((harea.sub continuousAt_const).const_mul ((rate/(2*Real.pi))*eta))
  · exact horizon_primitive_zero rate eta area heat hheat0
  · exact hbalance

#print axioms horizon_primitive_flux
#print axioms horizon_primitive_zero
#print axioms heat_area_clausius_implies_local

#print axioms curve_expansion_focusing
#print axioms horizon_flux_residual_limit
#print axioms local_clausius_forces_ricci
#print axioms primitive_quadratic_limit
#print axioms integrated_clausius_implies_local
end
end ChatgptAudit
