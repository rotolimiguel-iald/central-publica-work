import TGLExt.F1Fecho394.ScreenLorentzRepresentationR3

/-! Translation covariance and the existing longitudinal boost are realized by
 the actual transverse cocycle, on the same H1. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter Matrix
namespace F1Fecho.OrbitalScreen
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31
open ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.OrbitalSpatial

theorem transverseUnitary_U1 (L : generatedLorentz) (a : Fin 4 → ℝ) (f : H1) :
    transverseUnitary L (U1 a f)=U1 (L.val.val.mulVec a) (transverseUnitary L f) := by
  change transverseAction L (orbitalTranslation 0 a f)=
    orbitalTranslation 0 (L.val.val.mulVec a) (transverseAction L f)
  have htr := (shellAction_lift L⁻¹).1.quasiMeasurePreserving.ae (orbitalTranslation_ae 0 a f)
  apply Lp.ext
  filter_upwards [transverseAction_ae L (orbitalTranslation 0 a f),htr,
    orbitalTranslation_ae 0 (L.val.val.mulVec a) (transverseAction L f),
    transverseAction_ae L f,generatedPhase_ae L a] with p h1 h2 h3 h4 h5
  rw [h1,h2,h3,h4,h5,map_smul]

def transversePoincareH1 (a : Fin 4 → ℝ) (L : generatedLorentz) : H1≃ₗᵢ[ℂ]H1 :=
  (transverseUnitary L).trans (U1 a)

theorem transversePoincareH1_mul (a b : Fin 4 → ℝ) (L M : generatedLorentz) (f : H1) :
    transversePoincareH1 (a+L.val.val.mulVec b) (L*M) f=
      transversePoincareH1 a L (transversePoincareH1 b M f) := by
  change U1 (a+L.val.val.mulVec b) (transverseUnitary (L*M) f)=
    U1 a (transverseUnitary L (U1 b (transverseUnitary M f)))
  rw [transverseUnitary_U1]
  change U1 (a+L.val.val.mulVec b) (transverseAction (L*M) f)=_
  rw [transverseAction_mul]
  exact orbitalTranslation_add 0 a _ _

theorem screen_boost (s : ℝ) (y : MomentumCoordinates) (j : Fin 2) :
    wedgeBoostMap s (screen y j)=screen (coordinateShift s y) j := by
  fin_cases j
  · exact screenOne_boost s y
  · exact screenTwo_boost s y

theorem coefficientMatrix_boost (s : ℝ) (y : MomentumCoordinates) (hy : y.1≠0) :
    coefficientMatrix (lorentzLinear (theBoost s)) y (coordinateShift s y)=1 := by
  ext i j
  change ((-orbitPairing (screen (coordinateShift s y) i) (wedgeBoostMap s (screen y j)):ℝ):ℂ)=
    (1:Matrix (Fin 2) (Fin 2) ℂ) i j
  rw [screen_boost,ORDEM016.D1prime.screen_metric (coordinateShift s y) hy]
  by_cases h : i=j <;> simp [Matrix.one_apply,h]

theorem inverseChart_coordinateBoost (s : ℝ) (p : MomentumCoordinates) (hp : p.1≠0) :
    inverseRapidityChart 0 (coordinateBoost 0 s p)=coordinateShift s (inverseRapidityChart 0 p) := by
  have hr := transverseMass_pos_of_ne_zero 0 p.1 hp
  calc
    _ = inverseRapidityChart 0 (coordinateBoost 0 s (rapidityChart 0 (inverseRapidityChart 0 p))) := by
      rw [chart_inverse_of_positive 0 p hr]
    _ = inverseRapidityChart 0 (rapidityChart 0 (coordinateShift s (inverseRapidityChart 0 p))) := by
      rw [boost_chart_intertwines_of_positive 0 s (inverseRapidityChart 0 p) hr]
    _ = _ := inverse_chart_of_positive 0 (coordinateShift s (inverseRapidityChart 0 p)) hr

theorem transportMatrix_boost_ae (s : ℝ) :
    transportMatrix (generatedBoost s)=ᵐ[orbitalMeasure 0] fun _ => 1 := by
  have h := shellAction_eq_lift (shellLift_boost (-s))
  filter_upwards [h,regular_orbital_ae] with p hp hr
  unfold transportMatrix
  change coefficientMatrix (lorentzLinear (theBoost s))
    (inverseRapidityChart 0 (shellAction ((theBoost s)⁻¹) p)) (inverseRapidityChart 0 p)=1
  rw [theBoost_inv_eq,hp,inverseChart_coordinateBoost (-s) p hr]
  have he : coordinateShift s (coordinateShift (-s) (inverseRapidityChart 0 p))=
      inverseRapidityChart 0 p := by
    apply Prod.ext
    · rfl
    · dsimp [coordinateShift]; ring
  have hb := coefficientMatrix_boost s (coordinateShift (-s) (inverseRapidityChart 0 p)) hr
  rw [he] at hb
  exact hb

theorem transverseUnitary_boost (s : ℝ) (f : H1) :
    transverseUnitary (generatedBoost s) f=B0 s f := by
  rw [←generatedUnitary_boost]
  apply Lp.ext
  filter_upwards [transverseAction_ae (generatedBoost s) f,generatedUnitary_ae (generatedBoost s) f,
    transportMatrix_boost_ae s] with p hp hq hm
  change transverseAction (generatedBoost s) f p=_
  rw [hp,hq,hm,matrixFiberOperator_one]

end F1Fecho.OrbitalScreen
#print axioms F1Fecho.OrbitalScreen.transverseUnitary_U1
#print axioms F1Fecho.OrbitalScreen.transversePoincareH1_mul
#print axioms F1Fecho.OrbitalScreen.transverseUnitary_boost
