-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — LOTE 058..062 (09/09/2026), transposta em 10/09/2026 (ENTREGA_062 = elo do lote)
-- Os 77 modulos da sessao de 09/09 da bancada (cadeia de copias integradas 63 -> 72 -> 77 sobre a base v337 lida),
--   1065 teoremas declarados pela bancada. Cinco entregas espontaneas:
--   058: ATLAS GRAVITACIONAL SELECIONADO — continuidade + amostras densas + cortes racionais determinam o registro em U;
--     a leitura geometricLogReading caracteriza a sequencia booleana; a selecao por classe instancia IALDState e os
--     teoremas do Nome; o decodificador devolve classe, g, T e os pesos; Einstein do registro decodificado decorre das
--     leis de area e conservacao do registro original (jets, Levi-Civita, Ricci, Einstein preservados).
--   059: caracter completo reconstroi g/T/Einstein condicionado a area e conservacao; COLAGEM da Lambda unico nas
--     cartas compativeis; naturalidade infinitesimal de Ricci/escalar/Einstein em carta curva; potencial XX somavel
--     auto-adjunto com cauda em norma; exemplo de acoplamento atestado.
--   060: COCICLO UNITARIO INFINITO do potencial XX somavel na acao modular canonica; controle uniforme dos cortes;
--     gerador iV e ODE; grupo beta_t = Ad_u(t) o alpha_t que preserva o fator; transformacao finita de
--     Levi-Civita/Ricci/escalar/Einstein e lei de transformacao de Einstein nas sobreposicoes metricas abertas.
--   061: interacao local somavel com termos NAO comutativos (testemunha explicita); unicidade potencial <-> cociclo;
--     fase central Z^{-it} (gerador i(V - logZ I)); colagem suave selecionada -> Lambda global unico; estado perturbado
--     de Araki [DERIVED + KNOWN, analitico — NAO Lean].
--   062: seletor canonico e Born; reconstrucao do registro pelo seletor; entrelacamento angular; caracter da fase
--     relativa (duas probabilidades de interferencia recuperam a fase); estimativas de localidade de vinculo.
--   Estatuto: [REAL] o compilado; [DERIVED + KNOWN] Araki; [INPUT] R (o registro) e a origem fisica; [OPEN]
--   correspondencia fisica seletor-registro, materia/conservacao/area para os mesmos dados, atlas fisico compativel,
--   alem da classe globalmente limitada, anomalias e UV. Nenhum nome ligado a H3, area fisica ou gate.
-- Auditoria da gerencia (sessao d554e796, 10/09/2026): lote montado da CADEIA de recibos (INTEGRATION_RESULT 77 -> 72
--   -> 63); 77/77 hashes lidos dos bytes contra os recibos; zero proibidos; guarda de colisao; recompilacao INDEPENDENTE
--   77/77 contra o kernel v337, axiomas no trio; a copia integrada da bancada NAO foi usada (so as fontes congeladas).
--   Transposicao: cabecalho + prefixo TGLExt. nos imports locais (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.GeneralMetricClausius
import TGLExt.FiniteCoherentSources
import TGLExt.JointUnitaryPreparation

set_option autoImplicit false
set_option maxHeartbeats 300000
namespace ChatgptAudit.JointGravitation
open Matrix Filter Topology Set TGLExt ChatgptAudit.GeneralMetric
  ChatgptAudit.GeneralClausius ChatgptAudit.FiniteCoherentSource ChatgptAudit.JointUnitary
  ChatgptAudit.Coherent023 ChatgptAudit.Unitary022 ChatgptAudit.Micro021
  ChatgptAudit.Flow019 ChatgptAudit.Flow020
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section
variable {ι : Type} [Fintype ι]

def jointMatter (C : UnitaryLabelData ι) (g : TensorField4) (w : ι → CovectorField4) :
    TensorField4 :=
  finiteCoherentStressField g (metricInverse g) w C.weight C.axisA C.axisB C.initialU C.initialV

def jointPreparation (C : UnitaryLabelData ι) (w : ι → CovectorField4)
    (x direction : Coordinate4) : DiagonalStateCurve (jointBase C) :=
  jointCovectorCurve C (fun j => w j x) direction

theorem joint_matter_smooth (U : Set Coordinate4) (C : UnitaryLabelData ι)
    (g : TensorField4) (w : ι → CovectorField4)
    (hg : SmoothMatrixOn U g) (hLor : ∀ x ∈ U, LorentzByCongruence (g x))
    (hw : ∀ j, SmoothVectorOn U (w j)) : SmoothMatrixOn U (jointMatter C g w) :=
  finite_coherent_stress_smooth U g (metricInverse g) w C.weight C.axisA C.axisB
    C.initialU C.initialV hg (constructed_metric_inverse_smooth U g hg hLor) hw

theorem joint_matter_differentiable (U : Set Coordinate4) (C : UnitaryLabelData ι)
    (g : TensorField4) (w : ι → CovectorField4)
    (hg : SmoothMatrixOn U g) (hLor : ∀ x ∈ U, LorentzByCongruence (g x))
    (hw : ∀ j, SmoothVectorOn U (w j)) :
    ∀ i j, DifferentiableOn ℝ (fun x => jointMatter C g w x i j) U := by
  intro i j
  exact (joint_matter_smooth U C g w hg hLor hw i j).differentiableOn (by simp)

theorem joint_matter_symmetric (C : UnitaryLabelData ι)
    (g : TensorField4) (w : ι → CovectorField4) (x : Coordinate4)
    (hg : (g x)ᵀ = g x) : (jointMatter C g w x)ᵀ = jointMatter C g w x :=
  finite_coherent_stress_symmetric g (metricInverse g) w C.weight C.axisA C.axisB
    C.initialU C.initialV x hg

theorem joint_response_matches_matter (C : UnitaryLabelData ι)
    (g : TensorField4) (w : ι → CovectorField4) (x direction : Coordinate4)
    (hn : tensorQuad (g x) direction = 0) :
    jointResponse C (fun j => covectorRead (w j x) direction) =
      -Real.pi * tensorQuad (jointMatter C g w x) direction :=
  finite_response_matches_null_source g (metricInverse g) w C.weight C.axisA C.axisB
    C.initialU C.initialV x direction hn

theorem joint_heat_matching
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x direction : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x direction)
    (C : UnitaryLabelData ι) (w : ι → CovectorField4) (rate : ℝ)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ i j, DifferentiableOn ℝ (fun y => jointMatter C g w y i j) U)
    (hn : tensorQuad (g x) direction = 0) :
    Tendsto (fun t => microscopicHeatError (jointPreparation C w x direction) rate
      (constructedHeat P (jointMatter C g w) rate hU hg hT) t / t^2)
      (𝓝[<] 0) (𝓝 0) := by
  let X := jointPreparation C w x direction
  let heat := constructedHeat P (jointMatter C g w) rate hU hg hT
  have hQ := constructed_heat_quadratic_limit P (jointMatter C g w) rate hU hg hT
  have hK : Tendsto (fun t => modularIncrement (jointBase C) (X.weights t) / t^2)
      (𝓝[<] 0) (𝓝 (jointResponse C (fun j => covectorRead (w j x) direction))) :=
    joint_modular_quadratic_limit C (fun j => covectorRead (w j x) direction)
  have hl := hQ.sub (hK.const_mul (rate / (2*Real.pi)))
  have he : (fun t => microscopicHeatError X rate heat t / t^2) =
      (fun t => heat t / t^2 - rate / (2*Real.pi) *
        (modularIncrement (jointBase C) (X.weights t) / t^2)) := by
    funext t
    unfold microscopicHeatError
    ring
  change Tendsto (fun t => microscopicHeatError X rate heat t / t^2) _ _
  rw [he]
  rw [joint_response_matches_matter C g w x direction hn] at hl
  have cancel (matter : ℝ) :
      -rate * matter / 2 - rate / (2*Real.pi) * (-Real.pi * matter) = 0 := by
    field_simp [Real.pi_ne_zero]
    ring
  rw [cancel] at hl
  exact hl

