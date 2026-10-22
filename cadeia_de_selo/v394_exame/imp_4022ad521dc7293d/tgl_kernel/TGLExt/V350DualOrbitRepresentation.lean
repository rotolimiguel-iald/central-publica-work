import TGLExt.V350OperatorFieldAlgebra
import TGLExt.V350DualWeightCuts

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The bounded dual field is a genuine unital star representation on the
outer L² space, independently of any choice of finite-weight domain. -/
def dualOrbitRepresentation : (RegularHilbert H →L[ℂ] RegularHilbert H) →⋆ₐ[ℂ]
    (RegularHilbert (RegularHilbert H) →L[ℂ] RegularHilbert (RegularHilbert H)) where
  toFun A := operatorFieldLift (dualIntegralFamily A)
  map_one' := by
    rw [operatorFieldLift_constant (dualIntegralFamily 1) 1 (fun s => map_one (dualAmbient s))]
    exact fibre_one
  map_mul' A B := operatorFieldLift_mul _ _ _ (fun s => map_mul (dualAmbient s) A B)
  map_zero' := by
    rw [operatorFieldLift_constant (dualIntegralFamily 0) 0 (fun s => map_zero (dualAmbient s))]
    exact map_zero fibreRepresentation
  map_add' A B := operatorFieldLift_add _ _ _ (fun s => map_add (dualAmbient s) A B)
  commutes' c := by
    change operatorFieldLift (dualIntegralFamily (c • 1)) = c • 1
    rw [operatorFieldLift_smul (dualIntegralFamily 1) (dualIntegralFamily (c • 1)) c
      (fun s => map_smul (dualAmbient s) c 1)]
    rw [operatorFieldLift_constant (dualIntegralFamily 1) 1 (fun s => map_one (dualAmbient s)),
      fibre_one]
  map_star' A := operatorFieldLift_star _ _ (fun s => map_star (dualAmbient s) A)

theorem dualOrbitRepresentation_scalar_apply (c : ℂ)
    (v : RegularHilbert (RegularHilbert H)) :
    dualOrbitRepresentation (c • (1 : RegularHilbert H →L[ℂ] _)) v = c • v := by
  rw [map_smul,map_one]
  rfl

#print axioms dualOrbitRepresentation
#print axioms dualOrbitRepresentation_scalar_apply
end
end TGLV350.Regular
