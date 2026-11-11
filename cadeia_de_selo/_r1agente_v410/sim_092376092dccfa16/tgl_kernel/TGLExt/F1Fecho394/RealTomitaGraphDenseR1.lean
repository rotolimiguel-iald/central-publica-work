import TGLExt.F1Fecho394.RealTomitaGraphR3
/-! Transport of an existing pair-graph core into the actual real Hilbert graph.
The old graph closure is reused, without a new density hypothesis on vectors. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.RealTomitaGraph
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem dense_pair_graph (T:H→ₗ.[ℂ]H) (J:H≃ₛₗᵢ[starRingEnd ℂ]H)
    (D:Set (H×H)) (hD:closure D=CoefficientTomitaSquare.graph T J) :
    closure ((WithLp.ofLp : PairH H→H×H) ⁻¹' D)=(graph T J:Set (PairH H)) := by
  have hh:=(WithLp.prodContinuousLinearEquiv 2 ℝ H H).toHomeomorph.preimage_closure D
  change (WithLp.ofLp : PairH H→H×H) ⁻¹' closure D=
    closure ((WithLp.ofLp : PairH H→H×H) ⁻¹' D) at hh
  rw [←hh,hD]
  ext p
  change WithLp.ofLp p∈CoefficientTomitaSquare.graph T J ↔ p∈graph T J
  exact (mem_graph T J p).symm

end F1Fecho.RealTomitaGraph
#print axioms F1Fecho.RealTomitaGraph.dense_pair_graph
