import TGLExt.F1Fecho394.ConcreteWeylR1
import TGLExt.F1Fecho394.BosonicSectorContinuity
/-! Norm continuity of the actual exponential map and strong continuity of the
constructed Weyl family. The closed continuous-orbit subspace is reused from
the existing sector-continuity construction; no regularity is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
open Filter Topology
namespace F1Fecho.ConcreteWeyl
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential
open F1Fecho.WeylCoefficients F1Rede.BosonicSectorContinuity

theorem exponential_norm_sub (x y : H1) :
    ‖exponential y - exponential x‖ = Real.sqrt
      ((Complex.exp (inner ℂ y y) - Complex.exp (inner ℂ y x) -
        (Complex.exp (inner ℂ x y) - Complex.exp (inner ℂ x x))).re) := by
  rw [norm_eq_sqrt_re_inner (𝕜 := ℂ), inner_sub_left, inner_sub_right,
    inner_sub_right, exponential_inner, exponential_inner, exponential_inner, exponential_inner]
  rfl

theorem exponential_continuous : Continuous exponential := by
  apply continuous_iff_continuousAt.mpr
  intro x
  apply tendsto_iff_norm_sub_tendsto_zero.mpr
  have hc : Continuous (fun y : H1 => Real.sqrt
      ((Complex.exp (inner ℂ y y) - Complex.exp (inner ℂ y x) -
        (Complex.exp (inner ℂ x y) - Complex.exp (inner ℂ x x))).re)) := by fun_prop
  have ht := hc.tendsto x
  simpa only [← exponential_norm_sub, sub_self, norm_zero, Complex.zero_re, Real.sqrt_zero] using ht

theorem amplitude_continuous (g : H1) : Continuous (fun f : H1 => amplitude f g) := by
  unfold amplitude
  fun_prop

theorem W_strongly_continuous (ψ : F) : Continuous (fun f : H1 => W f ψ) := by
  let O := continuousOrbitSpace D
  have hs : Submodule.span ℂ (Set.range exponential) ≤ O := by
    apply Submodule.span_le.mpr
    rintro _ ⟨g,rfl⟩
    change Continuous (fun f : H1 => D f (exponential g))
    change Continuous (fun f : H1 => W f (exponential g))
    simp only [W_exponential]
    exact (amplitude_continuous g).smul
      (exponential_continuous.comp (continuous_const.add continuous_id))
  have ht := (Submodule.span ℂ (Set.range exponential)).topologicalClosure_minimal hs
    (continuousOrbitSpace_closed D)
  rw [exponential_total] at ht
  exact ht (Submodule.mem_top (x := ψ))

theorem W_regular (f : H1) (ψ : F) : Continuous (fun t : ℝ => W (t • f) ψ) :=
  (W_strongly_continuous ψ).comp (continuous_id.smul continuous_const)

end F1Fecho.ConcreteWeyl
#print axioms F1Fecho.ConcreteWeyl.exponential_norm_sub
#print axioms F1Fecho.ConcreteWeyl.exponential_continuous
#print axioms F1Fecho.ConcreteWeyl.amplitude_continuous
#print axioms F1Fecho.ConcreteWeyl.W_strongly_continuous
#print axioms F1Fecho.ConcreteWeyl.W_regular
