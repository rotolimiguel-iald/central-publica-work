import TGLExt.V350StrongOperatorIntegral
import TGLExt.V350L2OperatorLift

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 700000

namespace TGLV350.Regular
open MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The same bounded strongly continuous data used for integration also define
a spatial operator field. Only strong continuity, not norm continuity, is used. -/
theorem operatorField_jointly_continuous (F : StrongIntegral.Family (H := H)) :
    Continuous (fun p : H × ℝ => F.op p.2 p.1) := by
  apply continuous_prod_of_continuous_lipschitzWith _
    (⟨F.bound,F.bound_nonneg⟩ : NNReal) F.continuous_apply
  intro t
  apply LipschitzWith.of_dist_le_mul
  intro v w
  rw [dist_eq_norm, ← map_sub, dist_eq_norm]
  exact (F.op t).le_of_opNorm_le (F.norm_bound t) (v-w)

theorem operatorField_memLp (F : StrongIntegral.Family (H := H)) (f : RegularHilbert H) :
    MemLp (fun x : ℝ => F.op x (f x)) 2 volume := by
  have hm := (operatorField_jointly_continuous F).comp_aestronglyMeasurable
    ((Lp.memLp f).aestronglyMeasurable.prodMk aestronglyMeasurable_id)
  exact (Lp.memLp f).of_le_mul hm (Filter.Eventually.of_forall
    (fun x => (F.op x).le_of_opNorm_le (F.norm_bound x) (f x)))

def operatorFieldLp (F : StrongIntegral.Family (H := H)) (f : RegularHilbert H) :
    RegularHilbert H := (operatorField_memLp F f).toLp (fun x => F.op x (f x))

theorem operatorFieldLp_ae (F : StrongIntegral.Family (H := H)) (f : RegularHilbert H) :
    operatorFieldLp F f =ᵐ[volume] fun x : ℝ => F.op x (f x) :=
  (operatorField_memLp F f).coeFn_toLp

def operatorFieldLinear (F : StrongIntegral.Family (H := H)) :
    RegularHilbert H →ₗ[ℂ] RegularHilbert H where
  toFun := operatorFieldLp F
  map_add' f g := by
    apply Lp.ext
    filter_upwards [operatorFieldLp_ae F (f+g), operatorFieldLp_ae F f,
      operatorFieldLp_ae F g, Lp.coeFn_add f g,
      Lp.coeFn_add (operatorFieldLp F f) (operatorFieldLp F g)] with x h1 h2 h3 h4 h5
    simp only [Pi.add_apply] at h4 h5
    rw [h1,h5,h2,h3,h4,map_add]
  map_smul' c f := by
    apply Lp.ext
    filter_upwards [operatorFieldLp_ae F (c • f), operatorFieldLp_ae F f,
      Lp.coeFn_smul c f, Lp.coeFn_smul c (operatorFieldLp F f)] with x h1 h2 h3 h4
    simp only [Pi.smul_apply] at h3 h4
    simp only [RingHom.id_apply]
    rw [h1,h4,h2,h3,map_smul]

theorem operatorFieldLp_norm_le (F : StrongIntegral.Family (H := H)) (f : RegularHilbert H) :
    ‖operatorFieldLp F f‖ ≤ F.bound * ‖f‖ := by
  apply Lp.norm_le_mul_norm_of_ae_le_mul
  filter_upwards [operatorFieldLp_ae F f] with x hx
  rw [hx]
  exact (F.op x).le_of_opNorm_le (F.norm_bound x) (f x)

def operatorFieldLift (F : StrongIntegral.Family (H := H)) :
    RegularHilbert H →L[ℂ] RegularHilbert H :=
  (operatorFieldLinear F).mkContinuous F.bound (operatorFieldLp_norm_le F)

theorem operatorFieldLift_ae (F : StrongIntegral.Family (H := H)) (f : RegularHilbert H) :
    operatorFieldLift F f =ᵐ[volume] fun x : ℝ => F.op x (f x) := operatorFieldLp_ae F f

theorem operatorFieldLift_norm_le (F : StrongIntegral.Family (H := H)) :
    ‖operatorFieldLift F‖ ≤ F.bound :=
  ContinuousLinearMap.opNorm_le_bound _ F.bound_nonneg (operatorFieldLp_norm_le F)

theorem operatorFieldLift_commutes_fibre (F : StrongIntegral.Family (H := H))
    (C : H →L[ℂ] H) (hC : ∀ x : ℝ, F.op x * C = C * F.op x) :
    operatorFieldLift F * fibre C = fibre C * operatorFieldLift F := by
  ext1 f
  apply Lp.ext
  filter_upwards [operatorFieldLift_ae F (fibre C f), fibre_ae C f,
    fibre_ae C (operatorFieldLift F f), operatorFieldLift_ae F f] with x h1 h2 h3 h4
  change operatorFieldLift F (fibre C f) x = fibre C (operatorFieldLift F f) x
  rw [h1,h2,h3,h4]
  exact congrArg (fun T : H →L[ℂ] H => T (f x)) (hC x)

#print axioms operatorField_jointly_continuous
#print axioms operatorField_memLp
#print axioms operatorFieldLinear
#print axioms operatorFieldLift
#print axioms operatorFieldLift_ae
#print axioms operatorFieldLift_norm_le
#print axioms operatorFieldLift_commutes_fibre
end
end TGLV350.Regular
