import TGLExt.V350MatrixUnitResolventScaling
import TGLExt.V350ScaledRootGraphTransport
import TGLExt.V350ScalarTomitaPositiveRoot

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit
noncomputable section

theorem matrixUnit_positiveRoot_graph_scaling (P : SiteProfile) (N : ℕ)
    (i j : chainIdx N) (x : (scalarTomitaPositiveRoot P).domain) :
    (homogeneousRightGNS (matrixUnitRightData P N i j) (x : ScalarGNSHilbert P),
      (Real.sqrt (localEigenvalue P N i j) : ℂ) •
        homogeneousRightGNS (matrixUnitRightData P N i j) (scalarTomitaPositiveRoot P x)) ∈
      (scalarTomitaPositiveRoot P).graph :=
  resolvent_root_graph_scaled (scalarTomitaResolvent P)
    (homogeneousRightGNS (matrixUnitRightData P N i j))
    (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_le_one P)
    (scalarTomitaResolvent_injective P) (localEigenvalue P N i j)
    (localEigenvalue_pos (P := P) N i j) (matrixUnit_resolvent_right_scaling P N i j) _ _
    ((LinearPMap.mem_graph_iff (scalarTomitaPositiveRoot P)).mpr ⟨x,rfl,rfl⟩)

theorem matrixUnit_mem_rootDomain (P : SiteProfile) (N : ℕ)
    (i j : chainIdx N) (x : (scalarTomitaPositiveRoot P).domain) :
    homogeneousRightGNS (matrixUnitRightData P N i j) (x : ScalarGNSHilbert P) ∈
      (scalarTomitaPositiveRoot P).domain := by
  obtain ⟨u,hu,_⟩ := (LinearPMap.mem_graph_iff (scalarTomitaPositiveRoot P)).mp
    (matrixUnit_positiveRoot_graph_scaling P N i j x)
  change (u : ScalarGNSHilbert P)=homogeneousRightGNS (matrixUnitRightData P N i j)
    (x : ScalarGNSHilbert P) at hu
  rw [← hu]
  exact u.property

def matrixUnitRightRootInput (P : SiteProfile) (N : ℕ)
    (i j : chainIdx N) (x : (scalarTomitaPositiveRoot P).domain) : (scalarTomitaPositiveRoot P).domain :=
  ⟨homogeneousRightGNS (matrixUnitRightData P N i j) (x : ScalarGNSHilbert P),
    matrixUnit_mem_rootDomain P N i j x⟩

/-- The scaled relation holds on EVERY vector of the actual root domain.
No spectral ansatz or separate Hilbert realization replaces this B. -/
theorem matrixUnit_positiveRoot_right_scaling (P : SiteProfile) (N : ℕ)
    (i j : chainIdx N) (x : (scalarTomitaPositiveRoot P).domain) :
    scalarTomitaPositiveRoot P (matrixUnitRightRootInput P N i j x) =
      (Real.sqrt (localEigenvalue P N i j) : ℂ) •
        homogeneousRightGNS (matrixUnitRightData P N i j) (scalarTomitaPositiveRoot P x) := by
  obtain ⟨u,hu,hBu⟩ := (LinearPMap.mem_graph_iff (scalarTomitaPositiveRoot P)).mp
    (matrixUnit_positiveRoot_graph_scaling P N i j x)
  have he : matrixUnitRightRootInput P N i j x=u := Subtype.ext hu.symm
  rw [he]
  exact hBu

#print axioms matrixUnit_positiveRoot_graph_scaling
#print axioms matrixUnit_mem_rootDomain
#print axioms matrixUnitRightRootInput
#print axioms matrixUnit_positiveRoot_right_scaling
end
end TGLV350.Regular
