import TGLExt.TensorNullCone
import TGLExt.SmoothMatrixCalculus

set_option autoImplicit false
set_option maxHeartbeats 2000000
namespace ChatgptAudit.FiniteResponseRecord
open Matrix TGLExt
noncomputable section

abbrev ResponseSamples := Fin 10 → ℝ

def probeDirections : Fin 10 → Coordinate4 :=
  ![![1,0,0,0], ![0,1,0,0], ![0,0,1,0], ![0,0,0,1],
    ![1,1,0,0], ![1,0,1,0], ![1,0,0,1],
    ![0,1,1,0], ![0,1,0,1], ![0,0,1,1]]

def sampleResponse (q : Coordinate4 → ℝ) : ResponseSamples :=
  fun i => q (probeDirections i)

def decodeResponse (s : ResponseSamples) : Tensor4 :=
  !![s 0, (s 4-s 0-s 1)/2, (s 5-s 0-s 2)/2, (s 6-s 0-s 3)/2;
     (s 4-s 0-s 1)/2, s 1, (s 7-s 1-s 2)/2, (s 8-s 1-s 3)/2;
     (s 5-s 0-s 2)/2, (s 7-s 1-s 2)/2, s 2, (s 9-s 2-s 3)/2;
     (s 6-s 0-s 3)/2, (s 8-s 1-s 3)/2, (s 9-s 2-s 3)/2, s 3]

theorem ten_probe_directions : Fintype.card (Fin 10)=10 := by norm_num

theorem decoded_response_symmetric (s : ResponseSamples) :
    (decodeResponse s)ᵀ=decodeResponse s := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

theorem quadratic_response_samples (A : Tensor4) (hs : Aᵀ=A) :
    sampleResponse (tensorQuad A) =
      ![A 0 0, A 1 1, A 2 2, A 3 3,
        A 0 0+A 1 1+2*A 0 1, A 0 0+A 2 2+2*A 0 2, A 0 0+A 3 3+2*A 0 3,
        A 1 1+A 2 2+2*A 1 2, A 1 1+A 3 3+2*A 1 3, A 2 2+A 3 3+2*A 2 3] := by
  funext i
  fin_cases i
  · change tensorQuad A ![1,0,0,0]=A 0 0
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]
  · change tensorQuad A ![0,1,0,0]=A 1 1
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]
  · change tensorQuad A ![0,0,1,0]=A 2 2
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]
  · change tensorQuad A ![0,0,0,1]=A 3 3
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]
  · change tensorQuad A ![1,1,0,0]=A 0 0+A 1 1+2*A 0 1
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]
  · change tensorQuad A ![1,0,1,0]=A 0 0+A 2 2+2*A 0 2
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]
  · change tensorQuad A ![1,0,0,1]=A 0 0+A 3 3+2*A 0 3
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]
  · change tensorQuad A ![0,1,1,0]=A 1 1+A 2 2+2*A 1 2
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]
  · change tensorQuad A ![0,1,0,1]=A 1 1+A 3 3+2*A 1 3
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]
  · change tensorQuad A ![0,0,1,1]=A 2 2+A 3 3+2*A 2 3
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]

theorem decode_quadratic_response (A : Tensor4) (hs : Aᵀ=A) :
    decodeResponse (sampleResponse (tensorQuad A))=A := by
  rw [quadratic_response_samples A hs]
  have h10 := congrArg (fun M : Tensor4 => M 1 0) hs
  have h20 := congrArg (fun M : Tensor4 => M 2 0) hs
  have h30 := congrArg (fun M : Tensor4 => M 3 0) hs
  have h21 := congrArg (fun M : Tensor4 => M 2 1) hs
  have h31 := congrArg (fun M : Tensor4 => M 3 1) hs
  have h32 := congrArg (fun M : Tensor4 => M 3 2) hs
  simp only [Matrix.transpose_apply] at h10 h20 h30 h21 h31 h32
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [decodeResponse, h10, h20, h30, h21, h31, h32] <;> ring

theorem sample_decoded_response (s : ResponseSamples) :
    sampleResponse (tensorQuad (decodeResponse s))=s := by
  rw [quadratic_response_samples _ (decoded_response_symmetric s)]
  funext i
  fin_cases i <;>
    norm_num [decodeResponse] <;> ring

theorem response_samples_determine_symmetric_tensor (A B : Tensor4)
    (hA : Aᵀ=A) (hB : Bᵀ=B)
    (hs : sampleResponse (tensorQuad A)=sampleResponse (tensorQuad B)) : A=B := by
  rw [← decode_quadratic_response A hA, hs, decode_quadratic_response B hB]

theorem decoded_response_injective : Function.Injective decodeResponse := by
  intro s t h
  simpa only [sample_decoded_response] using congrArg (fun A => sampleResponse (tensorQuad A)) h

theorem response_samples_equality_iff (A B : Tensor4) (hA : Aᵀ=A) (hB : Bᵀ=B) :
    sampleResponse (tensorQuad A)=sampleResponse (tensorQuad B) ↔ A=B := by
  exact ⟨response_samples_determine_symmetric_tensor A B hA hB, fun h => congrArg (fun M => sampleResponse (tensorQuad M)) h⟩

/-- A response law is a substantive hypothesis; it is not inferred from ten arbitrary numbers. -/
theorem finite_response_reconstructs_given_tensor (q : Coordinate4 → ℝ) (A : Tensor4)
    (hA : Aᵀ=A) (hq : ∀ d, q d=tensorQuad A d) :
    decodeResponse (sampleResponse q)=A := by
  have he : q=tensorQuad A := funext hq
  rw [he, decode_quadratic_response A hA]

theorem reconstructed_quadratic_matches_all_directions (q : Coordinate4 → ℝ)
    (A : Tensor4) (hA : Aᵀ=A) (hq : ∀ d, q d=tensorQuad A d) :
    ∀ d, tensorQuad (decodeResponse (sampleResponse q)) d=q d := by
  rw [finite_response_reconstructs_given_tensor q A hA hq]
  exact fun d => (hq d).symm

#print axioms ResponseSamples
#print axioms probeDirections
#print axioms sampleResponse
#print axioms decodeResponse
#print axioms ten_probe_directions
#print axioms decoded_response_symmetric
#print axioms quadratic_response_samples
#print axioms decode_quadratic_response
#print axioms sample_decoded_response
#print axioms response_samples_determine_symmetric_tensor
#print axioms decoded_response_injective
#print axioms response_samples_equality_iff
#print axioms finite_response_reconstructs_given_tensor
#print axioms reconstructed_quadratic_matches_all_directions
end
end ChatgptAudit.FiniteResponseRecord
