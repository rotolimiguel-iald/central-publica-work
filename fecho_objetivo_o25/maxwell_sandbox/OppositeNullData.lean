import OppositeNullAngularWave
import AxisCompactCircularTransportR2

set_option autoImplicit false
set_option maxHeartbeats 2200000

/-! Construct opposite-null Schwartz data by longitudinal reflection and fiber sign. -/
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory SchwartzMap
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open F1Fecho.MaxwellStress ChatgptAudit.WignerRapidityMeasure016 F1Fecho.NullFrequency
open F1Fecho.WeightedPlancherel F1Fecho.OrbitalScreen
open scoped ContDiff

/-- The involutive unitary `(-1) ⊕ 1` on the helicity fiber. -/
def oppositeFiberSign : Fiber ≃ₗᵢ[ℂ] Fiber :=
  LinearIsometryEquiv.piLpCongrRight 2 (fun j : Fin 2 =>
    if j = 0 then LinearIsometryEquiv.neg ℂ else LinearIsometryEquiv.refl ℂ ℂ)

@[simp] theorem oppositeFiberSign_apply (v : Fiber) (j : Fin 2) :
    oppositeFiberSign v j = if j = 0 then -v j else v j := by
  fin_cases j <;> simp [oppositeFiberSign, LinearIsometryEquiv.piLpCongrRight_apply]

/-- Pullback by longitudinal reflection on the one-particle space. -/
def momentumReflectionH1 : H1 →ₗᵢ[ℂ] H1 :=
  Lp.compMeasurePreservingₗᵢ ℂ longitudinalReflectionEquiv
    longitudinalReflection_measurePreserving

