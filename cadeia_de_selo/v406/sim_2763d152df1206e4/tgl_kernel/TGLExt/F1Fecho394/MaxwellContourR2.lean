import TGLExt.F1Fecho394.MaxwellStripCoefficientR5
import TGLExt.F1Fecho394.MaxwellRapidityPolynomialR1
import TGLExt.F1Fecho394.RegularizedContourSpaceR4

/-! Gaussian-regularized contour equality for the actual Maxwell coefficient.
Support pays scalar analyticity and polynomial rapidity growth pays the
vector coefficient. No contour hypothesis is an input of the conclusion. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory
namespace F1Fecho.MaxwellStrip
open F1Fecho.MaxwellGlobal F1Fecho.WedgeLaplace
open ChatgptAudit.WignerRapidityMeasure016

theorem maxwell_term_mem_contourSpace (b : ℝ) (hb : 0 < b) (p : ℝ)
    (q : Fin 2 → ℝ) (f : SchwartzTensor) (hf : supportedTensorRight f)
    (j : Fin 2) (μ ν : Fin 4) :
    analyticStrength q j μ ν *
      scalarLaplace (transverseMass 0 q) (q 0) (q 1) (componentTest f μ ν)
      ∈ contourSpace b p := by
  have hm : 0 ≤ transverseMass 0 q := by unfold transverseMass; positivity
  exact polynomial_mul_mem_contourSpace b hb p (∫ x,‖componentTest f μ ν x‖)
    _ (integral_nonneg (fun _ => norm_nonneg _))
    (scalarLaplace_continuous_closed _ _ _ _ hm (componentTest_supported f hf μ ν))
    (scalarLaplace_diffContOnCl _ _ _ _ hm (componentTest_supported f hf μ ν)).1
    (fun z hz => scalarLaplace_bound _ _ _ _ z hm (componentTest_supported f hf μ ν) hz)
    _ (analyticStrength_mem q j μ ν)

theorem maxwellLaplace_mem_contourSpace (b : ℝ) (hb : 0 < b) (p : ℝ)
    (q : Fin 2 → ℝ) (f : SchwartzTensor) (hf : supportedTensorRight f) (j : Fin 2) :
    maxwellLaplace q f j ∈ contourSpace b p := by
  have hs : (∑ μ, ∑ ν, analyticStrength q j μ ν *
      scalarLaplace (transverseMass 0 q) (q 0) (q 1) (componentTest f μ ν))
      ∈ contourSpace b p := by
    apply Submodule.sum_mem
    intro μ _
    apply Submodule.sum_mem
    intro ν _
    exact maxwell_term_mem_contourSpace b hb p q f hf j μ ν
  convert (contourSpace b p).smul_mem (1/2:ℂ) hs using 1
  ext z
  simp [maxwellLaplace]

end F1Fecho.MaxwellStrip
#print axioms F1Fecho.MaxwellStrip.maxwell_term_mem_contourSpace
#print axioms F1Fecho.MaxwellStrip.maxwellLaplace_mem_contourSpace
