import TGLExt.F1Fecho394.CoefficientTomitaSquareR2
import Mathlib.Analysis.InnerProductSpace.ProdL2

/-! The closed antilinear Tomita graph as an actual real Hilbert subspace.
The L2 graph core can therefore use orthogonal projection without declaring
an antilinear graph to be a complex subspace. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RealTomitaGraph
open ChatgptAudit.Continuous050
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

abbrev PairH (H:Type) := WithLp 2 (H×H)

def realJ (J:H≃ₛₗᵢ[starRingEnd ℂ]H) : H→L[ℝ]H where
  toFun:=J
  map_add':=J.map_add
  map_smul' c x:=by
    change J ((c:ℂ) • x)=(c:ℂ) • J x
    rw [J.map_smulₛₗ]
    simp
  cont:=J.continuous

def graphMap (T:H→ₗ.[ℂ]H) (J:H≃ₛₗᵢ[starRingEnd ℂ]H) : T.domain→ₗ[ℝ]PairH H :=
  (WithLp.linearEquiv 2 ℝ (H×H)).symm.toLinearMap.comp
    ((T.domain.subtype.restrictScalars ℝ).prod
      ((realJ J).toLinearMap.comp (T.toFun.restrictScalars ℝ)))

def graph (T:H→ₗ.[ℂ]H) (J:H≃ₛₗᵢ[starRingEnd ℂ]H) : Submodule ℝ (PairH H) :=
  LinearMap.range (graphMap T J)

theorem mem_graph (T:H→ₗ.[ℂ]H) (J:H≃ₛₗᵢ[starRingEnd ℂ]H) (p:PairH H) :
    p∈graph T J ↔ WithLp.ofLp p∈CoefficientTomitaSquare.graph T J := by
  constructor
  · rintro ⟨u,hu⟩
    exact ⟨u,congrArg WithLp.ofLp hu⟩
  · rintro ⟨u,hu⟩
    exact ⟨u,congrArg (WithLp.toLp 2) hu⟩

theorem graph_closed (T:H→ₗ.[ℂ]H) (hT:T.IsClosed)
    (J:H≃ₛₗᵢ[starRingEnd ℂ]H) (hJ:Function.Involutive J) :
    IsClosed (graph T J:Set (PairH H)) := by
  have he : (graph T J:Set (PairH H))=
      (fun p:PairH H=>((WithLp.ofLp p).1,J (WithLp.ofLp p).2)) ⁻¹' (T.graph:Set (H×H)) := by
    ext p
    change p∈graph T J ↔ ((WithLp.ofLp p).1,J (WithLp.ofLp p).2)∈T.graph
    rw [mem_graph]
    constructor
    · rintro ⟨u,hu⟩
      have hx:(u:H)=(WithLp.ofLp p).1:=congrArg Prod.fst hu
      have hy:J (T u)=(WithLp.ofLp p).2:=congrArg Prod.snd hu
      exact (LinearPMap.mem_graph_iff T).mpr ⟨u,hx,by rw [←hy,hJ]⟩
    · intro h
      obtain ⟨u,hx,hy⟩ := (LinearPMap.mem_graph_iff T).mp h
      refine ⟨u,Prod.ext hx ?_⟩
      change J (T u)=(WithLp.ofLp p).2
      rw [hy,hJ]
  rw [he]
  exact hT.preimage ((WithLp.fstL 2 ℝ H H).continuous.prodMk
    (J.continuous.comp (WithLp.sndL 2 ℝ H H).continuous))

end F1Fecho.RealTomitaGraph
#print axioms F1Fecho.RealTomitaGraph.realJ
#print axioms F1Fecho.RealTomitaGraph.mem_graph
#print axioms F1Fecho.RealTomitaGraph.graph_closed
