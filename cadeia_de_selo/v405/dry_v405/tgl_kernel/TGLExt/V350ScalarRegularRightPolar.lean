import TGLExt.V350ScalarRegularRightSquare
import TGLExt.V350ScalarTomitaPolarInvolution

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit.Continuous049
noncomputable section

/-- Commutation is transferred from the full domain of A to its actual
bounded inverse (I+A)^(-1), using both inverse equations already proved. -/
theorem scalarTomitaResolvent_regular_right_commutes (P : SiteProfile) (t : ℝ) :
    Commute (scalarTomitaResolvent P) (regularRightGNS P t) := by
  apply ContinuousLinearMap.ext
  intro z
  obtain ⟨x,hx,he⟩ := scalarTomitaResolvent_equation P z
  calc
    _ = scalarTomitaResolvent P
        (regularRightGNS P t ((x : ScalarGNSHilbert P)+scalarTomitaSquare P x)) := by rw [he]; rfl
    _ = scalarTomitaResolvent P
        ((scalarRegularRightSquareInput P t x : ScalarGNSHilbert P)+
          scalarTomitaSquare P (scalarRegularRightSquareInput P t x)) := by
      rw [map_add,scalarTomitaSquare_regular_right_commutes]
      rfl
    _ = (scalarRegularRightSquareInput P t x : ScalarGNSHilbert P) :=
      scalarTomitaResolvent_inverse P _
    _ = _ := congrArg (regularRightGNS P t) hx

theorem scalarTomitaPositiveRoot_regular_right_graph (P : SiteProfile) (t : ℝ)
    (x : (scalarTomitaPositiveRoot P).domain) :
    (regularRightGNS P t (x : ScalarGNSHilbert P),
      regularRightGNS P t (scalarTomitaPositiveRoot P x)) ∈ (scalarTomitaPositiveRoot P).graph :=
  resolvent_sqrt_graph_transport_of_commute (scalarTomitaResolvent P) (regularRightGNS P t)
    (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_injective P)
    (scalarTomitaResolvent_regular_right_commutes P t) _ _
    ((LinearPMap.mem_graph_iff (scalarTomitaPositiveRoot P)).mpr ⟨x,rfl,rfl⟩)

theorem scalarRegularRight_mem_rootDomain (P : SiteProfile) (t : ℝ)
    (x : (scalarTomitaPositiveRoot P).domain) :
    regularRightGNS P t (x : ScalarGNSHilbert P) ∈ (scalarTomitaPositiveRoot P).domain := by
  obtain ⟨u,hu,_⟩ := (LinearPMap.mem_graph_iff (scalarTomitaPositiveRoot P)).mp
    (scalarTomitaPositiveRoot_regular_right_graph P t x)
  change (u : ScalarGNSHilbert P)=regularRightGNS P t (x : ScalarGNSHilbert P) at hu
  rw [← hu]
  exact u.property

def scalarRegularRightRootInput (P : SiteProfile) (t : ℝ)
    (x : (scalarTomitaPositiveRoot P).domain) : (scalarTomitaPositiveRoot P).domain :=
  ⟨regularRightGNS P t (x : ScalarGNSHilbert P),scalarRegularRight_mem_rootDomain P t x⟩

theorem scalarTomitaPositiveRoot_regular_right_commutes (P : SiteProfile) (t : ℝ)
    (x : (scalarTomitaPositiveRoot P).domain) :
    scalarTomitaPositiveRoot P (scalarRegularRightRootInput P t x) =
      regularRightGNS P t (scalarTomitaPositiveRoot P x) := by
  obtain ⟨u,hu,hBu⟩ := (LinearPMap.mem_graph_iff (scalarTomitaPositiveRoot P)).mp
    (scalarTomitaPositiveRoot_regular_right_graph P t x)
  have he : scalarRegularRightRootInput P t x=u := Subtype.ext hu.symm
  rw [he]
  exact hBu

