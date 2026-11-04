-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_024 (06/09/2026), transposta em 06/09/2026
-- Lote 024..026: a perturbacao de GIBBS realizada no mesmo Hilbert da torre (estado fiel,
--   normalizado, distinto da orbita modular; resposta quadratica; calor/fonte por normalizacao);
--   o LIMITE TERMICO: para perfil constante nao tracial a preparacao NAO tem limite em norma
--   (nao-Cauchy) e o acoplamento da torre e ilimitado; corte com escala escolhida; AFINIDADE:
--   criterio exato (Cauchy <=> afinidade-limite > 0), estado global no Hilbert original, fiel e
--   ciclico; perfil gradual (muda em infinitos sitios, ainda fiel). Estatuto [REAL / INPUT / OPEN]:
--   selecao fisica, area, H3 dinamico, dimensao/assinatura, globalizacao e a classificacao geral
--   dos estados normais (disjuncao) seguem INPUT/OPEN — a bancada NAO promoveu nao-Cauchy a teorema
--   geral de disjuncao nem importou Kakutani.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100%; manifestos 202/206/220;
--   3/3 auditores da bancada exit 0; recompilacao INDEPENDENTE 22/22, axiomas no trio; guarda de
--   colisao estatica no ROOT; enunciados lidos. Transposicao MECANICA (cabecalho + prefixo TGLExt.).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.TowerGibbsPerturbation

set_option autoImplicit false
set_option maxHeartbeats 12000000
namespace ChatgptAudit.Thermal024
open Matrix Filter Topology Set ChatgptAudit.Micro021 ChatgptAudit.Coherent023
  ChatgptAudit.Flow019 ChatgptAudit.Flow020
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section
variable {ι : Type} [Fintype ι]

def gibbsCoupling (p : ι → ℝ) : ℝ := modularVariance p/Real.pi
def gibbsResponse (p : ι → ℝ) (frequency : ℝ) : ℝ := -frequency^2*modularVariance p

theorem gibbs_coupling_nonnegative (p : ι → ℝ) (hp : ∀ i, 0<p i) : 0 ≤ gibbsCoupling p :=
  div_nonneg (modular_variance_nonnegative p hp) (le_of_lt Real.pi_pos)

theorem gibbs_response_null_stress (p : ι → ℝ) (g gInv : Tensor4) (w d : Coordinate4)
    (hn : tensorQuad g d=0) :
    gibbsResponse p (covectorRead w d)= -Real.pi*tensorQuad (covectorStress g gInv w (gibbsCoupling p)) d := by
  rw [covector_stress_null _ _ _ _ _ hn]
  unfold gibbsResponse gibbsCoupling
  field_simp [Real.pi_ne_zero]

variable [Nonempty ι]

theorem gibbs_heat_error_limit (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1)
    (frequency rate : ℝ) (heat : ℝ → ℝ) (coefficient : ℝ)
    (hq : Tendsto (fun t => heat t/t^2) (𝓝[<] 0) (𝓝 coefficient)) :
    Tendsto (fun t => microscopicHeatError (quadraticGibbsCurve p hp hs frequency) rate heat t/t^2)
      (𝓝[<] 0) (𝓝 (coefficient-rate/(2*Real.pi)*gibbsResponse p frequency)) := by
  have hl := hq.sub ((quadratic_gibbs_modular_limit p hp hs frequency).const_mul (rate/(2*Real.pi)))
  have he : (fun t => microscopicHeatError (quadraticGibbsCurve p hp hs frequency) rate heat t/t^2)=
      (fun t => heat t/t^2-rate/(2*Real.pi)*(modularIncrement p (quadraticGibbsWeights p frequency t)/t^2)) := by
    funext t
    unfold microscopicHeatError quadraticGibbsCurve
    ring
  rw [he]
  exact hl

