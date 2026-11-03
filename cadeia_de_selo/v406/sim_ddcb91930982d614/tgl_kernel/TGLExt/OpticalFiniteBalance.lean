-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_051 (06-07/09/2026), transposta em 07/09/2026
-- Lote 046..054 (ORDEM_008 cumprida; «tudo o que a bancada podia», 9 entregas, 43 modulos).
--   046: a ESPERANCA APERIODICA — aperiodicExpectationInput P : ExpectationInput P para TODO perfil da torre
--     (media de Cesaro do fluxo modular; limite forte; into/fixes/ortho); o levantamento do Lema 3 dispara para
--     todo perfil e todo horizonte (the_lift_fires_on_the_aperiodic_tower); unicidade; E comuta com sigma_t.
--   047: propriedades da esperanca — linear sobre M, preserva 1/estado/adjunto, bimodular sobre o centralizador,
--     COMPLETAMENTE POSITIVA (CompletelyPositiveMap da mathlib), contracao GNS, NORMAL (supremos positivos dirigidos).
--   048: obstrucoes da identificacao modular/geometrica — Borchers trivial sobrevive ao transporte de estado (027);
--     periodo do fluxo forca retorno de rotulos em localizacao fiel covariante; ligado ao boost 044 (negativos tipados).
--   049-050: SUBESPACO PADRAO CONTINUO em L^2 — T_c = M_exp(-c xi) positivo auto-adjunto (grafo limitado), J
--     antiunitaria, S_c = J T_c involucao fechada, K_c = Fix S_c subespaco padrao; adjunto S_c^dagger = T_c J,
--     Delta_c = S_c^dagger S_c = T_c^2 = T_{2c} com igualdade de dominios, resolvente (I + Delta_c)^{-1}.
--     Identificacao T_c = Delta_c^{1/2} e BW seguem OPEN.
--   051: balanco optico finito — Q - K DeltaA = K E com E >= 0 (integral optica), E/t^4 -> (a^2 + c^2)/12; Riccati;
--     no caso variavel o drift Z_R(s) - s R(s) persiste (controles).
--   052: setor horizontal (plano de Pauli X,Y do 1o sitio) — a esperanca centralizante zera as duas direcoes;
--     o horizonte modular faz o quarto de volta; forma invariante = c x produto GNS real; [INPUT] traco relativo = 1
--     fixa c = 1/2 (densidade de area 1/2); forma efetiva de densidade |2p - 1|. Escala livre sem calibracao por Omega.
--   053: polarizador D = P_R(-i)P_R no Hilbert real; acao GNS de todo TowerHorizon preserva Omega e entrelaca D;
--     radical = centralizador (setor auto-adjunto); CONTRAEXEMPLO: covariancia + calibracao comum NAO da unicidade
--     da area (9/10 vs 1377/1250 no 2o par).
--   054: custo modular do polarizador C_D(x) = sum 2||D^(n+1)x||^2/(2n+1): l.s.c., preservado por todo TowerHorizon,
--     custo zero <=> centralizador; f(0)=0, f(0)=2 localModularCost; C_D(X_1 Omega) = log2/3 na referencia p = 1/3.
--   Estatuto: [REAL] o que esta compilado; [INPUT] calibracao por Omega, traco relativo = 1; [OPEN] H3, selecao
--   fisica da area, escala dimensional, regiao <-> algebra, BW/identificacao T_c = Delta^{1/2}, reconstrucao geral.
-- Auditoria da gerencia (sessao d554e796, 07/09/2026): hashes 185/185 (9 entregas); 9/9 auditores exit 0;
--   recompilacao INDEPENDENTE 43/43, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.OpticalVolterraBalance
import TGLExt.JacobiRiccatiProfile
import TGLExt.OpticalHeatClausius
import TGLExt.OpticalConstructedHeat
import Mathlib.Analysis.Calculus.Deriv.Abs

set_option autoImplicit false
set_option maxHeartbeats 2500000

