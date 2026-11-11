import TGLExt.V350DualSquareRoot
import Mathlib.Topology.Semicontinuity.Basic

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open Filter ChatgptAudit.Continuous049
open scoped Topology ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- A continuous upper bound that holds on a dense set extends to a lower
semicontinuous extended-valued function. No finitude is assumed. -/
theorem lsc_le_continuous_of_dense (f g : H → ℝ≥0∞)
    (hf : LowerSemicontinuous f) (hg : Continuous g) (D : Set H) (hd : Dense D)
    (hle : ∀ u ∈ D, f u ≤ g u) (u : H) : f u ≤ g u := by
  have hc : IsClosed {u | f u ≤ g u} :=
    hf.isClosed_epigraph.preimage (continuous_id.prodMk hg)
  exact hc.closure_subset_iff.mpr hle (hd u)

/-- Density of Ran B in the parameter space is enough to approximate the
whole graph (Bu,Cu) by points with parameter in Ran B. -/
theorem bounded_graph_form_upper_bound (f : H → ℝ≥0∞)
    (hf : LowerSemicontinuous f) (B C : H →L[ℂ] H) (hi : Function.Injective B)
    (hd : Dense (B.range : Set H))
    (he : ∀ v : H, f (B (B v)) = ENNReal.ofReal (‖C (B v)‖^2))
    (x : (boundedGraphOperator B C hi).domain) :
    f (x : H) ≤ ENNReal.ofReal (‖boundedGraphOperator B C hi x‖^2) := by
  have hall (u : H) : f (B u) ≤ ENNReal.ofReal (‖C u‖^2) := by
    apply lsc_le_continuous_of_dense (fun u => f (B u))
      (fun u => ENNReal.ofReal (‖C u‖^2))
      (hf.comp B.continuous)
      (ENNReal.continuous_ofReal.comp (C.continuous.norm.pow 2))
      (B.range : Set H) hd
    rintro u ⟨v,rfl⟩
    exact (he v).le
  have h := hall (boundedGraphParameter B hi x)
  rw [bounded_graph_parameter_apply] at h
  exact h

theorem resolventSquareRoot_form_upper_bound
    (R : H →L[ℂ] H) (hR : 0 ≤ R) (hi : Function.Injective R)
    (f : H → ℝ≥0∞) (hf : LowerSemicontinuous f)
    (he : ∀ x : (resolventGraphOperator R hi).domain,
      ∃ y : (resolventSquareRoot R hR hi).domain,
        (y : H) = (x : H) ∧ f (x : H) =
          ENNReal.ofReal (‖resolventSquareRoot R hR hi y‖^2))
    (x : (resolventSquareRoot R hR hi).domain) :
    f (x : H) ≤ ENNReal.ofReal (‖resolventSquareRoot R hR hi x‖^2) := by
  apply bounded_graph_form_upper_bound f hf (CFC.sqrt R) (CFC.sqrt (1-R))
    (positive_sqrt_injective R hR hi) (resolventSquareRoot_dense R hR hi)
  intro v
  let z := boundedGraphLift R (1-R) hi v
  obtain ⟨y,hy,heq⟩ := he z
  let y0 := boundedGraphLift (CFC.sqrt R) (CFC.sqrt (1-R))
    (positive_sqrt_injective R hR hi) ((CFC.sqrt R : H →L[ℂ] H) v)
  have hs : (CFC.sqrt R : H →L[ℂ] H) ((CFC.sqrt R : H →L[ℂ] H) v) = R v :=
    congrArg (fun F : H →L[ℂ] H => F v) (CFC.sqrt_mul_sqrt_self R hR)
  have hyy : y = y0 := by
    apply Subtype.ext
    exact hy.trans hs.symm
  rw [hyy] at heq
  have happ : resolventSquareRoot R hR hi y0 =
      (CFC.sqrt (1-R) : H →L[ℂ] H) ((CFC.sqrt R : H →L[ℂ] H) v) :=
    bounded_graph_lift_apply _ _ _ _
  rw [happ] at heq
  change f (R v) = _ at heq
  rw [hs]
  exact heq

theorem dualSupportSquareRoot_form_upper_bound
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hone : R ≤ 1)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (x : (dualSupportSquareRoot A R hA hR hlim).domain) :
    dualQuadraticIntegral A (x : dualFormSupport A hA) ≤
      ENNReal.ofReal (‖dualSupportSquareRoot A R hA hR hlim x‖^2) := by
  exact resolventSquareRoot_form_upper_bound
    (dualSupportResolvent A R hA hlim) (dualSupportResolvent_nonneg A R hA hR hlim)
    (dualSupportResolvent_injective A R hA hR hlim)
    (fun u : dualFormSupport A hA => dualQuadraticIntegral A u)
    ((dualQuadraticIntegral_lowerSemicontinuous A hA).comp continuous_subtype_val)
    (dualSupportSquareRoot_energy_on_operator_domain A R hA hR hone hlim) x

/-- First inclusion only: the converse and equality of energies are separate obligations. -/
theorem dualSupportSquareRoot_domain_finite
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hone : R ≤ 1)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (x : (dualSupportSquareRoot A R hA hR hlim).domain) :
    dualQuadraticIntegral A (x : dualFormSupport A hA) < ⊤ :=
  lt_of_le_of_lt (dualSupportSquareRoot_form_upper_bound A R hA hR hone hlim x)
    ENNReal.ofReal_lt_top

#print axioms lsc_le_continuous_of_dense
#print axioms bounded_graph_form_upper_bound
#print axioms resolventSquareRoot_form_upper_bound
#print axioms dualSupportSquareRoot_form_upper_bound
#print axioms dualSupportSquareRoot_domain_finite
end
end TGLV350.Regular
