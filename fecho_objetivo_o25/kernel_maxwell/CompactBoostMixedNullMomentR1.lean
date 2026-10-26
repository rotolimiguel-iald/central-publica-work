import CompactBoostNullMomentLinkR5

/-! Mixed one-particle boost matrix elements on the existing axis-compact core.
The right vector is differentiated in the actual H1 norm. The left and right
Schwartz profiles may differ. The Bochner change of variables is the same as
in the diagonal theorem, including its measure, orientation and sign.
No equality with a Fock stress moment is assumed or asserted here. -/
set_option autoImplicit false
set_option maxHeartbeats 2200000
noncomputable section

namespace F1Fecho.MaxwellGlobal
open Set Filter MeasureTheory SchwartzMap
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.NullFrequency
open scoped Topology ContDiff LineDeriv

theorem nullSchwartz_mixed_lineDeriv_integrable
    (f g : 𝓢(NullFourierSpace, ℂ)) :
    Integrable (fun p => inner ℂ (f p) ((∂_{nullFrequencyDirection} g) p)) := by
  apply (L2.integrable_inner (𝕜 := ℂ) (f.toLp 2 volume)
    ((∂_{nullFrequencyDirection} g).toLp 2 volume)).congr
  filter_upwards [f.coeFn_toLp 2 volume,
    (∂_{nullFrequencyDirection} g).coeFn_toLp 2 volume] with p hp hd
  rw [hp, hd]

theorem compactBoost_mixed_profile_integrable (h : H1)
    (g : MomentumCoordinates → Fib) (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g) :
    Integrable (fun y => inner ℂ (h y) (compactBoostGenerator g y)) (orbitalMeasure 0) := by
  apply (L2.integrable_inner (𝕜 := ℂ) h (compactBoostDerivative g hg hc)).congr
  filter_upwards [compactBoostDerivative_ae g hg hc] with y hd
  rw [hd]

theorem compactBoost_mixed_inner_profile (h : H1)
    (g : MomentumCoordinates → Fib) (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g) :
    inner ℂ h (compactBoostDerivative g hg hc) =
      ∫ y, inner ℂ (h y) (compactBoostGenerator g y) ∂orbitalMeasure 0 := by
  rw [L2.inner_def]
  apply integral_congr_ae
  filter_upwards [compactBoostDerivative_ae g hg hc] with y hd
  rw [hd]

theorem compactBoost_mixed_inner_null_integrals (h k : H1)
    (g : MomentumCoordinates → Fib) (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g)
    (he : (k : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] g)
    (D0 : NullSchwartzData h 0) (D1 : NullSchwartzData h 1)
    (E0 : NullSchwartzData k 0) (E1 : NullSchwartzData k 1) :
    inner ℂ h (compactBoostDerivative g hg hc) =
      (∫ p, inner ℂ (D0.profile p) ((∂_{nullFrequencyDirection} E0.profile) p)) +
      (∫ p, inner ℂ (D1.profile p) ((∂_{nullFrequencyDirection} E1.profile) p)) := by
  let F : NullFourierSpace → ℂ := fun p =>
    inner ℂ (D0.profile p) ((∂_{nullFrequencyDirection} E0.profile) p) +
      inner ℂ (D1.profile p) ((∂_{nullFrequencyDirection} E1.profile) p)
  have hF : Integrable F :=
    (nullSchwartz_mixed_lineDeriv_integrable D0.profile E0.profile).add
      (nullSchwartz_mixed_lineDeriv_integrable D1.profile E1.profile)
  have hz : ∀ p, p 0 ≤ 0 → F p = 0 := by
    intro p hp
    simp [F, D0.zero_nonpositive p hp, D1.zero_nonpositive p hp]
  have hpoint : (fun y => inner ℂ (h y) (compactBoostGenerator g y)) =ᵐ[orbitalMeasure 0]
      fun y => shellNullFrequency y • F (nullFourierProfilePoint y) := by
    filter_upwards [transverseProjection_ne_zero_ae, D0.orbital_ae, D1.orbital_ae,
      nullSchwartz_compact_generator_ae k g hg he 0 E0,
      nullSchwartz_compact_generator_ae k g hg he 1 E1] with y haxis h0 h1 hd0 hd1
    have hv (a : Fin 2) : nullScreenCLM y a (h y) = nullProfileAmplitude h a y :=
      nullScreenCLM_apply y a (h y)
    rw [nullScreenCLM_inner y haxis, hv 0, hv 1, hd0, hd1, h0, h1]
    simp only [inner_smul_right_eq_smul, ← smul_add, F]
  have hInt : Integrable (fun y => shellNullFrequency y • F (nullFourierProfilePoint y))
      (orbitalMeasure 0) := (compactBoost_mixed_profile_integrable h g hg hc).congr hpoint
  calc
    _ = ∫ y, shellNullFrequency y • F (nullFourierProfilePoint y) ∂orbitalMeasure 0 := by
      rw [compactBoost_mixed_inner_profile h g hg hc]
      exact integral_congr_ae hpoint
    _ = ∫ q : Transverse, ∫ u in Ioi 0,
        F (nullFourierProfilePoint (nullMomentumCoordinates q u)) :=
      orbital_nullFrequency_bochner_cancel (fun y => F (nullFourierProfilePoint y)) hInt
    _ = ∫ q : Transverse, ∫ u in Ioi 0, F (nullFourierCoordinates q u) := by
      apply integral_congr_ae
      filter_upwards [] with q
      apply integral_congr_ae
      filter_upwards [ae_restrict_mem measurableSet_Ioi] with u hu
      congr 1
      unfold nullFourierProfilePoint
      change nullFourierCoordinates q
        (energy (transverseMass 0 q) (inverseLongitudinal (transverseMass 0 q) u) -
          inverseLongitudinal (transverseMass 0 q) u) = _
      rw [null_inverseLongitudinal (transverseMass 0 q) u hu]
    _ = ∫ p, F p := (nullFourier_integral_positive F hF hz).symm
    _ = _ := integral_add
      (nullSchwartz_mixed_lineDeriv_integrable D0.profile E0.profile)
      (nullSchwartz_mixed_lineDeriv_integrable D1.profile E1.profile)

