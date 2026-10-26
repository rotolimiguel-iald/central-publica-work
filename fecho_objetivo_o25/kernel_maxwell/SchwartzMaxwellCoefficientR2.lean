import CartesianMaxwellBivectorR6
import SchwartzRestrictionEstimateR2
import TGLExt.TheImportedSecondQuantization
import Mathlib.Analysis.Fourier.FourierTransformDeriv

/-! A Schwartz tensor restricted to the concrete mass shell gives a globally
measurable photon coefficient with an energy-square bound. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Matrix SchwartzMap Filter
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open scoped FourierTransform ENNReal
abbrev TensorValue := Matrix (Fin 4) (Fin 4) ℂ
abbrev SchwartzTensor := 𝓢(Spacetime,TensorValue)

def globalCoefficient (f : SchwartzTensor) (y : MomentumCoordinates) : Fib :=
  WithLp.toLp 2 (fun j => (1/2:ℂ)*∑ μ,∑ ν,
    (cartesianStrength y j μ ν:ℂ)*f (shellEmbedding y) μ ν)

theorem globalCoefficient_measurable (f : SchwartzTensor) : Measurable (globalCoefficient f) := by
  apply (PiLp.continuous_toLp 2 (fun _ : Fin 2 => ℂ)).measurable.comp
  apply measurable_pi_lambda
  intro j
  apply measurable_const.mul
  apply Finset.measurable_sum
  intro μ _
  apply Finset.measurable_sum
  intro ν _
  exact (Complex.continuous_ofReal.measurable.comp (cartesianStrength_measurable j μ ν)).mul
    ((measurable_pi_apply ν).comp ((measurable_pi_apply μ).comp
      (f.continuous.measurable.comp shellEmbedding_continuous.measurable)))

theorem globalCoefficient_component_bound (f : SchwartzTensor) (y : MomentumCoordinates) (j : Fin 2) :
    ‖globalCoefficient f y j‖ ≤ 8*shellEnergy y*‖f (shellEmbedding y)‖ := by
  have hb (μ ν : Fin 4) :
      ‖(cartesianStrength y j μ ν:ℂ)*f (shellEmbedding y) μ ν‖ ≤ shellEnergy y*‖f (shellEmbedding y)‖ := by
    rw [norm_mul,Complex.norm_real,Real.norm_eq_abs]
    exact mul_le_mul (cartesianStrength_bound y j μ ν)
      ((norm_le_pi_norm (f (shellEmbedding y) μ) ν).trans (norm_le_pi_norm (f (shellEmbedding y)) μ))
      (norm_nonneg _) (shellEnergy_nonneg y)
  change ‖(1/2:ℂ)*(∑ μ,∑ ν,(cartesianStrength y j μ ν:ℂ)*f (shellEmbedding y) μ ν)‖ ≤ _
  rw [norm_mul]
  norm_num only [norm_div,norm_one,Complex.norm_ofNat]
  have hs : ‖∑ μ,∑ ν,(cartesianStrength y j μ ν:ℂ)*f (shellEmbedding y) μ ν‖ ≤
      ∑ μ : Fin 4,∑ ν : Fin 4,shellEnergy y*‖f (shellEmbedding y)‖ := by
    apply (norm_sum_le _ _).trans
    apply Finset.sum_le_sum
    intro μ _
    apply (norm_sum_le _ _).trans
    exact Finset.sum_le_sum (fun ν _ => hb μ ν)
  have hh:=mul_le_mul_of_nonneg_left hs (by norm_num : (0:ℝ)≤1/2)
  convert hh using 1 <;> norm_num <;> ring

theorem globalCoefficient_sq_bound (f : SchwartzTensor) (y : MomentumCoordinates) :
    ‖globalCoefficient f y‖^2 ≤ 128*shellEnergy y^2*‖f (shellEmbedding y)‖^2 := by
  rw [PiLp.norm_sq_eq_of_L2]
  have hs:=Finset.sum_le_sum (fun (j : Fin 2) (_ : j∈Finset.univ) =>
    pow_le_pow_left₀ (norm_nonneg _) (globalCoefficient_component_bound f y j) 2)
  convert hs using 1 <;> norm_num <;> ring

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.globalCoefficient_measurable
#print axioms F1Fecho.MaxwellGlobal.globalCoefficient_component_bound
#print axioms F1Fecho.MaxwellGlobal.globalCoefficient_sq_bound
