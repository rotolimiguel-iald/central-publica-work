import GeneralMetricEinstein
import TGLExt.CoherentScalarStress

set_option autoImplicit false
set_option maxHeartbeats 3500000
namespace ChatgptAudit.SignedCoverage
open Matrix Set TGLExt ChatgptAudit.GeneralMetric ChatgptAudit.Coherent023
open scoped ContDiff
noncomputable section

def traceReverse (g gi A : Tensor4) : Tensor4 :=
  A - (Matrix.trace (gi * A) / 2) • g

def plusCovector (A : Tensor4) (i : Fin 4) : Coordinate4 :=
  fun j => (A i j + if i = j then 1 else 0) / 2

def minusCovector (A : Tensor4) (i : Fin 4) : Coordinate4 :=
  fun j => (A i j - if i = j then 1 else 0) / 2

theorem polarization_pair_entry (A : Tensor4) (i j k : Fin 4) :
    (Matrix.vecMulVec (plusCovector A i) (plusCovector A i) -
      Matrix.vecMulVec (minusCovector A i) (minusCovector A i)) j k =
    (A i j * (if i=k then 1 else 0) + (if i=j then 1 else 0) * A i k) / 2 := by
  simp only [Matrix.sub_apply, Matrix.vecMulVec, Matrix.of_apply, plusCovector, minusCovector]
  ring

