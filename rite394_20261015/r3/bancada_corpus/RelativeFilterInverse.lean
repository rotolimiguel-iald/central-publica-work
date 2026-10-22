import LikelihoodCocycleControls

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit.Relative031
open Matrix Filter Topology Set TGLExt ChatgptAudit ChatgptAudit.Cocycle030
  ChatgptAudit.Response028 ChatgptAudit.Profile026 ChatgptAudit.Transport027 ChatgptAudit.Thermal025
noncomputable section

local instance (P : SiteProfile) : NormedAlgebra ℚ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _
local instance (P : SiteProfile) : IsScalarTower ℚ ℂ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  IsScalarTower.restrictScalars ℚ ℂ _

def inverseLikelihoodFilter (b : SummableAmplitude) (t : ℝ) :
    TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference :=
  NormedSpace.exp ((-1/2 : ℂ) • likelihoodGenerator b t)

theorem filter_mul_inverse (b : SummableAmplitude) (t : ℝ) :
    likelihoodFilter b t*inverseLikelihoodFilter b t=1 := by
  have h : Commute ((1/2 : ℂ) • likelihoodGenerator b t)
      ((-1/2 : ℂ) • likelihoodGenerator b t) :=
    ((Commute.refl _).smul_left _).smul_right _
  unfold likelihoodFilter inverseLikelihoodFilter
  rw [←NormedSpace.exp_add_of_commute h,←add_smul]
  norm_num

theorem inverse_mul_filter (b : SummableAmplitude) (t : ℝ) :
    inverseLikelihoodFilter b t*likelihoodFilter b t=1 := by
  have h : Commute ((-1/2 : ℂ) • likelihoodGenerator b t)
      ((1/2 : ℂ) • likelihoodGenerator b t) :=
    ((Commute.refl _).smul_left _).smul_right _
  unfold likelihoodFilter inverseLikelihoodFilter
  rw [←NormedSpace.exp_add_of_commute h,←add_smul]
  norm_num

theorem inverse_filter_selfadjoint (b : SummableAmplitude) (t : ℝ) :
    IsSelfAdjoint (inverseLikelihoodFilter b t) := by
  change star (inverseLikelihoodFilter b t)=inverseLikelihoodFilter b t
  simp [inverseLikelihoodFilter,NormedSpace.star_exp,star_smul,
    (likelihood_generator_selfadjoint b t).star_eq]

theorem inverse_filter_mem_factor (b : SummableAmplitude) (t : ℝ) :
    inverseLikelihoodFilter b t∈theFactorObject thirdThermalReference := by
  apply NormedSpace.exp_mem (R := ℂ) (s := (theFactorObject thirdThermalReference).toStarSubalgebra)
    (factor_norm_closed _)
  exact (theFactorObject thirdThermalReference).toStarSubalgebra.smul_mem
    (likelihood_generator_mem_factor b t) _

def likelihoodFilterEquiv (b : SummableAmplitude) (t : ℝ) :
    TowerHilbert thirdThermalReference ≃L[ℂ] TowerHilbert thirdThermalReference where
  toLinearEquiv :=
    { toFun := likelihoodFilter b t
      invFun := inverseLikelihoodFilter b t
      map_add' := (likelihoodFilter b t).map_add
      map_smul' := (likelihoodFilter b t).map_smul
      left_inv := by
        intro x
        change (inverseLikelihoodFilter b t*likelihoodFilter b t) x=x
        rw [inverse_mul_filter]
        rfl
      right_inv := by
        intro x
        change (likelihoodFilter b t*inverseLikelihoodFilter b t) x=x
        rw [filter_mul_inverse]
        rfl }
  continuous_toFun := (likelihoodFilter b t).continuous
  continuous_invFun := (inverseLikelihoodFilter b t).continuous

theorem filter_equiv_apply (b : SummableAmplitude) (t : ℝ)
    (x : TowerHilbert thirdThermalReference) :
    likelihoodFilterEquiv b t x=likelihoodFilter b t x := rfl

theorem inverse_filter_equiv_apply (b : SummableAmplitude) (t : ℝ)
    (x : TowerHilbert thirdThermalReference) :
    (likelihoodFilterEquiv b t).symm x=inverseLikelihoodFilter b t x := rfl

theorem inverse_filter_vector (b : SummableAmplitude) (t : ℝ) :
    inverseLikelihoodFilter b t (amplitudeVector b t)=hOmega thirdThermalReference := by
  rw [←likelihood_filter_vector b t,←mul_apply_eq_comp,inverse_mul_filter]
  rfl

#print axioms inverseLikelihoodFilter
#print axioms likelihoodFilterEquiv
#print axioms filter_mul_inverse
#print axioms inverse_mul_filter
#print axioms inverse_filter_selfadjoint
#print axioms inverse_filter_mem_factor
#print axioms filter_equiv_apply
#print axioms inverse_filter_equiv_apply
#print axioms inverse_filter_vector
end
end ChatgptAudit.Relative031
