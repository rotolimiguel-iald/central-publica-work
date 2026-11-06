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
import TGLExt.SelectionOutcomeRecord

set_option autoImplicit false
set_option maxHeartbeats 600000

namespace ChatgptAudit.ScatteringRecord
open Matrix Complex TGLExt ChatgptAudit.SelectionAngle ChatgptAudit.SelectionRecord
  ChatgptAudit.Collapse057
open scoped ComplexOrder
noncomputable section

/-- The outgoing column of the canonical S matrix for the incident channel e1. -/
def outgoingColumn (θ : ℝ) : Matrix (Fin 2) (Fin 1) ℂ :=
  fun i _ => (Smat θ).mulVec e1 i

theorem canonical_density_is_outgoing_outer_product (θ : ℝ) :
    rhoOut θ = outgoingColumn θ * (outgoingColumn θ)ᴴ := by
  rw [rhoOut_eq]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [outgoingColumn, Matrix.mul_apply, Matrix.conjTranspose_apply,
      Smat_transmission, Smat_reflection, pow_two] <;>
      simp only [← Complex.ofReal_cos, ← Complex.ofReal_sin, Complex.conj_ofReal, true_or]

theorem canonical_scattering_density_positive (θ : ℝ) :
    (rhoOut θ).PosSemidef := by
  rw [canonical_density_is_outgoing_outer_product]
  exact Matrix.posSemidef_self_mul_conjTranspose (outgoingColumn θ)

/-- A genuine member of the canonical positive trace-one state type. -/
def scatteringDensity (θ : ℝ) : QubitDensity :=
  ⟨rhoOut θ, canonical_scattering_density_positive θ, rhoOut_trace θ⟩

/-- The selected probability is transmission for label 0, reflection for label 1. -/
def selectedProbability (p : ℝ) (outcome : Fin 2) : ℝ :=
  if outcome = 0 then 1 - p else p

def scatteringRecord (p : ℝ) (outcome : Fin 2) : WeightedPhaseRecord :=
  ⟨selectedProbability p outcome, phaseReading (Smat (selectionAngle p)), outcome⟩

/-- Reflection weight can be recovered from a branch weight only with its label. -/
def recoveredReflectionWeight (r : WeightedPhaseRecord) : ℝ :=
  if r.outcome = 0 then 1 - r.weight else r.weight

theorem selected_probabilities_normalized (p : ℝ) :
    selectedProbability p 0 + selectedProbability p 1 = 1 := by
  simp [selectedProbability]

theorem selected_probability_range {p : ℝ} (h0 : 0 ≤ p) (h1 : p ≤ 1)
    (outcome : Fin 2) :
    0 ≤ selectedProbability p outcome ∧ selectedProbability p outcome ≤ 1 := by
  fin_cases outcome <;> simp [selectedProbability] <;> constructor <;> linarith

theorem scattering_record_recovers_reflection_weight (p : ℝ) (outcome : Fin 2) :
    recoveredReflectionWeight (scatteringRecord p outcome) = p := by
  fin_cases outcome <;> simp [recoveredReflectionWeight, scatteringRecord, selectedProbability]

theorem scattering_record_decodes_form_and_label (p : ℝ) (outcome : Fin 2) :
    decodeRecord (scatteringRecord p outcome) = (Smat (selectionAngle p), outcome) := by
  change (angularDecoder (phaseReading (Smat (selectionAngle p))), outcome) = _
  rw [← angular_form_is_the_boundary_s_matrix]
  rw [angular_family_reconstructed_from_one_selected_face]

theorem canonical_branch_weight_is_selected_probability {p : ℝ}
    (h0 : 0 ≤ p) (h1 : p ≤ 1) (outcome : Fin 2) :
    branchWeight (rhoOut (selectionAngle p)) outcome =
      (selectedProbability p outcome : ℂ) := by
  fin_cases outcome
  · change rhoOut (selectionAngle p) 0 0 = ((1 - p : ℝ) : ℂ)
    rw [rhoOut_zero_zero]
    exact_mod_cast selection_angle_transmission h0 h1
  · change rhoOut (selectionAngle p) 1 1 = (p : ℂ)
    rw [rhoOut_one_one]
    exact_mod_cast selection_angle_reflection h0 h1

