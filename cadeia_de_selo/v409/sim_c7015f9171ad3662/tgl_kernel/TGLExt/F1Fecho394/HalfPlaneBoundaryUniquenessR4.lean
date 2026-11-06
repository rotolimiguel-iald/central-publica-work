import Mathlib.Analysis.Complex.RealDeriv
import Mathlib.Analysis.Complex.Convex
import Mathlib.Analysis.Analytic.IsolatedZeros
import Mathlib.Analysis.Complex.CauchyIntegral

/-! Boundary uniqueness after unilateral regularization. The regularity on
the closed half-plane is explicit; this lemma alone does not regularize a
positive-energy coefficient or assert density of any localized net. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open Set Filter Complex
open scoped Topology
namespace F1Fecho.HalfPlaneBoundary

def upper : Set ℂ := {z | 0 ≤ z.im}
def interiorUpper : Set ℂ := {z | 0 < z.im}
def right : Set ℂ := {z | 0 < z.re}

theorem boundary_derivative_zero (f : ℂ → ℂ) (x : ℝ) (hx : 0 < x)
    (d : ℂ) (hd : HasDerivWithinAt f d upper (x : ℂ))
    (hz : ∀ t : ℝ, 0 < t → f t = 0) : d = 0 := by
  have hreal : HasDerivAt (fun t : ℝ => f (t : ℂ)) d x := by
    simpa only [Function.comp_apply, ofRealCLM_apply, ofReal_one, mul_one] using!
      hd.comp_hasDerivAt x ofRealCLM.hasDerivAt
        (Filter.Eventually.of_forall (fun t : ℝ => by simp [upper]))
  have heq : (fun t : ℝ => f (t : ℂ)) =ᶠ[𝓝 x] fun _ => 0 := by
    filter_upwards [Ioi_mem_nhds hx] with t ht
    exact hz t ht
  exact hreal.unique ((hasDerivAt_const x (0 : ℂ)).congr_of_eventuallyEq heq)

def zeroExtension (f : ℂ → ℂ) (z : ℂ) : ℂ := if 0 ≤ z.im then f z else 0

theorem zeroExtension_differentiable (f : ℂ → ℂ)
    (hd : ∀ z ∈ upper, ∃ d, HasDerivWithinAt f d upper z)
    (hz : ∀ t : ℝ, 0 < t → f t = 0) :
    DifferentiableOn ℂ (zeroExtension f) right := by
  intro z hzr
  by_cases hp : 0 < z.im
  · obtain ⟨d,hd⟩ := hd z hp.le
    have hn : upper ∈ 𝓝 z := mem_of_superset
      ((isOpen_lt continuous_const continuous_im).mem_nhds hp) (fun w h => (show 0 ≤ w.im from le_of_lt h))
    have he : zeroExtension f =ᶠ[𝓝 z] f := by
      filter_upwards [hn] with w hw
      exact if_pos (show 0 ≤ w.im from hw)
    exact ((hd.hasDerivAt hn).congr_of_eventuallyEq he).differentiableAt.differentiableWithinAt
  · by_cases hn : z.im < 0
    · have he : zeroExtension f =ᶠ[𝓝 z] fun _ => 0 := by
        filter_upwards [(isOpen_lt continuous_im continuous_const).mem_nhds hn] with w hw
        simp only [zeroExtension,if_neg (not_le_of_gt hw)]
      exact ((hasDerivAt_const z (0 : ℂ)).congr_of_eventuallyEq he).differentiableAt.differentiableWithinAt
    · have hi : z.im = 0 := le_antisymm (le_of_not_gt hp) (le_of_not_gt hn)
      have hzre : (z.re : ℂ) = z := by apply Complex.ext <;> simp [hi]
      obtain ⟨d,hdf⟩ := hd z (by simp [upper,hi])
      have hd0 : d=0 := boundary_derivative_zero f z.re hzr d (hzre.symm ▸ hdf) hz
      subst d
      have hU : HasDerivWithinAt (zeroExtension f) 0 upper z := by
        apply hdf.congr
        · intro w hw
          exact if_pos hw
        · exact if_pos (by simp [hi])
      have hL : HasDerivWithinAt (zeroExtension f) 0 {w : ℂ | w.im ≤ 0 ∧ 0 < w.re} z := by
        apply (hasDerivWithinAt_const z {w : ℂ | w.im ≤ 0 ∧ 0 < w.re} (0 : ℂ)).congr
        · intro w hw
          by_cases he : 0 ≤ w.im
          · have hwi : w.im=0 := le_antisymm hw.1 he
            have hwr : (w.re : ℂ)=w := by apply Complex.ext <;> simp [hwi]
            simp only [zeroExtension,if_pos he]
            rw [←hwr]
            exact hz _ hw.2
          · exact if_neg he
        · change (if 0 ≤ z.im then f z else 0)=0
          rw [if_pos (by simp [hi]),←hzre]
          exact hz _ hzr
      have hu : upper ∪ {w : ℂ | w.im ≤ 0 ∧ 0 < w.re} ∈ 𝓝 z := by
        apply mem_of_superset ((isOpen_lt continuous_const continuous_re).mem_nhds hzr)
        intro w hw
        rcases le_total 0 w.im with hi | hi
        · exact Or.inl hi
        · exact Or.inr ⟨hi,hw⟩
      exact ((hU.union hL).hasDerivAt hu).differentiableAt.differentiableWithinAt

