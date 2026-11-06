import TGLExt.V350DualSemifiniteIdeal
import TGLExt.V350DualFormTransport
/-! Right multiplication by a base fibre preserves the existing uniform
finite-square ideal. Arbitrary right multiplication is not asserted. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularFiniteFibreRight
open TGLV350.Regular
open scoped ENNReal NNReal
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
theorem right_fibre (A : RegularHilbert H→L[ℂ]RegularHilbert H)
    (hA : HasFiniteDualSquare A) (B : H→L[ℂ]H) :
    HasFiniteDualSquare (A*fibre B) := by
  obtain ⟨C,hC⟩ := hA
  refine ⟨C*‖fibre B‖₊^2,fun v=>?_⟩
  have he : star (A*fibre B)*(A*fibre B)=star (fibre B)*(star A*A)*fibre B := by
    rw [star_mul]
    noncomm_ring
  rw [he,dualQuadraticIntegral_bimodule]
  calc
    _ ≤ (C : ℝ≥0∞)*ENNReal.ofReal (‖fibre B v‖^2) := hC _
    _ ≤ (C : ℝ≥0∞)*ENNReal.ofReal (‖fibre B‖^2*‖v‖^2) := by
      apply mul_le_mul' le_rfl
      apply ENNReal.ofReal_le_ofReal
      rw [←mul_pow]
      exact pow_le_pow_left₀ (norm_nonneg _) (ContinuousLinearMap.le_opNorm _ _) 2
    _ = _ := by
      rw [ENNReal.ofReal_mul (sq_nonneg _)]
      simp [ENNReal.ofReal_pow,ofReal_norm,enorm_eq_nnnorm,mul_assoc]
end F1Fecho.RegularFiniteFibreRight
#print axioms F1Fecho.RegularFiniteFibreRight.right_fibre
