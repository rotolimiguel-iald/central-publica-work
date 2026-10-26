import AxisCompactBoostEnergyShiftR2
import CompactFockNullPlaneChargeR1

/-! A normalized, nonzero-energy witness in the SAME concrete bosonic Fock.
The preceding phase theorem constructs a compact H1 profile whose actual
boost matrix-element derivative has nonzero imaginary part. Its existing
exponential vector has nonzero boost energy; scalar normalization preserves
the existing AxisCompactFock coefficient predicate and rescales the actual
derivative by a strictly positive factor.

The final modular corollary uses the existing lightH2 with explicit A and N.
No Regular predicate or complete MaxwellCertificate is assumed or supplied.
The other Regular clauses remain a separate construction. No own build. -/
set_option autoImplicit false
set_option maxHeartbeats 2200000
noncomputable section

namespace F1Fecho.MaxwellGlobal
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open F1Rede.BosonicFock F1Rede.BosonicFockGroupActions F1Fecho.Exponential
open F1Fecho.NetworkReuse F1Fecho.NetworkModularCore

theorem coherentBoostPair_diagonal_im (h : H1) :
    (coherentBoostPair h h).im =
      Real.exp (‖h‖ ^ 2) * (oneParticleBoostPair h h).im := by
  have he : inner ℂ h h = ((‖h‖ ^ 2 : ℝ) : ℂ) := by
    simpa only [Complex.ofReal_pow] using inner_self_eq_norm_sq_to_K (𝕜 := ℂ) h
  rw [coherentBoostPair, he, ← Complex.ofReal_exp]
  simp [Complex.mul_im]

theorem exponential_ne_zero_of_norm (h : H1) : exponential h ≠ 0 := by
  intro hz
  have hn := exponential_norm_sq h
  rw [hz, norm_zero, zero_pow (by norm_num : (2 : ℕ) ≠ 0)] at hn
  exact (ne_of_gt (Real.exp_pos (‖h‖ ^ 2))) hn.symm

/-- This scales an actual derivative, not a proposed charge formula. -/
theorem fock_hasBoostEnergy_smul (ψ : F) (b : ℝ)
    (hb : HasBoostEnergy VF ψ b) (z : ℂ) :
    HasBoostEnergy VF (z • ψ) (Complex.normSq z * b) := by
  unfold HasBoostEnergy at hb ⊢
  have he : (fun s : ℝ => inner ℂ (z • ψ) (VF s (z • ψ))) =
      fun s : ℝ => (Complex.normSq z : ℂ) * inner ℂ ψ (VF s ψ) := by
    funext s
    rw [map_smul, inner_smul_left, inner_smul_right, ← mul_assoc,
      ← Complex.normSq_eq_conj_mul_self]
  rw [he]
  convert hb.const_mul (Complex.normSq z : ℂ) using 1
  push_cast
  ring

theorem axisCompact_normalize_nonzero_boostEnergy (ψ : regularFockDomain)
    (hψ : AxisCompactFock ψ) (hne : ψ.val ≠ 0) (b : ℝ)
    (hb : HasBoostEnergy VF ψ.val b) (hbne : b ≠ 0) :
    ∃ χ : regularFockDomain, AxisCompactFock χ ∧ ‖χ.val‖ = 1 ∧
      ∃ c : ℝ, HasBoostEnergy VF χ.val c ∧ c ≠ 0 := by
  let z : ℂ := ((‖ψ.val‖⁻¹ : ℝ) : ℂ)
  have hn : ‖ψ.val‖ ≠ 0 := norm_ne_zero_iff.mpr hne
  have hz : z ≠ 0 := by
    dsimp [z]
    exact_mod_cast inv_ne_zero hn
  have hzn : ‖z‖ = ‖ψ.val‖⁻¹ := by
    simp only [z, Complex.norm_real, Real.norm_eq_abs,
      abs_of_nonneg (inv_nonneg.mpr (norm_nonneg ψ.val))]
  refine ⟨z • ψ, axisCompactFock_smul z ψ hψ, ?_,
    Complex.normSq z * b, fock_hasBoostEnergy_smul ψ.val b hb z, ?_⟩
  · change ‖z • ψ.val‖ = 1
    rw [norm_smul, hzn, inv_mul_cancel₀ hn]
  · apply mul_ne_zero _ hbne
    rw [Complex.normSq_eq_norm_sq]
    exact pow_ne_zero 2 (norm_ne_zero_iff.mpr hz)

