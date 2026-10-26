import CompactFockNullStressMomentR4
import CalibratedFockStressDomainBridgeR1
import TGLExt.ContratoQG_v31_Teoremas
import Mathlib.MeasureTheory.Group.Integral
import Mathlib.MeasureTheory.Group.MeasurableEquiv

/-! Convert the existing real Fock null moment into the contract's bilateral
nullPlaneCharge. The existing nullCoordinateEquiv is composed with id times
screen negation: no new Jacobian or alternative spacetime chart is postulated.
The same calibrated tensor and VF act on the same regularFockDomain.
The modular factor is supplied by the existing lightH2 theorem for arbitrary
explicit KillingNormalization N. No physical clock is selected here.
RemainingModularCoreInput remains an explicit unresolved assembly input;
the invariant smooth certificate domain and nonzero witness are separate. -/
set_option autoImplicit false
set_option maxHeartbeats 2200000
noncomputable section

namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open F1Fecho.NetworkReuse F1Fecho.NetworkModularCore
open F1Rede.BosonicFockGroupActions ChatgptAudit.WignerRapidityMeasure016

/-- Only the screen is reflected; the longitudinal coordinate is fixed. -/
def nullScreenReflection : (ℝ × Transverse) ≃ᵐ (ℝ × Transverse) :=
  (MeasurableEquiv.refl ℝ).prodCongr (MeasurableEquiv.neg Transverse)

@[simp] theorem nullScreenReflection_apply (z : ℝ × Transverse) :
    nullScreenReflection z = (z.1, -z.2) := rfl

theorem nullScreenReflection_measurePreserving : MeasurePreserving nullScreenReflection := by
  change MeasurePreserving (Prod.map (id : ℝ → ℝ) (Neg.neg : Transverse → Transverse))
    volume volume
  simpa only [Measure.volume_eq_prod] using
    (MeasurePreserving.id (volume : Measure ℝ)).prod
      (Measure.measurePreserving_neg (volume : Measure Transverse))

/-- Reuse the existing null Fourier coordinate equivalence after the screen reflection. -/
def nullContractCoordinateEquiv : (ℝ × Transverse) ≃ᵐ NullFourierSpace :=
  nullScreenReflection.trans nullCoordinateEquiv

@[simp] theorem nullContractCoordinateEquiv_apply (z : ℝ × Transverse) :
    nullContractCoordinateEquiv z = nullFourierCoordinates (-z.2) z.1 := by
  change nullCoordinateEquiv (z.1, -z.2) = _
  exact nullCoordinateEquiv_apply (z.1, -z.2)

theorem nullContractCoordinateEquiv_measurePreserving :
    MeasurePreserving nullContractCoordinateEquiv :=
  nullCoordinateEquiv_measurePreserving.comp nullScreenReflection_measurePreserving

@[simp] theorem nullContractCoordinateEquiv_zero (z : ℝ × Transverse) :
    (nullContractCoordinateEquiv z) 0 = z.1 := by
  simp [nullContractCoordinateEquiv_apply, nullFourierCoordinates]

@[simp] theorem nullContractCoordinateEquiv_screen (z : ℝ × Transverse) :
    nullFourierScreen (nullContractCoordinateEquiv z) = z.2 := by
  ext a
  simp [nullFourierScreen, nullContractCoordinateEquiv_apply, nullFourierCoordinates]

theorem nullContractCoordinateEquiv_plane (z : ℝ × Transverse) :
    nullPlanePoint ((nullContractCoordinateEquiv z) 0)
      (nullFourierScreen (nullContractCoordinateEquiv z)) =
      WithLp.toLp 2 (z.1 • nullDir + screenEmbed z.2) := by
  rw [nullContractCoordinateEquiv_zero, nullContractCoordinateEquiv_screen]
  ext μ
  fin_cases μ <;> simp [nullPlanePoint, nullDir, screenEmbed]

private theorem pairing_nullDir_components (M : Matrix (Fin 4) (Fin 4) ℝ) :
    pairing M nullDir nullDir = M 0 0 + M 0 1 + M 1 0 + M 1 1 := by
  simp [pairing, nullDir, Matrix.mulVec, dotProduct, Fin.sum_univ_four] <;> ring

