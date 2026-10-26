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
import TGLExt.GeneralSourceUnitaryRealization
import TGLExt.FiniteResponseReconstruction

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit.FullSourceResponse
open Matrix Set TGLExt ChatgptAudit.GeneralMetric ChatgptAudit.Coherent023
  ChatgptAudit.SignedCoverage ChatgptAudit.UnitaryCalibration
  ChatgptAudit.FiniteCoherentSource ChatgptAudit.JointUnitary
  ChatgptAudit.GeneralSourceUnitary ChatgptAudit.FiniteResponseRecord
noncomputable section

def calibratedPointResponse (g gi T : Tensor4) (d : Coordinate4) : ℝ :=
  jointResponse calibrationLabelData
    (fun j => covectorRead (calibrationCovector (traceReverse g gi T) j) d)

def normalizedSamples (s : ResponseSamples) : ResponseSamples :=
  fun i => s i / (-Real.pi)

def decodeSource (g gi : Tensor4) (s : ResponseSamples) : Tensor4 :=
  traceReverse g gi (decodeResponse (normalizedSamples s))

theorem calibrated_point_response_all_directions (g gi T : Tensor4) (d : Coordinate4)
    (hg : gᵀ = g) (hT : Tᵀ = T) :
    calibratedPointResponse g gi T d = -Real.pi * tensorQuad (traceReverse g gi T) d := by
  let F := traceReverse g gi T
  have hs : Fᵀ = F := trace_reverse_symmetric g gi T hg hT
  have hn : tensorQuad (0 : Tensor4) d = 0 := by simp [tensorQuad]
  have h := finite_response_matches_null_source (fun _ => (0 : Tensor4))
    (fun _ => (0 : Tensor4)) (fun j _ => calibrationCovector F j)
    calibrationLabelData.weight calibrationLabelData.axisA calibrationLabelData.axisB
    calibrationLabelData.initialU calibrationLabelData.initialV (0 : Coordinate4) d hn
  change calibratedPointResponse g gi T d =
    -Real.pi * tensorQuad (calibratedStress 0 0 F) d at h
  have hz : traceReverse (0 : Tensor4) 0 F = F := by simp [traceReverse]
  rw [calibrated_stress_is_signed_stress, signed_stress_is_trace_reverse 0 0 F hs, hz] at h
  exact h

theorem normalized_point_response (g gi T : Tensor4) (d : Coordinate4)
    (hg : gᵀ = g) (hT : Tᵀ = T) :
    calibratedPointResponse g gi T d / (-Real.pi) = tensorQuad (traceReverse g gi T) d := by
  rw [calibrated_point_response_all_directions g gi T d hg hT]
  field_simp [Real.pi_ne_zero]

theorem source_field_response_all_directions (g T : TensorField4) (x d : Coordinate4)
    (hg : (g x)ᵀ = g x) (hT : (T x)ᵀ = T x) :
    calibrationSourceResponse g T x d =
      -Real.pi * tensorQuad (traceReverse (g x) (metricInverse g x) (T x)) d :=
  calibrated_point_response_all_directions (g x) (metricInverse g x) (T x) d hg hT

theorem normalized_sample_response (q : Coordinate4 → ℝ) :
    normalizedSamples (sampleResponse q) = sampleResponse (fun d => q d / (-Real.pi)) :=
  rfl

theorem ten_responses_reconstruct_source (g gi T : Tensor4)
    (hi : gi*g = 1) (hg : gᵀ = g) (hT : Tᵀ = T) :
    decodeSource g gi (sampleResponse (calibratedPointResponse g gi T)) = T := by
  have hs := trace_reverse_symmetric g gi T hg hT
  have hq := finite_response_reconstructs_given_tensor
    (fun d => calibratedPointResponse g gi T d / (-Real.pi)) (traceReverse g gi T) hs
    (fun d => normalized_point_response g gi T d hg hT)
  unfold decodeSource
  rw [normalized_sample_response, hq, trace_reverse_involutive g gi T hi]

theorem ten_responses_determine_source (g gi T A : Tensor4)
    (hi : gi*g = 1) (hg : gᵀ = g) (hT : Tᵀ = T) (hA : Aᵀ = A)
    (hs : sampleResponse (calibratedPointResponse g gi T) =
      sampleResponse (calibratedPointResponse g gi A)) :
    T = A := by
  rw [← ten_responses_reconstruct_source g gi T hi hg hT, hs,
    ten_responses_reconstruct_source g gi A hi hg hA]

theorem ten_responses_reconstruct_source_field (g T : TensorField4) (x : Coordinate4)
    (hLor : LorentzByCongruence (g x)) (hT : (T x)ᵀ = T x) :
    decodeSource (g x) (metricInverse g x)
      (sampleResponse (calibrationSourceResponse g T x)) = T x :=
  ten_responses_reconstruct_source (g x) (metricInverse g x) (T x)
    (constructed_metric_inverse_left g x hLor) (lorentz_metric_symmetric (g x) hLor) hT

theorem ten_responses_determine_source_field (g T A : TensorField4) (x : Coordinate4)
    (hLor : LorentzByCongruence (g x)) (hT : (T x)ᵀ = T x) (hA : (A x)ᵀ = A x)
    (hs : sampleResponse (calibrationSourceResponse g T x) =
      sampleResponse (calibrationSourceResponse g A x)) :
    T x = A x :=
  ten_responses_determine_source (g x) (metricInverse g x) (T x) (A x)
    (constructed_metric_inverse_left g x hLor) (lorentz_metric_symmetric (g x) hLor) hT hA hs

theorem decode_source_injective (g gi : Tensor4) (hi : gi*g = 1) :
    Function.Injective (decodeSource g gi) := by
  intro s t h
  have ht := congrArg (traceReverse g gi) h
  change traceReverse g gi (traceReverse g gi (decodeResponse (normalizedSamples s))) =
    traceReverse g gi (traceReverse g gi (decodeResponse (normalizedSamples t))) at ht
  rw [trace_reverse_involutive g gi _ hi, trace_reverse_involutive g gi _ hi] at ht
  have hn := decoded_response_injective ht
  funext i
  have he : s i / (-Real.pi) = t i / (-Real.pi) := congrFun hn i
  have hm := congrArg (fun a : ℝ => a * (-Real.pi)) he
  simpa only [div_mul_cancel₀ _ (neg_ne_zero.mpr Real.pi_ne_zero)] using hm

theorem source_response_samples_roundtrip (g gi : Tensor4)
    (hi : gi*g = 1) (hg : gᵀ = g) (s : ResponseSamples) :
    sampleResponse (calibratedPointResponse g gi (decodeSource g gi s)) = s := by
  apply decode_source_injective g gi hi
  exact ten_responses_reconstruct_source g gi (decodeSource g gi s) hi hg
    (trace_reverse_symmetric g gi (decodeResponse (normalizedSamples s)) hg
      (decoded_response_symmetric (normalizedSamples s)))

#print axioms calibratedPointResponse
#print axioms normalizedSamples
#print axioms decodeSource
#print axioms calibrated_point_response_all_directions
#print axioms normalized_point_response
#print axioms source_field_response_all_directions
#print axioms normalized_sample_response
#print axioms ten_responses_reconstruct_source
#print axioms ten_responses_determine_source
#print axioms ten_responses_reconstruct_source_field
#print axioms ten_responses_determine_source_field
#print axioms decode_source_injective
#print axioms source_response_samples_roundtrip
end
end ChatgptAudit.FullSourceResponse
