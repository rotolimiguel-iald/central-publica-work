import TGLExt.V350DualFixedCore
import TGLExt.V350ResolventGraphTransport

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open Filter
open scoped Topology ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem range_closure_maps_of_commute (R U : H →L[ℂ] H) (h : Commute R U)
    (v : H) (hv : v ∈ R.range.topologicalClosure) :
    U v ∈ R.range.topologicalClosure := by
  have hc : IsClosed {x : H | U x ∈ R.range.topologicalClosure} :=
    R.range.isClosed_topologicalClosure.preimage U.continuous
  apply (hc.closure_subset_iff.mpr ?_) hv
  rintro _ ⟨w,rfl⟩
  have he : U (R w) = R (U w) :=
    (congrArg (fun T : H →L[ℂ] H => T w) h.eq).symm
  change U (R w) ∈ R.range.topologicalClosure
  rw [he]
  exact Submodule.le_topologicalClosure R.range ⟨U w,rfl⟩

theorem dualSupport_maps_of_commute
    (A R U : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (h : Commute R U) (v : RegularHilbert H) (hv : v ∈ dualFormSupport A hA) :
    U v ∈ dualFormSupport A hA := by
  have he := dualResolvent_range_closure_eq_finiteDomain_closure A R hA hR hlim
  change U v ∈ (dualClosedPositiveForm A hA).finiteDomain.topologicalClosure
  rw [← he]
  apply range_closure_maps_of_commute R U h v
  rwa [he]

def dualSupportCommutingMap
    (A R U : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (h : Commute R U) : dualFormSupport A hA →L[ℂ] dualFormSupport A hA :=
  U.restrict (dualSupport_maps_of_commute A R U hA hR hlim h)

theorem dualSupportCommutingMap_apply
    (A R U : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (h : Commute R U) (v : dualFormSupport A hA) :
    (dualSupportCommutingMap A R U hA hR hlim h v : RegularHilbert H) = U v := rfl

theorem dualSupportResolvent_commutes_map
    (A R U : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (h : Commute R U) : Commute (dualSupportResolvent A R hA hlim)
      (dualSupportCommutingMap A R U hA hR hlim h) := by
  apply ContinuousLinearMap.ext
  intro v
  apply Subtype.ext
  exact congrArg (fun T : RegularHilbert H →L[ℂ] RegularHilbert H => T v) h.eq

theorem dualSupportOperator_graph_transport
    (A R U : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (h : Commute R U) (x y : dualFormSupport A hA)
    (hxy : (x,y) ∈ (dualSupportOperator A R hA hR hlim).graph) :
    (dualSupportCommutingMap A R U hA hR hlim h x,
      dualSupportCommutingMap A R U hA hR hlim h y) ∈
      (dualSupportOperator A R hA hR hlim).graph :=
  resolvent_graph_transport_of_commute _ _ _
    (dualSupportResolvent_commutes_map A R U hA hR hlim h) x y hxy

theorem dualSupportSquareRoot_graph_transport
    (A R U : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (h : Commute R U) (x y : dualFormSupport A hA)
    (hxy : (x,y) ∈ (dualSupportSquareRoot A R hA hR hlim).graph) :
    (dualSupportCommutingMap A R U hA hR hlim h x,
      dualSupportCommutingMap A R U hA hR hlim h y) ∈
      (dualSupportSquareRoot A R hA hR hlim).graph :=
  resolvent_sqrt_graph_transport_of_commute _ _ _ _
    (dualSupportResolvent_commutes_map A R U hA hR hlim h) x y hxy

#print axioms range_closure_maps_of_commute
#print axioms dualSupport_maps_of_commute
#print axioms dualSupportCommutingMap
#print axioms dualSupportCommutingMap_apply
#print axioms dualSupportResolvent_commutes_map
#print axioms dualSupportOperator_graph_transport
#print axioms dualSupportSquareRoot_graph_transport
end
end TGLV350.Regular
