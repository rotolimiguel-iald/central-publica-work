import UnitarySourceCalibration
import FiniteCoherentSources
import JointUnitaryPreparation

set_option autoImplicit false
set_option maxHeartbeats 4000000
namespace ChatgptAudit.GeneralSourceUnitary
open Matrix Filter Topology Set TGLExt ChatgptAudit.GeneralMetric
  ChatgptAudit.Coherent023 ChatgptAudit.Unitary022 ChatgptAudit.SignedCoverage
  ChatgptAudit.UnitaryCalibration ChatgptAudit.FiniteCoherentSource
  ChatgptAudit.JointUnitary ChatgptAudit.Micro021
open scoped ContDiff
noncomputable section

/-- Eight positive label weights; the couplings have both signs. -/
def calibrationLabelData : UnitaryLabelData CalibrationIndex where
  weight := fun _ => 1/8
  weight_pos := calibration_weights_positive
  weight_sum := calibration_weights_normalized
  axisA := calibrationAxisA
  axisB := calibrationAxisB
  initialU := fun _ => 3/5
  initialV := fun _ => 4/5
  axis_normalized := calibration_axes_normalized
  initial_normalized := by intro j; norm_num
  positive_u := by intro j; norm_num
  positive_v := by intro j; norm_num

def calibrationSourceCovectors (g T : TensorField4) : CalibrationIndex → CovectorField4 :=
  fun j x => calibrationCovector (traceReverse (g x) (metricInverse g x) (T x)) j

def realizedSourceField (g T : TensorField4) : TensorField4 :=
  finiteCoherentStressField g (metricInverse g) (calibrationSourceCovectors g T)
    calibrationLabelData.weight calibrationLabelData.axisA calibrationLabelData.axisB
    calibrationLabelData.initialU calibrationLabelData.initialV

def calibrationSourceCurve (g T : TensorField4) (x d : Coordinate4) :
    DiagonalStateCurve (jointBase calibrationLabelData) :=
  jointCovectorCurve calibrationLabelData (fun j => calibrationSourceCovectors g T j x) d

def calibrationSourceResponse (g T : TensorField4) (x d : Coordinate4) : ℝ :=
  jointResponse calibrationLabelData
    (fun j => covectorRead (calibrationSourceCovectors g T j x) d)

theorem calibration_base_positive :
    ∀ k, 0 < jointBase calibrationLabelData k :=
  joint_base_positive calibrationLabelData

theorem calibration_base_normalized :
    (∑ k, jointBase calibrationLabelData k) = 1 := by
  calc
    _ = ∑ k, jointWeights calibrationLabelData (fun _ => 0) 0 k := by
      apply Finset.sum_congr rfl
      intro k _
      exact ((jointUnitaryCurve calibrationLabelData (fun _ => 0)).at_zero k).symm
    _ = 1 := joint_weights_normalized calibrationLabelData (fun _ => 0) 0

theorem calibration_source_covectors_smooth (U : Set Coordinate4) (g T : TensorField4)
    (hg : SmoothMatrixOn U g) (hT : SmoothMatrixOn U T)
    (hLor : ∀ x ∈ U, LorentzByCongruence (g x)) (j : CalibrationIndex) :
    SmoothVectorOn U (calibrationSourceCovectors g T j) :=
  general_source_unitary_covectors_smooth U g T hg hT hLor j

theorem realized_source_eq (g T : TensorField4) (x : Coordinate4)
    (hLor : LorentzByCongruence (g x)) (hT : (T x)ᵀ = T x) :
    realizedSourceField g T x = T x := by
  change calibratedStress (g x) (metricInverse g x)
    (traceReverse (g x) (metricInverse g x) (T x)) = T x
  exact every_symmetric_source_has_unitary_calibration _ _ _
    (constructed_metric_inverse_left g x hLor) (lorentz_metric_symmetric _ hLor) hT

