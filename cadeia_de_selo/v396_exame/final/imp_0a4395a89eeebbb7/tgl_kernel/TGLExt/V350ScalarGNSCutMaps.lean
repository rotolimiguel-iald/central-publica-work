import TGLExt.V350ScalarGNSRepresentation
import TGLExt.V350L2MeasurableCut

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Measurable cuts commute with a bounded operator field on the same L² space. -/
theorem measurableCut_operatorFieldLift (S : Set ℝ) (hS : MeasurableSet S)
    (F : StrongIntegral.Family (H := H)) (f : RegularHilbert H) :
    measurableCut S hS (operatorFieldLift F f) =
      operatorFieldLift F (measurableCut S hS f) := by
  apply Lp.ext
  filter_upwards [measurableCut_ae S hS (operatorFieldLift F f),
    operatorFieldLift_ae F f, operatorFieldLift_ae F (measurableCut S hS f),
    measurableCut_ae S hS f] with x h1 h2 h3 h4
  rw [h1,h3,h4]
  by_cases hx : x ∈ S
  · simp only [Set.indicator_of_mem hx,h2]
  · simp only [Set.indicator_of_notMem hx,map_zero]

/-- Exhausting cuts are jointly injective; no individual cut is asserted faithful. -/
theorem measurableCut_nat_joint_zero (f : RegularHilbert H)
    (h : ∀ n : ℕ, measurableCut (Set.Ioc (-(n : ℝ)) (n : ℝ)) measurableSet_Ioc f = 0) :
    f = 0 := by
  have hz : ∀ n : ℕ, ∀ᵐ x : ℝ, x ∈ Set.Ioc (-(n : ℝ)) (n : ℝ) → f x = 0 := by
    intro n
    have he := measurableCut_ae (Set.Ioc (-(n : ℝ)) (n : ℝ)) measurableSet_Ioc f
    rw [h n] at he
    filter_upwards [he,Lp.coeFn_zero H 2 volume] with x hx hx0
    intro hxn
    simpa only [Set.indicator_of_mem hxn,hx0,Pi.zero_apply] using hx.symm
  apply Lp.ext
  filter_upwards [ae_all_iff.mpr hz,Lp.coeFn_zero H 2 volume] with x hx hx0
  obtain ⟨n,hn⟩ := exists_nat_gt |x|
  have hxn : x ∈ Set.Ioc (-(n : ℝ)) (n : ℝ) := by
    constructor
    · have hl := neg_abs_le x
      linarith
    · exact le_trans (le_abs_self x) hn.le
  simpa only [hx0,Pi.zero_apply] using hx n hxn

/-- A contraction from the actual scalar GNS completion into its ambient L² space.
Its identification with the bounded cut functional is a separate norm theorem. -/
def scalarGNSCutMap (P : SiteProfile) (R : ℝ) :
    ScalarGNSHilbert P →L[ℂ] RegularHilbert (RegularHilbert (TowerHilbert P)) :=
  (measurableCut (Set.Ioc (-R) R) measurableSet_Ioc).comp (scalarGNSSubspace P).subtypeL

theorem scalarGNSCutMap_norm_le (P : SiteProfile) (R : ℝ) (v : ScalarGNSHilbert P) :
    ‖scalarGNSCutMap P R v‖ ≤ ‖v‖ :=
  measurableCutLp_norm_le (Set.Ioc (-R) R) measurableSet_Ioc v.val

theorem scalarGNSCutMap_intertwines (P : SiteProfile) (R : ℝ)
    (B : (regularCoreAlgebra P).toStarSubalgebra) (v : ScalarGNSHilbert P) :
    scalarGNSCutMap P R (scalarGNSRepresentation P B v) =
      dualOrbitRepresentation B.val (scalarGNSCutMap P R v) :=
  measurableCut_operatorFieldLift (Set.Ioc (-R) R) measurableSet_Ioc
    (dualIntegralFamily B.val) v.val

theorem scalarGNSCutMap_joint_zero (P : SiteProfile) (v : ScalarGNSHilbert P)
    (h : ∀ n : ℕ, scalarGNSCutMap P (n : ℝ) v = 0) : v = 0 := by
  apply Subtype.ext
  exact measurableCut_nat_joint_zero v.val h

#print axioms measurableCut_operatorFieldLift
#print axioms measurableCut_nat_joint_zero
#print axioms scalarGNSCutMap
#print axioms scalarGNSCutMap_norm_le
#print axioms scalarGNSCutMap_intertwines
#print axioms scalarGNSCutMap_joint_zero
end
end TGLV350.Regular
