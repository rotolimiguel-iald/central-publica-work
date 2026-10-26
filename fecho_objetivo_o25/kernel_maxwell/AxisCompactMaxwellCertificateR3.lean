import AxisCompactRegularR2
import AxisCompactFockNonzeroEnergyR3

/-! Assembly of the unchanged kernel MaxwellCertificate on the actual
AxisCompact Fock subdomain, retaining the global calibrated stress tensor.
Regular is proved by AxisCompactRegularR2; nonzero energy is independently
constructed by AxisCompactFockNonzeroEnergyR2. Neither is an input assumption.
The explicit RemainingModularCoreInput A remains the unresolved modular-core
input. This source is a candidate consumer, not a build or an R8 acceptance. -/
set_option autoImplicit false
set_option maxHeartbeats 2200000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open F1Fecho.NetworkReuse F1Fecho.NetworkModularCore
open F1Rede.BosonicFock F1Rede.BosonicFockGroupActions

/-- The full Regular predicate and a nonzero modular energy inhabit the SAME domain. -/
theorem axisCompact_calibrated_regular_nontrivial {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (N : KillingNormalization) :
    ∃ ψ : F, Regular (axisCompactFockDomain : Set F)
      (toStress (regularMaxwellCalibratedForm A)).toStressTensorData ψ ∧
      ∃ k : ℝ, HasModularEnergy (lightDelta A.toCertificate) ψ k ∧ k ≠ 0 := by
  obtain ⟨ψ, hψ, hn, k, hk, hkne⟩ :=
    exists_axisCompact_normalized_nonzero_modularEnergy A N
  exact ⟨ψ.val, axisCompact_calibrated_regular A ψ hψ hn, k, hk, hkne⟩

/-- Assemble the existing contract; no field is replaced by a weaker predicate. -/
def axisCompactMaxwellCertificate {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (N : KillingNormalization) :
    MaxwellCertificate A.toCertificate where
  Dom := (axisCompactFockDomain : Set F)
  Dom_vac := vacuum_mem_axisCompactFockDomain
  Dom_translate := fun a ψ hψ => gamma_U1_mem_axisCompactFockDomain a ψ hψ
  T := toStress (regularMaxwellCalibratedForm A)
  charge_link := by
    intro ψ hr k hk
    obtain ⟨hp, hc⟩ := hr.1
    exact axisCompact_calibrated_modular_charge_link A N ⟨ψ, hp⟩ hc k hk
  nontrivial := axisCompact_calibrated_regular_nontrivial A N

@[simp] theorem axisCompactMaxwellCertificate_dom {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (N : KillingNormalization) :
    (axisCompactMaxwellCertificate A N).Dom = (axisCompactFockDomain : Set F) := rfl

@[simp] theorem axisCompactMaxwellCertificate_stress {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (N : KillingNormalization) :
    (axisCompactMaxwellCertificate A N).T = toStress (regularMaxwellCalibratedForm A) := rfl

/-- The certificate's domain retains the already proved density in the same Fock. -/
theorem axisCompactMaxwellCertificate_dense {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (N : KillingNormalization) :
    Dense (axisCompactMaxwellCertificate A N).Dom := axisCompactFockDomain_dense

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.axisCompact_calibrated_regular_nontrivial
#print axioms F1Fecho.MaxwellGlobal.axisCompactMaxwellCertificate
#print axioms F1Fecho.MaxwellGlobal.axisCompactMaxwellCertificate_dom
#print axioms F1Fecho.MaxwellGlobal.axisCompactMaxwellCertificate_stress
#print axioms F1Fecho.MaxwellGlobal.axisCompactMaxwellCertificate_dense
