import TGLExt.MetricEinsteinVariation
import TGLExt.MixedGibbsGravitationalBridge
import TGLExt.ConeVolumeReconstruction
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
  { Matrix.detRowAlternating.toMultilinearMap with cont := continuous_id.matrix_det }

theorem determinant_row_first_variation (g h : Tensor4) :
    HasDerivAt (fun t : ℝ => (g+t • h).det)
      (∑ i : Fin 4, (Matrix.updateRow g i (h i)).det) 0 := by
  have H := (determinantMultilinear.hasFDerivAt g).comp_hasDerivAt_of_eq
    (0:ℝ) (matrix_affine_derivative g h) (by simp)
  convert! H using 1
  simp only [ContinuousMultilinearMap.linearDeriv_apply]
  rfl

theorem determinant_row_replacement (g h : Tensor4) (hg : IsUnit g) (i : Fin 4) :
    (Matrix.updateRow g i (h i)).det = (h*g⁻¹) i i * g.det := by
  have hl : h*g⁻¹*g=h := by rw [Matrix.mul_assoc,Matrix.nonsing_inv_mul _ (g.isUnit_iff_isUnit_det.mp hg),Matrix.mul_one]
  have he : h i = ∑ j : Fin 4, (h*g⁻¹) i j • g j := by
    funext k
    simpa only [Matrix.mul_apply,Finset.sum_apply,Pi.smul_apply,smul_eq_mul] using congrFun (congrFun hl i) k |>.symm
  rw [he,Matrix.det_updateRow_sum]
  rfl

theorem determinant_first_variation (g h : Tensor4) (hg : IsUnit g) :
    HasDerivAt (fun t : ℝ => (g+t • h).det) (g.det*(h*g⁻¹).trace) 0 := by
  convert! determinant_row_first_variation g h using 1
  simp only [determinant_row_replacement g h hg,Matrix.trace,Matrix.diag,←Finset.sum_mul]
  ring

theorem absolute_determinant_first_variation (g h : Tensor4) (hg : IsUnit g) :
    HasDerivAt (fun t : ℝ => |(g+t • h).det|) (|g.det|*(h*g⁻¹).trace) 0 := by
  have hd := determinant_first_variation g h hg
  have hn : g.det ≠ 0 := (g.isUnit_iff_isUnit_det.mp hg).ne_zero
  rcases lt_or_gt_of_ne hn with hn | hn
  · have H := (hasDerivAt_abs_neg hn).comp_of_eq 0 hd (by simp)
    simpa only [Function.comp_def,abs_of_neg hn,neg_one_mul,neg_mul] using H
  · have H := (hasDerivAt_abs_pos hn).comp_of_eq 0 hd (by simp)
    simpa only [Function.comp_def,abs_of_pos hn,one_mul] using H

theorem metric_volume_first_variation (g h : Tensor4) (hg : IsUnit g) :
    HasDerivAt (fun t : ℝ => metricVolumeDensity (g+t • h))
      (metricVolumeDensity g/2*(h*g⁻¹).trace) 0 := by
  have hn : |g.det| ≠ 0 := abs_ne_zero.mpr (g.isUnit_iff_isUnit_det.mp hg).ne_zero
  have H := (absolute_determinant_first_variation g h hg).sqrt (by simpa using hn)
  have hs : Real.sqrt |g.det| ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr (abs_pos.mpr (g.isUnit_iff_isUnit_det.mp hg).ne_zero))
  convert! H using 1
  simp only [zero_smul,add_zero,metricVolumeDensity]
  field_simp
  nlinarith [Real.sq_sqrt (abs_nonneg g.det)]

theorem quadratic_inverse_first_variation (g h : Tensor4) (w : Coordinate4) (hg : IsUnit g) :
    HasDerivAt (fun t : ℝ => tensorQuad (g+t • h)⁻¹ w)
      (-tensorQuad (g⁻¹*h*g⁻¹) w) 0 := by
  have hi := matrix_inverse_first_variation g h hg
  have H := HasDerivAt.fun_sum fun i (_ : i∈(Finset.univ : Finset (Fin 4))) =>
    (HasDerivAt.fun_sum fun j (_ : j∈(Finset.univ : Finset (Fin 4))) =>
      (((hasDerivAt_pi.mp (hasDerivAt_pi.mp hi i)) j).mul_const (w j))).const_mul (w i)
  convert! H using 1
  · rfl
  · simp only [tensorQuad,Matrix.mulVec,dotProduct,Matrix.neg_apply,neg_mul,
      Finset.sum_neg_distrib,mul_neg]

def scalarMatterDensity {J : Type} [Fintype J] (g : Tensor4) (w : J → Coordinate4) (c : J → ℝ) : ℝ :=
  metricVolumeDensity g/2 * ∑ j, c j * tensorQuad g⁻¹ (w j)

theorem scalar_density_raw_first_variation {J : Type} [Fintype J]
    (g h : Tensor4) (w : J → Coordinate4) (c : J → ℝ) (hg : IsUnit g) :
    HasDerivAt (fun t : ℝ => scalarMatterDensity (g+t • h) w c)
      (metricVolumeDensity g/2*((h*g⁻¹).trace/2*∑ j, c j*tensorQuad g⁻¹ (w j))-
        metricVolumeDensity g/2*∑ j, c j*tensorQuad (g⁻¹*h*g⁻¹) (w j)) 0 := by
  have Hv := (metric_volume_first_variation g h hg).div_const 2
  have Hq := HasDerivAt.fun_sum fun j (_ : j∈(Finset.univ : Finset J)) =>
    (quadratic_inverse_first_variation g h (w j) hg).const_mul (c j)
  convert! Hv.mul Hq using 1
  simp only [zero_smul,add_zero,mul_neg,Finset.sum_neg_distrib]
  ring

#print axioms determinantMultilinear
#print axioms determinant_row_first_variation
#print axioms determinant_row_replacement
#print axioms determinant_first_variation
#print axioms absolute_determinant_first_variation
#print axioms metric_volume_first_variation
#print axioms quadratic_inverse_first_variation
#print axioms scalarMatterDensity
#print axioms scalar_density_raw_first_variation
end
end ChatgptAudit.ScalarMatterVariation
