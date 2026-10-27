import MaxwellScreenReflection

set_option autoImplicit false
set_option maxHeartbeats 2200000

/-! A concrete free-streaming Maxwell witness with nonzero anisotropic pressure. -/
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory Filter Matrix SchwartzMap
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open F1Fecho.MaxwellStress ChatgptAudit.WignerRapidityMeasure016 F1Fecho.NullFrequency
open F1Fecho.WeightedPlancherel F1Fecho.OrbitalScreen

/-- A tensor01 wave with positive 01 moment has nonzero real 10 component. -/
theorem momentumSmear_wave10_ne_zero (f : SchwartzTensor)
    (hf : 0 < (regularWave f 0 1 0).re) :
    realProfileWave (momentumSmearCLM f) 1 0 0 ≠ 0 := by
  let h : H1 := momentumSmearCLM f
  have hp : (lowerProfileWave h 0 1 0).re = -(regularWave f 0 1 0).re := by
    unfold lowerProfileWave
    change (metricSignC 0 * metricSignC 1 * profileWave (momentumSmearCLM f) 0 1 0).re = _
    rw [profileWave_momentumSmear]
    simp [metricSignC]
  have hr : (realProfileWave h 0 1 0).re =
      -Real.sqrt 2 * (regularWave f 0 1 0).re := by
    simp [realProfileWave, realWaveProjection_apply, hp]
  have hn : realProfileWave h 0 1 0 ≠ 0 := by
    intro hz
    have hr0 := congrArg Complex.re hz
    rw [hr] at hr0
    simp only [Complex.zero_re] at hr0
    have hs : 0 < Real.sqrt 2 := Real.sqrt_pos.2 (by norm_num)
    nlinarith
  change realProfileWave h 1 0 0 ≠ 0
  rw [realProfileWave_antisymmetric h 0 1 0]
  exact neg_ne_zero.mpr hn

/-- Explicit Schwartz tensor01 witness with its single-fiber form and positive 01 moment. -/
theorem exists_tensor01_radiation_witness : ∃ f : SchwartzTensor, ∃ b : Spacetime → ℂ,
    (∀ p, f p = b p • tensorUnit01) ∧ 0 < (regularWave f 0 1 0).re := by
  let y : MomentumCoordinates := (![1, 0], 0)
  obtain ⟨b, _, hbc, hbs, hb01, hb1⟩ := exists_contDiff_tsupport_subset
    (x := shellEmbedding y) (n := ⊤) (s := Set.univ) (Filter.univ_mem)
  let v : Spacetime → TensorValue := fun p => (b p : ℂ) • tensorUnit01
  have hvC : HasCompactSupport v := hbc.of_isClosed_subset (isClosed_tsupport _) (by
    apply closure_mono
    intro p hp
    contrapose! hp
    simp only [Function.mem_support] at hp ⊢
    simp [v, hp])
  have hvD : ContDiff ℝ (⊤ : ℕ∞) v := by
    convert hbs.smul (contDiff_const (c := tensorUnit01)) using 1
    funext p
    simp [v]
  let f : SchwartzTensor := hvC.toSchwartzMap hvD
  have hf : ∀ p, f p = (b p : ℂ) • tensorUnit01 := fun _ => rfl
  have he : (fun z => (waveDensity f 0 1 z).re) =
      fun z => b (shellEmbedding z) * transverseMass 0 z.1 ^ 2 := by
    funext z
    rw [waveDensity_tensor01 f (fun p => (b p : ℂ)) hf]
    norm_cast
  have hi : Integrable (fun z => b (shellEmbedding z) * transverseMass 0 z.1 ^ 2)
      (orbitalMeasure 0) := by
    rw [← he]
    exact (waveDensity_integrable f 0 1).re
  have hc : Continuous (fun z : MomentumCoordinates =>
      b (shellEmbedding z) * transverseMass 0 z.1 ^ 2) :=
    (hbs.continuous.comp shellEmbedding_continuous).mul (by unfold transverseMass; fun_prop)
  have hn : 0 ≤ fun z : MomentumCoordinates =>
      b (shellEmbedding z) * transverseMass 0 z.1 ^ 2 := by
    intro z
    exact mul_nonneg (hb01 (mem_range_self (shellEmbedding z))).1 (sq_nonneg _)
  have hneq : b (shellEmbedding y) * transverseMass 0 y.1 ^ 2 ≠ 0 := by
    simp [hb1, y, transverseMass]
  letI := orbitalMeasure_openPos 0
  have hpos := integral_pos_of_integrable_nonneg_nonzero hc hi hn hneq
  refine ⟨f, (fun p => (b p : ℂ)), hf, ?_⟩
  have hr : (∫ y, (waveDensity f 0 1 y).re ∂orbitalMeasure 0) =
      (∫ y, waveDensity f 0 1 y ∂orbitalMeasure 0).re := by
    simpa only [RCLike.re_eq_complex_re] using integral_re (waveDensity_integrable f 0 1)
  rw [regularWave_zero_integral, ← hr]
  simpa only [he] using hpos

/-- Symmetrize first in the transverse screen and then longitudinally. -/
def fullySymmetrizedProfile (h : H1) : H1 :=
  (h + screenReflectionH1 h) + momentumReflectionH1 (h + screenReflectionH1 h)

