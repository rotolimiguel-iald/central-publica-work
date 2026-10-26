import MinkowskiSchwartzFourierR4
import Mathlib.Analysis.Distribution.SchwartzSpace.Fourier

/-! Actual spacetime Schwartz tests, Fourier transformed and restricted to the
physical mass shell, are mapped into the original H1. Integrability is proved
from energy cancellation and Schwartz decay, not supplied as a field. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Matrix SchwartzMap Filter
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.SchwartzRestriction
open scoped FourierTransform ENNReal

theorem shell_weighted_square_integrable (f : SchwartzTensor) :
    Integrable (fun y => shellEnergy y*‖f (shellEmbedding y)‖^2) momentumMeasure := by
  letI : momentumMeasure.IsAddHaarMeasure := by unfold momentumMeasure; infer_instance
  exact energy_weighted_square_integrable f shellEmbedding shellEnergy
    (by norm_num : (0:ℝ)≤2) shellEmbedding_proper_bound energy_le_twice_coordinate_norm
    shellEnergy_nonneg shellEmbedding_continuous.measurable shellEnergy_continuous.measurable

theorem density_normsq_bound (f : SchwartzTensor) (y : MomentumCoordinates) :
    ‖(orbitalWeight 0 y).toReal • ‖globalCoefficient f y‖^2‖ ≤
      128*(shellEnergy y*‖f (shellEmbedding y)‖^2) := by
  have hp:=shellEnergy_nonneg y
  have hw : (orbitalWeight 0 y).toReal=1/shellEnergy y := by
    unfold orbitalWeight shellEnergy
    exact ENNReal.toReal_ofReal (by positivity)
  rw [hw,smul_eq_mul,Real.norm_of_nonneg (mul_nonneg (by positivity) (sq_nonneg _))]
  by_cases hz : shellEnergy y=0
  · simp [hz]
  · calc
      (1/shellEnergy y)*‖globalCoefficient f y‖^2 ≤
          (1/shellEnergy y)*(128*shellEnergy y^2*‖f (shellEmbedding y)‖^2) :=
        mul_le_mul_of_nonneg_left (globalCoefficient_sq_bound f y) (by positivity)
      _ = 128*(shellEnergy y*‖f (shellEmbedding y)‖^2) := by field_simp [hz]; ring

theorem globalCoefficient_memLp (f : SchwartzTensor) :
    MemLp (globalCoefficient f) 2 (orbitalMeasure 0) := by
  apply (memLp_two_iff_integrable_sq_norm (globalCoefficient_measurable f).aestronglyMeasurable).mpr
  change Integrable (fun y => ‖globalCoefficient f y‖^2)
    (momentumMeasure.withDensity (orbitalWeight 0))
  apply (integrable_withDensity_iff_integrable_smul' (orbitalWeight_measurable 0)
    (Filter.Eventually.of_forall (fun y => ENNReal.ofReal_lt_top))).mpr
  apply ((shell_weighted_square_integrable f).const_mul 128).mono'
  · exact (((orbitalWeight_measurable 0).ennreal_toReal).mul
      ((globalCoefficient_measurable f).norm.pow_const 2)).aestronglyMeasurable
  · exact Filter.Eventually.of_forall (density_normsq_bound f)

def momentumSmear (f : SchwartzTensor) : H1 :=
  (globalCoefficient_memLp f).toLp (globalCoefficient f)

def spacetimeSmear (f : SchwartzTensor) : H1 := momentumSmear (minkowskiFourier f)

theorem spacetimeSmear_ae (f : SchwartzTensor) :
    spacetimeSmear f =ᵐ[orbitalMeasure 0] globalCoefficient (minkowskiFourier f) :=
  (globalCoefficient_memLp (minkowskiFourier f)).coeFn_toLp

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.shell_weighted_square_integrable
#print axioms F1Fecho.MaxwellGlobal.density_normsq_bound
#print axioms F1Fecho.MaxwellGlobal.globalCoefficient_memLp
#print axioms F1Fecho.MaxwellGlobal.spacetimeSmear
#print axioms F1Fecho.MaxwellGlobal.spacetimeSmear_ae
