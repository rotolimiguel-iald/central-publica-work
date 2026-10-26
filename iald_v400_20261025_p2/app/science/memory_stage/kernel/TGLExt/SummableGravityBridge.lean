-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_028 (06/09/2026), transposta em 06/09/2026
-- Lote 027..028: EQUIVALENCIA UNITARIA entre os GNS de perfis com afinidade positiva e o TRANSPORTE
--   MODULAR com dominios — Tomita do estado global Phi no Hilbert original (grafo fechado, S, J, Delta,
--   JS = Delta^{1/2} positivo auto-adjunto), grupo modular fortemente continuo que preserva fator e
--   estado, instancia nao trivial (perfil gradual: autovalor transportado 5/7); RESPOSTA GLOBAL finita
--   sem corte (familia de amplitude somavel, fiel), limite conjunto corte/tempo, contraexemplo
--   HARMONICO (entropia relativa finita com incremento modular e entropia DIVERGENTES);
--   einstein_from_summable_area_matching (condicional). Estatuto [REAL / INPUT / OPEN]: a lei de area
--   microscopica NAO foi derivada da torre (controle plano o impede); selecao fisica, H3 dinamico,
--   assinatura e globalizacao seguem INPUT/OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 20/20 + 20/20; manifestos 231/238;
--   2/2 auditores da bancada exit 0; recompilacao INDEPENDENTE 16/16, axiomas no trio; guarda de
--   colisao estatica no ROOT; enunciados lidos. Transposicao MECANICA (cabecalho + prefixo TGLExt.).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.UniformQuadraticResponse

set_option autoImplicit false
set_option maxHeartbeats 6000000
namespace ChatgptAudit.Response028
open Matrix Filter Topology Set TGLExt ChatgptAudit.Micro021 ChatgptAudit.Coherent023
  ChatgptAudit.Flow019 ChatgptAudit.Flow020
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

def amplitudeCoupling (b : SummableAmplitude) : ℝ := Real.log 2*amplitudeMass b/Real.pi

def amplitudeHeatDefect (b : SummableAmplitude) (frequency rate : ℝ) (heat : ℝ → ℝ) (t : ℝ) : ℝ :=
  heat t-rate/(2*Real.pi)*amplitudeModularIncrement b (frequency*t)

def amplitudeAreaDefect (b : SummableAmplitude) (frequency eta : ℝ) (area : ℝ → ℝ) (t : ℝ) : ℝ :=
  amplitudeEntropyIncrement b (frequency*t)-eta*(area t-area 0)

theorem amplitude_coupling_nonnegative (b : SummableAmplitude) : 0 ≤ amplitudeCoupling b :=
  div_nonneg (mul_nonneg (Real.log_pos (by norm_num : (1:ℝ)<2)).le
    (amplitude_mass_nonnegative b)) Real.pi_pos.le

theorem amplitude_response_null_stress (b : SummableAmplitude) (g gInv : Tensor4) (w d : Coordinate4)
    (hn : tensorQuad g d=0) :
    amplitudeResponse b (covectorRead w d)=
      -Real.pi*tensorQuad (covectorStress g gInv w (amplitudeCoupling b)) d := by
  rw [covector_stress_null _ _ _ _ _ hn]
  unfold amplitudeResponse amplitudeCoupling
  field_simp [Real.pi_ne_zero]

theorem amplitude_heat_defect_limit (b : SummableAmplitude) (frequency rate : ℝ)
    (heat : ℝ → ℝ) (coefficient : ℝ)
    (hq : Tendsto (fun t => heat t/t^2) (𝓝[<] 0) (𝓝 coefficient)) :
    Tendsto (fun t => amplitudeHeatDefect b frequency rate heat t/t^2) (𝓝[<] 0)
      (𝓝 (coefficient-rate/(2*Real.pi)*amplitudeResponse b frequency)) := by
  have h := hq.sub ((amplitude_modular_quadratic_limit b frequency).const_mul (rate/(2*Real.pi)))
  have he : (fun t => amplitudeHeatDefect b frequency rate heat t/t^2)=
      (fun t => heat t/t^2-rate/(2*Real.pi)*(amplitudeModularIncrement b (frequency*t)/t^2)) := by
    funext t
    unfold amplitudeHeatDefect
    ring
  rw [he]
  exact h