theorem joint_area_error_limit
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x direction : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x direction)
    (C : UnitaryLabelData ι) (w : ι → CovectorField4) (eta : ℝ)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (ht : ∀ i j k, Gamma x i k j = Gamma x j k i) :
    Tendsto (fun t => microscopicAreaError (jointPreparation C w x direction) eta
      (inducedArea g P.curve P.screen.vectors) t / t^2) (𝓝[<] 0)
      (𝓝 (jointResponse C (fun j => covectorRead (w j x) direction) +
        eta * tensorQuad (coordinateRicci Gamma x) direction / 2)) := by
  let X := jointPreparation C w x direction
  let A := inducedArea g P.curve P.screen.vectors
  have hS : Tendsto (fun t => (finiteEntropy (X.weights t) - finiteEntropy (jointBase C)) / t^2)
      (𝓝[<] 0) (𝓝 (jointResponse C (fun j => covectorRead (w j x) direction))) :=
    joint_entropy_quadratic_limit C (fun j => covectorRead (w j x) direction)
  have hA0 : A 0 = 1 := equilibrium_screen_area_initial _ _ _ _ _ P
  have hA : Tendsto (fun t => (A t-A 0) / t^2) (𝓝[<] 0)
      (𝓝 (-tensorQuad (coordinateRicci Gamma x) direction / 2)) := by
    rw [hA0]
    exact screen_area_quadratic_limit U hU g Gamma hg hG x direction P ht
  have hl := hS.sub (hA.const_mul eta)
  have he : (fun t => microscopicAreaError X eta A t / t^2) =
      (fun t => (finiteEntropy (X.weights t) - finiteEntropy (jointBase C)) / t^2 -
        eta * ((A t-A 0) / t^2)) := by
    funext t
    unfold microscopicAreaError
    ring
  change Tendsto (fun t => microscopicAreaError X eta A t / t^2) _ _
  rw [he]
  have coefficient (response ricci : ℝ) :
      response - eta * (-ricci / 2) = response + eta * ricci / 2 := by ring
  rw [coefficient] at hl
  exact hl

