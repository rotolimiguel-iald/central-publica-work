import AxisCompactNullMomentum
import TGLExt.NullMomentumInvariant

set_option autoImplicit false
set_option maxHeartbeats 2200000

/-! Algebraic opposite-null contraction and its classical positivity. -/
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory SchwartzMap
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open TGLExt.NullEnergyScaling TGLExt.NullMomentumInvariant
open F1Fecho.NetworkReuse F1Fecho.NetworkModularCore F1Fecho.CoherentKernel
open F1Fecho.WeightedPlancherel F1Rede.BosonicFock F1Rede.BosonicFockGroupActions
open F1Fecho.MaxwellStress
open ChatgptAudit.WignerRapidityMeasure016
open scoped FourierTransform

/-- The opposite-null Maxwell contraction is a sum of squares of differences. -/
theorem stress_opposite_null_contraction (F : Fin 4 → Fin 4 → ℂ)
    (ha : ∀ μ ν, F ν μ = -F μ ν) :
    stress metricSignC F 0 0 - stress metricSignC F 0 1 -
      stress metricSignC F 1 0 + stress metricSignC F 1 1 =
      (F 0 2 - F 1 2)^2 + (F 0 3 - F 1 3)^2 := by
  have h00 : F 0 0 = 0 := by have h := ha 0 0; linear_combination (1 / 2 : ℂ) * h
  have h11 : F 1 1 = 0 := by have h := ha 1 1; linear_combination (1 / 2 : ℂ) * h
  have hs0 : metricSignC (0 : Fin 4) = (1 : ℂ) := rfl
  have hs1 : metricSignC (1 : Fin 4) = (-1 : ℂ) := rfl
  have hs2 : metricSignC (2 : Fin 4) = (-1 : ℂ) := rfl
  have hs3 : metricSignC (3 : Fin 4) = (-1 : ℂ) := rfl
  simp only [stress, Fin.sum_univ_four, hs0, hs1, hs2, hs3, h00, h11, ha 0 1]
  norm_num
  ring

/-- The real opposite-null density on the opposite null plane. -/
def realOppositeNullStress (h : H1) (x : Spacetime) : ℝ :=
  (realProfileStress h 0 0 x - realProfileStress h 0 1 x -
    realProfileStress h 1 0 x + realProfileStress h 1 1 x).re

theorem realOppositeNullStress_eq_squares (h : H1) (x : Spacetime) :
    realOppositeNullStress h x =
      ((realProfileWave h 0 2 x - realProfileWave h 1 2 x)^2 +
       (realProfileWave h 0 3 x - realProfileWave h 1 3 x)^2).re := by
  unfold realOppositeNullStress realProfileStress
  exact congrArg Complex.re (stress_opposite_null_contraction (fun μ ν => realProfileWave h μ ν x)
    (fun μ ν => realProfileWave_antisymmetric h μ ν x))

/-- The real opposite-null density is nonnegative. -/
theorem realOppositeNullStress_nonneg (h : H1) (x : Spacetime) :
    0 ≤ realOppositeNullStress h x := by
  rw [realOppositeNullStress_eq_squares]
  simp only [realProfileWave, realWaveProjection_apply, ← Complex.ofReal_sub,
    ← Complex.ofReal_pow, ← Complex.ofReal_add, Complex.ofReal_re]
  positivity

/-- The normalized opposite-null density. -/
def unitaryFourierRealOppositeStress (h : H1) (x : Spacetime) : ℝ :=
  unitaryFourierStressScale * Real.exp (‖h‖ ^ 2) * realOppositeNullStress h x

theorem unitaryFourierRealOppositeStress_nonneg (h : H1) (x : Spacetime) :
    0 ≤ unitaryFourierRealOppositeStress h x :=
  mul_nonneg
    (mul_nonneg (le_of_lt unitaryFourierStressScale_pos) (Real.exp_pos _).le)
    (realOppositeNullStress_nonneg h x)

private theorem pairing_oppositeNullDir_components (M : Matrix (Fin 4) (Fin 4) ℝ) :
    pairing M oppositeNullDir oppositeNullDir = M 0 0 - M 0 1 - M 1 0 + M 1 1 := by
  unfold ContratoQGv31.pairing oppositeNullDir
  simp [Matrix.mulVec, dotProduct, Fin.sum_univ_four] <;> ring

/-- Real profile stress has zero imaginary part. -/
theorem realProfileStress_im_zero (h : H1) (μ ν : Fin 4) (x : Spacetime) :
    (realProfileStress h μ ν x).im = 0 := by
  have hs := realWaveProjection_stress_real (fun α β => lowerProfileWave h α β x) μ ν
  change (starRingEnd ℂ) (realProfileStress h μ ν x) = realProfileStress h μ ν x at hs
  have him := congrArg Complex.im hs
  simp only [Complex.conj_im] at him
  linarith

/-- The calibrated opposite-null density on a coherent vector is the normalized
    real opposite density. -/
theorem calibrated_oppositeNullEnergy_exponential {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (h : RegularLabel) (x : Spacetime) :
    oppositeNullEnergy (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential h).val x = unitaryFourierRealOppositeStress h.val x := by
  have hi : inner ℂ h.val h.val = ((‖h.val‖ ^ 2 : ℝ) : ℂ) := by
    rw [← inner_self_ofReal_re, inner_self_eq_norm_sq]
    norm_cast
  have he : Complex.exp (inner ℂ h.val h.val) = (Real.exp (‖h.val‖ ^ 2) : ℂ) := by
    rw [hi]
    exact (Complex.ofReal_exp _).symm
  rw [oppositeNullEnergy, pairing_oppositeNullDir_components]
  simp_rw [calibratedStress_eq_unitaryFourierFock]
  simp only [unitaryFourierPointStressForm_exponential, unitaryFourierCoherentStress,
    coherentProfileStress, coherentProfileWave_diagonal, realProfileStress,
    unitaryFourierRealOppositeStress, realOppositeNullStress, he,
    realProfileStress_im_zero, Complex.add_re, Complex.sub_re, Complex.mul_re,
    Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero]
  ring

/-- Positivity of the calibrated opposite density on a coherent vector. -/
theorem calibrated_oppositeNullEnergy_exponential_nonneg {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (h : RegularLabel) (x : Spacetime) :
    0 ≤ oppositeNullEnergy (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential h).val x := by
  rw [calibrated_oppositeNullEnergy_exponential]
  exact unitaryFourierRealOppositeStress_nonneg h.val x

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.stress_opposite_null_contraction
#print axioms F1Fecho.MaxwellGlobal.realOppositeNullStress_eq_squares
#print axioms F1Fecho.MaxwellGlobal.realOppositeNullStress_nonneg
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierRealOppositeStress_nonneg
#print axioms F1Fecho.MaxwellGlobal.calibrated_oppositeNullEnergy_exponential
#print axioms F1Fecho.MaxwellGlobal.calibrated_oppositeNullEnergy_exponential_nonneg