theorem amplitude_heat_matching
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x d : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x d) (gInv : TensorField4) (w : CovectorField4)
    (b : SummableAmplitude) (rate : ℝ) (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ i j, DifferentiableOn ℝ (fun y => covectorStressField g gInv w (amplitudeCoupling b) y i j) U)
    (hn : tensorQuad (g x) d=0) :
    Tendsto (fun t => amplitudeHeatDefect b (covectorRead (w x) d) rate
      (constructedHeat P (covectorStressField g gInv w (amplitudeCoupling b)) rate hU hg hT) t/t^2)
      (𝓝[<] 0) (𝓝 0) := by
  let T := covectorStressField g gInv w (amplitudeCoupling b)
  have he : amplitudeResponse b (covectorRead (w x) d)= -Real.pi*tensorQuad (T x) d :=
    amplitude_response_null_stress b (g x) (gInv x) (w x) d hn
  have h := amplitude_heat_defect_limit b (covectorRead (w x) d) rate
    (constructedHeat P T rate hU hg hT) (-rate*tensorQuad (T x) d/2)
    (constructed_heat_quadratic_limit P T rate hU hg hT)
  rw [he] at h
  have hz : -rate*tensorQuad (T x) d/2-rate/(2*Real.pi)*(-Real.pi*tensorQuad (T x) d)=0 := by
    field_simp [Real.pi_ne_zero]
    ring
  rwa [hz] at h

theorem amplitude_area_defect_limit
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x d : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x d) (b : SummableAmplitude) (frequency eta : ℝ)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (ht : ∀ i j k, Gamma x i k j=Gamma x j k i) :
    Tendsto (fun t => amplitudeAreaDefect b frequency eta
      (inducedArea g P.curve P.screen.vectors) t/t^2) (𝓝[<] 0)
      (𝓝 (amplitudeResponse b frequency+eta*tensorQuad (coordinateRicci Gamma x) d/2)) := by
  let A := inducedArea g P.curve P.screen.vectors
  have hA0 : A 0=1 := equilibrium_screen_area_initial _ _ _ _ _ P
  have hA : Tendsto (fun t => (A t-A 0)/t^2) (𝓝[<] 0)
      (𝓝 (-tensorQuad (coordinateRicci Gamma x) d/2)) := by
    rw [hA0]
    exact screen_area_quadratic_limit U hU g Gamma hg hG x d P ht
  have h := (amplitude_entropy_quadratic_limit b frequency).sub (hA.const_mul eta)
  have he : (fun t => amplitudeAreaDefect b frequency eta A t/t^2)=
      (fun t => amplitudeEntropyIncrement b (frequency*t)/t^2-eta*((A t-A 0)/t^2)) := by
    funext t
    unfold amplitudeAreaDefect
    ring
  have hc : amplitudeResponse b frequency-eta*(-tensorQuad (coordinateRicci Gamma x) d/2)=
      amplitudeResponse b frequency+eta*tensorQuad (coordinateRicci Gamma x) d/2 := by ring
  rw [hc] at h
  change Tendsto (fun t => amplitudeAreaDefect b frequency eta A t/t^2) _ _
  rw [he]
  exact h

theorem amplitude_area_matching_iff_ricci
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x d : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x d) (gInv : TensorField4) (w : CovectorField4)
    (b : SummableAmplitude) (eta : ℝ) (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hG : SmoothConnectionOn U Gamma) (ht : ∀ i j k, Gamma x i k j=Gamma x j k i)
    (hn : tensorQuad (g x) d=0) :
    Tendsto (fun t => amplitudeAreaDefect b (covectorRead (w x) d) eta
      (inducedArea g P.curve P.screen.vectors) t/t^2) (𝓝[<] 0) (𝓝 0) ↔
      eta*tensorQuad (coordinateRicci Gamma x) d=
        2*Real.pi*tensorQuad (covectorStressField g gInv w (amplitudeCoupling b) x) d := by
  rw [past_zero_limit_iff _ _ (amplitude_area_defect_limit P b (covectorRead (w x) d) eta hU hg hG ht),
    amplitude_response_null_stress b (g x) (gInv x) (w x) d hn]
  change -Real.pi*tensorQuad (covectorStressField g gInv w (amplitudeCoupling b) x) d+
    eta*tensorQuad (coordinateRicci Gamma x) d/2=0 ↔ _
  constructor <;> intro h <;> nlinarith only [h]

