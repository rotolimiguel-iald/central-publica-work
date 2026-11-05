import TGLExt.F1Fecho394.PhysicalWedgeSchwartzClosureR3
import TGLExt.F1Fecho394.PhysicalSmearBoostR2
import TGLExt.F1Fecho394.PhysicalSmearDensityR6
import TGLExt.F1Fecho394.CanonicalOutput
import TGLExt.F1Fecho394.PhysicalNetGeometryR1

/-! Final physical right-wedge consumer. Global density is supplied by the
explicit Maxwell dual tensor and compact off-axis profiles, not assumed.
This identifies the actual supported-test subspace with canonical KWR on
the same H1. Causal locality for arbitrary regions remains a separate theorem.
-/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellLocalization
open TGLExt.ImportedSQ F1Fecho.MaxwellGlobal F1Fecho.OrbitalScreen
open F1Rede.CanonicalWedge

theorem circularSmear_denseRange : DenseRange circularSmear :=
  circularH1.symm.surjective.denseRange.comp physicalSmear_denseRange
    circularH1.symm.continuous

theorem physical_right_wedge_complex_dense :
    (Submodule.span ℂ (localized physicalRightWedge:Set H1)).topologicalClosure=⊤ :=
  localized_complex_dense_of_global_density circularSmear_denseRange

theorem physical_right_wedge_eq_KWR :
    localized physicalRightWedge=KWR.toClosedSubmodule.toSubmodule :=
  localized_wedge_eq_KWR_of_complex_dense physical_right_wedge_complex_dense

theorem physicalNet_wedge_glue :
    physicalNet TGL.SpecificAQFT.rightWedge=KWR.toClosedSubmodule.toSubmodule :=
  physical_right_wedge_eq_KWR

theorem physical_right_wedge_nonzero :
    ∃ v:H1,v∈localized physicalRightWedge ∧ v≠0 := by
  obtain ⟨v,hv,hne⟩:=spectralOutput_nonzero
  refine ⟨v,?_,hne⟩
  rw [physical_right_wedge_eq_KWR]
  exact hv

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.circularSmear_denseRange
#print axioms F1Fecho.MaxwellLocalization.physical_right_wedge_complex_dense
#print axioms F1Fecho.MaxwellLocalization.physical_right_wedge_eq_KWR
#print axioms F1Fecho.MaxwellLocalization.physical_right_wedge_nonzero

#print axioms F1Fecho.MaxwellLocalization.physicalNet_wedge_glue
