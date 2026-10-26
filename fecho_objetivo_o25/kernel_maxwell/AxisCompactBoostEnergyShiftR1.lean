import AxisCompactFockTranslationR2
import Mathlib.Analysis.Complex.RealDeriv
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap

/-! A nonzero boost energy is obtained from the existing compact H1 core.
The actual spatial translation a=(0,1,0,0) has phase exp(-i p1).
Since the existing boost generator is -E*d/dp1, its diagonal imaginary
matrix element increases by the strictly positive energy integral.
No stress positivity or nonzero vector is substituted for nonzero energy.
The Fock normalization and modular transfer are in the following component.
This is a candidate; no build was run by the author. -/
set_option autoImplicit false
set_option maxHeartbeats 2200000
set_option backward.isDefEq.respectTransparency false
noncomputable section

namespace F1Fecho.MaxwellGlobal
open Set Filter MeasureTheory
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open scoped Topology ContDiff

def longitudinalUnitTranslation : Fin 4 → ℝ := ![0, 1, 0, 0]

def longitudinalUnitPhase (y : MomentumCoordinates) : ℂ :=
  orbitalPhase 0 longitudinalUnitTranslation y

theorem longitudinalUnitPhase_eq (y : MomentumCoordinates) :
    longitudinalUnitPhase y = Complex.exp ((-y.2 : ℂ) * Complex.I) := by
  simp [longitudinalUnitPhase, orbitalPhase, ChatgptAudit.WignerOrbit016.phase,
    ChatgptAudit.WignerOrbit016.orbitPairing, longitudinalUnitTranslation, shellMomentum]

theorem longitudinalUnitPhase_contDiff : ContDiff ℝ ∞ longitudinalUnitPhase := by
  simp only [funext longitudinalUnitPhase_eq]
  fun_prop

theorem longitudinalUnitPhase_star_mul (y : MomentumCoordinates) :
    (starRingEnd ℂ) (longitudinalUnitPhase y) * longitudinalUnitPhase y = 1 := by
  rw [← Complex.normSq_eq_conj_mul_self, Complex.normSq_eq_norm_sq]
  simp only [longitudinalUnitPhase, orbitalPhase_norm, one_pow, Complex.ofReal_one]

def longitudinalTranslatedProfile (g : MomentumCoordinates → Fib) : MomentumCoordinates → Fib :=
  fun y => longitudinalUnitPhase y • g y

theorem longitudinalTranslatedProfile_contDiff (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) : ContDiff ℝ ∞ (longitudinalTranslatedProfile g) :=
  longitudinalUnitPhase_contDiff.smul hg

theorem longitudinalTranslatedProfile_compact (g : MomentumCoordinates → Fib)
    (hc : HasCompactSupport g) : HasCompactSupport (longitudinalTranslatedProfile g) := by
  change HasCompactSupport (longitudinalUnitPhase • g)
  exact hc.smul_left

theorem longitudinalTranslatedProfile_ae (h : H1) (g : MomentumCoordinates → Fib)
    (he : (h : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] g) :
    (U1 longitudinalUnitTranslation h : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0]
      longitudinalTranslatedProfile g := by
  filter_upwards [orbitalTranslation_ae (E := Fib) 0 longitudinalUnitTranslation h, he]
    with y ht hy
  exact ht.trans (congrArg (fun v : Fib => longitudinalUnitPhase y • v) hy)

theorem longitudinalUnitPhase_boost_hasDerivAt (y : MomentumCoordinates) :
    HasDerivAt (fun s : ℝ => longitudinalUnitPhase (coordinateBoost 0 (-s) y))
      (longitudinalUnitPhase y * ((shellEnergy y : ℂ) * Complex.I)) 0 := by
  have hl : HasDerivAt (fun s : ℝ => (coordinateBoost 0 (-s) y).2) (-shellEnergy y) 0 := by
    convert (ContinuousLinearMap.snd ℝ Transverse ℝ).hasFDerivAt.comp_hasDerivAt 0
      (coordinateBoost_negative_hasDerivAt_zero y) using 1 <;>
      simp [Function.comp_def, momentumLongitudinalDirection]
  have hp := (hl.neg.ofReal_comp.mul_const Complex.I).cexp
  simpa [longitudinalUnitPhase_eq, coordinateBoost, Function.comp_def] using hp

