import NullFrequencyBochnerR2
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.MeasureTheory.Function.Jacobian

/-! Almost-everywhere transport from the actual massless orbital measure to
positive null-frequency coordinates. This proves the representative transport
obligation S4 without a new measurability hypothesis on the predicate.
R2 repairs elaboration, the null-image API, and the product-measure namespace.

The longitudinal exceptional set has Lebesgue measure zero. Its image under
the differentiable forward null-frequency map still has measure zero; the
already proved right-inverse identity controls the inverse-coordinate pullback.
The transverse zero axis is excluded by transverseMass_pos_ae.

This component does not construct NullSchwartzData, a strong H1 generator,
a real charge identity, a nonzero modular-energy witness, or a full certificate.
-/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section

namespace F1Fecho.NullFrequency
open Set MeasureTheory Filter
open ChatgptAudit.WignerRapidityMeasure016
open scoped ENNReal

theorem shell_null_differentiable (r : ℝ) (hr : 0 < r) :
    Differentiable ℝ (fun p : ℝ => energy r p - p) := by
  have hbase : Differentiable ℝ (fun p : ℝ => r ^ 2 + p ^ 2) := by
    fun_prop
  have hnonzero (p : ℝ) : r ^ 2 + p ^ 2 ≠ 0 := by
    have hpos : 0 < r ^ 2 + p ^ 2 := by
      nlinarith [sq_pos_of_pos hr, sq_nonneg p]
    exact hpos.ne'
  convert! (hbase.sqrt hnonzero).sub differentiable_id using 1 <;>
    simp only [energy, Pi.sub_apply, id_eq]

theorem inverseLongitudinal_ae (r : ℝ) (hr : 0 < r) (P : ℝ → Prop)
    (hP : ∀ᵐ p : ℝ, P p) :
    ∀ᵐ u ∂(volume : Measure ℝ).restrict (Ioi 0), P (inverseLongitudinal r u) := by
  have hnull : (volume : Measure ℝ) {p | ¬ P p} = 0 := ae_iff.mp hP
  have himage : (volume : Measure ℝ)
      ((fun p : ℝ => energy r p - p) '' {p | ¬ P p}) = 0 :=
    addHaar_image_eq_zero_of_differentiableOn_of_addHaar_eq_zero volume
      (shell_null_differentiable r hr).differentiableOn hnull
  have hae : ∀ᵐ u : ℝ,
      u ∉ (fun p : ℝ => energy r p - p) '' {p | ¬ P p} := by
    exact measure_eq_zero_iff_ae_notMem.mp himage
  apply (ae_restrict_iff' measurableSet_Ioi).2
  filter_upwards [hae] with u hu
  intro huPos
  by_contra hbad
  apply hu
  exact ⟨inverseLongitudinal r u, hbad, null_inverseLongitudinal r u huPos⟩

theorem orbital_ae_nullMomentum (P : MomentumCoordinates → Prop)
    (hP : ∀ᵐ y ∂orbitalMeasure 0, P y) :
    ∀ᵐ q : Transverse,
      ∀ᵐ u ∂(volume : Measure ℝ).restrict (Ioi 0),
        P (nullMomentumCoordinates q u) := by
  have hd : ∀ᵐ y ∂momentumMeasure, orbitalWeight 0 y ≠ 0 → P y :=
    (ae_withDensity_iff (orbitalWeight_measurable 0)).mp hP
  have hf : ∀ᵐ q : Transverse, ∀ᵐ p : ℝ,
      orbitalWeight 0 (q, p) ≠ 0 → P (q, p) :=
    MeasureTheory.Measure.ae_ae_of_ae_prod hd
  filter_upwards [hf, transverseMass_pos_ae 0] with q hq hmass
  have hq' : ∀ᵐ p : ℝ, P (q, p) := by
    filter_upwards [hq] with p hp
    apply hp
    change ENNReal.ofReal (1 / energy (transverseMass 0 q) p) ≠ 0
    apply ne_of_gt
    apply ENNReal.ofReal_pos.mpr
    apply one_div_pos.mpr
    unfold energy
    apply Real.sqrt_pos.2
    nlinarith [sq_pos_of_pos hmass, sq_nonneg p]
  exact inverseLongitudinal_ae (transverseMass 0 q) hmass (fun p => P (q, p)) hq'

theorem orbital_aeEq_nullMomentum {E : Type*} (h g : MomentumCoordinates → E)
    (hhg : h =ᵐ[orbitalMeasure 0] g) :
    ∀ᵐ q : Transverse,
      ∀ᵐ u ∂(volume : Measure ℝ).restrict (Ioi 0),
        h (nullMomentumCoordinates q u) = g (nullMomentumCoordinates q u) :=
  orbital_ae_nullMomentum (fun y => h y = g y) hhg

end F1Fecho.NullFrequency

#print axioms F1Fecho.NullFrequency.shell_null_differentiable
#print axioms F1Fecho.NullFrequency.inverseLongitudinal_ae
#print axioms F1Fecho.NullFrequency.orbital_ae_nullMomentum
#print axioms F1Fecho.NullFrequency.orbital_aeEq_nullMomentum
