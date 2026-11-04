import TGLExt.F1Fecho394.FourierConjugation

/-! Exact identification of the previously constructed spectral conjugation in the original
rapidity chart. This proves q -> -q, r unchanged, complex conjugation and helicity exchange.
It does not assert the remaining Poincare covariance or a complete four-dimensional net. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
open MeasureTheory Filter

namespace F1Rede.GeometricIdentification
open TGLExt.ImportedSQ AuditF13v31
open ChatgptAudit.WignerRapidityMeasure016
open F1Rede.Canonical F1Rede.CanonicalWedge F1Rede.FiberConjugation

def curriedRapidity : H1 ≃ₗᵢ[ℂ] RapidityHilbert := toRapidity.trans canonicalFub

/-- Removing Fourier removes the reflected frequency: the antiunitary acts on each fiber at r. -/
theorem Jcandidate_curried (f : H1) :
    curriedRapidity (Jcandidate f) =
      FourierConjugation.pointwise transverseGeometricJ (curriedRapidity f) := by
  apply (Lp.fourierTransformₗᵢ ℝ TransverseFiber).injective
  rw [FourierConjugation.fourier_pointwise transverseGeometricJ transverseGeometricJ_involutive]
  change Phi (Jcandidate f) = Js (Phi f)
  rw [Jcandidate_apply, LinearIsometryEquiv.apply_symm_apply]

def reflectTransverse (p : Transverse × ℝ) : Transverse × ℝ := (-p.1,p.2)

theorem reflectTransverse_preserves :
    MeasurePreserving reflectTransverse momentumMeasure momentumMeasure := by
  exact (Measure.measurePreserving_neg (volume : Measure Transverse)).prod
    (MeasurePreserving.id (volume : Measure ℝ))

def productReflection : Lp Fib 2 momentumMeasure →ₗᵢ[ℂ] Lp Fib 2 momentumMeasure :=
  Lp.compMeasurePreservingₗᵢ ℂ reflectTransverse reflectTransverse_preserves

theorem productReflection_ae (f : Lp Fib 2 momentumMeasure) :
    productReflection f =ᵐ[momentumMeasure] fun p => f (-p.1,p.2) :=
  Lp.coeFn_compMeasurePreserving f reflectTransverse_preserves

/-- Explicit geometric action in rapidity coordinates; it is defined without using Jcandidate. -/
def productJ : Lp Fib 2 momentumMeasure →SL[starRingEnd ℂ] Lp Fib 2 momentumMeasure :=
  (fiberSwappedJ.toContinuousLinearEquiv.toContinuousLinearMap.compLpL 2 momentumMeasure).comp
    productReflection.toContinuousLinearMap

theorem productJ_ae (f : Lp Fib 2 momentumMeasure) :
    productJ f =ᵐ[momentumMeasure] fun p => fiberSwappedJ (f (-p.1,p.2)) := by
  have hp := fiberSwappedJ.toContinuousLinearEquiv.toContinuousLinearMap.coeFn_compLpL
    (productReflection f)
  filter_upwards [hp,productReflection_ae f] with p h1 h2
  change (fiberSwappedJ.toContinuousLinearEquiv.toContinuousLinearMap.compLpL 2 momentumMeasure
    (productReflection f)) p = _
  rw [h1]
  change fiberSwappedJ (productReflection f p) = _
  rw [h2]

/-- Fubini preserves the explicit transverse action, as equality of L² operators. -/
theorem canonicalFub_productJ (f : Lp Fib 2 momentumMeasure) :
    canonicalFub (productJ f) =
      FourierConjugation.pointwise transverseGeometricJ (canonicalFub f) := by
  apply Lp.ext
  filter_upwards [canonicalFub_sections (productJ f),
    FourierConjugation.pointwise_ae transverseGeometricJ (canonicalFub f),
    canonicalFub_sections f,
    ae_ae_reverse (μ := (volume : Measure Transverse)) (ν := (volume : Measure ℝ))
      (productJ_ae f)] with r hc hj hf hp
  rw [hj]
  apply Lp.ext
  have hneg := (Measure.measurePreserving_neg (volume : Measure Transverse)).quasiMeasurePreserving.ae hf
  filter_upwards [hc, hp, hneg, transverseGeometricJ_ae (canonicalFub f r)] with q h1 h2 h3 h4
  rw [h1,h2,h4,h3]

/-- The previously constructed spectral antiunitary equals the independently defined geometric action. -/
theorem Jcandidate_rapidity (f : H1) : toRapidity (Jcandidate f) = productJ (toRapidity f) := by
  apply canonicalFub.injective
  rw [canonicalFub_productJ]
  exact Jcandidate_curried f

def geometricJ : H1 →SL[starRingEnd ℂ] H1 :=
  toRapidity.symm.toContinuousLinearEquiv.toContinuousLinearMap.comp
    (productJ.comp toRapidity.toContinuousLinearEquiv.toContinuousLinearMap)

theorem Jcandidate_eq_geometricJ (f : H1) : Jcandidate f = geometricJ f := by
  apply toRapidity.injective
  change toRapidity (Jcandidate f) = toRapidity (toRapidity.symm (productJ (toRapidity f)))
  rw [LinearIsometryEquiv.apply_symm_apply]
  exact Jcandidate_rapidity f

/-- Full almost-everywhere formula on the product measure: r is unchanged. -/
theorem Jcandidate_rapidity_ae (f : H1) :
    toRapidity (Jcandidate f) =ᵐ[momentumMeasure]
      fun p => fiberSwappedJ (toRapidity f (-p.1,p.2)) := by
  rw [Jcandidate_rapidity]
  exact productJ_ae (toRapidity f)

theorem Jcandidate_rapidity_coordinates (f : H1) :
    ∀ᵐ p ∂momentumMeasure, ∀ i : Fin 2,
      toRapidity (Jcandidate f) p i = star (toRapidity f (-p.1,p.2) (helicitySwap i)) := by
  filter_upwards [Jcandidate_rapidity_ae f] with p hp
  intro i
  rw [hp,fiberSwappedJ_apply]

#print axioms Jcandidate_curried
#print axioms canonicalFub_productJ
#print axioms Jcandidate_rapidity
#print axioms Jcandidate_eq_geometricJ
#print axioms Jcandidate_rapidity_coordinates
end F1Rede.GeometricIdentification
