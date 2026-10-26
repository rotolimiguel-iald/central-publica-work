import CanonicalFockModularCoreInputR1
import CircularMaxwellCertificateR1
import PhysicalFockSpacetimeCovarianceR2

/-! Joint consumer on the existing compact Maxwell net and canonical Fock.
The generic factory keeps D explicit; the physical consumer instantiates it
with physicalCanonicalNet. No trace/PF, nonzero energy, charge identity or
Wick identification is an additional hypothesis. N is still an arbitrary
Killing normalization, and G > 0 is the geometric contract's explicit input.
The stress is the actual regular-domain Wick form, with the circular state
transport required by the net. Point annihilation is an unbounded domain
map; smearing is Bochner integration in F. No bounded point field is claimed.
The H3 result is the existing fixed-null, linearized geometric response,
not the universal nonlinear Einstein contract or a device realization. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
noncomputable section

namespace F1Fecho.MaxwellGlobal
open MeasureTheory Set
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.ContratoQGv32
open F1Fecho.NetworkReuse F1Fecho.NetworkModularCore F1Fecho.MaxwellLocalization
open F1Fecho.OrbitalScreen F1Fecho.Annihilation F1Fecho.Creation
open F1Rede.BosonicFock F1Rede.BosonicFockGroupActions
open F1Fecho.CanonicalFockModularCoreInputR1

/-- The generic factory consumes the constructed modular input. -/
def assembledMaxwellCertificate (D : CanonicalNetInput) (N : KillingNormalization) :
    MaxwellCertificate (modularCoreInput D).toCertificate :=
  circularMaxwellCertificate (modularCoreInput D) N

/-- The already inhabited physical net, not a free net premise. -/
def physicalMaxwellCertificate (N : KillingNormalization) :
    MaxwellCertificate physicalFockCertificate :=
  assembledMaxwellCertificate physicalCanonicalNet N

theorem physicalMaxwell_net (O : Set (Fin 4 → ℝ)) :
    (lightNet physicalFockCertificate).net O = PhysicalFockNet.net O := rfl

theorem physicalMaxwell_domain (N : KillingNormalization) :
    (physicalMaxwellCertificate N).Dom = (axisCompactFockDomain : Set F) := rfl

theorem physicalMaxwell_domain_dense (N : KillingNormalization) :
    Dense (physicalMaxwellCertificate N).Dom := axisCompactFockDomain_dense

/-- The normalized smearing stays in the same local real subspace. -/
theorem normalizedCircularSmear_compact_mem (O : Set Spacetime)
    (f : SchwartzTensor) (hr : IsRealTest f)
    (hc : HasCompactSupport (f : Spacetime → TensorValue))
    (hs : tsupport (f : Spacetime → TensorValue) ⊆ O) :
    normalizedCircularSmearCLM f ∈ compactLocalized O := by
  have hf : circularSmear f ∈ compactLocalized O :=
    (Submodule.le_topologicalClosure _) (Submodule.subset_span ⟨f, hr, hc, hs, rfl⟩)
  exact (compactLocalized O).smul_mem unitaryFourierFieldAmplitude hf

theorem normalizedCircularWeyl_local (O : Set Spacetime)
    (f : SchwartzTensor) (hr : IsRealTest f)
    (hc : HasCompactSupport (f : Spacetime → TensorValue))
    (hs : tsupport (f : Spacetime → TensorValue) ⊆ O) :
    FieldWeyl.W (normalizedCircularSmearCLM f) ∈ PhysicalFockSpacetime.spacetimeNet O :=
  FieldWeyl.W_mem_R _ _ (normalizedCircularSmear_compact_mem O f hr hc hs)

/-- This tensor is defined from the four-term Wick form, not from the certificate. -/
def circularWickTensor (ψ : regularFockDomain) (x : Fin 4 → ℝ) :
    Matrix (Fin 4) (Fin 4) ℝ :=
  fun μ ν => (circularLocalWickStress ψ ψ μ ν (WithLp.toLp 2 x)).re

theorem circularWickTensor_eq_physicalMaxwell (N : KillingNormalization)
    (ψ : regularFockDomain) (x : Fin 4 → ℝ) :
    circularWickTensor ψ x = (physicalMaxwellCertificate N).T.T ψ.val x := by
  funext μ ν
  exact circularLocalWickStress_eq_certificate physicalModularCoreInput N ψ x μ ν

theorem circularWickTensor_symmetric (N : KillingNormalization)
    (ψ : regularFockDomain) (x : Fin 4 → ℝ) :
    (circularWickTensor ψ x).transpose = circularWickTensor ψ x := by
  rw [circularWickTensor_eq_physicalMaxwell N]
  exact (physicalMaxwellCertificate N).T.symmetric ψ.val x

