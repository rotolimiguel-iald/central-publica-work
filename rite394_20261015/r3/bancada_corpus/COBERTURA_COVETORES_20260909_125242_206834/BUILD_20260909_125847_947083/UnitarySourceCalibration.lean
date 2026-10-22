import SignedCovectorCoverage

set_option autoImplicit false
set_option maxHeartbeats 3500000
namespace ChatgptAudit.UnitaryCalibration
open Matrix Set TGLExt ChatgptAudit.GeneralMetric ChatgptAudit.Coherent023
  ChatgptAudit.Unitary022 ChatgptAudit.SignedCoverage
open scoped ContDiff
noncomputable section

def positiveCoupling : ℝ := coherentCoupling (-3/5) (4/5) (3/5) (4/5)
def negativeCoupling : ℝ := coherentCoupling 0 1 (3/5) (4/5)

theorem positive_coupling_positive : 0<positiveCoupling :=
  coherent_negative_control_coupling_positive

theorem negative_coupling_negative : negativeCoupling<0 := by
  unfold negativeCoupling coherentCoupling
  exact div_neg_of_neg_of_pos (neg_neg_of_pos positive_control_response_strict) Real.pi_pos

def positiveScale : ℝ := Real.sqrt (8/positiveCoupling)
def negativeScale : ℝ := Real.sqrt (8/(-negativeCoupling))

theorem positive_scale_squared : positiveScale^2=8/positiveCoupling := by
  exact Real.sq_sqrt (div_nonneg (by norm_num) (le_of_lt positive_coupling_positive))

theorem negative_scale_squared : negativeScale^2=8/(-negativeCoupling) := by
  exact Real.sq_sqrt (div_nonneg (by norm_num) (le_of_lt (neg_pos.mpr negative_coupling_negative)))

theorem positive_scale_identity : positiveCoupling*positiveScale^2=8 := by
  rw [positive_scale_squared]
  field_simp [ne_of_gt positive_coupling_positive]

theorem negative_scale_identity : negativeCoupling*negativeScale^2= -8 := by
  rw [negative_scale_squared]
  field_simp [ne_of_lt negative_coupling_negative]
  ring

theorem covector_stress_vector_smul (g gi : Tensor4) (w : Coordinate4) (r c : ℝ) :
    covectorStress g gi (r • w) c = covectorStress g gi w (c*r^2) := by
  ext i j
  simp only [covectorStress, Matrix.smul_apply, Matrix.sub_apply, Matrix.vecMulVec,
    Matrix.of_apply, Pi.smul_apply, smul_eq_mul, tensorQuad, Matrix.mulVec, dotProduct,
    Fin.sum_univ_four]
  ring

theorem weighted_scaled_stress (g gi : Tensor4) (w : Coordinate4) (r c weight : ℝ) :
    weight • covectorStress g gi (r • w) c =
      covectorStress g gi w (weight*(c*r^2)) := by
  rw [covector_stress_vector_smul]
  simp only [covectorStress, smul_smul]

theorem positive_calibration (g gi : Tensor4) (w : Coordinate4) :
    ((1:ℝ)/8) • covectorStress g gi (positiveScale • w) positiveCoupling =
      covectorStress g gi w 1 := by
  rw [weighted_scaled_stress, positive_scale_identity]
  norm_num

theorem negative_calibration (g gi : Tensor4) (w : Coordinate4) :
    ((1:ℝ)/8) • covectorStress g gi (negativeScale • w) negativeCoupling =
      covectorStress g gi w (-1) := by
  rw [weighted_scaled_stress, negative_scale_identity]
  norm_num

abbrev CalibrationIndex := Fin 4 × Fin 2

def calibrationAxisA (j : CalibrationIndex) : ℝ :=
  if j.2=0 then -3/5 else 0

def calibrationAxisB (j : CalibrationIndex) : ℝ :=
  if j.2=0 then 4/5 else 1

def calibrationCovector (A : Tensor4) (j : CalibrationIndex) : Coordinate4 :=
  if j.2=0 then positiveScale • plusCovector A j.1
  else negativeScale • minusCovector A j.1

