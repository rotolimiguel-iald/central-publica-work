import TGLExt.F1Fecho394.RegularScalarGNSStrongContinuityR1
import TGLExt.V350StrongBoundedApplication
set_option autoImplicit false
set_option maxErrors 2
set_option maxHeartbeats 1400000
noncomputable section
namespace F1Fecho.RegularScalarGNSJointContinuity
open TGLV350.Regular Filter F1Fecho.RegularScalarGNS F1Fecho.RegularScalarGNSRepresentation
open scoped Topology
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (D : Context H)
theorem representation_norm_le (B : D.algebra.toStarSubalgebra) :
    ‖scalarGNSRepresentation D B‖ ≤ ‖B.val‖ :=
  F1Fecho.RegularScalarGNSAction.scalarGNSAction_norm_le D B

theorem representation_joint_tendsto {ι : Type*} {l : Filter ι}
    (T : ι → D.algebra.toStarSubalgebra) (C : ℝ)
    (hb : ∀ i, ‖(T i).val‖ ≤ C)
    (hT : ∀ v, Tendsto (fun i => (T i).val v) l (𝓝 v))
    (v : ι → GNSHilbert D) (w : GNSHilbert D)
    (hv : Tendsto v l (𝓝 w)) :
    Tendsto (fun i => scalarGNSRepresentation D (T i) (v i)) l (𝓝 w) := by
  have hf : Tendsto (fun i => scalarGNSRepresentation D (T i) w) l (𝓝 w) := by
    have ht := F1Fecho.RegularScalarGNSStrongContinuity.scalarGNSRepresentation_tendsto_of_uniformly_bounded D T 1 C hb hT w
    simpa only [map_one,ContinuousLinearMap.one_apply] using ht
  exact bounded_application_tendsto (H := GNSHilbert D) l
    (fun i => scalarGNSRepresentation D (T i)) C
    (fun i => (representation_norm_le D (T i)).trans (hb i)) v w w hv hf
end F1Fecho.RegularScalarGNSJointContinuity
#print axioms F1Fecho.RegularScalarGNSJointContinuity.representation_norm_le
#print axioms F1Fecho.RegularScalarGNSJointContinuity.representation_joint_tendsto
