import TGLExt.F1Fecho394.KMSStripIntegralR2
import Mathlib.MeasureTheory.Function.L2Space
/-! The exponential-moment hypothesis of the strip integral follows from
the genuine half-modular L2 domains of both vectors. No differentiability or
analytic vector hypothesis is added to these domains. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory Filter Set
open scoped Topology InnerProductSpace
namespace F1Fecho.HalfModularStrip
open F1Fecho.StripPhase F1Fecho.StripIntegral
variable {X E : Type*} [MeasurableSpace X]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E]

def half (h : X→ℝ) (f : X→E) : X→E := fun x => (Real.exp (h x/2) : ℂ) • f x

theorem half_inner (h : X→ℝ) (f g : X→E) (x : X) :
    inner ℂ (half h f x) (half h g x) = (Real.exp (h x) : ℂ)*inner ℂ (f x) (g x) := by
  have he : Real.exp (h x/2)*Real.exp (h x/2)=Real.exp (h x) := by
    rw [← Real.exp_add]
    congr 1
    ring
  simp only [half,inner_smul_left,inner_smul_right,Complex.conj_ofReal]
  rw [← mul_assoc, ← Complex.ofReal_mul, he]

theorem half_norm_product (h : X→ℝ) (f g : X→E) (x : X) :
    ‖half h f x‖*‖half h g x‖ = Real.exp (h x)*(‖f x‖*‖g x‖) := by
  have he : Real.exp (h x/2)*Real.exp (h x/2)=Real.exp (h x) := by
    rw [← Real.exp_add]
    congr 1
    ring
  simp only [half,norm_smul,Complex.norm_real,Real.norm_eq_abs,abs_of_pos (Real.exp_pos _)]
  calc
    (Real.exp (h x/2)*‖f x‖)*(Real.exp (h x/2)*‖g x‖) =
        (Real.exp (h x/2)*Real.exp (h x/2))*(‖f x‖*‖g x‖) := by ring
    _ = _ := by rw [he]

theorem moment_integrable (μ : Measure X) (h : X→ℝ) (hh : Measurable h)
    (f g : X→E) (hf : MemLp f 2 μ) (hg : MemLp g 2 μ)
    (hfhalf : MemLp (half h f) 2 μ) (hghalf : MemLp (half h g) 2 μ) :
    Integrable (bound (fun x => inner ℂ (f x) (g x)) h) μ := by
  have hi := (hf.norm.integrable_mul hg.norm).add (hfhalf.norm.integrable_mul hghalf.norm)
  apply hi.mono'
  · exact (hf.1.inner hg.1).norm.mul
      (aestronglyMeasurable_const.add (Real.continuous_exp.measurable.comp hh).aestronglyMeasurable)
  · apply ae_of_all
    intro x
    simp only [bound, Real.norm_eq_abs, abs_of_nonneg (mul_nonneg (norm_nonneg _)
      (by positivity : 0 ≤ 1+Real.exp (h x))), Pi.add_apply, Pi.mul_apply]
    change ‖inner ℂ (f x) (g x)‖*(1+Real.exp (h x)) ≤
      ‖f x‖*‖g x‖+‖half h f x‖*‖half h g x‖
    rw [half_norm_product]
    have hn := norm_inner_le_norm (𝕜 := ℂ) (f x) (g x)
    nlinarith [Real.exp_pos (h x)]

theorem coefficient_analytic (μ : Measure X) (h : X→ℝ) (hh : Measurable h)
    (f g : X→E) (hf : MemLp f 2 μ) (hg : MemLp g 2 μ)
    (hfhalf : MemLp (half h f) 2 μ) (hghalf : MemLp (half h g) 2 μ) :
    DiffContOnCl ℂ (transform μ (fun x => inner ℂ (f x) (g x)) h)
      {z : ℂ | 0<z.im ∧ z.im<1} :=
  transform_diffContOnCl μ _ h (hf.1.inner hg.1) hh
    (moment_integrable μ h hh f g hf hg hfhalf hghalf)

theorem coefficient_top (μ : Measure X) (h : X→ℝ) (f g : X→E) (t : ℝ) :
    transform μ (fun x => inner ℂ (f x) (g x)) h ((t:ℂ)+Complex.I) =
      transform μ (fun x => inner ℂ (half h f x) (half h g x)) h t := by
  apply integral_congr_ae
  apply ae_of_all
  intro x
  dsimp only
  rw [phase_top,half_inner]
  ring

end F1Fecho.HalfModularStrip
#print axioms F1Fecho.HalfModularStrip.moment_integrable
#print axioms F1Fecho.HalfModularStrip.coefficient_analytic
#print axioms F1Fecho.HalfModularStrip.coefficient_top
