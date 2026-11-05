import TGLExt.F1Fecho394.WedgeLaplaceIntegralR3
import TGLExt.F1Fecho394.WedgeLaplaceDerivativeR3

/-! Analyticity is derived from the real support and the first Schwartz moment.
The argument does not assume an analytic continuation of the test's shell data. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter Set
open scoped Topology
namespace F1Fecho.WedgeLaplace
open F1Fecho.MaxwellGlobal SchwartzMap

def lowerOpenStrip : Set ℂ := {z | -Real.pi < z.im ∧ z.im < 0}

def integralDeriv (m q₂ q₃ : ℝ) (f : 𝓢(Spacetime,ℂ)) (z : ℂ) (x : Spacetime) : ℂ :=
  kernelDeriv m (x 0) (x 1) (q₂*x 2+q₃*x 3) z*f x

theorem integralDeriv_bound (m q₂ q₃ M : ℝ) (f : 𝓢(Spacetime,ℂ)) (z : ℂ)
    (hm : 0 ≤ m) (hf : supportedRight f) (hz : z ∈ lowerClosedStrip)
    (hr : |z.re| ≤ M) (x : Spacetime) :
    ‖integralDeriv m q₂ q₃ f z x‖ ≤ (4* |m| * Real.exp M)*(‖x‖*‖f x‖) := by
  by_cases hx : f x=0
  · simp [integralDeriv,hx]
  · have hk : ‖kernelDeriv m (x 0) (x 1) (q₂*x 2+q₃*x 3) z‖ ≤
        2* |m| * (|x 0|+|x 1|)*Real.exp M := by
      conv_lhs => rw [complex_as_lower z]
      simpa only [Complex.ofReal_neg] using kernelDeriv_bound m (x 0) (x 1) _ M z.re (-z.im) hm (hf x hx).le
        (neg_nonneg.mpr hz.2) (by linarith [hz.1]) hr
    have hb : 2* |m| * (|x 0|+|x 1|)*Real.exp M ≤ (4* |m| * Real.exp M)*‖x‖ := by
      have h0 : |x 0| ≤ ‖x‖ := PiLp.norm_apply_le x 0
      have h1 : |x 1| ≤ ‖x‖ := PiLp.norm_apply_le x 1
      calc
        _ = (2* |m| * Real.exp M)*(|x 0|+|x 1|) := by ring
        _ ≤ (2* |m| * Real.exp M)*(2*‖x‖) :=
          mul_le_mul_of_nonneg_left (by linarith) (by positivity)
        _ = _ := by ring
    rw [integralDeriv,norm_mul]
    calc
      _ ≤ ((4* |m| * Real.exp M)*‖x‖)*‖f x‖ :=
        mul_le_mul_of_nonneg_right (hk.trans hb) (norm_nonneg _)
      _ = _ := by ring

theorem scalarLaplace_differentiableAt (m q₂ q₃ : ℝ) (f : 𝓢(Spacetime,ℂ)) (z : ℂ)
    (hm : 0 ≤ m) (hf : supportedRight f) (hz : z ∈ lowerOpenStrip) :
    DifferentiableAt ℂ (scalarLaplace m q₂ q₃ f) z := by
  let M := |z.re|+1
  let U : Set ℂ := {w | |w.re| < M ∧ -Real.pi < w.im ∧ w.im < 0}
  have hU : U ∈ 𝓝 z := by
    apply ((isOpen_lt Complex.continuous_re.abs continuous_const).inter
      ((isOpen_lt continuous_const Complex.continuous_im).inter
        (isOpen_lt Complex.continuous_im continuous_const))).mem_nhds
    exact ⟨by dsimp [M]; linarith,hz⟩
  have hdm : AEStronglyMeasurable (integralDeriv m q₂ q₃ f z) volume := by
    apply Continuous.aestronglyMeasurable
    unfold integralDeriv kernelDeriv longitudinalDeriv kernel longitudinal
    fun_prop
  have hbound : Integrable (fun x : Spacetime => (4* |m| * Real.exp M)*(‖x‖*‖f x‖)) := by
    simpa only [pow_one] using (f.integrable_pow_mul volume 1).const_mul (4* |m| * Real.exp M)
  have hder : ∀ᵐ x ∂volume, ∀ w ∈ U,
      HasDerivAt (fun v => integrand m q₂ q₃ f v x) (integralDeriv m q₂ q₃ f w x) w := by
    apply ae_of_all
    intro x w _
    exact (kernel_hasDerivAt m (x 0) (x 1) (q₂*x 2+q₃*x 3) w).mul_const (f x)
  have hb : ∀ᵐ x ∂volume, ∀ w ∈ U,
      ‖integralDeriv m q₂ q₃ f w x‖ ≤ (4* |m| * Real.exp M)*(‖x‖*‖f x‖) := by
    apply ae_of_all
    intro x w hw
    exact integralDeriv_bound m q₂ q₃ M f w hm hf ⟨hw.2.1.le,hw.2.2.le⟩ hw.1.le x
  exact (hasDerivAt_integral_of_dominated_loc_of_deriv_le (μ:=volume) hU
    (Eventually.of_forall (integrand_measurable m q₂ q₃ f))
    (integrand_integrable m q₂ q₃ f z hm hf ⟨hz.1.le,hz.2.le⟩)
    hdm hb hbound hder).2.differentiableAt

theorem scalarLaplace_diffContOnCl (m q₂ q₃ : ℝ) (f : 𝓢(Spacetime,ℂ))
    (hm : 0 ≤ m) (hf : supportedRight f) :
    DiffContOnCl ℂ (scalarLaplace m q₂ q₃ f) lowerOpenStrip := by
  constructor
  · intro z hz
    exact (scalarLaplace_differentiableAt m q₂ q₃ f z hm hf hz).differentiableWithinAt
  · apply (scalarLaplace_continuous_closed m q₂ q₃ f hm hf).mono
    apply closure_minimal
    · intro z hz
      exact ⟨hz.1.le,hz.2.le⟩
    · exact (isClosed_le continuous_const Complex.continuous_im).inter
        (isClosed_le Complex.continuous_im continuous_const)

end F1Fecho.WedgeLaplace
#print axioms F1Fecho.WedgeLaplace.integralDeriv_bound
#print axioms F1Fecho.WedgeLaplace.scalarLaplace_differentiableAt
#print axioms F1Fecho.WedgeLaplace.scalarLaplace_diffContOnCl
