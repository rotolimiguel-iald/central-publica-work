import TGLExt.F1Fecho394.MaxwellCanonicalWedgeR2
import TGLExt.F1Fecho394.PhysicalLocalizedSubspacesR3

/-! The actual support-generated closed real subspace is contained in the
canonical standard right wedge. Equality remains a distinct obligation. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellLocalization
open F1Fecho.MaxwellGlobal F1Fecho.MaxwellStrip TGLExt.ImportedSQ
open F1Rede.CanonicalWedge

def physicalRightWedge : Set Spacetime := {x | |x 0| < x 1}

theorem localized_rightWedge_le_KWR :
    localized physicalRightWedge ≤ KWR.toClosedSubmodule.toSubmodule := by
  apply Submodule.topologicalClosure_minimal
    (Submodule.span ℝ (supportedGenerators physicalRightWedge))
  · apply Submodule.span_le.mpr
    rintro v ⟨f,hr,hs,rfl⟩
    exact circularSmear_mem_KWR f (fun x hx => hs hx) hr
  · exact KWR.toClosedSubmodule.isClosed

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.localized_rightWedge_le_KWR
