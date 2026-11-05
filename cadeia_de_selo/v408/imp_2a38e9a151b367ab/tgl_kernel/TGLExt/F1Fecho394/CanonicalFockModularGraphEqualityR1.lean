import TGLExt.F1Fecho394.RegularCovariantCoreR3
import TGLExt.F1Fecho394.RegularScalarWeightStarAlgebraR2
import TGLExt.F1Fecho394.CanonicalFockConjugationActionR3
import TGLExt.F1Fecho394.CanonicalFockFullWeightTomitaR5
import TGLExt.F1Fecho394.RegularScalarRealGraphR2
import TGLExt.F1Fecho394.UnitaryAntiunitaryTransportR2
import TGLExt.F1Fecho394.CanonicalFockCoefficientUnitaryR3
import TGLExt.F1Fecho394.CoefficientFockConjugationR2
import TGLExt.F1Fecho394.CanonicalFockCoefficientIntervalsR5
import TGLExt.F1Fecho394.CanonicalFockCoefficientInclusionR6
import TGLExt.F1Fecho394.GaussianResolventAverageR6
import TGLExt.F1Fecho394.ClosedGraphRegularizationR3
import TGLExt.F1Fecho394.ClosedTomitaSquareGraphR1
import TGLExt.F1Fecho394.CanonicalFockWeightModularFlowR3
import TGLExt.F1Fecho394.SpectralUnitaryTransportR1
import TGLExt.F1Fecho394.UnitaryRootGraphTransportR1
import TGLExt.V350PartialSelfadjointRange

-- BEGIN DERIVED BODY GenericStarConjugationR4
/-! Abstract regular conjugation and full finite-star-domain assembly, before Fock specialization. -/
set_option autoImplicit false
set_option maxErrors 3
noncomputable section
namespace F1Fecho.GenericStarConjugation
open TGLV350.Regular F1Fecho.RegularCovariantCore
open F1Fecho.RegularScalarGNS F1Fecho.RegularScalarWeightDomain
open F1Fecho.RegularScalarWeightStarAlgebra
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
theorem regular_conjugation_star (B:UnitaryFlow H) (t:ℝ)
    (A:RegularHilbert H →L[ℂ] RegularHilbert H) :
    star (regularUnitary B t*(A*regularUnitary B (-t))) =
      regularUnitary B t*(star A*regularUnitary B (-t)) := by
  rw [star_mul,star_mul,RegularCovariantCore.regular_star,RegularCovariantCore.regular_star,neg_neg,mul_assoc]
def starCoreOfLeft (D:Context H) (A B:scalarWeightLeftIdeal D)
    (h:star A.val=B.val) : scalarWeightStarCore D :=
  ⟨A.val,A.property,by
    change star A.val ∈ scalarWeightLeftIdeal D
    rw [h]
    exact B.property⟩
end F1Fecho.GenericStarConjugation
#print axioms F1Fecho.GenericStarConjugation.regular_conjugation_star
#print axioms F1Fecho.GenericStarConjugation.starCoreOfLeft

-- END DERIVED BODY GenericStarConjugationR4

