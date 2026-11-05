import TGLExt.V350ConstantFibreIdentification

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem mem_fibreImage_centralizer (N : VonNeumannAlgebra H)
    (D : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hD : ∀ A ∈ N, fibre A * D = D * fibre A) :
    D ∈ StarSubalgebra.centralizer ℂ (fibre '' (N : Set (H →L[ℂ] H))) := by
  rw [StarSubalgebra.mem_centralizer_iff]
  rintro _ ⟨A,hA,rfl⟩
  refine ⟨hD A hA,?_⟩
  rw [← fibre_star]
  exact hD (star A) (star_mem hA)

/-- Amplifying a von Neumann algebra has no extra elements in its bicommutant.
The proof uses commutation with external translations and characters, then
reflects membership through the faithful constant-fibre representation. -/
theorem mem_generated_fibre_iff (N : VonNeumannAlgebra H)
    (B : RegularHilbert H →L[ℂ] RegularHilbert H) :
    B ∈ generatedAlgebra (fibre '' (N : Set (H →L[ℂ] H))) ↔
      ∃ C ∈ N, B = fibre C := by
  constructor
  · intro hB
    change B ∈ StarSubalgebra.centralizer ℂ
      ((StarSubalgebra.centralizer ℂ (fibre '' (N : Set (H →L[ℂ] H)))) :
        Set (RegularHilbert H →L[ℂ] RegularHilbert H)) at hB
    rw [StarSubalgebra.mem_centralizer_iff] at hB
    have hb := hB
    have hs : ∀ t : ℝ, shift t * B = B * shift t := by
      intro t
      exact (hb (shift t) (mem_fibreImage_centralizer N (shift t)
        (fun A _ => (shift_commutes_fibre t A).symm))).1
    have hc : ∀ s : ℝ, characterMultiplier s * B = B * characterMultiplier s := by
      intro s
      exact (hb (characterMultiplier s) (mem_fibreImage_centralizer N (characterMultiplier s)
        (fun A _ => (characterMultiplier_commutes_fibre s A).symm))).1
    have he := eq_fibre_of_shift_character_commutation B hs hc
    refine ⟨fibreCandidate B,?_,he⟩
    rw [← VonNeumannAlgebra.commutant_commutant N,VonNeumannAlgebra.mem_commutant_iff]
    intro D hD
    have hd : fibre D ∈ StarSubalgebra.centralizer ℂ
        (fibre '' (N : Set (H →L[ℂ] H))) := by
      apply mem_fibreImage_centralizer
      intro A hA
      rw [← fibre_mul,← fibre_mul]
      exact congrArg fibre ((VonNeumannAlgebra.mem_commutant_iff.mp hD) A hA)
    have hh := (hb (fibre D) hd).1
    rw [he,← fibre_mul,← fibre_mul] at hh
    exact fibre_injective hh
  · rintro ⟨C,hC,rfl⟩
    exact generator_mem ⟨C,hC,rfl⟩

def fibreVonNeumann (N : VonNeumannAlgebra H) : VonNeumannAlgebra (RegularHilbert H) :=
  generatedAlgebra (fibre '' (N : Set (H →L[ℂ] H)))

theorem fibreVonNeumann_coe (N : VonNeumannAlgebra H) :
    (fibreVonNeumann N : Set (RegularHilbert H →L[ℂ] RegularHilbert H)) =
      fibre '' (N : Set (H →L[ℂ] H)) := by
  apply Set.Subset.antisymm
  · intro B hb
    obtain ⟨C,hC,hB⟩ := (mem_generated_fibre_iff N B).mp hb
    exact ⟨C,hC,hB.symm⟩
  · rintro B ⟨C,hC,rfl⟩
    exact generator_mem ⟨C,hC,rfl⟩

#print axioms mem_fibreImage_centralizer
#print axioms mem_generated_fibre_iff
#print axioms fibreVonNeumann
#print axioms fibreVonNeumann_coe
end
end TGLV350.Regular
