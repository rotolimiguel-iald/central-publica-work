-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — LOTE 063..066 (09/09/2026, noite), transposta em 10/09/2026 (ENTREGA_067 = elo do lote)
-- Os 21 modulos restantes da bancada (elos 83 -> 93 -> 98 da cadeia de copias integradas; 77 ja na v338).
--   063 (6 modulos, 113 teoremas): RESPOSTA GIBBS ANTES DA FONTE — protocolo misto (W = X + Z, medicao Z, s = v^2 t^2):
--     igualdade das respostas de entropia e energia de referencia na ordem quadratica; a fonte calculada da resposta com
--     conservacao por closed/wave; o seletor transporta o registro; O LIMITE LOCAL DE INTERACOES EXTENSIVAS (Lean);
--     a lei fisica de area e a metrica seguem entradas. [DERIVED, escrito]: Araki/GNS, tempo global, KMS no fecho C*.
--   065 (10 modulos, 108 teoremas): estabilidade do prefixo do caracter, resolucao finita, controle de malha do
--     registro, cotas de erro da resposta finita, precisao finita de Gibbs misto, janela de amostragem; METRICA DE
--     FISHER-LORENTZ SELECIONADA, variacao da densidade de materia escalar, ponte Fisher-Gibbs, CONSERVACAO sigma.
--   066 (5 modulos, 67 teoremas): sigma DOS MESMOS P (phi_j = sqrt(P_j/(1 - P_s))), resposta de Gibbs ASSINADA (dois
--     sinais com probabilidades positivas), esperanca negativa renormalizada, cobertura, reconstrucao por DEZ LIMITES
--     (SignedGibbsFiniteRecord); T e entrada; nao se identifica o observavel com stress de QFT.
--   Estatuto: [REAL] o compilado; [INPUT] a lei de area, a metrica, T, a acao/particao; [DERIVED + KNOWN] Araki, GNS,
--   KMS C*; [OPEN] correspondencia geral de selecao/materia/protocolo/area, realizacao interagente, anomalias, UV.
--   As ENTREGAS 067..087 sao MATEMATICA ESCRITA REVISADA (CAS, sem Lean) — registradas no diario e no Atlas como
--   [DERIVED], nao como flags; a propria bancada: "nao promover demonstracoes escritas a flags de compilacao".
-- Auditoria da gerencia (sessao d554e796, 10/09/2026): lote montado da CADEIA de recibos (98 -> 93 -> 83 -> 77...),
--   77 ja no kernel pulados; 21/21 hashes lidos dos bytes; zero proibidos; guarda de colisao; recompilacao INDEPENDENTE
--   21/21 contra o kernel v338, axiomas no trio; a copia integrada da bancada NAO foi usada (so as fontes congeladas).
--   Transposicao: cabecalho + prefixo TGLExt. nos imports locais (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.GravitationalResponseRecord
import TGLExt.FiniteCoherentSources

set_option autoImplicit false
set_option maxHeartbeats 1500000
namespace ChatgptAudit.ProbeSource
open Matrix Filter Topology Set TGLExt ChatgptAudit
  ChatgptAudit.Coherent023 ChatgptAudit.FiniteCoherentSource
  ChatgptAudit.GravitationalRecord ChatgptAudit.GeneralMetric
  ChatgptAudit.AngularTensorCodec ChatgptAudit.FullSourceResponse
  ChatgptAudit.SignedCoverage ChatgptAudit.FiniteResponseRecord
open scoped ContDiff
noncomputable section
variable {J : Type} [Fintype J] {U : Set Coordinate4}

def responseCoupling (slope : ℝ) : ℝ := slope^2/(2*Real.pi)

def probeEntropyResponse (slope : J → ℝ) (w : J → Coordinate4) (d : Coordinate4) : ℝ :=
  ∑ j, -(slope j * covectorRead (w j) d)^2/2

def probeResponseTensor (slope : J → ℝ) (w : J → Coordinate4) : Tensor4 :=
  ∑ j, responseCoupling (slope j) • Matrix.vecMulVec (w j) (w j)

theorem response_coupling_nonnegative (slope : ℝ) : 0 ≤ responseCoupling slope := by
  unfold responseCoupling
  positivity

theorem response_coupling_positive (slope : ℝ) (hs : slope ≠ 0) :
    0 < responseCoupling slope := by
  unfold responseCoupling
  positivity

theorem probe_response_nonpositive (slope : J → ℝ) (w : J → Coordinate4) (d : Coordinate4) :
    probeEntropyResponse slope w d ≤ 0 := by
  exact Finset.sum_nonpos (fun j _ => div_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr (sq_nonneg _)) (by norm_num))

