import TGLExt.F1Fecho394.MaxwellScreenIntertwinerR2
import TGLExt.F1Fecho394.SchwartzMaxwellCoefficientR5
import Mathlib.Analysis.Normed.Module.FiniteDimension

/-! Covariant test tensors transform by A-transpose T A. Their contraction
with p wedge epsilon therefore transports both contravariant vectors by A.
This finite algebra supplies the tensor part of the physical test action. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open Matrix
namespace F1Fecho.CovariantTensor
open F1Fecho.MaxwellGlobal F1Fecho.MaxwellOnShell

def pullLinear (A:Matrix (Fin 4) (Fin 4) ℂ) : TensorValue→ₗ[ℂ]TensorValue where
  toFun T := A.transpose*(Matrix.of T)*A
  map_add' T U := by
    change A.transpose*(Matrix.of T+Matrix.of U)*A=_
    simp only [Matrix.mul_add,Matrix.add_mul]
    rfl
  map_smul' c T := by
    change A.transpose*(c • Matrix.of T)*A=c • (A.transpose*Matrix.of T*A)
    simp only [Matrix.mul_smul,Matrix.smul_mul]

def pull (A:Matrix (Fin 4) (Fin 4) ℂ) : TensorValue→L[ℂ]TensorValue :=
  (pullLinear A).toContinuousLinearMap

def contraction (p e:Fin 4→ℂ) (T:TensorValue) : ℂ :=
  dotProduct p ((Matrix.of T).mulVec e)-dotProduct e ((Matrix.of T).mulVec p)

theorem contraction_eq_sum (p e:Fin 4→ℂ) (T:TensorValue) :
    contraction p e T=∑μ,∑ν,(p μ*e ν-p ν*e μ)*T μ ν := by
  simp only [contraction,Matrix.mulVec,dotProduct,Finset.mul_sum,
    Finset.sum_sub_distrib,sub_mul]
  congr 1 <;> apply Finset.sum_congr rfl <;> intro μ hμ <;>
    apply Finset.sum_congr rfl <;> intro ν hν <;> simp only [Matrix.of_apply] <;> ring

theorem contraction_pull (A:Matrix (Fin 4) (Fin 4) ℂ)
    (p e:Fin 4→ℂ) (T:TensorValue) :
    contraction p e (pull A T)=contraction (A.mulVec p) (A.mulVec e) T := by
  change dotProduct p ((A.transpose*(Matrix.of T)*A).mulVec e)-
      dotProduct e ((A.transpose*(Matrix.of T)*A).mulVec p)=_
  simp only [←Matrix.mulVec_mulVec,Matrix.dotProduct_transpose_mulVec,contraction]
  rw [dotProduct_comm ((Matrix.of T).mulVec (A.mulVec e)),
    dotProduct_comm ((Matrix.of T).mulVec (A.mulVec p))]

theorem real_contraction_eq_sum (p e:Fin 4→ℝ) (T:TensorValue) :
    contraction (realLift p) (realLift e) T=
      ∑μ,∑ν,(realStrength p e μ ν:ℂ)*T μ ν := by
  rw [contraction_eq_sum]
  simp only [realLift,realStrength,Complex.ofReal_sub,Complex.ofReal_mul]

theorem pull_real (A:Matrix (Fin 4) (Fin 4) ℝ) (T:TensorValue)
    (hT:∀μ ν,(T μ ν).im=0) : ∀μ ν,(pull (A.map Complex.ofReal) T μ ν).im=0 := by
  intro μ ν
  change (((A.map Complex.ofReal).transpose*(Matrix.of T)*A.map Complex.ofReal) μ ν).im=0
  simp [Matrix.mul_apply,Matrix.transpose_apply,Matrix.map_apply,Complex.mul_im,hT]

end F1Fecho.CovariantTensor
#print axioms F1Fecho.CovariantTensor.pull
#print axioms F1Fecho.CovariantTensor.contraction_eq_sum
#print axioms F1Fecho.CovariantTensor.contraction_pull
#print axioms F1Fecho.CovariantTensor.real_contraction_eq_sum
#print axioms F1Fecho.CovariantTensor.pull_real
