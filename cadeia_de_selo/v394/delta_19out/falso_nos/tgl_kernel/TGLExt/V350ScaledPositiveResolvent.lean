import TGLExt.V350PositiveRootIntertwining
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Order

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def scaledResolventDenominator (T : H →L[ℂ] H) (r : ℝ) : H →L[ℂ] H :=
  r • 1 + (1-r) • T

theorem scaledResolventDenominator_sub (T : H →L[ℂ] H) (r : ℝ) :
    scaledResolventDenominator T r - T = r • (1-T) := by
  unfold scaledResolventDenominator
  rw [sub_smul,one_smul,smul_sub]
  abel

theorem scaledResolventDenominator_alt (T : H →L[ℂ] H) (r : ℝ) :
    scaledResolventDenominator T r = 1 + (r-1) • (1-T) := by
  unfold scaledResolventDenominator
  simp only [smul_sub,sub_smul,one_smul]
  abel

theorem scaledResolventDenominator_positive (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0 < r) :
    IsStrictlyPositive (scaledResolventDenominator T r) := by
  by_cases hle : r ≤ 1
  · have hp : IsStrictlyPositive (r • (1 : H →L[ℂ] H)) := by
      rw [IsStrictlyPositive.iff_of_unital]
      refine ⟨smul_nonneg hr.le zero_le_one,?_⟩
      rw [← Algebra.algebraMap_eq_smul_one]
      exact (isUnit_iff_ne_zero.mpr hr.ne').map (algebraMap ℝ (H →L[ℂ] H))
    exact hp.add_nonneg (smul_nonneg (sub_nonneg.mpr hle) hT)
  · rw [scaledResolventDenominator_alt]
    have hp : IsStrictlyPositive (1 : H →L[ℂ] H) := by cfc_tac
    exact hp.add_nonneg (smul_nonneg (sub_nonneg.mpr (le_of_not_ge hle))
      (sub_nonneg.mpr h1))

theorem scaledResolventDenominator_commutes (T : H →L[ℂ] H) (r : ℝ) :
    Commute T (scaledResolventDenominator T r) := by
  change T * (r • 1 + (1-r) • T) = (r • 1 + (1-r) • T) * T
  simp only [mul_add,add_mul,mul_smul_comm,smul_mul_assoc,mul_one,one_mul]

theorem ring_inverse_commutes_of_unit (T D : H →L[ℂ] H)
    (h : Commute T D) (hd : IsUnit D) : Commute T (Ring.inverse D) := by
  change T * Ring.inverse D = Ring.inverse D * T
  calc
    _ = (Ring.inverse D * D) * T * Ring.inverse D := by rw [Ring.inverse_mul_cancel D hd,one_mul]
    _ = Ring.inverse D * (D * T) * Ring.inverse D := by simp only [mul_assoc]
    _ = Ring.inverse D * (T * D) * Ring.inverse D := by rw [h.eq]
    _ = (Ring.inverse D * T) * (D * Ring.inverse D) := by simp only [mul_assoc]
    _ = _ := by rw [Ring.mul_inverse_cancel D hd,mul_one]

def scaledPositiveResolvent (T : H →L[ℂ] H) (r : ℝ) : H →L[ℂ] H :=
  T * Ring.inverse (scaledResolventDenominator T r)

theorem scaledPositiveResolvent_nonneg (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0 < r) :
    0 ≤ scaledPositiveResolvent T r := by
  have hd := scaledResolventDenominator_positive T hT h1 r hr
  exact Commute.mul_nonneg hT hd.ringInverse.nonneg
    (ring_inverse_commutes_of_unit T _ (scaledResolventDenominator_commutes T r) hd.isUnit)

theorem scaledPositiveResolvent_complement (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0 < r) :
    1-scaledPositiveResolvent T r =
      r • ((1-T) * Ring.inverse (scaledResolventDenominator T r)) := by
  have hd := (scaledResolventDenominator_positive T hT h1 r hr).isUnit
  calc
    _ = (scaledResolventDenominator T r-T) * Ring.inverse (scaledResolventDenominator T r) := by
      rw [sub_mul,Ring.mul_inverse_cancel _ hd]
      rfl
    _ = _ := by rw [scaledResolventDenominator_sub,smul_mul_assoc]

theorem scaledPositiveResolvent_le_one (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0 < r) :
    scaledPositiveResolvent T r ≤ 1 := by
  rw [← sub_nonneg,scaledPositiveResolvent_complement T hT h1 r hr]
  have hd := scaledResolventDenominator_positive T hT h1 r hr
  have hc := ring_inverse_commutes_of_unit T _ (scaledResolventDenominator_commutes T r) hd.isUnit
  exact smul_nonneg hr.le (Commute.mul_nonneg (sub_nonneg.mpr h1) hd.ringInverse.nonneg
    (complement_commutes_of_commute T _ hc))

#print axioms scaledResolventDenominator_sub
#print axioms scaledResolventDenominator_alt
#print axioms scaledResolventDenominator_positive
#print axioms scaledResolventDenominator_commutes
#print axioms ring_inverse_commutes_of_unit
#print axioms scaledPositiveResolvent_nonneg
#print axioms scaledPositiveResolvent_complement
#print axioms scaledPositiveResolvent_le_one
end
end TGLV350.Regular
