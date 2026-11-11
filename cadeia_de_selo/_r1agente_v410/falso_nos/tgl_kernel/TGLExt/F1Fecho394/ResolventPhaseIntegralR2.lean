import TGLExt.V351ScaledResolventCalculus
import TGLExt.V351ResolventImaginaryContinuity
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Integral
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic

/-! Strong group averages on the dense damping range are the integral of
its bounded continuous phase calculus. No spectral smoothing is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory
namespace F1Fecho.ResolventPhaseIntegral
open TGLV350.Regular
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
local instance : Module ℝ (H →L[ℂ] H) := Module.restrictScalars ℝ ℂ _

theorem phase_bound (R:H→L[ℂ]H) (hR:0≤R) (h1:R≤1)
    (t:ℝ) (z:ℂ) (hz:z∈spectrum ℂ R) : ‖resolventPhaseFunction t z.re‖≤1 := by
  have hx:=positive_contraction_spectrum_bounds R hR h1
    ((IsSelfAdjoint.of_nonneg hR).spectrumRestricts.apply_mem hz)
  rw [resolventPhaseFunction_norm,Real.norm_eq_abs,abs_of_nonneg]
  · unfold resolventDamping
    nlinarith [sq_nonneg z.re]
  · exact mul_nonneg hx.1 (sub_nonneg.mpr hx.2)

theorem weighted_phase_integrable (R:H→L[ℂ]H) (hR:0≤R) (h1:R≤1)
    (w:ℝ→ℝ) (hw:Continuous w) (hi:Integrable w volume) :
    Integrable (fun t:ℝ=>(w t:ℂ) • resolventPhaseOperator R t) volume := by
  have hc: Continuous (fun q : ℝ × ℂ=>(w q.1:ℂ)*resolventPhaseFunction q.1 q.2.re) :=
    (Complex.continuous_ofReal.comp (hw.comp continuous_fst)).mul
      (resolventPhaseFunction_joint_continuous.comp
        (continuous_fst.prodMk (Complex.continuous_re.comp continuous_snd)))
  have hbound:∀ᵐ t:ℝ ∂volume,∀z∈spectrum ℂ R,
      ‖(w t:ℂ)*resolventPhaseFunction t z.re‖≤‖w t‖ := by
    apply ae_of_all
    intro t z hz
    rw [norm_mul,Complex.norm_real,Real.norm_eq_abs]
    exact (mul_le_mul_of_nonneg_left (phase_bound R hR h1 t z hz) (abs_nonneg _)).trans_eq (mul_one _)
  have h:=integrable_cfc (fun t:ℝ=>fun z:ℂ=>(w t:ℂ)*resolventPhaseFunction t z.re)
    (fun t=>‖w t‖) R hc.continuousOn hbound hi.norm.hasFiniteIntegral
    (IsSelfAdjoint.of_nonneg hR).isStarNormal
  have he:∀t:ℝ,cfc (fun z:ℂ=>(w t:ℂ)*resolventPhaseFunction t z.re) R=
      (w t:ℂ) • resolventPhaseOperator R t := by
    intro t
    exact cfc_const_mul _ _ R ((resolventPhaseFunction_continuous t).comp Complex.continuous_re).continuousOn
  simpa only [he] using h

theorem weighted_phase_integral (R:H→L[ℂ]H) (hR:0≤R) (h1:R≤1)
    (w:ℝ→ℝ) (hw:Continuous w) (hi:Integrable w volume) :
    cfc (fun z:ℂ=>∫t:ℝ,(w t:ℂ)*resolventPhaseFunction t z.re) R=
      ∫t:ℝ,(w t:ℂ) • resolventPhaseOperator R t := by
  have hc: Continuous (fun q : ℝ × ℂ=>(w q.1:ℂ)*resolventPhaseFunction q.1 q.2.re) :=
    (Complex.continuous_ofReal.comp (hw.comp continuous_fst)).mul
      (resolventPhaseFunction_joint_continuous.comp
        (continuous_fst.prodMk (Complex.continuous_re.comp continuous_snd)))
  have hbound:∀ᵐ t:ℝ ∂volume,∀z∈spectrum ℂ R,
      ‖(w t:ℂ)*resolventPhaseFunction t z.re‖≤‖w t‖ := by
    apply ae_of_all
    intro t z hz
    rw [norm_mul,Complex.norm_real,Real.norm_eq_abs]
    exact (mul_le_mul_of_nonneg_left (phase_bound R hR h1 t z hz) (abs_nonneg _)).trans_eq (mul_one _)
  rw [cfc_integral _ (fun t=>‖w t‖) R hc.continuousOn hbound hi.norm.hasFiniteIntegral
    (IsSelfAdjoint.of_nonneg hR).isStarNormal]
  apply integral_congr_ae
  apply ae_of_all
  intro t
  exact cfc_const_mul _ _ R ((resolventPhaseFunction_continuous t).comp Complex.continuous_re).continuousOn

end F1Fecho.ResolventPhaseIntegral
#print axioms F1Fecho.ResolventPhaseIntegral.phase_bound
#print axioms F1Fecho.ResolventPhaseIntegral.weighted_phase_integrable
#print axioms F1Fecho.ResolventPhaseIntegral.weighted_phase_integral
