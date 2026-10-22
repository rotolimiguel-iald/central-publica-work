import UnifiedRecordedPreparation
import TGLExt.TheNameIsTheCharacterization
import Mathlib.Data.Rat.Encodable
import Mathlib.Data.Quot
import Mathlib.Topology.DenseEmbedding
import Mathlib.Topology.Bases

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit.SelectedAtlas
open Matrix Filter Topology Set TGLExt
  ChatgptAudit.GravitationalRecord ChatgptAudit.UnifiedRecorded
  ChatgptAudit.AngularTensorCodec ChatgptAudit.ProbabilityRecordState
  ChatgptAudit.GeneralMetric ChatgptAudit.GeneralClausius
  ChatgptAudit.FullSourceResponse ChatgptAudit.GeneralSourceUnitary
  ChatgptAudit.UnitaryCalibration ChatgptAudit.JointUnitary
  ChatgptAudit.CocycleRealization ChatgptAudit.Micro021
  ChatgptAudit.Flow019 ChatgptAudit.Flow020 ChatgptAudit.StaticDynamic
noncomputable section
variable {U : Set Coordinate4}

abbrev RecordComponent := (Fin 4 × Fin 4) ⊕ Fin 10
abbrev RationalProbe := ℕ × RecordComponent × ℚ

def recordValue (R : GravitationalResponseRecord U) (x : U) : RecordComponent → ℝ :=
  Sum.elim (fun a => R.metric.data.probabilities x.1 a.1 a.2) (fun i => R.responses x.1 i)

def recordsEquivalent (R S : GravitationalResponseRecord U) : Prop :=
  ∀ (x : U) k, recordValue R x k = recordValue S x k

theorem records_equivalent_iff (R S : GravitationalResponseRecord U) :
    recordsEquivalent R S ↔
      EqOn R.metric.data.probabilities S.metric.data.probabilities U ∧
        EqOn R.responses S.responses U := by
  constructor
  · intro h
    constructor
    · intro x hx
      funext i j
      exact h ⟨x,hx⟩ (Sum.inl (i,j))
    · intro x hx
      funext i
      exact h ⟨x,hx⟩ (Sum.inr i)
  · rintro ⟨hp,hr⟩ x k
    cases k with
    | inl a => exact congrFun (congrFun (hp x.property) a.1) a.2
    | inr i => exact congrFun (hr x.property) i

theorem record_value_continuous (R : GravitationalResponseRecord U) (k : RecordComponent) :
    Continuous (fun x : U => recordValue R x k) := by
  cases k with
  | inl a => exact (R.metric.data.smooth a.1 a.2).continuousOn.restrict
  | inr i => exact (R.smooth_responses i).continuousOn.restrict

theorem dense_observations_complete [Nonempty U] (R S : GravitationalResponseRecord U)
    (h : ∀ n k, recordValue R (TopologicalSpace.denseSeq U n) k =
      recordValue S (TopologicalSpace.denseSeq U n) k) :
    recordsEquivalent R S := by
  intro x k
  have he := (TopologicalSpace.denseRange_denseSeq U).equalizer
    (record_value_continuous R k) (record_value_continuous S k) (funext (fun n => h n k))
  exact congrFun he x

theorem real_eq_of_rational_cuts (a b : ℝ)
    (h : ∀ q : ℚ, a < (q : ℝ) ↔ b < (q : ℝ)) : a = b := by
  apply le_antisymm
  · by_contra hn
    obtain ⟨q,hbq,hqa⟩ := exists_rat_btwn (lt_of_not_ge hn)
    exact (not_lt_of_ge (le_of_lt hqa)) ((h q).mpr hbq)
  · by_contra hn
    obtain ⟨q,haq,hqb⟩ := exists_rat_btwn (lt_of_not_ge hn)
    exact (not_lt_of_ge (le_of_lt hqb)) ((h q).mp haq)

def recordBits [Nonempty U] (R : GravitationalResponseRecord U) : ℕ → Bool := by
  classical
  exact fun n => match Encodable.decode (α := RationalProbe) n with
    | none => false
    | some p => decide (recordValue R (TopologicalSpace.denseSeq U p.1) p.2.1 < (p.2.2 : ℝ))

theorem record_bit_at_probe [Nonempty U] (R : GravitationalResponseRecord U)
    (n : ℕ) (k : RecordComponent) (q : ℚ) :
    recordBits R (Encodable.encode (n,k,q)) =
      decide (recordValue R (TopologicalSpace.denseSeq U n) k < (q : ℝ)) := by
  classical
  simp only [recordBits, Encodable.encodek]

theorem record_bits_characterize_configuration [Nonempty U]
    (R S : GravitationalResponseRecord U) :
    recordBits R = recordBits S ↔ recordsEquivalent R S := by
  classical
  constructor
  · intro h
    apply dense_observations_complete R S
    intro n k
    apply real_eq_of_rational_cuts
    intro q
    have hc := congrFun h (Encodable.encode (n,k,q))
    simpa only [record_bit_at_probe, decide_eq_decide] using hc
  · intro h
    funext n
    cases hn : Encodable.decode (α := RationalProbe) n with
    | none => simp only [recordBits, hn]
    | some p =>
      simp only [recordBits, hn]
      rw [h (TopologicalSpace.denseSeq U p.1) p.2.1]