theorem realized_source_eq_on (U : Set Coordinate4) (g T : TensorField4)
    (hLor : ∀ x ∈ U, LorentzByCongruence (g x)) (hT : ∀ x ∈ U, (T x)ᵀ = T x) :
    EqOn (realizedSourceField g T) T U := by
  intro x hx
  exact realized_source_eq g T x (hLor x hx) (hT x hx)

theorem realized_source_symmetric (g T : TensorField4) (x : Coordinate4)
    (hLor : LorentzByCongruence (g x)) :
    (realizedSourceField g T x)ᵀ = realizedSourceField g T x :=
  finite_coherent_stress_symmetric g (metricInverse g) _ _ _ _ _ _ x
    (lorentz_metric_symmetric _ hLor)

theorem realized_source_smooth (U : Set Coordinate4) (g T : TensorField4)
    (hg : SmoothMatrixOn U g) (hT : SmoothMatrixOn U T)
    (hLor : ∀ x ∈ U, LorentzByCongruence (g x)) :
    SmoothMatrixOn U (realizedSourceField g T) :=
  finite_coherent_stress_smooth U g (metricInverse g) _ _ _ _ _ _ hg
    (constructed_metric_inverse_smooth U g hg hLor)
    (calibration_source_covectors_smooth U g T hg hT hLor)

theorem realized_source_divergence_eq (U : Set Coordinate4) (hU : IsOpen U)
    (g T : TensorField4) (Gamma : ConnectionField4)
    (hLor : ∀ x ∈ U, LorentzByCongruence (g x)) (hT : ∀ x ∈ U, (T x)ᵀ = T x)
    (x : Coordinate4) (hx : x ∈ U) :
    tensorFieldDivergence (metricInverse g) Gamma (realizedSourceField g T) x =
      tensorFieldDivergence (metricInverse g) Gamma T x :=
  tensorFieldDivergence_congr_on U hU (metricInverse g) Gamma _ _
    (realized_source_eq_on U g T hLor hT) x hx

/-- Total conservation is transported from T, with no sectorwise wave assumption. -/
theorem realized_source_conserved (U : Set Coordinate4) (hU : IsOpen U)
    (g T : TensorField4) (Gamma : ConnectionField4)
    (hLor : ∀ x ∈ U, LorentzByCongruence (g x)) (hT : ∀ x ∈ U, (T x)ᵀ = T x)
    (hc : ∀ x ∈ U, ∀ j, tensorFieldDivergence (metricInverse g) Gamma T x j = 0) :
    ∀ x ∈ U, ∀ j, tensorFieldDivergence (metricInverse g) Gamma
      (realizedSourceField g T) x j = 0 := by
  intro x hx j
  rw [realized_source_divergence_eq U hU g T Gamma hLor hT x hx]
  exact hc x hx j

theorem calibration_source_weights_nonnegative (g T : TensorField4) (x d : Coordinate4)
    (t : ℝ) : ∀ k, 0 ≤ (calibrationSourceCurve g T x d).weights t k :=
  joint_weights_nonnegative calibrationLabelData _ t

theorem calibration_source_weights_normalized (g T : TensorField4) (x d : Coordinate4)
    (t : ℝ) : ∑ k, (calibrationSourceCurve g T x d).weights t k = 1 :=
  (calibrationSourceCurve g T x d).trace_one t

theorem calibration_source_curve_tangent_zero (g T : TensorField4) (x d : Coordinate4) :
    (calibrationSourceCurve g T x d).tangent 0 = 0 :=
  joint_curve_tangent_zero calibrationLabelData _

theorem calibration_source_entropy_quadratic_limit (g T : TensorField4) (x d : Coordinate4) :
    Tendsto (fun t => (finiteEntropy ((calibrationSourceCurve g T x d).weights t) -
      finiteEntropy (jointBase calibrationLabelData)) / t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 (calibrationSourceResponse g T x d)) :=
  joint_entropy_quadratic_limit calibrationLabelData _

theorem calibration_source_modular_quadratic_limit (g T : TensorField4) (x d : Coordinate4) :
    Tendsto (fun t => modularIncrement (jointBase calibrationLabelData)
      ((calibrationSourceCurve g T x d).weights t) / t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 (calibrationSourceResponse g T x d)) :=
  joint_modular_quadratic_limit calibrationLabelData _

