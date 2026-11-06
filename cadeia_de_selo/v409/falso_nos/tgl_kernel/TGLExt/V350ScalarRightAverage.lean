import TGLExt.V350ScalarWeightOrbit
import TGLExt.V350ShiftCharacterAverage
import TGLExt.V350ScalarModularInvariance

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory Filter
open scoped Topology ENNReal
noncomputable section

theorem regularUnitary_vacuum_is_shift (P : SiteProfile) (t : ℝ) :
    regularUnitary P t (regularVacuum P) = shift t (regularVacuum P) := by
  have h := congrArg (fun T : RegularHilbert (TowerHilbert P) →L[ℂ] _ => T (regularVacuum P))
    (shift_commutes_fibre t (modularFlowCLM P t)).symm
  change fibre (modularFlowCLM P t) (shift t (regularVacuum P)) =
    shift t (fibre (modularFlowCLM P t) (regularVacuum P)) at h
  change fibre (modularFlowCLM P t) (shift t (regularVacuum P)) = _
  rw [h,fibre_modular_fixes_regularVacuum]

/-- Right multiplication on an orbit is a phase and ordinary translation.
No KMS identity or modular identification is assumed. -/
theorem scalarOrbit_right_regular (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (s t : ℝ) :
    dualAmbient s (A.val * regularUnitary P t) (regularVacuum P) =
      characterPhase s t • shift t (dualAmbient s A.val (regularVacuum P)) := by
  rw [map_mul,dualAmbient_regular]
  change dualAmbient s A.val (characterPhase s t • regularUnitary P t (regularVacuum P)) = _
  rw [map_smul,regularUnitary_vacuum_is_shift]
  congr 1
  have h := (VonNeumannAlgebra.mem_commutant_iff.mp (shift_mem_regularCommutant P t))
    (regularDualAction P s A).val (regularDualAction P s A).property
  exact congrArg (fun T : RegularHilbert (TowerHilbert P) →L[ℂ] _ => T (regularVacuum P)) h

theorem scalarOrbit_right_average (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (s h : ℝ) :
    dualAmbient s (A.val * regularAverage P h) (regularVacuum P) =
      shiftCharacterAverage s h (dualAmbient s A.val (regularVacuum P)) := by
  rw [map_mul]
  change dualAmbient s A.val (dualAmbient s (regularAverage P h) (regularVacuum P)) = _
  rw [regularAverage_dual_apply,shiftCharacterAverage_apply]
  change dualAmbient s A.val (((h⁻¹ : ℝ) : ℂ) • _) = ((h⁻¹ : ℝ) : ℂ) • _
  rw [map_smul]
  congr 1
  have hc := (characterPhase_continuous s).smul
    (regular_strongly_continuous P (regularVacuum P))
  rw [← (dualAmbient s A.val).intervalIntegral_comp_comm (hc.intervalIntegrable 0 h)]
  apply intervalIntegral.integral_congr
  intro t _
  have he := scalarOrbit_right_regular P A s t
  rw [map_mul,dualAmbient_regular] at he
  exact he

theorem scalarOrbit_right_average_norm_le (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (s h : ℝ) :
    ‖dualAmbient s (A.val * regularAverage P h) (regularVacuum P)‖ ≤
      ‖dualAmbient s A.val (regularVacuum P)‖ := by
  rw [scalarOrbit_right_average]
  exact shiftCharacterAverage_norm_map_le s h _

theorem scalarOrbit_right_average_tendsto (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (s : ℝ) :
    Tendsto (fun h : ℝ => dualAmbient s (A.val * regularAverage P h) (regularVacuum P))
      (𝓝[≠] 0) (𝓝 (dualAmbient s A.val (regularVacuum P))) := by
  simp_rw [scalarOrbit_right_average]
  exact shiftCharacterAverage_tendsto_identity s _

theorem scalarWeight_right_average_le (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (h : ℝ) :
    dualQuadraticIntegral (star (A.val * regularAverage P h) * (A.val * regularAverage P h))
      (regularVacuum P) ≤ dualQuadraticIntegral (star A.val * A.val) (regularVacuum P) := by
  simp only [dualQuadraticIntegral,dualQuadraticIntegrand_star_mul]
  apply mul_le_mul_right
  apply lintegral_mono
  intro s
  exact ENNReal.ofReal_le_ofReal (pow_le_pow_left₀ (norm_nonneg _)
    (scalarOrbit_right_average_norm_le P A s h) 2)

def scalarWeightRightRegularization (P : SiteProfile) (A : scalarWeightLeftIdeal P) (h : ℝ) :
    scalarWeightLeftIdeal P :=
  ⟨⟨A.val.val * regularAverage P h,
    (regularCoreAlgebra P).mul_mem A.val.property (regularAverage_mem P h)⟩,
    (scalarWeight_right_average_le P A.val h).trans_lt A.property⟩

theorem scalarWeightRightRegularization_uniform (P : SiteProfile)
    (A : scalarWeightLeftIdeal P) (h : ℝ) (hh : 0 < h) :
    (scalarWeightRightRegularization P A h).val ∈ finiteDualLeftIdeal P :=
  HasFiniteDualSquare.left_mul _ _ (regularAverage_hasFiniteDualSquare P h hh)

#print axioms regularUnitary_vacuum_is_shift
#print axioms scalarOrbit_right_regular
#print axioms scalarOrbit_right_average
#print axioms scalarOrbit_right_average_norm_le
#print axioms scalarOrbit_right_average_tendsto
#print axioms scalarWeight_right_average_le
#print axioms scalarWeightRightRegularization
#print axioms scalarWeightRightRegularization_uniform
end
end TGLV350.Regular