theorem compactBoostGenerator_longitudinalTranslate
    (g : MomentumCoordinates → Fib) (hg : ContDiff ℝ ∞ g) (y : MomentumCoordinates) :
    compactBoostGenerator (longitudinalTranslatedProfile g) y =
      longitudinalUnitPhase y • compactBoostGenerator g y +
        (longitudinalUnitPhase y * ((shellEnergy y : ℂ) * Complex.I)) • g y := by
  have hp := (longitudinalUnitPhase_boost_hasDerivAt y).smul
    (compactBoost_profile_hasDerivAt_zero g hg y)
  have hzero : coordinateBoost 0 (-(0 : ℝ)) y = y := by
    rcases y with ⟨q, p⟩
    simp [coordinateBoost]
  have hd : HasDerivAt
      (fun s : ℝ => longitudinalTranslatedProfile g (coordinateBoost 0 (-s) y))
      (longitudinalUnitPhase y • compactBoostGenerator g y +
        (longitudinalUnitPhase y * ((shellEnergy y : ℂ) * Complex.I)) • g y) 0 := by
    simpa only [Pi.smul_apply, hzero, longitudinalTranslatedProfile] using hp
  exact (compactBoost_profile_hasDerivAt_zero (longitudinalTranslatedProfile g)
    (longitudinalTranslatedProfile_contDiff g hg) y).unique hd

theorem compactBoost_inner_longitudinalTranslate_point
    (g : MomentumCoordinates → Fib) (hg : ContDiff ℝ ∞ g) (y : MomentumCoordinates) :
    inner ℂ (longitudinalTranslatedProfile g y)
      (compactBoostGenerator (longitudinalTranslatedProfile g) y) =
      inner ℂ (g y) (compactBoostGenerator g y) +
        Complex.I * ((shellEnergy y * ‖g y‖ ^ 2 : ℝ) : ℂ) := by
  rw [compactBoostGenerator_longitudinalTranslate g hg y]
  simp only [longitudinalTranslatedProfile, inner_add_right, inner_smul_left,
    inner_smul_right, inner_self_eq_norm_sq_to_K, Complex.ofReal_mul, Complex.ofReal_pow]
  calc
    _ = ((starRingEnd ℂ) (longitudinalUnitPhase y) * longitudinalUnitPhase y) *
        inner ℂ (g y) (compactBoostGenerator g y) +
        ((starRingEnd ℂ) (longitudinalUnitPhase y) * longitudinalUnitPhase y) *
          (Complex.I * ((shellEnergy y : ℂ) * (‖g y‖ : ℂ) ^ 2)) := by ring
    _ = _ := by rw [longitudinalUnitPhase_star_mul]; ring

theorem compactBoost_pair_eq_profile (h : H1) (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g)
    (he : (h : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] g) :
    oneParticleBoostPair h h =
      ∫ y, inner ℂ (g y) (compactBoostGenerator g y) ∂orbitalMeasure 0 := by
  unfold oneParticleBoostPair
  rw [(compactBoost_mixed_hasDerivAt h h g hg hc he).deriv]
  exact compactBoost_inner_profile h g hg hc he

theorem axisCompact_boostPair_longitudinalTranslate (h : H1) (hh : AxisCompactProfile h) :
    oneParticleBoostPair (U1 longitudinalUnitTranslation h) (U1 longitudinalUnitTranslation h) =
      oneParticleBoostPair h h +
        Complex.I * ((∫ y, shellEnergy y * ‖h y‖ ^ 2 ∂orbitalMeasure 0 : ℝ) : ℂ) := by
  have hs := axisCompactProfile_strongRegular h hh
  obtain ⟨g, he, hc, hg, ε, hε, hgap⟩ := hh
  have hgt := longitudinalTranslatedProfile_contDiff g hg
  have hct := longitudinalTranslatedProfile_compact g hc
  have het := longitudinalTranslatedProfile_ae h g he
  rw [compactBoost_pair_eq_profile _ _ hgt hct het,
    compactBoost_pair_eq_profile h g hg hc he]
  have hE : Integrable (fun y => shellEnergy y * ‖g y‖ ^ 2) (orbitalMeasure 0) := by
    apply (strongRegular_finite_energy h hs).congr
    filter_upwards [he] with y hy
    rw [hy]
  have hEc : Integrable (fun y => Complex.I *
      ((shellEnergy y * ‖g y‖ ^ 2 : ℝ) : ℂ)) (orbitalMeasure 0) :=
    hE.ofReal.const_mul Complex.I
  have hsplit := integral_add (compactBoost_inner_profile_integrable h g hg hc he) hEc
  simp only [Pi.add_apply] at hsplit
  have hEeq : (∫ y, shellEnergy y * ‖g y‖ ^ 2 ∂orbitalMeasure 0) =
      ∫ y, shellEnergy y * ‖h y‖ ^ 2 ∂orbitalMeasure 0 := by
    apply integral_congr_ae
    filter_upwards [he] with y hy
    rw [hy]
  simp_rw [compactBoost_inner_longitudinalTranslate_point g hg]
  rw [hsplit, integral_const_mul, integral_ofReal, hEeq]