theorem probe_tensor_symmetric (slope : J → ℝ) (w : J → Coordinate4) :
    (probeResponseTensor slope w)ᵀ=probeResponseTensor slope w := by
  simp only [probeResponseTensor,Matrix.transpose_sum,Matrix.transpose_smul,outer_tensor_symmetric]

theorem probe_tensor_quad (slope : J → ℝ) (w : J → Coordinate4) (d : Coordinate4) :
    tensorQuad (probeResponseTensor slope w) d=
      ∑ j, responseCoupling (slope j)*(covectorRead (w j) d)^2 := by
  simp only [probeResponseTensor,tensorQuad,Matrix.sum_mulVec,dotProduct_sum,
    Matrix.smul_mulVec,dotProduct_smul,smul_eq_mul]
  change (∑ j, responseCoupling (slope j)*tensorQuad (Matrix.vecMulVec (w j) (w j)) d)=_
  simp only [outer_tensor_quad]

theorem normalized_probe_response (slope : J → ℝ) (w : J → Coordinate4) (d : Coordinate4) :
    probeEntropyResponse slope w d/(-Real.pi)=tensorQuad (probeResponseTensor slope w) d := by
  rw [probeEntropyResponse,Finset.sum_div,probe_tensor_quad]
  apply Finset.sum_congr rfl
  intro j _
  unfold responseCoupling
  field_simp [Real.pi_ne_zero]

theorem ten_probes_reconstruct_response (slope : J → ℝ) (w : J → Coordinate4) :
    decodeResponse (normalizedSamples (sampleResponse (probeEntropyResponse slope w)))=
      probeResponseTensor slope w := by
  rw [normalized_sample_response]
  exact finite_response_reconstructs_given_tensor _ _ (probe_tensor_symmetric slope w)
    (normalized_probe_response slope w)

theorem trace_reverse_scaled_outer (g gi : Tensor4) (w : Coordinate4) (c : ℝ) :
    traceReverse g gi (c • Matrix.vecMulVec w w)=covectorStress g gi w c := by
  simp only [traceReverse,Matrix.mul_smul,Matrix.trace_smul,trace_outer_is_quad,covectorStress]
  ext i j
  simp only [Matrix.sub_apply,Matrix.smul_apply,smul_eq_mul]
  ring

theorem ten_probes_reconstruct_source (g gi : Tensor4) (slope : J → ℝ) (w : J → Coordinate4) :
    decodeSource g gi (sampleResponse (probeEntropyResponse slope w))=
      ∑ j, covectorStress g gi (w j) (responseCoupling (slope j)) := by
  rw [decodeSource,ten_probes_reconstruct_response,probeResponseTensor,trace_reverse_sum]
  apply Finset.sum_congr rfl
  intro j _
  exact trace_reverse_scaled_outer g gi (w j) _

theorem probe_response_samples_smooth (slope : J → ℝ) (w : J → CovectorField4)
    (hw : ∀ j, SmoothVectorOn U (w j)) (i : Fin 10) :
    ContDiffOn ℝ ∞ (fun x => sampleResponse (probeEntropyResponse slope (fun j => w j x)) i) U := by
  simp only [sampleResponse,probeEntropyResponse]
  apply ContDiffOn.sum
  intro j _
  have hr : ContDiffOn ℝ ∞ (fun x => covectorRead (w j x) (probeDirections i)) U := by
    simp only [covectorRead,dotProduct]
    apply ContDiffOn.sum
    intro a _
    exact (hw j a).mul contDiffOn_const
  exact ((contDiffOn_const.mul hr).pow 2).neg.div_const 2

def probeRecord (metric : LorentzProbabilityRecord U) (slope : J → ℝ)
    (w : J → CovectorField4) (hw : ∀ j, SmoothVectorOn U (w j)) :
    GravitationalResponseRecord U where
  metric := metric
  responses := fun x => sampleResponse (probeEntropyResponse slope (fun j => w j x))
  smooth_responses := probe_response_samples_smooth slope w hw

theorem probe_record_metric (metric : LorentzProbabilityRecord U) (slope : J → ℝ)
    (w : J → CovectorField4) (hw : ∀ j, SmoothVectorOn U (w j)) :
    recordMetric (probeRecord metric slope w hw)=decodeRecord metric.data := rfl

