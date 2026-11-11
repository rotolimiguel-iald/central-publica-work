import Mathlib.Analysis.Fourier.LpSpace

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 2200000

namespace TGLV350.Fourier
open MeasureTheory FourierTransform SchwartzMap Real
open scoped FourierTransform ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem fourier_integrable_continuous (f : ℝ → H) (hf : Integrable f) :
    Continuous (𝓕 f) :=
  VectorFourier.fourierIntegral_continuous continuous_fourierChar continuous_inner hf

/-- Test-function pairing for the pointwise Fourier integral of an L1 function. -/
theorem fourier_test_pairing (f : ℝ → H) (hf : Integrable f) (g : 𝓢(ℝ, ℂ)) :
    (∫ x : ℝ, (𝓕 g) x • f x) = ∫ x : ℝ, g x • (𝓕 f) x := by
  simpa using! VectorFourier.integral_fourierIntegral_smul_eq_flip (L := innerₗ ℝ)
    continuous_fourierChar continuous_inner g.integrable hf

/-- For L1 intersect L2, the ordinary Fourier integral agrees almost everywhere
with the isometric L2 transform. Equality is obtained from distributions and
locally integrable test-function uniqueness, not assumed from a name match. -/
theorem fourier_integral_ae_eq_L2 (f : ℝ → H) (hf1 : Integrable f) (hf2 : MemLp f 2) :
    (𝓕 f) =ᵐ[volume] (𝓕 (hf2.toLp f) : Lp (α := ℝ) H 2 volume) := by
  let F : Lp (α := ℝ) H 2 volume := hf2.toLp f
  have hpair : ∀ g : 𝓢(ℝ, ℂ),
      (∫ x : ℝ, g x • (𝓕 f) x) = ∫ x : ℝ, g x • (𝓕 F : Lp (α := ℝ) H 2 volume) x := by
    intro g
    have hd := congrArg (fun T : 𝓢'(ℝ,H) => T g) (Lp.fourier_toTemperedDistribution_eq F)
    change (Lp.toTemperedDistribution F) (𝓕 g) =
      (Lp.toTemperedDistribution (𝓕 F)) g at hd
    rw [Lp.toTemperedDistribution_apply,Lp.toTemperedDistribution_apply] at hd
    calc
      _ = ∫ x : ℝ, (𝓕 g) x • f x := (fourier_test_pairing f hf1 g).symm
      _ = ∫ x : ℝ, (𝓕 g) x • F x := by
        apply integral_congr_ae
        filter_upwards [hf2.coeFn_toLp] with x hx
        rw [show F x = f x from hx]
      _ = _ := hd
  apply ae_eq_of_integral_contDiff_smul_eq
    (fourier_integrable_continuous f hf1).locallyIntegrable
    ((Lp.memLp (𝓕 F : Lp (α := ℝ) H 2 volume)).locallyIntegrable (by norm_num))
  intro g hg hc
  have hc' : HasCompactSupport (Complex.ofRealCLM ∘ g) := hc.comp_left rfl
  have hg' := Complex.ofRealCLM.contDiff.comp hg
  simpa using hpair (hc'.toSchwartzMap hg')

theorem fourier_integral_memLp_two (f : ℝ → H) (hf1 : Integrable f) (hf2 : MemLp f 2) :
    MemLp (𝓕 f) 2 :=
  (memLp_congr_ae (fourier_integral_ae_eq_L2 f hf1 hf2)).mpr
    (Lp.memLp (𝓕 (hf2.toLp f) : Lp (α := ℝ) H 2 volume))

theorem L2_integral_norm_sq (F : Lp (α := ℝ) H 2 volume) :
    (∫ x : ℝ, ‖F x‖ ^ 2) = ‖F‖ ^ 2 := by
  have h := congrArg (RCLike.re : ℂ → ℝ) (L2.inner_def (𝕜 := ℂ) F F)
  rw [← integral_re (L2.integrable_inner (𝕜 := ℂ) F F)] at h
  simpa only [inner_self_eq_norm_sq] using h.symm

theorem integral_norm_sq_eq_L2 (f : ℝ → H) (hf : MemLp f 2) :
    (∫ x : ℝ, ‖f x‖ ^ 2) = ‖hf.toLp f‖ ^ 2 := by
  rw [← L2_integral_norm_sq]
  apply integral_congr_ae
  filter_upwards [hf.coeFn_toLp] with x hx
  rw [hx]

/-- Plancherel for the actual Bochner Fourier integral, with L1 and L2
hypotheses discharged separately. -/
theorem fourier_integral_norm_sq (f : ℝ → H) (hf1 : Integrable f) (hf2 : MemLp f 2) :
    (∫ x : ℝ, ‖(𝓕 f) x‖ ^ 2) = ∫ x : ℝ, ‖f x‖ ^ 2 := by
  calc
    _ = ∫ x : ℝ, ‖(𝓕 (hf2.toLp f) : Lp (α := ℝ) H 2 volume) x‖ ^ 2 := by
      apply integral_congr_ae
      filter_upwards [fourier_integral_ae_eq_L2 f hf1 hf2] with x hx
      rw [hx]
    _ = ‖𝓕 (hf2.toLp f)‖ ^ 2 := L2_integral_norm_sq _
    _ = ‖hf2.toLp f‖ ^ 2 := by rw [Lp.norm_fourier_eq]
    _ = _ := (integral_norm_sq_eq_L2 f hf2).symm

theorem fourier_integral_lintegral_norm_sq (f : ℝ → H)
    (hf1 : Integrable f) (hf2 : MemLp f 2) :
    (∫⁻ x : ℝ, ENNReal.ofReal (‖(𝓕 f) x‖ ^ 2)) =
      ∫⁻ x : ℝ, ENNReal.ofReal (‖f x‖ ^ 2) := by
  have hF := fourier_integral_memLp_two f hf1 hf2
  rw [← ofReal_integral_eq_lintegral_ofReal
    ((memLp_two_iff_integrable_sq_norm hF.1).mp hF)
    (Filter.Eventually.of_forall (fun x => sq_nonneg _))]
  rw [← ofReal_integral_eq_lintegral_ofReal
    ((memLp_two_iff_integrable_sq_norm hf2.1).mp hf2)
    (Filter.Eventually.of_forall (fun x => sq_nonneg _))]
  rw [fourier_integral_norm_sq f hf1 hf2]

#print axioms fourier_integrable_continuous
#print axioms fourier_test_pairing
#print axioms fourier_integral_ae_eq_L2
#print axioms fourier_integral_memLp_two
#print axioms L2_integral_norm_sq
#print axioms integral_norm_sq_eq_L2
#print axioms fourier_integral_norm_sq
#print axioms fourier_integral_lintegral_norm_sq
end
end TGLV350.Fourier
