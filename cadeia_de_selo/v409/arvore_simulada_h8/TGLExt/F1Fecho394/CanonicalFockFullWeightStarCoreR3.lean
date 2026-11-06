import TGLExt.F1Fecho394.RegularScalarWeightStarAlgebraR2
import TGLExt.F1Fecho394.CanonicalFockWeightCompletionR5
import TGLExt.F1Fecho394.CanonicalFockWeightClosedTomitaR2
/-! Full finite-weight star algebra on the same Fock core. This file only
constructs its raw adjunction graph and includes the original uniform core;
equality of graph closures requires the separate sandwich approximation. -/
set_option autoImplicit false
set_option maxErrors 2
set_option maxHeartbeats 2000000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockFullWeightStarCore
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockFiniteWeight F1Fecho.CanonicalFockWeightDomain F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockWeightCompletion
open scoped Topology ENNReal
abbrev scalarWeightStarCore := F1Fecho.RegularScalarWeightStarAlgebra.scalarWeightStarCore weightContext

def scalarWeightStarEmbedding  (A : scalarWeightStarCore) : GNSHilbert :=
  scalarWeightGNSEmbedding ⟨A.val,A.property.1⟩

def scalarUniformToWeightStar  (A : F1Fecho.RegularScalarTomitaGraph.finiteStarCore weightContext) : scalarWeightStarCore :=
  ⟨A.val,finiteSquare_scalar_finite _ A.property.1,
    finiteSquare_scalar_finite _ A.property.2⟩

theorem scalarUniformToWeightStar_star  (A : F1Fecho.RegularScalarTomitaGraph.finiteStarCore weightContext) :
    scalarUniformToWeightStar (star A) = star (scalarUniformToWeightStar A) := rfl

theorem scalarWeightStarEmbedding_uniform  (A : F1Fecho.RegularScalarTomitaGraph.finiteStarCore weightContext) :
    scalarWeightStarEmbedding (scalarUniformToWeightStar A) = F1Fecho.RegularScalarTomitaGraph.scalarGNSStarEmbedding weightContext A :=
  scalarWeightGNSEmbedding_uniform ⟨A.val,A.property.1⟩

def scalarWeightTomitaGraph  : Set (GNSHilbert × GNSHilbert) :=
  Set.range fun A : scalarWeightStarCore =>
    (scalarWeightStarEmbedding A,scalarWeightStarEmbedding (star A))

theorem scalarTomitaGraph_subset_weight  :
    F1Fecho.RegularScalarTomitaGraph.scalarTomitaGraph weightContext ⊆ scalarWeightTomitaGraph := by
  rintro _ ⟨A,rfl⟩
  refine ⟨scalarUniformToWeightStar A,?_⟩
  simp only [← scalarUniformToWeightStar_star,scalarWeightStarEmbedding_uniform]

#print axioms scalarWeightStarCore
#print axioms scalarWeightStarEmbedding
#print axioms scalarUniformToWeightStar
#print axioms scalarUniformToWeightStar_star
#print axioms scalarWeightStarEmbedding_uniform
#print axioms scalarWeightTomitaGraph
#print axioms scalarTomitaGraph_subset_weight
end F1Fecho.CanonicalFockFullWeightStarCore
