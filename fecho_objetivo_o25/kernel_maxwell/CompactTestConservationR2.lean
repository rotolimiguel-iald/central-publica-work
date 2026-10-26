import Mathlib.Analysis.Calculus.LineDeriv.IntegrationByParts
import Mathlib.Analysis.Calculus.ContDiff.Operations
import Mathlib.MeasureTheory.Function.LocallyIntegrable
import Mathlib.Analysis.Complex.Basic
import Mathlib.Tactic

/-! Weak conservation from actual continuous coordinate derivatives, via
mathlib integration by parts. No equation is added to the concrete Maxwell
consumer: it will supply the already proved pointwise divergence. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.CompactConservation
open MeasureTheory Measure
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
  (μ : Measure E) [IsAddHaarMeasure μ]

 theorem compact_test_ibp (A D : E→ℂ) (v : E) (hA : Continuous A) (hD : Continuous D)
    (hAD : ∀x,HasLineDerivAt ℝ A (D x) x v) (f : E→ℂ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (hc : HasCompactSupport f) :
    (∫x,A x*(fderiv ℝ f x v) ∂μ)= -(∫x,D x*f x ∂μ) := by
  have hfd : Continuous (fun x=>fderiv ℝ f x v) :=
    (hf.continuous_fderiv (by simp)).clm_apply continuous_const
  apply integral_bilinear_hasLineDerivAt_right_eq_neg_left_of_integrable
    (B:=ContinuousLinearMap.mul ℝ ℂ)
  · exact (hD.mul hf.continuous).integrable_of_hasCompactSupport hc.mul_left
  · exact (hA.mul hfd).integrable_of_hasCompactSupport (hc.fderiv_apply v).mul_left
  · exact (hA.mul hf.continuous).integrable_of_hasCompactSupport hc.mul_left
  · exact fun x _=>hAD x
  · exact fun x _=>(hf.differentiable (by simp) x).hasFDerivAt.hasLineDerivAt v

 theorem compact_test_integrable (A : E→ℂ) (v : E) (hA : Continuous A)
    (f : E→ℂ) (hf : ContDiff ℝ (⊤ : ℕ∞) f) (hc : HasCompactSupport f) :
    Integrable (fun x=>A x*(fderiv ℝ f x v)) μ := by
  have hfd : Continuous (fun x=>fderiv ℝ f x v) :=
    (hf.continuous_fderiv (by simp)).clm_apply continuous_const
  exact (hA.mul hfd).integrable_of_hasCompactSupport (hc.fderiv_apply v).mul_left

 theorem weak_conservation {ι : Type*} [Fintype ι] (A D : ι→E→ℂ) (v : ι→E) (s : ι→ℂ)
    (hA : ∀i,Continuous (A i)) (hD : ∀i,Continuous (D i))
    (hAD : ∀i x,HasLineDerivAt ℝ (A i) (D i x) x (v i))
    (hdiv : ∀x,∑i,s i*D i x=0) (f : E→ℂ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (hc : HasCompactSupport f) :
    (∑i,∫x,s i*A i x*(fderiv ℝ f x (v i)) ∂μ)=0 := by
  have hi (i : ι) : Integrable (fun x=>s i*(D i x*f x)) μ :=
    ((hD i).mul hf.continuous).integrable_of_hasCompactSupport hc.mul_left |>.const_mul _
  calc
    _ = -(∑i,∫x,s i*(D i x*f x) ∂μ) := by
      rw [Finset.sum_neg_distrib]
      apply Finset.sum_congr rfl
      intro i _
      simp only [mul_assoc,integral_const_mul,
        compact_test_ibp μ (A i) (D i) (v i) (hA i) (hD i) (hAD i) f hf hc,mul_neg]
    _ = -(∫x,∑i,s i*(D i x*f x) ∂μ) := by
      rw [integral_finsetSum Finset.univ (fun i _=>hi i)]
    _ = 0 := by
      have he (x : E) : (∑i,s i*(D i x*f x))=0 := by
        simp only [← mul_assoc,← Finset.sum_mul,hdiv x,zero_mul]
      simp only [he,integral_zero,neg_zero]

end F1Fecho.CompactConservation
#print axioms F1Fecho.CompactConservation.compact_test_ibp
#print axioms F1Fecho.CompactConservation.compact_test_integrable
#print axioms F1Fecho.CompactConservation.weak_conservation
