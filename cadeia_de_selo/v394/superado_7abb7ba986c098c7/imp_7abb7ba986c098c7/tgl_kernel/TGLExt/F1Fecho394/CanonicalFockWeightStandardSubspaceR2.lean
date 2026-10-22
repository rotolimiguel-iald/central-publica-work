import TGLExt.F1Fecho394.CanonicalFockWeightClosedTomitaR2
import TGLExt.F1Fecho394.CanonicalFockWeightGraphR3
import TGLExt.ClosedAntilinearStandardSubspace
/-! The standard real subspace associated with the actual scalar dual weight
of the regular Fock core, constructed from its closed densely defined
adjunction operator. This subspace belongs to the weight GNS Hilbert space;
it is not asserted to be the geometric one-particle wedge or the Fock wedge.
No equality with the geometric modular group or scaled trace is concluded. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockWeightStandardSubspace
open TGLExt F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockWeightClosedTomita

def weightStandardSubspace : StandardSubspace GNSHilbert :=
  ChatgptAudit.Continuous049.closedAntilinearStandardSubspace
    closedTomitaDomain closedTomita graph_closed maps_domain involutive domain_dense

theorem mem_weightStandardSubspace (x : GNSHilbert) :
    x ∈ weightStandardSubspace.toClosedSubmodule ↔
      ∃ hx : x ∈ closedTomitaDomain, closedTomita ⟨x,hx⟩ = x := Iff.rfl

theorem domain_fixed_sum (x : GNSHilbert) :
    x ∈ closedTomitaDomain ↔
      ∃ h k : GNSHilbert, h ∈ weightStandardSubspace.toClosedSubmodule ∧
        k ∈ weightStandardSubspace.toClosedSubmodule ∧ x = h + Complex.I • k :=
  ChatgptAudit.Continuous049.mem_domain_iff_fixed_sum
    closedTomitaDomain closedTomita maps_domain involutive x

-- Nonzero GNS vectors are already supplied by CanonicalFockWeightGraph.exists_nonzero_graph_input.

end F1Fecho.CanonicalFockWeightStandardSubspace
#print axioms F1Fecho.CanonicalFockWeightStandardSubspace.weightStandardSubspace
#print axioms F1Fecho.CanonicalFockWeightStandardSubspace.mem_weightStandardSubspace
#print axioms F1Fecho.CanonicalFockWeightStandardSubspace.domain_fixed_sum
