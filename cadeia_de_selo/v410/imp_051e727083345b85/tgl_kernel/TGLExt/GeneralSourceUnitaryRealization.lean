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
import TGLExt.UnitarySourceCalibration
import TGLExt.FiniteCoherentSources
import TGLExt.JointUnitaryPreparation

set_option autoImplicit false
set_option maxHeartbeats 600000
namespace ChatgptAudit.GeneralSourceUnitary
open Matrix Filter Topology Set TGLExt ChatgptAudit.GeneralMetric
  ChatgptAudit.Coherent023 ChatgptAudit.Unitary022 ChatgptAudit.SignedCoverage
  ChatgptAudit.UnitaryCalibration ChatgptAudit.FiniteCoherentSource
  ChatgptAudit.JointUnitary ChatgptAudit.Micro021
open scoped ContDiff
noncomputable section


def calibrationLabelData : UnitaryLabelData CalibrationIndex where
  weight := fun _ => 1/8
  weight_pos := calibration_weights_positive
  weight_sum := calibration_weights_normalized
  axisA := calibrationAxisA
  axisB := calibrationAxisB
  initialU := fun _ => 3/5
  initialV := fun _ => 4/5
  axis_normalized := calibration_axes_normalized
  initial_normalized := by intro j; norm_num
  positive_u := by intro j; norm_num
  positive_v := by intro j; norm_num

#print axioms calibrationLabelData

def calibrationSourceCovectors (g T : TensorField4) : CalibrationIndex → CovectorField4 :=
  fun j x => calibrationCovector (traceReverse (g x) (metricInverse g x) (T x)) j

#print axioms calibrationSourceCovectors

def realizedSourceField (g T : TensorField4) : TensorField4 :=
  finiteCoherentStressField g (metricInverse g) (calibrationSourceCovectors g T)
    calibrationLabelData.weight calibrationLabelData.axisA calibrationLabelData.axisB
    calibrationLabelData.initialU calibrationLabelData.initialV

#print axioms realizedSourceField

def calibrationSourceCurve (g T : TensorField4) (x d : Coordinate4) :
    DiagonalStateCurve (jointBase calibrationLabelData) :=
  jointCovectorCurve calibrationLabelData (fun j => calibrationSourceCovectors g T j x) d

#print axioms calibrationSourceCurve

def calibrationSourceResponse (g T : TensorField4) (x d : Coordinate4) : ℝ :=
  jointResponse calibrationLabelData
    (fun j => covectorRead (calibrationSourceCovectors g T j x) d)

#print axioms calibrationSourceResponse

theorem calibration_base_positive :
    ∀ k, 0 < jointBase calibrationLabelData k :=
  joint_base_positive calibrationLabelData

#print axioms calibration_base_positive

theorem calibration_base_normalized :
    (∑ k, jointBase calibrationLabelData k) = 1 := by
  calc
    _ = ∑ k, jointWeights calibrationLabelData (fun _ => 0) 0 k := by
      apply Finset.sum_congr rfl
      intro k _
      exact ((jointUnitaryCurve calibrationLabelData (fun _ => 0)).at_zero k).symm
    _ = 1 := joint_weights_normalized calibrationLabelData (fun _ => 0) 0

#print axioms calibration_base_normalized

theorem calibration_source_covectors_smooth (U : Set Coordinate4) (g T : TensorField4)
    (hg : SmoothMatrixOn U g) (hT : SmoothMatrixOn U T)
    (hLor : ∀ x ∈ U, LorentzByCongruence (g x)) (j : CalibrationIndex) :
    SmoothVectorOn U (calibrationSourceCovectors g T j) :=
  general_source_unitary_covectors_smooth U g T hg hT hLor j

#print axioms calibration_source_covectors_smooth

theorem realized_source_eq (g T : TensorField4) (x : Coordinate4)
    (hLor : LorentzByCongruence (g x)) (hT : (T x)ᵀ = T x) :
    realizedSourceField g T x = T x := by
  change calibratedStress (g x) (metricInverse g x)
    (traceReverse (g x) (metricInverse g x) (T x)) = T x
  exact every_symmetric_source_has_unitary_calibration _ _ _
    (constructed_metric_inverse_left g x hLor) (lorentz_metric_symmetric _ hLor) hT

