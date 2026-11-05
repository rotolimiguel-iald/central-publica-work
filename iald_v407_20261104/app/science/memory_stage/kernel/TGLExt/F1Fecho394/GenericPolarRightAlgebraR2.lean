import TGLExt.V350AntiunitaryPositiveConjugation
import Mathlib.Algebra.Star.Subalgebra
/-! Algebraic closure of the polar-right identity, proved before specialization
at the large Fock representation. No actual modular identity is an input here. -/
set_option autoImplicit false
set_option maxHeartbeats 500000
noncomputable section
namespace F1Fecho.GenericPolarRightAlgebra
open TGLV350.Regular
variable {𝒜 : Type*} {H : Type} [Ring 𝒜] [Algebra ℂ 𝒜] [StarRing 𝒜] [StarModule ℂ 𝒜]
variable [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (N : Submodule ℂ 𝒜) (Λ : N →ₗ[ℂ] H) (π : 𝒜 →⋆ₐ[ℂ] (H →L[ℂ] H))
variable (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
/-- The actual polar right identity on the existing full weight domain. -/
def ScalarPolarRight  (b : 𝒜) : Prop :=
  ∀ A : N, ∃ h : A.val*b ∈ N,
    Λ ⟨A.val*b,h⟩ =
      antiunitaryConjugate J
        (π (star b)) (Λ A)

theorem scalarPolarRight_zero  : ScalarPolarRight N Λ π J 0 := by
  intro A
  have h : A.val*0 ∈ N := by simp
  refine ⟨h,?_⟩
  have he : (⟨A.val*0,h⟩ : N) = 0 := Subtype.ext (mul_zero _)
  rw [he,map_zero,antiunitaryConjugate_apply,star_zero,map_zero]
  simp only [zero_apply,map_zero]

theorem scalarPolarRight_one  : ScalarPolarRight N Λ π J 1 := by
  intro A
  have h : A.val*1 ∈ N := by simpa only [mul_one] using A.property
  refine ⟨h,?_⟩
  have he : (⟨A.val*1,h⟩ : N) = A := Subtype.ext (mul_one _)
  rw [he,antiunitaryConjugate_apply,star_one,map_one]
  simp only [one_apply_eq_self,LinearIsometryEquiv.apply_symm_apply]

theorem scalarPolarRight_add 
    (b c : 𝒜)
    (hb : ScalarPolarRight N Λ π J b) (hc : ScalarPolarRight N Λ π J c) : ScalarPolarRight N Λ π J (b+c) := by
  intro A
  obtain ⟨hAb,heb⟩ := hb A
  obtain ⟨hAc,hec⟩ := hc A
  have h : A.val*(b+c) ∈ N := by
    simpa only [mul_add] using (N).add_mem hAb hAc
  refine ⟨h,?_⟩
  have he : (⟨A.val*(b+c),h⟩ : N) =
      (⟨A.val*b,hAb⟩ : N) + ⟨A.val*c,hAc⟩ :=
    Subtype.ext (mul_add _ _ _)
  rw [he,map_add,heb,hec]
  simp only [antiunitaryConjugate_apply,star_add,map_add,add_apply]

theorem scalarPolarRight_smul 
    (b : 𝒜) (hb : ScalarPolarRight N Λ π J b) (c : ℂ) :
    ScalarPolarRight N Λ π J (c • b) := by
  intro A
  obtain ⟨hAb,heb⟩ := hb A
  have h : A.val*(c • b) ∈ N := by
    simpa only [mul_smul_comm] using (N).smul_mem c hAb
  refine ⟨h,?_⟩
  have he : (⟨A.val*(c • b),h⟩ : N) =
      c • (⟨A.val*b,hAb⟩ : N) := Subtype.ext (mul_smul_comm _ _ _)
  rw [he,map_smul,heb]
  simp only [antiunitaryConjugate_apply,star_smul,map_smul,
    smul_apply,LinearIsometryEquiv.map_smulₛₗ,starRingEnd_apply,star_star]

theorem scalarPolarRight_mul 
    (b c : 𝒜)
    (hb : ScalarPolarRight N Λ π J b) (hc : ScalarPolarRight N Λ π J c) : ScalarPolarRight N Λ π J (b*c) := by
  intro A
  obtain ⟨hAb,heb⟩ := hb A
  obtain ⟨hAbc,hec⟩ := hc ⟨A.val*b,hAb⟩
  have h : A.val*(b*c) ∈ N := by
    simpa only [mul_assoc] using hAbc
  refine ⟨h,?_⟩
  have he : (⟨A.val*(b*c),h⟩ : N) =
      ⟨(A.val*b)*c,hAbc⟩ := Subtype.ext (mul_assoc _ _ _).symm
  rw [he,hec,heb]
  simp only [antiunitaryConjugate_apply,star_mul,map_mul,mul_apply_eq_comp,
    LinearIsometryEquiv.symm_apply_apply]

/-- The two-sided star condition is explicit; it is not silently inferred
from a right-boundedness condition on b alone. -/
def scalarPolarRightAlgebra  :
    StarSubalgebra ℂ 𝒜 where
  carrier := {b | ScalarPolarRight N Λ π J b ∧ ScalarPolarRight N Λ π J (star b)}
  zero_mem' := by simpa only [Set.mem_setOf_eq,star_zero] using And.intro (scalarPolarRight_zero N Λ π J) (scalarPolarRight_zero N Λ π J)
  one_mem' := by simpa only [Set.mem_setOf_eq,star_one] using And.intro (scalarPolarRight_one N Λ π J) (scalarPolarRight_one N Λ π J)
  add_mem' := by
    intro b c hb hc
    exact ⟨scalarPolarRight_add N Λ π J b c hb.1 hc.1,
      by simpa only [star_add] using scalarPolarRight_add N Λ π J (star b) (star c) hb.2 hc.2⟩
  mul_mem' := by
    intro b c hb hc
    exact ⟨scalarPolarRight_mul N Λ π J b c hb.1 hc.1,
      by simpa only [star_mul] using scalarPolarRight_mul N Λ π J (star c) (star b) hc.2 hb.2⟩
  algebraMap_mem' c := by
    have h := scalarPolarRight_smul N Λ π J 1 (scalarPolarRight_one N Λ π J) c
    have hs := scalarPolarRight_smul N Λ π J 1 (scalarPolarRight_one N Λ π J) (star c)
    simpa only [Set.mem_setOf_eq,Algebra.algebraMap_eq_smul_one,star_smul,star_one] using And.intro h hs
  star_mem' := by
    intro b hb
    exact ⟨hb.2,by simpa only [star_star] using hb.1⟩


end F1Fecho.GenericPolarRightAlgebra
#print axioms F1Fecho.GenericPolarRightAlgebra.ScalarPolarRight
#print axioms F1Fecho.GenericPolarRightAlgebra.scalarPolarRight_zero
#print axioms F1Fecho.GenericPolarRightAlgebra.scalarPolarRight_one
#print axioms F1Fecho.GenericPolarRightAlgebra.scalarPolarRight_add
#print axioms F1Fecho.GenericPolarRightAlgebra.scalarPolarRight_smul
#print axioms F1Fecho.GenericPolarRightAlgebra.scalarPolarRight_mul
#print axioms F1Fecho.GenericPolarRightAlgebra.scalarPolarRightAlgebra
