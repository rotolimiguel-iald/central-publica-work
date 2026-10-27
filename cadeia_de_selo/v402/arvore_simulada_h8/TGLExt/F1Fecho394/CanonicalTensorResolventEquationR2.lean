import TGLExt.F1Fecho394.CanonicalTensorMultiplierR3
import TGLExt.F1Fecho394.BoundedPairResolventEquationR2
import TGLExt.F1Fecho394.CanonicalFockGraphRealizationR3
/-! Component equation for the actual resolvent on the unchanged Fock space.
The component projection is not assumed to commute with the resolvent. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter
namespace F1Fecho.TensorCoordinates
open F1Rede.BosonicSectors F1Rede.BosonicFock F1Rede.CanonicalWedge
open F1Fecho.GammaGraph F1Fecho.CanonicalFockPolar F1Fecho.ExponentialLift

def Q (n:ℕ) : F→L[ℂ]Space n :=
  (coordinates n).toLinearIsometry.toContinuousLinearMap.comp
    ((symmetricSpace (n+1)).subtypeL.comp (lp.evalCLM ℂ Sectors 2 (n+1)))

lemma Q_apply (n:ℕ) (x:F) : Q n x=coordinates n (x (n+1):TensorHilbert (n+1)) := rfl

def aMultiplier (n:ℕ) : Space n→L[ℂ]Space n :=
  productMultiplier (weightA rootParameter) (weightA_measurable rootParameter)
    (weightA_bound rootParameter) n

def bMultiplier (n:ℕ) : Space n→L[ℂ]Space n :=
  productMultiplier (weightB rootParameter) (weightB_measurable rootParameter)
    (weightB_bound rootParameter) n

lemma Q_GA (n:ℕ) (x:F) : Q n (GA x)=aMultiplier n (Q n x) :=
  sector_WA rootParameter n (x (n+1))
lemma Q_GB (n:ℕ) (x:F) : Q n (GB x)=bMultiplier n (Q n x) :=
  sector_WB rootParameter n (x (n+1))

theorem Q_resolvent_equation (n:ℕ) (x:F) :
    aMultiplier n (aMultiplier n (Q n (modularR x)))+
      bMultiplier n (bMultiplier n (Q n (modularR x)))=
      aMultiplier n (aMultiplier n (Q n x)) := by
  have h:=congrArg (fun A:F→L[ℂ]F=>Q n (A x))
    (BoundedPairResolvent.equation canonicalLift canonicalLift_selfadjoint GA GB
      GA_selfadjoint GB_selfadjoint graph_parameters GAB_commute)
  change Q n (GA (GA (modularR x))+GB (GB (modularR x)))=Q n (GA (GA x)) at h
  simpa only [map_add,Q_GA,Q_GB] using h

theorem Q_resolvent_equation_ae (n:ℕ) (x:F) :
    (fun p=>(productWeight (weightA rootParameter) n p*productWeight (weightA rootParameter) n p+
      productWeight (weightB rootParameter) n p*productWeight (weightB rootParameter) n p)•
        Q n (modularR x) p)=ᵐ[(data n).measure]
      fun p=>(productWeight (weightA rootParameter) n p*productWeight (weightA rootParameter) n p)•
        Q n x p := by
  have h:=Q_resolvent_equation n x
  let y:=Q n (modularR x)
  let z:=Q n x
  have ha (v:Space n):aMultiplier n v=ᵐ[(data n).measure]
      fun p=>productWeight (weightA rootParameter) n p•v p := productMultiplier_ae _ _ _ _ _
  have hb (v:Space n):bMultiplier n v=ᵐ[(data n).measure]
      fun p=>productWeight (weightB rootParameter) n p•v p := productMultiplier_ae _ _ _ _ _
  filter_upwards [ha y,ha (aMultiplier n y),hb y,hb (bMultiplier n y),
    ha z,ha (aMultiplier n z),Lp.coeFn_add (aMultiplier n (aMultiplier n y))
      (bMultiplier n (bMultiplier n y))] with p ha1 ha2 hb1 hb2 hz1 hz2 hs
  have he:=congrArg (fun v:Space n=>v p) h
  change (aMultiplier n (aMultiplier n y)+bMultiplier n (bMultiplier n y)) p=
    aMultiplier n (aMultiplier n z) p at he
  rw [hs,Pi.add_apply,ha2,hb2,hz2,ha1,hb1,hz1] at he
  simpa only [smul_smul,add_smul] using he

end F1Fecho.TensorCoordinates
#print axioms F1Fecho.TensorCoordinates.Q_resolvent_equation
#print axioms F1Fecho.TensorCoordinates.Q_resolvent_equation_ae
