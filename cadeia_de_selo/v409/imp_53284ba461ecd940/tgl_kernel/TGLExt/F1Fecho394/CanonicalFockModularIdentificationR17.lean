import TGLExt.F1Fecho394.CanonicalFockModularGraphEqualityR1
import TGLExt.F1Fecho394.ModularTransportTargetR1

/-! The actual dual-weight modular group is the regular implementation.
The concrete coefficient unitary transports the full Tomita graphs, then
recognition of their independently constructed resolvents transports CFC.
No modular-flow equality or trace is supplied as an input. -/
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option maxErrors 3
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockModularIdentification
open TGLV350.Regular F1Rede.BosonicFock ORDEM016.D6
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockCoefficientGNS
open F1Fecho.CanonicalFockCoefficientIntervals F1Fecho.CanonicalFockCoefficientInclusion
open F1Fecho.CanonicalFockCoefficientFlow F1Fecho.CanonicalFockCoefficientGraphEquality
open F1Fecho.CoefficientFockConjugation F1Fecho.CanonicalFockConjugation
open F1Fecho.CanonicalFockWeightModularOperator F1Fecho.CanonicalFockWeightModularFlow
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (GNSHilbert →L[ℂ] GNSHilbert) := F1Fecho.ClosedSubmoduleRestriction.endomorphismStar GNSSubspace

 theorem target_graph_eq : ClosedTomitaSquareGraph.graph actualClosedInput=
    (RegularScalarRealGraph.closedGraph weightContext:Set (GNSHilbert×GNSHilbert)) :=
  CanonicalFockWeightClosedTomita.graph_eq

 theorem target_graph_mem_iff (x y:GNSHilbert) :
    (x,y)∈ClosedTomitaSquareGraph.graph actualClosedInput ↔
      (x,y)∈RegularScalarRealGraph.closedGraph weightContext :=
  Iff.of_eq (congrArg (fun S:Set (GNSHilbert×GNSHilbert)=>(x,y)∈S) target_graph_eq)

 theorem unitary_graph :
    (coefficientUnitary.toHomeomorph.prodCongr coefficientUnitary.toHomeomorph) ''
      CoefficientTomitaSquare.graph coefficientRoot coefficientJ=
        ClosedTomitaSquareGraph.graph actualClosedInput := by
  have hpt (x y : RegularHilbert F) :
      (coefficientUnitary x,coefficientUnitary y) ∈ ClosedTomitaSquareGraph.graph actualClosedInput ↔
        (x,y) ∈ CoefficientTomitaSquare.graph coefficientRoot coefficientJ := by
    change (coefficientEmbedding x,coefficientEmbedding y) ∈ ClosedTomitaSquareGraph.graph actualClosedInput ↔ _
    exact (target_graph_mem_iff (coefficientEmbedding x) (coefficientEmbedding y)).trans
      ((coefficientGraph_mem x y).symm.trans
        (Iff.of_eq (congrArg (fun S : Set (RegularHilbert F × RegularHilbert F) => (x,y) ∈ S)
          coefficient_graph_eq_GNS.symm)))
  with_reducible
    exact ModularTransportTarget.graph_image (H := RegularHilbert F) (E := GNSHilbert)
      coefficientUnitary (CoefficientTomitaSquare.graph coefficientRoot coefficientJ)
      (ClosedTomitaSquareGraph.graph actualClosedInput) hpt

 theorem source_resolvent_mem (x:RegularHilbert F) :
    (coefficientR x,x-coefficientR x)∈antilinearSquareGraph
      (CoefficientTomitaSquare.graph coefficientRoot coefficientJ) := by
  rw [coefficient_square]
  apply (resolvent_graph_equation (H := RegularHilbert F) coefficientR hi
    (coefficientR x) (x-coefficientR x)).mpr
  change coefficientR x-coefficientR (coefficientR x)=coefficientR (x-coefficientR x)
  rw [map_sub]

 theorem resolvent_intertwines (x:RegularHilbert F) :
    coefficientUnitary (coefficientR x)=CanonicalFockWeightModularOperator.scalarTomitaResolvent (coefficientUnitary x) := by
  with_reducible
    exact unitary_recognizes_square_resolvent (H := RegularHilbert F) (K := GNSHilbert) coefficientUnitary (CoefficientTomitaSquare.graph coefficientRoot coefficientJ)
      (ClosedTomitaSquareGraph.graph actualClosedInput) unitary_graph
      coefficientR CanonicalFockWeightModularOperator.scalarTomitaResolvent source_resolvent_mem
      (ClosedTomitaSquareGraph.resolvent_inverse actualClosedInput) x

 theorem transported_resolvent_eq :
    SpectralTransport.transported (H := RegularHilbert F) (E := GNSHilbert) coefficientUnitary coefficientR=CanonicalFockWeightModularOperator.scalarTomitaResolvent := by
  with_reducible
    exact ModularTransportTarget.transported_eq (H := RegularHilbert F) (E := GNSHilbert)
      coefficientUnitary coefficientR CanonicalFockWeightModularOperator.scalarTomitaResolvent
      resolvent_intertwines

 theorem imaginary_intertwines (t:ℝ) (x:RegularHilbert F) :
    coefficientUnitary (FibreModularCalculus.liftedFlow
      CanonicalFockPolar.modularR CanonicalFockPolar.modularR_nonneg CanonicalFockPolar.modularR_le_one
      CanonicalFockPolar.modularR_injective CanonicalFockPolar.modularR_complement_injective t x)=
        scalarTomitaImaginaryPower t (coefficientUnitary x) := by
  dsimp only [FibreModularCalculus.liftedFlow,
    CanonicalFockWeightModularFlow.scalarTomitaImaginaryPower,
    ClosedTomitaFlow.scalarTomitaImaginaryPower]
  with_reducible
    exact ModularTransportTarget.imaginary_target (H := RegularHilbert F) (E := GNSHilbert)
      coefficientUnitary coefficientR CanonicalFockWeightModularOperator.scalarTomitaResolvent
      hR h1 hi hj scalarTomitaResolvent_nonneg scalarTomitaResolvent_le_one
      scalarTomitaResolvent_injective
      (F1Fecho.ClosedTomitaFlow.scalarTomitaResolvent_complement_injective actualClosedInput)
      transported_resolvent_eq t x

 theorem actual_modular_implementation (t:ℝ) (y:GNSHilbert) :
    scalarTomitaImaginaryPower t y=regularConjugationGNS t y := by
  calc
    _=scalarTomitaImaginaryPower t (coefficientUnitary (coefficientUnitary.symm y)):=
      congrArg (fun z:GNSHilbert=>scalarTomitaImaginaryPower t z)
        (coefficientUnitary.apply_symm_apply y).symm
    _=coefficientUnitary (FibreModularCalculus.liftedFlow
        CanonicalFockPolar.modularR CanonicalFockPolar.modularR_nonneg CanonicalFockPolar.modularR_le_one
        CanonicalFockPolar.modularR_injective CanonicalFockPolar.modularR_complement_injective
        t (coefficientUnitary.symm y)):=
      (imaginary_intertwines t (coefficientUnitary.symm y)).symm
    _=regularConjugationGNS t (coefficientUnitary (coefficientUnitary.symm y)):=
      cfc_intertwines t (coefficientUnitary.symm y)
    _=regularConjugationGNS t y:=congrArg (regularConjugationGNS t)
      (coefficientUnitary.apply_symm_apply y)

