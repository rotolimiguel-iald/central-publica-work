import TGLExt.F1Fecho394.PhysicalSmearReflectionR6
import TGLExt.F1Fecho394.PhysicalSmearLorentzR3
import TGLExt.F1Fecho394.PhysicalCanonicalWedgeEqualityR3
import TGLExt.F1Fecho394.ScreenGeometricReflectionR4
import TGLExt.F1Fecho394.OneParticleDualityR2

/-! Opposite physical wedge duality on the actual Maxwell test net.
The proof uses the already constructed test-map inversion, physical Lorentz
covariance, canonical right-wedge equality and one-particle modular duality.
No causal-locality or left-wedge equality is supplied as a hypothesis.
Locality for arbitrary causally disjoint regions is a separate step. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
namespace F1Fecho.MaxwellLocalization
open TGLExt.ImportedSQ F1Fecho.MaxwellGlobal F1Fecho.OrbitalScreen
open F1Fecho.SpacetimeLorentz F1Rede.CanonicalWedge
open F1Fecho.OneParticleSymplectic F1Fecho.OneParticleDuality

def physicalLeftWedge : Set Spacetime := {x | |x 0| < -x 1}

theorem halfTurn_action_coordinates (x : Spacetime) :
    (fun i => action halfTurn.val x i) = ![x 0,x 1,-x 2,-x 3] :=
  (action_apply halfTurn.val x).trans (lorentzLinear_halfTurn (fun i => x i))

theorem reflected_right_subset_left :
    lorentzRegion halfTurn (inverseRegion physicalRightWedge) ⊆ physicalLeftWedge := by
  rintro z ⟨y,⟨x,hx,rfl⟩,rfl⟩
  have h0 := congrFun (halfTurn_action_coordinates (-x)) 0
  have h1 := congrFun (halfTurn_action_coordinates (-x)) 1
  change |action halfTurn.val (-x) 0| < -action halfTurn.val (-x) 1
  rw [h0,h1]
  change |-x 0| < -(-x 1)
  change |x 0| < x 1 at hx
  simpa only [abs_neg,neg_neg] using hx

theorem reflected_left_subset_right :
    lorentzRegion halfTurn (inverseRegion physicalLeftWedge) ⊆ physicalRightWedge := by
  rintro z ⟨y,⟨x,hx,rfl⟩,rfl⟩
  have h0 := congrFun (halfTurn_action_coordinates (-x)) 0
  have h1 := congrFun (halfTurn_action_coordinates (-x)) 1
  change |action halfTurn.val (-x) 0| < action halfTurn.val (-x) 1
  rw [h0,h1]
  change |-x 0| < -x 1
  change |x 0| < -x 1 at hx
  simpa only [abs_neg] using hx

theorem Jcandidate_physical_right_to_left (v : H1) (hv : v ∈ localized physicalRightWedge) :
    Jcandidate v ∈ localized physicalLeftWedge := by
  rw [Jcandidate_eq_helicity_halfTurn_Theta]
  exact localized_mono reflected_right_subset_left
    (localized_lorentz halfTurn _ _ (localized_inversion _ v hv))

theorem Jcandidate_physical_left_to_right (v : H1) (hv : v ∈ localized physicalLeftWedge) :
    Jcandidate v ∈ localized physicalRightWedge := by
  rw [Jcandidate_eq_helicity_halfTurn_Theta]
  exact localized_mono reflected_left_subset_right
    (localized_lorentz halfTurn _ _ (localized_inversion _ v hv))

theorem physical_left_wedge_eq_symplectic :
    localized physicalLeftWedge = KWR.symplComp.toClosedSubmodule.toSubmodule := by
  apply le_antisymm
  · intro v hv
    have hr := Jcandidate_physical_left_to_right v hv
    rw [physical_right_wedge_eq_KWR] at hr
    change v ∈ KWR.symplComp.toClosedSubmodule
    simpa only [Jcandidate_involutive v] using Jcandidate_into_symplectic (Jcandidate v) hr
  · intro v hv
    have hr := Jcandidate_of_symplectic v hv
    have hp : Jcandidate v ∈ localized physicalRightWedge := by
      rw [physical_right_wedge_eq_KWR]
      exact hr
    simpa only [Jcandidate_involutive v] using Jcandidate_physical_right_to_left (Jcandidate v) hp

theorem physical_opposite_wedge_symplectic (f g : H1)
    (hf : f ∈ localized physicalRightWedge) (hg : g ∈ localized physicalLeftWedge) :
    (inner ℂ f g).im = 0 := by
  rw [physical_right_wedge_eq_KWR] at hf
  rw [physical_left_wedge_eq_symplectic] at hg
  exact ClosedSubmodule.mem_symplComp_iff.mp hg f hf

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.Jcandidate_physical_right_to_left
#print axioms F1Fecho.MaxwellLocalization.Jcandidate_physical_left_to_right
#print axioms F1Fecho.MaxwellLocalization.physical_left_wedge_eq_symplectic
#print axioms F1Fecho.MaxwellLocalization.physical_opposite_wedge_symplectic
