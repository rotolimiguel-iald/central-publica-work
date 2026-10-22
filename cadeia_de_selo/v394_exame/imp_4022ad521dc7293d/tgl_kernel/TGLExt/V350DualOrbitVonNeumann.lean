import TGLExt.V350FibreVonNeumann
import TGLExt.V350DualOrbitStrongLimits

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem dualCharacterField_lift_star (a : ℝ) :
    star (operatorFieldLift (dualCharacterField (H := H) a)) =
      operatorFieldLift (dualCharacterField (-a)) := by
  symm
  apply operatorFieldLift_star
  intro s
  change characterMultiplier (H := H) ((-a)*s) = star (characterMultiplier (H := H) (a*s))
  rw [characterMultiplier_star,neg_mul]

theorem dualCharacterField_lift_mul (a b : ℝ) :
    operatorFieldLift (dualCharacterField (H := H) a) *
      operatorFieldLift (dualCharacterField b) = operatorFieldLift (dualCharacterField (a+b)) := by
  symm
  apply operatorFieldLift_mul
  intro s
  change characterMultiplier ((a+b)*s) = characterMultiplier (a*s) * characterMultiplier (b*s)
  rw [characterMultiplier_mul,add_mul]

theorem dualCharacterField_lift_zero :
    operatorFieldLift (dualCharacterField (H := H) 0) = 1 := by
  have he := operatorFieldLift_constant (dualCharacterField (H := H) 0) 1
    (fun s => by change characterMultiplier (0*s) = 1; rw [zero_mul,characterMultiplier_zero])
  exact he.trans fibre_one

def dualOrbitImplementer :
    unitary (RegularHilbert (RegularHilbert H) →L[ℂ] RegularHilbert (RegularHilbert H)) :=
  ⟨operatorFieldLift (dualCharacterField 1),by
    rw [Unitary.mem_iff]
    constructor <;>
      simp only [dualCharacterField_lift_star,dualCharacterField_lift_mul,
        neg_add_cancel,add_neg_cancel,dualCharacterField_lift_zero]⟩

def dualOrbitConjugation :
    (RegularHilbert (RegularHilbert H) →L[ℂ] RegularHilbert (RegularHilbert H)) ≃⋆ₐ[ℂ]
      (RegularHilbert (RegularHilbert H) →L[ℂ] RegularHilbert (RegularHilbert H)) :=
  Unitary.conjStarAlgAut ℂ _ (dualOrbitImplementer (H := H))

theorem dualOrbitConjugation_fibre (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    dualOrbitConjugation (H := H) (fibre A) = dualOrbitRepresentation A := by
  change operatorFieldLift (dualCharacterField (H := H) 1) * fibre A *
    star (operatorFieldLift (dualCharacterField (H := H) 1)) = _
  rw [dualCharacterField_lift_star,dualOrbit_factorization]

theorem dualOrbitConjugation_image (N : VonNeumannAlgebra (RegularHilbert H)) :
    dualOrbitConjugation (H := H) '' (fibre '' (N : Set (RegularHilbert H →L[ℂ] RegularHilbert H))) =
      dualOrbitRepresentation (H := H) '' (N : Set (RegularHilbert H →L[ℂ] RegularHilbert H)) := by
  rw [Set.image_image]
  congr 1
  funext A
  exact dualOrbitConjugation_fibre A

def dualOrbitVonNeumann (N : VonNeumannAlgebra (RegularHilbert H)) :
    VonNeumannAlgebra (RegularHilbert (RegularHilbert H)) :=
  generatedAlgebra (dualOrbitRepresentation ''
    (N : Set (RegularHilbert H →L[ℂ] RegularHilbert H)))

theorem mem_dualOrbitVonNeumann_iff (N : VonNeumannAlgebra (RegularHilbert H))
    (B : RegularHilbert (RegularHilbert H) →L[ℂ] RegularHilbert (RegularHilbert H)) :
    B ∈ dualOrbitVonNeumann (H := H) N ↔ ∃ A ∈ N, B = dualOrbitRepresentation (H := H) A := by
  constructor
  · intro hB
    have ht := generated_transport (dualOrbitConjugation (H := H))
      (fibre '' (N : Set (RegularHilbert H →L[ℂ] RegularHilbert H)))
      ((dualOrbitConjugation (H := H)).symm B)
    rw [StarAlgEquiv.apply_symm_apply,dualOrbitConjugation_image] at ht
    obtain ⟨A,hA,he⟩ := (mem_generated_fibre_iff N _).mp (ht.mp hB)
    refine ⟨A,hA,?_⟩
    have hx := congrArg (dualOrbitConjugation (H := H)) he
    simpa only [StarAlgEquiv.apply_symm_apply,dualOrbitConjugation_fibre] using hx
  · rintro ⟨A,hA,rfl⟩
    exact generator_mem ⟨A,hA,rfl⟩

#print axioms dualCharacterField_lift_star
#print axioms dualCharacterField_lift_mul
#print axioms dualCharacterField_lift_zero
#print axioms dualOrbitImplementer
#print axioms dualOrbitConjugation
#print axioms dualOrbitConjugation_fibre
#print axioms dualOrbitConjugation_image
#print axioms dualOrbitVonNeumann
#print axioms mem_dualOrbitVonNeumann_iff
end
end TGLV350.Regular
