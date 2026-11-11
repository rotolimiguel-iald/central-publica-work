import TGLExt.F1Fecho394.StripPhaseBoundsR1
import Mathlib.Analysis.Complex.ReImTopology
/-! A two-sided exponential-moment strip theorem. This consumes an integrable
dominator derived from the two vectors' true half-modular domains; it does not
assume analyticity. The application to the concrete modular operator is a
separate consumer. No KMS boundary exchange is assumed or concluded here. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory Filter Set
open scoped Topology
namespace F1Fecho.StripIntegral
open F1Fecho.StripPhase ChatgptAudit.PositiveEnergy016
variable {X : Type*} [MeasurableSpace X]

def bound (a : X→ℂ) (h : X→ℝ) (x : X) : ℝ := ‖a x‖*(1+Real.exp (h x))
def transform (μ : Measure X) (a : X→ℂ) (h : X→ℝ) (z : ℂ) : ℂ :=
  ∫ x, a x*phase z (h x) ∂μ

theorem integrand_measurable (μ : Measure X) (a : X→ℂ) (h : X→ℝ)
    (ha : AEStronglyMeasurable a μ) (hh : Measurable h) (z : ℂ) :
    AEStronglyMeasurable (fun x => a x*phase z (h x)) μ :=
  ha.mul (spectralPhase_measurable (fun x => -h x) hh.neg z).aestronglyMeasurable

theorem integrand_bound (a : X→ℂ) (h : X→ℝ) (z : ℂ)
    (hz0 : 0≤z.im) (hz1 : z.im≤1) (x : X) :
    ‖a x*phase z (h x)‖ ≤ bound a h x := by
  rw [norm_mul]
  exact mul_le_mul_of_nonneg_left (phase_bound z (h x) hz0 hz1) (norm_nonneg _)

theorem integrand_integrable (μ : Measure X) (a : X→ℂ) (h : X→ℝ)
    (ha : AEStronglyMeasurable a μ) (hh : Measurable h)
    (hb : Integrable (bound a h) μ) (z : ℂ) (hz0 : 0≤z.im) (hz1 : z.im≤1) :
    Integrable (fun x => a x*phase z (h x)) μ :=
  hb.mono' (integrand_measurable μ a h ha hh z)
    (ae_of_all _ (integrand_bound a h z hz0 hz1))

theorem transform_bound (μ : Measure X) (a : X→ℂ) (h : X→ℝ)
    (hb : Integrable (bound a h) μ) (z : ℂ) (hz0 : 0≤z.im) (hz1 : z.im≤1) :
    ‖transform μ a h z‖ ≤ ∫ x, bound a h x ∂μ :=
  norm_integral_le_of_norm_le hb (ae_of_all _ (integrand_bound a h z hz0 hz1))

