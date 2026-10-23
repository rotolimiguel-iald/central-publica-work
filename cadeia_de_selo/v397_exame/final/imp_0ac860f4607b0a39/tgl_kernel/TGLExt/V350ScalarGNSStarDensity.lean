import TGLExt.V350ScalarGNSRepresentation
import TGLExt.V350ScalarGNSStarApproximation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory Filter
open scoped Topology
noncomputable section

def scalarGNSStarEmbedding (P : SiteProfile) (A : finiteDualStarCore P) :
    ScalarGNSHilbert P := scalarGNSEmbedding P ⟨A.val,A.property.1⟩

theorem scalarGNSEmbedding_leftRegularization_tendsto (P : SiteProfile)
    (A : finiteDualLeftIdeal P) :
    Tendsto (fun h : ℝ => scalarGNSEmbedding P (scalarGNSLeftRegularization P A h))
      (𝓝[>] 0) (𝓝 (scalarGNSEmbedding P A)) := by
  apply tendsto_subtype_rng.mpr
  exact scalarGNSOrbit_leftRegularization_tendsto P A

/-- Density is in the Hilbert norm inherited from the scalar weight, not
merely strong operator density of the algebraic domain inside N. -/
theorem scalarGNSStarEmbedding_denseRange (P : SiteProfile) :
    DenseRange (scalarGNSStarEmbedding P) := by
  have hs : Set.range (scalarGNSEmbedding P) ⊆ closure (Set.range (scalarGNSStarEmbedding P)) := by
    rintro v ⟨A,rfl⟩
    apply isClosed_closure.mem_of_tendsto (scalarGNSEmbedding_leftRegularization_tendsto P A)
    filter_upwards [self_mem_nhdsWithin] with h hh
    apply subset_closure
    exact ⟨⟨(scalarGNSLeftRegularization P A h).val,
      scalarGNSLeftRegularization_mem_starCore P A h hh⟩,rfl⟩
  intro v
  exact (closure_minimal hs isClosed_closure) ((scalarGNSEmbedding_denseRange P) v)

#print axioms scalarGNSStarEmbedding
#print axioms scalarGNSEmbedding_leftRegularization_tendsto
#print axioms scalarGNSStarEmbedding_denseRange
end
end TGLV350.Regular
