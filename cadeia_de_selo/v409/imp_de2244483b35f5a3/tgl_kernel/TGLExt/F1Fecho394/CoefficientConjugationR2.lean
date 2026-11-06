import TGLExt.V350L2OperatorLift
import TGLExt.GenericAntilinearAdjoint

/-! Pointwise antiunitary and argument reflection on Lebesgue L2.
Both operations are constructed on equivalence classes, with a.e. formulas. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
open MeasureTheory
namespace F1Fecho.CoefficientConjugation
open TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def liftMap (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
    RegularHilbert H →ₛₗᵢ[starRingEnd ℂ] RegularHilbert H where
  toLinearMap := (J.toLinearIsometry.toContinuousLinearMap.compLpL 2 volume).toLinearMap
  norm_map' f := by
    rw [Lp.norm_def,Lp.norm_def]
    congr 1
    apply eLpNorm_congr_norm_ae
    filter_upwards [J.toLinearIsometry.toContinuousLinearMap.coeFn_compLpL f] with a ha
    change ‖(J.toLinearIsometry.toContinuousLinearMap.compLpL 2 volume f) a‖=‖f a‖
    rw [ha]
    exact J.norm_map (f a)

theorem liftMap_ae (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (f : RegularHilbert H) :
    liftMap J f =ᵐ[volume] fun a => J (f a) :=
  J.toLinearIsometry.toContinuousLinearMap.coeFn_compLpL f

theorem liftMap_inverse (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (f : RegularHilbert H) :
    liftMap J.symm (liftMap J f)=f := by
  apply Lp.ext
  filter_upwards [liftMap_ae J.symm (liftMap J f),liftMap_ae J f] with a ha hb
  rw [ha,hb,LinearIsometryEquiv.symm_apply_apply]

def lift (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
    RegularHilbert H ≃ₛₗᵢ[starRingEnd ℂ] RegularHilbert H where
  toFun := liftMap J
  map_add' := (liftMap J).map_add
  map_smul' := (liftMap J).map_smulₛₗ
  norm_map' := (liftMap J).norm_map
  invFun := liftMap J.symm
  left_inv := liftMap_inverse J
  right_inv := liftMap_inverse J.symm

theorem lift_ae (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (f : RegularHilbert H) :
    lift J f =ᵐ[volume] fun a => J (f a) := liftMap_ae J f

theorem lift_involutive (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive J) :
    Function.Involutive (lift J) := by
  intro f
  apply Lp.ext
  filter_upwards [lift_ae J (lift J f),lift_ae J f] with a ha hb
  rw [ha,hb,hJ]

def reflectionMap : RegularHilbert H →ₗᵢ[ℂ] RegularHilbert H :=
  Lp.compMeasurePreservingₗᵢ ℂ (fun a : ℝ => -a) (Measure.measurePreserving_neg volume)

theorem reflectionMap_ae (f : RegularHilbert H) :
    reflectionMap f =ᵐ[volume] fun a : ℝ => f (-a) :=
  Lp.coeFn_compMeasurePreserving f (Measure.measurePreserving_neg volume)

theorem reflectionMap_involutive : Function.Involutive (reflectionMap (H:=H)) := by
  intro f
  have h := Lp.compMeasurePreserving_comp_apply f
    (Measure.measurePreserving_neg (volume : Measure ℝ))
    (Measure.measurePreserving_neg (volume : Measure ℝ))
  have hi : (fun a : ℝ => -a) ∘ (fun a : ℝ => -a)=id := by funext a; simp
  change Lp.compMeasurePreserving (fun a : ℝ => -a) _
    (Lp.compMeasurePreserving (fun a : ℝ => -a) _ f)=f
  simpa only [hi,Lp.compMeasurePreserving_id_apply] using h.symm

def reflection : RegularHilbert H ≃ₗᵢ[ℂ] RegularHilbert H where
  toFun := reflectionMap
  map_add' := reflectionMap.map_add
  map_smul' := reflectionMap.map_smul
  norm_map' := reflectionMap.norm_map
  invFun := reflectionMap
  left_inv := reflectionMap_involutive
  right_inv := reflectionMap_involutive

theorem reflection_fibre (A : H →L[ℂ] H) (f : RegularHilbert H) :
    reflection (fibre A f)=fibre A (reflection f) := by
  apply Lp.ext
  have hpre := (Measure.measurePreserving_neg (volume : Measure ℝ)).quasiMeasurePreserving.ae
    (fibre_ae A f)
  filter_upwards [reflectionMap_ae (fibre A f),hpre,
    fibre_ae A (reflection f),reflectionMap_ae f] with a ha hb hc hd
  change reflectionMap (fibre A f) a = fibre A (reflection f) a
  rw [ha,hb,hc]
  change A (f (-a))=A (reflectionMap f a)
  rw [hd]

theorem reflection_lift (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (f : RegularHilbert H) :
    reflection (lift J f)=lift J (reflection f) := by
  apply Lp.ext
  have hpre := (Measure.measurePreserving_neg (volume : Measure ℝ)).quasiMeasurePreserving.ae (lift_ae J f)
  filter_upwards [reflectionMap_ae (lift J f),hpre,lift_ae J (reflection f),
    reflectionMap_ae f] with a ha hb hc hd
  change reflectionMap (lift J f) a = lift J (reflection f) a
  rw [ha,hb,hc]
  change J (f (-a))=J (reflectionMap f a)
  rw [hd]

end F1Fecho.CoefficientConjugation
#print axioms F1Fecho.CoefficientConjugation.lift
#print axioms F1Fecho.CoefficientConjugation.lift_involutive
#print axioms F1Fecho.CoefficientConjugation.reflectionMap_involutive
#print axioms F1Fecho.CoefficientConjugation.reflection_fibre
#print axioms F1Fecho.CoefficientConjugation.reflection_lift
