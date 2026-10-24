import TGLExt.F1Fecho394.SectorDirectSum
import Mathlib.Analysis.InnerProductSpace.Orthonormal
import Mathlib.LinearAlgebra.Dimension.Finite
/-! A unit vector in each particle sector produces an infinite orthonormal
family in the Hilbert sum. The application must supply these vectors from
the actual sectors; non-vacuity is not an assumption about a Fock certificate. -/
set_option autoImplicit false
noncomputable section
open scoped InnerProductSpace

namespace F1Rede.SectorDirectSum
variable {E : ℕ → Type*} [∀ n, NormedAddCommGroup (E n)]
  [∀ n, InnerProductSpace ℂ (E n)] [∀ n, CompleteSpace (E n)]

theorem sector_vectors_orthonormal (e : ∀ n, E n) (he : ∀ n, ‖e n‖ = 1) :
    Orthonormal ℂ (fun n => sectorEmbedding n (e n)) := by
  constructor
  · intro n
    rw [(sectorEmbedding n).norm_map, he n]
  · intro n m hnm
    exact different_sectors_orthogonal n m hnm (e n) (e m)

theorem infinite_dimensional (e : ∀ n, E n) (he : ∀ n, ‖e n‖ = 1) :
    ¬ FiniteDimensional ℂ (SumSpace E) := by
  intro h
  letI := h
  exact Module.Finite.not_linearIndependent_of_infinite
    (fun n => sectorEmbedding n (e n))
    (sector_vectors_orthonormal e he).linearIndependent

end F1Rede.SectorDirectSum

#print axioms F1Rede.SectorDirectSum.sector_vectors_orthonormal
#print axioms F1Rede.SectorDirectSum.infinite_dimensional