def calibratedStress (g gi A : Tensor4) : Tensor4 :=
  ∑ j : CalibrationIndex, ((1:ℝ)/8) • covectorStress g gi (calibrationCovector A j)
    (coherentCoupling (calibrationAxisA j) (calibrationAxisB j) (3/5) (4/5))

theorem calibration_axes_normalized (j : CalibrationIndex) :
    (calibrationAxisA j)^2+(calibrationAxisB j)^2=1 := by
  unfold calibrationAxisA calibrationAxisB
  split_ifs <;> norm_num

theorem calibration_weights_positive : ∀ _j : CalibrationIndex, (0:ℝ)<1/8 := by
  intro _
  norm_num

theorem calibration_weights_normalized : (∑ _j : CalibrationIndex, (1:ℝ)/8)=1 := by
  norm_num

theorem calibrated_stress_is_signed_stress (g gi A : Tensor4) :
    calibratedStress g gi A=signedStress g gi A := by
  unfold calibratedStress
  rw [Fintype.sum_prod_type]
  simp only [Fin.sum_univ_two, calibrationAxisA, calibrationAxisB, calibrationCovector]
  norm_num only
  change (∑ i : Fin 4,
    ((1:ℝ)/8) • covectorStress g gi (positiveScale • plusCovector A i) positiveCoupling +
    ((1:ℝ)/8) • covectorStress g gi (negativeScale • minusCovector A i) negativeCoupling)=_
  simp only [positive_calibration, negative_calibration]
  rfl

theorem every_symmetric_source_has_unitary_calibration (g gi T : Tensor4)
    (hi : gi*g=1) (hg : gᵀ=g) (hT : Tᵀ=T) :
    calibratedStress g gi (traceReverse g gi T)=T := by
  rw [calibrated_stress_is_signed_stress,
    every_symmetric_source_has_eight_covectors g gi T hi hg hT]

theorem calibration_covector_smooth (U : Set Coordinate4) (A : TensorField4)
    (hA : SmoothMatrixOn U A) (j : CalibrationIndex) :
    SmoothVectorOn U (fun x => calibrationCovector (A x) j) := by
  intro k
  unfold calibrationCovector
  split_ifs
  · exact (plus_covector_smooth U A hA j.1 k).const_mul positiveScale
  · exact (minus_covector_smooth U A hA j.1 k).const_mul negativeScale

theorem general_source_unitary_covectors_smooth
    (U : Set Coordinate4) (g T : TensorField4)
    (hg : SmoothMatrixOn U g) (hT : SmoothMatrixOn U T)
    (hLor : ∀ x∈U, LorentzByCongruence (g x)) (j : CalibrationIndex) :
    SmoothVectorOn U (fun x =>
      calibrationCovector (traceReverse (g x) (metricInverse g x) (T x)) j) :=
  calibration_covector_smooth U _ (trace_reverse_field_smooth U g (metricInverse g) T hg
    (constructed_metric_inverse_smooth U g hg hLor) hT) j

#print axioms positiveCoupling
#print axioms negativeCoupling
#print axioms positive_coupling_positive
#print axioms negative_coupling_negative
#print axioms positiveScale
#print axioms negativeScale
#print axioms positive_scale_squared
#print axioms negative_scale_squared
#print axioms positive_scale_identity
#print axioms negative_scale_identity
#print axioms covector_stress_vector_smul
#print axioms weighted_scaled_stress
#print axioms positive_calibration
#print axioms negative_calibration
#print axioms CalibrationIndex
#print axioms calibrationAxisA
#print axioms calibrationAxisB
#print axioms calibrationCovector
#print axioms calibratedStress
#print axioms calibration_axes_normalized
#print axioms calibration_weights_positive
#print axioms calibration_weights_normalized
#print axioms calibrated_stress_is_signed_stress
#print axioms every_symmetric_source_has_unitary_calibration
#print axioms calibration_covector_smooth
#print axioms general_source_unitary_covectors_smooth
end
end ChatgptAudit.UnitaryCalibration