theorem signed_polarization (A : Tensor4) (hs : Aᵀ=A) :
    (∑ i : Fin 4, (Matrix.vecMulVec (plusCovector A i) (plusCovector A i) -
      Matrix.vecMulVec (minusCovector A i) (minusCovector A i))) = A := by
  ext j k
  simp only [Matrix.sum_apply, polarization_pair_entry, add_div, Finset.sum_add_distrib]
  simp only [mul_ite, ite_mul, mul_one, mul_zero, one_mul, zero_mul]
  rw [← Finset.sum_div, ← Finset.sum_div]
  simp only [Finset.sum_ite_eq', Finset.mem_univ, if_true]
  have h := congrArg (fun M : Tensor4 => M j k) hs
  simp only [Matrix.transpose_apply] at h
  rw [h]
  ring

theorem trace_reverse_symmetric (g gi A : Tensor4) (hg : gᵀ=g) (hA : Aᵀ=A) :
    (traceReverse g gi A)ᵀ=traceReverse g gi A := by
  simp only [traceReverse, Matrix.transpose_sub, Matrix.transpose_smul, hg, hA]

theorem trace_reverse_add (g gi A B : Tensor4) :
    traceReverse g gi (A+B)=traceReverse g gi A+traceReverse g gi B := by
  simp only [traceReverse, Matrix.mul_add, Matrix.trace_add, add_div, add_smul]
  abel

theorem trace_reverse_sub (g gi A B : Tensor4) :
    traceReverse g gi (A-B)=traceReverse g gi A-traceReverse g gi B := by
  simp only [traceReverse, Matrix.mul_sub, Matrix.trace_sub, sub_div, sub_smul]
  abel

theorem trace_reverse_sum {ι : Type} [Fintype ι] (g gi : Tensor4) (A : ι → Tensor4) :
    traceReverse g gi (∑ i, A i)=∑ i, traceReverse g gi (A i) := by
  simp only [traceReverse, Matrix.mul_sum, Matrix.trace_sum, Finset.sum_div,
    Finset.sum_smul, Finset.sum_sub_distrib]

theorem trace_reverse_trace (g gi A : Tensor4) (hi : gi*g=1) :
    Matrix.trace (gi*traceReverse g gi A) = -Matrix.trace (gi*A) := by
  simp only [traceReverse, Matrix.mul_sub, Matrix.mul_smul, Matrix.trace_sub,
    Matrix.trace_smul, hi]
  norm_num
  ring

theorem trace_reverse_involutive (g gi A : Tensor4) (hi : gi*g=1) :
    traceReverse g gi (traceReverse g gi A)=A := by
  rw [traceReverse, trace_reverse_trace g gi A hi]
  simp only [traceReverse, neg_div, neg_smul]
  abel

theorem trace_outer_is_quad (gi : Tensor4) (w : Coordinate4) :
    Matrix.trace (gi*Matrix.vecMulVec w w)=tensorQuad gi w := by
  rw [Matrix.mul_vecMulVec, Matrix.trace_vecMulVec, dotProduct_comm]
  rfl

theorem trace_reverse_outer (g gi : Tensor4) (w : Coordinate4) :
    traceReverse g gi (Matrix.vecMulVec w w)=covectorStress g gi w 1 := by
  simp only [traceReverse, trace_outer_is_quad, covectorStress, one_smul]

theorem signed_pair_stress (g gi A : Tensor4) (i : Fin 4) :
    covectorStress g gi (plusCovector A i) 1 +
      covectorStress g gi (minusCovector A i) (-1) =
    traceReverse g gi (Matrix.vecMulVec (plusCovector A i) (plusCovector A i) -
      Matrix.vecMulVec (minusCovector A i) (minusCovector A i)) := by
  rw [trace_reverse_sub, trace_reverse_outer, trace_reverse_outer]
  simp only [covectorStress, one_smul, neg_one_smul, sub_eq_add_neg]

def signedStress (g gi A : Tensor4) : Tensor4 :=
  ∑ i : Fin 4, (covectorStress g gi (plusCovector A i) 1 +
    covectorStress g gi (minusCovector A i) (-1))

theorem signed_stress_is_trace_reverse (g gi A : Tensor4) (hA : Aᵀ=A) :
    signedStress g gi A=traceReverse g gi A := by
  unfold signedStress
  simp only [signed_pair_stress]
  rw [← trace_reverse_sum, signed_polarization A hA]

theorem every_symmetric_source_has_eight_covectors (g gi T : Tensor4)
    (hi : gi*g=1) (hg : gᵀ=g) (hT : Tᵀ=T) :
    signedStress g gi (traceReverse g gi T)=T := by
  rw [signed_stress_is_trace_reverse g gi _ (trace_reverse_symmetric g gi T hg hT),
    trace_reverse_involutive g gi T hi]

theorem plus_covector_smooth (U : Set Coordinate4) (A : TensorField4)
    (hA : SmoothMatrixOn U A) (i : Fin 4) :
    SmoothVectorOn U (fun x => plusCovector (A x) i) := by
  intro j
  exact ((hA i j).add contDiffOn_const).div_const 2

theorem minus_covector_smooth (U : Set Coordinate4) (A : TensorField4)
    (hA : SmoothMatrixOn U A) (i : Fin 4) :
    SmoothVectorOn U (fun x => minusCovector (A x) i) := by
  intro j
  exact ((hA i j).sub contDiffOn_const).div_const 2

theorem trace_reverse_field_smooth (U : Set Coordinate4) (g gi A : TensorField4)
    (hg : SmoothMatrixOn U g) (hgi : SmoothMatrixOn U gi) (hA : SmoothMatrixOn U A) :
    SmoothMatrixOn U (fun x => traceReverse (g x) (gi x) (A x)) := by
  have hprod := SmoothMatrixOn.mul U gi A hgi hA
  have hsum : ContDiffOn ℝ ∞ (fun x => ∑ i : Fin 4, (gi x*A x) i i) U := by
    apply ContDiffOn.sum
    intro i _
    exact hprod i i
  have ht : ContDiffOn ℝ ∞ (fun x => Matrix.trace (gi x*A x)/2) U := by
    simpa only [Matrix.trace, Matrix.diag] using hsum.div_const 2
  intro i j
  exact (hA i j).sub (ht.mul (hg i j))

theorem smooth_metric_source_has_smooth_eight_covectors
    (U : Set Coordinate4) (g T : TensorField4)
    (hg : SmoothMatrixOn U g) (hT : SmoothMatrixOn U T)
    (hLor : ∀ x∈U, LorentzByCongruence (g x)) :
    (∀ i, SmoothVectorOn U
      (fun x => plusCovector (traceReverse (g x) (metricInverse g x) (T x)) i)) ∧
    (∀ i, SmoothVectorOn U
      (fun x => minusCovector (traceReverse (g x) (metricInverse g x) (T x)) i)) := by
  have hf := trace_reverse_field_smooth U g (metricInverse g) T hg
    (constructed_metric_inverse_smooth U g hg hLor) hT
  exact ⟨fun i => plus_covector_smooth U _ hf i, fun i => minus_covector_smooth U _ hf i⟩

theorem every_smooth_lorentz_source_is_represented
    (U : Set Coordinate4) (g T : TensorField4)
    (hLor : ∀ x∈U, LorentzByCongruence (g x))
    (hT : ∀ x∈U, (T x)ᵀ=T x) :
    ∀ x∈U, signedStress (g x) (metricInverse g x)
      (traceReverse (g x) (metricInverse g x) (T x))=T x := by
  intro x hx
  exact every_symmetric_source_has_eight_covectors (g x) (metricInverse g x) (T x)
    (constructed_metric_inverse_left U g hLor x hx)
    (lorentz_metric_symmetric (g x) (hLor x hx)) (hT x hx)

#print axioms traceReverse
#print axioms plusCovector
#print axioms minusCovector
#print axioms polarization_pair_entry
#print axioms signed_polarization
#print axioms trace_reverse_symmetric
#print axioms trace_reverse_add
#print axioms trace_reverse_sub
#print axioms trace_reverse_sum
#print axioms trace_reverse_trace
#print axioms trace_reverse_involutive
#print axioms trace_outer_is_quad
#print axioms trace_reverse_outer
#print axioms signed_pair_stress
#print axioms signedStress
#print axioms signed_stress_is_trace_reverse
#print axioms every_symmetric_source_has_eight_covectors
#print axioms plus_covector_smooth
#print axioms minus_covector_smooth
#print axioms trace_reverse_field_smooth
#print axioms smooth_metric_source_has_smooth_eight_covectors
#print axioms every_smooth_lorentz_source_is_represented
end
end ChatgptAudit.SignedCoverage