theorem joint_area_matching_iff_ricci
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x direction : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x direction)
    (C : UnitaryLabelData ι) (w : ι → CovectorField4) (eta : ℝ)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (ht : ∀ i j k, Gamma x i k j = Gamma x j k i)
    (hn : tensorQuad (g x) direction = 0) :
    Tendsto (fun t => microscopicAreaError (jointPreparation C w x direction) eta
      (inducedArea g P.curve P.screen.vectors) t / t^2) (𝓝[<] 0) (𝓝 0) ↔
      eta * tensorQuad (coordinateRicci Gamma x) direction =
        2*Real.pi * tensorQuad (jointMatter C g w x) direction := by
  rw [past_zero_limit_iff _ _ (joint_area_error_limit P C w eta hU hg hG ht),
    joint_response_matches_matter C g w x direction hn]
  have scalar_balance (ricci matter : ℝ) :
      -Real.pi * matter + eta * ricci / 2 = 0 ↔ eta * ricci = 2*Real.pi*matter := by
    constructor <;> intro hh <;> nlinarith only [hh]
  exact scalar_balance _ _

theorem joint_area_implies_clausius
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x direction : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x direction)
    (C : UnitaryLabelData ι) (w : ι → CovectorField4) (rate eta : ℝ)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ i j, DifferentiableOn ℝ (fun y => jointMatter C g w y i j) U)
    (hn : tensorQuad (g x) direction = 0)
    (harea : Tendsto (fun t => microscopicAreaError (jointPreparation C w x direction) eta
      (inducedArea g P.curve P.screen.vectors) t / t^2) (𝓝[<] 0) (𝓝 0)) :
    Tendsto (fun t => horizonBalancePrimitive rate eta (inducedArea g P.curve P.screen.vectors)
      (constructedHeat P (jointMatter C g w) rate hU hg hT) t / t^2) (𝓝[<] 0) (𝓝 0) := by
  have hl := microscopic_residual_coefficient (jointPreparation C w x direction)
    (joint_base_positive C) rate eta _ _
    (joint_heat_matching P C w rate hU hg hT hn) harea
  have hz : (jointPreparation C w x direction).tangent 0 = 0 :=
    joint_curve_tangent_zero C (fun j => covectorRead (w j x) direction)
  rw [hz] at hl
  have hf : diagonalFisher (jointBase C) (0 : ι × Fin 2 → ℝ) = 0 := by
    simp only [diagonalFisher, Pi.zero_apply, zero_pow (by decide : 2 ≠ 0),
      zero_div, Finset.sum_const_zero]
  simpa only [hf, zero_div, mul_zero] using hl

