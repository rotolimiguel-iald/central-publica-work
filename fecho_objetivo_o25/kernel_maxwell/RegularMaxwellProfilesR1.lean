import RegularMaxwellWaveDensityR2
import PhysicalSmearTranslationR2

/-! A concrete regular one-particle domain, defined by all energy moments in
L1 of the original mass-shell measure. Schwartz photon profiles are proved
members. No regularity field is supplied to a Maxwell certificate. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open scoped ENNReal

def RegularProfile (h : H1) : Prop :=
  ∀ m : ℕ,Integrable (fun y=>shellEnergy y^m*‖h y‖) (orbitalMeasure 0)

theorem globalCoefficient_norm_bound (f : SchwartzTensor) (y : MomentumCoordinates) :
    ‖globalCoefficient f y‖≤16*shellEnergy y*‖f (shellEmbedding y)‖ := by
  have hs:=globalCoefficient_sq_bound f y
  have hp:=shellEnergy_nonneg y
  have hf:=norm_nonneg (f (shellEmbedding y))
  have hn:=norm_nonneg (globalCoefficient f y)
  nlinarith [sq_nonneg (shellEnergy y*‖f (shellEmbedding y)‖)]

theorem coefficient_moment_density_bound (f : SchwartzTensor) (m : ℕ) (y : MomentumCoordinates) :
    ‖(orbitalWeight 0 y).toReal • (shellEnergy y^m*‖globalCoefficient f y‖)‖≤
      16*(shellEnergy y^m*‖f (shellEmbedding y)‖) := by
  have hp:=shellEnergy_nonneg y
  have hw : (orbitalWeight 0 y).toReal=1/shellEnergy y := by
    unfold orbitalWeight shellEnergy
    exact ENNReal.toReal_ofReal (by positivity)
  rw [hw,smul_eq_mul,Real.norm_of_nonneg
    (mul_nonneg (div_nonneg zero_le_one hp) (mul_nonneg (pow_nonneg hp _) (norm_nonneg _)))]
  by_cases hz : shellEnergy y=0
  · simp only [hz,div_zero,zero_mul]
    positivity
  · calc
      _ ≤ (1/shellEnergy y)*(shellEnergy y^m*(16*shellEnergy y*‖f (shellEmbedding y)‖)) :=
        mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left
          (globalCoefficient_norm_bound f y) (pow_nonneg hp _)) (div_nonneg zero_le_one hp)
      _ = _ := by field_simp [hz]

theorem momentumSmear_regular (f : SchwartzTensor) : RegularProfile (momentumSmearCLM f) := by
  intro m
  have hi : Integrable (fun y=>shellEnergy y^m*‖globalCoefficient f y‖) (orbitalMeasure 0) := by
    change Integrable _ (momentumMeasure.withDensity (orbitalWeight 0))
    apply (integrable_withDensity_iff_integrable_smul' (orbitalWeight_measurable 0)
      (Filter.Eventually.of_forall (fun y=>ENNReal.ofReal_lt_top))).mpr
    apply ((shell_moment_integrable f m).const_mul 16).mono'
    · exact (((orbitalWeight_measurable 0).ennreal_toReal).mul
        ((shellEnergy_continuous.measurable.pow_const m).mul (globalCoefficient_measurable f).norm)).aestronglyMeasurable
    · exact Filter.Eventually.of_forall (coefficient_moment_density_bound f m)
  apply hi.congr
  filter_upwards [(globalCoefficient_memLp f).coeFn_toLp] with y hy
  change shellEnergy y^m*‖globalCoefficient f y‖=shellEnergy y^m*‖momentumSmear f y‖
  rw [hy]

theorem physicalSmear_regular (f : SchwartzTensor) : RegularProfile (physicalSmearCLM f) :=
  momentumSmear_regular (physicalFourierCLM f)

theorem regularProfile_zero : RegularProfile (0:H1) := by
  intro m
  apply (integrable_zero _ _ _).congr
  filter_upwards [Lp.coeFn_zero Fib 2 (orbitalMeasure 0)] with y hy
  simp only [hy,norm_zero,mul_zero,Pi.zero_apply]

theorem exists_nonzero_regularProfile : ∃ h : H1,RegularProfile h ∧ h≠0 := by
  obtain ⟨f,hf⟩:=exists_nonzero_real_physicalSmear
  exact ⟨physicalSmearCLM f.val,physicalSmear_regular f.val,hf⟩

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.momentumSmear_regular
#print axioms F1Fecho.MaxwellGlobal.physicalSmear_regular
#print axioms F1Fecho.MaxwellGlobal.regularProfile_zero
#print axioms F1Fecho.MaxwellGlobal.exists_nonzero_regularProfile