theorem scalarRegularRight_rootDomain_iff (P : SiteProfile) (t : ℝ)
    (x : ScalarGNSHilbert P) :
    regularRightGNS P t x ∈ (scalarTomitaPositiveRoot P).domain ↔
      x ∈ (scalarTomitaPositiveRoot P).domain := by
  constructor
  · intro hx
    have h := scalarRegularRight_mem_rootDomain P (-t) ⟨regularRightGNS P t x,hx⟩
    change (regularRightGNS P (-t) * regularRightGNS P t) x ∈ _ at h
    simpa only [regularRightGNS_mul,neg_add_cancel,regularRightGNS_zero,
      one_apply_eq_self] using h
  · intro hx
    exact scalarRegularRight_mem_rootDomain P t ⟨x,hx⟩

/-- The actual polar antiunitary exchanges this right action with left
multiplication. The extension uses the dense image of the SAME positive root. -/
theorem scalarTomitaPolarFactor_regular_right (P : SiteProfile) (t : ℝ)
    (z : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P (regularRightGNS P t z) =
      scalarGNSRepresentation P (star (regularRightCoreElement P t))
        (scalarTomitaPolarFactor P z) := by
  refine (scalarTomitaPositiveRoot_denseRange P).induction ?_
    (isClosed_eq (by fun_prop) (by fun_prop)) z
  rintro _ ⟨x,rfl⟩
  have he : Submodule.inclusion (scalarTomitaRootDomain_le_closed P)
      (scalarRegularRightRootInput P t x) =
    scalarRegularRightClosedTomitaInput P t
      (Submodule.inclusion (scalarTomitaRootDomain_le_closed P) x) := Subtype.ext rfl
  calc
    _ = scalarTomitaPolarFactor P
        (scalarTomitaPositiveRoot P (scalarRegularRightRootInput P t x)) :=
      congrArg (scalarTomitaPolarFactor P) (scalarTomitaPositiveRoot_regular_right_commutes P t x).symm
    _ = scalarClosedTomita P (Submodule.inclusion (scalarTomitaRootDomain_le_closed P)
        (scalarRegularRightRootInput P t x)) := scalarTomitaPolarFactor_root P _
    _ = scalarClosedTomita P (scalarRegularRightClosedTomitaInput P t
        (Submodule.inclusion (scalarTomitaRootDomain_le_closed P) x)) :=
      congrArg (scalarClosedTomita P) he
    _ = scalarGNSRepresentation P (star (regularRightCoreElement P t))
        (scalarClosedTomita P (Submodule.inclusion (scalarTomitaRootDomain_le_closed P) x)) :=
      scalarClosedTomita_regular_right_intertwines P t _
    _ = _ := congrArg (scalarGNSRepresentation P (star (regularRightCoreElement P t)))
      (scalarTomitaPolarFactor_root P x).symm

theorem scalarTomitaPolar_conjugate_regular_right (P : SiteProfile) (t : ℝ) :
    antiunitaryConjugate (scalarTomitaPolarFactor P) (regularRightGNS P t) =
      scalarGNSRepresentation P (star (regularRightCoreElement P t)) := by
  apply ContinuousLinearMap.ext
  intro x
  have h := scalarTomitaPolarFactor_regular_right P t ((scalarTomitaPolarFactor P).symm x)
  simpa only [antiunitaryConjugate_apply,LinearIsometryEquiv.apply_symm_apply] using h

theorem scalarTomitaPolarFactor_regular_left (P : SiteProfile) (t : ℝ)
    (z : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P
      (scalarGNSRepresentation P (star (regularRightCoreElement P t)) z) =
        regularRightGNS P t (scalarTomitaPolarFactor P z) := by
  have h := congrArg (scalarTomitaPolarFactor P)
    (scalarTomitaPolarFactor_regular_right P t (scalarTomitaPolarFactor P z))
  simpa only [scalarTomitaPolarFactor_involutive P z,
    scalarTomitaPolarFactor_involutive P (regularRightGNS P t (scalarTomitaPolarFactor P z))] using h.symm

#print axioms scalarTomitaResolvent_regular_right_commutes
#print axioms scalarTomitaPositiveRoot_regular_right_graph
#print axioms scalarRegularRight_mem_rootDomain
#print axioms scalarRegularRightRootInput
#print axioms scalarTomitaPositiveRoot_regular_right_commutes
#print axioms scalarRegularRight_rootDomain_iff
#print axioms scalarTomitaPolarFactor_regular_right
#print axioms scalarTomitaPolar_conjugate_regular_right
#print axioms scalarTomitaPolarFactor_regular_left
end
end TGLV350.Regular