theorem transform_differentiableAt (μ : Measure X) (a : X→ℂ) (h : X→ℝ)
    (ha : AEStronglyMeasurable a μ) (hh : Measurable h)
    (hb : Integrable (bound a h) μ) (z : ℂ) (hz0 : 0<z.im) (hz1 : z.im<1) :
    DifferentiableAt ℂ (transform μ a h) z := by
  let δ : ℝ := min z.im (1-z.im)/2
  have hd : 0<δ := by dsimp [δ]; positivity
  have hd0 : δ<z.im := by
    have hm := min_le_left z.im (1-z.im)
    dsimp [δ]
    linarith
  have hd1 : z.im<1-δ := by
    have hm := min_le_right z.im (1-z.im)
    dsimp [δ]
    linarith
  let U : Set ℂ := {w | δ<w.im ∧ w.im<1-δ}
  have hU : U∈𝓝 z :=
    ((isOpen_lt continuous_const Complex.continuous_im).inter
      (isOpen_lt Complex.continuous_im continuous_const)).mem_nhds ⟨hd0,hd1⟩
  have hm : ∀ᶠ w in 𝓝 z, AEStronglyMeasurable (fun x => a x*phase w (h x)) μ :=
    Eventually.of_forall (integrand_measurable μ a h ha hh)
  have hdm : AEStronglyMeasurable
      (fun x => a x*(((-h x : ℝ) : ℂ)*Complex.I*phase z (h x))) μ := by
    apply ha.mul
    exact (((Complex.continuous_ofReal.measurable.comp hh.neg).mul_const Complex.I).mul
      (spectralPhase_measurable (fun x => -h x) hh.neg z)).aestronglyMeasurable
  have hdb : ∀ᵐ x ∂μ, ∀ w∈U,
      ‖a x*(((-h x : ℝ) : ℂ)*Complex.I*phase w (h x))‖ ≤ (1/δ)*bound a h x := by
    apply ae_of_all
    intro x w hw
    rw [norm_mul]
    calc
      _ ≤ ‖a x‖*((1/δ)*(1+Real.exp (h x))) :=
        mul_le_mul_of_nonneg_left (derivative_bound w (h x) δ hd hw.1.le hw.2.le) (norm_nonneg _)
      _ = _ := by unfold bound; ring
  have hder : ∀ᵐ x ∂μ, ∀ w∈U,
      HasDerivAt (fun v => a x*phase v (h x))
        (a x*(((-h x : ℝ) : ℂ)*Complex.I*phase w (h x))) w :=
    ae_of_all _ (fun x w _ => (phase_derivative w (h x)).const_mul (a x))
  exact (hasDerivAt_integral_of_dominated_loc_of_deriv_le (μ:=μ) hU hm
    (integrand_integrable μ a h ha hh hb z hz0.le hz1.le) hdm hdb
    (hb.const_mul (1/δ)) hder).2.differentiableAt

theorem transform_continuous_closed (μ : Measure X) (a : X→ℂ) (h : X→ℝ)
    (ha : AEStronglyMeasurable a μ) (hh : Measurable h)
    (hb : Integrable (bound a h) μ) :
    ContinuousOn (transform μ a h) {z : ℂ | 0≤z.im ∧ z.im≤1} := by
  apply continuousOn_of_dominated (bound:=bound a h)
  · intro z _
    exact integrand_measurable μ a h ha hh z
  · intro z hz
    exact ae_of_all _ (integrand_bound a h z hz.1 hz.2)
  · exact hb
  · apply ae_of_all
    intro x
    have hd : Differentiable ℂ (fun z => a x*phase z (h x)) :=
      fun z => ((phase_derivative z (h x)).const_mul (a x)).differentiableAt
    exact hd.continuous.continuousOn

theorem transform_diffContOnCl (μ : Measure X) (a : X→ℂ) (h : X→ℝ)
    (ha : AEStronglyMeasurable a μ) (hh : Measurable h)
    (hb : Integrable (bound a h) μ) :
    DiffContOnCl ℂ (transform μ a h) {z : ℂ | 0<z.im ∧ z.im<1} := by
  constructor
  · intro z hz
    exact (transform_differentiableAt μ a h ha hh hb z hz.1 hz.2).differentiableWithinAt
  · apply (transform_continuous_closed μ a h ha hh hb).mono
    apply closure_minimal
    · intro z hz
      exact ⟨hz.1.le,hz.2.le⟩
    · exact (isClosed_le continuous_const Complex.continuous_im).inter
        (isClosed_le Complex.continuous_im continuous_const)

theorem phase_top (t h : ℝ) : phase ((t:ℂ)+Complex.I) h = (Real.exp h : ℂ)*phase t h := by
  unfold phase spectralPhase
  rw [Complex.ofReal_exp,← Complex.exp_add]
  congr 1
  push_cast
  calc
    ((t:ℂ)+Complex.I)*((-h:ℂ)*Complex.I) =
        (t:ℂ)*((-h:ℂ)*Complex.I)+h := by ring_nf; simp
    _ = _ := by ring

end F1Fecho.StripIntegral
#print axioms F1Fecho.StripIntegral.transform_bound
#print axioms F1Fecho.StripIntegral.transform_diffContOnCl
#print axioms F1Fecho.StripIntegral.phase_top
