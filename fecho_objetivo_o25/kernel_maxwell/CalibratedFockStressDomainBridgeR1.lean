import RegularFockMaxwellCalibratedR1
import UnitaryFourierFockStressR1

/-! Reuse the already constructed calibrated Maxwell form. Its constant is
definitionally the unitary Fourier stress scale, and its tensor agrees with
the normalized regular Fock form. An invariant subdomain may be named without
changing the form on that domain. The input A still contains the unresolved
trace/PF data. No charge identity, smooth-domain inhabitant or nonzero modular
energy is supplied as an assumption disguised as a proof here. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open TGLExt TGLExt.ImportedSQ TGLExt.MaxwellBridge
open F1Fecho.NetworkReuse F1Fecho.NetworkModularCore

theorem maxwellStressCalibration_eq_unitaryFourierStressScale :
    maxwellStressCalibration = unitaryFourierStressScale := rfl

theorem calibratedForm_eq_unitaryFourierFock {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (ψ : regularFockDomain)
    (x : Fin 4 → ℝ) (μ ν : Fin 4) :
    (regularMaxwellCalibratedForm A).Q ψ.val x μ ν =
      (unitaryFourierPointStressForm ψ ψ μ ν (WithLp.toLp 2 x)).re := by
  rw [regularMaxwellCalibratedForm_exact A ψ x]
  change maxwellStressCalibration * realCoordinateStress ψ x μ ν = _
  simp only [maxwellStressCalibration_eq_unitaryFourierStressScale,
    realCoordinateStress, unitaryFourierPointStressForm, Complex.mul_re,
    Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero]

theorem calibratedStress_eq_unitaryFourierFock {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (ψ : regularFockDomain)
    (x : Fin 4 → ℝ) (μ ν : Fin 4) :
    (toStress (regularMaxwellCalibratedForm A)).T ψ.val x μ ν =
      (unitaryFourierPointStressForm ψ ψ μ ν (WithLp.toLp 2 x)).re := by
  rw [toStress_on_dom (regularMaxwellCalibratedForm A) ψ.property]
  exact calibratedForm_eq_unitaryFourierFock A ψ x μ ν

/-- Restriction preserves the actual quadratic form; invariance is explicit. -/
def restrictMaxwellQuadraticForm {L : LightOneParticle} {C : FockCertificate L}
    (Q : MaxwellQuadraticForm C) (D : Set C.F) (hD : D ⊆ Q.Dom)
    (hv : C.Ω ∈ D)
    (ht : ∀ (a : Fin 4 → ℝ) (ψ : C.F), C.Γ (U1 a) ψ ∈ D ↔ ψ ∈ D)
    (hb : ∀ (s : ℝ) (ψ : C.F), C.Γ (B0 s) ψ ∈ D ↔ ψ ∈ D) :
    MaxwellQuadraticForm C where
  Dom := D
  Dom_vac := hv
  Dom_translate := ht
  Dom_boost := hb
  Q := Q.Q
  Q_vac := Q.Q_vac
  Q_covariant := fun a ψ x h => Q.Q_covariant a ψ x (hD h)
  Q_symmetric := fun ψ x h => Q.Q_symmetric ψ x (hD h)
  Q_test_integrable := fun ψ h => Q.Q_test_integrable ψ (hD h)
  Q_conserved := fun ψ h => Q.Q_conserved ψ (hD h)
  Q_boost_covariant := fun s ψ x h => Q.Q_boost_covariant s ψ x (hD h)

theorem restrictMaxwellQuadraticForm_on_domain
    {L : LightOneParticle} {C : FockCertificate L}
    (Q : MaxwellQuadraticForm C) (D : Set C.F) (hD : D ⊆ Q.Dom)
    (hv : C.Ω ∈ D)
    (ht : ∀ (a : Fin 4 → ℝ) (ψ : C.F), C.Γ (U1 a) ψ ∈ D ↔ ψ ∈ D)
    (hb : ∀ (s : ℝ) (ψ : C.F), C.Γ (B0 s) ψ ∈ D ↔ ψ ∈ D)
    (ψ : C.F) (hψ : ψ ∈ D) :
    (toStress (restrictMaxwellQuadraticForm Q D hD hv ht hb)).T ψ =
      (toStress Q).T ψ := by
  rw [toStress_on_dom (restrictMaxwellQuadraticForm Q D hD hv ht hb) hψ,
    toStress_on_dom Q (hD hψ)]
  rfl

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.maxwellStressCalibration_eq_unitaryFourierStressScale
#print axioms F1Fecho.MaxwellGlobal.calibratedForm_eq_unitaryFourierFock
#print axioms F1Fecho.MaxwellGlobal.calibratedStress_eq_unitaryFourierFock
#print axioms F1Fecho.MaxwellGlobal.restrictMaxwellQuadraticForm
#print axioms F1Fecho.MaxwellGlobal.restrictMaxwellQuadraticForm_on_domain
