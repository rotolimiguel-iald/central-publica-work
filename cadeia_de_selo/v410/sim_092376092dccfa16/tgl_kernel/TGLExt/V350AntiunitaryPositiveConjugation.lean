import TGLExt.GenericAntilinearAdjoint
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic
import Mathlib.Analysis.InnerProductSpace.StarOrder

set_option autoImplicit false
set_option linter.unusedSectionVars false

namespace TGLV350.Regular
open ChatgptAudit.Continuous050
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (U : H ≃ₛₗᵢ[starRingEnd ℂ] H)

/-- Fix the canonical Hilbert-operator CFC instances before specializing H. -/
def hilbertPositiveSqrt (T : H →L[ℂ] H) : H →L[ℂ] H := CFC.sqrt T

theorem hilbertComplement_nonneg (T : H →L[ℂ] H) (h : T ≤ 1) : 0 ≤ 1-T :=
  sub_nonneg.mpr h

/-- Complex-linear conjugation by an antiunitary; U need not be involutive. -/
def antiunitaryConjugate (T : H →L[ℂ] H) : H →L[ℂ] H :=
  U.toLinearIsometry.toContinuousLinearMap.comp
    (T.comp U.symm.toLinearIsometry.toContinuousLinearMap)

theorem antiunitaryConjugate_apply (T : H →L[ℂ] H) (x : H) :
    antiunitaryConjugate U T x=U (T (U.symm x)) := rfl

theorem antiunitaryConjugate_mul (T V : H →L[ℂ] H) :
    antiunitaryConjugate U (T*V)=antiunitaryConjugate U T * antiunitaryConjugate U V := by
  ext x
  simp only [ContinuousLinearMap.mul_apply,antiunitaryConjugate_apply,U.symm_apply_apply]

theorem antiunitaryConjugate_nonneg (T : H →L[ℂ] H) (hT : 0 ≤ T) :
    0 ≤ antiunitaryConjugate U T := by
  apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
  apply (ContinuousLinearMap.isPositive_iff_complex _).mpr
  intro x
  have hinner : inner ℂ (antiunitaryConjugate U T x) x =
      star (inner ℂ (T (U.symm x)) (U.symm x)) := by
    have h := antiunitary_inner_conj U (T (U.symm x)) (U.symm x)
    simpa only [U.apply_symm_apply,antiunitaryConjugate_apply] using h
  have h := (ContinuousLinearMap.isPositive_iff_complex T).mp
    ((ContinuousLinearMap.nonneg_iff_isPositive T).mp hT) (U.symm x)
  rw [hinner]
  constructor
  · calc
      _ = ((inner ℂ (T (U.symm x)) (U.symm x)).re : ℂ) := rfl
      _ = star (((inner ℂ (T (U.symm x)) (U.symm x)).re : ℂ)) := by simp
      _ = _ := congrArg star h.1
  · exact h.2

theorem antiunitaryConjugate_sqrt (T : H →L[ℂ] H) (hT : 0 ≤ T) :
    CFC.sqrt (antiunitaryConjugate U T)=antiunitaryConjugate U (CFC.sqrt T) := by
  apply CFC.sqrt_unique
  · calc
      _ = antiunitaryConjugate U (CFC.sqrt T * CFC.sqrt T) :=
        (antiunitaryConjugate_mul U (CFC.sqrt T) (CFC.sqrt T)).symm
      _ = antiunitaryConjugate U T :=
        congrArg (antiunitaryConjugate U) (CFC.sqrt_mul_sqrt_self T hT)
  · exact antiunitaryConjugate_nonneg U (CFC.sqrt T) (CFC.sqrt_nonneg T)

#print axioms antiunitaryConjugate
#print axioms antiunitaryConjugate_apply
#print axioms antiunitaryConjugate_mul
#print axioms antiunitaryConjugate_nonneg
#print axioms antiunitaryConjugate_sqrt
#print axioms hilbertPositiveSqrt
#print axioms hilbertComplement_nonneg
end
end TGLV350.Regular
