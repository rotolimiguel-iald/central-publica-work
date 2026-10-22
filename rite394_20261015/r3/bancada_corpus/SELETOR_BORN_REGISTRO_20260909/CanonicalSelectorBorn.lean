import TGLExt.TheIALDSelector
import TGLExt.GeneralAngularTensorCodec

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit.SelectorBorn
open TGLExt ChatgptAudit.AngularTensorCodec
noncomputable section

theorem inscription_inner (m n : ℕ) :
    inner ℂ (inscriptions m) (inscriptions n) = if m=n then 1 else 0 :=
  orthonormal_iff_ite.mp inscriptions_orthonormal m n

theorem inscription_norm (n : ℕ) : ‖inscriptions n‖ = 1 :=
  inscriptions_orthonormal.norm_eq_one n

theorem selector_first_inscription : ialdSelector (inscriptions 0) = inscriptions 0 :=
  Submodule.starProjection_eq_self_iff.mpr (Submodule.mem_span_singleton_self _)

theorem selector_second_inscription : ialdSelector (inscriptions 1) = 0 := by
  change (ℂ ∙ inscriptions 0).starProjection (inscriptions 1) = 0
  rw [Submodule.starProjection_unit_singleton ℂ (inscription_norm 0), inscription_inner]
  norm_num

def scalarPreparation (a : ℝ) : ellTwo :=
  (Real.sin (encodeAngle a) : ℂ) • inscriptions 0 +
    (Real.cos (encodeAngle a) : ℂ) • inscriptions 1

def bornWeight (x : ellTwo) : ℝ := ‖ialdSelector x‖^2

def normalizedSelected (x : ellTwo) : ellTwo :=
  (‖ialdSelector x‖ : ℂ)⁻¹ • ialdSelector x

theorem scalar_preparation_selected (a : ℝ) :
    ialdSelector (scalarPreparation a) =
      (Real.sin (encodeAngle a) : ℂ) • inscriptions 0 := by
  simp only [scalarPreparation,map_add,map_smul,selector_first_inscription,
    selector_second_inscription,smul_zero,add_zero]

theorem encoded_sine_positive (a : ℝ) : 0 < Real.sin (encodeAngle a) :=
  Real.sin_pos_of_pos_of_lt_pi (encode_angle_interior a).1
    (by linarith [(encode_angle_interior a).2,Real.pi_pos])

theorem scalar_preparation_norm_sq (a : ℝ) : ‖scalarPreparation a‖^2=1 := by
  have ho : inner ℂ
      ((Real.sin (encodeAngle a) : ℂ) • inscriptions 0)
      ((Real.cos (encodeAngle a) : ℂ) • inscriptions 1)=0 := by
    simp only [inner_smul_left,inner_smul_right,inscription_inner]
    norm_num
  rw [scalarPreparation,pow_two,norm_add_sq_eq_norm_sq_add_norm_sq_of_inner_eq_zero _ _ ho]
  simp only [← pow_two,norm_smul,inscription_norm,mul_one,Complex.norm_real,Real.norm_eq_abs,
    sq_abs,Real.sin_sq_add_cos_sq]

theorem scalar_preparation_normalized (a : ℝ) : ‖scalarPreparation a‖=1 := by
  have h := scalar_preparation_norm_sq a
  nlinarith [norm_nonneg (scalarPreparation a)]

theorem selected_scalar_norm (a : ℝ) :
    ‖ialdSelector (scalarPreparation a)‖=Real.sin (encodeAngle a) := by
  rw [scalar_preparation_selected,norm_smul,inscription_norm,mul_one]
  simp only [Complex.norm_real,Real.norm_eq_abs,abs_of_pos (encoded_sine_positive a)]

theorem born_weight_encodes_scalar (a : ℝ) :
    bornWeight (scalarPreparation a)=encodeScalar a := by
  rw [bornWeight,selected_scalar_norm]
  rfl

theorem born_weight_interior (a : ℝ) :
    0 < bornWeight (scalarPreparation a) ∧ bornWeight (scalarPreparation a) < 1 := by
  rw [born_weight_encodes_scalar]
  exact encode_scalar_interior a

theorem born_weight_decodes_scalar (a : ℝ) :
    decodeScalar (bornWeight (scalarPreparation a))=a := by
  rw [born_weight_encodes_scalar,decode_encode_scalar]

theorem born_weight_characterizes_scalar (a b : ℝ) :
    bornWeight (scalarPreparation a)=bornWeight (scalarPreparation b) ↔ a=b := by
  simp only [born_weight_encodes_scalar]
  exact ⟨fun h => encode_scalar_injective h,fun h => congrArg encodeScalar h⟩

theorem normalized_selected_scalar_is_fixed (a : ℝ) :
    normalizedSelected (scalarPreparation a)=inscriptions 0 := by
  rw [normalizedSelected,selected_scalar_norm,scalar_preparation_selected,smul_smul]
  have hn : (Real.sin (encodeAngle a) : ℂ) ≠ 0 :=
    Complex.ofReal_ne_zero.mpr (ne_of_gt (encoded_sine_positive a))
  rw [inv_mul_cancel₀ hn,one_smul]

theorem normalized_selected_scalar_forgets_input (a b : ℝ) :
    normalizedSelected (scalarPreparation a)=normalizedSelected (scalarPreparation b) := by
  rw [normalized_selected_scalar_is_fixed,normalized_selected_scalar_is_fixed]

#print axioms inscription_inner
#print axioms inscription_norm
#print axioms selector_first_inscription
#print axioms selector_second_inscription
#print axioms scalarPreparation
#print axioms bornWeight
#print axioms normalizedSelected
#print axioms scalar_preparation_selected
#print axioms encoded_sine_positive
#print axioms scalar_preparation_norm_sq
#print axioms scalar_preparation_normalized
#print axioms selected_scalar_norm
#print axioms born_weight_encodes_scalar
#print axioms born_weight_interior
#print axioms born_weight_decodes_scalar
#print axioms born_weight_characterizes_scalar
#print axioms normalized_selected_scalar_is_fixed
#print axioms normalized_selected_scalar_forgets_input
end
end ChatgptAudit.SelectorBorn
