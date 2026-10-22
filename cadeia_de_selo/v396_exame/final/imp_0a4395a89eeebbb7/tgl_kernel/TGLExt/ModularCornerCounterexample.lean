import TGLExt.SMatrix

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ModularCornerCounterexample
open Matrix NormedSpace TGLExt
noncomputable section

abbrev M2 := Matrix (Fin 2) (Fin 2) ℂ
def p : M2 := !![1,0;0,0]
/-- A selfadjoint Pauli generator, unitarily equivalent to sigma_x. -/
def residual : M2 := Complex.I • Grot
def flow (s : ℝ) : M2 := exp ((-(s : ℂ)*Complex.I) • residual)

theorem p_projection : p*p=p ∧ pᴴ=p := by
  constructor <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [p,Matrix.mul_apply,Fin.sum_univ_two,Matrix.conjTranspose_apply]

theorem residual_selfadjoint : residualᴴ=residual := by
  rw [residual, Matrix.conjTranspose_smul, Grot_conjTranspose]
  simp

theorem compressed_generator_zero : p*residual*p=0 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [p,residual,Grot,Matrix.mul_apply,Fin.sum_univ_two]

theorem residual_nonzero : residual ≠ 0 := by
  intro h
  have hh := congrArg (fun a : M2 => a 0 1) h
  simp [residual,Grot] at hh

/-- Reuses the existing matrix-S exponential theorem; no new evolution postulate. -/
theorem flow_eq (s : ℝ) : flow s=Smat s := by
  unfold flow residual
  rw [smul_smul]
  have h : (-(s : ℂ)*Complex.I)*Complex.I = (s : ℂ) := by
    simp [mul_assoc]
  rw [h]
  exact exp_smul_Grot s

theorem compressed_flow (s : ℝ) : p*flow s*p=(Real.cos s : ℂ) • p := by
  rw [flow_eq,Smat_eq]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [p,Matrix.mul_apply,Fin.sum_univ_two]

theorem compressed_flow_half_turn : p*flow (Real.pi/2)*p=0 := by
  rw [compressed_flow,Real.cos_pi_div_two,Complex.ofReal_zero,zero_smul]

theorem p_nonzero : p ≠ 0 := by
  intro h
  have hh := congrArg (fun a : M2 => a 0 0) h
  simp [p] at hh

theorem compression_does_not_control_flow :
    p*residual*p=0 ∧ p*flow (Real.pi/2)*p ≠ p := by
  exact ⟨compressed_generator_zero, by rw [compressed_flow_half_turn]; exact Ne.symm p_nonzero⟩

theorem half_turn_leaves_corner :
    flow (Real.pi/2)*p*(flow (Real.pi/2))ᴴ=1-p := by
  rw [flow_eq,Smat_eq]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [p,Matrix.mul_apply,Fin.sum_univ_two,Matrix.conjTranspose_apply]

theorem corner_not_invariant :
    flow (Real.pi/2)*p*(flow (Real.pi/2))ᴴ ≠ p := by
  rw [half_turn_leaves_corner]
  intro h
  have hh := congrArg (fun a : M2 => a 0 0) h
  norm_num [p] at hh

#print axioms p_projection
#print axioms residual_selfadjoint
#print axioms compressed_generator_zero
#print axioms residual_nonzero
#print axioms flow_eq
#print axioms compressed_flow
#print axioms compressed_flow_half_turn
#print axioms p_nonzero
#print axioms compression_does_not_control_flow
#print axioms half_turn_leaves_corner
#print axioms corner_not_invariant
end
end ModularCornerCounterexample