theorem calibration_source_response_null (g T : TensorField4) (x d : Coordinate4)
    (hLor : LorentzByCongruence (g x)) (hT : (T x)ᵀ = T x)
    (hn : tensorQuad (g x) d = 0) :
    calibrationSourceResponse g T x d = -Real.pi * tensorQuad (T x) d := by
  have h := finite_response_matches_null_source g (metricInverse g)
    (calibrationSourceCovectors g T) calibrationLabelData.weight
    calibrationLabelData.axisA calibrationLabelData.axisB calibrationLabelData.initialU
    calibrationLabelData.initialV x d hn
  change calibrationSourceResponse g T x d =
    -Real.pi * tensorQuad (realizedSourceField g T x) d at h
  rw [realized_source_eq g T x hLor hT] at h
  exact h

theorem calibration_source_entropy_null_limit (g T : TensorField4) (x d : Coordinate4)
    (hLor : LorentzByCongruence (g x)) (hT : (T x)ᵀ = T x)
    (hn : tensorQuad (g x) d = 0) :
    Tendsto (fun t => (finiteEntropy ((calibrationSourceCurve g T x d).weights t) -
      finiteEntropy (jointBase calibrationLabelData)) / t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 (-Real.pi * tensorQuad (T x) d)) := by
  rw [← calibration_source_response_null g T x d hLor hT hn]
  exact calibration_source_entropy_quadratic_limit g T x d

theorem calibration_source_modular_null_limit (g T : TensorField4) (x d : Coordinate4)
    (hLor : LorentzByCongruence (g x)) (hT : (T x)ᵀ = T x)
    (hn : tensorQuad (g x) d = 0) :
    Tendsto (fun t => modularIncrement (jointBase calibrationLabelData)
      ((calibrationSourceCurve g T x d).weights t) / t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 (-Real.pi * tensorQuad (T x) d)) := by
  rw [← calibration_source_response_null g T x d hLor hT hn]
  exact calibration_source_modular_quadratic_limit g T x d

theorem calibration_source_block_unitary (g T : TensorField4) (x d : Coordinate4) (t : ℝ) :
    let F := jointBlockFlow calibrationLabelData
      (fun j => covectorRead (calibrationSourceCovectors g T j x) d) t
    Fᴴ * F = 1 ∧ F * Fᴴ = 1 :=
  joint_block_flow_unitary calibrationLabelData _ t

theorem calibration_source_amplitude_weights (g T : TensorField4)
    (x d : Coordinate4) (t : ℝ) (k : Fin 2 × CalibrationIndex) :
    let A := jointBlockAmplitude calibrationLabelData
      (fun j => covectorRead (calibrationSourceCovectors g T j x) d) t
    A k * star (A k) = ((calibrationSourceCurve g T x d).weights t (k.2,k.1) : ℂ) :=
  joint_block_amplitude_weights calibrationLabelData _ t k

#print axioms calibrationLabelData
#print axioms calibrationSourceCovectors
#print axioms realizedSourceField
#print axioms calibrationSourceCurve
#print axioms calibrationSourceResponse
#print axioms calibration_base_positive
#print axioms calibration_base_normalized
#print axioms calibration_source_covectors_smooth
#print axioms realized_source_eq
#print axioms realized_source_eq_on
#print axioms realized_source_symmetric
#print axioms realized_source_smooth
#print axioms realized_source_divergence_eq
#print axioms realized_source_conserved
#print axioms calibration_source_weights_nonnegative
#print axioms calibration_source_weights_normalized
#print axioms calibration_source_curve_tangent_zero
#print axioms calibration_source_entropy_quadratic_limit
#print axioms calibration_source_modular_quadratic_limit
#print axioms calibration_source_response_null
#print axioms calibration_source_entropy_null_limit
#print axioms calibration_source_modular_null_limit
#print axioms calibration_source_block_unitary
#print axioms calibration_source_amplitude_weights
end
end ChatgptAudit.GeneralSourceUnitary
