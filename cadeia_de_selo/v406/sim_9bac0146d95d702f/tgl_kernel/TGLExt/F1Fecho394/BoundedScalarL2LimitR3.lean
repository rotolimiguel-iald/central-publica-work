import TGLExt.V350StrongOperatorField
import TGLExt.V350FourierL1L2
import Mathlib.MeasureTheory.Integral.DominatedConvergence

/-! Bounded complex scalar multiplication on the existing vector L2 space.
The strong limit is proved by dominated convergence of squared norms. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter
open scoped Topology
namespace F1Fecho.BoundedScalarL2
open TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def field (w : ℝ → ℂ) (hw : Continuous w) (C : ℝ) (hC : 0 ≤ C)
    (hbound : ∀ r, ‖w r‖ ≤ C) : TGLV350.StrongIntegral.Family (H:=H) where
  op r := w r • ContinuousLinearMap.id ℂ H
  continuous_apply v := hw.smul continuous_const
  bound := C
  bound_nonneg := hC
  norm_bound r := ContinuousLinearMap.opNorm_le_bound _ hC (fun v => by
    change ‖w r • v‖ ≤ C*‖v‖
    rw [norm_smul]
    exact mul_le_mul_of_nonneg_right (hbound r) (norm_nonneg v))

def multiply (w : ℝ → ℂ) (hw : Continuous w) (C : ℝ) (hC : 0 ≤ C)
    (hbound : ∀ r, ‖w r‖ ≤ C) : RegularHilbert H →L[ℂ] RegularHilbert H :=
  operatorFieldLift (field w hw C hC hbound)

theorem multiply_ae (w : ℝ → ℂ) (hw : Continuous w) (C : ℝ) (hC : 0 ≤ C)
    (hbound : ∀ r, ‖w r‖ ≤ C) (f : RegularHilbert H) :
    multiply w hw C hC hbound f =ᵐ[volume] fun r => w r • f r :=
  operatorFieldLift_ae (field w hw C hC hbound) f

theorem multiply_tendsto (w : ℕ → ℝ → ℂ) (hw : ∀ n, Continuous (w n))
    (C : ℝ) (hC : 0 ≤ C) (hbound : ∀ n r, ‖w n r‖ ≤ C)
    (hlim : ∀ r, Tendsto (fun n => w n r) atTop (𝓝 1)) (f : RegularHilbert H) :
    Tendsto (fun n => multiply (w n) (hw n) C hC (hbound n) f) atTop (𝓝 f) := by
  let g := fun n r => w n r • f r - f r
  have hb (n r) : ‖g n r‖ ≤ (C+1)*‖f r‖ := by
    calc
      _ ≤ ‖w n r • f r‖+‖f r‖ := norm_sub_le _ _
      _ ≤ C*‖f r‖+‖f r‖ := by
        rw [norm_smul]
        exact add_le_add (mul_le_mul_of_nonneg_right (hbound n r) (norm_nonneg (f r))) le_rfl
      _ = _ := by ring
  have hI : Tendsto (fun n => ∫ r, ‖g n r‖^2) atTop (𝓝 (∫ _r : ℝ, (0:ℝ))) := by
    apply tendsto_integral_filter_of_dominated_convergence (fun r => (C+1)^2*‖f r‖^2)
    · exact Eventually.of_forall fun n =>
        (((hw n).aestronglyMeasurable.smul (Lp.aestronglyMeasurable f)).sub
          (Lp.aestronglyMeasurable f)).norm.pow 2
    · exact Eventually.of_forall fun n => Eventually.of_forall fun r => by
        rw [Real.norm_eq_abs,abs_of_nonneg (sq_nonneg _)]
        exact (pow_le_pow_left₀ (norm_nonneg _) (hb n r) 2).trans_eq (mul_pow _ _ _)
    · exact ((memLp_two_iff_integrable_sq_norm (Lp.aestronglyMeasurable f)).mp
        (Lp.memLp f)).const_mul ((C+1)^2)
    · exact Eventually.of_forall fun r => by
        have ht : Tendsto (fun n => w n r • f r-f r) atTop (𝓝 ((1:ℂ)•f r-f r)) :=
          ((hlim r).smul (tendsto_const_nhds (x:=f r))).sub tendsto_const_nhds
        simpa only [g,one_smul,sub_self,norm_zero,zero_pow (by norm_num : (2:ℕ)≠0)] using ht.norm.pow 2
  have he (n) : ‖multiply (w n) (hw n) C hC (hbound n) f-f‖^2=∫ r,‖g n r‖^2 := by
    rw [← TGLV350.Fourier.L2_integral_norm_sq]
    apply integral_congr_ae
    filter_upwards [Lp.coeFn_sub (multiply (w n) (hw n) C hC (hbound n) f) f,
      multiply_ae (w n) (hw n) C hC (hbound n) f] with r hs hm
    simp only [Pi.sub_apply] at hs
    rw [hs,hm]
  have hs : Tendsto (fun n => ‖multiply (w n) (hw n) C hC (hbound n) f-f‖^2)
      atTop (𝓝 (0:ℝ)) := by simpa only [he,integral_zero] using hI
  have hn := Real.continuous_sqrt.continuousAt.tendsto.comp hs
  apply tendsto_iff_dist_tendsto_zero.mpr
  simpa only [Function.comp_def,Real.sqrt_sq_eq_abs,abs_norm,Real.sqrt_zero,dist_eq_norm] using hn

end F1Fecho.BoundedScalarL2
#print axioms F1Fecho.BoundedScalarL2.multiply_ae
#print axioms F1Fecho.BoundedScalarL2.multiply_tendsto
