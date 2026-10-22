import TGLExt.JointUnitaryPreparation
import TGLExt.CoherentScalarStress

set_option autoImplicit false
set_option maxHeartbeats 2800000
namespace ChatgptAudit.JointCovariance
open Matrix Set TGLExt ChatgptAudit.JointUnitary ChatgptAudit.Coherent023
noncomputable section

def frameMetric (E g : Tensor4) : Tensor4 := Eᵀ*g*E
def frameInverse (D gi : Tensor4) : Tensor4 := D*gi*Dᵀ
def frameCovectors {ι : Type} (E : Tensor4) (w : ι → Coordinate4) : ι → Coordinate4 :=
  fun j => Eᵀ *ᵥ w j

theorem frame_covectors_identity {ι : Type} (w : ι → Coordinate4) :
    frameCovectors 1 w=w := by
  funext j
  simp [frameCovectors]

theorem frame_covectors_composition {ι : Type} (E F : Tensor4) (w : ι → Coordinate4) :
    frameCovectors F (frameCovectors E w)=frameCovectors (E*F) w := by
  funext j
  simp only [frameCovectors, Matrix.mulVec_mulVec, Matrix.transpose_mul]

theorem frame_covectors_recovered {ι : Type} (E D : Tensor4) (hED : E*D=1)
    (w : ι → Coordinate4) : frameCovectors D (frameCovectors E w)=w := by
  rw [frame_covectors_composition, hED, frame_covectors_identity]

theorem transported_frequency {ι : Type} (E : Tensor4) (w : ι → Coordinate4)
    (d : Coordinate4) (j : ι) :
    covectorRead (frameCovectors E w j) d=covectorRead (w j) (E *ᵥ d) :=
  covector_read_change_basis E (w j) d

theorem transported_null_direction (E g : Tensor4) (d : Coordinate4) :
    tensorQuad (frameMetric E g) d=0 ↔ tensorQuad g (E *ᵥ d)=0 := by
  rw [frameMetric, tensorQuad_congruence]

theorem transported_inverse_is_inverse (E D g gi : Tensor4)
    (hED : E*D=1) (hDE : D*E=1) (hgi : gi*g=1) :
    frameInverse D gi * frameMetric E g=1 := by
  unfold frameInverse frameMetric
  have ht : Dᵀ*Eᵀ=1 := by rw [← Matrix.transpose_mul, hED, Matrix.transpose_one]
  calc
    (D*gi*Dᵀ)*(Eᵀ*g*E)=D*gi*(Dᵀ*Eᵀ)*g*E := by noncomm_ring
    _ = 1 := by rw [ht, mul_one, mul_assoc D gi g, hgi, mul_one, hDE]

theorem transported_inverse_quad (E D gi : Tensor4) (hED : E*D=1) (w : Coordinate4) :
    tensorQuad (frameInverse D gi) (Eᵀ *ᵥ w)=tensorQuad gi w := by
  have he : frameInverse D gi=(Dᵀ)ᵀ*gi*Dᵀ := by simp [frameInverse]
  rw [he, tensorQuad_congruence, Matrix.mulVec_mulVec, ← Matrix.transpose_mul,
    hED, Matrix.transpose_one, Matrix.one_mulVec]

theorem transported_covector_stress (E D g gi : Tensor4) (hED : E*D=1)
    (w : Coordinate4) (coupling : ℝ) :
    covectorStress (frameMetric E g) (frameInverse D gi) (Eᵀ *ᵥ w) coupling =
      Eᵀ * covectorStress g gi w coupling * E := by
  simp only [covectorStress, transported_inverse_quad E D gi hED w,
    outer_tensor_change_basis, frameMetric, Matrix.mul_smul, Matrix.smul_mul,
    Matrix.mul_sub, Matrix.sub_mul]

variable {ι : Type} [Fintype ι]

theorem transported_finite_source (E D g gi : Tensor4) (hED : E*D=1)
    (w : ι → Coordinate4) (weight coupling : ι → ℝ) :
    (∑ j, weight j • covectorStress (frameMetric E g) (frameInverse D gi)
      (frameCovectors E w j) (coupling j)) =
      Eᵀ * (∑ j, weight j • covectorStress g gi (w j) (coupling j)) * E := by
  simp only [frameCovectors, transported_covector_stress E D g gi hED,
    Matrix.mul_sum, Matrix.sum_mul, Matrix.mul_smul, Matrix.smul_mul]

theorem joint_curve_frame_covariance (C : UnitaryLabelData ι) (E : Tensor4)
    (w : ι → Coordinate4) (d : Coordinate4) :
    jointCovectorCurve C (frameCovectors E w) d=jointCovectorCurve C w (E *ᵥ d) := by
  unfold jointCovectorCurve
  congr 1
  funext j
  exact transported_frequency E w d j

theorem joint_weights_frame_covariance (C : UnitaryLabelData ι) (E : Tensor4)
    (w : ι → Coordinate4) (d : Coordinate4) (t : ℝ) :
    (jointCovectorCurve C (frameCovectors E w) d).weights t =
      (jointCovectorCurve C w (E *ᵥ d)).weights t := by
  rw [joint_curve_frame_covariance]

theorem joint_response_frame_covariance (C : UnitaryLabelData ι) (E : Tensor4)
    (w : ι → Coordinate4) (d : Coordinate4) :
    jointResponse C (fun j => covectorRead (frameCovectors E w j) d) =
      jointResponse C (fun j => covectorRead (w j) (E *ᵥ d)) := by
  congr 1
  funext j
  exact transported_frequency E w d j

theorem joint_flow_frame_covariance [DecidableEq ι] (C : UnitaryLabelData ι)
    (E : Tensor4) (w : ι → Coordinate4) (d : Coordinate4) (t : ℝ) :
    jointBlockFlow C (fun j => covectorRead (frameCovectors E w j) d) t =
      jointBlockFlow C (fun j => covectorRead (w j) (E *ᵥ d)) t := by
  congr 1
  funext j
  exact transported_frequency E w d j

theorem joint_amplitude_frame_covariance (C : UnitaryLabelData ι)
    (E : Tensor4) (w : ι → Coordinate4) (d : Coordinate4) (t : ℝ) :
    jointBlockAmplitude C (fun j => covectorRead (frameCovectors E w j) d) t =
      jointBlockAmplitude C (fun j => covectorRead (w j) (E *ᵥ d)) t := by
  congr 1
  funext j
  exact transported_frequency E w d j

#print axioms frameMetric
#print axioms frameInverse
#print axioms frameCovectors
#print axioms frame_covectors_identity
#print axioms frame_covectors_composition
#print axioms frame_covectors_recovered
#print axioms transported_frequency
#print axioms transported_null_direction
#print axioms transported_inverse_is_inverse
#print axioms transported_inverse_quad
#print axioms transported_covector_stress
#print axioms transported_finite_source
#print axioms joint_curve_frame_covariance
#print axioms joint_weights_frame_covariance
#print axioms joint_response_frame_covariance
#print axioms joint_flow_frame_covariance
#print axioms joint_amplitude_frame_covariance
end
end ChatgptAudit.JointCovariance