/-- Unconditional witness: the H1 seed, its nonzero energy, and its Fock
normalization are all constructed. No non-vacuity premise is added. -/
theorem exists_axisCompact_normalized_nonzero_boostEnergy :
    ∃ ψ : regularFockDomain, AxisCompactFock ψ ∧ ‖ψ.val‖ = 1 ∧
      ∃ b : ℝ, HasBoostEnergy VF ψ.val b ∧ b ≠ 0 := by
  obtain ⟨h, hh, hb⟩ := exists_axisCompact_nonzero_boostPair
  let label : RegularLabel := ⟨h, axisCompactProfile_strongRegular h hh⟩
  let ψ : regularFockDomain := regularExponential label
  have hψ : AxisCompactFock ψ := axisCompactFock_exponential label hh
  have hne : ψ.val ≠ 0 := exponential_ne_zero_of_norm h
  have hbne : (regularFockBoostPair ψ ψ).im ≠ 0 := by
    change (regularFockBoostPair (regularExponential label) (regularExponential label)).im ≠ 0
    rw [regularFockBoostPair_exponential, coherentBoostPair_diagonal_im]
    exact mul_ne_zero (ne_of_gt (Real.exp_pos _)) hb
  exact axisCompact_normalize_nonzero_boostEnergy ψ hψ hne _
    (axisCompact_regularFock_hasBoostEnergy ψ hψ) hbne

theorem exists_axisCompact_normalized_nonzero_modularEnergy
    {D : CanonicalNetInput} (A : RemainingModularCoreInput D) (N : KillingNormalization) :
    ∃ ψ : regularFockDomain, AxisCompactFock ψ ∧ ‖ψ.val‖ = 1 ∧
      ∃ k : ℝ, HasModularEnergy (lightDelta A.toCertificate) ψ.val k ∧ k ≠ 0 := by
  obtain ⟨ψ, hψ, hn, b, hb, hbne⟩ := exists_axisCompact_normalized_nonzero_boostEnergy
  refine ⟨ψ, hψ, hn, 2 * Real.pi * b, ?_, ?_⟩
  · apply ContratoH2.modularEnergy_of_boostEnergy (lightH2 A.toCertificate N)
    change HasBoostEnergy VF ψ.val b
    exact hb
  · exact mul_ne_zero (mul_ne_zero (by norm_num) (ne_of_gt Real.pi_pos)) hbne

/-- The same normalized witness also has nonzero charge of the actual calibrated
tensor, by the already constructed charge identity. Full Regular is separate. -/
theorem exists_axisCompact_normalized_nonzero_nullPlaneCharge
    {D : CanonicalNetInput} (A : RemainingModularCoreInput D) (N : KillingNormalization) :
    ∃ ψ : regularFockDomain, AxisCompactFock ψ ∧ ‖ψ.val‖ = 1 ∧
      nullPlaneCharge (toStress (regularMaxwellCalibratedForm A)).toStressTensorData ψ.val ≠ 0 := by
  obtain ⟨ψ, hψ, hn, k, hk, hkne⟩ := exists_axisCompact_normalized_nonzero_modularEnergy A N
  refine ⟨ψ, hψ, hn, ?_⟩
  intro hz
  have he := axisCompact_calibrated_modular_charge_link A N ψ hψ k hk
  rw [hz, mul_zero] at he
  exact hkne he

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.coherentBoostPair_diagonal_im
#print axioms F1Fecho.MaxwellGlobal.exponential_ne_zero_of_norm
#print axioms F1Fecho.MaxwellGlobal.fock_hasBoostEnergy_smul
#print axioms F1Fecho.MaxwellGlobal.axisCompact_normalize_nonzero_boostEnergy
#print axioms F1Fecho.MaxwellGlobal.exists_axisCompact_normalized_nonzero_boostEnergy
#print axioms F1Fecho.MaxwellGlobal.exists_axisCompact_normalized_nonzero_modularEnergy
#print axioms F1Fecho.MaxwellGlobal.exists_axisCompact_normalized_nonzero_nullPlaneCharge