theorem amplitude_balance_from_matching (b : SummableAmplitude) (frequency rate eta : ℝ)
    (area heat : ℝ → ℝ)
    (hheat : Tendsto (fun t => amplitudeHeatDefect b frequency rate heat t/t^2) (𝓝[<] 0) (𝓝 0))
    (harea : Tendsto (fun t => amplitudeAreaDefect b frequency eta area t/t^2) (𝓝[<] 0) (𝓝 0)) :
    Tendsto (fun t => horizonBalancePrimitive rate eta area heat t/t^2) (𝓝[<] 0) (𝓝 0) := by
  have h := (hheat.add (harea.const_mul (rate/(2*Real.pi)))).add
    ((amplitude_relative_quadratic_limit b frequency).const_mul (rate/(2*Real.pi)))
  have he : (fun t => horizonBalancePrimitive rate eta area heat t/t^2)=
      (fun t => amplitudeHeatDefect b frequency rate heat t/t^2+
        rate/(2*Real.pi)*(amplitudeAreaDefect b frequency eta area t/t^2)+
        rate/(2*Real.pi)*(amplitudeRelativeEntropy b (frequency*t)/t^2)) := by
    funext t
    unfold horizonBalancePrimitive amplitudeHeatDefect amplitudeAreaDefect amplitudeEntropyIncrement
    ring
  rw [he]
  simpa only [mul_zero,add_zero] using h

theorem einstein_from_summable_area_matching
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (A B : TensorField4) (w : CovectorField4) (b : SummableAmplitude)
    (rate eta : ℝ) (hrate : rate≠0) (heta : eta≠0)
    (hAB : ∀ x∈U, A x*B x=1) (hBA : ∀ x∈U, B x*A x=1)
    (hA : SmoothMatrixOn U A) (hB : SmoothMatrixOn U B) (hw : SmoothVectorOn U w)
    (hclosed : ClosedCovectorOn U w)
    (hwave : CovectorWaveOn U (inverseFrameMetricField B) (frameLeviCivita A B) w)
    (harea : ∀ x (hx : x∈U) d (hd : d≠0) (hn : tensorQuad (frameMetricField A x) d=0),
      let P := localEquilibriumScreen U hU A B hAB hBA hA hB x d hx hd hn
      Tendsto (fun t => amplitudeAreaDefect b (covectorRead (w x) d) eta
        (inducedArea (frameMetricField A) P.curve P.screen.vectors) t/t^2) (𝓝[<] 0) (𝓝 0)) :
    ∃ cosmological : ℝ, ∀ x∈U, frameEinsteinTensor A B x+cosmological • frameMetricField A x=
      (2*Real.pi/eta) • frameCovectorStress A B w (amplitudeCoupling b) x := by
  let T := frameCovectorStress A B w (amplitudeCoupling b)
  have hT : ∀ i j, DifferentiableOn ℝ (fun y => T y i j) U :=
    covector_stress_field_differentiable U _ _ w _ (frame_metric_smooth U A hA)
      (inverse_frame_metric_smooth U B hB) hw
  have hsT : ∀ x∈U, (T x)ᵀ=T x :=
    fun x _ => covector_stress_symmetric _ _ _ _ (frame_metric_symmetric A x)
  apply einstein_from_constructed_clausius U hU A B hAB hBA hA hB T hT rate eta hconn hrate heta hsT
    (frame_covector_stress_conserved U hU A B w _ hAB hBA hA hB hw hclosed hwave)
  intro x hx d hd hn
  let P := localEquilibriumScreen U hU A B hAB hBA hA hB x d hx hd hn
  exact amplitude_balance_from_matching b (covectorRead (w x) d) rate eta
    (inducedArea (frameMetricField A) P.curve P.screen.vectors)
    (constructedHeat P T rate hU (frame_metric_smooth U A hA) hT)
    (amplitude_heat_matching P (inverseFrameMetricField B) w b rate hU (frame_metric_smooth U A hA) hT hn)
    (harea x hx d hd hn)

#print axioms amplitude_coupling_nonnegative
#print axioms amplitude_response_null_stress
#print axioms amplitude_heat_defect_limit
#print axioms amplitude_heat_matching
#print axioms amplitude_area_defect_limit
#print axioms amplitude_area_matching_iff_ricci
#print axioms amplitude_balance_from_matching
#print axioms einstein_from_summable_area_matching
end
end ChatgptAudit.Response028
