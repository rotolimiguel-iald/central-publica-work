import TGLExt.V351InverseLimitFaithful
import TGLExt.V351RegularCoreTraceContract
import Mathlib.Algebra.Order.Archimedean.Basic

set_option autoImplicit false
set_option maxHeartbeats 1600000

namespace TGLV350.Regular
open TGLExt
open scoped ENNReal
noncomputable section

private theorem hilbertPositiveSqrt_transport {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (f : (H →L[ℂ] H) ≃⋆ₐ[ℂ] (H →L[ℂ] H))
    (A B : H →L[ℂ] H) (r : ℝ) (hA : 0 ≤ A) (hB : 0 ≤ B)
    (hr : 0 ≤ r) (hf : f A = (r : ℂ) • B) :
    f (hilbertPositiveSqrt A) = (Real.sqrt r : ℂ) • hilbertPositiveSqrt B := by
  have hsa (T : H →L[ℂ] H) (hT : 0 ≤ T) :
      hilbertPositiveSqrt T * hilbertPositiveSqrt T = T := CFC.sqrt_mul_sqrt_self T hT
  have hp : 0 ≤ f (hilbertPositiveSqrt A) := by
    have ha : 0 ≤ hilbertPositiveSqrt A := CFC.sqrt_nonneg A
    have h := OrderHomClass.monotone f ha
    simpa only [map_zero] using h
  have hq : 0 ≤ (Real.sqrt r : ℂ) • hilbertPositiveSqrt B := by
    apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
    apply ((ContinuousLinearMap.nonneg_iff_isPositive _).mp (CFC.sqrt_nonneg B)).smul_of_nonneg
    exact_mod_cast Real.sqrt_nonneg r
  apply (CFC.mul_self_eq_mul_self_iff _ _ hp hq).mp
  have hc : (Real.sqrt r : ℂ) * (Real.sqrt r : ℂ) = (r : ℂ) := by
    exact_mod_cast Real.mul_self_sqrt hr
  rw [← map_mul,hsa A hA,hf,smul_mul_assoc,mul_smul_comm,smul_smul,hc,hsa B hB]

/-- The existing positive square root follows the actual dual action on Bε. -/
theorem regularInverseCutoffSqrt_dual (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) (s : ℝ) :
    dualAmbient s (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) =
      (Real.sqrt (Real.exp s) : ℂ) •
        hilbertPositiveSqrt (regularInverseGeneratorCutoff P (ε * Real.exp s)) :=
  hilbertPositiveSqrt_transport (dualAmbient s) _ _ _
    (regularInverseGeneratorCutoff_nonneg P ε hε)
    (regularInverseGeneratorCutoff_nonneg P _ (mul_pos hε (Real.exp_pos s)))
    (Real.exp_pos s).le (regularInverseGeneratorCutoff_dual P ε hε s)

/-- Transport the whole sandwich by theta_(-s). The regulator moves with it;
the original dual weight is invariant, and the resulting scalar has sign -s. -/
theorem scalarInverseCutoffWeight_dual (P : SiteProfile) (ε : ℝ) (hε : 0 < ε)
    (s : ℝ) (X : PositiveCoreInput P) :
    scalarInverseCutoffWeight P ε (TGLV351.positiveDual P s X) =
      ENNReal.ofReal (Real.exp (-s)) *
        scalarInverseCutoffWeight P (ε * Real.exp (-s)) X := by
  change dualQuadraticIntegral
    (star (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) *
      dualAmbient s X.val * hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε))
      (regularVacuum P) = _
  rw [← dualQuadraticIntegral_dual_invariant (-s)]
  rw [map_mul,map_mul,map_star,regularInverseCutoffSqrt_dual P ε hε (-s)]
  have hx : dualAmbient (-s) (dualAmbient s X.val) = X.val := by
    rw [← dualAmbient_symm s,StarAlgEquiv.symm_apply_apply]
  rw [hx]
  have hc : (Real.sqrt (Real.exp (-s)) : ℂ) * (Real.sqrt (Real.exp (-s)) : ℂ) =
      (Real.exp (-s) : ℂ) := by exact_mod_cast Real.mul_self_sqrt (Real.exp_pos (-s)).le
  simp only [star_smul,Complex.star_def,Complex.conj_ofReal,
    smul_mul_assoc,mul_smul_comm,smul_smul,hc]
  exact dualQuadraticIntegral_smul_operator (Real.exp (-s)) (Real.exp_pos (-s)).le
    _ (regularVacuum P)

/-- Any positive rescaling of the regulators gives the same supremum.
Both comparisons use cofinality and the proved antitonicity, not a bijection. -/
theorem scalarInverseLimitWeight_scaled_sequence (P : SiteProfile) (r : ℝ) (hr : 0 < r)
    (X : PositiveCoreInput P) :
    (⨆ n : ℕ, scalarInverseCutoffWeight P (r / ((n : ℝ)+1)) X) =
      scalarInverseLimitWeight P X := by
  apply le_antisymm
  · apply iSup_le
    intro n
    obtain ⟨m,hm⟩ := exists_nat_one_div_lt (by positivity : 0 < r/((n : ℝ)+1))
    exact le_iSup_of_le m (scalarInverseCutoffWeight_antitone P _ _
      (by positivity) (by positivity) hm.le X)
  · unfold scalarInverseLimitWeight
    apply iSup_le
    intro n
    obtain ⟨m,hm⟩ := exists_nat_one_div_lt (by positivity : 0 < (1/((n : ℝ)+1))/r)
    have ho : r/((m : ℝ)+1) ≤ 1/((n : ℝ)+1) := by
      have hh := (lt_div_iff₀ hr).mp hm
      simpa only [one_div,mul_comm,div_eq_mul_inv,one_mul] using hh.le
    exact le_iSup_of_le m (scalarInverseCutoffWeight_antitone P _ _
      (by positivity) (by positivity) ho X)

/-- Exact dual scaling of the constructed limit on the original positive core.
This field does not supply semifiniteness or the tracial law. -/
theorem scalarInverseLimitWeight_dual (P : SiteProfile) (s : ℝ) (X : PositiveCoreInput P) :
    scalarInverseLimitWeight P (TGLV351.positiveDual P s X) =
      ENNReal.ofReal (Real.exp (-s)) * scalarInverseLimitWeight P X := by
  change (⨆ n : ℕ, scalarInverseCutoffWeight P (1/((n : ℝ)+1))
    (TGLV351.positiveDual P s X)) = _
  have hw (n : ℕ) := scalarInverseCutoffWeight_dual P (1/((n : ℝ)+1))
    (by positivity) s X
  simp only [hw]
  rw [← ENNReal.mul_iSup]
  congr 1
  have he (n : ℕ) : (1/((n : ℝ)+1)) * Real.exp (-s) = Real.exp (-s)/((n : ℝ)+1) := by ring
  simp only [he]
  exact scalarInverseLimitWeight_scaled_sequence P _ (Real.exp_pos (-s)) X

end
end TGLV350.Regular
