import TGLExt.V350DualFixedCore

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1600000

namespace TGLV350.Regular
noncomputable section

/-- Ordinary translations commute with the regular modular unitaries in the
constant-fibre representation. These are distinct one-parameter groups. -/
theorem shift_commutes_regularUnitary (P : TGLExt.SiteProfile) (s t : ℝ) :
    shift s * regularUnitary P t = regularUnitary P t * shift s := by
  unfold regularUnitary
  calc
    _ = (shift s * fibre (TGLExt.modularFlowCLM P t)) * shift t := by rw [mul_assoc]
    _ = fibre (TGLExt.modularFlowCLM P t) * (shift s * shift t) := by
      rw [shift_commutes_fibre, mul_assoc]
    _ = fibre (TGLExt.modularFlowCLM P t) * (shift t * shift s) := by
      rw [shift_mul, shift_mul, add_comm s t]
    _ = _ := by rw [mul_assoc]

/-- Every member of N commutes with ordinary translations. This follows from
its generators and bicommutant closure, not a decomposition theorem. -/
theorem regularCore_le_shiftCommutant (P : TGLExt.SiteProfile) :
    regularCoreAlgebra P ≤
      starCommutantAlgebra (Set.range (shift (H := TGLExt.TowerHilbert P))) := by
  apply regularCore_minimal
  · intro A _
    change fibre A ∈ StarSubalgebra.centralizer ℂ _
    rw [StarSubalgebra.mem_centralizer_iff]
    rintro _ ⟨s,rfl⟩
    refine ⟨shift_commutes_fibre s A, ?_⟩
    rw [shift_star]
    exact shift_commutes_fibre (-s) A
  · intro t
    change regularUnitary P t ∈ StarSubalgebra.centralizer ℂ _
    rw [StarSubalgebra.mem_centralizer_iff]
    rintro _ ⟨s,rfl⟩
    refine ⟨shift_commutes_regularUnitary P s t, ?_⟩
    rw [shift_star]
    exact shift_commutes_regularUnitary P (-s) t

theorem shift_mem_regularCommutant (P : TGLExt.SiteProfile) (s : ℝ) :
    shift s ∈ (regularCoreAlgebra P).commutant := by
  rw [VonNeumannAlgebra.mem_commutant_iff]
  intro B hB
  have h := regularCore_le_shiftCommutant P hB
  change B ∈ StarSubalgebra.centralizer ℂ _ at h
  rw [StarSubalgebra.mem_centralizer_iff] at h
  exact (h _ ⟨s,rfl⟩).1.symm

/-- A fixed core operator commutes with both translation and modulation.
Identifying such an operator with a constant fibre is the next, separate step. -/
theorem dualFixedCore_commutes_shift_and_character (P : TGLExt.SiteProfile)
    (B : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P))
    (hB : B ∈ dualFixedCore P) (s : ℝ) :
    shift s * B = B * shift s ∧ characterMultiplier s * B = B * characterMultiplier s := by
  obtain ⟨hm,hf⟩ := (dualFixedCore_mem_iff P B).mp hB
  refine ⟨?_, (dualAmbient_fixed_iff_commutes s B).mp (hf s)⟩
  exact ((VonNeumannAlgebra.mem_commutant_iff.mp (shift_mem_regularCommutant P s)) B hm).symm

#print axioms shift_commutes_regularUnitary
#print axioms regularCore_le_shiftCommutant
#print axioms shift_mem_regularCommutant
#print axioms dualFixedCore_commutes_shift_and_character
end
end TGLV350.Regular