theorem scattering_record_matches_canonical_branch {p : ℝ}
    (h0 : 0 ≤ p) (h1 : p ≤ 1) (outcome : Fin 2) :
    recordMatchesBranch (scatteringDensity (selectionAngle p)).val
      (scatteringRecord p outcome) :=
  canonical_branch_weight_is_selected_probability h0 h1 outcome

theorem scattering_record_reconstructs_branch {p : ℝ}
    (h0 : 0 ≤ p) (h1 : p ≤ 1) (outcome : Fin 2) :
    ((scatteringRecord p outcome).weight : ℂ) • recordReadout (scatteringRecord p outcome) =
      unnormalizedBranch (rhoOut (selectionAngle p)) outcome :=
  by
    rw [selective_branch_formula, canonical_branch_weight_is_selected_probability h0 h1 outcome]
    rfl

theorem scattering_record_normalizes_nonzero_branch {p : ℝ}
    (h0 : 0 ≤ p) (h1 : p ≤ 1) (outcome : Fin 2)
    (hp : selectedProbability p outcome ≠ 0) :
    (branchWeight (rhoOut (selectionAngle p)) outcome)⁻¹ •
      unnormalizedBranch (rhoOut (selectionAngle p)) outcome =
        recordReadout (scatteringRecord p outcome) :=
  by
    apply normalized_branch_requires_nonzero_weight
    rw [canonical_branch_weight_is_selected_probability h0 h1 outcome]
    exact_mod_cast hp

theorem scattering_record_zero_weight_zero_branch {p : ℝ}
    (h0 : 0 ≤ p) (h1 : p ≤ 1) (outcome : Fin 2)
    (hp : selectedProbability p outcome = 0) :
    unnormalizedBranch (rhoOut (selectionAngle p)) outcome = 0 :=
  by
    apply zero_weight_is_no_normalized_branch
    rw [canonical_branch_weight_is_selected_probability h0 h1 outcome, hp]
    norm_num

theorem fair_scattering_records_equal_fair_records (outcome : Fin 2) :
    scatteringRecord (1 / 2) outcome = fairRecord outcome := by
  fin_cases outcome <;> norm_num [scatteringRecord, selectedProbability, fairRecord, selectionRecord]

theorem fair_scattering_labels_remain_distinct :
    scatteringRecord (1 / 2) 0 ≠ scatteringRecord (1 / 2) 1 := by
  rw [fair_scattering_records_equal_fair_records, fair_scattering_records_equal_fair_records]
  exact fair_records_are_distinct

theorem scattering_record_parameters_are_recovered (p : ℝ) (outcome : Fin 2) :
    (recoveredReflectionWeight (scatteringRecord p outcome),
      (scatteringRecord p outcome).outcome) = (p, outcome) := by
  rw [scattering_record_recovers_reflection_weight]
  rfl

theorem scattering_record_separates_parameters {p q : ℝ} {i j : Fin 2}
    (h : scatteringRecord p i = scatteringRecord q j) : p = q ∧ i = j := by
  have hp := congrArg recoveredReflectionWeight h
  rw [scattering_record_recovers_reflection_weight,
    scattering_record_recovers_reflection_weight] at hp
  exact ⟨hp, congrArg WeightedPhaseRecord.outcome h⟩


/-- Scattering convention: weight is the selected channel probability, not always reflection. -/
def readScatteringRecord (A : QubitMatrix) (outcome : Fin 2) : WeightedPhaseRecord :=
  ⟨selectedProbability (reflectionWeight A) outcome, phaseReading A, outcome⟩

def encodeScatteringOccurrence (x : AngularOccurrence) : WeightedPhaseRecord :=
  readScatteringRecord x.1.val x.2

theorem scattering_decode_encode_occurrence (x : AngularOccurrence) :
    decodeRecord (encodeScatteringOccurrence x) = (x.1.val, x.2) := by
  rcases x.1.property with ⟨θ, hθ⟩
  change (angularDecoder (phaseReading x.1.val), x.2) = (x.1.val, x.2)
  rw [hθ, angular_family_reconstructed_from_one_selected_face]

theorem scattering_encode_injective : Function.Injective encodeScatteringOccurrence := by
  intro x y h
  have hd := congrArg decodeRecord h
  rw [scattering_decode_encode_occurrence, scattering_decode_encode_occurrence] at hd
  apply Prod.ext
  · exact Subtype.ext (congrArg Prod.fst hd)
  · exact congrArg (fun z : QubitMatrix × Fin 2 => z.2) hd

