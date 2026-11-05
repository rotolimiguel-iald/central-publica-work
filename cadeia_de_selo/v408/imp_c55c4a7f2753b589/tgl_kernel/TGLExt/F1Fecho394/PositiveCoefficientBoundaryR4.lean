import TGLExt.F1Fecho394.DominatedWithinIntegralR3
import TGLExt.F1Fecho394.HalfPlaneBoundaryUniquenessR4
import TGLExt.O16.PositiveEnergyIntegral_v4
import Mathlib.Analysis.Calculus.MeanValue

/-! Positive-frequency coefficients with an integrable first moment have
derivatives up to the boundary. Vanishing on the positive real ray then
forces vanishing on the entire closed upper half-plane. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
open MeasureTheory Filter Set Complex
open scoped Topology
namespace F1Fecho.PositiveCoefficientBoundary
open ChatgptAudit.PositiveEnergy016 HalfPlaneBoundary

theorem phase_derivative_bound (r : ℝ) (hr : 0≤r) (z : ℂ) (hz : z∈upper) :
    ‖((r:ℂ)*Complex.I)*spectralPhase z r‖≤r := by
  rw [norm_mul,norm_mul,Complex.norm_real,Real.norm_eq_abs,abs_of_nonneg hr,Complex.norm_I,mul_one]
  exact (mul_le_mul_of_nonneg_left (spectralPhase_norm_le_one z r hz hr) hr).trans_eq (mul_one r)

theorem phase_lipschitz (r : ℝ) (hr : 0≤r) (z w : ℂ) (hz : z∈upper) (hw : w∈upper) :
    ‖spectralPhase w r-spectralPhase z r‖≤r*‖w-z‖ := by
  exact Convex.norm_image_sub_le_of_norm_hasDerivWithin_le
    (fun z _ => (spectralPhase_hasDerivAt z r).hasDerivWithinAt)
    (fun z hz => phase_derivative_bound r hr z hz)
    (convex_halfSpace_im_ge 0) hz hw

variable {X : Type*} [MeasurableSpace X] (μ : Measure X)
  (p : X→ℝ) (hp : Measurable p) (hpos : ∀ x,0≤p x)
  (h : X→ℂ) (hh : Integrable h μ)
  (hm : Integrable (fun x=>p x*‖h x‖) μ)

def coefficient (z : ℂ) : ℂ := ∫ x,spectralPhase z (p x)*h x ∂μ

include hp hpos hh

theorem integrable_coefficient (z : ℂ) (hz : z∈upper) :
    Integrable (fun x=>spectralPhase z (p x)*h x) μ := by
  apply hh.norm.mono'
    ((spectralPhase_measurable p hp z).aestronglyMeasurable.mul hh.aestronglyMeasurable)
  apply ae_of_all
  intro x
  change ‖spectralPhase z (p x)*h x‖≤‖h x‖
  rw [norm_mul]
  exact (mul_le_mul_of_nonneg_right (spectralPhase_norm_le_one z (p x) hz (hpos x))
    (norm_nonneg _)).trans_eq (one_mul _)

include hm

theorem coefficient_derivative (z : ℂ) (hz : z∈upper) :
    HasDerivWithinAt (coefficient μ p h)
      (∫x,((p x:ℂ)*Complex.I)*spectralPhase z (p x)*h x ∂μ) upper z := by
  have hD : Integrable (fun x=>((p x:ℂ)*Complex.I)*spectralPhase z (p x)*h x) μ := by
    apply hm.mono'
    · exact ((((Complex.continuous_ofReal.measurable.comp hp).mul_const Complex.I).mul
        (spectralPhase_measurable p hp z)).aestronglyMeasurable.mul hh.aestronglyMeasurable)
    · apply ae_of_all
      intro x
      rw [norm_mul]
      exact mul_le_mul_of_nonneg_right (phase_derivative_bound (p x) (hpos x) z hz) (norm_nonneg _)
  apply DominatedWithin.integral_hasDerivWithinAt μ
    (fun w hw=>integrable_coefficient μ p hp hpos h hh w hw) hz hD hm
    (ae_of_all _ fun x=>mul_nonneg (hpos x) (norm_nonneg _))
  · apply ae_of_all
    intro x w hw
    rw [←sub_mul,norm_mul]
    calc
      ‖spectralPhase w (p x)-spectralPhase z (p x)‖*‖h x‖ ≤
        (p x*‖w-z‖)*‖h x‖ := mul_le_mul_of_nonneg_right
          (phase_lipschitz (p x) (hpos x) z w hz hw) (norm_nonneg _)
      _ = (p x*‖h x‖)*‖w-z‖ := by ring
  · exact ae_of_all _ fun x=>(spectralPhase_hasDerivAt z (p x)).mul_const (h x) |>.hasDerivWithinAt

theorem vanishes_from_positive_ray
    (hz : ∀ t:ℝ,0<t→coefficient μ p h t=0) :
    ∀ z∈upper,coefficient μ p h z=0 := by
  have hd : ∀ z∈upper,∃d,HasDerivWithinAt (coefficient μ p h) d upper z :=
    fun z hz=>⟨_,coefficient_derivative μ p hp hpos h hh hm z hz⟩
  have hu : EqOn (coefficient μ p h) (fun _=>0) interiorUpper :=
    HalfPlaneBoundary.eq_zero_on_upper (coefficient μ p h) hd hz
  apply hu.of_subset_closure
  · intro z hz
    obtain ⟨d,hd⟩:=hd z hz
    exact hd.continuousWithinAt
  · exact continuousOn_const
  · intro z hz
    exact (show 0 ≤ z.im from le_of_lt (show 0 < z.im from hz))
  · change {z:ℂ|0≤z.im}⊆closure {z:ℂ|0<z.im}
    rw [Complex.closure_setOf_lt_im]

end F1Fecho.PositiveCoefficientBoundary
#print axioms F1Fecho.PositiveCoefficientBoundary.phase_lipschitz
#print axioms F1Fecho.PositiveCoefficientBoundary.coefficient_derivative
#print axioms F1Fecho.PositiveCoefficientBoundary.vanishes_from_positive_ray