#print axioms realized_source_eq

theorem realized_source_eq_on (U : Set Coordinate4) (g T : TensorField4)
    (hLor : ∀ x ∈ U, LorentzByCongruence (g x)) (hT : ∀ x ∈ U, (T x)ᵀ = T x) :
    EqOn (realizedSourceField g T) T U := by
  intro x hx
  exact realized_source_eq g T x (hLor x hx) (hT x hx)

#print axioms realized_source_eq_on

theorem realized_source_symmetric (g T : TensorField4) (x : Coordinate4)
    (hLor : LorentzByCongruence (g x)) :
    (realizedSourceField g T x)ᵀ = realizedSourceField g T x :=
  finite_coherent_stress_symmetric g (metricInverse g) _ _ _ _ _ _ x
    (lorentz_metric_symmetric _ hLor)

#print axioms realized_source_symmetric

theorem realized_source_smooth (U : Set Coordinate4) (g T : TensorField4)
    (hg : SmoothMatrixOn U g) (hT : SmoothMatrixOn U T)
    (hLor : ∀ x ∈ U, LorentzByCongruence (g x)) :
    SmoothMatrixOn U (realizedSourceField g T) :=
  finite_coherent_stress_smooth U g (metricInverse g) _ _ _ _ _ _ hg
    (constructed_metric_inverse_smooth U g hg hLor)
    (calibration_source_covectors_smooth U g T hg hT hLor)

#print axioms realized_source_smooth

theorem realized_source_divergence_eq (U : Set Coordinate4) (hU : IsOpen U)
    (g T : TensorField4) (Gamma : ConnectionField4)
    (hLor : ∀ x ∈ U, LorentzByCongruence (g x)) (hT : ∀ x ∈ U, (T x)ᵀ = T x)
    (x : Coordinate4) (hx : x ∈ U) :
    tensorFieldDivergence (metricInverse g) Gamma (realizedSourceField g T) x =
      tensorFieldDivergence (metricInverse g) Gamma T x :=
  tensorFieldDivergence_congr_on U hU (metricInverse g) Gamma _ _
    (realized_source_eq_on U g T hLor hT) x hx


#print axioms realized_source_divergence_eq

theorem realized_source_conserved (U : Set Coordinate4) (hU : IsOpen U)
    (g T : TensorField4) (Gamma : ConnectionField4)
    (hLor : ∀ x ∈ U, LorentzByCongruence (g x)) (hT : ∀ x ∈ U, (T x)ᵀ = T x)
    (hc : ∀ x ∈ U, ∀ j, tensorFieldDivergence (metricInverse g) Gamma T x j = 0) :
    ∀ x ∈ U, ∀ j, tensorFieldDivergence (metricInverse g) Gamma
      (realizedSourceField g T) x j = 0 := by
  intro x hx j
  rw [realized_source_divergence_eq U hU g T Gamma hLor hT x hx]
  exact hc x hx j

#print axioms realized_source_conserved

theorem calibration_source_weights_nonnegative (g T : TensorField4) (x d : Coordinate4)
    (t : ℝ) : ∀ k, 0 ≤ (calibrationSourceCurve g T x d).weights t k :=
  joint_weights_nonnegative calibrationLabelData (fun j => covectorRead (calibrationSourceCovectors g T j x) d) t

#print axioms calibration_source_weights_nonnegative

theorem calibration_source_weights_normalized (g T : TensorField4) (x d : Coordinate4)
    (t : ℝ) : ∑ k, (calibrationSourceCurve g T x d).weights t k = 1 :=
  (calibrationSourceCurve g T x d).trace_one t

#print axioms calibration_source_weights_normalized

theorem calibration_source_curve_tangent_zero (g T : TensorField4) (x d : Coordinate4) :
    (calibrationSourceCurve g T x d).tangent 0 = 0 :=
  joint_curve_tangent_zero calibrationLabelData (fun j => covectorRead (calibrationSourceCovectors g T j x) d)

#print axioms calibration_source_curve_tangent_zero