-- BEGIN DERIVED BODY CanonicalFockGNSCovarianceR13
/-! Regular conjugation preserves the FULL actual GNS adjunction graph.
The star action and finite domain are paid by actual left/right products;
modular identification is not assumed from this covariance. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockGNSCovariance
open TGLExt.ImportedSQ F1Rede.BosonicFock
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockWeightDomain F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockRegularRightGNS F1Fecho.CanonicalFockConjugation
open F1Fecho.CanonicalFockFullWeightStarCore F1Fecho.CanonicalFockFullWeightTomita
open F1Fecho.RegularScalarRealGraph F1Fecho.CanonicalFockWeightSandwich

 def conjugateLeft (t:ℝ) (A:scalarWeightStarCore) : scalarWeightLeftIdeal :=
  scalarWeightLeftProduct (regularRightCoreElement t)
    (scalarRegularRightProduct (-t) ⟨A.val,A.property.1⟩)

 theorem conjugateLeft_star (t:ℝ) (A:scalarWeightStarCore) :
    star (conjugateLeft t A).val=(conjugateLeft t (star A)).val := by
  apply Subtype.ext
  change star (regularUnitary t*(A.val.val*regularUnitary (-t)))=
    regularUnitary t*(star A.val.val*regularUnitary (-t))
  exact GenericStarConjugation.regular_conjugation_star fockFlow t A.val.val

 def conjugateStar (t:ℝ) (A:scalarWeightStarCore) : scalarWeightStarCore :=
  GenericStarConjugation.starCoreOfLeft weightContext (conjugateLeft t A)
    (conjugateLeft t (star A)) (conjugateLeft_star t A)


 theorem conjugateStar_star (t:ℝ) (A:scalarWeightStarCore) :
    star (conjugateStar t A)=conjugateStar t (star A) :=
  Subtype.ext (conjugateLeft_star t A)

 theorem conjugate_embedding (t:ℝ) (A:scalarWeightStarCore) :
    regularConjugationGNS t (scalarWeightStarEmbedding A)=
      scalarWeightStarEmbedding (conjugateStar t A) :=
  regularConjugationGNS_intertwines t ⟨A.val,A.property.1⟩

 def conjugatePair (t:ℝ) : (GNSHilbert×GNSHilbert)→L[ℂ](GNSHilbert×GNSHilbert) :=
  (regularConjugationGNS t).prodMap (regularConjugationGNS t)

 theorem conjugate_raw_graph (t:ℝ) (p:GNSHilbert×GNSHilbert)
    (hp:p∈scalarWeightTomitaGraph) : conjugatePair t p∈scalarWeightTomitaGraph := by
  obtain ⟨A,rfl⟩:=hp
  refine ⟨conjugateStar t A,?_⟩
  apply Prod.ext
  · exact (conjugate_embedding t A).symm
  · exact (congrArg scalarWeightStarEmbedding (conjugateStar_star t A)).trans
      (conjugate_embedding t (star A)).symm

 theorem conjugate_closed_graph (t:ℝ) (p:GNSHilbert×GNSHilbert)
    (hp:p∈closedGraph weightContext) : conjugatePair t p∈closedGraph weightContext := by
  have hmap : ∀p∈closure scalarWeightTomitaGraph,
      conjugatePair t p∈closure scalarWeightTomitaGraph :=
    closure_minimal (fun p hp=>subset_closure (conjugate_raw_graph t p hp))
      (isClosed_closure.preimage (conjugatePair t).continuous)
  change conjugatePair t p∈closure (RegularScalarTomitaGraph.scalarTomitaGraph weightContext)
  change p∈closure (RegularScalarTomitaGraph.scalarTomitaGraph weightContext) at hp
  exact Eq.mp (congrArg (fun s=>conjugatePair t p∈s) scalarWeightTomitaGraph_closure_eq)
    (hmap p (Eq.mpr (congrArg (fun s=>p∈s) scalarWeightTomitaGraph_closure_eq) hp))
end F1Fecho.CanonicalFockGNSCovariance
#print axioms F1Fecho.CanonicalFockGNSCovariance.conjugateLeft_star
#print axioms F1Fecho.CanonicalFockGNSCovariance.conjugateStar_star
#print axioms F1Fecho.CanonicalFockGNSCovariance.conjugate_embedding
#print axioms F1Fecho.CanonicalFockGNSCovariance.conjugate_raw_graph
#print axioms F1Fecho.CanonicalFockGNSCovariance.conjugate_closed_graph

-- END DERIVED BODY CanonicalFockGNSCovarianceR13

-- BEGIN DERIVED BODY CanonicalFockWeightPolarBasicsR4

/-! Concrete antiunitary on the actual weight GNS, by the already proved
coefficient unitary. Its identification as the polar factor is a separate
graph theorem, not assumed by this definition. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockWeightPolar
open TGLV350.Regular F1Rede.BosonicFock
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockCoefficientGNS
open F1Fecho.CoefficientFockConjugation

def scalarTomitaPolarFactor : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert :=
  UnitaryAntiunitaryTransport.conjugate (H := RegularHilbert F) (E := GNSHilbert) coefficientUnitary coefficientJ

theorem scalarTomitaPolarFactor_apply (x : GNSHilbert) :
    scalarTomitaPolarFactor x =
      coefficientUnitary (coefficientJ (coefficientUnitary.symm x)) := rfl

theorem scalarTomitaPolarFactor_coefficient (x : RegularHilbert F) :
    scalarTomitaPolarFactor (coefficientUnitary x) = coefficientUnitary (coefficientJ x) := by
  change coefficientUnitary (coefficientJ (coefficientUnitary.symm (coefficientUnitary x)))=
    coefficientUnitary (coefficientJ x)
  exact congrArg (fun v:RegularHilbert F=>coefficientUnitary (coefficientJ v))
    (coefficientUnitary.symm_apply_apply x)

theorem scalarTomitaPolarFactor_involutive : Function.Involutive scalarTomitaPolarFactor := by
  intro x
  change coefficientUnitary (coefficientJ (coefficientUnitary.symm
    (coefficientUnitary (coefficientJ (coefficientUnitary.symm x)))))=x
  calc
    _=coefficientUnitary (coefficientJ (coefficientJ (coefficientUnitary.symm x))):=
      congrArg (fun v:RegularHilbert F=>coefficientUnitary (coefficientJ v))
        (coefficientUnitary.symm_apply_apply (coefficientJ (coefficientUnitary.symm x)))
    _=coefficientUnitary (coefficientUnitary.symm x):=
      congrArg coefficientUnitary (coefficientJ_involutive (coefficientUnitary.symm x))
    _=x:=coefficientUnitary.apply_symm_apply x