/-- The explicit tensor01 radiation has strictly positive screen-pressure anisotropy. -/
theorem tensor01_fullySymmetric_pressure_contrast_pos (f : SchwartzTensor) (b : Spacetime → ℂ)
    (hf : ∀ p, f p = b p • tensorUnit01) (hpos : 0 < (regularWave f 0 1 0).re) :
    0 < (realProfileStress (fullySymmetrizedProfile (momentumSmearCLM f)) 2 2 0 -
      realProfileStress (fullySymmetrizedProfile (momentumSmearCLM f)) 1 1 0).re := by
  let h : H1 := momentumSmearCLM f
  let k : H1 := h + screenReflectionH1 h
  change 0 < (realProfileStress (k + momentumReflectionH1 k) 2 2 0 -
    realProfileStress (k + momentumReflectionH1 k) 1 1 0).re
  have hh : RegularProfile h := momentumSmear_regular f
  have hs : ∀ᵐ y ∂orbitalMeasure 0, h y 1 = 0 := momentumSmear_singleFiber f b hf
  have hk : RegularProfile k :=
    regularProfile_add h (screenReflectionH1 h) hh (regularProfile_screenReflection h hh)
  have hsk : ∀ᵐ y ∂orbitalMeasure 0, k y 1 = 0 := screenSymmetric_singleFiber h hs
  rw [realProfileStress_symmetricReflection_contrast k hk hsk]
  have h13 : realProfileWave k 1 3 0 = 0 := by
    change realProfileWave (h + screenReflectionH1 h) 1 3 0 = 0
    rw [realProfileWave_screenSymmetric h hh hs]
    norm_num [screenParitySign, screenParitySignR, Matrix.cons_val_three]
  have h23 : realProfileWave k 2 3 0 = 0 := by
    have hz : realProfileWave h 2 3 0 = 0 := momentumSmear_wave23_zero f b hf
    change realProfileWave (h + screenReflectionH1 h) 2 3 0 = 0
    rw [realProfileWave_screenSymmetric h hh hs, hz]
    norm_num [screenParitySign, screenParitySignR]
  have h10 : realProfileWave k 1 0 0 ≠ 0 := by
    have hn : realProfileWave h 1 0 0 ≠ 0 := momentumSmear_wave10_ne_zero f hpos
    change realProfileWave (h + screenReflectionH1 h) 1 0 0 ≠ 0
    rw [realProfileWave_screenSymmetric h hh hs]
    simpa [screenParitySign, screenParitySignR] using
      mul_ne_zero (show (2 : ℂ) ≠ 0 by norm_num) hn
  have h12 : realProfileWave k 1 2 0 = -realProfileWave k 2 1 0 :=
    realProfileWave_antisymmetric k 2 1 0
  rw [h13, h23, h12]
  rw [show (2 * realProfileWave k 1 0 0) ^ 2 + (2 * realProfileWave k 2 1 0) ^ 2 -
      (2 * -realProfileWave k 2 1 0) ^ 2 - (2 * 0) ^ 2 + (2 * 0) ^ 2 =
      (2 * realProfileWave k 1 0 0) ^ 2 by ring]
  have hn : 2 * realProfileWave k 1 0 0 ≠ 0 := mul_ne_zero (by norm_num) h10
  have hre : (2 * realProfileWave k 1 0 0).re ≠ 0 := by
    intro hr
    apply hn
    apply Complex.ext
    · simpa using hr
    · simp [realProfileWave, realWaveProjection_apply]
  have him : (2 * realProfileWave k 1 0 0).im = 0 := by
    simp [realProfileWave, realWaveProjection_apply]
  rw [pow_two, Complex.mul_re]
  simp only [him, mul_zero, sub_zero]
  exact mul_self_pos.mpr hre

/-- Double symmetrization preserves every regular moment. -/
theorem fullySymmetrizedProfile_regular (h : H1) (hh : RegularProfile h) :
    RegularProfile (fullySymmetrizedProfile h) := by
  have hk : RegularProfile (h + screenReflectionH1 h) :=
    regularProfile_add h (screenReflectionH1 h) hh (regularProfile_screenReflection h hh)
  exact regularProfile_add (h + screenReflectionH1 h)
    (momentumReflectionH1 (h + screenReflectionH1 h)) hk
    (regularProfile_momentumReflection (h + screenReflectionH1 h) hk)

/-- The fully symmetrized radiation stress is conserved. -/
theorem fullySymmetrized_stress_conserved (h : H1) (hh : RegularProfile h)
    (ν : Fin 4) (x : Spacetime) :
    (∑ μ : Fin 4, metricSignC μ *
      deriv (fun t : ℝ => realProfileStress (fullySymmetrizedProfile h) μ ν
        (x + t • spacetimeBasis μ)) 0) = 0 :=
  realProfileStress_conserved (fullySymmetrizedProfile h)
    (fullySymmetrizedProfile_regular h hh) ν x

/-- Nonvacuous existence of the formally anisotropic radiation sector. -/
theorem exists_fullySymmetric_anisotropic_radiation : ∃ h : H1,
    0 < (realProfileStress h 2 2 0 - realProfileStress h 1 1 0).re := by
  obtain ⟨f, b, hf, hpos⟩ := exists_tensor01_radiation_witness
  exact ⟨fullySymmetrizedProfile (momentumSmearCLM f),
    tensor01_fullySymmetric_pressure_contrast_pos f b hf hpos⟩

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.momentumSmear_wave10_ne_zero
#print axioms F1Fecho.MaxwellGlobal.exists_tensor01_radiation_witness
#print axioms F1Fecho.MaxwellGlobal.tensor01_fullySymmetric_pressure_contrast_pos
#print axioms F1Fecho.MaxwellGlobal.fullySymmetrizedProfile_regular
#print axioms F1Fecho.MaxwellGlobal.fullySymmetrized_stress_conserved
#print axioms F1Fecho.MaxwellGlobal.exists_fullySymmetric_anisotropic_radiation
