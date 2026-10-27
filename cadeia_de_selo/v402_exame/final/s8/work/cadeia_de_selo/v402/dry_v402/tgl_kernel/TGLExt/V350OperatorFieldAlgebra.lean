import TGLExt.V350StrongOperatorField

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 700000

namespace TGLV350.Regular
open MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem operatorFieldLift_constant (F : StrongIntegral.Family (H := H))
    (T : H →L[ℂ] H) (h : ∀ x, F.op x = T) :
    operatorFieldLift F = fibre T := by
  ext1 f
  apply Lp.ext
  filter_upwards [operatorFieldLift_ae F f, fibre_ae T f] with x h1 h2
  rw [h1,h2,h x]

theorem operatorFieldLift_add (F G K : StrongIntegral.Family (H := H))
    (h : ∀ x, K.op x = F.op x + G.op x) :
    operatorFieldLift K = operatorFieldLift F + operatorFieldLift G := by
  ext1 f
  apply Lp.ext
  filter_upwards [operatorFieldLift_ae K f, operatorFieldLift_ae F f,
    operatorFieldLift_ae G f, Lp.coeFn_add (operatorFieldLift F f) (operatorFieldLift G f)]
    with x h1 h2 h3 h4
  simp only [Pi.add_apply] at h4
  change operatorFieldLift K f x = (operatorFieldLift F f + operatorFieldLift G f) x
  rw [h1,h4,h2,h3,h x]
  rfl

theorem operatorFieldLift_mul (F G K : StrongIntegral.Family (H := H))
    (h : ∀ x, K.op x = F.op x * G.op x) :
    operatorFieldLift K = operatorFieldLift F * operatorFieldLift G := by
  ext1 f
  apply Lp.ext
  filter_upwards [operatorFieldLift_ae K f,
    operatorFieldLift_ae F (operatorFieldLift G f), operatorFieldLift_ae G f]
    with x h1 h2 h3
  change operatorFieldLift K f x = operatorFieldLift F (operatorFieldLift G f) x
  rw [h1,h2,h3,h x]
  rfl

theorem operatorFieldLift_smul (F G : StrongIntegral.Family (H := H)) (c : ℂ)
    (h : ∀ x, G.op x = c • F.op x) :
    operatorFieldLift G = c • operatorFieldLift F := by
  ext1 f
  apply Lp.ext
  filter_upwards [operatorFieldLift_ae G f,operatorFieldLift_ae F f,
    Lp.coeFn_smul c (operatorFieldLift F f)] with x h1 h2 h3
  simp only [Pi.smul_apply] at h3
  change operatorFieldLift G f x = (c • operatorFieldLift F f) x
  rw [h1,h3,h2,h x]
  rfl

theorem operatorFieldLift_star (F G : StrongIntegral.Family (H := H))
    (h : ∀ x, G.op x = star (F.op x)) :
    operatorFieldLift G = star (operatorFieldLift F) := by
  ext1 f
  apply ext_inner_left ℂ
  intro g
  simp only [ContinuousLinearMap.star_eq_adjoint]
  rw [ContinuousLinearMap.adjoint_inner_right]
  rw [L2.inner_def,L2.inner_def]
  apply integral_congr_ae
  filter_upwards [operatorFieldLift_ae G f,operatorFieldLift_ae F g] with x h1 h2
  rw [h1,h2,h x,ContinuousLinearMap.star_eq_adjoint,
    ContinuousLinearMap.adjoint_inner_right]

#print axioms operatorFieldLift_constant
#print axioms operatorFieldLift_add
#print axioms operatorFieldLift_mul
#print axioms operatorFieldLift_smul
#print axioms operatorFieldLift_star
end
end TGLV350.Regular
