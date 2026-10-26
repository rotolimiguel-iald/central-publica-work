import AxisCompactMaxwellCertificateR4
import AxisCompactCircularTransportR2
import PointAnnihilationSmearingR4

/-! The compact physical net uses circular smearing. Its stress therefore
uses the already constructed circular unitary on the state as well as on
the field. This explicit transport preserves the original calibrated tensor,
the Fock space, the dense AxisCompact domain, and the boost/modular energy.
The local object is a Wick form on the regular domain, not a bounded point
field. The geometric consumer retains its fixed-null linearized scope. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
noncomputable section

namespace F1Fecho.MaxwellGlobal
open MeasureTheory Set
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.ContratoQGv32
open TGLExt.MaxwellBridge F1Fecho.NetworkReuse F1Fecho.NetworkModularCore
open F1Fecho.OrbitalScreen F1Fecho.Annihilation F1Fecho.FockSegalTransport
open F1Rede.BosonicFock F1Rede.BosonicFockGroupActions

/-- The old tensor evaluated on the explicitly transported state. -/
def circularCalibratedStress {D : CanonicalNetInput} (A : RemainingModularCoreInput D) :
    StressTensorDataLocalV32 (lightNet A.toCertificate) (lightBoost A.toCertificate) where
  T ψ x := (toStress (regularMaxwellCalibratedForm A)).T (gamma circularH1 ψ) x
  T_vac x := by
    change (toStress (regularMaxwellCalibratedForm A)).T (gamma circularH1 vacuum) x = 0
    rw [gamma_vacuum]
    exact (toStress (regularMaxwellCalibratedForm A)).T_vac x
  T_covariant a ψ x := by
    change (toStress (regularMaxwellCalibratedForm A)).T
      (gamma circularH1 (gamma (U1 a) ψ)) x = _
    rw [gamma_circular_U1]
    exact (toStress (regularMaxwellCalibratedForm A)).T_covariant a (gamma circularH1 ψ) x
  symmetric ψ x := (toStress (regularMaxwellCalibratedForm A)).symmetric (gamma circularH1 ψ) x
  test_integrable ψ ν μ f hf hc :=
    (toStress (regularMaxwellCalibratedForm A)).test_integrable (gamma circularH1 ψ) ν μ f hf hc
  conserved ψ ν f hf hc :=
    (toStress (regularMaxwellCalibratedForm A)).conserved (gamma circularH1 ψ) ν f hf hc
  boost_covariant s ψ x := by
    change (toStress (regularMaxwellCalibratedForm A)).T
      (gamma circularH1 (gamma (B0 s) ψ)) x = _
    rw [gamma_circular_B0]
    exact (toStress (regularMaxwellCalibratedForm A)).boost_covariant s (gamma circularH1 ψ) x