theorem actual_regular_conjugation_norm (t:ℝ) (y:GNSHilbert) :
    ‖regularConjugationGNS t y‖=‖y‖ := by
  exact (congrArg norm (actual_modular_implementation t y)).symm.trans
    ((scalarTomitaImaginaryPower t).norm_map y)

theorem actual_regular_conjugation_group (s t:ℝ) (y:GNSHilbert) :
    regularConjugationGNS s (regularConjugationGNS t y)=regularConjugationGNS (s+t) y := by
  calc
    _=scalarTomitaImaginaryPower s (regularConjugationGNS t y):=
      (actual_modular_implementation s (regularConjugationGNS t y)).symm
    _=scalarTomitaImaginaryPower s (scalarTomitaImaginaryPower t y):=
      congrArg (fun z:GNSHilbert=>scalarTomitaImaginaryPower s z)
        (actual_modular_implementation t y).symm
    _=scalarTomitaImaginaryPower (s+t) y:=scalarTomitaImaginaryPower_add s t y
    _=regularConjugationGNS (s+t) y:=actual_modular_implementation (s+t) y

end F1Fecho.CanonicalFockModularIdentification
#print axioms F1Fecho.CanonicalFockModularIdentification.unitary_graph
#print axioms F1Fecho.CanonicalFockModularIdentification.resolvent_intertwines
#print axioms F1Fecho.CanonicalFockModularIdentification.transported_resolvent_eq
#print axioms F1Fecho.CanonicalFockModularIdentification.imaginary_intertwines
#print axioms F1Fecho.CanonicalFockModularIdentification.actual_modular_implementation

#print axioms F1Fecho.CanonicalFockModularIdentification.actual_regular_conjugation_norm
#print axioms F1Fecho.CanonicalFockModularIdentification.actual_regular_conjugation_group

-- END DERIVED BODY CanonicalFockModularIdentificationR12

