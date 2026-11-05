import TGLExt.F1Fecho394.ScreenFutureHelicityR2
import TGLExt.F1Fecho394.WedgeReflectionTranslations

/-! The actual rotation by pi around the longitudinal spatial axis. Its screen
cocycle is the identity, so its action is the existing transverse reflection. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter Matrix
namespace F1Fecho.OrbitalScreen
open TGLExt TGLExt.ImportedSQ ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.OrbitalSpatial F1Rede.GeometricIdentification F1Rede.WedgeReflectionTranslations

def transverseHalfTurn : Spatial ≃ₗᵢ[ℝ] Spatial where
  toFun x := WithLp.toLp 2 (-x.fst,x.snd)
  invFun x := WithLp.toLp 2 (-x.fst,x.snd)
  left_inv x := by apply WithLp.ofLp_injective; simp; rfl
  right_inv x := by apply WithLp.ofLp_injective; simp; rfl
  map_add' x y := by apply WithLp.ofLp_injective; simp [add_comm]
  map_smul' c x := by apply WithLp.ofLp_injective; simp
  norm_map' x := by
    apply (sq_eq_sq₀ (norm_nonneg _) (norm_nonneg _)).mp
    simp only [WithLp.prod_norm_sq_eq_of_L2]
    change ‖-x.fst‖^2+‖x.snd‖^2=‖x.fst‖^2+‖x.snd‖^2
    rw [norm_neg]

def halfTurn : generatedLorentz :=
  generatedSpatial (Unitary.linearIsometryEquiv.symm transverseHalfTurn)

theorem lorentzLinear_halfTurn (v : Fin 4 → ℝ) :
    lorentzLinear halfTurn.val v=![v 0,v 1,-v 2,-v 3] := by
  change (spatialMatrix (Unitary.linearIsometryEquiv
    (Unitary.linearIsometryEquiv.symm transverseHalfTurn))).mulVec v=_
  rw [Unitary.linearIsometryEquiv.apply_symm_apply,spatialMatrix_mulVec]
  funext i
  fin_cases i <;> rfl

theorem halfTurn_sq : halfTurn*halfTurn=1 := by
  apply Subtype.ext
  apply Subtype.ext
  apply Matrix.toLin'.injective
  apply LinearMap.ext
  intro v
  change lorentzLinear (halfTurn.val*halfTurn.val) v=lorentzLinear 1 v
  rw [lorentzLinear_mul,lorentzLinear_one]
  change lorentzLinear halfTurn.val (lorentzLinear halfTurn.val v)=v
  rw [lorentzLinear_halfTurn,lorentzLinear_halfTurn]
  funext i
  fin_cases i <;> simp

theorem halfTurn_inv : halfTurn⁻¹=halfTurn := inv_eq_of_mul_eq_one_right halfTurn_sq

theorem shellAction_halfTurn (p : MomentumCoordinates) :
    shellAction halfTurn.val p=reflectTransverse p := by
  change momentumOf (lorentzLinear halfTurn.val (shellMomentum 0 p))=reflectTransverse p
  rw [lorentzLinear_halfTurn]
  apply Prod.ext
  · funext i; fin_cases i <;> rfl
  · rfl

theorem inverseChart_reflect (p : MomentumCoordinates) :
    inverseRapidityChart 0 (reflectTransverse p)=reflectTransverse (inverseRapidityChart 0 p) := by
  simp [inverseRapidityChart,reflectTransverse,transverseMass_neg]

theorem screen_halfTurn (y : MomentumCoordinates) (j : Fin 2) :
    lorentzLinear halfTurn.val (screen y j)=screen (reflectTransverse y) j := by
  rw [lorentzLinear_halfTurn]
  fin_cases j <;> funext i <;> fin_cases i <;>
    simp [screen,screenOne,screenTwo,reflectTransverse,transverseMass_neg] <;> ring

theorem coefficientMatrix_halfTurn (y : MomentumCoordinates) (hy : y.1≠0) :
    coefficientMatrix (lorentzLinear halfTurn.val) y (reflectTransverse y)=1 := by
  ext i j
  change ((-orbitPairing (screen (reflectTransverse y) i)
    (lorentzLinear halfTurn.val (screen y j)) : ℝ) : ℂ)=(1:Matrix (Fin 2) (Fin 2) ℂ) i j
  rw [screen_halfTurn,ORDEM016.D1prime.screen_metric (reflectTransverse y) (by simpa [reflectTransverse] using hy)]
  by_cases h : i=j <;> simp [Matrix.one_apply,h]

theorem transportMatrix_halfTurn_ae : transportMatrix halfTurn=ᵐ[orbitalMeasure 0] fun _ => 1 := by
  filter_upwards [regular_orbital_ae] with p hp
  unfold transportMatrix
  rw [halfTurn_inv,shellAction_halfTurn,inverseChart_reflect]
  have hy : (reflectTransverse (inverseRapidityChart 0 p)).1≠0 := by
    simpa [reflectTransverse,inverseRapidityChart] using hp
  simpa [reflectTransverse] using coefficientMatrix_halfTurn
    (reflectTransverse (inverseRapidityChart 0 p)) hy

theorem transverseUnitary_halfTurn_ae (f : H1) :
    transverseUnitary halfTurn f=ᵐ[orbitalMeasure 0] fun p => f (reflectTransverse p) := by
  filter_upwards [transverseAction_ae halfTurn f,transportMatrix_halfTurn_ae] with p hp hm
  change transverseAction halfTurn f p=_
  simpa only [hm,halfTurn_inv,shellAction_halfTurn,matrixFiberOperator_one] using hp

end F1Fecho.OrbitalScreen
#print axioms F1Fecho.OrbitalScreen.lorentzLinear_halfTurn
#print axioms F1Fecho.OrbitalScreen.halfTurn_sq
#print axioms F1Fecho.OrbitalScreen.transportMatrix_halfTurn_ae
#print axioms F1Fecho.OrbitalScreen.transverseUnitary_halfTurn_ae
