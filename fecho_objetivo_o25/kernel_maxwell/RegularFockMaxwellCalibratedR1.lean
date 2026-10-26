import RegularFockMaxwellQuadraticR2

/-! Constant calibration of the existing Maxwell quadratic form on the SAME
regular Fock domain and canonical assembly. The positive factor (2*pi)^(-3)
transports the existing tensor laws; it does not prove a null-plane charge
identity, a nonzero modular-energy witness, or an inhabitant of the remaining
trace/PF input. R2 is preserved. This sandbox component requires independent
review and does not close the full R8 requirement. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.ContratoQGv32
open TGLExt.MaxwellBridge
open F1Fecho.NetworkReuse F1Fecho.NetworkModularCore

/-- All existing tensor laws are homogeneous in the stress. -/
def scaleMaxwellQuadraticForm {L : LightOneParticle} {C : FockCertificate L}
    (c : ℝ) (Q : MaxwellQuadraticForm C) : MaxwellQuadraticForm C where
  Dom := Q.Dom
  Dom_vac := Q.Dom_vac
  Dom_translate := Q.Dom_translate
  Dom_boost := Q.Dom_boost
  Q := fun ψ x => c • Q.Q ψ x
  Q_vac := fun x => by rw [Q.Q_vac x, smul_zero]
  Q_covariant := fun a ψ x hψ => by rw [Q.Q_covariant a ψ x hψ]
  Q_symmetric := fun ψ x hψ => by
    ext μ ν
    change c * Q.Q ψ x ν μ = c * Q.Q ψ x μ ν
    exact congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => c * M μ ν)
      (Q.Q_symmetric ψ x hψ)
  Q_test_integrable := fun ψ hψ ν μ f hf hc => by
    have hi := (Q.Q_test_integrable ψ hψ ν μ f hf hc).const_mul c
    have he (x : Fin 4 → ℝ) :
        metricSignV32 μ * (c • Q.Q ψ x) μ ν * testDerivativeV32 f μ x =
          c * (metricSignV32 μ * Q.Q ψ x μ ν * testDerivativeV32 f μ x) := by
      change metricSignV32 μ * (c * Q.Q ψ x μ ν) * testDerivativeV32 f μ x = _
      ring
    simpa only [he] using hi
  Q_conserved := fun ψ hψ ν f hf hc => by
    have he (μ : Fin 4) (x : Fin 4 → ℝ) :
        metricSignV32 μ * (c • Q.Q ψ x) μ ν * testDerivativeV32 f μ x =
          c * (metricSignV32 μ * Q.Q ψ x μ ν * testDerivativeV32 f μ x) := by
      change metricSignV32 μ * (c * Q.Q ψ x μ ν) * testDerivativeV32 f μ x = _
      ring
    simp_rw [he, integral_const_mul]
    rw [← Finset.mul_sum, Q.Q_conserved ψ hψ ν f hf hc, mul_zero]
  Q_boost_covariant := fun s ψ x hψ => by
    rw [Q.Q_boost_covariant s ψ x hψ]
    simp only [Matrix.mul_smul, Matrix.smul_mul]

/-- Proposed angular-Fourier calibration; the charge theorem is separate. -/
def maxwellStressCalibration : ℝ := ((2 * Real.pi) ^ (3 : ℕ))⁻¹

theorem maxwellStressCalibration_pos : 0 < maxwellStressCalibration := by
  unfold maxwellStressCalibration
  positivity

def regularMaxwellCalibratedForm {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) : MaxwellQuadraticForm A.toCertificate :=
  scaleMaxwellQuadraticForm maxwellStressCalibration (regularMaxwellQuadraticForm A)

theorem regularMaxwellCalibratedForm_domain {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) :
    (regularMaxwellCalibratedForm A).Dom = (regularFockDomain : Set F1Rede.BosonicFock.F) := rfl

theorem regularMaxwellCalibratedForm_exact {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (ψ : regularFockDomain) (x : Fin 4 → ℝ) :
    (regularMaxwellCalibratedForm A).Q ψ.val x =
      maxwellStressCalibration • realCoordinateStress ψ x := by
  change maxwellStressCalibration • (regularMaxwellQuadraticForm A).Q ψ.val x = _
  rw [regularMaxwellQuadraticForm_exact A ψ x]

theorem regularMaxwellCalibratedStress_on_domain {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (ψ : regularFockDomain) :
    (toStress (regularMaxwellCalibratedForm A)).T ψ.val =
      fun x => maxwellStressCalibration • realCoordinateStress ψ x := by
  have hm : ψ.val ∈ (regularMaxwellCalibratedForm A).Dom := ψ.property
  exact (toStress_on_dom (regularMaxwellCalibratedForm A) hm).trans
    (funext (fun x => regularMaxwellCalibratedForm_exact A ψ x))

/-- A nonzero point tensor remains nonzero; this is not modular nontriviality. -/
theorem regularMaxwellCalibratedForm_point_nontrivial {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) :
    ∃ ψ : A.toCertificate.F, ψ ∈ (regularMaxwellCalibratedForm A).Dom ∧
      0 < (regularMaxwellCalibratedForm A).Q ψ 0 0 0 := by
  obtain ⟨ψ, hψ, hp⟩ := regularMaxwellQuadraticForm_nontrivial A
  refine ⟨ψ, hψ, ?_⟩
  change 0 < maxwellStressCalibration * (regularMaxwellQuadraticForm A).Q ψ 0 0 0
  exact mul_pos maxwellStressCalibration_pos hp

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.scaleMaxwellQuadraticForm
#print axioms F1Fecho.MaxwellGlobal.maxwellStressCalibration_pos
#print axioms F1Fecho.MaxwellGlobal.regularMaxwellCalibratedForm
#print axioms F1Fecho.MaxwellGlobal.regularMaxwellCalibratedForm_domain
#print axioms F1Fecho.MaxwellGlobal.regularMaxwellCalibratedForm_exact
#print axioms F1Fecho.MaxwellGlobal.regularMaxwellCalibratedStress_on_domain
#print axioms F1Fecho.MaxwellGlobal.regularMaxwellCalibratedForm_point_nontrivial
