import OppositeNullAmplitude
import TGLExt.NullMomentumInvariant

set_option autoImplicit false
set_option maxHeartbeats 2200000

/-! Opposite-null coordinates, phase, and the orbital measure reflection. -/
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory SchwartzMap
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open TGLExt.NullMomentumInvariant
open F1Fecho.MaxwellStress ChatgptAudit.WignerRapidityMeasure016 F1Fecho.NullFrequency

/-- Reflection of the longitudinal momentum coordinate. -/
def longitudinalReflection (y : MomentumCoordinates) : MomentumCoordinates := (y.1, -y.2)

theorem longitudinalReflection_measurable : Measurable longitudinalReflection := by
  unfold longitudinalReflection
  fun_prop

theorem longitudinalReflection_involutive : Function.Involutive longitudinalReflection := by
  intro y
  cases y
  simp [longitudinalReflection]

/-- The reflection as a measurable involution. -/
def longitudinalReflectionEquiv : MomentumCoordinates ≃ᵐ MomentumCoordinates :=
  MeasurableEquiv.ofInvolutive longitudinalReflection longitudinalReflection_involutive
    longitudinalReflection_measurable

/-- The orbital weight is even in the longitudinal coordinate. -/
theorem longitudinalReflection_weight (y : MomentumCoordinates) :
    orbitalWeight 0 (longitudinalReflection y) = orbitalWeight 0 y := by
  simp [longitudinalReflection, orbitalWeight, energy, transverseMass]

/-- The reflected orbital measure is the same measure. -/
theorem longitudinalReflection_measurePreserving :
    MeasurePreserving longitudinalReflectionEquiv (orbitalMeasure 0) (orbitalMeasure 0) := by
  refine ⟨longitudinalReflection_measurable, ?_⟩
  have hc : longitudinalReflectionEquiv ∘ longitudinalReflectionEquiv = id := by
    funext y
    exact longitudinalReflection_involutive y
  ext s hs
  rw [Measure.map_apply longitudinalReflectionEquiv.measurable hs]
  simp only [orbitalMeasure, withDensity_apply _ (longitudinalReflectionEquiv.measurable hs),
    withDensity_apply _ hs]
  have h := setLIntegral_map (μ := momentumMeasure) hs (orbitalWeight_measurable 0)
    longitudinalReflectionEquiv.measurable
  convert h using 1
  rw [← withDensity_apply _ (longitudinalReflectionEquiv.measurable hs), ← withDensity_apply _ hs]
  rw [Measure.map_apply (μ := momentumMeasure) longitudinalReflectionEquiv.measurable hs]

/-- Integrals are invariant under longitudinal reflection. -/
theorem integral_longitudinalReflection (f : MomentumCoordinates → ℂ) :
    (∫ y, f (longitudinalReflection y) ∂orbitalMeasure 0) = ∫ y, f y ∂orbitalMeasure 0 :=
  longitudinalReflection_measurePreserving.integral_comp' f

/-- Integrability is preserved by longitudinal reflection. -/
theorem integrable_longitudinalReflection (f : MomentumCoordinates → ℂ)
    (hf : Integrable f (orbitalMeasure 0)) :
    Integrable (fun y => f (longitudinalReflection y)) (orbitalMeasure 0) :=
  longitudinalReflection_measurePreserving.integrable_comp_of_integrable hf

/-- The opposite momentum coordinate has the opposite future frequency `u`. -/
def oppositeMomentumCoordinates (q : Transverse) (u : ℝ) : MomentumCoordinates :=
  (q, -inverseLongitudinal (transverseMass 0 q) u)

theorem shellOppositeFrequency_oppositeMomentumCoordinates (q : Transverse)
    {u : ℝ} (hu : 0 < u) : shellOppositeFrequency (oppositeMomentumCoordinates q u) = u := by
  have hn := null_inverseLongitudinal (transverseMass 0 q) u hu
  have he : shellEnergy (q, -inverseLongitudinal (transverseMass 0 q) u) =
      energy (transverseMass 0 q) (inverseLongitudinal (transverseMass 0 q) u) := by
    simp [shellEnergy, energy, transverseMass, neg_sq]
  unfold oppositeMomentumCoordinates shellOppositeFrequency
  rw [he]
  change energy (transverseMass 0 q) (inverseLongitudinal (transverseMass 0 q) u) -
    inverseLongitudinal (transverseMass 0 q) u = u
  exact hn

/-- A point on the opposite null plane. -/
def oppositeNullPlanePoint (ell : ℝ) (z : Fin 2 → ℝ) : Spacetime :=
  WithLp.toLp 2 (ell • oppositeNullDir + screenEmbed z)

/-- The phase on the opposite null plane. -/
theorem wavePhase_oppositeNullPlanePoint (ell : ℝ) (z : Fin 2 → ℝ) (y : MomentumCoordinates) :
    wavePhase (oppositeNullPlanePoint ell z) y =
      Complex.exp (Complex.I *
        ((-shellOppositeFrequency y * ell + y.1 0 * z 0 + y.1 1 * z 1 : ℝ) : ℂ)) := by
  have hp : -(inner ℝ (metricFlip (shellEmbedding y)) (oppositeNullPlanePoint ell z)) =
      -shellOppositeFrequency y * ell + y.1 0 * z 0 + y.1 1 * z 1 := by
    rw [metricFlip_inner]
    simp [oppositeNullPlanePoint, shellEmbedding, oppositeNullDir, screenEmbed,
      shellOppositeFrequency, shellEnergy, shellMomentum] <;> ring
  unfold wavePhase
  rw [hp]

/-- The opposite frequency factor cancels in the orbital measure. -/
theorem orbital_oppositeFrequency_bochner_cancel (f : MomentumCoordinates → ℂ)
    (hf : Integrable (fun y => (shellOppositeFrequency y) • f y) (orbitalMeasure 0)) :
    (∫ y, (shellOppositeFrequency y) • f y ∂orbitalMeasure 0) =
      ∫ q : Transverse, ∫ u in Ioi 0, f (oppositeMomentumCoordinates q u) := by
  have href0 := integrable_longitudinalReflection (fun y => (shellOppositeFrequency y) • f y) hf
  have href : Integrable (fun y =>
      (energy (transverseMass 0 y.1) y.2 - y.2) • f (longitudinalReflection y))
      (orbitalMeasure 0) := by
    simpa [shellOppositeFrequency, longitudinalReflection, shellEnergy, energy, transverseMass,
      sub_eq_add_neg] using href0
  have heq := orbital_nullFrequency_bochner_cancel (fun y => f (longitudinalReflection y)) href
  have hreflect := integral_longitudinalReflection (fun y => (shellOppositeFrequency y) • f y)
  rw [← hreflect]
  simpa [oppositeMomentumCoordinates, nullMomentumCoordinates, longitudinalReflection,
    shellOppositeFrequency, shellEnergy, energy, transverseMass, sub_eq_add_neg] using heq

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.longitudinalReflection_weight
#print axioms F1Fecho.MaxwellGlobal.longitudinalReflection_measurePreserving
#print axioms F1Fecho.MaxwellGlobal.integral_longitudinalReflection
#print axioms F1Fecho.MaxwellGlobal.integrable_longitudinalReflection
#print axioms F1Fecho.MaxwellGlobal.shellOppositeFrequency_oppositeMomentumCoordinates
#print axioms F1Fecho.MaxwellGlobal.wavePhase_oppositeNullPlanePoint
#print axioms F1Fecho.MaxwellGlobal.orbital_oppositeFrequency_bochner_cancel
