import TGLExt.F1Fecho394.ScreenFutureHelicityR2
import TGLExt.F1Fecho394.GeometricFiberConjugation

/-! The existing helicity-exchanging fiber conjugation acts on canonical H1.
Its Lorentz commutation is proved from the actual circular phase formula. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open MeasureTheory Filter Matrix Complex
namespace F1Fecho.OrbitalScreen
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.WignerOrbit016
open F1Fecho.OrbitalSpatial F1Rede.FiberConjugation

def thetaMap : H1 →SL[starRingEnd ℂ] H1 :=
  fiberSwappedJ.toContinuousLinearEquiv.toContinuousLinearMap.compLpL 2 (orbitalMeasure 0)

theorem thetaMap_ae (f : H1) : thetaMap f=ᵐ[orbitalMeasure 0] fun p => fiberSwappedJ (f p) :=
  fiberSwappedJ.toContinuousLinearEquiv.toContinuousLinearMap.coeFn_compLpL f

theorem thetaMap_involutive : Function.Involutive thetaMap := by
  intro f
  apply Lp.ext
  filter_upwards [thetaMap_ae (thetaMap f),thetaMap_ae f] with p hp hq
  rw [hp,hq,fiberSwappedJ_involutive]

theorem thetaMap_norm (f : H1) : ‖thetaMap f‖=‖f‖ := by
  simp only [Lp.norm_def]
  congr 1
  apply eLpNorm_congr_norm_ae
  filter_upwards [thetaMap_ae f] with p hp
  rw [hp,fiberSwappedJ.norm_map]

def Theta : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1 where
  toLinearEquiv := {thetaMap.toLinearMap with
    invFun := thetaMap
    left_inv := thetaMap_involutive
    right_inv := thetaMap_involutive}
  norm_map' := thetaMap_norm

theorem Theta_ae (f : H1) : Theta f=ᵐ[orbitalMeasure 0] fun p => fiberSwappedJ (f p) :=
  thetaMap_ae f

theorem Theta_involutive : Function.Involutive Theta := thetaMap_involutive

theorem phaseMatrix_swappedJ (z : ℂ) (v : Fiber) :
    fiberSwappedJ (matrixFiberOperator (phaseMatrix z) v)=
      matrixFiberOperator (phaseMatrix z) (fiberSwappedJ v) := by
  ext i
  fin_cases i <;>
    simp [matrixFiberOperator,Matrix.ofLp_toEuclideanCLM,phaseMatrix,
      Matrix.mulVec,dotProduct,Fin.sum_univ_two,fiberSwappedJ_apply,helicitySwap]

theorem Theta_helicity (L : generatedLorentz) (hd : L.val.val.det=1) (f : H1) :
    Theta (helicityUnitary L f)=helicityUnitary L (Theta f) := by
  have hc := (shellAction_lift L⁻¹).1.quasiMeasurePreserving.ae (Theta_ae f)
  apply Lp.ext
  filter_upwards [Theta_ae (helicityUnitary L f),helicityUnitary_diagonal_ae L hd f,
    helicityUnitary_diagonal_ae L hd (Theta f),hc] with p hp hq hr hs
  rw [hp,hq,hr,hs,phaseMatrix_swappedJ]

theorem orbitalPhase_negation (a : Fin 4 → ℝ) (p : MomentumCoordinates) :
    star (orbitalPhase 0 a p)=orbitalPhase 0 (-a) p := by
  have hn : orbitPairing (-a) (shellMomentum 0 p)= -orbitPairing a (shellMomentum 0 p) := by
    simp [orbitPairing]
    ring
  unfold orbitalPhase phase
  rw [hn]
  change (starRingEnd ℂ) (Complex.exp _)=Complex.exp _
  rw [←Complex.exp_conj]
  congr 1
  simp

theorem Theta_U1 (a : Fin 4 → ℝ) (f : H1) : Theta (U1 a f)=U1 (-a) (Theta f) := by
  apply Lp.ext
  filter_upwards [Theta_ae (U1 a f),orbitalTranslation_ae 0 a f,
    orbitalTranslation_ae 0 (-a) (Theta f),Theta_ae f] with p hp hq hr hs
  change U1 a f p=orbitalPhase 0 a p • f p at hq
  change U1 (-a) (Theta f) p=orbitalPhase 0 (-a) p • Theta f p at hr
  rw [hp,hq,hr,hs,map_smulₛₗ]
  exact congrArg (fun z : ℂ => z • fiberSwappedJ (f p)) (orbitalPhase_negation a p)

end F1Fecho.OrbitalScreen
#print axioms F1Fecho.OrbitalScreen.Theta
#print axioms F1Fecho.OrbitalScreen.Theta_involutive
#print axioms F1Fecho.OrbitalScreen.phaseMatrix_swappedJ
#print axioms F1Fecho.OrbitalScreen.Theta_helicity
#print axioms F1Fecho.OrbitalScreen.Theta_U1