theorem gibbs_heat_matching
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x d : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x d) (gInv : TensorField4) (w : CovectorField4)
    (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1) (rate : ℝ)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ i j, DifferentiableOn ℝ (fun y => covectorStressField g gInv w (gibbsCoupling p) y i j) U)
    (hn : tensorQuad (g x) d=0) :
    Tendsto (fun t => microscopicHeatError (quadraticGibbsCurve p hp hs (covectorRead (w x) d)) rate
      (constructedHeat P (covectorStressField g gInv w (gibbsCoupling p)) rate hU hg hT) t/t^2)
      (𝓝[<] 0) (𝓝 0) := by
  let T := covectorStressField g gInv w (gibbsCoupling p)
  have he : gibbsResponse p (covectorRead (w x) d)= -Real.pi*tensorQuad (T x) d :=
    gibbs_response_null_stress p (g x) (gInv x) (w x) d hn
  have hl := gibbs_heat_error_limit p hp hs (covectorRead (w x) d) rate
    (constructedHeat P T rate hU hg hT) (-rate*tensorQuad (T x) d/2)
    (constructed_heat_quadratic_limit P T rate hU hg hT)
  rw [he] at hl
  have hz : -rate*tensorQuad (T x) d/2-rate/(2*Real.pi)*(-Real.pi*tensorQuad (T x) d)=0 := by
    field_simp [Real.pi_ne_zero]
    ring
  rwa [hz] at hl

theorem gibbs_area_error_limit
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x d : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x d) (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1)
    (frequency eta : ℝ) (hU : IsOpen U) (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (ht : ∀ i j k, Gamma x i k j=Gamma x j k i) :
    Tendsto (fun t => microscopicAreaError (quadraticGibbsCurve p hp hs frequency) eta
      (inducedArea g P.curve P.screen.vectors) t/t^2) (𝓝[<] 0)
      (𝓝 (gibbsResponse p frequency+eta*tensorQuad (coordinateRicci Gamma x) d/2)) := by
  let A := inducedArea g P.curve P.screen.vectors
  have hA0 : A 0=1 := equilibrium_screen_area_initial _ _ _ _ _ P
  have hA : Tendsto (fun t => (A t-A 0)/t^2) (𝓝[<] 0)
      (𝓝 (-tensorQuad (coordinateRicci Gamma x) d/2)) := by
    rw [hA0]
    exact screen_area_quadratic_limit U hU g Gamma hg hG x d P ht
  have hl := (quadratic_gibbs_entropy_limit p hp hs frequency).sub (hA.const_mul eta)
  have he : (fun t => microscopicAreaError (quadraticGibbsCurve p hp hs frequency) eta A t/t^2)=
      (fun t => (finiteEntropy (quadraticGibbsWeights p frequency t)-finiteEntropy p)/t^2-
        eta*((A t-A 0)/t^2)) := by
    funext t
    unfold microscopicAreaError quadraticGibbsCurve
    ring
  have hc : -frequency^2*modularVariance p-eta*(-tensorQuad (coordinateRicci Gamma x) d/2)=
      gibbsResponse p frequency+eta*tensorQuad (coordinateRicci Gamma x) d/2 := by
    unfold gibbsResponse
    ring
  rw [hc] at hl
  change Tendsto (fun t => microscopicAreaError (quadraticGibbsCurve p hp hs frequency) eta A t/t^2) _ _
  rw [he]
  exact hl

theorem gibbs_area_matching_iff_ricci
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x d : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x d) (gInv : TensorField4) (w : CovectorField4)
    (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1) (eta : ℝ)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (ht : ∀ i j k, Gamma x i k j=Gamma x j k i) (hn : tensorQuad (g x) d=0) :
    Tendsto (fun t => microscopicAreaError (quadraticGibbsCurve p hp hs (covectorRead (w x) d)) eta
      (inducedArea g P.curve P.screen.vectors) t/t^2) (𝓝[<] 0) (𝓝 0) ↔
      eta*tensorQuad (coordinateRicci Gamma x) d=
        2*Real.pi*tensorQuad (covectorStressField g gInv w (gibbsCoupling p) x) d := by
  rw [past_zero_limit_iff _ _ (gibbs_area_error_limit P p hp hs (covectorRead (w x) d) eta hU hg hG ht),
    gibbs_response_null_stress p (g x) (gInv x) (w x) d hn]
  change -Real.pi*tensorQuad (covectorStressField g gInv w (gibbsCoupling p) x) d+
    eta*tensorQuad (coordinateRicci Gamma x) d/2=0 ↔ _
  constructor <;> intro hh <;> nlinarith only [hh]

