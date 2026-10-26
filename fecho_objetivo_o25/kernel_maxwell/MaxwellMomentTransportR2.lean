import MaxwellBoostEnergyR2
import PhysicalSmearTranslationR2

/-! The existing translations and boost preserve each polynomial energy
moment of a photon profile, for arbitrary natural norm power. No field-tensor
covariance is inferred from this one-particle domain statement. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016

theorem U1_profile_norm_ae (a : Fin 4→ℝ) (h : H1) :
    (fun y=>‖U1 a h y‖)=ᵐ[orbitalMeasure 0] fun y=>‖h y‖ := by
  filter_upwards [orbitalTranslation_ae 0 a h] with y hy
  change ‖orbitalTranslation 0 a h y‖=‖h y‖
  rw [hy,norm_smul,orbitalPhase_norm,one_mul]

theorem B0_profile_ae (s : ℝ) (h : H1) :
    (B0 s h : MomentumCoordinates→Fib)=ᵐ[orbitalMeasure 0]
      fun y=>h (coordinateBoost 0 (-s) y) := orbitalScalarBoost_ae 0 s h

theorem moment_U1_integrable (a : Fin 4→ℝ) (h : H1) (m p : ℕ)
    (hi : Integrable (fun y=>shellEnergy y^m*‖h y‖^p) (orbitalMeasure 0)) :
    Integrable (fun y=>shellEnergy y^m*‖U1 a h y‖^p) (orbitalMeasure 0) := by
  apply hi.congr
  filter_upwards [U1_profile_norm_ae a h] with y hy
  rw [hy]

theorem moment_B0_integrable (s : ℝ) (h : H1) (m p : ℕ)
    (hi : Integrable (fun y=>shellEnergy y^m*‖h y‖^p) (orbitalMeasure 0)) :
    Integrable (fun y=>shellEnergy y^m*‖B0 s h y‖^p) (orbitalMeasure 0) := by
  have hc := (coordinateBoost_measurePreserving 0 (-s)).integrable_comp_of_integrable hi
  apply (hc.const_mul (boostEnergyConstant s^m)).mono'
  · exact ((shellEnergy_continuous.measurable.pow_const m).aestronglyMeasurable.mul
      (Lp.aestronglyMeasurable (B0 s h).norm.pow p))
  · filter_upwards [B0_profile_ae s h,shellEnergy_boost_reverse_bound_ae s] with y hy he
    rw [Real.norm_of_nonneg (mul_nonneg (pow_nonneg (shellEnergy_nonneg y) _)
      (pow_nonneg (norm_nonneg _) _)),hy]
    change shellEnergy y^m*‖h (coordinateBoost 0 (-s) y)‖^p ≤
      boostEnergyConstant s^m*(shellEnergy (coordinateBoost 0 (-s) y)^m*
        ‖h (coordinateBoost 0 (-s) y)‖^p)
    calc
      _ ≤ (boostEnergyConstant s*shellEnergy (coordinateBoost 0 (-s) y))^m*
          ‖h (coordinateBoost 0 (-s) y)‖^p := mul_le_mul_of_nonneg_right (pow_le_pow_left₀ (shellEnergy_nonneg y) he m)
            (pow_nonneg (norm_nonneg _) p)
      _ = _ := by rw [mul_pow]; ring

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.U1_profile_norm_ae
#print axioms F1Fecho.MaxwellGlobal.B0_profile_ae
#print axioms F1Fecho.MaxwellGlobal.moment_U1_integrable
#print axioms F1Fecho.MaxwellGlobal.moment_B0_integrable
