import TGLExt.F1Fecho394.RegularCoreConjugationR1
import TGLExt.F1Fecho394.RegularCoreAverageR2
import TGLExt.V350ShiftCharacterAverage
import TGLExt.V350RegularFiniteWeight
set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularRightAverage
open TGLV350.Regular MeasureTheory Filter
open scoped Topology ENNReal
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
theorem regularUnitary_vacuum_is_shift (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (M : VonNeumannAlgebra H) (v : RegularHilbert H) (hv : ∀ t : ℝ, fibre (F1Fecho.RegularCovariantCore.boostCLM B t) v = v) (t : ℝ) :
    F1Fecho.RegularCovariantCore.regularUnitary B t v = shift t v := by
  have h := congrArg (fun T : RegularHilbert H →L[ℂ] _ => T v)
    (shift_commutes_fibre t (F1Fecho.RegularCovariantCore.boostCLM B t)).symm
  change fibre (F1Fecho.RegularCovariantCore.boostCLM B t) (shift t v) =
    shift t (fibre (F1Fecho.RegularCovariantCore.boostCLM B t) v) at h
  change fibre (F1Fecho.RegularCovariantCore.boostCLM B t) (shift t v) = _
  rw [h,hv]

/-- Right multiplication on an orbit is a phase and ordinary translation.
No KMS identity or modular identification is assumed. -/
theorem scalarOrbit_right_regular (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (M : VonNeumannAlgebra H) (v : RegularHilbert H) (hv : ∀ t : ℝ, fibre (F1Fecho.RegularCovariantCore.boostCLM B t) v = v)
    (A : (F1Fecho.RegularCovariantCore.core B M).toStarSubalgebra) (s t : ℝ) :
    dualAmbient s (A.val * F1Fecho.RegularCovariantCore.regularUnitary B t) v =
      characterPhase s t • shift t (dualAmbient s A.val v) := by
  rw [map_mul,F1Fecho.RegularCovariantCore.dual_on_regular B]
  change dualAmbient s A.val (characterPhase s t • F1Fecho.RegularCovariantCore.regularUnitary B t v) = _
  rw [map_smul,regularUnitary_vacuum_is_shift B M v hv t]
  congr 1
  have h := (VonNeumannAlgebra.mem_commutant_iff.mp (F1Fecho.RegularCoreFixed.shift_mem_regularCommutant B M t))
    (F1Fecho.RegularCovariantCore.dualAction B M s A).val (F1Fecho.RegularCovariantCore.dualAction B M s A).property
  exact congrArg (fun T : RegularHilbert H →L[ℂ] _ => T v) h

theorem scalarOrbit_right_average (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (M : VonNeumannAlgebra H) (v : RegularHilbert H) (hv : ∀ t : ℝ, fibre (F1Fecho.RegularCovariantCore.boostCLM B t) v = v)
    (A : (F1Fecho.RegularCovariantCore.core B M).toStarSubalgebra) (s h : ℝ) :
    dualAmbient s (A.val * F1Fecho.RegularCoreAverage.regularAverage B h) v =
      shiftCharacterAverage s h (dualAmbient s A.val v) := by
  rw [map_mul]
  change dualAmbient s A.val (dualAmbient s (F1Fecho.RegularCoreAverage.regularAverage B h) v) = _
  rw [F1Fecho.RegularCoreAverage.regularAverage_dual_apply B,shiftCharacterAverage_apply]
  change dualAmbient s A.val (((h⁻¹ : ℝ) : ℂ) • _) = ((h⁻¹ : ℝ) : ℂ) • _
  rw [map_smul]
  congr 1
  have hc := (characterPhase_continuous s).smul
    (F1Fecho.RegularCovariantCore.regular_strongly_continuous B v)
  rw [← (dualAmbient s A.val).intervalIntegral_comp_comm (hc.intervalIntegrable 0 h)]
  apply intervalIntegral.integral_congr
  intro t _
  have he := scalarOrbit_right_regular B M v hv A s t
  rw [map_mul,F1Fecho.RegularCovariantCore.dual_on_regular B] at he
  exact he

theorem scalarOrbit_right_average_norm_le (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (M : VonNeumannAlgebra H) (v : RegularHilbert H) (hv : ∀ t : ℝ, fibre (F1Fecho.RegularCovariantCore.boostCLM B t) v = v)
    (A : (F1Fecho.RegularCovariantCore.core B M).toStarSubalgebra) (s h : ℝ) :
    ‖dualAmbient s (A.val * F1Fecho.RegularCoreAverage.regularAverage B h) v‖ ≤
      ‖dualAmbient s A.val v‖ := by
  rw [scalarOrbit_right_average B M v hv A s h]
  exact shiftCharacterAverage_norm_map_le s h _

theorem scalarOrbit_right_average_tendsto (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (M : VonNeumannAlgebra H) (v : RegularHilbert H) (hv : ∀ t : ℝ, fibre (F1Fecho.RegularCovariantCore.boostCLM B t) v = v)
    (A : (F1Fecho.RegularCovariantCore.core B M).toStarSubalgebra) (s : ℝ) :
    Tendsto (fun h : ℝ => dualAmbient s (A.val * F1Fecho.RegularCoreAverage.regularAverage B h) v)
      (𝓝[≠] 0) (𝓝 (dualAmbient s A.val v)) := by
  simp_rw [scalarOrbit_right_average B M v hv A s]
  exact shiftCharacterAverage_tendsto_identity s _

theorem scalarWeight_right_average_le (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (M : VonNeumannAlgebra H) (v : RegularHilbert H) (hv : ∀ t : ℝ, fibre (F1Fecho.RegularCovariantCore.boostCLM B t) v = v)
    (A : (F1Fecho.RegularCovariantCore.core B M).toStarSubalgebra) (h : ℝ) :
    dualQuadraticIntegral (star (A.val * F1Fecho.RegularCoreAverage.regularAverage B h) * (A.val * F1Fecho.RegularCoreAverage.regularAverage B h))
      v ≤ dualQuadraticIntegral (star A.val * A.val) v := by
  simp only [dualQuadraticIntegral,dualQuadraticIntegrand_star_mul]
  apply mul_le_mul_right
  apply lintegral_mono
  intro s
  exact ENNReal.ofReal_le_ofReal (pow_le_pow_left₀ (norm_nonneg _)
    (scalarOrbit_right_average_norm_le B M v hv A s h) 2)


end F1Fecho.RegularRightAverage
#print axioms F1Fecho.RegularRightAverage.regularUnitary_vacuum_is_shift
#print axioms F1Fecho.RegularRightAverage.scalarOrbit_right_regular
#print axioms F1Fecho.RegularRightAverage.scalarOrbit_right_average
#print axioms F1Fecho.RegularRightAverage.scalarOrbit_right_average_norm_le
#print axioms F1Fecho.RegularRightAverage.scalarOrbit_right_average_tendsto
#print axioms F1Fecho.RegularRightAverage.scalarWeight_right_average_le
