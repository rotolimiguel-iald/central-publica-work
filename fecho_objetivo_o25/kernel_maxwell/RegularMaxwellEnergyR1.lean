import RegularMaxwellProfilesR2
import SchwartzRestrictionSquareMomentsR1

/-! A concrete common regular domain with both L1 and quadratic L2 energy
moments. These are proved for the actual Schwartz-to-photon map. This supplies
finite one-particle kinetic energy, not a Maxwell stress/charge identity. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.SchwartzRestriction
open scoped ENNReal

def EnergySquareProfile (h : H1) : Prop :=
  ∀ m : ℕ,Integrable (fun y=>shellEnergy y^m*‖h y‖^2) (orbitalMeasure 0)

def StrongRegularProfile (h : H1) : Prop := RegularProfile h ∧ EnergySquareProfile h

theorem shell_square_moment_integrable (f : SchwartzTensor) (m : ℕ) :
    Integrable (fun y=>shellEnergy y^m*‖f (shellEmbedding y)‖^2) momentumMeasure := by
  letI : momentumMeasure.IsAddHaarMeasure := by unfold momentumMeasure; infer_instance
  exact energy_moment_square_restriction_integrable f shellEmbedding shellEnergy
    (by norm_num : (0:ℝ)≤2) shellEmbedding_proper_bound energy_le_twice_coordinate_norm
    shellEnergy_nonneg shellEmbedding_continuous.measurable shellEnergy_continuous.measurable m

theorem coefficient_square_moment_density_bound (f : SchwartzTensor) (m : ℕ)
    (y : MomentumCoordinates) :
    ‖(orbitalWeight 0 y).toReal • (shellEnergy y^m*‖globalCoefficient f y‖^2)‖≤
      128*(shellEnergy y^(m+1)*‖f (shellEmbedding y)‖^2) := by
  have hp:=shellEnergy_nonneg y
  have hw : (orbitalWeight 0 y).toReal=1/shellEnergy y := by
    unfold orbitalWeight shellEnergy
    exact ENNReal.toReal_ofReal (by positivity)
  rw [hw,smul_eq_mul,Real.norm_of_nonneg
    (mul_nonneg (div_nonneg zero_le_one hp) (mul_nonneg (pow_nonneg hp _) (sq_nonneg _)))]
  by_cases hz : shellEnergy y=0
  · simp [hz]
  · calc
      _ ≤ (1/shellEnergy y)*(shellEnergy y^m*
          (128*shellEnergy y^2*‖f (shellEmbedding y)‖^2)) :=
        mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left
          (globalCoefficient_sq_bound f y) (pow_nonneg hp _)) (div_nonneg zero_le_one hp)
      _ = _ := by rw [pow_succ]; field_simp [hz]; ring

theorem momentumSmear_energySquare (f : SchwartzTensor) :
    EnergySquareProfile (momentumSmearCLM f) := by
  intro m
  have hi : Integrable (fun y=>shellEnergy y^m*‖globalCoefficient f y‖^2) (orbitalMeasure 0) := by
    change Integrable _ (momentumMeasure.withDensity (orbitalWeight 0))
    apply (integrable_withDensity_iff_integrable_smul' (orbitalWeight_measurable 0)
      (Filter.Eventually.of_forall (fun y=>ENNReal.ofReal_lt_top))).mpr
    apply ((shell_square_moment_integrable f (m+1)).const_mul 128).mono'
    · exact (((orbitalWeight_measurable 0).ennreal_toReal).mul
        ((shellEnergy_continuous.measurable.pow_const m).mul
          ((globalCoefficient_measurable f).norm.pow_const 2))).aestronglyMeasurable
    · exact Filter.Eventually.of_forall (coefficient_square_moment_density_bound f m)
  apply hi.congr
  filter_upwards [(globalCoefficient_memLp f).coeFn_toLp] with y hy
  change shellEnergy y^m*‖globalCoefficient f y‖^2= shellEnergy y^m*‖momentumSmear f y‖^2
  rw [hy]

theorem physicalSmear_strongRegular (f : SchwartzTensor) :
    StrongRegularProfile (physicalSmearCLM f) :=
  ⟨physicalSmear_regular f,momentumSmear_energySquare (physicalFourierCLM f)⟩

theorem energySquareProfile_zero : EnergySquareProfile (0:H1) := by
  intro m
  apply (integrable_zero _ _ _).congr
  filter_upwards [Lp.coeFn_zero Fib 2 (orbitalMeasure 0)] with y hy
  simp only [hy,norm_zero,zero_pow (by norm_num : (2:ℕ)≠0),mul_zero,Pi.zero_apply]

theorem strongRegularProfile_zero : StrongRegularProfile (0:H1) :=
  ⟨regularProfile_zero,energySquareProfile_zero⟩

theorem exists_nonzero_strongRegularProfile : ∃ h : H1,StrongRegularProfile h ∧ h≠0 := by
  obtain ⟨f,hf⟩:=exists_nonzero_real_physicalSmear
  exact ⟨physicalSmearCLM f.val,physicalSmear_strongRegular f.val,hf⟩

theorem strongRegular_finite_energy (h : H1) (hh : StrongRegularProfile h) :
    Integrable (fun y=>shellEnergy y*‖h y‖^2) (orbitalMeasure 0) := by
  simpa only [pow_one] using hh.2 1

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.momentumSmear_energySquare
#print axioms F1Fecho.MaxwellGlobal.physicalSmear_strongRegular
#print axioms F1Fecho.MaxwellGlobal.strongRegularProfile_zero
#print axioms F1Fecho.MaxwellGlobal.exists_nonzero_strongRegularProfile
#print axioms F1Fecho.MaxwellGlobal.strongRegular_finite_energy
