import TGLExt.F1Fecho394.RealLpGraphCoreR3

/-! Closed subspace valued L2 functions are approximated by interval vectors
with values in any dense subset of the closed subspace. This is a graph-core
lemma when the subspace is an actual closed real Tomita graph. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
open MeasureTheory
namespace F1Fecho.LpClosedSubspaceCore
open RealLpGraphCore
variable {E:Type} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

theorem lift_interval (A:E→L[ℝ]E) (a b:ℝ) (v:E) :
    A.compLpL 2 (volume:Measure ℝ) (intervalVector a b v)=intervalVector a b (A v) := by
  apply Lp.ext
  filter_upwards [A.coeFn_compLpL (intervalVector a b v),
    indicatorConstLp_coeFn (p:=2) (hs:=measurableSet_Ioc)
      (hμs:=by simp [Real.volume_Ioc]) (c:=v),
    indicatorConstLp_coeFn (p:=2) (hs:=measurableSet_Ioc)
      (hμs:=by simp [Real.volume_Ioc]) (c:=A v)] with t ht hv hw
  change intervalVector a b v t = _ at hv
  change intervalVector a b (A v) t = _ at hw
  rw [ht,hv,hw]
  by_cases h:t∈Set.Ioc a b
  · simp only [Set.indicator_of_mem h]
  · simp only [Set.indicator_of_notMem h,map_zero]

theorem mem_of_intervals (G:Submodule ℝ E) [G.HasOrthogonalProjection]
    (N:Submodule ℝ (Lp E 2 (volume:Measure ℝ)))
    (hN:IsClosed (N:Set (Lp E 2 (volume:Measure ℝ))))
    (hi:∀ a b v,v∈G→intervalVector a b v∈N)
    (f:Lp E 2 (volume:Measure ℝ)) (hf:∀ᵐ t:ℝ ∂volume,f t∈G) : f∈N := by
  let P:=G.starProjection.compLpL 2 (volume:Measure ℝ)
  have he : N.comap P.toLinearMap=⊤ := by
    apply closed_submodule_eq_top
    · exact hN.preimage P.continuous
    · intro a b v
      change P (intervalVector a b v)∈N
      change G.starProjection.compLpL 2 volume (intervalVector a b v)∈N
      rw [lift_interval]
      apply hi
      exact (G.orthogonalProjectionOnto v).property
  have hp : P f=f := by
    apply Lp.ext
    filter_upwards [G.starProjection.coeFn_compLpL f,hf] with t ht hg
    exact ht.trans (G.starProjection_eq_self_iff.mpr hg)
  have hm : f∈N.comap P.toLinearMap := by rw [he]; trivial
  change P f∈N at hm
  rwa [hp] at hm

theorem mem_of_dense_interval_values (G:Submodule ℝ E) [G.HasOrthogonalProjection]
    (D:Set E) (hD:closure D=(G:Set E))
    (N:Submodule ℝ (Lp E 2 (volume:Measure ℝ)))
    (hN:IsClosed (N:Set (Lp E 2 (volume:Measure ℝ))))
    (hi:∀ a b v,v∈D→intervalVector a b v∈N)
    (f:Lp E 2 (volume:Measure ℝ)) (hf:∀ᵐ t:ℝ ∂volume,f t∈G) : f∈N := by
  apply mem_of_intervals G N hN ?_ f hf
  intro a b v hv
  have hc:IsClosed {v:E|intervalVector a b v∈N}:=hN.preimage (intervalVector_continuous a b)
  apply closure_minimal (fun v hv=>hi a b v hv) hc
  rwa [hD]

end F1Fecho.LpClosedSubspaceCore
#print axioms F1Fecho.LpClosedSubspaceCore.lift_interval
#print axioms F1Fecho.LpClosedSubspaceCore.mem_of_intervals
#print axioms F1Fecho.LpClosedSubspaceCore.mem_of_dense_interval_values
