import TGLExt.F1Fecho394.RegularFibreAverageStarR3
import TGLExt.F1Fecho394.RegularBoostedReflectionR1
import TGLExt.F1Fecho394.RegularSpectralCoreRangeR3
import TGLExt.F1Fecho394.RegularIntervalVectorsR2
import TGLExt.F1Fecho394.RegularOrbitMultiplicationR2
/-! Actual Fourier coefficients of finite adjunction pairs, in the existing
regular representation. Both sides retain the base vacuum and its modular flow. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularSpectralAdjunction
open MeasureTheory TGLV350.Regular
open F1Fecho.RegularCovariantCore F1Fecho.RegularNormalizedFourier
open F1Fecho.RegularSpectralAverage F1Fecho.RegularSpectralBoostedAverage
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem fibre_coefficient (A:H→L[ℂ]H) (h:ℝ) (v:H) :
    fibre A (coefficient h v)=coefficient h (A v) := by
  rw [RegularIntervalVectors.coefficient_interval,RegularIntervalVectors.coefficient_interval,
    RegularIntervalVectors.fibre_interval]

theorem left_average_coefficient (B:UnitaryFlow H) (Ω:H) (hΩ:∀t,B.U t Ω=Ω)
    (A:H→L[ℂ]H) (h:ℝ) (hh:0<h) :
    spectralCode ((h⁻¹:ℝ) • coefficient h (A Ω)) =ᵐ[volume] fun s=>
      (Real.sqrt dualHaarFactor:ℝ) • dualAmbient s
        (fibre A*RegularCoreAverage.regularAverage B h) (testVector Ω) := by
  have he : (h⁻¹:ℝ) • coefficient h (A Ω)=fibre A ((h⁻¹:ℝ) • coefficient h Ω) := by
    rw [(fibre A).map_smul_of_tower,fibre_coefficient]
  rw [he,spectralCode_fibre,←RegularSpectralCoreRange.dualOrbit_fibre]
  exact RegularOrbitMultiplication.apply_orbit_ae _ _ _ _ _
    (spectralCode_average_ae B Ω hΩ h hh)

theorem right_average_coefficient (B:UnitaryFlow H) (Ω:H) (A:H→L[ℂ]H)
    (h:ℝ) (hh:0<h) :
    spectralCode ((h⁻¹:ℝ) • boostedCoefficient B h (A Ω)) =ᵐ[volume] fun s=>
      (Real.sqrt dualHaarFactor:ℝ) • dualAmbient s
        (RegularCoreAverage.regularAverage B h*fibre A) (testVector Ω) := by
  filter_upwards [spectralCode_boostedAverage_ae B (A Ω) h hh] with s hs
  rw [hs,map_mul,ContinuousLinearMap.mul_apply,dualAmbient_fibre,fibre_testVector]

theorem adjoint_average_coefficient (B:UnitaryFlow H) (Ω:H) (A:H→L[ℂ]H)
    (h:ℝ) (hh:0<h) :
    spectralCode ((h⁻¹:ℝ) • CoefficientConjugation.reflection
      (CoefficientBoost.multiplier B (-1) (coefficient h (star A Ω)))) =ᵐ[volume]
      fun s=>(Real.sqrt dualHaarFactor:ℝ) • dualAmbient s
        (star (fibre A*RegularCoreAverage.regularAverage B h)) (testVector Ω) := by
  rw [←RegularBoostedReflection.regular_boosted_reflection]
  rw [←(F1Fecho.RegularCovariantCore.regularUnitary B (-h)).map_smul_of_tower]
  rw [RegularSpectralCoreRange.spectralCode_regular]
  have hs := RegularOrbitMultiplication.apply_orbit_ae
    (RegularCoreAverage.regularAverage B h*fibre (star A))
    (F1Fecho.RegularCovariantCore.regularUnitary B (-h)) (testVector Ω)
    (Real.sqrt dualHaarFactor) _ (right_average_coefficient B Ω (star A) h hh)
  simpa only [RegularFibreAverageStar.fibre_average_star] using hs
end F1Fecho.RegularSpectralAdjunction
#print axioms F1Fecho.RegularSpectralAdjunction.fibre_coefficient
#print axioms F1Fecho.RegularSpectralAdjunction.left_average_coefficient
#print axioms F1Fecho.RegularSpectralAdjunction.right_average_coefficient
#print axioms F1Fecho.RegularSpectralAdjunction.adjoint_average_coefficient
