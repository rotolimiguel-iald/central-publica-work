import TGLExt.V350ReducingCommutantTransport
import TGLExt.V350BoundedInjectivePolar
import TGLExt.V350SeparatingCyclicCommutant

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Compression of an arbitrary ambient operator; no multiplicativity is asserted. -/
def reducingOperatorCompression (S : Submodule ℂ H) [CompleteSpace S]
    (D : H →L[ℂ] H) : S →L[ℂ] S :=
  S.orthogonalProjectionOnto.comp (D.comp S.subtypeL)

theorem reducingCommutant_column_intertwines
    (M : VonNeumannAlgebra H) (S : Submodule ℂ H) [CompleteSpace S]
    (hS : ∀ a : M.toStarSubalgebra, ∀ v ∈ S, a.val v ∈ S)
    (D : H →L[ℂ] H) (hD : D ∈ M.commutant) (a : M.toStarSubalgebra) :
    (D.comp S.subtypeL).comp (reducingStarRepresentation M.toStarSubalgebra.subtype S hS a) =
      a.val.comp (D.comp S.subtypeL) := by
  ext1 x
  exact (congrArg (fun T : H →L[ℂ] H => T x.val)
    ((VonNeumannAlgebra.mem_commutant_iff.mp hD) a.val a.property)).symm

theorem reducingCommutant_compression_commutes
    (M : VonNeumannAlgebra H) (S : Submodule ℂ H) [CompleteSpace S]
    (hS : ∀ a : M.toStarSubalgebra, ∀ v ∈ S, a.val v ∈ S)
    (D : H →L[ℂ] H) (hD : D ∈ M.commutant) (a : M.toStarSubalgebra) :
    Commute (reducingOperatorCompression S D)
      (reducingStarRepresentation M.toStarSubalgebra.subtype S hS a) := by
  ext1 x
  change S.orthogonalProjectionOnto (D (a.val x.val)) =
    reducingStarRepresentation M.toStarSubalgebra.subtype S hS a
      (S.orthogonalProjectionOnto (D x.val))
  have he := congrArg (fun T : H →L[ℂ] H => T x.val)
    ((VonNeumannAlgebra.mem_commutant_iff.mp hD) a.val a.property)
  change a.val (D x.val) = D (a.val x.val) at he
  rw [← he]
  exact reducing_projection_intertwines M.toStarSubalgebra.subtype S hS a (D x.val)

theorem reducingCommutant_gram_commutes
    (M : VonNeumannAlgebra H) (S : Submodule ℂ H) [CompleteSpace S]
    (hS : ∀ a : M.toStarSubalgebra, ∀ v ∈ S, a.val v ∈ S)
    (D : H →L[ℂ] H) (hD : D ∈ M.commutant) (a : M.toStarSubalgebra) :
    Commute ((D.comp S.subtypeL).adjoint.comp (D.comp S.subtypeL))
      (reducingStarRepresentation M.toStarSubalgebra.subtype S hS a) := by
  apply boundedMapGram_commutes_of_intertwines (D.comp S.subtypeL) _ a.val
  · exact reducingCommutant_column_intertwines M S hS D hD a
  · rw [← map_star]
    exact reducingCommutant_column_intertwines M S hS D hD (star a)

/-- The estimate on the commutant orbit which makes the bicommutant lift bounded.
The hypothesis refers to the actual restricted image, not to an assumed closed image. -/
theorem reducingBicommutant_orbit_bound
    (M : VonNeumannAlgebra H) (S : Submodule ℂ H) [CompleteSpace S]
    (hS : ∀ a : M.toStarSubalgebra, ∀ v ∈ S, a.val v ∈ S)
    (B : S →L[ℂ] S)
    (hB : ∀ Q : S →L[ℂ] S,
      (∀ a : M.toStarSubalgebra,
        Commute Q (reducingStarRepresentation M.toStarSubalgebra.subtype S hS a)) →
      Commute B Q)
    (D : H →L[ℂ] H) (hD : D ∈ M.commutant) (v : S) :
    ‖D (B v).val‖ ≤ ‖B‖ * ‖D v.val‖ := by
  let C := D.comp S.subtypeL
  have hc : Commute (C.adjoint.comp C) B :=
    (hB _ (reducingCommutant_gram_commutes M S hS D hD)).symm
  have hs := positive_sqrt_commutes_of_commute (C.adjoint.comp C) B hc
  have he : boundedMapModulus C (B v) = B (boundedMapModulus C v) :=
    congrArg (fun T : S →L[ℂ] S => T v) hs.eq
  calc
    ‖D (B v).val‖ = ‖boundedMapModulus C (B v)‖ := (boundedMapModulus_norm C (B v)).symm
    _ = ‖B (boundedMapModulus C v)‖ := congrArg norm he
    _ ≤ ‖B‖ * ‖boundedMapModulus C v‖ := B.le_opNorm _
    _ = ‖B‖ * ‖D v.val‖ := congrArg (fun r : ℝ => ‖B‖ * r) (boundedMapModulus_norm C v)

#print axioms reducingOperatorCompression
#print axioms reducingCommutant_column_intertwines
#print axioms reducingCommutant_compression_commutes
#print axioms reducingCommutant_gram_commutes
#print axioms reducingBicommutant_orbit_bound
end
end TGLV350.Regular
