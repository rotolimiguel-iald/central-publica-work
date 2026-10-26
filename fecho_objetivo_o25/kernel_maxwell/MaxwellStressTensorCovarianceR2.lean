import MaxwellStressJetAlgebraR3
import CartesianMaxwellBianchiR3
import TGLExt.PoincareGroup

/-! Algebraic tensor covariance of the actual quadratic Maxwell stress.
The matrix theorem is generic; Lorentz metric preservation is supplied by
existing LorentzGrp terms, not by a new stress-covariance assumption. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellStress
open Matrix
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def quadraticTensor (η F : Matrix ι ι ℂ) : Matrix ι ι ℂ := F*η*F.transpose

def stressMatrix (η F : Matrix ι ι ℂ) : Matrix ι ι ℂ :=
  -quadraticTensor η F+((1/4:ℂ)*(η*quadraticTensor η F).trace) • η

theorem quadraticTensor_apply (s : ι→ℂ) (F : Matrix ι ι ℂ) (μ ν : ι) :
    quadraticTensor (Matrix.diagonal s) F μ ν=∑α,s α*F μ α*F ν α := by
  simp [quadraticTensor,Matrix.mul_apply,Matrix.transpose_apply,Matrix.diagonal_apply,
    mul_comm,mul_left_comm,mul_assoc]

theorem stress_as_matrix (s : ι→ℂ) (F : ι→ι→ℂ) :
    Matrix.of (stress s F)=stressMatrix (Matrix.diagonal s) (Matrix.of F) := by
  have ht : (Matrix.diagonal s * quadraticTensor (Matrix.diagonal s) (Matrix.of F)).trace =
      ∑ α, ∑ β, s α * s β * F α β * F α β := by
    simp [Matrix.trace, Matrix.diag, Matrix.diagonal_mul,
      quadraticTensor_apply, Finset.mul_sum, mul_assoc]
  ext μ ν
  simp only [stress,stressMatrix,Matrix.add_apply,Matrix.neg_apply,Matrix.smul_apply,
    smul_eq_mul,quadraticTensor_apply,Matrix.of_apply,ht,Matrix.diagonal_apply]
  ring

theorem quadraticTensor_covariant (η A F : Matrix ι ι ℂ)
    (hA : A*η*A.transpose=η) :
    quadraticTensor η (A.transpose*F*A)=A.transpose*quadraticTensor η F*A := by
  unfold quadraticTensor
  rw [Matrix.transpose_mul,Matrix.transpose_mul,Matrix.transpose_transpose]
  calc
    _ = A.transpose*F*(A*η*A.transpose)*F.transpose*A := by noncomm_ring
    _ = _ := by rw [hA]; noncomm_ring

theorem tensorTrace_covariant (η A Q : Matrix ι ι ℂ)
    (hA : A*η*A.transpose=η) :
    (η*(A.transpose*Q*A)).trace=(η*Q).trace := by
  calc
    _ = ((η*A.transpose*Q)*A).trace := by congr 1; noncomm_ring
    _ = (A*(η*A.transpose*Q)).trace := Matrix.trace_mul_comm _ _
    _ = ((A*η*A.transpose)*Q).trace := by congr 1; noncomm_ring
    _ = _ := by rw [hA]

theorem stressMatrix_covariant (η A F : Matrix ι ι ℂ)
    (hA : A*η*A.transpose=η) (hAt : A.transpose*η*A=η) :
    stressMatrix η (A.transpose*F*A)=A.transpose*stressMatrix η F*A := by
  unfold stressMatrix
  rw [quadraticTensor_covariant η A F hA,tensorTrace_covariant η A _ hA]
  simp only [Matrix.mul_add,Matrix.add_mul,Matrix.mul_neg,Matrix.neg_mul,
    Matrix.mul_smul,Matrix.smul_mul,hAt]

end F1Fecho.MaxwellStress
#print axioms F1Fecho.MaxwellStress.stress_as_matrix
#print axioms F1Fecho.MaxwellStress.stressMatrix_covariant