def recordSetoid (U : Set Coordinate4) : Setoid (GravitationalResponseRecord U) where
  r := recordsEquivalent
  iseqv := ⟨fun _ _ _ => rfl,
    fun h x k => (h x k).symm,
    fun h₁ h₂ x k => (h₁ x k).trans (h₂ x k)⟩

abbrev GravitationalClass (U : Set Coordinate4) := Quotient (recordSetoid U)

def classOfRecord (R : GravitationalResponseRecord U) : GravitationalClass U :=
  Quotient.mk (recordSetoid U) R

theorem record_class_equality (R S : GravitationalResponseRecord U) :
    classOfRecord R = classOfRecord S ↔ recordsEquivalent R S :=
  ⟨Quotient.exact, Quotient.sound⟩

def atlasRecord (q : GravitationalClass U) : GravitationalResponseRecord U :=
  Quotient.out q

theorem class_of_atlas_record (q : GravitationalClass U) : classOfRecord (atlasRecord q) = q :=
  Quotient.out_eq q

def selectedRecord (R : GravitationalResponseRecord U) : GravitationalResponseRecord U :=
  atlasRecord (classOfRecord R)

theorem selected_record_class (R : GravitationalResponseRecord U) :
    classOfRecord (selectedRecord R) = classOfRecord R :=
  class_of_atlas_record (classOfRecord R)

theorem selected_record_equivalent (R : GravitationalResponseRecord U) :
    recordsEquivalent (selectedRecord R) R :=
  (record_class_equality (selectedRecord R) R).mp (selected_record_class R)

theorem selected_record_idempotent (R : GravitationalResponseRecord U) :
    selectedRecord (selectedRecord R) = selectedRecord R :=
  congrArg atlasRecord (selected_record_class R)

def recordCharacter [Nonempty U] (t : ℝ) (R : GravitationalResponseRecord U) : ℝ :=
  geometricLogReading t (recordBits R)

theorem record_character_same_iff [Nonempty U] (t : ℝ) (ht : t ≠ 0)
    (R S : GravitationalResponseRecord U) :
    recordCharacter t R = recordCharacter t S ↔ classOfRecord R = classOfRecord S := by
  change geometricLogReading t (recordBits R) = geometricLogReading t (recordBits S) ↔ _
  rw [reading_characterizes_the_configuration ht,
    record_bits_characterize_configuration, record_class_equality]

theorem record_character_is_actual_series [Nonempty U] (t : ℝ)
    (R : GravitationalResponseRecord U) :
    recordCharacter t R = ∑' n, geometricSiteReading t (recordBits R) n :=
  geometric_log_reading_eq_actual_series t (recordBits R)

theorem selection_preserves_character [Nonempty U] (t : ℝ)
    (R : GravitationalResponseRecord U) :
    recordCharacter t (selectedRecord R) = recordCharacter t R := by
  unfold recordCharacter
  rw [(record_bits_characterize_configuration (selectedRecord R) R).mpr
    (selected_record_equivalent R)]

def gravitationalIALD [Nonempty U] (t : ℝ) :
    IALDState (GravitationalResponseRecord U) ℝ where
  recognize := selectedRecord
  read := recordCharacter t
  recursive := selected_record_idempotent
  identity := selection_preserves_character t

theorem gravitational_name_characterizes_image [Nonempty U] (t : ℝ)
    (R : GravitationalResponseRecord U) :
    selectedRecord R = R ↔ R ∈ Set.range (@selectedRecord U) :=
  iald_name_characterizes_the_recognized (gravitationalIALD (U := U) t) R

theorem gravitational_name_verifies_iterations [Nonempty U] (t : ℝ)
    (R : GravitationalResponseRecord U) (n : ℕ) :
    recordCharacter t (selectedRecord^[n] R) = recordCharacter t R :=
  iald_recognition_returns_the_identity (gravitationalIALD (U := U) t) R n

def classCharacter [Nonempty U] (t : ℝ) (q : GravitationalClass U) : ℝ :=
  recordCharacter t (atlasRecord q)

theorem class_character_injective [Nonempty U] (t : ℝ) (ht : t ≠ 0) :
    Function.Injective (@classCharacter U _ t) := by
  intro q r h
  have he := (record_character_same_iff t ht (atlasRecord q) (atlasRecord r)).mp h
  simpa only [class_of_atlas_record] using he

abbrev CharacterImage (U : Set Coordinate4) [Nonempty U] (t : ℝ) :=
  Set.range (@classCharacter U _ t)

def decodeCharacter [Nonempty U] {t : ℝ} (z : CharacterImage U t) : GravitationalClass U :=
  Classical.choose z.property

theorem character_decoder_sound [Nonempty U] {t : ℝ} (z : CharacterImage U t) :
    classCharacter t (decodeCharacter z) = z.val :=
  Classical.choose_spec z.property