theorem circularCalibratedStress_regular_iff {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (ψ : F) :
    Regular (axisCompactFockDomain : Set F) (circularCalibratedStress A).toStressTensorData ψ ↔
      Regular (axisCompactFockDomain : Set F)
        (toStress (regularMaxwellCalibratedForm A)).toStressTensorData (gamma circularH1 ψ) := by
  simp only [Regular, nullEnergy, circularCalibratedStress,
    axisCompactFockDomain_circular, LinearIsometryEquiv.norm_map]

theorem circular_modularEnergy_iff {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (ψ : F) (k : ℝ) :
    HasModularEnergy (lightDelta A.toCertificate) (gamma circularH1 ψ) k ↔
      HasModularEnergy (lightDelta A.toCertificate) ψ k := by
  have he : (fun t : ℝ => inner ℂ (gamma circularH1 ψ)
      (lightDelta A.toCertificate t (gamma circularH1 ψ))) =
      (fun t : ℝ => inner ℂ ψ (lightDelta A.toCertificate t ψ)) := by
    funext t
    change inner ℂ (gamma circularH1 ψ)
      (gamma (B0 (-(2 * Real.pi * t))) (gamma circularH1 ψ)) =
      inner ℂ ψ (gamma (B0 (-(2 * Real.pi * t))) ψ)
    rw [← gamma_circular_B0, LinearIsometryEquiv.inner_map_map]
  unfold HasModularEnergy
  rw [he]

theorem circularCalibratedStress_charge_link {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (N : KillingNormalization) (ψ : F)
    (hψ : Regular (axisCompactFockDomain : Set F)
      (circularCalibratedStress A).toStressTensorData ψ)
    (k : ℝ) (hk : HasModularEnergy (lightDelta A.toCertificate) ψ k) :
    k = 2 * Real.pi * nullPlaneCharge (circularCalibratedStress A).toStressTensorData ψ := by
  exact (axisCompactMaxwellCertificate A N).charge_link (gamma circularH1 ψ)
    ((circularCalibratedStress_regular_iff A ψ).mp hψ) k
    ((circular_modularEnergy_iff A ψ k).mpr hk)

/-- The same normalized nonzero-energy state, pulled back by the inverse unitary. -/
theorem circularCalibratedStress_nontrivial {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (N : KillingNormalization) :
    ∃ ψ : F, Regular (axisCompactFockDomain : Set F)
      (circularCalibratedStress A).toStressTensorData ψ ∧
      ∃ k : ℝ, HasModularEnergy (lightDelta A.toCertificate) ψ k ∧ k ≠ 0 := by
  obtain ⟨χ, hχ, k, hk, hkne⟩ := (axisCompactMaxwellCertificate A N).nontrivial
  let ψ : F := (gamma circularH1).symm χ
  have hback : gamma circularH1 ψ = χ := (gamma circularH1).apply_symm_apply χ
  refine ⟨ψ, (circularCalibratedStress_regular_iff A ψ).mpr ?_, k, ?_, hkne⟩
  · rw [hback]
    exact hχ
  · apply (circular_modularEnergy_iff A ψ k).mp
    rw [hback]
    exact hk

/-- The unchanged Maxwell contract, now for the circular field of the net. -/
def circularMaxwellCertificate {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (N : KillingNormalization) :
    MaxwellCertificate A.toCertificate where
  Dom := (axisCompactFockDomain : Set F)
  Dom_vac := vacuum_mem_axisCompactFockDomain
  Dom_translate := fun a ψ hψ => gamma_U1_mem_axisCompactFockDomain a ψ hψ
  T := circularCalibratedStress A
  charge_link := circularCalibratedStress_charge_link A N
  nontrivial := circularCalibratedStress_nontrivial A N

theorem circularMaxwellCertificate_dense {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (N : KillingNormalization) :
    Dense (circularMaxwellCertificate A N).Dom := axisCompactFockDomain_dense

/-- Transport of the actual four-term local Wick form, before tensor identification. -/
def circularLocalWickStress (ψ χ : regularFockDomain) (μ ν : Fin 4) (x : Spacetime) : ℂ :=
  localWickStress (regularCircular ψ) (regularCircular χ) μ ν x

theorem circularLocalWickStress_eq_certificate {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (N : KillingNormalization)
    (ψ : regularFockDomain) (x : Fin 4 → ℝ) (μ ν : Fin 4) :
    (circularLocalWickStress ψ ψ μ ν (WithLp.toLp 2 x)).re =
      (circularMaxwellCertificate A N).T.T ψ.val x μ ν :=
  localWickStress_eq_calibrated A (regularCircular ψ) x μ ν

/-- Actual circular annihilation, with the same state transported on both sides.
All integrals are Bochner integrals in F; their integrability is provided below. -/
theorem normalizedCircular_annihilation_point_integral
    (f : SchwartzTensor) (ψ : regularFockDomain) :
    gamma circularH1 (annihilation (normalizedCircularSmearCLM f) (regularDomainInput ψ)) =
      (1/2 : ℂ) • ∑ μ : Fin 4, ∑ ν : Fin 4,
        ∫ x, ((starRingEnd ℂ) (f x μ ν) * metricSignC μ * metricSignC ν) •
          (pointAnnihilation μ ν x (regularCircular ψ)).val := by
  have ht := annihilation_gamma circularH1 (normalizedCircularSmearCLM f) (regularDomainInput ψ)
  rw [circularH1_normalizedCircularSmear, domainGamma_regularCircular] at ht
  exact ht.symm.trans (normalizedPhysical_annihilation_point_integral f (regularCircular ψ))

theorem circular_point_integrable (f : SchwartzTensor) (μ ν : Fin 4)
    (ψ : regularFockDomain) :
    Integrable (fun x => ((starRingEnd ℂ) (f x μ ν) * metricSignC μ * metricSignC ν) •
      (pointAnnihilation μ ν x (regularCircular ψ)).val) :=
  pointAnnihilation_test_integrable f μ ν (regularCircular ψ)

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.circularCalibratedStress
#print axioms F1Fecho.MaxwellGlobal.circularCalibratedStress_regular_iff
#print axioms F1Fecho.MaxwellGlobal.circular_modularEnergy_iff
#print axioms F1Fecho.MaxwellGlobal.circularCalibratedStress_charge_link
#print axioms F1Fecho.MaxwellGlobal.circularCalibratedStress_nontrivial
#print axioms F1Fecho.MaxwellGlobal.circularMaxwellCertificate
#print axioms F1Fecho.MaxwellGlobal.circularMaxwellCertificate_dense
#print axioms F1Fecho.MaxwellGlobal.circularLocalWickStress_eq_certificate
#print axioms F1Fecho.MaxwellGlobal.normalizedCircular_annihilation_point_integral
#print axioms F1Fecho.MaxwellGlobal.circular_point_integrable
