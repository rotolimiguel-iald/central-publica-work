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
import TGLExt.OpticalHeatFlow

set_option autoImplicit false
set_option maxHeartbeats 2500000
namespace ChatgptAudit.Heat041
open Filter Set TGLExt ChatgptAudit ChatgptAudit.Optical036
  ChatgptAudit.Quartic037
open scoped Topology
noncomputable section

/-- Finite heat-area residual for the explicit Jacobi-screen flux integral. -/
def opticalClausiusDefect (a c rate mass eta t : ℝ) : ℝ :=
  opticalHeat a c rate mass t -
    (rate/(2*Real.pi))*eta*(geometricJacobiArea a c t-1)

/-- Quadratic matter-curvature matching is an explicit input, not derived here. -/
theorem optical_clausius_quartic_limit (a c rate mass eta : ℝ)
    (ha : 0≤a) (hc : 0≤c) (hmatch : eta*(a+c)=2*Real.pi*mass) :
    Tendsto (fun t : ℝ => opticalClausiusDefect a c rate mass eta t/t^4)
      (𝓝[≠] 0) (𝓝 (rate*eta*(a^2+c^2)/(24*Real.pi))) := by
  have hm : mass=eta*(a+c)/(2*Real.pi) := by
    apply (eq_div_iff (mul_ne_zero (by norm_num) Real.pi_ne_zero)).2
    nlinarith [hmatch]
  have h := (optical_heat_quartic_limit a c rate mass ha hc).sub
    ((geometric_jacobi_area_quartic_limit a c ha hc).const_mul (rate/(2*Real.pi)*eta))
  have he : (fun t : ℝ => opticalClausiusDefect a c rate mass eta t/t^4) =ᶠ[𝓝[≠] 0]
      (fun t => (opticalHeat a c rate mass t+rate*mass*t^2/2)/t^4 -
        (rate/(2*Real.pi)*eta)*
          ((geometricJacobiArea a c t-1+(a+c)*t^2/2)/t^4)) := by
    filter_upwards [self_mem_nhdsWithin] with t ht
    have hn : t≠0 := ht
    unfold opticalClausiusDefect
    rw [hm]
    field_simp [hn,Real.pi_ne_zero]
    ring
  have hscalar : rate*mass*(a+c)/8 -
      (rate/(2*Real.pi)*eta)*((a^2+6*a*c+c^2)/24) =
      rate*eta*(a^2+c^2)/(24*Real.pi) := by
    rw [hm]
    field_simp [Real.pi_ne_zero]
    ring
  rw [hscalar] at h
  exact (tendsto_congr' he).2 h

/-- The fourth-order defect does not spoil the already established quadratic balance. -/
theorem optical_clausius_quadratic_zero (a c rate mass eta : ℝ)
    (ha : 0≤a) (hc : 0≤c) (hmatch : eta*(a+c)=2*Real.pi*mass) :
    Tendsto (fun t : ℝ => opticalClausiusDefect a c rate mass eta t/t^2)
      (𝓝[≠] 0) (𝓝 0) := by
  have ht : Tendsto (fun t : ℝ => t^2) (𝓝[≠] 0) (𝓝 0) := by
    simpa using ((continuousAt_id : ContinuousAt (fun t : ℝ => t) 0).pow 2).tendsto.mono_left nhdsWithin_le_nhds
  have h := (optical_clausius_quartic_limit a c rate mass eta ha hc hmatch).mul ht
  have he : (fun t : ℝ => opticalClausiusDefect a c rate mass eta t/t^2) =ᶠ[𝓝[≠] 0]
      (fun t => (opticalClausiusDefect a c rate mass eta t/t^4)*t^2) := by
    filter_upwards [self_mem_nhdsWithin] with t ht0
    have hn : t≠0 := ht0
    field_simp [hn]
  apply (tendsto_congr' he).2
  simpa only [mul_zero] using h

theorem optical_clausius_coefficient_positive (a c rate eta : ℝ)
    (hrate : 0<rate) (heta : 0<eta)
    (hcurvature : 0<a+c) :
    0<rate*eta*(a^2+c^2)/(24*Real.pi) := by
  have hs : 0<a^2+c^2 := by
    nlinarith [sq_nonneg a,sq_nonneg c,sq_pos_of_pos hcurvature,sq_nonneg (a-c)]
  exact div_pos (mul_pos (mul_pos hrate heta) hs) (mul_pos (by norm_num) Real.pi_pos)

/-- Exact finite Clausius equality fails locally; this is not a no-go for its infinitesimal form. -/
theorem optical_clausius_not_eventually_exact (a c rate mass eta : ℝ)
    (ha : 0≤a) (hc : 0≤c) (hrate : 0<rate) (heta : 0<eta)
    (hcurvature : 0<a+c) (hmatch : eta*(a+c)=2*Real.pi*mass) :
    ¬ ∀ᶠ t in 𝓝[≠] (0:ℝ),
      opticalHeat a c rate mass t =
        (rate/(2*Real.pi))*eta*(geometricJacobiArea a c t-1) := by
  intro he
  have hz : Tendsto (fun t : ℝ => opticalClausiusDefect a c rate mass eta t/t^4)
      (𝓝[≠] 0) (𝓝 0) := by
    have heq : (fun t : ℝ => opticalClausiusDefect a c rate mass eta t/t^4) =ᶠ[𝓝[≠] 0]
        (fun _ => (0:ℝ)) := by
      filter_upwards [he] with t ht
      simp only [opticalClausiusDefect,ht,sub_self,zero_div]
    exact (tendsto_congr' heq).2 tendsto_const_nhds
  have hh := tendsto_nhds_unique
    (optical_clausius_quartic_limit a c rate mass eta ha hc hmatch) hz
  exact (ne_of_gt (optical_clausius_coefficient_positive a c rate eta hrate heta hcurvature)) hh

theorem optical_clausius_eventually_positive (a c rate mass eta : ℝ)
    (ha : 0≤a) (hc : 0≤c) (hrate : 0<rate) (heta : 0<eta)
    (hcurvature : 0<a+c) (hmatch : eta*(a+c)=2*Real.pi*mass) :
    ∀ᶠ t in 𝓝[≠] (0:ℝ), 0<opticalClausiusDefect a c rate mass eta t := by
  have h := (optical_clausius_quartic_limit a c rate mass eta ha hc hmatch).eventually
    (Ioi_mem_nhds (optical_clausius_coefficient_positive a c rate eta hrate heta hcurvature))
  filter_upwards [h,self_mem_nhdsWithin] with t ht hn
  have hne : t≠0 := hn
  have hp : 0<t^4 := by positivity
  have hm := mul_pos ht hp
  simpa only [div_mul_cancel₀ _ (ne_of_gt hp)] using hm

theorem optical_clausius_rs_quartic_limit (r s rate mass eta : ℝ)
    (hs : |s|<r/2) (hmatch : eta*r=2*Real.pi*mass) :
    Tendsto (fun t : ℝ =>
      opticalClausiusDefect (r/2+s) (r/2-s) rate mass eta t/t^4)
      (𝓝[≠] 0) (𝓝 ((rate*eta/(2*Real.pi))*(r^2/24+s^2/6))) := by
  obtain ⟨ha,hc⟩ := optical_rs_positive_coefficients r s hs
  have hm : eta*(r/2+s+(r/2-s))=2*Real.pi*mass := by
    convert hmatch using 1
    ring
  have h := optical_clausius_quartic_limit (r/2+s) (r/2-s) rate mass eta ha.le hc.le hm
  have hscalar : rate*eta*((r/2+s)^2+(r/2-s)^2)/(24*Real.pi) =
      (rate*eta/(2*Real.pi))*(r^2/24+s^2/6) := by
    field_simp [Real.pi_ne_zero]
    ring
  rw [hscalar] at h
  exact h

theorem isotropic_unit_control :
    Tendsto (fun t : ℝ => opticalClausiusDefect 1 1 1 1 Real.pi t/t^4)
      (𝓝[≠] 0) (𝓝 (1/12:ℝ)) := by
  have h := optical_clausius_quartic_limit 1 1 1 1 Real.pi
    (by norm_num) (by norm_num) (by ring)
  have hscalar : (1:ℝ)*Real.pi*(1^2+1^2)/(24*Real.pi)=1/12 := by
    field_simp [Real.pi_ne_zero]
    ring
  rw [hscalar] at h
  exact h

theorem flat_zero_control (rate eta t : ℝ) :
    opticalClausiusDefect 0 0 rate 0 eta t = 0 := by
  simp [opticalClausiusDefect,optical_heat_zero_mass,geometric_jacobi_area_abs,
    opticalJacobiArea,jacobiOscillator]

theorem flat_matching_forces_zero_mass (eta mass : ℝ)
    (hmatch : eta*((0:ℝ)+0)=2*Real.pi*mass) : mass=0 := by
  have hm : (2*Real.pi)*mass=0 := by simpa using hmatch.symm
  exact (mul_eq_zero.mp hm).resolve_left (mul_ne_zero (by norm_num) Real.pi_ne_zero)

#print axioms opticalClausiusDefect
#print axioms optical_clausius_quartic_limit
#print axioms optical_clausius_quadratic_zero
#print axioms optical_clausius_coefficient_positive
#print axioms optical_clausius_not_eventually_exact
#print axioms optical_clausius_eventually_positive
#print axioms optical_clausius_rs_quartic_limit
#print axioms isotropic_unit_control
#print axioms flat_zero_control
#print axioms flat_matching_forces_zero_mass
end
end ChatgptAudit.Heat041
