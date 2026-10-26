import TGLExt.NullRestSector
import TGLExt.MaxwellLiteratureBridge

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# Interface exata entre o certificado Maxwell e a escala nula

`Regular` fornece a integrabilidade da carga ponderada no plano e caudas
unilaterais; não fornece as integrais completas das duas componentes de momento,
positividade ou repouso. Este módulo deriva somente o que o certificado contém:
um estado com carga não nula e a recusa dessa carga como `τ` dual.
-/
namespace TGLExt.MaxwellNullScalingBridge
open Matrix TGLExt.ContratoQGv31 TGLExt.ContratoQGv32 MeasureTheory
open TGLExt.ImportedSQ TGLExt.NullEnergyScaling

/-- A segunda cláusula de `Regular`, no ponto zero, é exatamente a integrabilidade
    da carga usada pelo teorema de invariância. -/
theorem maxwell_regular_charge_integrable {L : LightOneParticle} {C : FockCertificate L}
    (M : MaxwellCertificate C) (ψ : C.F)
    (hψ : Regular M.Dom M.T.toStressTensorData ψ) :
    Integrable (chargeIntegrand M.T.toStressTensorData ψ) := by
  change Integrable (fun p : ℝ × (Fin 2 → ℝ) =>
    p.1 * nullEnergy M.T.toStressTensorData ψ (p.1 • nullDir + screenEmbed p.2))
  apply (hψ.2.1 0).congr
  filter_upwards [] with p
  simp

/-- A energia modular não nula força a carga nula a ser não nula. -/
theorem maxwell_charge_ne_zero_of_modularEnergy {L : LightOneParticle} {C : FockCertificate L}
    (M : MaxwellCertificate C) (ψ : C.F)
    (hψ : Regular M.Dom M.T.toStressTensorData ψ)
    (k : ℝ) (hk : HasModularEnergy (lightDelta C) ψ k) (hkne : k ≠ 0) :
    nullPlaneCharge M.T.toStressTensorData ψ ≠ 0 := by
  have hlink := M.charge_link ψ hψ k hk
  intro hzero
  rw [hzero, mul_zero] at hlink
  exact hkne hlink

/-- O certificado contém um estado regular com carga integrável e não nula. -/
theorem maxwell_exists_nontrivial_charge {L : LightOneParticle} {C : FockCertificate L}
    (M : MaxwellCertificate C) :
    ∃ ψ : C.F, Regular M.Dom M.T.toStressTensorData ψ ∧
      Integrable (chargeIntegrand M.T.toStressTensorData ψ) ∧
      nullPlaneCharge M.T.toStressTensorData ψ ≠ 0 := by
  obtain ⟨ψ, hψ, k, hk, hkne⟩ := M.nontrivial
  exact ⟨ψ, hψ, maxwell_regular_charge_integrable M ψ hψ,
    maxwell_charge_ne_zero_of_modularEnergy M ψ hψ k hk hkne⟩

/-- A carga Maxwell não nula não pode ocupar o lugar de `τ` na lei dual. -/
theorem maxwell_boosted_charge_not_dual {L : LightOneParticle} {C : FockCertificate L}
    (M : MaxwellCertificate C) (ψ : C.F)
    (hψ : Regular M.Dom M.T.toStressTensorData ψ)
    (k : ℝ) (hk : HasModularEnergy (lightDelta C) ψ k) (hkne : k ≠ 0)
    (hB : Integrable (chargeIntegrand M.T.toStressTensorData ((lightBoost C).V 1 ψ))) :
    nullPlaneCharge M.T.toStressTensorData ((lightBoost C).V 1 ψ) ≠
      Real.exp (-(1 : ℝ)) * nullPlaneCharge M.T.toStressTensorData ψ :=
  nullPlaneCharge_not_dual_scaling (lightBoost C) M.T ψ
    (maxwell_regular_charge_integrable M ψ hψ) hB
    (maxwell_charge_ne_zero_of_modularEnergy M ψ hψ k hk hkne)

end TGLExt.MaxwellNullScalingBridge

#print axioms TGLExt.MaxwellNullScalingBridge.maxwell_regular_charge_integrable
#print axioms TGLExt.MaxwellNullScalingBridge.maxwell_charge_ne_zero_of_modularEnergy
#print axioms TGLExt.MaxwellNullScalingBridge.maxwell_exists_nontrivial_charge
#print axioms TGLExt.MaxwellNullScalingBridge.maxwell_boosted_charge_not_dual
