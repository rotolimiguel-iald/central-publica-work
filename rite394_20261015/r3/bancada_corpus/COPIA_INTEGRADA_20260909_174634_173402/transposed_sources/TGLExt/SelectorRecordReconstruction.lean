import TGLExt.CanonicalSelectorBorn
import TGLExt.SelectedGravitationalAtlas

set_option autoImplicit false
set_option maxHeartbeats 900000
namespace ChatgptAudit.SelectorRecord
open TGLExt Set Filter Topology ChatgptAudit.SelectorBorn ChatgptAudit.SelectedAtlas
  ChatgptAudit.GravitationalRecord ChatgptAudit.AngularTensorCodec
  ChatgptAudit.GeneralMetric ChatgptAudit.GeneralClausius ChatgptAudit.Micro021
noncomputable section
variable {U : Set Coordinate4}

theorem selector_preserves_born_weight (x : ellTwo) :
    bornWeight (ialdSelector x)=bornWeight x := by
  simp only [bornWeight,iald_is_idempotent]

def canonicalBornIALD : IALDState ellTwo ℝ where
  recognize := ialdSelector
  read := bornWeight
  recursive := iald_is_idempotent
  identity := selector_preserves_born_weight

def recordVector [Nonempty U] (t : ℝ) (R : GravitationalResponseRecord U) : ellTwo :=
  scalarPreparation (recordCharacter t R)

def selectorCharacterReading (x : ellTwo) : ℝ := decodeScalar (bornWeight x)

theorem selector_character_reading_preserved (x : ellTwo) :
    selectorCharacterReading (ialdSelector x)=selectorCharacterReading x := by
  rw [selectorCharacterReading,selector_preserves_born_weight]
  rfl

theorem record_vector_normalized [Nonempty U] (t : ℝ)
    (R : GravitationalResponseRecord U) : ‖recordVector t R‖=1 :=
  scalar_preparation_normalized _

theorem record_vector_born_interior [Nonempty U] (t : ℝ)
    (R : GravitationalResponseRecord U) :
    0 < bornWeight (recordVector t R) ∧ bornWeight (recordVector t R) < 1 :=
  born_weight_interior _

theorem selector_reads_record_character [Nonempty U] (t : ℝ)
    (R : GravitationalResponseRecord U) :
    selectorCharacterReading (recordVector t R)=recordCharacter t R :=
  born_weight_decodes_scalar _

theorem selected_vector_reads_record_character [Nonempty U] (t : ℝ)
    (R : GravitationalResponseRecord U) :
    selectorCharacterReading (ialdSelector (recordVector t R))=recordCharacter t R := by
  rw [selector_character_reading_preserved,selector_reads_record_character]

theorem class_character_of_record [Nonempty U] (t : ℝ)
    (R : GravitationalResponseRecord U) :
    classCharacter t (classOfRecord R)=recordCharacter t R :=
  selection_preserves_character t R

theorem selected_record_reading_characterizes_class [Nonempty U] (t : ℝ) (ht : t ≠ 0)
    (R S : GravitationalResponseRecord U) :
    selectorCharacterReading (ialdSelector (recordVector t R))=
      selectorCharacterReading (ialdSelector (recordVector t S)) ↔
      classOfRecord R=classOfRecord S := by
  rw [selected_vector_reads_record_character,selected_vector_reads_record_character]
  exact record_character_same_iff t ht R S

def operatorCharacter [Nonempty U] (t : ℝ)
    (R : GravitationalResponseRecord U) : CharacterImage U t :=
  ⟨selectorCharacterReading (ialdSelector (recordVector t R)),
    ⟨classOfRecord R,by rw [class_character_of_record,selected_vector_reads_record_character]⟩⟩

theorem operator_character_eq [Nonempty U] (t : ℝ)
    (R : GravitationalResponseRecord U) :
    operatorCharacter t R=
      (⟨classCharacter t (classOfRecord R),⟨classOfRecord R,rfl⟩⟩ : CharacterImage U t) := by
  apply Subtype.ext
  exact (selected_vector_reads_record_character t R).trans (class_character_of_record t R).symm

theorem selector_reconstructs_metric_and_source [Nonempty U] (t : ℝ) (ht : t ≠ 0)
    (R : GravitationalResponseRecord U) :
    let D := reconstructedRecord (operatorCharacter t R)
    EqOn (recordMetric D) (recordMetric R) U ∧ EqOn (recordSource D) (recordSource R) U := by
  rw [operator_character_eq]
  exact character_reconstructs_metric_and_source t ht R

theorem normalized_selected_records_all_agree [Nonempty U] (t : ℝ)
    (R S : GravitationalResponseRecord U) :
    normalizedSelected (recordVector t R)=normalizedSelected (recordVector t S) :=
  normalized_selected_scalar_forgets_input _ _

theorem selector_reconstructs_einstein_from_area [Nonempty U]
    (t : ℝ) (ht : t ≠ 0) (hU : IsOpen U) (hconn : IsPreconnected U)
    (R : GravitationalResponseRecord U)
    (screens : MetricScreenFamily U (recordMetric R)) (eta : ℝ) (heta : eta ≠ 0)
    (hd : ∀ x ∈ U, ∀ j, tensorFieldDivergence (metricInverse (recordMetric R))
      (leviCivitaField (recordMetric R) (metricInverse (recordMetric R))) (recordSource R) x j=0)
    (harea : ∀ x (hx : x ∈ U) d (hv : d ≠ 0) (hn : tensorQuad (recordMetric R x) d=0),
      Tendsto (fun tau => microscopicAreaError (ChatgptAudit.UnifiedRecorded.unifiedPreparation R x d) eta
        (inducedArea (recordMetric R) (screens x hx d hv hn).curve
          (screens x hx d hv hn).screen.vectors) tau/tau^2) (𝓝[<] (0 : ℝ)) (𝓝 0)) :
    let D := reconstructedRecord (operatorCharacter t R)
    ∃ cosmological : ℝ, ∀ x ∈ U,
      geometricEinsteinTensor (recordMetric D) (metricInverse (recordMetric D))
        (leviCivitaField (recordMetric D) (metricInverse (recordMetric D))) x +
        cosmological • recordMetric D x=(2*Real.pi/eta) • recordSource D x := by
  rw [operator_character_eq]
  exact character_reconstructs_einstein_from_area t ht hU hconn R screens eta heta hd harea

#print axioms selector_preserves_born_weight
#print axioms canonicalBornIALD
#print axioms recordVector
#print axioms selectorCharacterReading
#print axioms selector_character_reading_preserved
#print axioms record_vector_normalized
#print axioms record_vector_born_interior
#print axioms selector_reads_record_character
#print axioms selected_vector_reads_record_character
#print axioms class_character_of_record
#print axioms selected_record_reading_characterizes_class
#print axioms operatorCharacter
#print axioms operator_character_eq
#print axioms selector_reconstructs_metric_and_source
#print axioms normalized_selected_records_all_agree
#print axioms selector_reconstructs_einstein_from_area
end
end ChatgptAudit.SelectorRecord