theorem circularWickTensor_test_integrable (N : KillingNormalization)
    (ψ : regularFockDomain) (ν μ : Fin 4) (f : (Fin 4 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (hc : HasCompactSupport f) :
    Integrable (fun x => metricSignV32 μ * circularWickTensor ψ x μ ν * testDerivativeV32 f μ x) := by
  have he : (fun x => metricSignV32 μ * circularWickTensor ψ x μ ν * testDerivativeV32 f μ x) =
      (fun x => metricSignV32 μ * (physicalMaxwellCertificate N).T.T ψ.val x μ ν *
        testDerivativeV32 f μ x) := by
    funext x
    rw [circularWickTensor_eq_physicalMaxwell N]
  rw [he]
  exact (physicalMaxwellCertificate N).T.test_integrable ψ.val ν μ f hf hc

theorem circularWickTensor_conserved (N : KillingNormalization)
    (ψ : regularFockDomain) (ν : Fin 4) (f : (Fin 4 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (hc : HasCompactSupport f) :
    (∑ μ : Fin 4, ∫ x : Fin 4 → ℝ,
      metricSignV32 μ * circularWickTensor ψ x μ ν * testDerivativeV32 f μ x) = 0 := by
  have he : (fun x => circularWickTensor ψ x) =
      (fun x => (physicalMaxwellCertificate N).T.T ψ.val x) :=
    funext (circularWickTensor_eq_physicalMaxwell N ψ)
  simp only [show circularWickTensor ψ =
    (physicalMaxwellCertificate N).T.T ψ.val from he]
  exact (physicalMaxwellCertificate N).T.conserved ψ.val ν f hf hc

/-- One normalized state carries Regular, nonzero modular energy, the actual
charge identity and the Wick tensor identification simultaneously. -/
theorem physicalMaxwell_joint_witness (N : KillingNormalization) :
    ∃ ψ : regularFockDomain, AxisCompactFock ψ ∧
      Regular (physicalMaxwellCertificate N).Dom
        (physicalMaxwellCertificate N).T.toStressTensorData ψ.val ∧ ‖ψ.val‖ = 1 ∧
      ∃ k : ℝ, HasModularEnergy (lightDelta physicalFockCertificate) ψ.val k ∧ k ≠ 0 ∧
        k = 2 * Real.pi * nullPlaneCharge (physicalMaxwellCertificate N).T.toStressTensorData ψ.val ∧
        ∀ x, circularWickTensor ψ x = (physicalMaxwellCertificate N).T.T ψ.val x := by
  obtain ⟨χ, hχ, k, hk, hkne⟩ := (physicalMaxwellCertificate N).nontrivial
  obtain ⟨hp, hc⟩ := hχ.1
  let ψ : regularFockDomain := ⟨χ, hp⟩
  exact ⟨ψ, hc, hχ, hχ.2.2.1, k, hk, hkne,
    (physicalMaxwellCertificate N).charge_link χ hχ k hk,
    circularWickTensor_eq_physicalMaxwell N ψ⟩

/-- Same tensor, same physical net, same modular pair in the geometric consumer. -/
def physicalMaxwellH3 (N : KillingNormalization) (G : ℝ) (hG : 0 < G) :
    ContratoH3v32 (lightNet physicalFockCertificate) (lightRealization physicalFockCertificate)
      N (lightBoost physicalFockCertificate) (physicalMaxwellCertificate N).T :=
  lightH3v32 (physicalMaxwellCertificate N) N G hG

def physicalMaxwellImport (N : KillingNormalization) (G : ℝ) (hG : 0 < G) :
    ContratoImportH3v32 (lightNet physicalFockCertificate) (lightRealization physicalFockCertificate)
      N (lightBoost physicalFockCertificate) (physicalMaxwellCertificate N).T
      (lightH2v32 physicalFockCertificate N) :=
  lightImport (physicalMaxwellCertificate N) N G hG

theorem physicalMaxwellH3_admissible (N : KillingNormalization) (G : ℝ) (hG : 0 < G) :
    (physicalMaxwellH3 N G hG).admissible =
      {ψ | Regular (physicalMaxwellCertificate N).Dom
        (physicalMaxwellCertificate N).T.toStressTensorData ψ} := rfl

/-- The fixed-null source is the same Wick tensor, in the same admissible state. -/
theorem physicalMaxwellH3_raychaudhuri_wick (N : KillingNormalization)
    (G : ℝ) (hG : 0 < G) (ψ : regularFockDomain)
    (hψ : Regular (physicalMaxwellCertificate N).Dom
      (physicalMaxwellCertificate N).T.toStressTensorData ψ.val) (x : Fin 4 → ℝ) :
    HasDerivAt (fun l : ℝ => (physicalMaxwellH3 N G hG).theta ψ.val (x + l • nullDir))
      (-(8 * Real.pi * G) * pairing (circularWickTensor ψ x) nullDir nullDir) 0 := by
  rw [circularWickTensor_eq_physicalMaxwell N]
  exact (physicalMaxwellH3 N G hG).raychaudhuri_einstein ψ.val hψ x

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.assembledMaxwellCertificate
#print axioms F1Fecho.MaxwellGlobal.physicalMaxwellCertificate
#print axioms F1Fecho.MaxwellGlobal.physicalMaxwell_net
#print axioms F1Fecho.MaxwellGlobal.physicalMaxwell_domain
#print axioms F1Fecho.MaxwellGlobal.physicalMaxwell_domain_dense
#print axioms F1Fecho.MaxwellGlobal.normalizedCircularSmear_compact_mem
#print axioms F1Fecho.MaxwellGlobal.normalizedCircularWeyl_local
#print axioms F1Fecho.MaxwellGlobal.circularWickTensor_eq_physicalMaxwell
#print axioms F1Fecho.MaxwellGlobal.circularWickTensor_symmetric
#print axioms F1Fecho.MaxwellGlobal.circularWickTensor_test_integrable
#print axioms F1Fecho.MaxwellGlobal.circularWickTensor_conserved
#print axioms F1Fecho.MaxwellGlobal.physicalMaxwell_joint_witness
#print axioms F1Fecho.MaxwellGlobal.physicalMaxwellH3
#print axioms F1Fecho.MaxwellGlobal.physicalMaxwellImport
#print axioms F1Fecho.MaxwellGlobal.physicalMaxwellH3_admissible
#print axioms F1Fecho.MaxwellGlobal.physicalMaxwellH3_raychaudhuri_wick