theorem calibrated_nullEnergy_contract_coordinates {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (ψ : regularFockDomain) (z : ℝ × Transverse) :
    nullEnergy (toStress (regularMaxwellCalibratedForm A)).toStressTensorData ψ.val
      (z.1 • nullDir + screenEmbed z.2) =
      (unitaryFourierFockNullStress ψ ψ (nullContractCoordinateEquiv z)).re := by
  rw [nullEnergy, pairing_nullDir_components]
  simp_rw [calibratedStress_eq_unitaryFourierFock A ψ]
  simp only [unitaryFourierFockNullStress, nullContractCoordinateEquiv_plane, Complex.add_re]

theorem calibrated_nullCharge_integrand_coordinates {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (ψ : regularFockDomain) (z : ℝ × Transverse) :
    z.1 * nullEnergy (toStress (regularMaxwellCalibratedForm A)).toStressTensorData ψ.val
      (z.1 • nullDir + screenEmbed z.2) =
      (nullContractCoordinateEquiv z) 0 *
        (unitaryFourierFockNullStress ψ ψ (nullContractCoordinateEquiv z)).re := by
  rw [calibrated_nullEnergy_contract_coordinates, nullContractCoordinateEquiv_zero]

/-- The equivalence transports even the integrability obligation in the contract. -/
theorem axisCompact_calibrated_nullCharge_integrable {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (ψ : regularFockDomain) (hψ : AxisCompactFock ψ) :
    Integrable (fun z : ℝ × (Fin 2 → ℝ) => z.1 *
      nullEnergy (toStress (regularMaxwellCalibratedForm A)).toStressTensorData ψ.val
        (z.1 • nullDir + screenEmbed z.2)) := by
  have hi := nullContractCoordinateEquiv_measurePreserving.integrable_comp_of_integrable
    (axisCompact_fockNullStress_real_moment_integrable ψ hψ)
  apply hi.congr
  filter_upwards [] with z
  exact (calibrated_nullCharge_integrand_coordinates A ψ z).symm

theorem calibrated_nullPlaneCharge_eq_moment {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (ψ : regularFockDomain) :
    nullPlaneCharge (toStress (regularMaxwellCalibratedForm A)).toStressTensorData ψ.val =
      ∫ x : NullFourierSpace, x 0 * (unitaryFourierFockNullStress ψ ψ x).re := by
  unfold nullPlaneCharge
  calc
    _ = ∫ z : ℝ × Transverse, (nullContractCoordinateEquiv z) 0 *
        (unitaryFourierFockNullStress ψ ψ (nullContractCoordinateEquiv z)).re := by
      apply integral_congr_ae
      filter_upwards [] with z
      exact calibrated_nullCharge_integrand_coordinates A ψ z
    _ = _ := nullContractCoordinateEquiv_measurePreserving.integral_comp'
      (fun x : NullFourierSpace => x 0 * (unitaryFourierFockNullStress ψ ψ x).re)

theorem axisCompact_calibrated_hasBoostEnergy_nullPlaneCharge {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (ψ : regularFockDomain) (hψ : AxisCompactFock ψ) :
    HasBoostEnergy VF ψ.val
      (nullPlaneCharge (toStress (regularMaxwellCalibratedForm A)).toStressTensorData ψ.val) := by
  rw [calibrated_nullPlaneCharge_eq_moment]
  exact axisCompact_fock_hasBoostEnergy_null_moment ψ hψ

theorem axisCompact_calibrated_hasModularEnergy_nullPlaneCharge {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (N : KillingNormalization)
    (ψ : regularFockDomain) (hψ : AxisCompactFock ψ) :
    HasModularEnergy (lightDelta A.toCertificate) ψ.val
      (2 * Real.pi * nullPlaneCharge
        (toStress (regularMaxwellCalibratedForm A)).toStressTensorData ψ.val) := by
  apply ContratoH2.modularEnergy_of_boostEnergy (lightH2 A.toCertificate N)
  change HasBoostEnergy VF ψ.val _
  exact axisCompact_calibrated_hasBoostEnergy_nullPlaneCharge A ψ hψ

/-- The charge equation on the explicit smooth coefficient core of the same Fock. -/
theorem axisCompact_calibrated_modular_charge_link {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (N : KillingNormalization)
    (ψ : regularFockDomain) (hψ : AxisCompactFock ψ) (k : ℝ)
    (hk : HasModularEnergy (lightDelta A.toCertificate) ψ.val k) :
    k = 2 * Real.pi * nullPlaneCharge
      (toStress (regularMaxwellCalibratedForm A)).toStressTensorData ψ.val :=
  ContratoH2.modularEnergy_unique hk
    (axisCompact_calibrated_hasModularEnergy_nullPlaneCharge A N ψ hψ)

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.nullScreenReflection_measurePreserving
#print axioms F1Fecho.MaxwellGlobal.nullContractCoordinateEquiv_measurePreserving
#print axioms F1Fecho.MaxwellGlobal.nullContractCoordinateEquiv_plane
#print axioms F1Fecho.MaxwellGlobal.calibrated_nullEnergy_contract_coordinates
#print axioms F1Fecho.MaxwellGlobal.axisCompact_calibrated_nullCharge_integrable
#print axioms F1Fecho.MaxwellGlobal.calibrated_nullPlaneCharge_eq_moment
#print axioms F1Fecho.MaxwellGlobal.axisCompact_calibrated_hasBoostEnergy_nullPlaneCharge
#print axioms F1Fecho.MaxwellGlobal.axisCompact_calibrated_hasModularEnergy_nullPlaneCharge
#print axioms F1Fecho.MaxwellGlobal.axisCompact_calibrated_modular_charge_link
