import TGLExt.V350ScalarDualWeight
import TGLExt.V350FixedCoreShiftCommutation
import TGLExt.ModularPower

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 700000

namespace TGLV350.Regular
open TGLExt ChatgptAudit
noncomputable section

/-- On N, conjugation by a regular unitary agrees with fibre modular
conjugation: the ordinary shift belongs to N'. -/
theorem regular_conjugation_eq_fibre_modular (P : SiteProfile) (t : ℝ)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hA : A ∈ regularCoreAlgebra P) :
    star (regularUnitary P t) * A * regularUnitary P t =
      star (fibre (modularFlowCLM P t)) * A * fibre (modularFlowCLM P t) := by
  have hs : shift (-t) * A = A * shift (-t) :=
    ((VonNeumannAlgebra.mem_commutant_iff.mp (shift_mem_regularCommutant P (-t))) A hA).symm
  rw [regular_star]
  unfold regularUnitary
  rw [← fibre_star, modularFlowCLM_star]
  calc
    _ = fibre (modularFlowCLM P (-t)) * (shift (-t) * A) *
        (fibre (modularFlowCLM P t) * shift t) := by simp only [mul_assoc]
    _ = fibre (modularFlowCLM P (-t)) * A *
        (shift (-t) * fibre (modularFlowCLM P t)) * shift t := by
      rw [hs]
      simp only [mul_assoc]
    _ = (fibre (modularFlowCLM P (-t)) * A * fibre (modularFlowCLM P t)) *
        (shift (-t) * shift t) := by
      rw [shift_commutes_fibre]
      simp only [mul_assoc]
    _ = _ := by rw [shift_mul, neg_add_cancel, shift_zero, mul_one]

theorem fibre_modular_fixes_regularVacuum (P : SiteProfile) (t : ℝ) :
    fibre (modularFlowCLM P t) (regularVacuum P) = regularVacuum P := by
  change fibre (modularFlowCLM P t) (testVector (hOmega P)) = testVector (hOmega P)
  rw [fibre_testVector, modularFlowCLM_apply, modularFlow_fixes_omega]

theorem dualQuadraticIntegral_regular_conjugate_vacuum (P : SiteProfile) (t : ℝ)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hA : A ∈ regularCoreAlgebra P) :
    dualQuadraticIntegral (star (regularUnitary P t) * A * regularUnitary P t) (regularVacuum P) =
      dualQuadraticIntegral A (regularVacuum P) := by
  rw [regular_conjugation_eq_fibre_modular P t A hA, dualQuadraticIntegral_bimodule,
    fibre_modular_fixes_regularVacuum]

def PositiveCoreInput.regularConjugate {P : SiteProfile} (A : PositiveCoreInput P) (t : ℝ) :
    PositiveCoreInput P :=
  ⟨star (regularUnitary P t) * A.val * regularUnitary P t,
    (regularCoreAlgebra P).mul_mem
      ((regularCoreAlgebra P).mul_mem
        ((regularCoreAlgebra P).toStarSubalgebra.star_mem' (regularUnitary_mem P t)) A.property.1)
      (regularUnitary_mem P t),
    star_left_conjugate_nonneg A.property.2 _⟩

/-- Invariance is proved for the candidate modular group. It does not
identify that group with the weight's modular group without KMS/domain data. -/
theorem scalarDualWeight_regular_invariant (P : SiteProfile) (A : PositiveCoreInput P) (t : ℝ) :
    scalarDualWeight P (A.regularConjugate t) = scalarDualWeight P A :=
  dualQuadraticIntegral_regular_conjugate_vacuum P t A.val A.property.1

#print axioms regular_conjugation_eq_fibre_modular
#print axioms fibre_modular_fixes_regularVacuum
#print axioms dualQuadraticIntegral_regular_conjugate_vacuum
#print axioms PositiveCoreInput.regularConjugate
#print axioms scalarDualWeight_regular_invariant
end
end TGLV350.Regular
