import TGLExt.V350FiniteSetFibreRead
import TGLExt.V350RegularGeneratedAlgebra

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The ranges of finite-set embeddings determine every bounded operator. -/
theorem finiteSetEmbedding_ranges_total (T : RegularHilbert H →L[ℂ] RegularHilbert H)
    (h : ∀ s : FiniteFibreSet, T.comp (finiteSetEmbedding s) = 0) : T = 0 := by
  have hz : T.adjoint = 0 := by
    ext1 f
    apply finiteSetEmbedding_reads_separate
    intro s
    have he := congrArg ContinuousLinearMap.adjoint (h s)
    rw [ContinuousLinearMap.adjoint_comp,map_zero] at he
    exact congrArg (fun A : RegularHilbert H →L[ℂ] H => A f) he
  have he := congrArg ContinuousLinearMap.adjoint hz
  simpa only [ContinuousLinearMap.adjoint_adjoint,map_zero] using he

def fibreSlice (T : RegularHilbert H →L[ℂ] RegularHilbert H)
    (s t : FiniteFibreSet) : H →L[ℂ] H :=
  (finiteSetEmbedding s).adjoint.comp (T.comp (finiteSetEmbedding t))

/-- Two-sided finite-set coefficients are jointly faithful. -/
theorem fibreSlice_zero (T : RegularHilbert H →L[ℂ] RegularHilbert H)
    (h : ∀ s t : FiniteFibreSet, fibreSlice T s t = 0) : T = 0 := by
  apply finiteSetEmbedding_ranges_total
  intro t
  ext1 v
  apply finiteSetEmbedding_reads_separate
  intro s
  exact congrArg (fun A : H →L[ℂ] H => A v) (h s t)

theorem fibreSlice_left (T : RegularHilbert H →L[ℂ] RegularHilbert H)
    (A : H →L[ℂ] H) (s t : FiniteFibreSet) :
    fibreSlice (fibre A * T) s t = A * fibreSlice T s t := by
  have he := finiteSetEmbedding_adjoint_intertwines s A
  ext1 v
  exact congrArg (fun D : RegularHilbert H →L[ℂ] H => D (T (finiteSetEmbedding t v))) he

theorem fibreSlice_right (T : RegularHilbert H →L[ℂ] RegularHilbert H)
    (A : H →L[ℂ] H) (s t : FiniteFibreSet) :
    fibreSlice (T * fibre A) s t = fibreSlice T s t * A := by
  change (finiteSetEmbedding s).adjoint.comp (T.comp ((fibre A).comp (finiteSetEmbedding t))) =
    (finiteSetEmbedding s).adjoint.comp (T.comp ((finiteSetEmbedding t).comp A))
  rw [finiteSetEmbedding_intertwines]

theorem fibreSlice_sub (T U : RegularHilbert H →L[ℂ] RegularHilbert H)
    (s t : FiniteFibreSet) : fibreSlice (T-U) s t = fibreSlice T s t - fibreSlice U s t := by
  change (finiteSetEmbedding s).adjoint.comp ((T-U).comp (finiteSetEmbedding t)) = _
  rw [ContinuousLinearMap.sub_comp,ContinuousLinearMap.comp_sub]
  rfl

/-- Commutation with amplified generators passes to all their star-bicommutant.
This proof uses finite-set coefficients, not a density theorem as an axiom. -/
theorem fibre_commutes_of_generated (S : Set (H →L[ℂ] H))
    (T : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hT : T ∈ StarSubalgebra.centralizer ℂ (fibre '' S))
    (A : H →L[ℂ] H) (hA : A ∈ generatedAlgebra S) :
    fibre A * T = T * fibre A := by
  have hs : ∀ s t : FiniteFibreSet, fibreSlice T s t ∈ StarSubalgebra.centralizer ℂ S := by
    intro s t
    rw [StarSubalgebra.mem_centralizer_iff]
    intro B hB
    have hb := ((StarSubalgebra.mem_centralizer_iff ℂ).mp hT) (fibre B) ⟨B,hB,rfl⟩
    constructor
    · have he := congrArg (fun D => fibreSlice D s t) hb.1
      simpa only [fibreSlice_left,fibreSlice_right] using he
    · have he := congrArg (fun D => fibreSlice D s t) hb.2
      rw [← fibre_star] at he
      simpa only [fibreSlice_left,fibreSlice_right] using he
  apply sub_eq_zero.mp
  apply fibreSlice_zero
  intro s t
  rw [fibreSlice_sub,fibreSlice_left,fibreSlice_right]
  change A ∈ StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ S) : Set (H →L[ℂ] H)) at hA
  exact sub_eq_zero.mpr
    ((((StarSubalgebra.mem_centralizer_iff ℂ).mp hA) (fibreSlice T s t) (hs s t)).1.symm)

theorem fibre_generated_mem (S : Set (H →L[ℂ] H))
    (A : H →L[ℂ] H) (hA : A ∈ generatedAlgebra S) :
    fibre A ∈ generatedAlgebra (fibre '' S) := by
  change fibre A ∈ StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ (fibre '' S)) : Set (RegularHilbert H →L[ℂ] RegularHilbert H))
  rw [StarSubalgebra.mem_centralizer_iff]
  intro T hT
  exact ⟨(fibre_commutes_of_generated S T hT A hA).symm,
    (fibre_commutes_of_generated S (star T)
      (star_mem hT) A hA).symm⟩

#print axioms finiteSetEmbedding_ranges_total
#print axioms fibreSlice
#print axioms fibreSlice_zero
#print axioms fibreSlice_left
#print axioms fibreSlice_right
#print axioms fibreSlice_sub
#print axioms fibre_commutes_of_generated
#print axioms fibre_generated_mem
end
end TGLV350.Regular