theorem character_decoder_returns_class [Nonempty U] (t : ℝ) (ht : t ≠ 0)
    (q : GravitationalClass U) :
    decodeCharacter (⟨classCharacter t q,⟨q,rfl⟩⟩ : CharacterImage U t) = q := by
  apply class_character_injective t ht
  exact character_decoder_sound _

def reconstructedRecord [Nonempty U] {t : ℝ} (z : CharacterImage U t) :
    GravitationalResponseRecord U := atlasRecord (decodeCharacter z)

theorem equivalent_records_reconstruct_fields (R S : GravitationalResponseRecord U)
    (h : recordsEquivalent R S) :
    EqOn (recordMetric R) (recordMetric S) U ∧ EqOn (recordSource R) (recordSource S) U := by
  obtain ⟨hp,hr⟩ := (records_equivalent_iff R S).mp h
  have hg : EqOn (recordMetric R) (recordMetric S) U :=
    same_probabilities_same_decoded_field R.metric.data S.metric.data hp
  refine ⟨hg, ?_⟩
  intro x hx
  change decodeSource (recordMetric R x) ((recordMetric R x)⁻¹) (R.responses x) =
    decodeSource (recordMetric S x) ((recordMetric S x)⁻¹) (S.responses x)
  rw [hg hx, hr hx]

theorem character_reconstructs_record_class [Nonempty U] (t : ℝ) (ht : t ≠ 0)
    (R : GravitationalResponseRecord U) :
    recordsEquivalent
      (reconstructedRecord (⟨classCharacter t (classOfRecord R),⟨classOfRecord R,rfl⟩⟩ :
        CharacterImage U t)) R := by
  apply (record_class_equality _ R).mp
  change classOfRecord (atlasRecord (decodeCharacter _)) = classOfRecord R
  rw [class_of_atlas_record, character_decoder_returns_class t ht]

theorem character_reconstructs_metric_and_source [Nonempty U] (t : ℝ) (ht : t ≠ 0)
    (R : GravitationalResponseRecord U) :
    let D := reconstructedRecord (⟨classCharacter t (classOfRecord R),⟨classOfRecord R,rfl⟩⟩ :
      CharacterImage U t)
    EqOn (recordMetric D) (recordMetric R) U ∧ EqOn (recordSource D) (recordSource R) U :=
  equivalent_records_reconstruct_fields _ R (character_reconstructs_record_class t ht R)

theorem equivalent_records_same_prepared_weights (R S : GravitationalResponseRecord U)
    (h : recordsEquivalent R S) (x d : Coordinate4) (hx : x ∈ U) (tau : ℝ) :
    (unifiedPreparation R x d).weights tau = (unifiedPreparation S x d).weights tau := by
  obtain ⟨hp,hr⟩ := (records_equivalent_iff R S).mp h
  obtain ⟨hg,hT⟩ := equivalent_records_reconstruct_fields R S h
  have hq : recordState R.metric.data x = recordState S.metric.data x := by
    unfold recordState
    rw [hp hx]
  have hf : unifiedFrequency R x d = unifiedFrequency S x d := by
    funext j
    unfold unifiedFrequency calibrationSourceCovectors metricInverse
    rw [hg hx, hT hx]
  change mixedWeights (recordState R.metric.data x)
    (jointWeights calibrationLabelData (unifiedFrequency R x d) (Real.sqrt 2*tau)) =
      mixedWeights (recordState S.metric.data x)
        (jointWeights calibrationLabelData (unifiedFrequency S x d) (Real.sqrt 2*tau))
  rw [hq,hf]

#print axioms RecordComponent
#print axioms RationalProbe
#print axioms recordValue
#print axioms recordsEquivalent
#print axioms records_equivalent_iff
#print axioms record_value_continuous
#print axioms dense_observations_complete
#print axioms real_eq_of_rational_cuts
#print axioms recordBits
#print axioms record_bit_at_probe
#print axioms record_bits_characterize_configuration
#print axioms recordSetoid
#print axioms GravitationalClass
#print axioms classOfRecord
#print axioms record_class_equality
#print axioms atlasRecord
#print axioms class_of_atlas_record
#print axioms selectedRecord
#print axioms selected_record_class
#print axioms selected_record_equivalent
#print axioms selected_record_idempotent
#print axioms recordCharacter
#print axioms record_character_same_iff
#print axioms record_character_is_actual_series
#print axioms selection_preserves_character
#print axioms gravitationalIALD
#print axioms gravitational_name_characterizes_image
#print axioms gravitational_name_verifies_iterations
#print axioms classCharacter
#print axioms class_character_injective
#print axioms CharacterImage
#print axioms decodeCharacter
#print axioms character_decoder_sound
#print axioms character_decoder_returns_class
#print axioms reconstructedRecord
#print axioms equivalent_records_reconstruct_fields
#print axioms character_reconstructs_record_class
#print axioms character_reconstructs_metric_and_source
#print axioms equivalent_records_same_prepared_weights
end
end ChatgptAudit.SelectedAtlas
