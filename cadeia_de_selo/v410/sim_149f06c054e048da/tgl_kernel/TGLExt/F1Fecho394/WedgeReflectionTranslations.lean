import TGLExt.F1Fecho394.GeometricIdentification

/-! Translation covariance of the constructed antiunitary, on the unchanged canonical H1.
The reflection is exactly diag(-1,-1,+1,+1) in the existing (t,x1,x2,x3) coordinates.
This is one geometric covariance law; no full Poincare net is asserted. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
open MeasureTheory Filter

namespace F1Rede.WedgeReflectionTranslations
open TGLExt.ImportedSQ AuditF13v31
open ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.WignerOrbit016
open F1Rede.GeometricIdentification F1Rede.CanonicalWedge F1Rede.FiberConjugation

def wedgeReflection (a : Fin 4 → ℝ) : Fin 4 → ℝ := ![-a 0,-a 1,a 2,a 3]

theorem wedgeReflection_involutive : Function.Involutive wedgeReflection := by
  intro a
  ext i
  fin_cases i <;> simp [wedgeReflection]

theorem transverseMass_neg (m : ℝ) (q : Transverse) : transverseMass m (-q) = transverseMass m q := by
  simp [transverseMass, Pi.neg_apply]

theorem pairing_reflection (a : Fin 4 → ℝ) (p : MomentumCoordinates) :
    orbitPairing (wedgeReflection a) (shellMomentum 0 (rapidityChart 0 p)) =
      -orbitPairing a (shellMomentum 0 (rapidityChart 0 (reflectTransverse p))) := by
  simp only [orbitPairing,shellMomentum,rapidityChart,reflectTransverse,transverseMass_neg]
  let k := longitudinal (transverseMass 0 p.1) p.2
  let e := energy (transverseMass 0 p.1) k
  change (-a 0)*e - (-a 1)*k - a 2*(p.1 0) - a 3*(p.1 1) =
    -(a 0*e - a 1*k - a 2*(-p.1 0) - a 3*(-p.1 1))
  ring

theorem phase_reflection (a : Fin 4 → ℝ) (p : MomentumCoordinates) :
    star (orbitalPhase 0 a (rapidityChart 0 (reflectTransverse p))) =
      orbitalPhase 0 (wedgeReflection a) (rapidityChart 0 p) := by
  unfold orbitalPhase phase
  rw [pairing_reflection]
  change (starRingEnd ℂ) (Complex.exp _) = Complex.exp _
  rw [← Complex.exp_conj]
  congr 1
  simp

theorem toRapidity_U1_ae (a : Fin 4 → ℝ) (f : H1) :
    toRapidity (U1 a f) =ᵐ[momentumMeasure]
      fun p => orbitalPhase 0 a (rapidityChart 0 p) • toRapidity f p := by
  have hphase := (rapidityChart_measurePreserving 0).quasiMeasurePreserving.ae
    (orbitalTranslation_ae 0 a f)
  filter_upwards [orbitalL2Pullback_ae 0 (U1 a f), orbitalL2Pullback_ae 0 f, hphase]
    with p h1 h2 h3
  change toRapidity (U1 a f) p = U1 a f (rapidityChart 0 p) at h1
  change toRapidity f p = f (rapidityChart 0 p) at h2
  change U1 a f (rapidityChart 0 p) = orbitalPhase 0 a (rapidityChart 0 p) • f (rapidityChart 0 p) at h3
  rw [h1,h3,h2]

/-- Reflection intertwines translations by the exact geometric action on spacetime. -/
theorem Jcandidate_translation_intertwines (a : Fin 4 → ℝ) (f : H1) :
    Jcandidate (U1 a f) = U1 (wedgeReflection a) (Jcandidate f) := by
  apply toRapidity.injective
  apply Lp.ext
  have hr := reflectTransverse_preserves.quasiMeasurePreserving.ae (toRapidity_U1_ae a f)
  filter_upwards [Jcandidate_rapidity_ae (U1 a f),
    toRapidity_U1_ae (wedgeReflection a) (Jcandidate f), Jcandidate_rapidity_ae f,hr]
    with p h1 h2 h3 h4
  change toRapidity (U1 a f) (-p.1,p.2) =
    orbitalPhase 0 a (rapidityChart 0 (reflectTransverse p)) • toRapidity f (-p.1,p.2) at h4
  rw [h1,h4,map_smulₛₗ,h2,h3]
  exact congrArg (fun z : ℂ => z • fiberSwappedJ (toRapidity f (-p.1,p.2))) (phase_reflection a p)

/-- J U1(a) J = U1(jW a) on the canonical one-particle Hilbert space. -/
theorem Jcandidate_conjugates_translations (a : Fin 4 → ℝ) (f : H1) :
    Jcandidate (U1 a (Jcandidate f)) = U1 (wedgeReflection a) f := by
  rw [Jcandidate_translation_intertwines, Jcandidate_involutive]

#print axioms pairing_reflection
#print axioms phase_reflection
#print axioms toRapidity_U1_ae
#print axioms Jcandidate_translation_intertwines
#print axioms Jcandidate_conjugates_translations
end F1Rede.WedgeReflectionTranslations
