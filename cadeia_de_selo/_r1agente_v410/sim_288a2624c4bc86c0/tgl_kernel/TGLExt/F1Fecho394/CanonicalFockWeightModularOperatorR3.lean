import TGLExt.F1Fecho394.ClosedTomitaOperatorR1
import TGLExt.F1Fecho394.CanonicalFockWeightClosedTomitaR2
/-! Instantiation of the generic closed-involution construction with the already
constructed Tomita operator of the actual scalar dual-weight GNS space.
Every input field is paid by the preceding concrete construction. -/
set_option autoImplicit false
set_option maxErrors 2
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockWeightModularOperator
open TGLExt TGLV350.Regular F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockWeightClosedTomita
local instance : PartialOrder (GNSHilbert →L[ℂ] GNSHilbert) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := GNSHilbert)
def actualClosedInput : F1Fecho.ClosedTomitaOperator.Input GNSHilbert where
  domain := closedTomitaDomain
  operator := closedTomita
  dense := domain_dense
  closed := graph_closed
  maps_domain := maps_domain
  involutive := involutive
abbrev scalarTomitaAdjoint := F1Fecho.ClosedTomitaOperator.scalarTomitaAdjoint actualClosedInput
abbrev scalarTomitaSquare := F1Fecho.ClosedTomitaOperator.scalarTomitaSquare actualClosedInput
abbrev scalarTomitaResolvent := F1Fecho.ClosedTomitaOperator.scalarTomitaResolvent actualClosedInput

theorem scalarTomitaSquare_domain_iff (x : GNSHilbert) :
    x ∈ scalarTomitaSquare.domain ↔ ∃ hx : x ∈ closedTomitaDomain,
      closedTomita ⟨x,hx⟩ ∈ scalarTomitaAdjoint.domain := Iff.rfl

theorem scalarTomitaSquare_pairing (x : scalarTomitaSquare.domain) (y : closedTomitaDomain) :
    inner ℂ (scalarTomitaSquare x) (y : GNSHilbert) =
      inner ℂ (closedTomita y)
        (closedTomita (F1Fecho.ClosedTomitaOperator.scalarTomitaSquareInput actualClosedInput x)) :=
  F1Fecho.ClosedTomitaOperator.scalarTomitaSquare_pairing actualClosedInput x y

theorem scalarTomitaSquare_positive (x : scalarTomitaSquare.domain) :
    0 ≤ (inner ℂ (x : GNSHilbert) (scalarTomitaSquare x)).re :=
  F1Fecho.ClosedTomitaOperator.scalarTomitaSquare_positive actualClosedInput x

theorem scalarTomitaSquare_domain_dense : Dense (scalarTomitaSquare.domain : Set GNSHilbert) :=
  F1Fecho.ClosedTomitaOperator.scalarTomitaSquare_domain_dense actualClosedInput

theorem scalarTomitaSquare_selfadjoint : IsSelfAdjoint scalarTomitaSquare :=
  F1Fecho.ClosedTomitaOperator.scalarTomitaSquare_selfadjoint actualClosedInput

theorem scalarTomitaSquare_isClosed : scalarTomitaSquare.IsClosed :=
  F1Fecho.ClosedTomitaOperator.scalarTomitaSquare_isClosed actualClosedInput

theorem scalarTomitaSquare_zero_only (x : scalarTomitaSquare.domain)
    (h : scalarTomitaSquare x = 0) : (x : GNSHilbert) = 0 :=
  F1Fecho.ClosedTomitaOperator.scalarTomitaSquare_zero_only actualClosedInput x h

theorem scalarTomitaResolvent_equation (z : GNSHilbert) :
    ∃ x : scalarTomitaSquare.domain, (x : GNSHilbert) = scalarTomitaResolvent z ∧
      (x : GNSHilbert)+scalarTomitaSquare x = z :=
  F1Fecho.ClosedTomitaOperator.scalarTomitaResolvent_equation actualClosedInput z

theorem scalarTomitaResolvent_inverse (x : scalarTomitaSquare.domain) :
    scalarTomitaResolvent ((x : GNSHilbert)+scalarTomitaSquare x) = (x : GNSHilbert) :=
  F1Fecho.ClosedTomitaOperator.scalarTomitaResolvent_inverse actualClosedInput x

theorem scalarTomitaResolvent_injective : Function.Injective scalarTomitaResolvent :=
  F1Fecho.ClosedTomitaOperator.scalarTomitaResolvent_injective actualClosedInput

theorem scalarTomitaResolvent_nonneg : 0 ≤ scalarTomitaResolvent :=
  F1Fecho.ClosedTomitaOperator.scalarTomitaResolvent_nonneg actualClosedInput

theorem scalarTomitaResolvent_le_one : scalarTomitaResolvent ≤ 1 :=
  F1Fecho.ClosedTomitaOperator.scalarTomitaResolvent_le_one actualClosedInput

theorem scalarTomitaResolvent_graph :
    resolventGraphOperator (H := GNSHilbert) scalarTomitaResolvent scalarTomitaResolvent_injective =
      scalarTomitaSquare :=
  F1Fecho.ClosedTomitaOperator.scalarTomitaResolvent_graph actualClosedInput

end F1Fecho.CanonicalFockWeightModularOperator
#print axioms F1Fecho.CanonicalFockWeightModularOperator.actualClosedInput
#print axioms F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaAdjoint
#print axioms F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaSquare
#print axioms F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaResolvent
#print axioms F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaSquare_domain_iff
#print axioms F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaSquare_pairing
#print axioms F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaSquare_positive
#print axioms F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaSquare_domain_dense
#print axioms F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaSquare_selfadjoint
#print axioms F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaSquare_isClosed
#print axioms F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaSquare_zero_only
#print axioms F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaResolvent_equation
#print axioms F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaResolvent_inverse
#print axioms F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaResolvent_injective
#print axioms F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaResolvent_nonneg
#print axioms F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaResolvent_le_one
#print axioms F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaResolvent_graph