theorem read_scattering_record_on_boundary {p : ℝ}
    (h0 : 0 ≤ p) (h1 : p ≤ 1) (outcome : Fin 2) :
    readScatteringRecord (Smat (selectionAngle p)) outcome = scatteringRecord p outcome := by
  have hw : reflectionWeight (Smat (selectionAngle p)) = p :=
    (the_selection_opens_the_boundary h0 h1).1
  simp only [readScatteringRecord, scatteringRecord, hw]

theorem scattering_record_round_trip {p : ℝ}
    (h0 : 0 ≤ p) (h1 : p ≤ 1) (outcome : Fin 2) :
    readScatteringRecord (decodeRecord (scatteringRecord p outcome)).1
      (decodeRecord (scatteringRecord p outcome)).2 = scatteringRecord p outcome := by
  rw [scattering_record_decodes_form_and_label]
  exact read_scattering_record_on_boundary h0 h1 outcome

theorem scattering_record_round_trip_on_admissible_image (r : WeightedPhaseRecord)
    (h : ∃ x : AngularOccurrence, encodeScatteringOccurrence x = r) :
    readScatteringRecord (decodeRecord r).1 (decodeRecord r).2 = r := by
  rcases h with ⟨x, rfl⟩
  rw [scattering_decode_encode_occurrence]
  rfl

theorem weight_conventions_differ_at_pure_transmission :
    selectionRecord 0 0 ≠ scatteringRecord 0 0 := by
  intro h
  have hw := congrArg WeightedPhaseRecord.weight h
  norm_num [selectionRecord, scatteringRecord, selectedProbability] at hw


/-- On the prepared principal family, selected weight and label already determine the form. -/
def decodePrincipalScattering (r : WeightedPhaseRecord) : QubitMatrix × Fin 2 :=
  (Smat (selectionAngle (recoveredReflectionWeight r)), r.outcome)

theorem selected_weight_and_label_reconstruct_principal_form (p : ℝ) (outcome : Fin 2) :
    decodePrincipalScattering (scatteringRecord p outcome) =
      (Smat (selectionAngle p), outcome) := by
  unfold decodePrincipalScattering
  rw [scattering_record_recovers_reflection_weight]
  rfl

theorem phase_and_weight_decoders_agree_on_principal_record (p : ℝ) (outcome : Fin 2) :
    decodeRecord (scatteringRecord p outcome) =
      decodePrincipalScattering (scatteringRecord p outcome) := by
  rw [scattering_record_decodes_form_and_label,
    selected_weight_and_label_reconstruct_principal_form]

#print axioms outgoingColumn
#print axioms canonical_density_is_outgoing_outer_product
#print axioms canonical_scattering_density_positive
#print axioms scatteringDensity
#print axioms selectedProbability
#print axioms scatteringRecord
#print axioms recoveredReflectionWeight
#print axioms selected_probabilities_normalized
#print axioms selected_probability_range
#print axioms scattering_record_recovers_reflection_weight
#print axioms scattering_record_decodes_form_and_label
#print axioms canonical_branch_weight_is_selected_probability
#print axioms scattering_record_matches_canonical_branch
#print axioms scattering_record_reconstructs_branch
#print axioms scattering_record_normalizes_nonzero_branch
#print axioms scattering_record_zero_weight_zero_branch
#print axioms fair_scattering_records_equal_fair_records
#print axioms fair_scattering_labels_remain_distinct
#print axioms scattering_record_parameters_are_recovered
#print axioms scattering_record_separates_parameters
#print axioms readScatteringRecord
#print axioms encodeScatteringOccurrence
#print axioms scattering_decode_encode_occurrence
#print axioms scattering_encode_injective
#print axioms read_scattering_record_on_boundary
#print axioms scattering_record_round_trip
#print axioms scattering_record_round_trip_on_admissible_image
#print axioms weight_conventions_differ_at_pure_transmission
#print axioms decodePrincipalScattering
#print axioms selected_weight_and_label_reconstruct_principal_form
#print axioms phase_and_weight_decoders_agree_on_principal_record

end
end ChatgptAudit.ScatteringRecord
