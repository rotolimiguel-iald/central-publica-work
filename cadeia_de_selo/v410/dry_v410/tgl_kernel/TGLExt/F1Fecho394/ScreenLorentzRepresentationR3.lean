import TGLExt.F1Fecho394.ScreenMatrixMultiplierR4
import TGLExt.F1Fecho394.ScreenLorentzCocycleR3

/-! The actual transverse Lorentz representation on the canonical H1.
The screen cocycle and measure-preserving pullback provide all unitary/group
laws. Strong continuity and circular helicity identification are separate. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter Matrix
namespace F1Fecho.OrbitalScreen
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.OrbitalSpatial

theorem matrixFiberOperator_one (v : Fiber) : matrixFiberOperator 1 v=v := by
  simp [matrixFiberOperator]

theorem matrixFiberOperator_mul (A B : Matrix (Fin 2) (Fin 2) ℂ) (v : Fiber) :
    matrixFiberOperator (A*B) v=matrixFiberOperator A (matrixFiberOperator B v) := by
  unfold matrixFiberOperator
  rw [map_mul]
  rfl

def transverseAction (L : generatedLorentz) : H1 →L[ℂ] H1 :=
  (matrixMultiplier (transportMatrix L) (transportMatrix_measurable L)
    (transportMatrix_unitary_ae L)).comp (generatedUnitary L).toLinearIsometry.toContinuousLinearMap

theorem transverseAction_ae (L : generatedLorentz) (f : H1) :
    transverseAction L f=ᵐ[orbitalMeasure 0] fun p =>
      matrixFiberOperator (transportMatrix L p) (f (shellAction (L⁻¹).val p)) := by
  filter_upwards [matrixMultiplier_ae (transportMatrix L) (transportMatrix_measurable L)
    (transportMatrix_unitary_ae L) (generatedUnitary L f),generatedUnitary_ae L f]
      with p hp hq
  change transverseAction L f p=_
  change matrixMultiplier (transportMatrix L) (transportMatrix_measurable L)
    (transportMatrix_unitary_ae L) (generatedUnitary L f) p=_
  rw [hp,hq]

theorem transverseAction_norm (L : generatedLorentz) (f : H1) : ‖transverseAction L f‖=‖f‖ := by
  change ‖matrixMultiplier (transportMatrix L) (transportMatrix_measurable L)
    (transportMatrix_unitary_ae L) (generatedUnitary L f)‖=_
  rw [matrixMultiplier_norm,(generatedUnitary L).norm_map]

theorem transverseAction_one (f : H1) : transverseAction 1 f=f := by
  apply Lp.ext
  filter_upwards [transverseAction_ae 1 f,transportMatrix_one_ae,shellAction_one_ae]
    with p hp hm hs
  simpa only [hm,inv_one,OneMemClass.coe_one,hs,id_eq,matrixFiberOperator_one] using hp

theorem transverseAction_mul (L M : generatedLorentz) (f : H1) :
    transverseAction (L*M) f=transverseAction L (transverseAction M f) := by
  have hi := (shellAction_lift L⁻¹).1.quasiMeasurePreserving.ae (transverseAction_ae M f)
  apply Lp.ext
  filter_upwards [transverseAction_ae (L*M) f,transverseAction_ae L (transverseAction M f),hi,
    transportMatrix_mul_ae L M,shellAction_mul_ae M⁻¹ L⁻¹] with p hp hq hi hc hs
  rw [hp,hq,hi,hc,matrixFiberOperator_mul]
  congr 2
  simpa only [_root_.mul_inv_rev,Function.comp_apply] using congrArg (fun q => f q) hs

theorem transverseAction_inverse (L : generatedLorentz) (f : H1) :
    transverseAction L (transverseAction L⁻¹ f)=f := by
  rw [←transverseAction_mul,mul_inv_cancel,transverseAction_one]

def transverseIsometry (L : generatedLorentz) : H1 →ₗᵢ[ℂ] H1 where
  toLinearMap := (transverseAction L).toLinearMap
  norm_map' := transverseAction_norm L

def transverseUnitary (L : generatedLorentz) : H1 ≃ₗᵢ[ℂ] H1 :=
  LinearIsometryEquiv.ofLinearIsometry (transverseIsometry L)
    (transverseAction L⁻¹).toLinearMap
    (by apply LinearMap.ext; intro f; exact transverseAction_inverse L f)
    (by
      apply LinearMap.ext
      intro f
      change transverseAction L⁻¹ (transverseAction L f)=f
      simpa only [inv_inv] using transverseAction_inverse L⁻¹ f)

def transverseUnitaryHom : generatedLorentz →* (H1 ≃ₗᵢ[ℂ] H1) where
  toFun := transverseUnitary
  map_one' := by apply LinearIsometryEquiv.ext; intro f; exact transverseAction_one f
  map_mul' L M := by apply LinearIsometryEquiv.ext; intro f; exact transverseAction_mul L M f

end F1Fecho.OrbitalScreen
#print axioms F1Fecho.OrbitalScreen.transverseAction_ae
#print axioms F1Fecho.OrbitalScreen.transverseAction_mul
#print axioms F1Fecho.OrbitalScreen.transverseUnitaryHom
