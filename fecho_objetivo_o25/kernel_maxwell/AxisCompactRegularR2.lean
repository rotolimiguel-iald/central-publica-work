import AxisCompactFockTranslationR2
import CompactFockNullPlaneChargeR1

/-! Full kernel Regular on normalized AxisCompact finite coherent vectors.
The null ray is the restriction of the constructed Schwartz Fourier wave.
All translated planes and all null rays follow from the existing covariance.
No Regular clause, tail bound, or charge equality is added as a hypothesis.
The modular-core input A remains explicit. Candidate; compilation is separate.
R2 fixes only explicit norm rewriting, Fin.cases, private predicate unfolding,
measure inference and the concrete Fock namespace; statements/limits unchanged. -/
set_option autoImplicit false
set_option maxHeartbeats 2200000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory SchwartzMap
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open F1Fecho.NetworkReuse F1Fecho.NetworkModularCore F1Fecho.CoherentKernel
open F1Fecho.WeightedPlancherel F1Rede.BosonicFock F1Rede.BosonicFockGroupActions
open ChatgptAudit.WignerRapidityMeasure016
open scoped FourierTransform

private def RaySchwartz (f : ℝ → ℂ) : Prop := ∃ s : 𝓢(ℝ, ℂ), ∀ u, s u = f u

private theorem ray_zero : RaySchwartz (fun _ => 0) := ⟨0, fun _ => rfl⟩

private theorem ray_add {f g : ℝ → ℂ} (hf : RaySchwartz f) (hg : RaySchwartz g) :
    RaySchwartz (fun u => f u + g u) := by
  obtain ⟨s, hs⟩ := hf
  obtain ⟨t, ht⟩ := hg
  exact ⟨s + t, fun u => by simp only [SchwartzMap.add_apply, hs, ht]⟩

private theorem ray_const_mul {f : ℝ → ℂ} (hf : RaySchwartz f) (c : ℂ) :
    RaySchwartz (fun u => c * f u) := by
  obtain ⟨s, hs⟩ := hf
  exact ⟨c • s, fun u => by simp only [SchwartzMap.smul_apply, smul_eq_mul, hs]⟩

private theorem ray_mul {f g : ℝ → ℂ} (hf : RaySchwartz f) (hg : RaySchwartz g) :
    RaySchwartz (fun u => f u * g u) := by
  obtain ⟨s, hs⟩ := hf
  obtain ⟨t, ht⟩ := hg
  refine ⟨SchwartzMap.pairing (ContinuousLinearMap.mul ℂ ℂ) s t, ?_⟩
  intro u
  change s u * t u = _
  rw [hs, ht]

private theorem ray_conj {f : ℝ → ℂ} (hf : RaySchwartz f) :
    RaySchwartz (fun u => (starRingEnd ℂ) (f u)) := by
  obtain ⟨s, hs⟩ := hf
  refine ⟨s.postcompCLM Complex.conjCLE.toContinuousLinearMap, ?_⟩
  intro u
  change (starRingEnd ℂ) (s u) = _
  rw [hs]

private theorem ray_sum {ι : Type*} (s : Finset ι) (f : ι → ℝ → ℂ)
    (hf : ∀ i ∈ s, RaySchwartz (f i)) : RaySchwartz (fun u => ∑ i ∈ s, f i u) := by
  classical
  revert hf
  induction s using Finset.induction_on with
  | empty =>
    intro _
    simpa using ray_zero
  | @insert a s ha ih =>
    intro hf
    have hh := ray_add (hf a (Finset.mem_insert_self a s))
      (ih (fun i hi => hf i (Finset.mem_insert_of_mem hi)))
    simpa only [Finset.sum_insert ha] using hh

