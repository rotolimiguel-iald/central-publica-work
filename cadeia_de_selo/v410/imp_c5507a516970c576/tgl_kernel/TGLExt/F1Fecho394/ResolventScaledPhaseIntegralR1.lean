import TGLExt.F1Fecho394.ResolventPhaseIntegralR2

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory
namespace F1Fecho.ResolventScaledPhaseIntegral
open TGLV350.Regular F1Fecho.ResolventPhaseIntegral
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
local instance : Module ℝ (H →L[ℂ] H) := Module.restrictScalars ℝ ℂ _

theorem weighted_phase_integrable (R:H→L[ℂ]H) (hR:0≤R) (h1:R≤1)
    (c:ℝ) (w:ℝ→ℝ) (hw:Continuous w) (hi:Integrable w volume) :
    Integrable (fun t:ℝ=>(w t:ℂ) • resolventPhaseOperator R (c*t)) volume := by
  have hc: Continuous (fun q : ℝ × ℂ=>(w q.1:ℂ)*resolventPhaseFunction (c*q.1) q.2.re) :=
    (Complex.continuous_ofReal.comp (hw.comp continuous_fst)).mul
      (resolventPhaseFunction_joint_continuous.comp
        ((continuous_const.mul continuous_fst).prodMk (Complex.continuous_re.comp continuous_snd)))
  have hbound:∀ᵐ t:ℝ ∂volume,∀z∈spectrum ℂ R,
      ‖(w t:ℂ)*resolventPhaseFunction (c*t) z.re‖≤‖w t‖ := by
    apply ae_of_all
    intro t z hz
    rw [norm_mul,Complex.norm_real,Real.norm_eq_abs]
    exact (mul_le_mul_of_nonneg_left (phase_bound R hR h1 (c*t) z hz) (abs_nonneg _)).trans_eq (mul_one _)
  have h:=integrable_cfc (fun t:ℝ=>fun z:ℂ=>(w t:ℂ)*resolventPhaseFunction (c*t) z.re)
    (fun t=>‖w t‖) R hc.continuousOn hbound hi.norm.hasFiniteIntegral
    (IsSelfAdjoint.of_nonneg hR).isStarNormal
  have he:∀t:ℝ,cfc (fun z:ℂ=>(w t:ℂ)*resolventPhaseFunction (c*t) z.re) R=
      (w t:ℂ) • resolventPhaseOperator R (c*t) := by
    intro t
    exact cfc_const_mul _ _ R ((resolventPhaseFunction_continuous (c*t)).comp Complex.continuous_re).continuousOn
  simpa only [he] using h

theorem weighted_phase_integral (R:H→L[ℂ]H) (hR:0≤R) (h1:R≤1)
    (c:ℝ) (w:ℝ→ℝ) (hw:Continuous w) (hi:Integrable w volume) :
    cfc (fun z:ℂ=>∫t:ℝ,(w t:ℂ)*resolventPhaseFunction (c*t) z.re) R=
      ∫t:ℝ,(w t:ℂ) • resolventPhaseOperator R (c*t) := by
  have hc: Continuous (fun q : ℝ × ℂ=>(w q.1:ℂ)*resolventPhaseFunction (c*q.1) q.2.re) :=
    (Complex.continuous_ofReal.comp (hw.comp continuous_fst)).mul
      (resolventPhaseFunction_joint_continuous.comp
        ((continuous_const.mul continuous_fst).prodMk (Complex.continuous_re.comp continuous_snd)))
  have hbound:∀ᵐ t:ℝ ∂volume,∀z∈spectrum ℂ R,
      ‖(w t:ℂ)*resolventPhaseFunction (c*t) z.re‖≤‖w t‖ := by
    apply ae_of_all
    intro t z hz
    rw [norm_mul,Complex.norm_real,Real.norm_eq_abs]
    exact (mul_le_mul_of_nonneg_left (phase_bound R hR h1 (c*t) z hz) (abs_nonneg _)).trans_eq (mul_one _)
  rw [cfc_integral _ (fun t=>‖w t‖) R hc.continuousOn hbound hi.norm.hasFiniteIntegral
    (IsSelfAdjoint.of_nonneg hR).isStarNormal]
  apply integral_congr_ae
  apply ae_of_all
  intro t
  exact cfc_const_mul _ _ R ((resolventPhaseFunction_continuous (c*t)).comp Complex.continuous_re).continuousOn

end F1Fecho.ResolventScaledPhaseIntegral
#print axioms F1Fecho.ResolventScaledPhaseIntegral.weighted_phase_integrable
#print axioms F1Fecho.ResolventScaledPhaseIntegral.weighted_phase_integral