/-- Longitudinal reflection preserves smooth compact profiles away from the axis. -/
theorem axisCompactProfile_momentumReflection (h : H1) (hh : AxisCompactProfile h) :
    AxisCompactProfile (momentumReflectionH1 h) := by
  obtain ⟨g, he, hc, hg, ε, hε, hgap⟩ := hh
  let g' : MomentumCoordinates → Fiber := fun y => g (longitudinalReflection y)
  let e : MomentumCoordinates ≃L[ℝ] MomentumCoordinates :=
    (ContinuousLinearEquiv.refl ℝ Transverse).prodCongr (ContinuousLinearEquiv.neg ℝ)
  have he' : (momentumReflectionH1 h : MomentumCoordinates → Fiber) =ᵐ[orbitalMeasure 0] g' := by
    filter_upwards [Lp.coeFn_compMeasurePreserving h longitudinalReflection_measurePreserving,
      longitudinalReflection_measurePreserving.quasiMeasurePreserving.ae he] with y hy hy'
    change (Lp.compMeasurePreserving longitudinalReflectionEquiv
      longitudinalReflection_measurePreserving h) y = g (longitudinalReflection y)
    exact hy.trans hy'
  have hc' : HasCompactSupport g' := by
    have ht := hc.comp_homeomorph e.toHomeomorph
    simpa [g', e, Function.comp_def, longitudinalReflection] using ht
  have hg' : ContDiff ℝ ∞ g' := by
    exact hg.comp (contDiff_fst.prodMk contDiff_snd.neg)
  have hgap' : ∀ y : MomentumCoordinates, ‖transverseProjection y‖ ≤ ε → g' y = 0 := by
    intro y hy
    change g (longitudinalReflection y) = 0
    apply hgap (longitudinalReflection y)
    simpa [transverseProjection, longitudinalReflection] using hy
  exact ⟨g', he', hc', hg', ε, hε, hgap'⟩

/-- Reflection in momentum followed by the opposite-polarization fiber sign. -/
def oppositeLift (h : H1) : H1 := fiberLift oppositeFiberSign (momentumReflectionH1 h)

theorem axisCompactProfile_oppositeLift (h : H1) (hh : AxisCompactProfile h) :
    AxisCompactProfile (oppositeLift h) :=
  axisCompactProfile_fiberLift oppositeFiberSign _
    (axisCompactProfile_momentumReflection h hh)

@[simp] theorem nullPolarization_longitudinalReflection (y : MomentumCoordinates) :
    nullPolarization (longitudinalReflection y) = nullPolarization y := rfl

/-- The transformed direct amplitude is the opposite amplitude at the reflected point. -/
theorem nullAmplitude_oppositeLift_ae (h : H1) (a : Fin 2) :
    (fun y => nullProfileAmplitude (oppositeLift h) a y) =ᵐ[orbitalMeasure 0]
      (fun y => oppositeNullProfileAmplitude h a (longitudinalReflection y)) := by
  have hlift : (oppositeLift h : MomentumCoordinates → Fiber) =ᵐ[orbitalMeasure 0]
      (fun y => oppositeFiberSign (h (longitudinalReflection y))) := by
    filter_upwards [fiberLiftMap_ae oppositeFiberSign (momentumReflectionH1 h),
      Lp.coeFn_compMeasurePreserving h longitudinalReflection_measurePreserving] with y hy hy'
    change fiberLiftMap oppositeFiberSign (momentumReflectionH1 h) y =
      oppositeFiberSign (h (longitudinalReflection y))
    rw [hy]
    exact congrArg oppositeFiberSign hy'
  filter_upwards [hlift] with y hy
  simp only [nullProfileAmplitude, oppositeNullProfileAmplitude]
  rw [hy]
  apply Finset.sum_congr rfl
  intro j _
  simp only [oppositeFiberSign_apply, nullPolarization_longitudinalReflection]
  by_cases hj : j = 0 <;> simp [hj]

/-- Direct Fourier coordinates at the reflected point are opposite Fourier coordinates. -/
theorem nullFourierProfilePoint_longitudinalReflection (y : MomentumCoordinates) :
    nullFourierProfilePoint (longitudinalReflection y) = oppositeFourierProfilePoint y := by
  simp [nullFourierProfilePoint, oppositeFourierProfilePoint, shellNullFrequency,
    shellOppositeFrequency, shellEnergy, energy, longitudinalReflection, transverseMass]

/-- Objective construction of opposite Schwartz data on every axis-compact profile. -/
def axisCompactOppositeData (h : H1) (hh : AxisCompactProfile h) (a : Fin 2) :
    OppositeNullSchwartzData h a :=
  let h' := oppositeLift h
  let hh' := axisCompactProfile_oppositeLift h hh
  let D := axisCompactNullData h' hh' a
  have ha := nullAmplitude_oppositeLift_ae h a
  have hn : ∀ᵐ q : Transverse, ∀ᵐ u ∂volume.restrict (Ioi 0),
      oppositeNullProfileAmplitude h a (oppositeMomentumCoordinates q u) =
        D.profile (nullFourierCoordinates q u) := by
    have ha' := orbital_ae_nullMomentum
      (fun y => nullProfileAmplitude h' a y =
        oppositeNullProfileAmplitude h a (longitudinalReflection y)) ha
    filter_upwards [D.null_ae, ha'] with q hq hq'
    filter_upwards [hq, hq'] with u hu hu'
    change oppositeNullProfileAmplitude h a
      (longitudinalReflection (nullMomentumCoordinates q u)) = _
    exact hu'.symm.trans hu
  have ho : (fun y => oppositeNullProfileAmplitude h a y) =ᵐ[orbitalMeasure 0]
      (fun y => D.profile (oppositeFourierProfilePoint y)) := by
    have hD := longitudinalReflection_measurePreserving.quasiMeasurePreserving.ae D.orbital_ae
    have ha' := longitudinalReflection_measurePreserving.quasiMeasurePreserving.ae ha
    filter_upwards [hD, ha'] with y hy hy'
    have hr : longitudinalReflection (longitudinalReflectionEquiv y) = y :=
      longitudinalReflection_involutive y
    rw [hr] at hy'
    calc
      oppositeNullProfileAmplitude h a y =
          nullProfileAmplitude h' a (longitudinalReflectionEquiv y) := hy'.symm
      _ = D.profile (nullFourierProfilePoint (longitudinalReflectionEquiv y)) := hy
      _ = D.profile (oppositeFourierProfilePoint y) := by
        change D.profile (nullFourierProfilePoint (longitudinalReflection y)) = _
        rw [nullFourierProfilePoint_longitudinalReflection]
  { profile := D.profile
    zero_nonpositive := D.zero_nonpositive
    null_ae := hn
    orbital_ae := ho }

/-- The concrete physical opposite wave is Fourier-Schwartz on AxisCompact. -/
theorem axisCompact_oppositeContractedWave (h : H1) (hh : AxisCompactProfile h)
    (a : Fin 2) (x : NullFourierSpace) :
    oppositeContractedWave h a x = angularForward (axisCompactOppositeData h hh a).profile x :=
  oppositeContractedWave_eq_angularForward h (axisCompactProfile_strongRegular h hh).1
    a (axisCompactOppositeData h hh a) x

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.oppositeFiberSign_apply
#print axioms F1Fecho.MaxwellGlobal.axisCompactProfile_momentumReflection
#print axioms F1Fecho.MaxwellGlobal.axisCompactProfile_oppositeLift
#print axioms F1Fecho.MaxwellGlobal.nullAmplitude_oppositeLift_ae
#print axioms F1Fecho.MaxwellGlobal.nullFourierProfilePoint_longitudinalReflection
#print axioms F1Fecho.MaxwellGlobal.axisCompactOppositeData
#print axioms F1Fecho.MaxwellGlobal.axisCompact_oppositeContractedWave
