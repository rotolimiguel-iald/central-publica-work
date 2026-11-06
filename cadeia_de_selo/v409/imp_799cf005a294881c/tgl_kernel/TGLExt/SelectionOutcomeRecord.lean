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
import TGLExt.SelectionAngleReconstruction
import TGLExt.TheSelectionIsTheBallast

set_option autoImplicit false
set_option maxHeartbeats 600000

namespace ChatgptAudit.SelectionRecord
open Matrix Complex TGLExt ChatgptAudit.SelectionAngle ChatgptAudit.Collapse057
noncomputable section

/-- An angular form, without a preferred representative of its periodic angle. -/
abbrev AngularForm := {A : QubitMatrix // ∃ θ : ℝ, A = angFamily θ}

/-- A modeled occurrence carries the admissible form and a supplied outcome label. -/
abbrev AngularOccurrence := AngularForm × Fin 2

/-- The record keeps the phase and the outcome, not merely their common weight. -/
structure WeightedPhaseRecord where
  weight : ℝ
  phase : ℂ
  outcome : Fin 2

def reflectionWeight (A : QubitMatrix) : ℝ :=
  Complex.normSq (A.mulVec e1 1)

def readRecord (A : QubitMatrix) (outcome : Fin 2) : WeightedPhaseRecord :=
  ⟨reflectionWeight A, phaseReading A, outcome⟩

def encodeOccurrence (x : AngularOccurrence) : WeightedPhaseRecord :=
  readRecord x.1.val x.2

/-- A candidate decoder; its exactness is asserted only on the admissible image. -/
def decodeRecord (r : WeightedPhaseRecord) : QubitMatrix × Fin 2 :=
  (angularDecoder r.phase, r.outcome)

def recordReadout (r : WeightedPhaseRecord) : QubitMatrix :=
  selectedReadout r.outcome

theorem encode_records_weight (x : AngularOccurrence) :
    (encodeOccurrence x).weight = reflectionWeight x.1.val := rfl

theorem encode_records_phase (x : AngularOccurrence) :
    (encodeOccurrence x).phase = phaseReading x.1.val := rfl

theorem encode_records_outcome (x : AngularOccurrence) :
    (encodeOccurrence x).outcome = x.2 := rfl

theorem decode_encode_occurrence (x : AngularOccurrence) :
    decodeRecord (encodeOccurrence x) = (x.1.val, x.2) := by
  rcases x.1.property with ⟨θ, hθ⟩
  change (angularDecoder (phaseReading x.1.val), x.2) = (x.1.val, x.2)
  rw [hθ, angular_family_reconstructed_from_one_selected_face]

theorem decode_encode_form (x : AngularOccurrence) :
    (decodeRecord (encodeOccurrence x)).1 = x.1.val :=
  congrArg Prod.fst (decode_encode_occurrence x)

theorem decode_encode_outcome (x : AngularOccurrence) :
    (decodeRecord (encodeOccurrence x)).2 = x.2 := rfl

theorem encode_occurrence_injective : Function.Injective encodeOccurrence := by
  intro x y h
  have hd := congrArg decodeRecord h
  rw [decode_encode_occurrence, decode_encode_occurrence] at hd
  apply Prod.ext
  · exact Subtype.ext (congrArg Prod.fst hd)
  · exact congrArg (fun z : QubitMatrix × Fin 2 => z.2) hd

theorem decoded_form_is_admissible (r : WeightedPhaseRecord)
    (h : ∃ x : AngularOccurrence, encodeOccurrence x = r) :
    ∃ θ : ℝ, (decodeRecord r).1 = angFamily θ := by
  rcases h with ⟨x, rfl⟩
  rw [decode_encode_form]
  exact x.1.property

theorem record_round_trip_on_admissible_image (r : WeightedPhaseRecord)
    (h : ∃ x : AngularOccurrence, encodeOccurrence x = r) :
    readRecord (decodeRecord r).1 (decodeRecord r).2 = r := by
  rcases h with ⟨x, rfl⟩
  rw [decode_encode_occurrence]
  rfl

def selectionRecord (p : ℝ) (outcome : Fin 2) : WeightedPhaseRecord :=
  ⟨p, phaseReading (Smat (selectionAngle p)), outcome⟩

theorem selection_record_has_correct_weight {p : ℝ}
    (h0 : 0 ≤ p) (h1 : p ≤ 1) (outcome : Fin 2) :
    readRecord (Smat (selectionAngle p)) outcome = selectionRecord p outcome := by
  have hw : reflectionWeight (Smat (selectionAngle p)) = p :=
    (the_selection_opens_the_boundary h0 h1).1
  simp only [readRecord, selectionRecord, hw]

theorem selection_record_reconstructs_boundary (p : ℝ) (outcome : Fin 2) :
    decodeRecord (selectionRecord p outcome) = (Smat (selectionAngle p), outcome) := by
  change (angularDecoder (phaseReading (Smat (selectionAngle p))), outcome) = _
  rw [← angular_form_is_the_boundary_s_matrix]
  rw [angular_family_reconstructed_from_one_selected_face]

theorem selection_record_is_admissible {p : ℝ}
    (h0 : 0 ≤ p) (h1 : p ≤ 1) (outcome : Fin 2) :
    ∃ x : AngularOccurrence, encodeOccurrence x = selectionRecord p outcome := by
  refine ⟨(⟨Smat (selectionAngle p),
    ⟨selectionAngle p, (angular_form_is_the_boundary_s_matrix _).symm⟩⟩, outcome), ?_⟩
  exact selection_record_has_correct_weight h0 h1 outcome

def fairRecord (outcome : Fin 2) : WeightedPhaseRecord :=
  selectionRecord (1 / 2) outcome

theorem fair_records_share_weight_and_phase :
    (fairRecord 0).weight = (fairRecord 1).weight ∧
    (fairRecord 0).phase = (fairRecord 1).phase := ⟨rfl, rfl⟩

theorem fair_records_share_angle :
    selectionAngle (fairRecord 0).weight = Real.pi / 4 ∧
    selectionAngle (fairRecord 1).weight = Real.pi / 4 :=
  ⟨fair_selection_opens_forty_five, fair_selection_opens_forty_five⟩

theorem fair_records_are_distinct : fairRecord 0 ≠ fairRecord 1 := by
  intro h
  have he := congrArg WeightedPhaseRecord.outcome h
  change (0 : Fin 2) = 1 at he
  exact zero_ne_one he

theorem fair_record_readouts_are_distinct :
    recordReadout (fairRecord 0) ≠ recordReadout (fairRecord 1) := by
  simpa [recordReadout, fairRecord, selectionRecord, selectedReadout] using
    distinct_readout_fixed_points.2.2

theorem fair_record_has_canonical_branch_weight (outcome : Fin 2) :
    branchWeight plusDensity outcome = ((fairRecord outcome).weight : ℂ) := by
  change branchWeight plusDensity outcome = (((1 / 2 : ℝ)) : ℂ)
  rw [(fair_branch_weights outcome).1]
  norm_num

theorem fair_record_reconstructs_canonical_unnormalized_branch (outcome : Fin 2) :
    ((fairRecord outcome).weight : ℂ) • recordReadout (fairRecord outcome) =
      unnormalizedBranch plusDensity outcome := by
  rw [selective_branch_formula, fair_record_has_canonical_branch_weight]
  rfl

theorem fair_record_reconstructs_normalized_readout (outcome : Fin 2) :
    (branchWeight plusDensity outcome)⁻¹ • unnormalizedBranch plusDensity outcome =
      recordReadout (fairRecord outcome) := by
  apply normalized_branch_requires_nonzero_weight
  rw [(fair_branch_weights outcome).1]
  norm_num

theorem forgetting_fair_record_outcome_loses_distinction :
    (fairRecord 0).weight = (fairRecord 1).weight ∧
    (fairRecord 0).phase = (fairRecord 1).phase ∧
    fairRecord 0 ≠ fairRecord 1 :=
  ⟨rfl, rfl, fair_records_are_distinct⟩

/-- Exact record decoding is compatible with irreversibility of the reduction. -/
theorem angular_record_exactness_does_not_invert_reduction :
    Function.Injective encodeOccurrence ∧
    ¬ ∃ R : QubitMatrix → QubitMatrix, Function.LeftInverse R qubitReduction :=
  ⟨encode_occurrence_injective, qubit_reduction_no_inverse⟩


/-- Compatibility between a record and the weight of a specified modeled branch. -/
def recordMatchesBranch (A : QubitMatrix) (r : WeightedPhaseRecord) : Prop :=
  branchWeight A r.outcome = (r.weight : ℂ)

theorem matching_record_reconstructs_unnormalized_branch (A : QubitMatrix)
    (r : WeightedPhaseRecord) (h : recordMatchesBranch A r) :
    (r.weight : ℂ) • recordReadout r = unnormalizedBranch A r.outcome := by
  rw [selective_branch_formula, h]
  rfl

theorem matching_nonzero_record_reconstructs_normalized_branch (A : QubitMatrix)
    (r : WeightedPhaseRecord) (h : recordMatchesBranch A r) (hw : r.weight ≠ 0) :
    (branchWeight A r.outcome)⁻¹ • unnormalizedBranch A r.outcome = recordReadout r := by
  apply normalized_branch_requires_nonzero_weight
  rw [h]
  exact_mod_cast hw

theorem matching_zero_record_has_zero_branch (A : QubitMatrix)
    (r : WeightedPhaseRecord) (h : recordMatchesBranch A r) (hw : r.weight = 0) :
    unnormalizedBranch A r.outcome = 0 := by
  apply zero_weight_is_no_normalized_branch
  rw [h, hw]
  norm_num

#print axioms AngularForm
#print axioms AngularOccurrence
#print axioms WeightedPhaseRecord
#print axioms reflectionWeight
#print axioms readRecord
#print axioms encodeOccurrence
#print axioms decodeRecord
#print axioms recordReadout
#print axioms encode_records_weight
#print axioms encode_records_phase
#print axioms encode_records_outcome
#print axioms decode_encode_occurrence
#print axioms decode_encode_form
#print axioms decode_encode_outcome
#print axioms encode_occurrence_injective
#print axioms decoded_form_is_admissible
#print axioms record_round_trip_on_admissible_image
#print axioms selectionRecord
#print axioms selection_record_has_correct_weight
#print axioms selection_record_reconstructs_boundary
#print axioms selection_record_is_admissible
#print axioms fairRecord
#print axioms fair_records_share_weight_and_phase
#print axioms fair_records_share_angle
#print axioms fair_records_are_distinct
#print axioms fair_record_readouts_are_distinct
#print axioms fair_record_has_canonical_branch_weight
#print axioms fair_record_reconstructs_canonical_unnormalized_branch
#print axioms fair_record_reconstructs_normalized_readout
#print axioms forgetting_fair_record_outcome_loses_distinction
#print axioms angular_record_exactness_does_not_invert_reduction
#print axioms recordMatchesBranch
#print axioms matching_record_reconstructs_unnormalized_branch
#print axioms matching_nonzero_record_reconstructs_normalized_branch
#print axioms matching_zero_record_has_zero_branch

end
end ChatgptAudit.SelectionRecord
