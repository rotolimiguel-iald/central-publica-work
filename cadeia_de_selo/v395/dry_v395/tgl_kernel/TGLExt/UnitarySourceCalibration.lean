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
import TGLExt.SignedCovectorCoverage

set_option autoImplicit false
set_option maxHeartbeats 3500000
namespace ChatgptAudit.UnitaryCalibration
open Matrix Set TGLExt ChatgptAudit.GeneralMetric ChatgptAudit.Coherent023
  ChatgptAudit.Unitary022 ChatgptAudit.SignedCoverage
open scoped ContDiff
noncomputable section

def positiveCoupling : ℝ := coherentCoupling (-3/5) (4/5) (3/5) (4/5)
def negativeCoupling : ℝ := coherentCoupling 0 1 (3/5) (4/5)

theorem positive_coupling_positive : 0<positiveCoupling :=
  coherent_negative_control_coupling_positive

theorem negative_coupling_negative : negativeCoupling<0 := by
  unfold negativeCoupling coherentCoupling
  exact div_neg_of_neg_of_pos (neg_neg_of_pos positive_control_response_strict) Real.pi_pos

def positiveScale : ℝ := Real.sqrt (8/positiveCoupling)
def negativeScale : ℝ := Real.sqrt (8/(-negativeCoupling))

theorem positive_scale_squared : positiveScale^2=8/positiveCoupling := by
  exact Real.sq_sqrt (div_nonneg (by norm_num) (le_of_lt positive_coupling_positive))

theorem negative_scale_squared : negativeScale^2=8/(-negativeCoupling) := by
  exact Real.sq_sqrt (div_nonneg (by norm_num) (le_of_lt (neg_pos.mpr negative_coupling_negative)))

theorem positive_scale_identity : positiveCoupling*positiveScale^2=8 := by
  rw [positive_scale_squared]
  field_simp [ne_of_gt positive_coupling_positive]

theorem negative_scale_identity : negativeCoupling*negativeScale^2= -8 := by
  rw [negative_scale_squared]
  field_simp [ne_of_lt negative_coupling_negative]

theorem covector_stress_vector_smul (g gi : Tensor4) (w : Coordinate4) (r c : ℝ) :
    covectorStress g gi (r • w) c = covectorStress g gi w (c*r^2) := by
  ext i j
  simp only [covectorStress, Matrix.smul_apply, Matrix.sub_apply, Matrix.vecMulVec,
    Matrix.of_apply, Pi.smul_apply, smul_eq_mul, tensorQuad, Matrix.mulVec, dotProduct,
    Fin.sum_univ_four]
  ring

theorem weighted_scaled_stress (g gi : Tensor4) (w : Coordinate4) (r c weight : ℝ) :
    weight • covectorStress g gi (r • w) c =
      covectorStress g gi w (weight*(c*r^2)) := by
  rw [covector_stress_vector_smul]
  simp only [covectorStress, smul_smul]

theorem positive_calibration (g gi : Tensor4) (w : Coordinate4) :
    ((1:ℝ)/8) • covectorStress g gi (positiveScale • w) positiveCoupling =
      covectorStress g gi w 1 := by
  rw [weighted_scaled_stress, positive_scale_identity]
  norm_num

theorem negative_calibration (g gi : Tensor4) (w : Coordinate4) :
    ((1:ℝ)/8) • covectorStress g gi (negativeScale • w) negativeCoupling =
      covectorStress g gi w (-1) := by
  rw [weighted_scaled_stress, negative_scale_identity]
  norm_num

abbrev CalibrationIndex := Fin 4 × Fin 2

def calibrationAxisA (j : CalibrationIndex) : ℝ :=
  if j.2=0 then -3/5 else 0

def calibrationAxisB (j : CalibrationIndex) : ℝ :=
  if j.2=0 then 4/5 else 1

def calibrationCovector (A : Tensor4) (j : CalibrationIndex) : Coordinate4 :=
  if j.2=0 then positiveScale • plusCovector A j.1
  else negativeScale • minusCovector A j.1