namespace ChatgptAudit.Optical051
open Filter Set ChatgptAudit.Optical036 ChatgptAudit.Optical043 ChatgptAudit.Heat041
open scoped Topology
noncomputable section

/-- Expansion of the two existing logarithmic Jacobi rates. -/
def opticalExpansion (a c t : ℝ) : ℝ :=
  jacobiLogDerivative a t + jacobiLogDerivative c t

/-- The quadratic optical distortion, defined without any heat or balance term. -/
def opticalDistortionSquared (a c t : ℝ) : ℝ :=
  (jacobiLogDerivative a t)^2 + (jacobiLogDerivative c t)^2

/-- A Volterra integral built solely from the geometric Jacobi area and optical rates. -/
def opticalAccumulatedCorrection (a c : ℝ) : ℝ → ℝ :=
  opticalVolterraCorrection (geometricJacobiArea a c) (opticalDistortionSquared a c)

theorem optical_distortion_nonneg (a c t : ℝ) : 0 ≤ opticalDistortionSquared a c t :=
  add_nonneg (sq_nonneg _) (sq_nonneg _)

theorem optical_expansion_zero (a c : ℝ) : opticalExpansion a c 0 = 0 := by
  simp only [opticalExpansion, jacobi_log_derivative_zero, add_zero]

theorem optical_expansion_derivative (a c : ℝ) (ha : 0≤a) (hc : 0≤c) (t : ℝ)
    (hna : jacobiOscillator a t≠0) (hnc : jacobiOscillator c t≠0) :
    HasDerivAt (opticalExpansion a c)
      (-(a+c)-opticalDistortionSquared a c t) t := by
  have h := (jacobi_log_derivative_hasDerivAt a ha t hna).add
    (jacobi_log_derivative_hasDerivAt c hc t hnc)
  apply h.congr_deriv
  dsimp [opticalDistortionSquared]
  ring

theorem optical_distortion_continuousOn (a c : ℝ) (I : Set ℝ)
    (hn : ∀ t∈I, jacobiOscillator a t≠0 ∧ jacobiOscillator c t≠0) :
    ContinuousOn (opticalDistortionSquared a c) I := by
  intro t ht
  have hA := (jacobi_log_derivative_contDiffAt a t (hn t ht).1).continuousAt
  have hC := (jacobi_log_derivative_contDiffAt c t (hn t ht).2).continuousAt
  exact ((hA.pow 2).add (hC.pow 2)).continuousWithinAt

theorem optical_area_positive (a c t : ℝ)
    (hna : jacobiOscillator a t≠0) (hnc : jacobiOscillator c t≠0) :
    0 < geometricJacobiArea a c t := by
  rw [geometric_jacobi_area_abs, abs_pos]
  exact mul_ne_zero hna hnc

/-- The area derivative is valid for either sign of the oriented Jacobi product. -/
theorem optical_area_derivative (a c t : ℝ)
    (hna : jacobiOscillator a t≠0) (hnc : jacobiOscillator c t≠0) :
    HasDerivAt (geometricJacobiArea a c)
      (geometricJacobiArea a c t * opticalExpansion a c t) t := by
  have hprod : HasDerivAt (opticalJacobiArea a c)
      (opticalJacobiArea a c t * opticalExpansion a c t) t := by
    have h := (jacobi_oscillator_hasDerivAt a t).mul
      (jacobi_oscillator_hasDerivAt c t)
    apply h.congr_deriv
    change jacobiOscillatorVelocity a t * jacobiOscillator c t +
      jacobiOscillator a t * jacobiOscillatorVelocity c t =
      (jacobiOscillator a t * jacobiOscillator c t) *
        (jacobiLogDerivative a t + jacobiLogDerivative c t)
    rw [← jacobi_log_derivative_mul a t hna, ← jacobi_log_derivative_mul c t hnc]
    ring
  have hn : opticalJacobiArea a c t≠0 := mul_ne_zero hna hnc
  rw [show geometricJacobiArea a c = (fun s => |opticalJacobiArea a c s|) from
    funext (geometric_jacobi_area_abs a c)]
  rcases hn.lt_or_gt with hneg | hpos
  · have h := (hasDerivAt_abs_neg hneg).comp t hprod
    apply h.congr_deriv
    change (-1) * (opticalJacobiArea a c t * opticalExpansion a c t) =
      |opticalJacobiArea a c t| * opticalExpansion a c t
    rw [abs_of_neg hneg]
    ring
  · have h := (hasDerivAt_abs_pos hpos).comp t hprod
    apply h.congr_deriv
    change (1:ℝ) * (opticalJacobiArea a c t * opticalExpansion a c t) =
      |opticalJacobiArea a c t| * opticalExpansion a c t
    rw [abs_of_pos hpos]
    ring

