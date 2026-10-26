import TGLExt.V350StrongOperatorField
import TGLExt.V350L2Translation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 700000

namespace TGLV350.Regular
open MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- L2 action determines a strongly continuous operator field pointwise.
For each fixed vector only countably many interval tests are combined ae. -/
theorem continuous_operator_action_eq_of_L2_tests
    (F G : ℝ → (H →L[ℂ] H))
    (hF : ∀ v : H, Continuous (fun x : ℝ => F x v))
    (hG : ∀ v : H, Continuous (fun x : ℝ => G x v))
    (htests : ∀ f : RegularHilbert H, (fun x : ℝ => F x (f x)) =ᵐ[volume]
      (fun x : ℝ => G x (f x))) : ∀ x : ℝ, F x = G x := by
  intro x
  ext v
  have hlocal : ∀ n : ℤ, ∀ᵐ y : ℝ ∂volume,
      y-(n : ℝ) ∈ Set.Ioc (0 : ℝ) 1 → F y v = G y v := by
    intro n
    let f : RegularHilbert H := shift (n : ℝ) (testVector v)
    have hv := (measurePreserving_sub_right volume (n : ℝ)).quasiMeasurePreserving.ae
      (indicatorConstLp_coeFn (p := (2 : ENNReal))
        (hs := measurableSet_Ioc (a := (0 : ℝ)) (b := 1)) (hμs := by simp) (c := v))
    filter_upwards [htests f, shift_ae (n : ℝ) (testVector v), hv] with y htest hshift hind
    intro hy
    have he : f y = v := hshift.trans (hind.trans (Set.indicator_of_mem hy _))
    simpa only [he] using htest
  have hall : ∀ᵐ y : ℝ ∂volume, ∀ n : ℤ,
      y-(n : ℝ) ∈ Set.Ioc (0 : ℝ) 1 → F y v = G y v := ae_all_iff.mpr hlocal
  have hae : (fun y : ℝ => F y v) =ᵐ[volume] fun y : ℝ => G y v := by
    filter_upwards [hall] with y hy
    apply hy (Int.ceil y - 1)
    have hlo := Int.ceil_lt_add_one y
    have hhi := Int.le_ceil y
    constructor <;> push_cast <;> linarith
  exact congrFun (((hF v).ae_eq_iff_eq volume (hG v)).mp hae) x

theorem operatorFieldLift_faithful (F G : StrongIntegral.Family (H := H))
    (he : operatorFieldLift F = operatorFieldLift G) : ∀ x : ℝ, F.op x = G.op x := by
  apply continuous_operator_action_eq_of_L2_tests F.op G.op F.continuous_apply G.continuous_apply
  intro f
  filter_upwards [operatorFieldLift_ae F f, operatorFieldLift_ae G f] with x hF hG
  have hx := congrArg (fun T : RegularHilbert H →L[ℂ] RegularHilbert H => T f x) he
  rw [hF,hG] at hx
  exact hx

/-- Commutation of a continuous field lift with a constant amplification
reflects pointwise commutation on the original Hilbert space. -/
theorem operatorFieldLift_commutation_reflects (F : StrongIntegral.Family (H := H))
    (C : H →L[ℂ] H)
    (he : operatorFieldLift F * fibre C = fibre C * operatorFieldLift F) :
    ∀ x : ℝ, F.op x * C = C * F.op x := by
  apply continuous_operator_action_eq_of_L2_tests
    (fun x => F.op x * C) (fun x => C * F.op x)
    (fun v => F.continuous_apply (C v))
    (fun v => C.continuous.comp (F.continuous_apply v))
  intro f
  filter_upwards [operatorFieldLift_ae F (fibre C f), fibre_ae C f,
    fibre_ae C (operatorFieldLift F f), operatorFieldLift_ae F f] with x h1 h2 h3 h4
  have hx := congrArg (fun T : RegularHilbert H →L[ℂ] RegularHilbert H => T f x) he
  change operatorFieldLift F (fibre C f) x = fibre C (operatorFieldLift F f) x at hx
  rw [h1,h2,h3,h4] at hx
  exact hx

#print axioms continuous_operator_action_eq_of_L2_tests
#print axioms operatorFieldLift_faithful
#print axioms operatorFieldLift_commutation_reflects
end
end TGLV350.Regular