theorem gibbs_matching_produces_clausius
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x d : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x d) (gInv : TensorField4) (w : CovectorField4)
    (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1) (rate eta : ℝ)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ i j, DifferentiableOn ℝ (fun y => covectorStressField g gInv w (gibbsCoupling p) y i j) U)
    (hn : tensorQuad (g x) d=0)
    (harea : Tendsto (fun t => microscopicAreaError (quadraticGibbsCurve p hp hs (covectorRead (w x) d)) eta
      (inducedArea g P.curve P.screen.vectors) t/t^2) (𝓝[<] 0) (𝓝 0)) :
    Tendsto (fun t => horizonBalancePrimitive rate eta (inducedArea g P.curve P.screen.vectors)
      (constructedHeat P (covectorStressField g gInv w (gibbsCoupling p)) rate hU hg hT) t/t^2)
      (𝓝[<] 0) (𝓝 0) := by
  have hh := microscopic_residual_coefficient (quadraticGibbsCurve p hp hs (covectorRead (w x) d))
    hp rate eta (inducedArea g P.curve P.screen.vectors)
    (constructedHeat P (covectorStressField g gInv w (gibbsCoupling p)) rate hU hg hT)
    (gibbs_heat_matching P gInv w p hp hs rate hU hg hT hn) harea
  simpa [quadratic_gibbs_tangent_zero,diagonalFisher] using hh

theorem einstein_from_gibbs_area_matching
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (A B : TensorField4) (w : CovectorField4) (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1)
    (rate eta : ℝ) (hrate : rate≠0) (heta : eta≠0)
    (hAB : ∀ x∈U, A x*B x=1) (hBA : ∀ x∈U, B x*A x=1)
    (hA : SmoothMatrixOn U A) (hB : SmoothMatrixOn U B) (hw : SmoothVectorOn U w)
    (hclosed : ClosedCovectorOn U w)
    (hwave : CovectorWaveOn U (inverseFrameMetricField B) (frameLeviCivita A B) w)
    (harea : ∀ x (hx : x∈U) d (hd : d≠0) (hn : tensorQuad (frameMetricField A x) d=0),
      let P := localEquilibriumScreen U hU A B hAB hBA hA hB x d hx hd hn
      Tendsto (fun t => microscopicAreaError (quadraticGibbsCurve p hp hs (covectorRead (w x) d)) eta
        (inducedArea (frameMetricField A) P.curve P.screen.vectors) t/t^2) (𝓝[<] 0) (𝓝 0)) :
    ∃ cosmological : ℝ, ∀ x∈U, frameEinsteinTensor A B x+cosmological • frameMetricField A x=
      (2*Real.pi/eta) • frameCovectorStress A B w (gibbsCoupling p) x := by
  let T := frameCovectorStress A B w (gibbsCoupling p)
  have hT : ∀ i j, DifferentiableOn ℝ (fun y => T y i j) U :=
    covector_stress_field_differentiable U _ _ w _ (frame_metric_smooth U A hA)
      (inverse_frame_metric_smooth U B hB) hw
  have hsT : ∀ x∈U, (T x)ᵀ=T x :=
    fun x _ => covector_stress_symmetric _ _ _ _ (frame_metric_symmetric A x)
  apply einstein_from_constructed_clausius U hU A B hAB hBA hA hB T hT rate eta hconn hrate heta hsT
    (frame_covector_stress_conserved U hU A B w _ hAB hBA hA hB hw hclosed hwave)
  intro x hx d hd hn
  exact gibbs_matching_produces_clausius
    (localEquilibriumScreen U hU A B hAB hBA hA hB x d hx hd hn)
    (inverseFrameMetricField B) w p hp hs rate eta hU (frame_metric_smooth U A hA)
    hT hn (harea x hx d hd hn)

#print axioms gibbs_coupling_nonnegative
#print axioms gibbs_response_null_stress
#print axioms gibbs_heat_error_limit
#print axioms gibbs_heat_matching
#print axioms gibbs_area_error_limit
#print axioms gibbs_area_matching_iff_ricci
#print axioms gibbs_matching_produces_clausius
#print axioms einstein_from_gibbs_area_matching
end
end ChatgptAudit.Thermal024