/-- Exact finite identity on a connected interval before any oscillator zero.
The matter-curvature matching is an explicit hypothesis. -/
theorem optical_finite_balance (I : Set ℝ) (ho : IsOpen I)
    (hI : Convex ℝ I) (h0 : (0:ℝ)∈I)
    (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (hn : ∀ t∈I, jacobiOscillator a t≠0 ∧ jacobiOscillator c t≠0)
    (rate mass eta : ℝ) (hmatch : eta*(a+c)=2*Real.pi*mass)
    (t : ℝ) (ht : t∈I) :
    opticalClausiusDefect a c rate mass eta t =
      (rate/(2*Real.pi)*eta)*opticalAccumulatedCorrection a c t := by
  have hk : (rate/(2*Real.pi)*eta)*(a+c)=rate*mass := by
    calc
      _ = rate*(eta*(a+c))/(2*Real.pi) := by ring
      _ = rate*(2*Real.pi*mass)/(2*Real.pi) := by rw [hmatch]
      _ = rate*mass := by field_simp [Real.pi_ne_zero]
  have hQ : ∀ s∈I, HasDerivAt (opticalHeat a c rate mass)
      (-(rate/(2*Real.pi)*eta)*s*(a+c)*geometricJacobiArea a c s) s := by
    intro s _
    apply (optical_heat_derivative a c rate mass s).congr_deriv
    unfold opticalHeatFlux
    calc
      _ = -((rate/(2*Real.pi)*eta)*(a+c))*s*geometricJacobiArea a c s := by
        rw [hk]
        ring
      _ = _ := by ring
  have h := optical_volterra_balance_constant I ho hI h0
    (geometricJacobiArea a c) (opticalExpansion a c)
    (opticalDistortionSquared a c) (opticalHeat a c rate mass)
    (rate/(2*Real.pi)*eta) (a+c)
    (optical_distortion_continuousOn a c I hn)
    (fun s hs => optical_area_derivative a c s (hn s hs).1 (hn s hs).2)
    (fun s hs => optical_expansion_derivative a c ha hc s (hn s hs).1 (hn s hs).2)
    (optical_expansion_zero a c) hQ (optical_heat_zero a c rate mass) t ht
  simpa only [opticalClausiusDefect, geometric_jacobi_area_zero,
    opticalAccumulatedCorrection] using h

/-- Both orientations of the nested integral give a nonnegative optical correction. -/
theorem optical_correction_nonneg (I : Set ℝ) (hI : Convex ℝ I)
    (h0 : (0:ℝ)∈I) (a c t : ℝ) (ht : t∈I) :
    0 ≤ opticalAccumulatedCorrection a c t := by
  apply optical_volterra_correction_nonneg I hI h0
    (geometricJacobiArea a c) (opticalDistortionSquared a c)
    (fun s _ => ?_) (fun s _ => optical_distortion_nonneg a c s) t ht
  rw [geometric_jacobi_area_abs]
  exact abs_nonneg _

/-- The finite identity holds on an actual neighbourhood, obtained from nonvanishing. -/
theorem optical_finite_balance_near_zero (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (rate mass eta : ℝ) (hmatch : eta*(a+c)=2*Real.pi*mass) :
    opticalClausiusDefect a c rate mass eta =ᶠ[𝓝 (0:ℝ)]
      (fun t => (rate/(2*Real.pi)*eta)*opticalAccumulatedCorrection a c t) := by
  have hn : ∀ᶠ t in 𝓝 (0:ℝ),
      jacobiOscillator a t≠0 ∧ jacobiOscillator c t≠0 := by
    filter_upwards [optical_congruence_domain_eventually a c] with t ht
    exact (optical_congruence_domain_central_iff a c t).mp ht
  obtain ⟨eps,heps,hsub⟩ := Metric.mem_nhds_iff.mp hn
  have h0 : (0:ℝ)∈Metric.ball (0:ℝ) eps := by
    simpa only [Metric.mem_ball, dist_self] using heps
  filter_upwards [Metric.ball_mem_nhds (0:ℝ) heps] with t ht
  exact optical_finite_balance (Metric.ball (0:ℝ) eps) Metric.isOpen_ball
    (convex_ball (0:ℝ) eps) h0 a c ha hc (fun s hs => hsub hs)
    rate mass eta hmatch t ht

/-- Only the already proved past germ is asserted for constructedHeat043. -/
theorem constructed_heat_finite_balance_germ (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (rate mass eta : ℝ) (hmatch : eta*(a+c)=2*Real.pi*mass) :
    opticalScreenClausiusDefect a c ha hc rate mass eta =ᶠ[𝓝[<] (0:ℝ)]
      (fun t => (rate/(2*Real.pi)*eta)*opticalAccumulatedCorrection a c t) :=
  (optical_screen_clausius_germ a c ha hc rate mass eta).trans
    ((optical_finite_balance_near_zero a c ha hc rate mass eta hmatch).filter_mono
      nhdsWithin_le_nhds)

/-- The fourth-order coefficient follows from the exact identity and the existing041 limit. -/
theorem optical_correction_quartic_limit (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    Tendsto (fun t : ℝ => opticalAccumulatedCorrection a c t/t^4)
      (𝓝[≠] (0:ℝ)) (𝓝 ((a^2+c^2)/12)) := by
  have hm : (1:ℝ)*(a+c)=2*Real.pi*((a+c)/(2*Real.pi)) := by
    field_simp [Real.pi_ne_zero]
  have h := optical_clausius_quartic_limit a c (2*Real.pi)
    ((a+c)/(2*Real.pi)) 1 ha hc hm
  have hfactor : ((2*Real.pi)/(2*Real.pi))*1=(1:ℝ) := by
    field_simp [Real.pi_ne_zero]
  have hcoeff : (2*Real.pi)*1*(a^2+c^2)/(24*Real.pi)=(a^2+c^2)/12 := by
    field_simp [Real.pi_ne_zero]; ring
  rw [hcoeff] at h
  have he : (fun t : ℝ => opticalAccumulatedCorrection a c t/t^4) =ᶠ[𝓝[≠] (0:ℝ)]
      (fun t => opticalClausiusDefect a c (2*Real.pi) ((a+c)/(2*Real.pi)) 1 t/t^4) := by
    filter_upwards [(optical_finite_balance_near_zero a c ha hc (2*Real.pi)
      ((a+c)/(2*Real.pi)) 1 hm).filter_mono
        (show 𝓝[≠] (0:ℝ) ≤ 𝓝 (0:ℝ) from nhdsWithin_le_nhds)] with t ht
    rw [hfactor, one_mul] at ht
    rw [← ht]
  exact (tendsto_congr' he).2 h

#print axioms opticalExpansion
#print axioms opticalDistortionSquared
#print axioms opticalAccumulatedCorrection
#print axioms optical_distortion_nonneg
#print axioms optical_expansion_zero
#print axioms optical_expansion_derivative
#print axioms optical_distortion_continuousOn
#print axioms optical_area_positive
#print axioms optical_area_derivative
#print axioms optical_finite_balance
#print axioms optical_correction_nonneg
#print axioms optical_finite_balance_near_zero
#print axioms constructed_heat_finite_balance_germ
#print axioms optical_correction_quartic_limit

end
end ChatgptAudit.Optical051
