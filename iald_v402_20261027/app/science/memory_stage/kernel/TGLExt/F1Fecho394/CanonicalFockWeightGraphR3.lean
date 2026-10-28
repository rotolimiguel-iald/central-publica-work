import TGLExt.F1Fecho394.CanonicalFockGNSR5
import TGLExt.F1Fecho394.RegularScalarTomitaClosureR2
/-! The initial adjunction graph of the actual scalar Fock weight is closable
and is not vacuous. This file does not assert Hilbert-norm density of its star
domain, identify its modular flow, or construct a scaled trace. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockWeightGraph
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockFiniteWeight F1Fecho.CanonicalFockGNS
open F1Fecho.RegularScalarTomitaGraph

abbrev starDomain := finiteStarCore weightContext
abbrev initialGraph := scalarTomitaGraph weightContext

theorem initialGraph_single_valued (x y z : GNSHilbert)
    (hy : (x,y) ∈ initialGraph) (hz : (x,z) ∈ initialGraph) : y=z :=
  scalarTomitaGraph_single_valued weightContext x y z hy hz

theorem initialGraph_swap (p : GNSHilbert × GNSHilbert)
    (hp : p ∈ initialGraph) : p.swap ∈ initialGraph :=
  scalarTomitaGraph_swap weightContext p hp

theorem closure_vertical (y : GNSHilbert) (hy : (0,y) ∈ closure initialGraph) : y=0 :=
  F1Fecho.RegularScalarTomitaClosure.scalarTomitaGraph_closure_vertical weightContext y hy

theorem closure_single_valued (x y z : GNSHilbert)
    (hy : (x,y) ∈ closure initialGraph) (hz : (x,z) ∈ closure initialGraph) : y=z :=
  F1Fecho.RegularScalarTomitaClosure.scalarTomitaGraph_closure_single_valued weightContext x y z hy hz

theorem exists_nonzero_graph_input : ∃ x y : GNSHilbert, x≠0 ∧ (x,y) ∈ initialGraph := by
  let B := F1Fecho.RegularCoreAverage.regularAverage fockFlow 1
  let a : core.toStarSubalgebra := ⟨star B*B,
    core.mul_mem (core.toStarSubalgebra.star_mem'
      (F1Fecho.RegularCoreAverage.regularAverage_mem fockFlow M 1))
      (F1Fecho.RegularCoreAverage.regularAverage_mem fockFlow M 1)⟩
  have ha : a≠0 := by
    intro h
    have hz : a.val=0 := congrArg Subtype.val h
    have hw : dualQuadraticIntegral a.val regularFockVacuum=1 := by
      simpa only [weight,averageSquare,inv_one,ENNReal.ofReal_one,a,B] using
        weight_averageSquare 1 zero_lt_one
    rw [hz,dualQuadraticIntegral_zero] at hw
    exact zero_ne_one hw
  have hf : HasFiniteDualSquare a.val :=
    HasFiniteDualSquare.left_mul (star B) B
      (F1Fecho.RegularCoreFiniteWeight.regularAverage_hasFiniteDualSquare fockFlow 1 zero_lt_one)
  have hs : HasFiniteDualSquare (star a.val) := by
    have he : star a.val=a.val := IsSelfAdjoint.star_mul_self B
    exact he.symm ▸ hf
  let A : starDomain := ⟨a,hf,hs⟩
  refine ⟨scalarGNSStarEmbedding weightContext A,
    scalarGNSStarEmbedding weightContext (star A),?_,⟨A,rfl⟩⟩
  intro h
  have he : F1Fecho.RegularScalarGNS.GNSEmbedding weightContext ⟨a,hf⟩ =
      F1Fecho.RegularScalarGNS.GNSEmbedding weightContext 0 := by
    exact h.trans (F1Fecho.RegularScalarGNS.GNSEmbedding weightContext).map_zero.symm
  have hz := F1Fecho.RegularScalarGNS.GNSEmbedding_injective weightContext he
  exact ha (congrArg Subtype.val hz)

end F1Fecho.CanonicalFockWeightGraph
#print axioms F1Fecho.CanonicalFockWeightGraph.starDomain
#print axioms F1Fecho.CanonicalFockWeightGraph.initialGraph
#print axioms F1Fecho.CanonicalFockWeightGraph.initialGraph_single_valued
#print axioms F1Fecho.CanonicalFockWeightGraph.initialGraph_swap
#print axioms F1Fecho.CanonicalFockWeightGraph.closure_vertical
#print axioms F1Fecho.CanonicalFockWeightGraph.closure_single_valued
#print axioms F1Fecho.CanonicalFockWeightGraph.exists_nonzero_graph_input