theorem joint_matter_conserved_of_sectors
    (U : Set Coordinate4) (hU : IsOpen U) (C : UnitaryLabelData ι)
    (g : TensorField4) (w : ι → CovectorField4)
    (hg : SmoothMatrixOn U g) (hLor : ∀ x ∈ U, LorentzByCongruence (g x))
    (hw : ∀ j, SmoothVectorOn U (w j))
    (hsector : ∀ q, ∀ x ∈ U, ∀ j, tensorFieldDivergence (metricInverse g)
      (leviCivitaField g (metricInverse g))
      (covectorStressField g (metricInverse g) (w q)
        (coherentCoupling (C.axisA q) (C.axisB q) (C.initialU q) (C.initialV q))) x j = 0) :
    ∀ x ∈ U, ∀ j, tensorFieldDivergence (metricInverse g)
      (leviCivitaField g (metricInverse g)) (jointMatter C g w) x j = 0 := by
  intro x hx j
  rw [jointMatter, finiteCoherentStressField,
    finite_covector_stress_divergence U hU g (metricInverse g)
      (leviCivitaField g (metricInverse g)) w C.weight _
      hg (constructed_metric_inverse_smooth U g hg hLor) hw x hx j]
  apply Finset.sum_eq_zero
  intro q _
  rw [hsector q x hx j, mul_zero]

theorem joint_matter_conserved_of_closed_wave
    (U : Set Coordinate4) (hU : IsOpen U) (C : UnitaryLabelData ι)
    (g : TensorField4) (w : ι → CovectorField4)
    (hg : SmoothMatrixOn U g) (hLor : ∀ x ∈ U, LorentzByCongruence (g x))
    (hw : ∀ j, SmoothVectorOn U (w j))
    (hclosed : ∀ j, ClosedCovectorOn U (w j))
    (hwave : ∀ j, CovectorWaveOn U (metricInverse g) (leviCivitaField g (metricInverse g)) (w j)) :
    ∀ x ∈ U, ∀ j, tensorFieldDivergence (metricInverse g)
      (leviCivitaField g (metricInverse g)) (jointMatter C g w) x j = 0 := by
  have hs : ∀ x ∈ U, (g x)ᵀ = g x :=
    fun x hx => lorentz_metric_symmetric (g x) (hLor x hx)
  have hl : ∀ x ∈ U, metricInverse g x * g x = 1 :=
    fun x hx => constructed_metric_inverse_left g x (hLor x hx)
  have hr : ∀ x ∈ U, g x * metricInverse g x = 1 :=
    fun x hx => constructed_metric_inverse_right g x (hLor x hx)
  exact finite_coherent_stress_conserved U hU g (metricInverse g)
    (leviCivitaField g (metricInverse g)) w C.weight C.axisA C.axisB C.initialU C.initialV
    hg (constructed_metric_inverse_smooth U g hg hLor) hw
    (levi_civita_field_metric_compatible U hU g (metricInverse g) hs hl hr) hs hl hr
    (levi_civita_field_torsion_free U hU g (metricInverse g) hs) hclosed hwave

