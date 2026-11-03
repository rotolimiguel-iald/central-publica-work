import TGLExt.V350ScaledPositiveResolvent

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem positive_roots_commute (A B : H →L[ℂ] H) (h : Commute A B) :
    Commute (CFC.sqrt A) (CFC.sqrt B) := by
  rw [CFC.sqrt_eq_cfc,CFC.sqrt_eq_cfc]
  exact ((h.cfc_nnreal NNReal.sqrt).symm.cfc_nnreal NNReal.sqrt).symm

theorem positive_sqrt_product (A B : H →L[ℂ] H)
    (hA : 0 ≤ A) (hB : 0 ≤ B) (h : Commute A B) :
    CFC.sqrt (A*B) = CFC.sqrt A * CFC.sqrt B := by
  have hc := positive_roots_commute A B h
  apply CFC.sqrt_unique
  · calc
      _ = CFC.sqrt A * (CFC.sqrt B * CFC.sqrt A) * CFC.sqrt B := by simp only [mul_assoc]
      _ = CFC.sqrt A * (CFC.sqrt A * CFC.sqrt B) * CFC.sqrt B := by rw [hc.eq]
      _ = (CFC.sqrt A * CFC.sqrt A) * (CFC.sqrt B * CFC.sqrt B) := by simp only [mul_assoc]
      _ = _ := by rw [CFC.sqrt_mul_sqrt_self A hA,CFC.sqrt_mul_sqrt_self B hB]
  · exact Commute.mul_nonneg (CFC.sqrt_nonneg A) (CFC.sqrt_nonneg B) hc

theorem positive_sqrt_real_smul (A : H →L[ℂ] H) (hA : 0 ≤ A) (r : ℝ) (hr : 0 ≤ r) :
    CFC.sqrt (r • A) = Real.sqrt r • CFC.sqrt A := by
  apply CFC.sqrt_unique
  · rw [smul_mul_assoc,mul_smul_comm,smul_smul,Real.mul_self_sqrt hr,
      CFC.sqrt_mul_sqrt_self A hA]
  · exact smul_nonneg (Real.sqrt_nonneg r) (CFC.sqrt_nonneg A)

theorem scaledResolvent_root_pair_first (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0 < r) :
    CFC.sqrt (scaledPositiveResolvent T r) =
      CFC.sqrt T * CFC.sqrt (Ring.inverse (scaledResolventDenominator T r)) := by
  have hd := scaledResolventDenominator_positive T hT h1 r hr
  exact positive_sqrt_product T _ hT hd.ringInverse.nonneg
    (ring_inverse_commutes_of_unit T _ (scaledResolventDenominator_commutes T r) hd.isUnit)

theorem scaledResolvent_root_pair_second (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0 < r) :
    CFC.sqrt (1-scaledPositiveResolvent T r) =
      Real.sqrt r • (CFC.sqrt (1-T) * CFC.sqrt (Ring.inverse (scaledResolventDenominator T r))) := by
  have hd := scaledResolventDenominator_positive T hT h1 r hr
  have hc := complement_commutes_of_commute T _
    (ring_inverse_commutes_of_unit T _ (scaledResolventDenominator_commutes T r) hd.isUnit)
  rw [scaledPositiveResolvent_complement T hT h1 r hr,
    positive_sqrt_real_smul _ (Commute.mul_nonneg (sub_nonneg.mpr h1) hd.ringInverse.nonneg hc) r hr.le,
    positive_sqrt_product _ _ (sub_nonneg.mpr h1) hd.ringInverse.nonneg hc]

#print axioms positive_roots_commute
#print axioms positive_sqrt_product
#print axioms positive_sqrt_real_smul
#print axioms scaledResolvent_root_pair_first
#print axioms scaledResolvent_root_pair_second
end
end TGLV350.Regular
