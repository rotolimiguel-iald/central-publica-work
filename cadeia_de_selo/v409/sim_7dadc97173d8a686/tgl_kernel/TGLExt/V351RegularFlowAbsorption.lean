import TGLExt.V350OperatorFieldAlgebra
import TGLExt.V350RegularTowerRepresentation

set_option autoImplicit false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit MeasureTheory Filter
noncomputable section

/-- A bounded operator field from the existing tower flow. The real argument
a indexes field composition; the absorption unitary below uses a=1. -/
def regularFlowField (P : SiteProfile) (a : ℝ) :
    StrongIntegral.Family (H := TowerHilbert P) where
  op x := modularFlowCLM P (a*x)
  continuous_apply v := (modularFlow_strongly_continuous v).comp (continuous_const.mul continuous_id)
  bound := 1
  bound_nonneg := zero_le_one
  norm_bound x := by
    apply ContinuousLinearMap.opNorm_le_bound _ zero_le_one
    intro v
    change ‖(modularFlowIsometry P (a*x)) v‖ ≤ 1*‖v‖
    rw [(modularFlowIsometry P (a*x)).norm_map, one_mul]

theorem regularFlowField_lift_star (P : SiteProfile) (a : ℝ) :
    star (operatorFieldLift (regularFlowField P a)) =
      operatorFieldLift (regularFlowField P (-a)) := by
  symm
  apply operatorFieldLift_star
  intro x
  change modularFlowCLM P ((-a)*x) = star (modularFlowCLM P (a*x))
  rw [modularFlowCLM_star, neg_mul]

theorem regularFlowField_lift_mul (P : SiteProfile) (a b : ℝ) :
    operatorFieldLift (regularFlowField P a) * operatorFieldLift (regularFlowField P b) =
      operatorFieldLift (regularFlowField P (a+b)) := by
  symm
  apply operatorFieldLift_mul
  intro x
  change modularFlowCLM P ((a+b)*x) = modularFlowCLM P (a*x) * modularFlowCLM P (b*x)
  rw [modularFlowCLM_mul, add_mul]

theorem regularFlowField_lift_zero (P : SiteProfile) :
    operatorFieldLift (regularFlowField P 0) = 1 := by
  have h := operatorFieldLift_constant (regularFlowField P 0) 1
    (fun x => by change modularFlowCLM P (0*x) = 1; rw [zero_mul, modularFlowCLM_zero])
  exact h.trans fibre_one

/-- A concrete unitary on the regular Hilbert space; no membership in the
regular core is asserted. It is the field x ↦ Delta_base^(ix). -/
def regularFlowAbsorptionUnitary (P : SiteProfile) :
    unitary (RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) :=
  ⟨operatorFieldLift (regularFlowField P 1), by
    rw [Unitary.mem_iff]
    constructor <;> simp only [regularFlowField_lift_star, regularFlowField_lift_mul,
      neg_add_cancel, add_neg_cancel, regularFlowField_lift_zero]⟩

/-- The whole regular unitary group is conjugate to the actual L² translation
group. This consumes the existing operator-field lift and the same tower flow. -/
theorem regularUnitary_shift_conjugate (P : SiteProfile) (t : ℝ) :
    (regularFlowAbsorptionUnitary P).val * shift t *
        star (regularFlowAbsorptionUnitary P).val = regularUnitary P t := by
  change operatorFieldLift (regularFlowField P 1) * shift t *
      star (operatorFieldLift (regularFlowField P 1)) = _
  rw [regularFlowField_lift_star]
  apply ContinuousLinearMap.ext
  intro f
  apply Lp.ext
  filter_upwards [operatorFieldLift_ae (regularFlowField P 1)
      (shift t (operatorFieldLift (regularFlowField P (-1)) f)),
    shift_ae t (operatorFieldLift (regularFlowField P (-1)) f),
    (measurePreserving_sub_right volume t).quasiMeasurePreserving.ae
      (operatorFieldLift_ae (regularFlowField P (-1)) f),
    fibre_ae (modularFlowCLM P t) (shift t f), shift_ae t f] with x h1 h2 h3 h4 h5
  change operatorFieldLift (regularFlowField P 1)
      (shift t (operatorFieldLift (regularFlowField P (-1)) f)) x =
    fibre (modularFlowCLM P t) (shift t f) x
  rw [h1, h2, h3, h4, h5]
  change modularFlowCLM P (1*x) (modularFlowCLM P ((-1)*(x-t)) (f (x-t))) =
    modularFlowCLM P t (f (x-t))
  rw [← mul_apply_eq_comp, modularFlowCLM_mul]
  congr 2
  ring

#print axioms regularFlowField
#print axioms regularFlowField_lift_star
#print axioms regularFlowField_lift_mul
#print axioms regularFlowField_lift_zero
#print axioms regularFlowAbsorptionUnitary
#print axioms regularUnitary_shift_conjugate
end
end TGLV350.Regular