def calibratedStress (g gi A : Tensor4) : Tensor4 :=
  ∑ j : CalibrationIndex, ((1:ℝ)/8) • covectorStress g gi (calibrationCovector A j)
    (coherentCoupling (calibrationAxisA j) (calibrationAxisB j) (3/5) (4/5))

theorem calibration_axes_normalized (j : CalibrationIndex) :
    (calibrationAxisA j)^2+(calibrationAxisB j)^2=1 := by
  unfold calibrationAxisA calibrationAxisB
  split_ifs <;> norm_num

theorem calibration_weights_positive : ∀ _j : CalibrationIndex, (0:ℝ)<1/8 := by
  intro _
  norm_num

theorem calibration_weights_normalized : (∑ _j : CalibrationIndex, (1:ℝ)/8)=1 := by
  norm_num

theorem calibrated_stress_is_signed_stress (g gi A : Tensor4) :
    calibratedStress g gi A=signedStress g gi A := by
  unfold calibratedStress
  rw [Fintype.sum_prod_type]
  simp only [Fin.sum_univ_two, calibrationAxisA, calibrationAxisB, calibrationCovector]
  norm_num only
  have h10 : (1 : Fin 2) ≠ 0 := by decide
  simp only [if_true, h10, if_false]
  simp only [← neg_div]
  change (∑ i : Fin 4,
    (((1:ℝ)/8) • covectorStress g gi (positiveScale • plusCovector A i) positiveCoupling +
    ((1:ℝ)/8) • covectorStress g gi (negativeScale • minusCovector A i) negativeCoupling))=_
  simp only [positive_calibration, negative_calibration]
  rfl

theorem every_symmetric_source_has_unitary_calibration (g gi T : Tensor4)
    (hi : gi*g=1) (hg : gᵀ=g) (hT : Tᵀ=T) :
    calibratedStress g gi (traceReverse g gi T)=T := by
  rw [calibrated_stress_is_signed_stress,
    every_symmetric_source_has_eight_covectors g gi T hi hg hT]

theorem calibration_covector_smooth (U : Set Coordinate4) (A : TensorField4)
    (hA : SmoothMatrixOn U A) (j : CalibrationIndex) :
    SmoothVectorOn U (fun x => calibrationCovector (A x) j) := by
  intro k
  unfold calibrationCovector
  split_ifs
  · exact contDiffOn_const.mul (plus_covector_smooth U A hA j.1 k)
  · exact contDiffOn_const.mul (minus_covector_smooth U A hA j.1 k)

theorem general_source_unitary_covectors_smooth
    (U : Set Coordinate4) (g T : TensorField4)
    (hg : SmoothMatrixOn U g) (hT : SmoothMatrixOn U T)
    (hLor : ∀ x∈U, LorentzByCongruence (g x)) (j : CalibrationIndex) :
    SmoothVectorOn U (fun x =>
      calibrationCovector (traceReverse (g x) (metricInverse g x) (T x)) j) :=
  calibration_covector_smooth U _ (trace_reverse_field_smooth U g (metricInverse g) T hg
    (constructed_metric_inverse_smooth U g hg hLor) hT) j

#print axioms positiveCoupling
#print axioms negativeCoupling
#print axioms positive_coupling_positive
#print axioms negative_coupling_negative
#print axioms positiveScale
#print axioms negativeScale
#print axioms positive_scale_squared
#print axioms negative_scale_squared
#print axioms positive_scale_identity
#print axioms negative_scale_identity
#print axioms covector_stress_vector_smul
#print axioms weighted_scaled_stress
#print axioms positive_calibration
#print axioms negative_calibration
#print axioms CalibrationIndex
#print axioms calibrationAxisA
#print axioms calibrationAxisB
#print axioms calibrationCovector
#print axioms calibratedStress
#print axioms calibration_axes_normalized
#print axioms calibration_weights_positive
#print axioms calibration_weights_normalized
#print axioms calibrated_stress_is_signed_stress
#print axioms every_symmetric_source_has_unitary_calibration
#print axioms calibration_covector_smooth
#print axioms general_source_unitary_covectors_smooth
end
end ChatgptAudit.UnitaryCalibration