theorem scalarTomitaPolarFactor_norm (x : GNSHilbert) :
    ‖scalarTomitaPolarFactor x‖ = ‖x‖ := scalarTomitaPolarFactor.norm_map x
end F1Fecho.CanonicalFockWeightPolar
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolarFactor_coefficient
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolarFactor_involutive
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolarFactor_norm

-- END DERIVED BODY CanonicalFockWeightPolarBasicsR4

-- BEGIN DERIVED BODY CanonicalFockCoefficientFlowR16
/-! The coefficient embedding intertwines the actual regular GNS conjugation
with the actual CFC flow of the coefficient Tomita square. This is a unitary
flow calculation; equality of the two Tomita graphs is still separate. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockCoefficientFlow
open F1Rede.BosonicFock
open TGLV350.Regular F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockCoefficientGNS F1Fecho.CanonicalFockCoefficientIntervals
open F1Fecho.CanonicalFockConjugation F1Fecho.CanonicalFockGNSCovariance
open F1Fecho.RegularNormalizedFourier F1Fecho.CanonicalFockPolar

theorem intertwines (t:ℝ) (f:RegularHilbert F) :
    coefficientEmbedding (fibre (RegularCovariantCore.boostCLM fockFlow t) f)=
      regularConjugationGNS t (coefficientEmbedding f) := by
  apply Subtype.ext
  exact (spectralCode_fibre (RegularCovariantCore.boostCLM fockFlow t) f).trans
    (regularConjugationGNS_ambient t (coefficientEmbedding f)).symm

theorem cfc_intertwines (t:ℝ) (f:RegularHilbert F) :
    coefficientEmbedding (FibreModularCalculus.liftedFlow modularR modularR_nonneg modularR_le_one
      modularR_injective modularR_complement_injective t f)=
      regularConjugationGNS t (coefficientEmbedding f) := by
  have he := CoefficientFockConjugation.coefficient_modular_flow t f
  exact (congrArg coefficientEmbedding he).trans (intertwines t f)

theorem graph_invariant (t:ℝ) (f g:RegularHilbert F) (hfg:(f,g)∈coefficientGraph) :
    (fibre (RegularCovariantCore.boostCLM fockFlow t) f,
      fibre (RegularCovariantCore.boostCLM fockFlow t) g)∈coefficientGraph := by
  apply (coefficientGraph_mem _ _).mpr
  have he : (coefficientEmbedding (fibre (RegularCovariantCore.boostCLM fockFlow t) f),
      coefficientEmbedding (fibre (RegularCovariantCore.boostCLM fockFlow t) g)) =
      (regularConjugationGNS t (coefficientEmbedding f),
        regularConjugationGNS t (coefficientEmbedding g)) :=
    Prod.ext (intertwines t f) (intertwines t g)
  have hp := conjugate_closed_graph t (coefficientEmbedding f,coefficientEmbedding g)
    ((coefficientGraph_mem f g).mp hfg)
  change (regularConjugationGNS t (coefficientEmbedding f),
    regularConjugationGNS t (coefficientEmbedding g))∈
      RegularScalarRealGraph.closedGraph weightContext at hp
  exact Eq.mpr (congrArg (fun p:GNSHilbert×GNSHilbert=>
    p∈RegularScalarRealGraph.closedGraph weightContext) he) hp
end F1Fecho.CanonicalFockCoefficientFlow
#print axioms F1Fecho.CanonicalFockCoefficientFlow.intertwines
#print axioms F1Fecho.CanonicalFockCoefficientFlow.cfc_intertwines
#print axioms F1Fecho.CanonicalFockCoefficientFlow.graph_invariant

-- END DERIVED BODY CanonicalFockCoefficientFlowR16

-- BEGIN DERIVED BODY CanonicalFockCoefficientGraphEqualityR12
/-! Equality of the actual coefficient and GNS Tomita graphs. The reverse
inclusion uses constructed Gaussian regularizers, their actual root-domain
range, and their strong convergence; no maximality or graph equality is an input. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
open MeasureTheory Filter
open scoped Topology
namespace F1Fecho.CanonicalFockCoefficientGraphEquality
open F1Rede.BosonicFock TGLV350.Regular
open F1Fecho.CanonicalFockPolar F1Fecho.CoefficientFockConjugation
open F1Fecho.CanonicalFockCoefficientGNS F1Fecho.CanonicalFockCoefficientIntervals
open F1Fecho.CanonicalFockCoefficientInclusion F1Fecho.CanonicalFockCoefficientFlow
open F1Fecho.GaussianResolventAverage F1Fecho.FibreModularCalculus
local instance : InnerProductSpace ℝ (RegularHilbert F) := InnerProductSpace.complexToReal

