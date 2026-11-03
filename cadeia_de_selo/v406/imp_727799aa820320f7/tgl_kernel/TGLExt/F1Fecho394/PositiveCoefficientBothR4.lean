import TGLExt.F1Fecho394.PositiveCoefficientBoundaryR4

/-! The negative real ray gives the same uniqueness result, by conjugating
the scalar density while keeping the nonnegative frequency unchanged. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory Complex
open scoped ComplexConjugate
namespace F1Fecho.PositiveCoefficientBoundary
open ChatgptAudit.PositiveEnergy016
variable {X : Type*} [MeasurableSpace X]

theorem coefficient_conjugate_real (μ : Measure X) (p : X→ℝ) (h : X→ℂ) (t : ℝ) :
    coefficient μ p (fun x=>conj (h x)) t=conj (coefficient μ p h (-t)) := by
  rw [coefficient,coefficient,←integral_conj]
  apply integral_congr_ae
  apply ae_of_all
  intro x
  simp only [map_mul,←Complex.exp_conj,spectralPhase]
  congr 1
  congr 1
  simp

theorem vanishes_from_negative_ray (μ : Measure X) (p : X→ℝ)
    (hp : Measurable p) (hpos : ∀x,0≤p x) (h : X→ℂ) (hh : Integrable h μ)
    (hm : Integrable (fun x=>p x*‖h x‖) μ)
    (hz : ∀ t:ℝ,t<0→coefficient μ p h t=0) :
    ∀t:ℝ,coefficient μ p h t=0 := by
  have hc : Integrable (fun x=>conj (h x)) μ := (RCLike.conjLIE : ℂ ≃ₗᵢ[ℝ] ℂ).integrable_comp_iff.mpr hh
  have hm' : Integrable (fun x=>p x*‖conj (h x)‖) μ := by simpa only [norm_conj] using hm
  have hv:=vanishes_from_positive_ray μ p hp hpos _ hc hm'
    (fun t ht=>by
      rw [coefficient_conjugate_real,←Complex.ofReal_neg,hz (-t) (neg_neg_of_pos ht),map_zero])
  intro t
  have ht:=hv (-t:ℝ) (by simp [HalfPlaneBoundary.upper])
  rw [coefficient_conjugate_real,Complex.ofReal_neg,neg_neg] at ht
  simpa using congrArg (starRingEnd ℂ) ht

end F1Fecho.PositiveCoefficientBoundary
#print axioms F1Fecho.PositiveCoefficientBoundary.coefficient_conjugate_real
#print axioms F1Fecho.PositiveCoefficientBoundary.vanishes_from_negative_ray
