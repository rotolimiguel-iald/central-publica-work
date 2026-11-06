import TGLExt.V350DualOrbitVonNeumann
import TGLExt.V350FibreSlices
/-! Star-bicommutant transport for the already concrete dual-orbit representation. -/
set_option autoImplicit false
set_option maxErrors 2
set_option maxHeartbeats 800000
noncomputable section
namespace F1Fecho.RegularDualOrbitGenerated
open TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem dualOrbit_generated_mem (S : Set (RegularHilbert H →L[ℂ] RegularHilbert H))
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : A ∈ generatedAlgebra S) :
    dualOrbitRepresentation A ∈ generatedAlgebra ((dualOrbitRepresentation (H:=H)) '' S) := by
  have hf := fibre_generated_mem S A hA
  have ht := generated_transport (dualOrbitConjugation (H:=H)) (fibre '' S) (fibre A)
  rw [dualOrbitConjugation_fibre] at ht
  have he : dualOrbitConjugation (H:=H) '' (fibre '' S) = (dualOrbitRepresentation (H:=H)) '' S := by
    rw [Set.image_image]
    congr 1
    funext x
    exact dualOrbitConjugation_fibre x
  rw [he] at ht
  exact ht.mpr hf

theorem dualOrbit_commutes_of_generators
    (S : Set (RegularHilbert H →L[ℂ] RegularHilbert H))
    (Q : RegularHilbert (RegularHilbert H) →L[ℂ] RegularHilbert (RegularHilbert H))
    (hQ : Q ∈ StarSubalgebra.centralizer ℂ ((dualOrbitRepresentation (H:=H)) '' S))
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : A ∈ generatedAlgebra S) :
    dualOrbitRepresentation A * Q = Q * dualOrbitRepresentation A := by
  have h := dualOrbit_generated_mem S A hA
  change dualOrbitRepresentation A ∈ StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ ((dualOrbitRepresentation (H:=H)) '' S)) : Set _) at h
  exact ((StarSubalgebra.mem_centralizer_iff ℂ).mp h Q hQ).1.symm

end F1Fecho.RegularDualOrbitGenerated
#print axioms F1Fecho.RegularDualOrbitGenerated.dualOrbit_generated_mem
#print axioms F1Fecho.RegularDualOrbitGenerated.dualOrbit_commutes_of_generators
