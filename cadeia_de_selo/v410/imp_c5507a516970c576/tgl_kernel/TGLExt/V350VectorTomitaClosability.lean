import TGLExt.V350SeparatingCyclicCommutant

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The algebraic vector graph, with the ambient von Neumann algebra explicit. -/
def vectorTomitaGraph (N : VonNeumannAlgebra H) (v : H) : Set (H × H) :=
  {p | ∃ A : H →L[ℂ] H, A ∈ N ∧ p = (A v,(star A) v)}

theorem vectorTomita_pairing (N : VonNeumannAlgebra H) (v : H)
    (A B : H →L[ℂ] H) (hA : A ∈ N) (hB : B ∈ N.commutant) :
    inner ℂ ((star A) v) (B v) = inner ℂ ((star B) v) (A v) := by
  simp only [ContinuousLinearMap.star_eq_adjoint,ContinuousLinearMap.adjoint_inner_left]
  have hc := congrArg (fun T : H →L[ℂ] H => T v)
    ((VonNeumannAlgebra.mem_commutant_iff.mp hB) A hA)
  exact congrArg (fun z => inner ℂ v z) hc

theorem vectorTomita_closure_pairing (N : VonNeumannAlgebra H) (v : H)
    (p : H × H) (hp : p ∈ closure (vectorTomitaGraph N v))
    (B : H →L[ℂ] H) (hB : B ∈ N.commutant) :
    inner ℂ p.2 (B v) = inner ℂ ((star B) v) p.1 := by
  have hc : IsClosed {q : H × H |
      inner ℂ q.2 (B v) = inner ℂ ((star B) v) q.1} := by
    apply isClosed_eq <;> fun_prop
  apply closure_minimal (t := {q : H × H |
      inner ℂ q.2 (B v) = inner ℂ ((star B) v) q.1}) ?_ hc hp
  rintro q ⟨A,hA,rfl⟩
  exact vectorTomita_pairing N v A B hA hB

/-- Separating suffices for no vertical fibre in the closure. The N-orbit of
v need not be dense in the whole ambient Hilbert space. -/
theorem vectorTomita_closure_vertical (N : VonNeumannAlgebra H) (v : H)
    (hsep : ∀ A ∈ N, A v = 0 → A = 0)
    (y : H) (hy : (0,y) ∈ closure (vectorTomitaGraph N v)) : y = 0 := by
  apply (separating_commutant_orbit_dense N v hsep).eq_zero_of_inner_left (𝕜 := ℂ)
  intro B
  simpa only [inner_zero_right] using
    vectorTomita_closure_pairing N v (0,y) hy B.val B.property

theorem vectorTomita_closure_single_valued (N : VonNeumannAlgebra H) (v : H)
    (hsep : ∀ A ∈ N, A v = 0 → A = 0)
    (x y z : H) (hy : (x,y) ∈ closure (vectorTomitaGraph N v))
    (hz : (x,z) ∈ closure (vectorTomitaGraph N v)) : y = z := by
  apply (separating_commutant_orbit_dense N v hsep).eq_of_inner_left (𝕜 := ℂ)
  intro B
  exact (vectorTomita_closure_pairing N v (x,y) hy B.val B.property).trans
    (vectorTomita_closure_pairing N v (x,z) hz B.val B.property).symm

#print axioms vectorTomitaGraph
#print axioms vectorTomita_pairing
#print axioms vectorTomita_closure_pairing
#print axioms vectorTomita_closure_vertical
#print axioms vectorTomita_closure_single_valued
end
end TGLV350.Regular