theorem probe_record_source (metric : LorentzProbabilityRecord U) (slope : J → ℝ)
    (w : J → CovectorField4) (hw : ∀ j, SmoothVectorOn U (w j)) :
    recordSource (probeRecord metric slope w hw)=
      finiteCovectorStressField (decodeRecord metric.data) (metricInverse (decodeRecord metric.data))
        w (fun _ => 1) (fun j => responseCoupling (slope j)) := by
  funext x
  change decodeSource _ _ (sampleResponse (probeEntropyResponse slope (fun j => w j x)))=_
  rw [ten_probes_reconstruct_source]
  simp only [finiteCovectorStressField,one_smul,covectorStressField,probe_record_metric]

theorem probe_record_null_response (metric : LorentzProbabilityRecord U) (slope : J → ℝ)
    (w : J → CovectorField4) (hw : ∀ j, SmoothVectorOn U (w j)) (x d : Coordinate4)
    (hn : tensorQuad (decodeRecord metric.data x) d=0) :
    probeEntropyResponse slope (fun j => w j x) d=
      -Real.pi*tensorQuad (recordSource (probeRecord metric slope w hw) x) d := by
  rw [probe_record_source,finite_covector_stress_null _ _ _ _ _ x d hn]
  simp only [one_mul,Finset.mul_sum,probeEntropyResponse]
  apply Finset.sum_congr rfl
  intro j _
  unfold responseCoupling
  field_simp [Real.pi_ne_zero]

theorem probe_record_null_nonnegative (metric : LorentzProbabilityRecord U) (slope : J → ℝ)
    (w : J → CovectorField4) (hw : ∀ j, SmoothVectorOn U (w j)) (x d : Coordinate4)
    (hn : tensorQuad (decodeRecord metric.data x) d=0) :
    0 ≤ tensorQuad (recordSource (probeRecord metric slope w hw) x) d := by
  rw [probe_record_source]
  exact finite_covector_stress_null_nonnegative _ _ _ _ _ x d hn
    (fun j => by simpa using response_coupling_nonnegative (slope j))

theorem probe_record_conserved (hU : IsOpen U) (metric : LorentzProbabilityRecord U)
    (slope : J → ℝ) (w : J → CovectorField4) (hw : ∀ j, SmoothVectorOn U (w j))
    (hc : ∀ j, ClosedCovectorOn U (w j))
    (hwave : ∀ j, CovectorWaveOn U (metricInverse (decodeRecord metric.data))
      (leviCivitaField (decodeRecord metric.data) (metricInverse (decodeRecord metric.data))) (w j)) :
    ∀ x∈U, ∀ a, tensorFieldDivergence (metricInverse (decodeRecord metric.data))
      (leviCivitaField (decodeRecord metric.data) (metricInverse (decodeRecord metric.data)))
        (recordSource (probeRecord metric slope w hw)) x a=0 := by
  rw [probe_record_source]
  let g := decodeRecord metric.data
  let gi := metricInverse g
  have hg : SmoothMatrixOn U g := decoded_record_smooth metric.data
  have hgi : SmoothMatrixOn U gi := constructed_metric_inverse_smooth U g hg metric.lorentz
  have hs : ∀ x∈U, (g x)ᵀ=g x := fun x hx => lorentz_metric_symmetric _ (metric.lorentz x hx)
  have hl : ∀ x∈U, gi x*g x=1 := fun x hx => constructed_metric_inverse_left g x (metric.lorentz x hx)
  have hr : ∀ x∈U, g x*gi x=1 := fun x hx => constructed_metric_inverse_right g x (metric.lorentz x hx)
  exact finite_covector_stress_conserved U hU g gi (leviCivitaField g gi) w
    (fun _ => 1) (fun j => responseCoupling (slope j)) hg hgi hw
    (levi_civita_field_metric_compatible U hU g gi hs hl hr) hs hl hr
    (levi_civita_field_torsion_free U hU g gi hs) hc hwave

#print axioms responseCoupling
#print axioms probeEntropyResponse
#print axioms probeResponseTensor
#print axioms response_coupling_nonnegative
#print axioms response_coupling_positive
#print axioms probe_response_nonpositive
#print axioms probe_tensor_symmetric
#print axioms probe_tensor_quad
#print axioms normalized_probe_response
#print axioms ten_probes_reconstruct_response
#print axioms trace_reverse_scaled_outer
#print axioms ten_probes_reconstruct_source
#print axioms probe_response_samples_smooth
#print axioms probeRecord
#print axioms probe_record_metric
#print axioms probe_record_source
#print axioms probe_record_null_response
#print axioms probe_record_null_nonnegative
#print axioms probe_record_conserved
end
end ChatgptAudit.ProbeSource
