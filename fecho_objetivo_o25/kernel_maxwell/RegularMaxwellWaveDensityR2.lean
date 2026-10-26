import PhysicalSchwartzMaxwellR1
import SchwartzRestrictionMomentsR1

/-! Actual regular on-shell wave density from a Schwartz profile. All energy
moments are integrable, establishing the pointwise domain before local Wick
stress is attempted. No covariance or coincident-point operator is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory SchwartzMap Filter
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.SchwartzRestriction
open scoped ENNReal

def waveDensity (f : SchwartzTensor) (μ ν : Fin 4) (y : MomentumCoordinates) : ℂ :=
  ∑ j : Fin 2,(cartesianStrength y j μ ν:ℂ)*globalCoefficient f y j

theorem waveDensity_measurable (f : SchwartzTensor) (μ ν : Fin 4) :
    Measurable (waveDensity f μ ν) := by
  apply Finset.measurable_sum
  intro j hj
  exact (Complex.continuous_ofReal.measurable.comp (cartesianStrength_measurable j μ ν)).mul
    ((PiLp.continuous_apply 2 _ j).measurable.comp (globalCoefficient_measurable f))

theorem waveDensity_bound (f : SchwartzTensor) (μ ν : Fin 4) (y : MomentumCoordinates) :
    ‖waveDensity f μ ν y‖≤16*shellEnergy y^2*‖f (shellEmbedding y)‖ := by
  have hh (j : Fin 2) : ‖(cartesianStrength y j μ ν:ℂ)*globalCoefficient f y j‖≤
      8*shellEnergy y^2*‖f (shellEmbedding y)‖ := by
    rw [norm_mul,Complex.norm_real,Real.norm_eq_abs]
    have h:=mul_le_mul (cartesianStrength_bound y j μ ν)
      (globalCoefficient_component_bound f y j) (norm_nonneg _) (shellEnergy_nonneg y)
    calc
      _ ≤ shellEnergy y*(8*shellEnergy y*‖f (shellEmbedding y)‖) := h
      _ = _ := by ring
  have h:= (norm_sum_le Finset.univ (fun j : Fin 2=>
    (cartesianStrength y j μ ν:ℂ)*globalCoefficient f y j)).trans
      (Finset.sum_le_sum (fun j _=>hh j))
  simp only [Finset.sum_const,Finset.card_univ,Fintype.card_fin,nsmul_eq_mul] at h
  change ‖∑ j : Fin 2,(cartesianStrength y j μ ν:ℂ)*globalCoefficient f y j‖≤_
  norm_num at h
  nlinarith only [h]

theorem shell_moment_integrable (f : SchwartzTensor) (m : ℕ) :
    Integrable (fun y=>shellEnergy y^m*‖f (shellEmbedding y)‖) momentumMeasure := by
  letI : momentumMeasure.IsAddHaarMeasure := by unfold momentumMeasure; infer_instance
  exact energy_moment_restriction_integrable f shellEmbedding shellEnergy
    (by norm_num : (0:ℝ)≤2) shellEmbedding_proper_bound energy_le_twice_coordinate_norm
    shellEnergy_nonneg shellEmbedding_continuous.measurable shellEnergy_continuous.measurable m

theorem waveDensity_weighted_bound (f : SchwartzTensor) (μ ν : Fin 4)
    (m : ℕ) (y : MomentumCoordinates) :
    ‖(orbitalWeight 0 y).toReal • (shellEnergy y^m*‖waveDensity f μ ν y‖)‖≤
      16*(shellEnergy y^(m+1)*‖f (shellEmbedding y)‖) := by
  have hp:=shellEnergy_nonneg y
  have hw : (orbitalWeight 0 y).toReal=1/shellEnergy y := by
    unfold orbitalWeight shellEnergy
    exact ENNReal.toReal_ofReal (by positivity)
  rw [hw,smul_eq_mul,Real.norm_of_nonneg
    (mul_nonneg (div_nonneg zero_le_one hp) (mul_nonneg (pow_nonneg hp _) (norm_nonneg _)))]
  by_cases hz : shellEnergy y=0
  · simp [hz]
  · calc
      _ ≤ (1/shellEnergy y)*(shellEnergy y^m*(16*shellEnergy y^2*‖f (shellEmbedding y)‖)) :=
        mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left
          (waveDensity_bound f μ ν y) (pow_nonneg hp _)) (div_nonneg zero_le_one hp)
      _ = _ := by rw [pow_succ]; field_simp [hz]; ring

theorem waveDensity_moment_integrable (f : SchwartzTensor) (μ ν : Fin 4) (m : ℕ) :
    Integrable (fun y=>shellEnergy y^m*‖waveDensity f μ ν y‖) (orbitalMeasure 0) := by
  change Integrable _ (momentumMeasure.withDensity (orbitalWeight 0))
  apply (integrable_withDensity_iff_integrable_smul' (orbitalWeight_measurable 0)
    (Filter.Eventually.of_forall (fun y=>ENNReal.ofReal_lt_top))).mpr
  apply ((shell_moment_integrable f (m+1)).const_mul 16).mono'
  · exact (((orbitalWeight_measurable 0).ennreal_toReal).mul
      ((shellEnergy_continuous.measurable.pow_const m).mul (waveDensity_measurable f μ ν).norm)).aestronglyMeasurable
  · exact Filter.Eventually.of_forall (waveDensity_weighted_bound f μ ν m)

theorem waveDensity_integrable (f : SchwartzTensor) (μ ν : Fin 4) :
    Integrable (waveDensity f μ ν) (orbitalMeasure 0) := by
  apply (integrable_norm_iff (waveDensity_measurable f μ ν).aestronglyMeasurable).mp
  simpa only [pow_zero,one_mul] using waveDensity_moment_integrable f μ ν 0

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.waveDensity_bound
#print axioms F1Fecho.MaxwellGlobal.shell_moment_integrable
#print axioms F1Fecho.MaxwellGlobal.waveDensity_moment_integrable
#print axioms F1Fecho.MaxwellGlobal.waveDensity_integrable
