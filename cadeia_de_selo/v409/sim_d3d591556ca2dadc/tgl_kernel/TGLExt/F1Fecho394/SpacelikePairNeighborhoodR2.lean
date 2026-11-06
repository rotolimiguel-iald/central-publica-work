import TGLExt.F1Fecho394.SpacelikePairWedgesR2

/-! Open neighborhoods, not only points, fit into the opposite wedges supplied
by the spacelike-pair construction. This is the local geometric input for
partitioning compact physical test supports. -/
set_option autoImplicit false
set_option maxHeartbeats 500000
noncomputable section
namespace F1Fecho.SpacelikeGeometry
open TGL.SpecificAQFT F1Fecho.OrbitalSpatial F1Fecho.OrbitalScreen ChatgptAudit.WignerOrbit016

def frameMap (L : generatedLorentz) (m : V) (z : V) : V := lorentzLinear L.val (z-m)

def frameRightRegion (L : generatedLorentz) (m : V) : Set V :=
  frameMap L m ⁻¹' rightWedge

def frameLeftRegion (L : generatedLorentz) (m : V) : Set V :=
  frameMap L m ⁻¹' leftWedge

theorem frameMap_continuous (L : generatedLorentz) (m : V) : Continuous (frameMap L m) :=
  (lorentzLinear L.val).continuous_of_finiteDimensional.comp (continuous_id.sub continuous_const)

theorem frameRightRegion_open (L : generatedLorentz) (m : V) : IsOpen (frameRightRegion L m) :=
  (isOpen_lt (continuous_apply 0).abs (continuous_apply 1)).preimage (frameMap_continuous L m)

theorem frameLeftRegion_open (L : generatedLorentz) (m : V) : IsOpen (frameLeftRegion L m) :=
  (isOpen_lt (continuous_apply 0).abs (continuous_apply 1).neg).preimage (frameMap_continuous L m)

theorem spacelike_pair_opposite_neighborhoods (x y : V) (hxy : minkowskiSq (x-y)<0) :
    ∃ L : generatedLorentz, ∃ m : V, ∃ r s : ℝ,
      0<r ∧ 0<s ∧ Metric.ball x r ⊆ frameRightRegion L m ∧
        Metric.ball y s ⊆ frameLeftRegion L m := by
  obtain ⟨L,m,hx,hy⟩ := spacelike_pair_opposite_wedges x y hxy
  obtain ⟨r,hr,hxr⟩ := Metric.isOpen_iff.mp (frameRightRegion_open L m) x hx
  obtain ⟨s,hs,hys⟩ := Metric.isOpen_iff.mp (frameLeftRegion_open L m) y hy
  exact ⟨L,m,r,s,hr,hs,hxr,hys⟩

end F1Fecho.SpacelikeGeometry
#print axioms F1Fecho.SpacelikeGeometry.frameRightRegion_open
#print axioms F1Fecho.SpacelikeGeometry.frameLeftRegion_open
#print axioms F1Fecho.SpacelikeGeometry.spacelike_pair_opposite_neighborhoods
