import OppositeNullSwap

set_option autoImplicit false
set_option maxHeartbeats 2200000

/-! One coherent AxisCompact witness with both null momenta strictly positive. -/
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory SchwartzMap
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open TGLExt.NullEnergyScaling TGLExt.NullMomentumInvariant
open F1Fecho.MaxwellStress ChatgptAudit.WignerRapidityMeasure016 F1Fecho.NullFrequency
open F1Fecho.WeightedPlancherel F1Fecho.OrbitalScreen
open F1Fecho.NetworkReuse F1Fecho.NetworkModularCore F1Fecho.CoherentKernel
open F1Rede.BosonicFock F1Rede.BosonicFockGroupActions
open scoped ContDiff

/-- Axis-compact smooth profiles are closed under addition. -/
theorem axisCompactProfile_add (h k : H1) (hh : AxisCompactProfile h)
    (hk : AxisCompactProfile k) : AxisCompactProfile (h + k) := by
  obtain ⟨g, he, hc, hg, ε, hε, hgap⟩ := hh
  obtain ⟨l, he', hc', hg', ε', hε', hgap'⟩ := hk
  refine ⟨fun y => g y + l y, ?_, hc.add hc', hg.add hg', min ε ε', lt_min hε hε', ?_⟩
  · filter_upwards [Lp.coeFn_add h k, he, he'] with y ha hy hy'
    change (h + k) y = g y + l y
    rw [ha]
    simp only [Pi.add_apply]
    rw [hy, hy']
  · intro y hy
    simp [hgap y (le_trans hy (min_le_left _ _)),
      hgap' y (le_trans hy (min_le_right _ _))]

/-- Linearity of the lower Maxwell wave on regular profiles. -/
theorem lowerProfileWave_add (h k : H1) (hh : RegularProfile h) (hk : RegularProfile k)
    (μ ν : Fin 4) (x : Spacetime) :
    lowerProfileWave (h + k) μ ν x = lowerProfileWave h μ ν x + lowerProfileWave k μ ν x := by
  rw [lowerProfileWave_integral, lowerProfileWave_integral, lowerProfileWave_integral,
    ← integral_add (lowerProfileWaveIntegrand_integrable h hh μ ν x)
      (lowerProfileWaveIntegrand_integrable k hk μ ν x)]
  apply integral_congr_ae
  filter_upwards [Lp.coeFn_add h k] with y hy
  simp only [lowerProfileDensity, profileDensity]
  rw [hy]
  simp only [Fin.sum_univ_two, Pi.add_apply, PiLp.add_apply]
  ring

/-- Linearity of the real Maxwell wave on regular profiles. -/
theorem realProfileWave_add (h k : H1) (hh : RegularProfile h) (hk : RegularProfile k)
    (μ ν : Fin 4) (x : Spacetime) :
    realProfileWave (h + k) μ ν x = realProfileWave h μ ν x + realProfileWave k μ ν x := by
  unfold realProfileWave
  rw [lowerProfileWave_add h k hh hk, map_add]

/-- Zero direct density forces both direct real contracted waves to vanish. -/
theorem axisCompact_realNullWave_zero_of_stress_zero (h : H1) (hh : AxisCompactProfile h)
    (a : Fin 2) (x : NullFourierSpace) (hz : realNullStress h x = 0) :
    realProfileWave h 0 (nullScreenIndex a) (nullPlanePoint (x 0) (nullFourierScreen x)) +
      realProfileWave h 1 (nullScreenIndex a) (nullPlanePoint (x 0) (nullFourierScreen x)) = 0 := by
  have hs := axisCompact_realNullStress h hh x
  rw [hz] at hs
  have hr0 : (angularForward (axisCompactNullData h hh 0).profile x).re = 0 := by
    have h0 := sq_nonneg (angularForward (axisCompactNullData h hh 0).profile x).re
    have h1 := sq_nonneg (angularForward (axisCompactNullData h hh 1).profile x).re
    nlinarith
  have hr1 : (angularForward (axisCompactNullData h hh 1).profile x).re = 0 := by
    have h0 := sq_nonneg (angularForward (axisCompactNullData h hh 0).profile x).re
    have h1 := sq_nonneg (angularForward (axisCompactNullData h hh 1).profile x).re
    nlinarith
  have hr (b : Fin 2) : (angularForward (axisCompactNullData h hh b).profile x).re = 0 := by
    fin_cases b
    · exact hr0
    · exact hr1
  rw [axisCompact_realNullWave h hh a, hr a]
  simp

/-- Adding a profile of zero direct density does not change the direct density. -/
theorem realNullStress_add_of_right_zero (h k : H1) (hh : AxisCompactProfile h)
    (hk : AxisCompactProfile k) (x : NullFourierSpace) (hz : realNullStress k x = 0) :
    realNullStress (h + k) x = realNullStress h x := by
  let X := nullPlanePoint (x 0) (nullFourierScreen x)
  have hk0 := axisCompact_realNullWave_zero_of_stress_zero k hk 0 x hz
  have hk1 := axisCompact_realNullWave_zero_of_stress_zero k hk 1 x hz
  change realProfileWave k 0 2 X + realProfileWave k 1 2 X = 0 at hk0
  change realProfileWave k 0 3 X + realProfileWave k 1 3 X = 0 at hk1
  unfold realNullStress realProfileStress
  rw [stress_null_contraction _ (fun μ ν => realProfileWave_antisymmetric (h + k) μ ν X),
    stress_null_contraction _ (fun μ ν => realProfileWave_antisymmetric h μ ν X)]
  change ((realProfileWave (h + k) 0 2 X + realProfileWave (h + k) 1 2 X)^2 +
    (realProfileWave (h + k) 0 3 X + realProfileWave (h + k) 1 3 X)^2).re = _
  simp_rw [realProfileWave_add h k (axisCompactProfile_strongRegular h hh).1
    (axisCompactProfile_strongRegular k hk).1]
  have ha : (realProfileWave h 0 2 X + realProfileWave k 0 2 X) +
      (realProfileWave h 1 2 X + realProfileWave k 1 2 X) =
      realProfileWave h 0 2 X + realProfileWave h 1 2 X := by
    linear_combination hk0
  have hb : (realProfileWave h 0 3 X + realProfileWave k 0 3 X) +
      (realProfileWave h 1 3 X + realProfileWave k 1 3 X) =
      realProfileWave h 0 3 X + realProfileWave h 1 3 X := by
    linear_combination hk1
  rw [ha, hb]

/-- The symmetric combination of a profile and its opposite lift. -/
def symmetricLift (h : H1) : H1 := h + oppositeLift h

theorem axisCompactProfile_symmetricLift (h : H1) (hh : AxisCompactProfile h) :
    AxisCompactProfile (symmetricLift h) :=
  axisCompactProfile_add h (oppositeLift h) hh (axisCompactProfile_oppositeLift h hh)

theorem oppositeLift_symmetricLift (h : H1) : oppositeLift (symmetricLift h) = symmetricLift h := by
  calc
    oppositeLift (symmetricLift h) = oppositeLift h + oppositeLift (oppositeLift h) := by
      simp only [symmetricLift, oppositeLift, map_add]
    _ = h + oppositeLift h := by
      rw [oppositeLift_involutive]
      exact add_comm _ _

/-- Positive direct momentum is equivalent to positivity of the unnormalized real integral. -/
theorem calibrated_nullPlaneMomentum_pos_iff {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (h : RegularLabel) (hh : AxisCompactProfile h.val) :
    0 < nullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential h).val ↔ 0 < ∫ x : NullFourierSpace, realNullStress h.val x := by
  rw [calibrated_nullPlaneMomentum_exponential_eq A h hh, integral_const_mul]
  have hc : 0 < unitaryFourierStressScale * Real.exp (‖h.val‖ ^ 2) :=
    mul_pos unitaryFourierStressScale_pos (Real.exp_pos _)
  exact mul_pos_iff_of_pos_left hc

/-- Opposite null momentum is always nonnegative on coherent AxisCompact labels. -/
theorem calibrated_oppositeNullPlaneMomentum_nonneg {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (h : RegularLabel) (hh : AxisCompactProfile h.val) :
    0 ≤ oppositeNullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential h).val := by
  rw [calibrated_oppositeNullPlaneMomentum_exponential_eq A h hh]
  exact integral_nonneg (fun x => unitaryFourierRealOppositeStress_nonneg h.val
    (oppositeNullPlanePoint (x 0) (nullFourierScreen x)))

/-- A direct positive label yields one label positive in both null sectors. -/
theorem calibrated_simultaneous_pos_of_direct_pos {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (h : RegularLabel) (hh : AxisCompactProfile h.val)
    (hp : 0 < nullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential h).val) :
    ∃ k : RegularLabel, AxisCompactProfile k.val ∧
      0 < nullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
        (regularExponential k).val ∧
      0 < oppositeNullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
        (regularExponential k).val := by
  let k : RegularLabel := oppositeLiftLabel h hh
  have hk : AxisCompactProfile k.val := axisCompactProfile_oppositeLiftLabel h hh
  have hm := calibrated_oppositeNullPlaneMomentum_nonneg A h hh
  by_cases hpos : 0 < oppositeNullPlaneMomentum
      (toStress (regularMaxwellCalibratedForm A)).toStressTensorData (regularExponential h).val
  · exact ⟨h, hh, hp, hpos⟩
  · have hz : oppositeNullPlaneMomentum
        (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
        (regularExponential h).val = 0 := le_antisymm (le_of_not_gt hpos) hm
    let s : RegularLabel := ⟨h.val + k.val,
      axisCompactProfile_strongRegular _ (axisCompactProfile_add h.val k.val hh hk)⟩
    have hs : AxisCompactProfile s.val := axisCompactProfile_add h.val k.val hh hk
    have hkd : nullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
        (regularExponential k).val = 0 := by
      rw [← calibrated_oppositeNullPlaneMomentum_eq_direct A h hh]
      exact hz
    have hkint : (∫ x : NullFourierSpace, realNullStress k.val x) = 0 := by
      rw [calibrated_nullPlaneMomentum_exponential_eq A k hk, integral_const_mul] at hkd
      exact (mul_eq_zero.mp hkd).resolve_left
        (mul_ne_zero (ne_of_gt unitaryFourierStressScale_pos) (ne_of_gt (Real.exp_pos _)))
    have hki : Integrable (realNullStress k.val) := by
      have hi := axisCompact_realOppositeStress3D_integrable h.val hh
      apply hi.congr
      filter_upwards [] with x
      exact axisCompact_realOppositeStress3D_eq_direct h.val hh x
    have hkae : realNullStress k.val =ᵐ[volume] 0 :=
      (integral_eq_zero_iff_of_nonneg (axisCompact_realNullStress_nonneg k.val hk) hki).mp hkint
    have hplus : 0 < nullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
        (regularExponential s).val := by
      rw [calibrated_nullPlaneMomentum_exponential_eq A s hs, integral_const_mul]
      apply mul_pos (mul_pos unitaryFourierStressScale_pos (Real.exp_pos _))
      have hae : realNullStress s.val =ᵐ[volume] realNullStress h.val := by
        filter_upwards [hkae] with x hx
        exact realNullStress_add_of_right_zero h.val k.val hh hk x hx
      rw [integral_congr_ae hae]
      exact (calibrated_nullPlaneMomentum_pos_iff A h hh).mp hp
    have hminus : 0 < oppositeNullPlaneMomentum
        (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
        (regularExponential s).val := by
      rw [calibrated_oppositeNullPlaneMomentum_eq_direct A s hs]
      have hsi : oppositeLiftLabel s hs = s := by
        apply Subtype.ext
        exact oppositeLift_symmetricLift h.val
      rw [hsi]
      exact hplus
    exact ⟨s, hs, hplus, hminus⟩

/-- Concrete coherent AxisCompact witness with both null momenta strictly positive. -/
theorem exists_axisCompact_bothNullMomenta_pos {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) :
    ∃ h : RegularLabel, AxisCompactProfile h.val ∧
      0 < nullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
        (regularExponential h).val ∧
      0 < oppositeNullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
        (regularExponential h).val := by
  obtain ⟨h, hh, hm⟩ := exists_axisCompact_oppositeNullPlaneMomentum_pos A
  let k : RegularLabel := oppositeLiftLabel h hh
  have hk : AxisCompactProfile k.val := axisCompactProfile_oppositeLiftLabel h hh
  have hp : 0 < nullPlaneMomentum (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
      (regularExponential k).val := by
    rw [← calibrated_oppositeNullPlaneMomentum_eq_direct A h hh]
    exact hm
  exact calibrated_simultaneous_pos_of_direct_pos A k hk hp

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.axisCompactProfile_add
#print axioms F1Fecho.MaxwellGlobal.lowerProfileWave_add
#print axioms F1Fecho.MaxwellGlobal.realProfileWave_add
#print axioms F1Fecho.MaxwellGlobal.axisCompact_realNullWave_zero_of_stress_zero
#print axioms F1Fecho.MaxwellGlobal.realNullStress_add_of_right_zero
#print axioms F1Fecho.MaxwellGlobal.axisCompactProfile_symmetricLift
#print axioms F1Fecho.MaxwellGlobal.oppositeLift_symmetricLift
#print axioms F1Fecho.MaxwellGlobal.calibrated_nullPlaneMomentum_pos_iff
#print axioms F1Fecho.MaxwellGlobal.calibrated_oppositeNullPlaneMomentum_nonneg
#print axioms F1Fecho.MaxwellGlobal.calibrated_simultaneous_pos_of_direct_pos
#print axioms F1Fecho.MaxwellGlobal.exists_axisCompact_bothNullMomenta_pos
