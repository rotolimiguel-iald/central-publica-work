import TGLExt.V350ScalarWeightStarCore

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory Filter
open scoped Topology ENNReal
noncomputable section

theorem scalarWeightGNSEmbedding_sandwich_uniform (P : SiteProfile)
    (A : scalarWeightLeftIdeal P) (h : ℝ) (hh : 0 < h) :
    scalarWeightGNSEmbedding P (scalarWeightSandwich P A h) =
      scalarGNSStarEmbedding P ⟨regularSandwich P A.val h,
        regularSandwich_mem_finiteDualStarCore P A.val h hh⟩ := by
  change _ = scalarGNSEmbedding P ⟨regularSandwich P A.val h,
    (regularSandwich_mem_finiteDualStarCore P A.val h hh).1⟩
  rw [← scalarWeightGNSEmbedding_uniform]
  apply congrArg (scalarWeightGNSEmbedding P)
  exact Subtype.ext (scalarWeightSandwich_val P A h)

/-- Both coordinates of the full-weight star graph are approximated by the
same uniform-star-core sandwich, in the GNS product topology. -/
theorem scalarWeightTomitaGraph_subset_closure_original (P : SiteProfile) :
    scalarWeightTomitaGraph P ⊆ closure (scalarTomitaGraph P) := by
  rintro _ ⟨A,rfl⟩
  let a : scalarWeightLeftIdeal P := ⟨A.val,A.property.1⟩
  let astar : scalarWeightLeftIdeal P := ⟨(star A).val,(star A).property.1⟩
  have ht : Tendsto (fun h : ℝ =>
      (scalarWeightGNSEmbedding P (scalarWeightSandwich P a h),
        scalarWeightGNSEmbedding P (scalarWeightSandwich P astar h)))
      (𝓝[>] (0 : ℝ))
      (𝓝 (scalarWeightStarEmbedding P A,scalarWeightStarEmbedding P (star A))) :=
    ((scalarWeightGNSEmbedding_sandwich_tendsto P a).prodMk_nhds
      (scalarWeightGNSEmbedding_sandwich_tendsto P astar)).mono_left
        (nhdsWithin_mono (0 : ℝ) (by intro h hh; exact ne_of_gt hh))
  apply isClosed_closure.mem_of_tendsto ht
  filter_upwards [self_mem_nhdsWithin] with h hh
  let b : finiteDualStarCore P := ⟨regularSandwich P A.val h,
    regularSandwich_mem_finiteDualStarCore P A.val h hh⟩
  apply subset_closure
  refine ⟨b,?_⟩
  apply Prod.ext
  · exact (scalarWeightGNSEmbedding_sandwich_uniform P a h hh).symm
  · rw [scalarWeightGNSEmbedding_sandwich_uniform P astar h hh]
    apply congrArg (scalarGNSStarEmbedding P)
    exact Subtype.ext (regularSandwich_star P A.val h)

theorem scalarWeightTomitaGraph_closure_eq (P : SiteProfile) :
    closure (scalarWeightTomitaGraph P) = closure (scalarTomitaGraph P) :=
  Set.Subset.antisymm
    (closure_minimal (scalarWeightTomitaGraph_subset_closure_original P) isClosed_closure)
    (closure_mono (scalarTomitaGraph_subset_weight P))

/-- The existing closed S is exactly the closure of the full-weight star
graph. This does not assert equality with the raw algebraic graph. -/
theorem scalarClosedTomita_graph_eq_weight (P : SiteProfile) :
    Set.range (fun x : scalarClosedTomitaDomain P =>
      ((x : ScalarGNSHilbert P),scalarClosedTomita P x)) =
        closure (scalarWeightTomitaGraph P) := by
  rw [scalarWeightTomitaGraph_closure_eq]
  exact scalarClosedTomita_graph_eq

theorem scalarWeightStar_mem_closedTomitaDomain (P : SiteProfile)
    (A : scalarWeightStarCore P) :
    scalarWeightStarEmbedding P A ∈ scalarClosedTomitaDomain P :=
  ⟨scalarWeightStarEmbedding P (star A),
    scalarWeightTomitaGraph_subset_closure_original P ⟨A,rfl⟩⟩

theorem scalarClosedTomita_extends_weight_star (P : SiteProfile)
    (A : scalarWeightStarCore P) :
    scalarClosedTomita P ⟨scalarWeightStarEmbedding P A,
      scalarWeightStar_mem_closedTomitaDomain P A⟩ = scalarWeightStarEmbedding P (star A) :=
  scalarTomitaGraph_closure_single_valued P (scalarWeightStarEmbedding P A) _ _
    (scalarClosedTomita_graph ⟨scalarWeightStarEmbedding P A,
      scalarWeightStar_mem_closedTomitaDomain P A⟩)
    (scalarWeightTomitaGraph_subset_closure_original P ⟨A,rfl⟩)

#print axioms scalarWeightGNSEmbedding_sandwich_uniform
#print axioms scalarWeightTomitaGraph_subset_closure_original
#print axioms scalarWeightTomitaGraph_closure_eq
#print axioms scalarClosedTomita_graph_eq_weight
#print axioms scalarWeightStar_mem_closedTomitaDomain
#print axioms scalarClosedTomita_extends_weight_star
end
end TGLV350.Regular
