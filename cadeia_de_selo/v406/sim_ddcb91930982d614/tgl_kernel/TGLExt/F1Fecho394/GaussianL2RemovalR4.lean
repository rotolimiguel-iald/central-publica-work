import TGLExt.F1Fecho394.BoundedScalarL2LimitR3
import TGLExt.F1Fecho394.LowerGaussianReflectionR1
import Mathlib.Analysis.SpecificLimits.Basic

/-! The actual lower-strip Gaussian regulator tends strongly to identity on
the same vector L2 space. No closed-subspace membership is assumed here. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter
open scoped Topology
namespace F1Fecho.GaussianL2Removal
open WedgeLaplace BoundedScalarL2 ChatgptAudit.LightRayCore016
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def width (n : ℕ) : ℝ := 1/((n:ℝ)+1)
theorem width_pos (n : ℕ) : 0 < width n := by unfold width; positivity
theorem width_le_one (n : ℕ) : width n ≤ 1 := by
  unfold width
  exact (div_le_one (by positivity : 0 < (n:ℝ)+1)).mpr (by linarith [Nat.cast_nonneg (α:=ℝ) n])
theorem width_tendsto : Tendsto width atTop (𝓝 0) := tendsto_one_div_add_atTop_nhds_zero_nat

def bound : ℝ := Real.exp (Real.pi^2/4)
theorem bound_pos : 0 < bound := Real.exp_pos _
theorem regulator_bound (n : ℕ) (r : ℝ) : ‖lowerGaussian (width n) r‖ ≤ bound := by
  apply (lowerGaussian_real_bound (width n) (width_pos n) r).trans
  apply Real.exp_le_exp.mpr
  have h := mul_le_mul_of_nonneg_right (width_le_one n) (sq_nonneg Real.pi)
  nlinarith

theorem regulator_continuous (n : ℕ) : Continuous (fun r : ℝ => lowerGaussian (width n) r) :=
  (lowerGaussian_entire (width n)).continuous.comp Complex.continuous_ofReal

theorem regulator_tendsto (r : ℝ) :
    Tendsto (fun n => lowerGaussian (width n) r) atTop (𝓝 1) := by
  have h := (Complex.continuous_ofReal.continuousAt.tendsto.comp width_tendsto).neg.mul_const
    (((-(r:ℂ))-(0:ℂ)-Complex.I*((Real.pi/2:ℝ):ℂ))^2)
  have he := Complex.continuous_exp.continuousAt.tendsto.comp h
  simpa only [Function.comp_def,lowerGaussian,twistedGaussian,Complex.ofReal_zero,neg_zero,zero_mul,
    Complex.exp_zero] using he

def regularize (n : ℕ) : TGLV350.Regular.RegularHilbert H →L[ℂ]
    TGLV350.Regular.RegularHilbert H :=
  multiply (fun r => lowerGaussian (width n) r) (regulator_continuous n)
    bound bound_pos.le (regulator_bound n)

theorem regularize_ae (n : ℕ) (f : TGLV350.Regular.RegularHilbert H) :
    regularize n f =ᵐ[volume] fun r => lowerGaussian (width n) r • f r :=
  multiply_ae _ _ _ _ _ f

theorem regularize_tendsto (f : TGLV350.Regular.RegularHilbert H) :
    Tendsto (fun n => regularize n f) atTop (𝓝 f) :=
  multiply_tendsto _ regulator_continuous bound bound_pos.le regulator_bound regulator_tendsto f

end F1Fecho.GaussianL2Removal
#print axioms F1Fecho.GaussianL2Removal.regulator_bound
#print axioms F1Fecho.GaussianL2Removal.regulator_tendsto
#print axioms F1Fecho.GaussianL2Removal.regularize_tendsto
