import TGLExt.F1Fecho394.RealSubspaceTotalityR5
import TGLExt.F1Fecho394.FieldWeylR3
/-!
Araki cyclicity and separation on the already constructed canonical Fock space.
The field convention is W(f)=D(i f). No cyclicity/separation of the algebra is
assumed. Standardness is an input for general K and has an existing concrete
inhabitant KWR. This file does not identify the algebra-vacuum Tomita operator.
-/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.WedgeCyclic
open ClosedSubmodule
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential
open F1Fecho.WedgeExponential F1Fecho.FieldWeyl F1Fecho.WeylCoefficients

def vacuumOrbit (K : Submodule ℝ H1) : Set F :=
  (fun a : F →L[ℂ] F => a vacuum) '' (R K : Set (F →L[ℂ] F))

theorem orthogonal_vacuumOrbit_zero (K : StandardSubspace H1) (v : F)
    (hv : ∀ a ∈ R K.toClosedSubmodule.toSubmodule, inner ℂ v (a vacuum) = 0) :
    v = 0 := by
  apply exponential_real_subspace_orthogonal_zero K.mulI.toClosedSubmodule.toSubmodule
    (standard_complex_span_dense K.mulI) v
  intro x hx
  change x ∈ K.toClosedSubmodule.toSubmodule.map
    (scalarSMulCLE H1 Complex.UnitI).toLinearMap at hx
  obtain ⟨y,hy,rfl⟩ := hx
  have hw := hv (W y) (W_mem_R _ y hy)
  rw [W_vacuum] at hw
  have hp : amplitude (rotate y) 0 * inner ℂ v (exponential (rotate y)) = 0 := by
    simpa only [inner_smul_right] using hw
  exact (mul_eq_zero.mp hp).resolve_left (amplitude_ne_zero _ _)

theorem vacuum_cyclic (K : StandardSubspace H1) :
    Dense ((Submodule.span ℂ (vacuumOrbit K.toClosedSubmodule.toSubmodule) : Submodule ℂ F) : Set F) := by
  apply Submodule.dense_iff_topologicalClosure_eq_top.mpr
  apply Submodule.topologicalClosure_eq_top_iff.mpr
  apply le_antisymm _ bot_le
  intro v hv
  change v = 0
  apply orthogonal_vacuumOrbit_zero K v
  intro a ha
  exact (Submodule.mem_orthogonal' _ v).mp hv (a vacuum)
    (Submodule.subset_span ⟨a,ha,rfl⟩)

theorem vacuum_separating (K : StandardSubspace H1)
    (a : F →L[ℂ] F) (ha : a ∈ R K.toClosedSubmodule.toSubmodule)
    (h0 : a vacuum = 0) : a = 0 := by
  apply ContinuousLinearMap.ext_on (vacuum_cyclic K.symplComp)
  rintro x ⟨b,hb,rfl⟩
  have hsymp : ∀ f ∈ K.toClosedSubmodule.toSubmodule,
      ∀ g ∈ K.symplComp.toClosedSubmodule.toSubmodule, (inner ℂ f g).im = 0 := by
    intro f hf g hg
    exact ClosedSubmodule.mem_symplComp_iff.mp hg f hf
  have hc := R_local _ _ hsymp a ha b hb
  change a (b vacuum) = 0
  calc
    a (b vacuum) = (a*b) vacuum := rfl
    _ = (b*a) vacuum := congrArg (fun c : F →L[ℂ] F => c vacuum) hc.eq
    _ = b (a vacuum) := rfl
    _ = 0 := by rw [h0,map_zero]

theorem canonical_wedge_cyclic :
    Dense ((Submodule.span ℂ
      (vacuumOrbit F1Rede.CanonicalWedge.spectralOutput.KWR.toClosedSubmodule.toSubmodule) :
      Submodule ℂ F) : Set F) :=
  vacuum_cyclic F1Rede.CanonicalWedge.spectralOutput.KWR

theorem canonical_wedge_separating (a : F →L[ℂ] F)
    (ha : a ∈ R F1Rede.CanonicalWedge.spectralOutput.KWR.toClosedSubmodule.toSubmodule)
    (h0 : a vacuum = 0) : a = 0 :=
  vacuum_separating F1Rede.CanonicalWedge.spectralOutput.KWR a ha h0

end F1Fecho.WedgeCyclic
#print axioms F1Fecho.WedgeCyclic.orthogonal_vacuumOrbit_zero
#print axioms F1Fecho.WedgeCyclic.vacuum_cyclic
#print axioms F1Fecho.WedgeCyclic.vacuum_separating
#print axioms F1Fecho.WedgeCyclic.canonical_wedge_cyclic
#print axioms F1Fecho.WedgeCyclic.canonical_wedge_separating
