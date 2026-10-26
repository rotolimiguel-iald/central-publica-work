import NullFrequencyCoordinatesR3
import TGLExt.O16.OrbitalRapidityMeasure_v4
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap
import Mathlib.MeasureTheory.Integral.Prod

/-! Bochner transport to positive null frequency on the actual
orbital measure. R2 makes positive-interval membership explicit in the final cancellation.
Earlier failed build is retained separately; acceptance requires this file own receipt. The only analytic input
of the global formula is integrability of its actual integrand. Fiber formulas
also carry equivalences of integrability, so they are not offered as evidence
of convergence merely because the total Bochner integral is defined as zero
outside its integrable domain. The transverse zero axis is discarded using
the already proved almost-everywhere positive transverse mass.

This supplies the measure/Jacobian step for the contracted Maxwell wave.
The phase, null-polarization contraction, Fourier/charge identity, generator
domain and nonzero modular-energy witness remain separate obligations. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.NullFrequency
open Set MeasureTheory Filter
open ChatgptAudit.WignerRapidityMeasure016
open scoped ENNReal

variable {G : Type*} [NormedAddCommGroup G] [NormedSpace ℝ G] [CompleteSpace G]

private theorem longitudinal_density_smul (r : ℝ) (hr : 0 < r) (x : ℝ) (v : G) :
    |r * Real.cosh x| • ((1 / energy r (longitudinal r x)) • v) = v := by
  have hp := mul_pos hr (Real.cosh_pos x)
  rw [energy_longitudinal r hr x, abs_of_pos hp, smul_smul]
  have he : (r * Real.cosh x) * (1 / (r * Real.cosh x)) = 1 := by
    field_simp [hp.ne']
  rw [he, one_smul]

private theorem frequency_density_smul (r : ℝ) (hr : 0 < r) (x : ℝ) (v : G) :
    |-frequency r x| • ((1 / frequency r x) • v) = v := by
  have hp := frequency_pos r hr x
  rw [abs_neg, abs_of_pos hp, smul_smul]
  have he : frequency r x * (1 / frequency r x) = 1 := by
    field_simp [hp.ne']
  rw [he, one_smul]

theorem longitudinal_bochner (r : ℝ) (hr : 0 < r) (g : ℝ → G) :
    (∫ p, (1 / energy r p) • g p) = ∫ x, g (longitudinal r x) := by
  have hb := longitudinal_bijective r hr
  have hc := integral_image_eq_integral_abs_deriv_smul
    (s := (univ : Set ℝ)) MeasurableSet.univ
    (fun x _ => (longitudinal_hasDerivAt r x).hasDerivWithinAt)
    hb.1.injOn (fun p => (1 / energy r p) • g p)
  have hi : longitudinal r '' (univ : Set ℝ) = univ :=
    Set.image_univ.trans (Set.range_eq_univ.mpr hb.2)
  rw [hi] at hc
  simpa only [Measure.restrict_univ, longitudinal_density_smul r hr] using hc

theorem longitudinal_bochner_integrable_iff (r : ℝ) (hr : 0 < r) (g : ℝ → G) :
    Integrable (fun p => (1 / energy r p) • g p) ↔
      Integrable (fun x => g (longitudinal r x)) := by
  have hb := longitudinal_bijective r hr
  have hc := integrableOn_image_iff_integrableOn_abs_deriv_smul
    (s := (univ : Set ℝ)) MeasurableSet.univ
    (fun x _ => (longitudinal_hasDerivAt r x).hasDerivWithinAt)
    hb.1.injOn (fun p => (1 / energy r p) • g p)
  have hi : longitudinal r '' (univ : Set ℝ) = univ :=
    Set.image_univ.trans (Set.range_eq_univ.mpr hb.2)
  rw [hi] at hc
  simpa only [IntegrableOn, Measure.restrict_univ, longitudinal_density_smul r hr] using hc

theorem frequency_bochner (r : ℝ) (hr : 0 < r) (g : ℝ → G) :
    (∫ u in Ioi 0, (1 / u) • g u) = ∫ x, g (frequency r x) := by
  have hc := integral_image_eq_integral_abs_deriv_smul
    (s := (univ : Set ℝ)) MeasurableSet.univ
    (fun x _ => (frequency_hasDerivAt r x).hasDerivWithinAt)
    (frequency_injective r hr).injOn (fun u => (1 / u) • g u)
  rw [frequency_image r hr] at hc
  simpa only [Measure.restrict_univ, frequency_density_smul r hr] using hc

theorem frequency_bochner_integrable_iff (r : ℝ) (hr : 0 < r) (g : ℝ → G) :
    IntegrableOn (fun u => (1 / u) • g u) (Ioi 0) ↔
      Integrable (fun x => g (frequency r x)) := by
  have hc := integrableOn_image_iff_integrableOn_abs_deriv_smul
    (s := (univ : Set ℝ)) MeasurableSet.univ
    (fun x _ => (frequency_hasDerivAt r x).hasDerivWithinAt)
    (frequency_injective r hr).injOn (fun u => (1 / u) • g u)
  rw [frequency_image r hr] at hc
  simpa only [IntegrableOn, Measure.restrict_univ, frequency_density_smul r hr] using hc

theorem longitudinal_null_bochner (r : ℝ) (hr : 0 < r) (g : ℝ → G) :
    (∫ p, (1 / energy r p) • g (energy r p - p)) =
      ∫ u in Ioi 0, (1 / u) • g u := by
  rw [longitudinal_bochner r hr]
  simp_rw [frequency_is_shell_null r hr]
  exact (frequency_bochner r hr g).symm

theorem longitudinal_null_bochner_integrable_iff
    (r : ℝ) (hr : 0 < r) (g : ℝ → G) :
    Integrable (fun p => (1 / energy r p) • g (energy r p - p)) ↔
      IntegrableOn (fun u => (1 / u) • g u) (Ioi 0) := by
  rw [longitudinal_bochner_integrable_iff r hr]
  simp_rw [frequency_is_shell_null r hr]
  exact (frequency_bochner_integrable_iff r hr g).symm

theorem longitudinal_null_bochner_inverse (r : ℝ) (hr : 0 < r) (g : ℝ → G) :
    (∫ p, (1 / energy r p) • g p) =
      ∫ u in Ioi 0, (1 / u) • g (inverseLongitudinal r u) := by
  have hi (p : ℝ) := inverseLongitudinal_null r p hr
  simpa only [hi] using
    longitudinal_null_bochner r hr (fun u => g (inverseLongitudinal r u))

theorem longitudinal_null_bochner_inverse_integrable_iff
    (r : ℝ) (hr : 0 < r) (g : ℝ → G) :
    Integrable (fun p => (1 / energy r p) • g p) ↔
      IntegrableOn (fun u => (1 / u) • g (inverseLongitudinal r u)) (Ioi 0) := by
  have hi (p : ℝ) := inverseLongitudinal_null r p hr
  simpa only [hi] using
    longitudinal_null_bochner_integrable_iff r hr (fun u => g (inverseLongitudinal r u))

/-- The inverse coordinate on the same massless orbital momentum space. -/
def nullMomentumCoordinates (q : Transverse) (u : ℝ) : MomentumCoordinates :=
  (q, inverseLongitudinal (transverseMass 0 q) u)

private theorem orbitalWeight_zero_toReal_reciprocal (y : MomentumCoordinates) :
    (orbitalWeight 0 y).toReal = 1 / energy (transverseMass 0 y.1) y.2 := by
  unfold orbitalWeight
  exact ENNReal.toReal_ofReal (div_nonneg zero_le_one (Real.sqrt_nonneg _))

/-- Global Bochner transport, using Fubini only under actual integrability. -/
theorem orbital_nullFrequency_bochner (f : MomentumCoordinates → G)
    (hf : Integrable f (orbitalMeasure 0)) :
    (∫ y, f y ∂orbitalMeasure 0) =
      ∫ q : Transverse, ∫ u in Ioi 0, (1 / u) • f (nullMomentumCoordinates q u) := by
  have hfinite : ∀ᵐ y ∂momentumMeasure, orbitalWeight 0 y < ∞ :=
    ae_of_all _ (fun _ => ENNReal.ofReal_lt_top)
  have hi : Integrable
      (fun y : MomentumCoordinates => (1 / energy (transverseMass 0 y.1) y.2) • f y)
      momentumMeasure := by
    have h := (integrable_withDensity_iff_integrable_smul'
      (orbitalWeight_measurable 0) hfinite).mp hf
    simpa only [orbitalWeight_zero_toReal_reciprocal] using h
  have he : (∫ y, f y ∂orbitalMeasure 0) =
      ∫ q : Transverse, ∫ p : ℝ, (1 / energy (transverseMass 0 q) p) • f (q, p) := by
    unfold orbitalMeasure
    rw [integral_withDensity_eq_integral_toReal_smul (orbitalWeight_measurable 0) hfinite]
    simp_rw [orbitalWeight_zero_toReal_reciprocal]
    exact integral_prod _ hi
  rw [he]
  apply integral_congr_ae
  filter_upwards [transverseMass_pos_ae 0] with q hq
  exact longitudinal_null_bochner_inverse (transverseMass 0 q) hq (fun p => f (q, p))

/-- The null-strength factor cancels du/u. This is the exact measure step
needed before inserting the Maxwell phase and polarization, not charge_link. -/
theorem orbital_nullFrequency_bochner_cancel (f : MomentumCoordinates → G)
    (hf : Integrable
      (fun y => (energy (transverseMass 0 y.1) y.2 - y.2) • f y)
      (orbitalMeasure 0)) :
    (∫ y, (energy (transverseMass 0 y.1) y.2 - y.2) • f y ∂orbitalMeasure 0) =
      ∫ q : Transverse, ∫ u in Ioi 0, f (nullMomentumCoordinates q u) := by
  rw [orbital_nullFrequency_bochner _ hf]
  apply integral_congr_ae
  filter_upwards [] with q
  apply integral_congr_ae
  filter_upwards [ae_restrict_mem measurableSet_Ioi] with u hu
  change (1 / u) •
      ((energy (transverseMass 0 q) (inverseLongitudinal (transverseMass 0 q) u) -
        inverseLongitudinal (transverseMass 0 q) u) • f (nullMomentumCoordinates q u)) = _
  rw [null_inverseLongitudinal (transverseMass 0 q) u hu, smul_smul]
  have hu0 : 0 < u := hu
  have he : (1 / u) * u = 1 := by field_simp [ne_of_gt hu0]
  rw [he, one_smul]

end F1Fecho.NullFrequency
#print axioms F1Fecho.NullFrequency.longitudinal_bochner
#print axioms F1Fecho.NullFrequency.longitudinal_bochner_integrable_iff
#print axioms F1Fecho.NullFrequency.frequency_bochner
#print axioms F1Fecho.NullFrequency.frequency_bochner_integrable_iff
#print axioms F1Fecho.NullFrequency.longitudinal_null_bochner
#print axioms F1Fecho.NullFrequency.longitudinal_null_bochner_integrable_iff
#print axioms F1Fecho.NullFrequency.longitudinal_null_bochner_inverse
#print axioms F1Fecho.NullFrequency.longitudinal_null_bochner_inverse_integrable_iff
#print axioms F1Fecho.NullFrequency.orbital_nullFrequency_bochner
#print axioms F1Fecho.NullFrequency.orbital_nullFrequency_bochner_cancel