theorem calibration_source_entropy_quadratic_limit (g T : TensorField4) (x d : Coordinate4) :
    Tendsto (fun t => (finiteEntropy ((calibrationSourceCurve g T x d).weights t) -
      finiteEntropy (jointBase calibrationLabelData)) / t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 (calibrationSourceResponse g T x d)) :=
  joint_entropy_quadratic_limit calibrationLabelData (fun j => covectorRead (calibrationSourceCovectors g T j x) d)

#print axioms calibration_source_entropy_quadratic_limit

theorem calibration_source_modular_quadratic_limit (g T : TensorField4) (x d : Coordinate4) :
    Tendsto (fun t => modularIncrement (jointBase calibrationLabelData)
      ((calibrationSourceCurve g T x d).weights t) / t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 (calibrationSourceResponse g T x d)) :=
  joint_modular_quadratic_limit calibrationLabelData (fun j => covectorRead (calibrationSourceCovectors g T j x) d)

#print axioms calibration_source_modular_quadratic_limit

theorem calibration_source_response_null (g T : TensorField4) (x d : Coordinate4)
    (hLor : LorentzByCongruence (g x)) (hT : (T x)ᵀ = T x)
    (hn : tensorQuad (g x) d = 0) :
    calibrationSourceResponse g T x d = -Real.pi * tensorQuad (T x) d := by
  have h := finite_response_matches_null_source g (metricInverse g)
    (calibrationSourceCovectors g T) calibrationLabelData.weight
    calibrationLabelData.axisA calibrationLabelData.axisB calibrationLabelData.initialU
    calibrationLabelData.initialV x d hn
  change calibrationSourceResponse g T x d =
    -Real.pi * tensorQuad (realizedSourceField g T x) d at h
  rw [realized_source_eq g T x hLor hT] at h
  exact h

#print axioms calibration_source_response_null

theorem calibration_source_entropy_null_limit (g T : TensorField4) (x d : Coordinate4)
    (hLor : LorentzByCongruence (g x)) (hT : (T x)ᵀ = T x)
    (hn : tensorQuad (g x) d = 0) :
    Tendsto (fun t => (finiteEntropy ((calibrationSourceCurve g T x d).weights t) -
      finiteEntropy (jointBase calibrationLabelData)) / t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 (-Real.pi * tensorQuad (T x) d)) := by
  rw [← calibration_source_response_null g T x d hLor hT hn]
  exact calibration_source_entropy_quadratic_limit g T x d

#print axioms calibration_source_entropy_null_limit

theorem calibration_source_modular_null_limit (g T : TensorField4) (x d : Coordinate4)
    (hLor : LorentzByCongruence (g x)) (hT : (T x)ᵀ = T x)
    (hn : tensorQuad (g x) d = 0) :
    Tendsto (fun t => modularIncrement (jointBase calibrationLabelData)
      ((calibrationSourceCurve g T x d).weights t) / t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 (-Real.pi * tensorQuad (T x) d)) := by
  rw [← calibration_source_response_null g T x d hLor hT hn]
  exact calibration_source_modular_quadratic_limit g T x d

#print axioms calibration_source_modular_null_limit

theorem calibration_source_block_unitary (g T : TensorField4) (x d : Coordinate4) (t : ℝ) :
    let F := jointBlockFlow calibrationLabelData
      (fun j => covectorRead (calibrationSourceCovectors g T j x) d) t
    Fᴴ * F = 1 ∧ F * Fᴴ = 1 :=
  joint_block_flow_unitary calibrationLabelData (fun j => covectorRead (calibrationSourceCovectors g T j x) d) t

#print axioms calibration_source_block_unitary

theorem calibration_source_amplitude_weights (g T : TensorField4)
    (x d : Coordinate4) (t : ℝ) (k : Fin 2 × CalibrationIndex) :
    let A := jointBlockAmplitude calibrationLabelData
      (fun j => covectorRead (calibrationSourceCovectors g T j x) d) t
    A k * star (A k) = ((calibrationSourceCurve g T x d).weights t (k.2,k.1) : ℂ) :=
  joint_block_amplitude_weights calibrationLabelData (fun j => covectorRead (calibrationSourceCovectors g T j x) d) t k

#print axioms calibration_source_amplitude_weights

end
end ChatgptAudit.GeneralSourceUnitary