private theorem ray_angular (f : 𝓢(NullFourierSpace, ℂ)) :
    RaySchwartz (fun u => angularForward f (nullContractCoordinateEquiv (u, 0))) := by
  let v : NullFourierSpace := (2 * Real.pi)⁻¹ • nullFrequencyDirection
  have hv0 : v ≠ 0 := by
    intro h
    have hz := congrArg (fun z : NullFourierSpace => z 0) h
    have hp : (2 * Real.pi)⁻¹ ≠ 0 := inv_ne_zero (mul_ne_zero (by norm_num) Real.pi_ne_zero)
    apply hp
    simpa [v, nullFrequencyDirection, nullFourierCoordinates] using hz
  have hv : ‖v‖ ≠ 0 := norm_ne_zero_iff.mpr hv0
  have ht : (fun u : ℝ => u • v).HasTemperateGrowth := by fun_prop
  have hb : ∃ (k : ℕ) (C : ℝ), ∀ u : ℝ, ‖u‖ ≤ C * (1 + ‖u • v‖)^k := by
    refine ⟨1, ‖v‖⁻¹, fun u => ?_⟩
    rw [pow_one]
    calc
      ‖u‖ = ‖v‖⁻¹ * ‖u • v‖ := by
        have hnorm : ‖u • v‖ = ‖u‖ * ‖v‖ := norm_smul u v
        rw [hnorm]
        calc
          ‖u‖ = ‖u‖ * (‖v‖⁻¹ * ‖v‖) := by rw [inv_mul_cancel₀ hv, mul_one]
          _ = ‖v‖⁻¹ * (‖u‖ * ‖v‖) := by ring
      _ ≤ ‖v‖⁻¹ * (1 + ‖u • v‖) :=
        mul_le_mul_of_nonneg_left (by linarith) (inv_nonneg.mpr (norm_nonneg v))
  refine ⟨SchwartzMap.compCLM ℂ ht hb (𝓕 f), fun u => ?_⟩
  change (𝓕 f) (u • v) = (𝓕 f) ((2 * Real.pi)⁻¹ • nullContractCoordinateEquiv (u, 0))
  congr 1
  have hcoord : nullContractCoordinateEquiv (u, 0) = u • nullFrequencyDirection := by
    ext i
    refine Fin.cases ?_ (fun j => ?_) i
    · simp [nullContractCoordinateEquiv_apply, nullFourierCoordinates, nullFrequencyDirection]
    · simp [nullContractCoordinateEquiv_apply, nullFourierCoordinates, nullFrequencyDirection]
  rw [hcoord]
  exact smul_comm u ((2 * Real.pi)⁻¹) nullFrequencyDirection

private theorem ray_coherent (h k : H1) (hh : AxisCompactProfile h) (hk : AxisCompactProfile k) :
    RaySchwartz (fun u => unitaryFourierCoherentNullStress h k (nullContractCoordinateEquiv (u, 0))) := by
  have hs (a : Fin 2) := ray_const_mul
    (ray_add (ray_conj (ray_angular (axisCompactNullData h hh a).profile))
      (ray_angular (axisCompactNullData k hk a).profile)) (Real.sqrt 2 : ℂ)⁻¹
  have ht := ray_const_mul (ray_add (ray_mul (hs 0) (hs 0)) (ray_mul (hs 1) (hs 1)))
    ((unitaryFourierStressScale : ℂ) * Complex.exp (inner ℂ h k))
  simpa only [axisCompact_coherentNullStress h k hh hk, pow_two] using ht

/-- The actual finite coherent null stress, restricted to the contract's null ray. -/
theorem axisCompact_nullStress_ray_schwartz (ψ χ : regularFockDomain)
    (hψ : AxisCompactFock ψ) (hχ : AxisCompactFock χ) :
    ∃ s : 𝓢(ℝ, ℂ), ∀ u,
      s u = unitaryFourierFockNullStress ψ χ (nullContractCoordinateEquiv (u, 0)) := by
  have ht : RaySchwartz (fun u => finiteKernel
      (fun h k : RegularLabel => unitaryFourierCoherentNullStress h.val k.val
        (nullContractCoordinateEquiv (u, 0))) (regularCoefficients ψ) (regularCoefficients χ)) := by
    unfold finiteKernel Finsupp.sum
    apply ray_sum
    intro h hh
    apply ray_sum
    intro k hk
    exact ray_const_mul (ray_coherent h.val k.val (hψ h hh) (hχ k hk))
      ((starRingEnd ℂ) ((regularCoefficients ψ) h) * (regularCoefficients χ) k)
  dsimp only [RaySchwartz] at ht
  simpa only [unitaryFourierFockNullStress_eq_finiteKernel] using ht

