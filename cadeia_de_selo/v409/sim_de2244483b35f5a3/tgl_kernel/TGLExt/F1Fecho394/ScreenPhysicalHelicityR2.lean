import TGLExt.F1Fecho394.ScreenPoincareCovarianceR2
import TGLExt.F1Fecho394.ScreenCircularCoefficientsR1
import TGLExt.F1Fecho394.ScreenOrientationDetRootR3

/-! The proper Lorentz helicity phase is derived from its geometric screen
transport; no independent screen orientation hypothesis is added. -/
set_option autoImplicit false
set_option maxHeartbeats 2000000
noncomputable section
open MeasureTheory Filter Matrix
namespace F1Fecho.OrbitalScreen
open TGLExt TGLExt.ImportedSQ ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.OrbitalSpatial ORDEM016.D1prime

theorem lorentzLinear_toMatrix (L : LorentzGrp) : LinearMap.toMatrix' (lorentzLinear L)=L.val := by
  change LinearMap.toMatrix' (Matrix.toLin' L.val)=L.val
  exact LinearMap.toMatrix'_toLin' L.val

theorem transport_orientation_ae (L : generatedLorentz) (hd : L.val.val.det=1) :
    ∀ᵐ p ∂orbitalMeasure 0, ScreenOrientationMeasured (lorentzLinear L.val)
      (inverseRapidityChart 0 (shellAction (L⁻¹).val p)) (inverseRapidityChart 0 p) := by
  have hr := (shellAction_lift L⁻¹).1.quasiMeasurePreserving.ae regular_orbital_ae
  have hc := (shellAction_lift L⁻¹).1.quasiMeasurePreserving.ae (chart_inverse_ae 0)
  filter_upwards [regular_orbital_ae,hr,chart_inverse_ae 0,hc,inverse_shell_transport_ae L]
    with p hp hq hpc hqc ht
  apply F1Fecho.ScreenOrientation.screen_orientation_of_proper_transport
    (lorentzLinear L.val) (inverseRapidityChart 0 (shellAction (L⁻¹).val p))
    (inverseRapidityChart 0 p) hq hp
  · rw [hqc,hpc]
    exact ht
  · exact orbitPairing_lorentz L.val
  · rw [lorentzLinear_toMatrix]
    exact hd

def transportPhase (L : generatedLorentz) (p : MomentumCoordinates) : ℂ :=
  screenPhase (lorentzLinear L.val)
    (inverseRapidityChart 0 (shellAction (L⁻¹).val p)) (inverseRapidityChart 0 p)

theorem transportPhase_unit_ae (L : generatedLorentz) (hd : L.val.val.det=1) :
    ∀ᵐ p ∂orbitalMeasure 0, Complex.normSq (transportPhase L p)=1 := by
  have mL := (shellAction_lift L⁻¹).1.quasiMeasurePreserving
  filter_upwards [regular_orbital_ae,mL.ae regular_orbital_ae,chart_inverse_ae 0,
    mL.ae (chart_inverse_ae 0),inverse_shell_transport_ae L,transport_orientation_ae L hd]
    with p hp hq hpc hqc ht ho
  apply oriented_screen_phase_unit (lorentzLinear L.val) (inverseRapidityChart 0 (shellAction (L⁻¹).val p))
    (inverseRapidityChart 0 p) hq hp
  · rw [hqc,hpc]
    exact ht
  · exact orbitPairing_lorentz L.val
  · exact ho

theorem transportPhase_mul_ae (L M : generatedLorentz) (hd : M.val.val.det=1) :
    transportPhase (L*M)=ᵐ[orbitalMeasure 0]
      fun p => transportPhase L p*transportPhase M (shellAction (L⁻¹).val p) := by
  have mL := (shellAction_lift L⁻¹).1.quasiMeasurePreserving
  have mM := (shellAction_lift M⁻¹).1.quasiMeasurePreserving
  filter_upwards [regular_orbital_ae,mL.ae regular_orbital_ae,
    mL.ae (mM.ae regular_orbital_ae),chart_inverse_ae 0,mL.ae (chart_inverse_ae 0),
    mL.ae (mM.ae (chart_inverse_ae 0)),inverse_shell_transport_ae L,
    mL.ae (inverse_shell_transport_ae M),shellAction_mul_ae M⁻¹ L⁻¹,
    mL.ae (transport_orientation_ae M hd)]
      with p hp hq hr hpc hqc hrc hLp hMq hc ho
  unfold transportPhase
  simp only [_root_.mul_inv_rev]
  rw [show shellAction (M⁻¹*L⁻¹).val p=
      shellAction (M⁻¹).val (shellAction (L⁻¹).val p) from hc,
    Subgroup.coe_mul,lorentzLinear_mul]
  apply screen_phase_cocycle
  · exact hr
  · exact hq
  · exact hp
  · rw [hrc,hqc]; exact hMq
  · rw [hqc,hpc]; exact hLp
  · exact orbitPairing_lorentz M.val
  · exact ho

theorem transportMatrix_circular_ae (L : generatedLorentz) (hd : L.val.val.det=1) :
    ∀ᵐ p ∂orbitalMeasure 0,
      (transportMatrix L p).mulVec (circularCoefficients 1)=transportPhase L p • circularCoefficients 1 ∧
      (transportMatrix L p).mulVec (circularCoefficients (-1))=
        star (transportPhase L p) • circularCoefficients (-1) := by
  have mL := (shellAction_lift L⁻¹).1.quasiMeasurePreserving
  filter_upwards [regular_orbital_ae,mL.ae regular_orbital_ae,chart_inverse_ae 0,
    mL.ae (chart_inverse_ae 0),inverse_shell_transport_ae L,transport_orientation_ae L hd]
    with p hp hq hpc hqc ht ho
  have hg : lorentzLinear L.val (shellMomentum 0 (rapidityChart 0
      (inverseRapidityChart 0 (shellAction (L⁻¹).val p))))=
      shellMomentum 0 (rapidityChart 0 (inverseRapidityChart 0 p)) := by
    rw [hqc,hpc]; exact ht
  exact ⟨circularCoefficient_plus _ _ _ hq hp hg (orbitPairing_lorentz L.val) ho,
    circularCoefficient_minus _ _ _ hq hp hg (orbitPairing_lorentz L.val) ho⟩

end F1Fecho.OrbitalScreen
#print axioms F1Fecho.OrbitalScreen.transport_orientation_ae
#print axioms F1Fecho.OrbitalScreen.transportPhase_unit_ae
#print axioms F1Fecho.OrbitalScreen.transportPhase_mul_ae
#print axioms F1Fecho.OrbitalScreen.transportMatrix_circular_ae