abbrev coefficientR := fibre modularR
abbrev hR := fibre_nonneg modularR_nonneg
abbrev h1 := lifted_le_one modularR modularR_le_one
abbrev hi := fibre_operator_injective modularR modularR_injective
abbrev hj := lifted_complement_injective modularR modularR_complement_injective
abbrev coefficientAverage (n:ℕ) := average coefficientR hR h1 hi hj (scale n)

def realGNSGraph : Submodule ℝ (WithLp 2 (RegularHilbert F×RegularHilbert F)) :=
  coefficientGraph.comap (WithLp.prodContinuousLinearEquiv 2 ℝ (RegularHilbert F)
    (RegularHilbert F)).toLinearMap

theorem realGNSGraph_closed : IsClosed (realGNSGraph:Set (WithLp 2 (RegularHilbert F×RegularHilbert F))) :=
  coefficientGraph_closed.preimage (WithLp.prodContinuousLinearEquiv 2 ℝ (RegularHilbert F)
    (RegularHilbert F)).continuous

theorem average_preserves (n:ℕ) (x y:RegularHilbert F) (hxy:(x,y)∈coefficientGraph) :
    (coefficientAverage n x,coefficientAverage n y)∈coefficientGraph := by
  let U:ℝ→RegularHilbert F≃ₗᵢ[ℂ]RegularHilbert F := fun t=>
    resolventImaginaryPower coefficientR hR h1 hi hj (scale n*t)
  have hc:∀x,Continuous (fun t=>U t x) := fun x=>
    (resolventImaginaryPower_strongly_continuous coefficientR hR h1 hi hj x).comp
      (continuous_const.mul continuous_id)
  have hu:∀t x y,WithLp.toLp 2 (x,y)∈realGNSGraph→
      WithLp.toLp 2 (U t x,U t y)∈realGNSGraph := by
    intro t x y hxy
    change (U t x,U t y)∈coefficientGraph
    change (x,y)∈coefficientGraph at hxy
    change (liftedFlow modularR modularR_nonneg modularR_le_one modularR_injective
        modularR_complement_injective (scale n*t) x,
      liftedFlow modularR modularR_nonneg modularR_le_one modularR_injective
        modularR_complement_injective (scale n*t) y)∈coefficientGraph
    rw [coefficient_modular_flow,coefficient_modular_flow]
    exact graph_invariant (scale n*t) x y hxy
  exact ClosedGraphRegularization.average_preserves_graph realGNSGraph realGNSGraph_closed
    U hc hu GaussianLogScalar.gaussianWeight GaussianLogScalar.gaussianWeight_integrable x y hxy

theorem average_range (n:ℕ) (x:RegularHilbert F) :
    ∃y,(coefficientAverage n x,y)∈CoefficientTomitaSquare.graph coefficientRoot coefficientJ := by
  obtain ⟨y,hy⟩:=average_root_domain coefficientR hR h1 hi hj (scale n) (scale_ne_zero n) x
  refine ⟨coefficientJ y,?_⟩
  apply (CoefficientFockPointwise.generic_graph_iff coefficientRoot coefficientJ
    coefficientJ_involutive _ _).mpr
  rw [coefficientJ_involutive y]
  change (coefficientAverage n x,y)∈(resolventSquareRoot coefficientR hR hi).graph
  exact hy

theorem coefficient_graph_eq_GNS :
    CoefficientTomitaSquare.graph coefficientRoot coefficientJ=
      (coefficientGraph:Set (RegularHilbert F×RegularHilbert F)) := by
  refine ClosedGraphRegularization.graph_eq_of_regularizers _ _ coefficient_graph_closed ?_
    coefficientGNSGraph_functional (fun n x=>coefficientAverage n x)
    (average_tendsto coefficientR hR h1 hi hj) average_preserves average_range
  rintro ⟨x,y⟩ hxy
  exact (coefficientGraph_mem x y).mpr (coefficient_graph_into_GNS x y hxy)

end F1Fecho.CanonicalFockCoefficientGraphEquality
#print axioms F1Fecho.CanonicalFockCoefficientGraphEquality.average_preserves
#print axioms F1Fecho.CanonicalFockCoefficientGraphEquality.average_range
#print axioms F1Fecho.CanonicalFockCoefficientGraphEquality.coefficient_graph_eq_GNS

-- END DERIVED BODY CanonicalFockCoefficientGraphEqualityR12

