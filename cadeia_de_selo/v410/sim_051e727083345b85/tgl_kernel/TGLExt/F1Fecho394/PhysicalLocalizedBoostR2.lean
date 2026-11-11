import TGLExt.F1Fecho394.PhysicalSmearBoostR2

/-! Boost covariance for every physical region, with the actual supported
Maxwell tests. No causal locality or wedge equality is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.MaxwellLocalization
open TGLExt TGLExt.ImportedSQ F1Fecho.MaxwellGlobal F1Fecho.OrbitalScreen
open F1Fecho.SpacetimeLorentz F1Fecho.PhysicalTensorLorentz

def boostRegion (s:ℝ) (O:Set Spacetime) : Set Spacetime := action (theBoost s) '' O

theorem boost_action_neg (s:ℝ) (x:Spacetime) :
    action (theBoost (-s)) (action (theBoost s) x)=x := by
  rw [←F1Fecho.OrbitalSpatial.theBoost_inv_eq]
  exact (action (theBoost s)).symm_apply_apply x

theorem boostRegion_inverse (s:ℝ) (O:Set Spacetime) :
    boostRegion (-s) (boostRegion s O)=O := by
  ext x
  constructor
  · rintro ⟨y,⟨z,hz,rfl⟩,rfl⟩
    simpa only [boost_action_neg] using hz
  · intro hx
    exact ⟨action (theBoost s) x,⟨x,hx,rfl⟩,boost_action_neg s x⟩

theorem boosted_generator (s:ℝ) (O:Set Spacetime) (v:H1)
    (hv:v∈supportedGenerators O) :
    B0 s v∈supportedGenerators (boostRegion s O) := by
  obtain ⟨f,hr,hs,rfl⟩:=hv
  exact ⟨transform (theBoost s) f,transform_real _ f hr,
    (transform_support _ f).trans (Set.image_mono hs),circularSmear_boost s f⟩

theorem localized_boost (s:ℝ) (O:Set Spacetime) (v:H1)
    (hv:v∈localized O) : B0 s v∈localized (boostRegion s O) := by
  let T:H1→L[ℝ]H1:=(B0 s).toLinearIsometry.toContinuousLinearMap.restrictScalars ℝ
  have hs:(Submodule.span ℝ (supportedGenerators O)).map T.toLinearMap≤
      Submodule.span ℝ (supportedGenerators (boostRegion s O)) := by
    rw [Submodule.map_span]
    apply Submodule.span_le.mpr
    rintro w ⟨x,hx,rfl⟩
    exact Submodule.subset_span (boosted_generator s O x hx)
  exact (Submodule.topologicalClosure_mono hs)
    ((Submodule.topologicalClosure_map T _) (Submodule.mem_map.mpr ⟨v,hv,rfl⟩))

theorem localized_boost_iff (s:ℝ) (O:Set Spacetime) (v:H1) :
    v∈localized O ↔ B0 s v∈localized (boostRegion s O) := by
  constructor
  · exact localized_boost s O v
  · intro hv
    have h:=localized_boost (-s) (boostRegion s O) (B0 s v) hv
    rw [boostRegion_inverse] at h
    have hi:B0 (-s) (B0 s v)=v := by
      have hh:=congrArg (fun u:H1≃ₗᵢ[ℂ]H1=>u v) (B0_add (-s) s)
      rw [neg_add_cancel,B0_zero] at hh
      exact hh.symm
    rwa [hi] at h

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.boostRegion_inverse
#print axioms F1Fecho.MaxwellLocalization.localized_boost
#print axioms F1Fecho.MaxwellLocalization.localized_boost_iff