theorem eq_zero_on_upper (f : ℂ → ℂ)
    (hd : ∀ z ∈ upper, ∃ d, HasDerivWithinAt f d upper z)
    (hz : ∀ t : ℝ, 0 < t → f t = 0) :
    ∀ z ∈ interiorUpper, f z = 0 := by
  have hg := (zeroExtension_differentiable f hd hz).analyticOnNhd
    (isOpen_lt continuous_const continuous_re)
  have hge : zeroExtension f =ᶠ[𝓝 (1-Complex.I)] 0 := by
    filter_upwards [(isOpen_lt continuous_im continuous_const).mem_nhds
      (show (1-Complex.I).im < 0 by simp)] with z hz
    exact if_neg (not_le_of_gt hz)
  have hg0 := hg.eqOn_zero_of_preconnected_of_eventuallyEq_zero
    (convex_halfSpace_re_gt 0).isPreconnected
    (show 1-Complex.I ∈ right by simp [right]) hge
  have hfd : DifferentiableOn ℂ f interiorUpper := by
    intro z hz
    obtain ⟨d,h⟩ := hd z (show 0≤z.im from le_of_lt hz)
    exact ((h.hasDerivAt (mem_of_superset
      ((isOpen_lt continuous_const continuous_im).mem_nhds (show 0<z.im from hz))
      (fun w h => (show 0 ≤ w.im from le_of_lt h)))).differentiableAt).differentiableWithinAt
  have hf := hfd.analyticOnNhd (isOpen_lt continuous_const continuous_im)
  have he : f =ᶠ[𝓝 (1+Complex.I)] 0 := by
    filter_upwards [(isOpen_lt continuous_const continuous_re).mem_nhds
      (show 0<(1+Complex.I).re by simp),
      (isOpen_lt continuous_const continuous_im).mem_nhds
      (show 0<(1+Complex.I).im by simp)] with z hr hi
    simpa only [zeroExtension,if_pos hi.le] using hg0 hr
  exact hf.eqOn_zero_of_preconnected_of_eventuallyEq_zero
    (convex_halfSpace_im_gt 0).isPreconnected
    (show 1+Complex.I ∈ interiorUpper by simp [interiorUpper]) he

end F1Fecho.HalfPlaneBoundary
#print axioms F1Fecho.HalfPlaneBoundary.boundary_derivative_zero
#print axioms F1Fecho.HalfPlaneBoundary.zeroExtension_differentiable
#print axioms F1Fecho.HalfPlaneBoundary.eq_zero_on_upper
