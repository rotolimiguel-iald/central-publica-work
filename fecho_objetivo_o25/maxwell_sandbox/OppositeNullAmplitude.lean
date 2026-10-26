import OppositeRealNullStress

set_option autoImplicit false
set_option maxHeartbeats 2200000

/-! Opposite-null frequency and amplitude, before the coordinate change. -/
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory SchwartzMap
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open F1Fecho.MaxwellStress ChatgptAudit.WignerRapidityMeasure016

/-- Frequency on the opposite future light cone. -/
def shellOppositeFrequency (y : MomentumCoordinates) : ℝ := shellEnergy y + y.2

/-- Amplitude associated with the opposite null direction. -/
def oppositeNullProfileAmplitude (h : H1) (a : Fin 2)
    (y : MomentumCoordinates) : ℂ :=
  ∑ j : Fin 2, ((if j = 0 then -nullPolarization y a j else nullPolarization y a j : ℝ) : ℂ) * h y j

/-- The opposite frequency is positive outside the transverse axis. -/
theorem shellOppositeFrequency_pos (y : MomentumCoordinates) (hy : y.1 ≠ 0) :
    0 < shellOppositeFrequency y := by
  have hr := transverseMass_pos_of_ne_zero 0 y.1 hy
  have hs := shellEnergy_sq y
  have hn := shellEnergy_nonneg y
  unfold shellOppositeFrequency
  nlinarith [sq_nonneg y.2, transverseMass_sq 0 y.1, sq_pos_of_pos hr]

/-- Exact density factor for the opposite contraction. -/
theorem lowerProfileDensity_opposite_factor (h : H1) (a : Fin 2) (y : MomentumCoordinates) :
    lowerProfileDensity h 0 (nullScreenIndex a) y -
      lowerProfileDensity h 1 (nullScreenIndex a) y =
      (shellOppositeFrequency y : ℂ) * oppositeNullProfileAmplitude h a y := by
  have h0 : metricSignC (0 : Fin 4) = 1 := rfl
  have h1 : metricSignC (1 : Fin 4) = -1 := rfl
  have ha : metricSignC (nullScreenIndex a) = -1 := by
    fin_cases a <;> norm_num [nullScreenIndex, metricSignC]
  have hs (j : Fin 2) :
      -cartesianStrength y j 0 (nullScreenIndex a) -
        cartesianStrength y j 1 (nullScreenIndex a) =
          shellOppositeFrequency y *
            (if j = 0 then -nullPolarization y a j else nullPolarization y a j) := by
    fin_cases a <;> fin_cases j <;>
      simp [cartesianStrength, transverseRatio, shellOppositeFrequency, shellEnergy,
        transverseMass, nullScreenIndex, nullPolarization] <;> ring
  calc
    _ = ∑ j : Fin 2,
        ((-cartesianStrength y j 0 (nullScreenIndex a) -
          cartesianStrength y j 1 (nullScreenIndex a) : ℝ) : ℂ) * h y j := by
      simp only [lowerProfileDensity, profileDensity, h0, h1, ha, Fin.sum_univ_two]
      push_cast
      ring
    _ = _ := by
      simp only [hs, Complex.ofReal_mul, oppositeNullProfileAmplitude,
        Finset.mul_sum, mul_assoc]

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.shellOppositeFrequency_pos
#print axioms F1Fecho.MaxwellGlobal.lowerProfileDensity_opposite_factor
