import TGLExt.F1Fecho394.PhysicalOppositeWedgeR4
import TGLExt.F1Fecho394.SpacelikePairNeighborhoodR2

/-! Physical Maxwell subspaces of translated Lorentz-frame wedges commute
symplectically. The proof transports actual test subspaces by the already
constructed translation and Lorentz unitaries. It does not assume locality.
Arbitrary region locality still requires support decomposition. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
namespace F1Fecho.MaxwellLocalization
open TGLExt.ImportedSQ F1Fecho.MaxwellGlobal F1Fecho.OrbitalScreen
open F1Fecho.OrbitalSpatial F1Fecho.SpacetimeLorentz

def physicalFrameRegion (L : generatedLorentz) (a : Spacetime)
    (W : Set Spacetime) : Set Spacetime := {x | action L.val (x-a) ∈ W}

theorem frame_region_transport (L : generatedLorentz) (a : Spacetime)
    (W : Set Spacetime) :
    lorentzRegion L (translateRegion (-a) (physicalFrameRegion L a W)) ⊆ W := by
  rintro z ⟨x,hx,rfl⟩
  change action L.val ((x-(-a))-a) ∈ W at hx
  simpa only [sub_neg_eq_add,add_sub_cancel_right] using hx

theorem localized_frame_transport (L : generatedLorentz) (a : Spacetime)
    (W : Set Spacetime) (v : H1) (hv : v ∈ localized (physicalFrameRegion L a W)) :
    helicityUnitary L (U1 (fun i => (-a) i) v) ∈ localized W :=
  localized_mono (frame_region_transport L a W)
    (localized_lorentz L _ _ (localized_translate (-a) _ v hv))

theorem physical_frame_opposite_symplectic (L : generatedLorentz) (a : Spacetime)
    (f g : H1)
    (hf : f ∈ localized (physicalFrameRegion L a physicalRightWedge))
    (hg : g ∈ localized (physicalFrameRegion L a physicalLeftWedge)) :
    (inner ℂ f g).im = 0 := by
  have h := physical_opposite_wedge_symplectic _ _
    (localized_frame_transport L a physicalRightWedge f hf)
    (localized_frame_transport L a physicalLeftWedge g hg)
  simpa only [LinearIsometryEquiv.inner_map_map] using h

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.frame_region_transport
#print axioms F1Fecho.MaxwellLocalization.localized_frame_transport
#print axioms F1Fecho.MaxwellLocalization.physical_frame_opposite_symplectic
