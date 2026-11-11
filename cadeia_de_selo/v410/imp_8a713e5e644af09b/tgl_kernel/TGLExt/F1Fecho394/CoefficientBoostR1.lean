import TGLExt.F1Fecho394.RegularCovariantCoreR3
import TGLExt.V350StrongOperatorField

/-! The coefficient boost f(a) -> B_(epsilon*a) f(a) is an actual
L2 unitary. Strong continuity is sufficient; no norm-continuous boost is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open MeasureTheory
namespace F1Fecho.CoefficientBoost
open TGLV350.Regular F1Fecho.RegularCovariantCore
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (B : UnitaryFlow H) (epsilon : ℝ)

def family : TGLV350.StrongIntegral.Family (H:=H) where
  op a := boostCLM B (epsilon*a)
  continuous_apply v := (B.strong v).comp (continuous_const.mul continuous_id)
  bound := 1
  bound_nonneg := by norm_num
  norm_bound a := by
    apply ContinuousLinearMap.opNorm_le_bound _ (by norm_num : (0:ℝ)≤1)
    intro v
    change ‖B.U (epsilon*a) v‖≤1*‖v‖
    rw [(B.U (epsilon*a)).norm_map,one_mul]

def multiplier : RegularHilbert H →L[ℂ] RegularHilbert H :=
  operatorFieldLift (family B epsilon)

theorem multiplier_ae (f : RegularHilbert H) :
    multiplier B epsilon f =ᵐ[volume] fun a => B.U (epsilon*a) (f a) :=
  operatorFieldLift_ae (family B epsilon) f

theorem multiplier_norm (f : RegularHilbert H) : ‖multiplier B epsilon f‖=‖f‖ := by
  rw [Lp.norm_def,Lp.norm_def]
  congr 1
  apply eLpNorm_congr_norm_ae
  filter_upwards [multiplier_ae B epsilon f] with a ha
  rw [ha,(B.U (epsilon*a)).norm_map]

theorem multiplier_inverse (f : RegularHilbert H) :
    multiplier B (-epsilon) (multiplier B epsilon f)=f := by
  apply Lp.ext
  filter_upwards [multiplier_ae B (-epsilon) (multiplier B epsilon f),
    multiplier_ae B epsilon f] with a ha hb
  rw [ha,hb]
  have h := congrArg (fun U : H≃ₗᵢ[ℂ]H => U (f a)) (B.add (-epsilon*a) (epsilon*a))
  simp only [LinearIsometryEquiv.trans_apply] at h
  rw [show -epsilon*a+epsilon*a=0 by ring,B.zero] at h
  exact h.symm

def unitary : RegularHilbert H ≃ₗᵢ[ℂ] RegularHilbert H where
  toFun := multiplier B epsilon
  map_add' := (multiplier B epsilon).map_add
  map_smul' := (multiplier B epsilon).map_smul
  norm_map' := multiplier_norm B epsilon
  invFun := multiplier B (-epsilon)
  left_inv := multiplier_inverse B epsilon
  right_inv f := by simpa only [neg_neg] using multiplier_inverse B (-epsilon) f

theorem unitary_ae (f : RegularHilbert H) :
    unitary B epsilon f =ᵐ[volume] fun a => B.U (epsilon*a) (f a) := multiplier_ae B epsilon f

theorem multiplier_commutes_fibre (A : H→L[ℂ]H)
    (hA : ∀ a, boostCLM B a*A=A*boostCLM B a) :
    multiplier B epsilon*fibre A=fibre A*multiplier B epsilon :=
  operatorFieldLift_commutes_fibre (family B epsilon) A (fun a => hA (epsilon*a))

end F1Fecho.CoefficientBoost
#print axioms F1Fecho.CoefficientBoost.multiplier_norm
#print axioms F1Fecho.CoefficientBoost.multiplier_inverse
#print axioms F1Fecho.CoefficientBoost.unitary
#print axioms F1Fecho.CoefficientBoost.unitary_ae
#print axioms F1Fecho.CoefficientBoost.multiplier_commutes_fibre