/-- Both unweighted and first-moment full-line integrability are proved here. -/
theorem axisCompact_calibrated_nullRay_regular {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (ψ : regularFockDomain) (hψ : AxisCompactFock ψ) :
    Continuous (fun u : ℝ => nullEnergy (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      ψ.val (u • nullDir)) ∧
    Integrable (fun u : ℝ => nullEnergy (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      ψ.val (u • nullDir)) ∧
    Integrable (fun u : ℝ => u * nullEnergy (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      ψ.val (u • nullDir)) := by
  obtain ⟨s, hs⟩ := axisCompact_nullStress_ray_schwartz ψ ψ hψ hψ
  have he (u : ℝ) : nullEnergy (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      ψ.val (u • nullDir) = (s u).re := by
    have ht := calibrated_nullEnergy_contract_coordinates A ψ (u, 0)
    have hz : screenEmbed (0 : Fin 2 → ℝ) = 0 := by
      ext i
      fin_cases i <;> rfl
    rw [hz, add_zero] at ht
    exact ht.trans (congrArg Complex.re (hs u).symm)
  have hp : (fun u : ℝ => (u : ℂ)).HasTemperateGrowth := by fun_prop
  have hi0 : Integrable (SchwartzMap.smulLeftCLM ℂ (fun u : ℝ => (u : ℂ)) s)
      (volume : Measure ℝ) :=
    (SchwartzMap.smulLeftCLM ℂ (fun u : ℝ => (u : ℂ)) s).integrable
  have hi := hi0.re
  have him : Integrable (fun u : ℝ => u * (s u).re) := by
    simpa only [SchwartzMap.smulLeftCLM_apply_apply hp, smul_eq_mul, Complex.mul_re,
      Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero, RCLike.re_eq_complex_re] using hi
  simp only [he]
  exact ⟨Complex.continuous_re.comp s.continuous, s.integrable.re, him⟩

/-- Covariance on the SAME global calibrated tensor, used without a certificate. -/
theorem calibrated_nullEnergy_translate_base {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (ψ : regularFockDomain) (x y : Fin 4 → ℝ) :
    nullEnergy (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularGamma (U1 (-x)) (strongRegularProfile_U1 (-x)) ψ).val y =
    nullEnergy (toStress (regularMaxwellCalibratedForm A)).toStressTensorData ψ.val (x + y) := by
  change nullEnergy (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
    ((lightNet A.toCertificate).U (-x) ψ.val) y = _
  simp only [nullEnergy, (toStress (regularMaxwellCalibratedForm A)).T_covariant]
  congr 2
  abel

/-- All six clauses are exactly TGLExt.ImportedSQ.Regular, including every base point. -/
theorem axisCompact_calibrated_regular {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (ψ : regularFockDomain) (hψ : AxisCompactFock ψ)
    (hn : ‖ψ.val‖ = 1) :
    Regular (axisCompactFockDomain : Set F)
      (toStress (regularMaxwellCalibratedForm A)).toStressTensorData ψ.val := by
  have hc (x : Fin 4 → ℝ) := axisCompact_calibrated_nullRay_regular A
    (regularGamma (U1 (-x)) (strongRegularProfile_U1 (-x)) ψ)
    (axisCompactFock_translate (-x) ψ hψ)
  have hj (x : Fin 4 → ℝ) := axisCompact_calibrated_nullCharge_integrable A
    (regularGamma (U1 (-x)) (strongRegularProfile_U1 (-x)) ψ)
    (axisCompactFock_translate (-x) ψ hψ)
  simp only [calibrated_nullEnergy_translate_base] at hc hj
  exact ⟨(mem_axisCompactFockDomain_iff ψ).mpr hψ, hj, hn,
    fun x => (hc x).1, fun x l => (hc x).2.1.integrableOn,
    fun x l => (hc x).2.2.integrableOn⟩

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.axisCompact_nullStress_ray_schwartz
#print axioms F1Fecho.MaxwellGlobal.axisCompact_calibrated_nullRay_regular
#print axioms F1Fecho.MaxwellGlobal.calibrated_nullEnergy_translate_base
#print axioms F1Fecho.MaxwellGlobal.axisCompact_calibrated_regular
