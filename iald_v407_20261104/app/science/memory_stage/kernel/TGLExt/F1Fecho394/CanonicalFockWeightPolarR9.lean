import TGLExt.F1Fecho394.CanonicalFockModularIdentificationR17
import TGLExt.F1Fecho394.GenericPolarGraphTransportR1


/-! Actual polar decomposition on the SAME dual-weight GNS.
The root is the positive root of the independently constructed S-adjoint-S
resolvent; transport of the full graphs proves S=J root with equal domains.
No polar identity, traciality, or scaled trace is supplied as a hypothesis. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockWeightPolar
open TGLV350.Regular ChatgptAudit.Continuous049
open F1Rede.BosonicFock F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockCoefficientGNS F1Fecho.CoefficientFockConjugation
open F1Fecho.CanonicalFockCoefficientGraphEquality F1Fecho.CanonicalFockModularIdentification
open F1Fecho.CanonicalFockWeightModularOperator F1Fecho.CanonicalFockWeightClosedTomita
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (GNSHilbert →L[ℂ] GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar GNSSubspace

abbrev scalarTomitaPositiveRoot :=
  resolventSquareRoot (H := GNSHilbert) CanonicalFockWeightModularOperator.scalarTomitaResolvent scalarTomitaResolvent_nonneg scalarTomitaResolvent_injective

theorem root_coefficient_graph_iff (x y : RegularHilbert F) :
    (coefficientUnitary x,coefficientUnitary y) ∈ scalarTomitaPositiveRoot.graph ↔
      (x,y) ∈ coefficientRoot.graph := by
  dsimp only [coefficientRoot,FibreModularCalculus.liftedRoot]
  with_reducible
    exact ModularTransportTarget.root_target (H := RegularHilbert F) (E := GNSHilbert)
      coefficientUnitary coefficientR CanonicalFockWeightModularOperator.scalarTomitaResolvent
      hR h1 hi scalarTomitaResolvent_nonneg scalarTomitaResolvent_injective
      transported_resolvent_eq x y

theorem polar_graph (x y : GNSHilbert) (hxy : (x,y) ∈ scalarTomitaPositiveRoot.graph) :
    (x,scalarTomitaPolarFactor y) ∈ ClosedTomitaSquareGraph.graph actualClosedInput := by
  let u : RegularHilbert F := coefficientUnitary.symm x
  let v : RegularHilbert F := coefficientUnitary.symm y
  have hx : coefficientUnitary u = x := coefficientUnitary.apply_symm_apply x
  have hy : coefficientUnitary v = y := coefficientUnitary.apply_symm_apply y
  have hxy' : (coefficientUnitary u,coefficientUnitary v) ∈ scalarTomitaPositiveRoot.graph :=
    Eq.mpr (congrArg (fun p : GNSHilbert × GNSHilbert => p ∈ scalarTomitaPositiveRoot.graph)
      (Prod.ext hx hy)) hxy
  have hs := (root_coefficient_graph_iff u v).mp hxy'
  have hg : (u,coefficientJ v) ∈ CoefficientTomitaSquare.graph coefficientRoot coefficientJ :=
    GenericPolarGraphTransport.root_to_polar_graph coefficientRoot coefficientJ u v hs
  have ht : (coefficientUnitary u,coefficientUnitary (coefficientJ v)) ∈
      ClosedTomitaSquareGraph.graph actualClosedInput :=
    (target_graph_mem_iff _ _).mpr (CanonicalFockCoefficientInclusion.coefficient_graph_into_GNS _ _ hg)
  have hj : coefficientUnitary (coefficientJ v) = scalarTomitaPolarFactor y :=
    (scalarTomitaPolarFactor_coefficient v).symm.trans (congrArg scalarTomitaPolarFactor hy)
  exact Eq.mp (congrArg (fun p : GNSHilbert × GNSHilbert =>
    p ∈ ClosedTomitaSquareGraph.graph actualClosedInput) (Prod.ext hx hj)) ht

theorem scalarTomitaRootDomain_le_closed : scalarTomitaPositiveRoot.domain ≤ closedTomitaDomain := by
  intro x hx
  have hg := polar_graph x (scalarTomitaPositiveRoot ⟨x,hx⟩)
    ((LinearPMap.mem_graph_iff scalarTomitaPositiveRoot).mpr ⟨⟨x,hx⟩,rfl,rfl⟩)
  obtain ⟨u,hu⟩ := hg
  have he : (u:GNSHilbert)=x := congrArg Prod.fst hu
  rw [←he]
  exact u.property

theorem scalarTomitaPolarFactor_root (x : scalarTomitaPositiveRoot.domain) :
    scalarTomitaPolarFactor (scalarTomitaPositiveRoot x) =
      closedTomita (Submodule.inclusion scalarTomitaRootDomain_le_closed x) := by
  have hg := polar_graph x (scalarTomitaPositiveRoot x)
    ((LinearPMap.mem_graph_iff scalarTomitaPositiveRoot).mpr ⟨x,rfl,rfl⟩)
  obtain ⟨u,hu⟩ := hg
  have he : u=Submodule.inclusion scalarTomitaRootDomain_le_closed x :=
    Subtype.ext (congrArg Prod.fst hu)
  have hs := congrArg Prod.snd hu
  change closedTomita u=scalarTomitaPolarFactor (scalarTomitaPositiveRoot x) at hs
  exact hs.symm.trans (congrArg closedTomita he)

theorem scalarClosedTomitaDomain_le_root : closedTomitaDomain ≤ scalarTomitaPositiveRoot.domain := by
  intro x hx
  let u : RegularHilbert F := coefficientUnitary.symm x
  let y := closedTomita ⟨x,hx⟩
  let v : RegularHilbert F := coefficientUnitary.symm y
  have hu : coefficientUnitary u = x := coefficientUnitary.apply_symm_apply x
  have hv : coefficientUnitary v = y := coefficientUnitary.apply_symm_apply y
  have hg : (x,y) ∈ ClosedTomitaSquareGraph.graph actualClosedInput := ⟨⟨x,hx⟩,rfl⟩
  have hg' : (coefficientUnitary u,coefficientUnitary v) ∈ ClosedTomitaSquareGraph.graph actualClosedInput :=
    Eq.mpr (congrArg (fun p : GNSHilbert × GNSHilbert =>
      p ∈ ClosedTomitaSquareGraph.graph actualClosedInput) (Prod.ext hu hv)) hg
  have hc : (u,v) ∈ CanonicalFockCoefficientIntervals.coefficientGraph :=
    (CanonicalFockCoefficientIntervals.coefficientGraph_mem u v).mpr ((target_graph_mem_iff _ _).mp hg')
  have hs : (u,v) ∈ CoefficientTomitaSquare.graph coefficientRoot coefficientJ :=
    Eq.mpr (congrArg (fun S : Set (RegularHilbert F × RegularHilbert F) => (u,v) ∈ S)
      coefficient_graph_eq_GNS) hc
  have hmem : coefficientUnitary u ∈ scalarTomitaPositiveRoot.domain :=
    GenericPolarGraphTransport.mapped_domain_of_polar_graph coefficientUnitary
      coefficientRoot scalarTomitaPositiveRoot coefficientJ root_coefficient_graph_iff u v hs
  exact Eq.mp (congrArg (fun a : GNSHilbert => a ∈ scalarTomitaPositiveRoot.domain) hu) hmem

theorem scalarTomitaRootDomain_eq_closed : scalarTomitaPositiveRoot.domain=closedTomitaDomain :=
  le_antisymm scalarTomitaRootDomain_le_closed scalarClosedTomitaDomain_le_root

theorem scalarTomitaPositiveRoot_selfadjoint : IsSelfAdjoint scalarTomitaPositiveRoot :=
  resolventSquareRoot_selfadjoint _ scalarTomitaResolvent_nonneg
    scalarTomitaResolvent_injective scalarTomitaResolvent_le_one

theorem scalarTomitaPositiveRoot_dense : Dense (scalarTomitaPositiveRoot.domain:Set GNSHilbert) :=
  resolventSquareRoot_dense _ scalarTomitaResolvent_nonneg scalarTomitaResolvent_injective

theorem scalarTomitaPositiveRoot_zero_only (x:scalarTomitaPositiveRoot.domain)
    (hz:scalarTomitaPositiveRoot x=0) : (x:GNSHilbert)=0 := by
  have he := scalarTomitaPolarFactor_root x
  have hs : closedTomita (Submodule.inclusion scalarTomitaRootDomain_le_closed x)=0 :=
    he.symm.trans ((congrArg scalarTomitaPolarFactor hz).trans (map_zero scalarTomitaPolarFactor))
  have hh := CanonicalFockWeightClosedTomita.involutive
    (Submodule.inclusion scalarTomitaRootDomain_le_closed x)
  have hez : (⟨closedTomita (Submodule.inclusion scalarTomitaRootDomain_le_closed x),
      CanonicalFockWeightClosedTomita.maps_domain _⟩:closedTomitaDomain)=0 := Subtype.ext hs
  have hz2 : closedTomita ⟨closedTomita (Submodule.inclusion scalarTomitaRootDomain_le_closed x),
      CanonicalFockWeightClosedTomita.maps_domain _⟩ = 0 :=
    (congrArg closedTomita hez).trans (map_zero closedTomita)
  exact hh.symm.trans hz2

theorem scalarTomitaPositiveRoot_denseRange : DenseRange scalarTomitaPositiveRoot.toFun :=
  partialSelfadjoint_denseRange scalarTomitaPositiveRoot scalarTomitaPositiveRoot_dense
    scalarTomitaPositiveRoot_selfadjoint scalarTomitaPositiveRoot_zero_only
end F1Fecho.CanonicalFockWeightPolar
#print axioms F1Fecho.CanonicalFockWeightPolar.root_coefficient_graph_iff
#print axioms F1Fecho.CanonicalFockWeightPolar.polar_graph
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaRootDomain_le_closed
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolarFactor_root
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarClosedTomitaDomain_le_root
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaRootDomain_eq_closed
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaPositiveRoot_selfadjoint
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaPositiveRoot_zero_only
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaPositiveRoot_denseRange

-- END DERIVED BODY CanonicalFockWeightPolarR6
