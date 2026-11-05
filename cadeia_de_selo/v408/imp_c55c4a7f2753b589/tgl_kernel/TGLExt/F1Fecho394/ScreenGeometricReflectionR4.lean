import TGLExt.F1Fecho394.ScreenHalfTurnR3
import TGLExt.F1Fecho394.ScreenChargeConjugationR2

/-! Connect the existing spectral/geometric J to the concrete helicity action.
Fourier conjugation and the canonical J formula are imported, not reconstructed. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter
namespace F1Fecho.OrbitalScreen
open TGLExt.ImportedSQ AuditF13v31 ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.OrbitalSpatial F1Rede.GeometricIdentification F1Rede.WedgeReflectionTranslations
open F1Rede.CanonicalWedge F1Rede.FiberConjugation

theorem helicityUnitary_halfTurn_ae (f : H1) :
    helicityUnitary halfTurn f=ᵐ[orbitalMeasure 0] fun p => f (reflectTransverse p) := by
  have he : circularH1 (helicityUnitary halfTurn f)=transverseUnitary halfTurn (circularH1 f) := by
    rw [helicityUnitary_apply,circularH1.apply_symm_apply]
  have hc := (shellAction_lift halfTurn⁻¹).1.quasiMeasurePreserving.ae (fiberLiftMap_ae circularFiber f)
  filter_upwards [fiberLiftMap_ae circularFiber (helicityUnitary halfTurn f),
    transverseUnitary_halfTurn_ae (circularH1 f),hc] with p hp hq hr
  have hev := congrArg (fun v : H1 => v p) he
  change fiberLiftMap circularFiber (helicityUnitary halfTurn f) p=
    transverseUnitary halfTurn (circularH1 f) p at hev
  rw [hp,hq] at hev
  rw [halfTurn_inv,shellAction_halfTurn] at hr
  change circularFiber (helicityUnitary halfTurn f p)=fiberLiftMap circularFiber f (reflectTransverse p) at hev
  rw [hr] at hev
  exact circularFiber.injective hev

theorem rapidityChart_reflect (p : MomentumCoordinates) :
    rapidityChart 0 (reflectTransverse p)=reflectTransverse (rapidityChart 0 p) := by
  simp [rapidityChart,reflectTransverse,transverseMass_neg]

theorem Jcandidate_eq_helicity_halfTurn_Theta (f : H1) :
    Jcandidate f=helicityUnitary halfTurn (Theta f) := by
  apply toRapidity.injective
  apply Lp.ext
  have hrot := (rapidityChart_measurePreserving 0).quasiMeasurePreserving.ae
    (helicityUnitary_halfTurn_ae (Theta f))
  have htheta := reflectTransverse_preserves.quasiMeasurePreserving.ae
    ((rapidityChart_measurePreserving 0).quasiMeasurePreserving.ae (Theta_ae f))
  have hf := reflectTransverse_preserves.quasiMeasurePreserving.ae (orbitalL2Pullback_ae 0 f)
  filter_upwards [Jcandidate_rapidity_ae f,
    orbitalL2Pullback_ae 0 (helicityUnitary halfTurn (Theta f)),hrot,htheta,hf]
      with p hj hp hr ht hf
  change toRapidity (helicityUnitary halfTurn (Theta f)) p=
    helicityUnitary halfTurn (Theta f) (rapidityChart 0 p) at hp
  change toRapidity f (reflectTransverse p)=f (rapidityChart 0 (reflectTransverse p)) at hf
  rw [hj,hp,hr]
  change fiberSwappedJ (toRapidity f (reflectTransverse p)) =
    Theta f (reflectTransverse (rapidityChart 0 p))
  rw [hf,←rapidityChart_reflect,ht]

theorem Jcandidate_helicity_intertwines (L : generatedLorentz) (hd : L.val.val.det=1) (f : H1) :
    Jcandidate (helicityUnitary L f)=helicityUnitary (halfTurn*L*halfTurn) (Jcandidate f) := by
  rw [Jcandidate_eq_helicity_halfTurn_Theta,Theta_helicity L hd,
    Jcandidate_eq_helicity_halfTurn_Theta,←helicityUnitary_mul,←helicityUnitary_mul]
  simp only [mul_assoc,halfTurn_sq,mul_one]

theorem Jcandidate_conjugates_helicity (L : generatedLorentz) (hd : L.val.val.det=1) (f : H1) :
    Jcandidate (helicityUnitary L (Jcandidate f))=helicityUnitary (halfTurn*L*halfTurn) f := by
  rw [Jcandidate_helicity_intertwines L hd,Jcandidate_involutive]

end F1Fecho.OrbitalScreen
#print axioms F1Fecho.OrbitalScreen.helicityUnitary_halfTurn_ae
#print axioms F1Fecho.OrbitalScreen.Jcandidate_eq_helicity_halfTurn_Theta
#print axioms F1Fecho.OrbitalScreen.Jcandidate_helicity_intertwines
#print axioms F1Fecho.OrbitalScreen.Jcandidate_conjugates_helicity
