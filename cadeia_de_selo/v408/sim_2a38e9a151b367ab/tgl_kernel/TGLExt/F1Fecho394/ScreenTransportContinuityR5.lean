import TGLExt.F1Fecho394.ScreenLorentzTransportR7

/-! Pointwise continuity of the actual screen cocycle away from its null chart axis. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter Matrix
namespace F1Fecho.OrbitalScreen
open TGLExt ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.OrbitalSpatial

attribute [local fun_prop] Real.continuous_arsinh Complex.continuous_ofReal

@[fun_prop] theorem transverseMass_continuous (m : ℝ) : Continuous (transverseMass m) := by
  unfold transverseMass
  fun_prop

theorem screen_continuousAt (i : Fin 2) (x : MomentumCoordinates) (hx : x.1 ≠ 0) :
    ContinuousAt (fun y => screen y i) x := by
  have hr : transverseMass 0 x.1 ≠ 0 := (transverseMass_pos_of_ne_zero 0 x.1 hx).ne'
  apply continuousAt_pi.mpr
  intro j
  fin_cases i <;> fin_cases j
  all_goals
    dsimp [screen,screenOne,screenTwo]
    fun_prop (disch := assumption)

theorem inverseRapidityChart_continuousAt (p : MomentumCoordinates) (hp : p.1 ≠ 0) :
    ContinuousAt (inverseRapidityChart 0) p := by
  have hr : transverseMass 0 p.1 ≠ 0 := (transverseMass_pos_of_ne_zero 0 p.1 hp).ne'
  unfold inverseRapidityChart
  fun_prop (disch := assumption)

theorem inverseShell_continuous (p : MomentumCoordinates) :
    Continuous (fun L : generatedLorentz => shellAction (L⁻¹).val p) := by
  change Continuous (fun L : generatedLorentz =>
    momentumOf ((lorentzInv L.val.val).mulVec (shellMomentum 0 p)))
  unfold momentumOf lorentzInv
  fun_prop

theorem transportMatrix_continuousAt (L : generatedLorentz) (p : MomentumCoordinates)
    (hq : (shellAction (L⁻¹).val p).1 ≠ 0) :
    ContinuousAt (fun M : generatedLorentz => transportMatrix M p) L := by
  have hx : ContinuousAt (fun M : generatedLorentz => inverseRapidityChart 0 (shellAction (M⁻¹).val p)) L :=
    (inverseRapidityChart_continuousAt (shellAction (L⁻¹).val p) hq).comp (f := fun M : generatedLorentz => shellAction (M⁻¹).val p) (inverseShell_continuous p).continuousAt
  have hs (j : Fin 2) : ContinuousAt (fun M : generatedLorentz =>
      screen (inverseRapidityChart 0 (shellAction (M⁻¹).val p)) j) L :=
    (screen_continuousAt j (inverseRapidityChart 0 (shellAction (L⁻¹).val p)) hq).comp (f := fun M : generatedLorentz => inverseRapidityChart 0 (shellAction (M⁻¹).val p)) hx
  apply continuousAt_pi.mpr
  intro i
  apply continuousAt_pi.mpr
  intro j
  have hg : ContinuousAt (fun M : generatedLorentz =>
      lorentzLinear M.val (screen (inverseRapidityChart 0 (shellAction (M⁻¹).val p)) j)) L := by
    change ContinuousAt (fun M : generatedLorentz =>
      M.val.val.mulVec (screen (inverseRapidityChart 0 (shellAction (M⁻¹).val p)) j)) L
    fun_prop
  change ContinuousAt (fun M : generatedLorentz =>
    ((-orbitPairing (screen (inverseRapidityChart 0 p) i)
      (lorentzLinear M.val (screen (inverseRapidityChart 0 (shellAction (M⁻¹).val p)) j)) : ℝ) : ℂ)) L
  have hgk (k : Fin 4) : ContinuousAt (fun M : generatedLorentz =>
      lorentzLinear M.val (screen (inverseRapidityChart 0 (shellAction (M⁻¹).val p)) j) k) L :=
    (continuous_apply k).continuousAt.comp
      (f := fun M : generatedLorentz => lorentzLinear M.val
        (screen (inverseRapidityChart 0 (shellAction (M⁻¹).val p)) j)) hg
  exact Complex.continuous_ofReal.continuousAt.comp
    (((((continuousAt_const.mul (hgk 0)).sub (continuousAt_const.mul (hgk 1))).sub
      (continuousAt_const.mul (hgk 2))).sub (continuousAt_const.mul (hgk 3))).neg)

theorem transportMatrix_continuousAt_ae (L : generatedLorentz) :
    ∀ᵐ p ∂orbitalMeasure 0, ContinuousAt (fun M : generatedLorentz => transportMatrix M p) L := by
  filter_upwards [(shellAction_lift L⁻¹).1.quasiMeasurePreserving.ae regular_orbital_ae] with p hp
  exact transportMatrix_continuousAt L p hp

end F1Fecho.OrbitalScreen
#print axioms F1Fecho.OrbitalScreen.transportMatrix_continuousAt_ae
