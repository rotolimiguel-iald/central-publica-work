-- SONDA C3 do auditor: T7' (second_face_iff_leak) prova-se SEM importar TGLExt.Fundacao.
import TGLExt.TheAxiomAndTheFalseWitness

set_option autoImplicit false
namespace AuditorRepro2
open TGLExt.TheAxiomAndTheFalseWitness

theorem second_face_iff_leak_without_fundacao {A : Type*} [Ring A] [Algebra ℂ A] {P : A}
    (hP : IsIdempotentElem P) (hne : (1 : A) - P ≠ 0) (s : ℝ) :
    axiomFlow P s * (1 - P) = 1 - P ↔ s = 0 := by
  rw [axiomFlow_gradient hP]
  constructor
  · intro h
    have h2 : (((Real.exp (-s) : ℝ) : ℂ) - 1) • ((1 : A) - P) = 0 := by
      rw [sub_smul, one_smul, h, sub_self]
    rcases smul_eq_zero.mp h2 with hc | hc
    · have hc' : ((Real.exp (-s) : ℝ) : ℂ) = 1 := sub_eq_zero.mp hc
      have hr : Real.exp (-s) = 1 := by exact_mod_cast hc'
      rw [Real.exp_eq_one_iff] at hr
      linarith
    · exact absurd hc hne
  · rintro rfl
    simp

end AuditorRepro2
#print axioms AuditorRepro2.second_face_iff_leak_without_fundacao