/-- The derivative of the existing H1 matrix element, not a proposed charge. -/
def oneParticleBoostPair (h k : H1) : ℂ :=
  deriv (fun s : ℝ => inner ℂ h (B0 s k)) 0

theorem compactBoost_mixed_hasDerivAt (h k : H1)
    (g : MomentumCoordinates → Fib) (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g)
    (he : (k : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] g) :
    HasDerivAt (fun s : ℝ => inner ℂ h (B0 s k))
      (inner ℂ h (compactBoostDerivative g hg hc)) 0 := by
  simpa only [inner_zero_left, add_zero] using
    (hasDerivAt_const (0 : ℝ) h).inner ℂ (compactBoost_hasDerivAt k g hg hc he)

theorem axisCompact_mixed_hasDerivAt (h k : H1) (hk : AxisCompactProfile k) :
    HasDerivAt (fun s : ℝ => inner ℂ h (B0 s k)) (oneParticleBoostPair h k) 0 := by
  obtain ⟨g, he, hc, hg, ε, hε, hcut⟩ := hk
  have hd := compactBoost_mixed_hasDerivAt h k g hg hc he
  change HasDerivAt (fun s : ℝ => inner ℂ h (B0 s k))
    (deriv (fun s : ℝ => inner ℂ h (B0 s k)) 0) 0
  rw [hd.deriv]
  exact hd

theorem axisCompact_oneParticleBoostPair_null_integrals (h k : H1)
    (hh : AxisCompactProfile h) (hk : AxisCompactProfile k) :
    oneParticleBoostPair h k =
      (∫ p, inner ℂ ((axisCompactNullData h hh 0).profile p)
        ((∂_{nullFrequencyDirection} (axisCompactNullData k hk 0).profile) p)) +
      (∫ p, inner ℂ ((axisCompactNullData h hh 1).profile p)
        ((∂_{nullFrequencyDirection} (axisCompactNullData k hk 1).profile) p)) := by
  have hkcopy := hk
  obtain ⟨g, he, hc, hg, ε, hε, hcut⟩ := hkcopy
  change deriv (fun s : ℝ => inner ℂ h (B0 s k)) 0 = _
  rw [(compactBoost_mixed_hasDerivAt h k g hg hc he).deriv]
  exact compactBoost_mixed_inner_null_integrals h k g hg hc he
    (axisCompactNullData h hh 0) (axisCompactNullData h hh 1)
    (axisCompactNullData k hk 0) (axisCompactNullData k hk 1)

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.nullSchwartz_mixed_lineDeriv_integrable
#print axioms F1Fecho.MaxwellGlobal.compactBoost_mixed_profile_integrable
#print axioms F1Fecho.MaxwellGlobal.compactBoost_mixed_inner_null_integrals
#print axioms F1Fecho.MaxwellGlobal.compactBoost_mixed_hasDerivAt
#print axioms F1Fecho.MaxwellGlobal.axisCompact_mixed_hasDerivAt
#print axioms F1Fecho.MaxwellGlobal.axisCompact_oneParticleBoostPair_null_integrals
