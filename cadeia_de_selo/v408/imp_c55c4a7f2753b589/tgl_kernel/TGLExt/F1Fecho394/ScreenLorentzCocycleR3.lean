import TGLExt.F1Fecho394.ScreenLorentzTransportR7

/-! Actual measurable Lorentz screen cocycle, with the chart axes handled a.e. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter Matrix
namespace F1Fecho.OrbitalScreen
open TGLExt ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.OrbitalSpatial

theorem transportMatrix_mul_ae (L M : generatedLorentz) :
    transportMatrix (L*M)=ᵐ[orbitalMeasure 0]
      fun p => transportMatrix L p*transportMatrix M (shellAction (L⁻¹).val p) := by
  have mL := (shellAction_lift L⁻¹).1.quasiMeasurePreserving
  have mM := (shellAction_lift M⁻¹).1.quasiMeasurePreserving
  filter_upwards [regular_orbital_ae,mL.ae regular_orbital_ae,
    mL.ae (mM.ae regular_orbital_ae),chart_inverse_ae 0,mL.ae (chart_inverse_ae 0),
    mL.ae (mM.ae (chart_inverse_ae 0)),inverse_shell_transport_ae L,
    mL.ae (inverse_shell_transport_ae M),shellAction_mul_ae M⁻¹ L⁻¹]
      with p hp hq hr hpc hqc hrc hLp hMq hc
  unfold transportMatrix
  simp only [_root_.mul_inv_rev]
  rw [show shellAction (M⁻¹*L⁻¹).val p=
      shellAction (M⁻¹).val (shellAction (L⁻¹).val p) from hc,
    Subgroup.coe_mul,lorentzLinear_mul]
  apply coefficientMatrix_comp
  · exact hr
  · exact hq
  · exact hp
  · rw [hrc,hqc]
    exact hMq
  · rw [hqc,hpc]
    exact hLp
  · exact orbitPairing_lorentz M.val

end F1Fecho.OrbitalScreen
#print axioms F1Fecho.OrbitalScreen.transportMatrix_mul_ae
