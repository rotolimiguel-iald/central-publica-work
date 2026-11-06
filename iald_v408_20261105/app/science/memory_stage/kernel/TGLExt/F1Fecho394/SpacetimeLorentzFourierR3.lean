import TGLExt.F1Fecho394.ScreenPhysicalHelicityR2
import TGLExt.F1Fecho394.PhysicalFourierTranslationR3
import Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar

/-! The already constructed Lorentz matrices act on the actual Euclidean
coordinate model used by Schwartz tensors. Haar volume and the positive
angular Fourier pairing are transported explicitly. No net covariance is
inferred from this scalar change-of-variables lemma. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Matrix
open scoped FourierTransform
namespace F1Fecho.SpacetimeLorentz
open TGLExt F1Fecho.MaxwellGlobal F1Fecho.OrbitalSpatial F1Fecho.OrbitalScreen
open ChatgptAudit.WignerOrbit016

def coordinateEquiv : Spacetime ≃ₗ[ℝ] (Fin 4→ℝ) := WithLp.linearEquiv 2 ℝ _

def lorentzEquiv (L:LorentzGrp) : (Fin 4→ℝ) ≃ₗ[ℝ] (Fin 4→ℝ) where
  toFun := L.val.mulVec
  map_add' := Matrix.mulVec_add L.val
  map_smul' c x := by simp [Matrix.mulVec_smul]
  invFun := lorentzLinear L⁻¹
  left_inv x := by
    change L⁻¹.val.mulVec (L.val.mulVec x)=x
    rw [Matrix.mulVec_mulVec,←lorentzGrp_mul_val,inv_mul_cancel,lorentzGrp_one_val,Matrix.one_mulVec]
  right_inv x := by
    change L.val.mulVec (L⁻¹.val.mulVec x)=x
    rw [Matrix.mulVec_mulVec,←lorentzGrp_mul_val,mul_inv_cancel,lorentzGrp_one_val,Matrix.one_mulVec]

def action (L:LorentzGrp) : Spacetime ≃L[ℝ] Spacetime :=
  ((coordinateEquiv.trans (lorentzEquiv L)).trans coordinateEquiv.symm).toContinuousLinearEquiv

theorem action_apply (L:LorentzGrp) (x:Spacetime) :
    (fun i=>action L x i)=L.val.mulVec (fun i=>x i) := rfl

theorem action_det (L:LorentzGrp) :
    LinearMap.det (action L).toLinearMap=L.val.det := by
  change LinearMap.det (coordinateEquiv.symm.toLinearMap.comp
    ((lorentzLinear L).comp coordinateEquiv.toLinearMap))=L.val.det
  exact (LinearMap.det_conj (lorentzLinear L) coordinateEquiv.symm).trans
    (by change LinearMap.det (Matrix.toLin' L.val)=L.val.det; exact LinearMap.det_toLin' L.val)

theorem action_measurePreserving (L:LorentzGrp) :
    MeasurePreserving (action L) volume volume := by
  have hs:=lorentz_det_sq L
  have hn:L.val.det≠0 := by intro h; rw [h] at hs; norm_num at hs
  have ha:|L.val.det|=1 := by nlinarith [sq_abs L.val.det,abs_nonneg L.val.det]
  refine ⟨(action L).continuous.measurable,?_⟩
  change Measure.map (action L).toLinearMap volume=volume
  rw [Measure.map_linearMap_addHaar_eq_smul_addHaar volume (by rwa [action_det]),action_det,
    abs_inv,ha,inv_one,ENNReal.ofReal_one,one_smul]

theorem pairing_action (L:LorentzGrp) (x p:Spacetime) :
    orbitPairing (fun i=>action L x i) (fun i=>action L p i)=
      orbitPairing (fun i=>x i) (fun i=>p i) := orbitPairing_lorentz L _ _

theorem pairing_transfer (L:LorentzGrp) (x p:Spacetime) :
    orbitPairing (fun i=>action L x i) (fun i=>p i)=
      orbitPairing (fun i=>x i) (fun i=>(action L).symm p i) := by
  have h:=pairing_action L x ((action L).symm p)
  simpa only [ContinuousLinearEquiv.apply_symm_apply] using h

variable {E:Type*} [NormedAddCommGroup E] [NormedSpace ℂ E]

theorem angular_inverse_integral (f:Spacetime→E) (p:Spacetime) :
    (𝓕⁻ f) ((2*Real.pi)⁻¹ • metricFlip p)=
      ∫x:Spacetime,Complex.exp ((orbitPairing (fun i=>x i) (fun i=>p i):ℂ)*Complex.I) • f x := by
  rw [Real.fourierInv_eq']
  congr 1
  funext x
  rw [PhysicalFourier.angular_pairing]

theorem angular_inverse_lorentz (L:LorentzGrp) (f:Spacetime→E) (p:Spacetime) :
    (𝓕⁻ (f∘(action L).symm)) ((2*Real.pi)⁻¹ • metricFlip p)=
      (𝓕⁻ f) ((2*Real.pi)⁻¹ • metricFlip ((action L).symm p)) := by
  rw [angular_inverse_integral,angular_inverse_integral]
  rw [←(action_measurePreserving L).integral_comp
    (action L).toHomeomorph.measurableEmbedding]
  apply integral_congr_ae
  apply ae_of_all
  intro x
  simp only [Function.comp_apply,ContinuousLinearEquiv.symm_apply_apply,pairing_transfer]

end F1Fecho.SpacetimeLorentz
#print axioms F1Fecho.SpacetimeLorentz.lorentzEquiv
#print axioms F1Fecho.SpacetimeLorentz.action_measurePreserving
#print axioms F1Fecho.SpacetimeLorentz.pairing_transfer
#print axioms F1Fecho.SpacetimeLorentz.angular_inverse_lorentz
