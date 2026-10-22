import TGLExt.V354PositiveShiftCompatibility

set_option autoImplicit false

namespace IndependentTraceCompatibility
open TGLExt TGLV350.Regular TGLV351 TGLV354 TGLV354.TraceCompletion
noncomputable section

theorem unit_read_exact (P : SiteProfile) :
    cyclicTraceCandidate P (1 : (regularCoreAlgebra P).toStarSubalgebra) =
      scalarInverseLimitWeight P (positiveUnit P) :=
  cyclicTraceCandidate_positive P (positiveUnit P)

theorem unit_read_nonzero (P : SiteProfile) :
    cyclicTraceCandidate P (1 : (regularCoreAlgebra P).toStarSubalgebra) ≠ 0 := by
  intro h
  apply positiveUnit_ne_zero P
  apply (cyclicTraceCandidate_positive_faithful P (positiveUnit P)).mp
  exact h

theorem polar_one : boundedPolar (1 : ℂ →L[ℂ] ℂ) = 1 := by
  simpa only [star_one, one_mul, CFC.sqrt_one, mul_one] using
    boundedPolar_mul_absolute (1 : ℂ →L[ℂ] ℂ)

theorem polar_one_product :
    star (boundedPolar (1 : ℂ →L[ℂ] ℂ)) * boundedPolar (1 : ℂ →L[ℂ] ℂ) = 1 := by
  rw [polar_one, star_one, one_mul]

theorem polar_one_product_nonzero :
    star (boundedPolar (1 : ℂ →L[ℂ] ℂ)) * boundedPolar (1 : ℂ →L[ℂ] ℂ) ≠ 0 := by
  rw [polar_one_product]
  exact one_ne_zero

theorem polar_zero : boundedPolar (0 : ℂ →L[ℂ] ℂ) = 0 := by
  ext x
  exact (boundedPolar_apply_eq_zero_iff _ x).mpr rfl

theorem zero_power_zero_at_one : ((0 : ℂ →L[ℂ] ℂ) ^ 0) 1 = 1 := by simp

theorem zero_operator_at_one : (0 : ℂ →L[ℂ] ℂ) 1 = 0 := by simp

theorem zero_power_zero_nonzero : ((0 : ℂ →L[ℂ] ℂ) ^ 0) 1 ≠ 0 := by simp

end
end IndependentTraceCompatibility
