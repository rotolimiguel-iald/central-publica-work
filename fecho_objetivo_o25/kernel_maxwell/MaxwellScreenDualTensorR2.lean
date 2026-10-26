import CartesianMaxwellBivectorR6

/-! Concrete right inverse of the actual antisymmetric tensor contraction,
on the regular transverse chart. It uses components 01 and 23 of the already
constructed p-wedge-screen bivectors. No spacetime extension is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Matrix ChatgptAudit.WignerRapidityMeasure016

def screenDualTensor (q : Transverse) (v : Fin 2→ℂ) : Matrix (Fin 4) (Fin 4) ℂ :=
  let r : ℂ:=transverseMass 0 q
  !![0,v 0/r,0,0; -v 0/r,0,0,0; 0,0,0,v 1/r; 0,0,-v 1/r,0]

theorem screenDualTensor_antisymmetric (q : Transverse) (v : Fin 2→ℂ) (μ ν : Fin 4) :
    screenDualTensor q v μ ν= -screenDualTensor q v ν μ := by
  fin_cases μ <;> fin_cases ν <;> simp [screenDualTensor,neg_div]

theorem screenDualTensor_right_inverse (y : MomentumCoordinates) (hy : y.1≠0)
    (v : Fin 2→ℂ) (j : Fin 2) :
    (1/2:ℂ)*∑μ : Fin 4,∑ν : Fin 4,
      (cartesianStrength y j μ ν : ℂ)*screenDualTensor y.1 v μ ν=v j := by
  have hr : (transverseMass 0 y.1 : ℂ)≠0 := by
    exact_mod_cast (transverseMass_pos_of_ne_zero 0 y.1 hy).ne'
  fin_cases j <;>
    simp [cartesianStrength,screenDualTensor,Fin.sum_univ_succ] <;>
    field_simp [hr] <;> ring

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.screenDualTensor_antisymmetric
#print axioms F1Fecho.MaxwellGlobal.screenDualTensor_right_inverse
