import TGLExt.F1Fecho394.WedgeLaplaceKernelR2
import TGLExt.F1Fecho394.KMSStripIntegralR2

/-! An actual Fourier-Laplace integral of a Schwartz test supported in the
right wedge. Its uniform bound and continuous closed-strip boundary follow
from support and dominated convergence, without an assumed analytic vector. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter Set
namespace F1Fecho.WedgeLaplace
open F1Fecho.MaxwellGlobal SchwartzMap

def lowerClosedStrip : Set ℂ := {z | -Real.pi ≤ z.im ∧ z.im ≤ 0}

theorem complex_as_lower (z : ℂ) : z=(z.re:ℂ)-Complex.I*(-z.im) := by
  apply Complex.ext <;> simp

theorem kernel_bound_at (m t x v : ℝ) (z : ℂ) (hm : 0 ≤ m)
    (hw : |t| ≤ x) (hz : z ∈ lowerClosedStrip) : ‖kernel m t x v z‖ ≤ 1 := by
  rw [complex_as_lower z]
  simpa only [Complex.ofReal_neg] using kernel_norm_le_one_on_right_wedge m t x v z.re (-z.im) hm hw
    (neg_nonneg.mpr hz.2) (by linarith [hz.1])

def supportedRight (f : 𝓢(Spacetime,ℂ)) : Prop :=
  ∀ x ∈ Function.support (f : Spacetime → ℂ), |x 0| < x 1

def integrand (m q₂ q₃ : ℝ) (f : 𝓢(Spacetime,ℂ)) (z : ℂ) (x : Spacetime) : ℂ :=
  kernel m (x 0) (x 1) (q₂*x 2+q₃*x 3) z*f x

def scalarLaplace (m q₂ q₃ : ℝ) (f : 𝓢(Spacetime,ℂ)) (z : ℂ) : ℂ :=
  ∫ x,integrand m q₂ q₃ f z x

theorem integrand_bound (m q₂ q₃ : ℝ) (f : 𝓢(Spacetime,ℂ)) (z : ℂ)
    (hm : 0 ≤ m) (hf : supportedRight f) (hz : z ∈ lowerClosedStrip) (x : Spacetime) :
    ‖integrand m q₂ q₃ f z x‖ ≤ ‖f x‖ := by
  by_cases hx : f x=0
  · simp [integrand,hx]
  · rw [integrand,norm_mul]
    exact mul_le_of_le_one_left (norm_nonneg _) (kernel_bound_at _ _ _ _ _ hm (hf x hx).le hz)

theorem integrand_measurable (m q₂ q₃ : ℝ) (f : 𝓢(Spacetime,ℂ)) (z : ℂ) :
    AEStronglyMeasurable (integrand m q₂ q₃ f z) volume := by
  apply Continuous.aestronglyMeasurable
  unfold integrand kernel longitudinal
  fun_prop

theorem integrand_integrable (m q₂ q₃ : ℝ) (f : 𝓢(Spacetime,ℂ)) (z : ℂ)
    (hm : 0 ≤ m) (hf : supportedRight f) (hz : z ∈ lowerClosedStrip) :
    Integrable (integrand m q₂ q₃ f z) :=
  f.integrable.norm.mono' (integrand_measurable m q₂ q₃ f z)
    (ae_of_all _ (integrand_bound m q₂ q₃ f z hm hf hz))

theorem scalarLaplace_bound (m q₂ q₃ : ℝ) (f : 𝓢(Spacetime,ℂ)) (z : ℂ)
    (hm : 0 ≤ m) (hf : supportedRight f) (hz : z ∈ lowerClosedStrip) :
    ‖scalarLaplace m q₂ q₃ f z‖ ≤ ∫ x,‖f x‖ :=
  norm_integral_le_of_norm_le f.integrable.norm
    (ae_of_all _ (integrand_bound m q₂ q₃ f z hm hf hz))

theorem scalarLaplace_continuous_closed (m q₂ q₃ : ℝ) (f : 𝓢(Spacetime,ℂ))
    (hm : 0 ≤ m) (hf : supportedRight f) :
    ContinuousOn (scalarLaplace m q₂ q₃ f) lowerClosedStrip := by
  apply continuousOn_of_dominated (bound := fun x => ‖f x‖)
  · intro z _
    exact integrand_measurable m q₂ q₃ f z
  · intro z hz
    exact ae_of_all _ (integrand_bound m q₂ q₃ f z hm hf hz)
  · exact f.integrable.norm
  · apply ae_of_all
    intro x
    exact (((kernel_entire m (x 0) (x 1) (q₂*x 2+q₃*x 3)).continuous).mul
      continuous_const).continuousOn

end F1Fecho.WedgeLaplace
#print axioms F1Fecho.WedgeLaplace.kernel_bound_at
#print axioms F1Fecho.WedgeLaplace.integrand_integrable
#print axioms F1Fecho.WedgeLaplace.scalarLaplace_bound
#print axioms F1Fecho.WedgeLaplace.scalarLaplace_continuous_closed