theorem axisCompact_boostEnergy_longitudinalTranslate (h : H1) (hh : AxisCompactProfile h) :
    (oneParticleBoostPair (U1 longitudinalUnitTranslation h) (U1 longitudinalUnitTranslation h)).im =
      (oneParticleBoostPair h h).im +
        ∫ y, shellEnergy y * ‖h y‖ ^ 2 ∂orbitalMeasure 0 := by
  rw [axisCompact_boostPair_longitudinalTranslate h hh]
  simp [Complex.mul_im]

theorem strongRegular_energyIntegral_pos (h : H1) (hh : StrongRegularProfile h) (hne : h ≠ 0) :
    0 < ∫ y, shellEnergy y * ‖h y‖ ^ 2 ∂orbitalMeasure 0 := by
  have hnonneg : ∀ y, 0 ≤ shellEnergy y * ‖h y‖ ^ 2 :=
    fun y => mul_nonneg (shellEnergy_nonneg y) (sq_nonneg _)
  have hneI : (∫ y, shellEnergy y * ‖h y‖ ^ 2 ∂orbitalMeasure 0) ≠ 0 := by
    intro hz
    have hae := (integral_eq_zero_iff_of_nonneg hnonneg
      (strongRegular_finite_energy h hh)).mp hz
    apply hne
    apply Lp.eq_zero_iff_ae_eq_zero.mpr
    filter_upwards [hae, transverseProjection_ne_zero_ae] with y hy haxis
    have hyaxis : y.1 ≠ 0 := haxis
    have hp : 0 < shellEnergy y :=
      lt_of_lt_of_le (transverseMass_pos_of_ne_zero 0 y.1 hyaxis) (transverse_le_energy y)
    change shellEnergy y * ‖h y‖ ^ 2 = 0 at hy
    have hs : ‖h y‖ ^ 2 = 0 := (mul_eq_zero.mp hy).resolve_left (ne_of_gt hp)
    exact norm_eq_zero.mp (sq_eq_zero_iff.mp hs)
  exact lt_of_le_of_ne (integral_nonneg hnonneg) (Ne.symm hneI)

/-- One of the two actual translation phases has nonzero boost energy. -/
theorem exists_axisCompact_nonzero_boostPair :
    ∃ h : H1, AxisCompactProfile h ∧ (oneParticleBoostPair h h).im ≠ 0 := by
  obtain ⟨h, hne, hh, hs, _⟩ := exists_nonzero_axisCompact_physical_regular
  by_cases hb : (oneParticleBoostPair h h).im = 0
  · refine ⟨U1 longitudinalUnitTranslation h, axisCompactProfile_U1 _ h hh, ?_⟩
    rw [axisCompact_boostEnergy_longitudinalTranslate h hh, hb, zero_add]
    exact ne_of_gt (strongRegular_energyIntegral_pos h hs hne)
  · exact ⟨h, hh, hb⟩

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.longitudinalUnitPhase_boost_hasDerivAt
#print axioms F1Fecho.MaxwellGlobal.compactBoostGenerator_longitudinalTranslate
#print axioms F1Fecho.MaxwellGlobal.compactBoost_inner_longitudinalTranslate_point
#print axioms F1Fecho.MaxwellGlobal.axisCompact_boostPair_longitudinalTranslate
#print axioms F1Fecho.MaxwellGlobal.axisCompact_boostEnergy_longitudinalTranslate
#print axioms F1Fecho.MaxwellGlobal.strongRegular_energyIntegral_pos
#print axioms F1Fecho.MaxwellGlobal.exists_axisCompact_nonzero_boostPair
