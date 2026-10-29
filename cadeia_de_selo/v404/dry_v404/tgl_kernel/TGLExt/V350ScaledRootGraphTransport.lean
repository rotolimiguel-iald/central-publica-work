import TGLExt.V350ScaledResolventRoots

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open ChatgptAudit.Continuous049
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem unit_operator_surjective (F : H →L[ℂ] H) (hF : IsUnit F) :
    Function.Surjective F := by
  intro z
  refine ⟨Ring.inverse F z,?_⟩
  have hh := congrArg (fun C : H →L[ℂ] H => C z) (Ring.mul_inverse_cancel F hF)
  exact hh

theorem complement_intertwines (A B U : H →L[ℂ] H) (h : A*U=U*B) :
    (1-A)*U=U*(1-B) := by
  simp only [sub_mul,mul_sub,one_mul,mul_one,h]

/-- Scaling is transported to the actual bounded-pair graph. No boundedness,
surjectivity or inverse is assumed for the unbounded root itself. -/
theorem resolvent_root_graph_scaled (T U : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (hi : Function.Injective T)
    (r : ℝ) (hr : 0 < r)
    (hU : T*U=U*scaledPositiveResolvent T r)
    (x y : H) (hxy : (x,y) ∈ (resolventSquareRoot T hT hi).graph) :
    (U x,Real.sqrt r • U y) ∈ (resolventSquareRoot T hT hi).graph := by
  let E := Ring.inverse (scaledResolventDenominator T r)
  have hd := scaledResolventDenominator_positive T hT h1 r hr
  have he : IsStrictlyPositive E := hd.ringInverse
  obtain ⟨z,hx,hy⟩ := (bounded_graph_param_iff (CFC.sqrt T) (CFC.sqrt (1-T))
    (positive_sqrt_injective T hT hi) x y).mp hxy
  obtain ⟨w,hw⟩ := unit_operator_surjective (CFC.sqrt E) he.sqrt.isUnit z
  have hfirst : CFC.sqrt (scaledPositiveResolvent T r) w=x := by
    rw [scaledResolvent_root_pair_first T hT h1 r hr]
    change CFC.sqrt T (CFC.sqrt E w)=x
    rw [hw]
    exact hx
  have hsecond : CFC.sqrt (1-scaledPositiveResolvent T r) w=Real.sqrt r • y := by
    rw [scaledResolvent_root_pair_second T hT h1 r hr]
    change Real.sqrt r • (CFC.sqrt (1-T) (CFC.sqrt E w))=Real.sqrt r • y
    rw [hw,hy]
  have hq := scaledPositiveResolvent_nonneg T hT h1 r hr
  have hq1 := scaledPositiveResolvent_le_one T hT h1 r hr
  have hS := congrArg (fun F : H →L[ℂ] H => F w)
    (positive_sqrt_intertwines T (scaledPositiveResolvent T r) U hT hq hU)
  have hC := congrArg (fun F : H →L[ℂ] H => F w)
    (positive_sqrt_intertwines (1-T) (1-scaledPositiveResolvent T r) U
      (sub_nonneg.mpr h1) (sub_nonneg.mpr hq1) (complement_intertwines T _ U hU))
  apply (bounded_graph_param_iff (CFC.sqrt T) (CFC.sqrt (1-T))
    (positive_sqrt_injective T hT hi) _ _).mpr
  refine ⟨U w,?_,?_⟩
  · exact hS.trans (congrArg U hfirst)
  · calc
      _ = U (CFC.sqrt (1-scaledPositiveResolvent T r) w) := hC
      _ = U (Real.sqrt r • y) := congrArg U hsecond
      _ = _ := U.map_smul_of_tower (Real.sqrt r) y

#print axioms unit_operator_surjective
#print axioms complement_intertwines
#print axioms resolvent_root_graph_scaled
end
end TGLV350.Regular
