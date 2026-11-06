import TGLExt.V350FourierL1L2

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 2200000

namespace TGLV350.Fourier
open MeasureTheory FourierTransform SchwartzMap
open scoped FourierTransform
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Injectivity of the ordinary Fourier integral on integrable functions,
as equality almost everywhere. No continuity of the original functions or
integrability of their transforms is assumed. -/
theorem fourier_integral_ae_injective (f g : ℝ → H)
    (hf : Integrable f) (hg : Integrable g) (he : ∀ x : ℝ, (𝓕 f) x = (𝓕 g) x) :
    f =ᵐ[volume] g := by
  have hpair : ∀ φ : 𝓢(ℝ, ℂ), (∫ x : ℝ, φ x • f x) = ∫ x : ℝ, φ x • g x := by
    intro φ
    have hfφ := fourier_test_pairing f hf (𝓕⁻ φ)
    have hgφ := fourier_test_pairing g hg (𝓕⁻ φ)
    rw [fourier_fourierInv_eq] at hfφ hgφ
    rw [hfφ, hgφ]
    apply integral_congr_ae
    exact Filter.Eventually.of_forall (fun x => congrArg (fun y => (𝓕⁻ φ) x • y) (he x))
  apply ae_eq_of_integral_contDiff_smul_eq hf.locallyIntegrable hg.locallyIntegrable
  intro φ hφ hc
  have hc' : HasCompactSupport (Complex.ofRealCLM ∘ φ) := hc.comp_left rfl
  have hφ' := Complex.ofRealCLM.contDiff.comp hφ
  simpa using hpair (hc'.toSchwartzMap hφ')

#print axioms fourier_integral_ae_injective
end
end TGLV350.Fourier