theorem joint_einstein_from_area
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (C : UnitaryLabelData ι) (g : TensorField4) (w : ι → CovectorField4)
    (hg : SmoothMatrixOn U g) (hLor : ∀ x ∈ U, LorentzByCongruence (g x))
    (hw : ∀ j, SmoothVectorOn U (w j))
    (screens : MetricScreenFamily U g) (eta : ℝ) (heta : eta ≠ 0)
    (hd : ∀ x ∈ U, ∀ j, tensorFieldDivergence (metricInverse g)
      (leviCivitaField g (metricInverse g)) (jointMatter C g w) x j = 0)
    (harea : ∀ x (hx : x ∈ U) direction (hv : direction ≠ 0)
      (hn : tensorQuad (g x) direction = 0),
      Tendsto (fun t => microscopicAreaError (jointPreparation C w x direction) eta
        (inducedArea g (screens x hx direction hv hn).curve
          (screens x hx direction hv hn).screen.vectors) t / t^2) (𝓝[<] 0) (𝓝 0)) :
    ∃ cosmological : ℝ, ∀ x ∈ U,
      geometricEinsteinTensor g (metricInverse g) (leviCivitaField g (metricInverse g)) x +
        cosmological • g x = (2*Real.pi/eta) • jointMatter C g w x := by
  have divide_balance (ricci matter : ℝ) (h : eta * ricci = 2*Real.pi*matter) :
      ricci - (2*Real.pi/eta)*matter = 0 := by
    apply (mul_left_cancel₀ heta)
    field_simp [heta]
    nlinarith only [h]
  apply metric_only_einstein_equation U hU hconn g (jointMatter C g w) (2*Real.pi/eta)
    hLor hg (joint_matter_differentiable U C g w hg hLor hw)
    (fun x hx => joint_matter_symmetric C g w x (lorentz_metric_symmetric (g x) (hLor x hx)))
  · intro x hx direction hn
    by_cases hv : direction = 0
    · subst direction
      simp [tensorQuad]
    · have hG := levi_civita_field_smooth U hU g (metricInverse g) hg
        (constructed_metric_inverse_smooth U g hg hLor)
      have ht := levi_civita_field_torsion_free U hU g (metricInverse g)
        (fun y hy => lorentz_metric_symmetric (g y) (hLor y hy))
      have hb := (joint_area_matching_iff_ricci (screens x hx direction hv hn)
        C w eta hU hg hG (ht x hx) hn).mp (harea x hx direction hv hn)
      rw [tensorQuad_sub_smul]
      exact divide_balance _ _ hb
  · exact hd

theorem joint_einstein_from_area_and_closed_wave
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (C : UnitaryLabelData ι) (g : TensorField4) (w : ι → CovectorField4)
    (hg : SmoothMatrixOn U g) (hLor : ∀ x ∈ U, LorentzByCongruence (g x))
    (hw : ∀ j, SmoothVectorOn U (w j))
    (hclosed : ∀ j, ClosedCovectorOn U (w j))
    (hwave : ∀ j, CovectorWaveOn U (metricInverse g) (leviCivitaField g (metricInverse g)) (w j))
    (screens : MetricScreenFamily U g) (eta : ℝ) (heta : eta ≠ 0)
    (harea : ∀ x (hx : x ∈ U) direction (hv : direction ≠ 0)
      (hn : tensorQuad (g x) direction = 0),
      Tendsto (fun t => microscopicAreaError (jointPreparation C w x direction) eta
        (inducedArea g (screens x hx direction hv hn).curve
          (screens x hx direction hv hn).screen.vectors) t / t^2) (𝓝[<] 0) (𝓝 0)) :
    ∃ cosmological : ℝ, ∀ x ∈ U,
      geometricEinsteinTensor g (metricInverse g) (leviCivitaField g (metricInverse g)) x +
        cosmological • g x = (2*Real.pi/eta) • jointMatter C g w x :=
  joint_einstein_from_area U hU hconn C g w hg hLor hw screens eta heta
    (joint_matter_conserved_of_closed_wave U hU C g w hg hLor hw hclosed hwave) harea

#print axioms jointMatter
#print axioms jointPreparation
#print axioms joint_matter_smooth
#print axioms joint_matter_differentiable
#print axioms joint_matter_symmetric
#print axioms joint_response_matches_matter
#print axioms joint_heat_matching
#print axioms joint_area_error_limit
#print axioms joint_area_matching_iff_ricci
#print axioms joint_area_implies_clausius
#print axioms joint_matter_conserved_of_sectors
#print axioms joint_matter_conserved_of_closed_wave
#print axioms joint_einstein_from_area
#print axioms joint_einstein_from_area_and_closed_wave

end
end ChatgptAudit.JointGravitation
