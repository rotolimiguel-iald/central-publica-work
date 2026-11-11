import TGLExt.F1Fecho394.RegularSpectralAdjunctionR1
import TGLExt.F1Fecho394.RegularTranslatedAverageR2
import TGLExt.F1Fecho394.RegularTranslatedReflectionR1
/-! Both Fourier coefficients of a translated finite star pair, for every
nonempty interval. The source is the same regular core representation. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularTranslatedSpectralAdjunction
open MeasureTheory TGLV350.Regular
open F1Fecho.RegularCovariantCore F1Fecho.RegularNormalizedFourier
open F1Fecho.RegularSpectralAverage F1Fecho.LpIntervalTotality
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem translated_coefficient (B:UnitaryFlow H) (Ω:H) (hΩ:∀t,B.U t Ω=Ω)
    (A:H→L[ℂ]H) (a b:ℝ) (hab:a<b) :
    spectralCode (((b-a)⁻¹:ℝ) • intervalVector a b (A Ω)) =ᵐ[volume] fun s=>
      (Real.sqrt dualHaarFactor:ℝ) • dualAmbient s
        (fibre A*(regularUnitary B a*RegularCoreAverage.regularAverage B (b-a))) (testVector Ω) := by
  have he : ((b-a)⁻¹:ℝ) • intervalVector a b (A Ω)=
      fibre A (regularUnitary B a (((b-a)⁻¹:ℝ) • coefficient (b-a) Ω)) := by
    rw [(regularUnitary B a).map_smul_of_tower,(fibre A).map_smul_of_tower,
      RegularIntervalVectors.regular_coefficient B Ω hΩ,
      RegularIntervalVectors.fibre_interval]
  rw [he,spectralCode_fibre,←RegularSpectralCoreRange.dualOrbit_fibre,
    RegularSpectralCoreRange.spectralCode_regular]
  exact RegularOrbitMultiplication.apply_orbit_ae _ _ _ _ _
    (RegularOrbitMultiplication.apply_orbit_ae _ _ _ _ _
      (spectralCode_average_ae B Ω hΩ (b-a) (sub_pos.mpr hab)))

theorem translated_star_coefficient (B:UnitaryFlow H) (Ω:H) (A:H→L[ℂ]H)
    (a b:ℝ) (hab:a<b) :
    spectralCode (((b-a)⁻¹:ℝ) • CoefficientConjugation.reflection
      (CoefficientBoost.multiplier B (-1) (intervalVector a b (star A Ω)))) =ᵐ[volume] fun s=>
      (Real.sqrt dualHaarFactor:ℝ) • dualAmbient s
        (star (fibre A*(regularUnitary B a*RegularCoreAverage.regularAverage B (b-a)))) (testVector Ω) := by
  rw [←RegularTranslatedReflection.regular_boosted_reflection]
  rw [←(regularUnitary B (-b)).map_smul_of_tower,
    RegularSpectralCoreRange.spectralCode_regular]
  have hs:=RegularOrbitMultiplication.apply_orbit_ae
    (RegularCoreAverage.regularAverage B (b-a)*fibre (star A)) (regularUnitary B (-b))
    (testVector Ω) (Real.sqrt dualHaarFactor) _
    (RegularSpectralAdjunction.right_average_coefficient B Ω (star A) (b-a) (sub_pos.mpr hab))
  have he : -(a+(b-a))=-b := by ring
  simpa only [RegularTranslatedAverage.translated_star,he] using hs
end F1Fecho.RegularTranslatedSpectralAdjunction
#print axioms F1Fecho.RegularTranslatedSpectralAdjunction.translated_coefficient
#print axioms F1Fecho.RegularTranslatedSpectralAdjunction.translated_star_coefficient
