import TGLExt.MetricEinsteinVariation
import TGLExt.MixedGibbsGravitationalBridge
import Mathlib.Analysis.Calculus.FDeriv.Analytic
import Mathlib.Analysis.Calculus.Deriv.Abs
import Mathlib.Analysis.SpecialFunctions.Sqrt

set_option autoImplicit false
set_option maxHeartbeats 4000000
namespace ChatgptAudit.ScalarMatterVariation
open Matrix Filter Topology Set
  ChatgptAudit.MetricVariation ChatgptAudit.Coherent023
  ChatgptAudit.FiniteCoherentSource ChatgptAudit.ConeVolume
noncomputable section

def determinantMultilinear : ContinuousMultilinearMap ℝ (fun _ : Fin 4 => Fin 4 → ℝ) ℝ :=
  { Matrix.detRowAlternating.toMultilinearMap with cont := Matrix.continuous_det }

theorem determinant_row_first_variation (g h : Tensor4) :
    HasDerivAt (fun t : ℝ => (g+t • h).det)
      (∑ i : Fin 4, (Matrix.updateRow g i (h i)).det) 0 := by
  have H := (determinantMultilinear.hasFDerivAt g).comp_hasDerivAt_of_eq
    (0:ℝ) (matrix_affine_derivative g h) (by simp)
  simpa only [ContinuousMultilinearMap.linearDeriv_apply, determinantMultilinear,
    Function.comp_def] using H

theorem determinant_row_replacement (g h : Tensor4) (hg : IsUnit g) (i : Fin 4) :
    (Matrix.updateRow g i (h i)).det = (h*g⁻¹) i i * g.det := by
  have hl : h*g⁻¹*g=h := by rw [Matrix.mul_assoc,Matrix.nonsing_inv_mul _ (Matrix.isUnit_det.mpr hg),Matrix.mul_one]
  have he : h i = ∑ j : Fin 4, (h*g⁻¹) i j • g j := by
    funext k
    simpa only [Matrix.mul_apply,Finset.sum_apply,Pi.smul_apply,smul_eq_mul] using congrFun (congrFun hl i) k |>.symm
  rw [he,Matrix.det_updateRow_sum]

theorem determinant_first_variation (g h : Tensor4) (hg : IsUnit g) :
    HasDerivAt (fun t : ℝ => (g+t • h).det) (g.det*(h*g⁻¹).trace) 0 := by
  convert! determinant_row_first_variation g h using 1
  simp only [determinant_row_replacement g h hg,Matrix.trace,←Finset.sum_mul]
  ring

#print axioms determinantMultilinear
#print axioms determinant_row_first_variation
#print axioms determinant_row_replacement
#print axioms determinant_first_variation
end
end ChatgptAudit.ScalarMatterVariation
