import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.Tactic
/-!
The one-excitation jump already written in the device/clock contract is
J=|b><a|+|c><b| on the basis (a,b,c). This file formalizes the existing
Schrodinger-picture obstruction: its isolated dissipator is not unital,
whereas every Hermitian-jump dissipator annihilates the identity.
Thus no change by a unital algebra equivalence, even with nonzero time scaling,
identifies these isolated generators. This does not exclude a dilation,
effective reduction, additional balancing channels, or the full device model.
It does not concern the always-unital Heisenberg dual of a trace-preserving map.
-/
set_option autoImplicit false
set_option maxHeartbeats 500000
noncomputable section
namespace F1Fecho.DeviceRootObstruction
open Matrix
abbrev M := Matrix (Fin 3) (Fin 3) ℂ

def dissipator (L ρ : M) : M :=
  L * ρ * Lᴴ - (1/2 : ℂ) • (Lᴴ * L * ρ + ρ * Lᴴ * L)

theorem dissipator_one (L : M) : dissipator L 1 = L*Lᴴ-Lᴴ*L := by
  simp only [dissipator,mul_one,one_mul,smul_add,← add_smul]
  norm_num

theorem hermitian_jump_annihilates_one (L : M) (hL : Lᴴ=L) : dissipator L 1 = 0 := by
  rw [dissipator_one,hL,sub_self]

def deviceJump : M := fun i j => if (i.val=1 ∧ j.val=0) ∨ (i.val=2 ∧ j.val=1) then 1 else 0

theorem device_jump_on_one : dissipator deviceJump 1 = (fun i j => if i.val=j.val then (if i.val=0 then -1 else if i.val=2 then 1 else 0) else 0) := by
  rw [dissipator_one]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [deviceJump,Matrix.mul_apply,Fin.sum_univ_three,Matrix.conjTranspose_apply]

theorem device_jump_not_unital : dissipator deviceJump 1 ≠ 0 := by
  intro h
  have he := congrArg (fun A : M => A 2 2) h
  rw [device_jump_on_one] at he
  norm_num at he

def generator (H L : M) (rate : ℂ) (ρ : M) : M :=
  -Complex.I • (H*ρ-ρ*H) + rate • dissipator L ρ

theorem generator_one (H L : M) (rate : ℂ) :
    generator H L rate 1 = rate • dissipator L 1 := by
  simp [generator]

theorem no_unital_conjugacy (H K L : M) (hL : Lᴴ=L)
    (rate otherRate : ℂ) (hrate : rate ≠ 0) (e : M ≃ₐ[ℂ] M) :
    ¬ ∀ ρ : M, generator H deviceJump rate ρ = e (generator K L otherRate (e.symm ρ)) := by
  intro h
  have he := h 1
  simp only [map_one,generator_one,hermitian_jump_annihilates_one L hL,
    smul_zero,map_zero] at he
  have hv := congrArg (fun A : M => A 2 2) he
  rw [device_jump_on_one] at hv
  simp at hv
  exact hrate hv

end F1Fecho.DeviceRootObstruction
#print axioms F1Fecho.DeviceRootObstruction.dissipator_one
#print axioms F1Fecho.DeviceRootObstruction.hermitian_jump_annihilates_one
#print axioms F1Fecho.DeviceRootObstruction.device_jump_on_one
#print axioms F1Fecho.DeviceRootObstruction.device_jump_not_unital
#print axioms F1Fecho.DeviceRootObstruction.generator_one
#print axioms F1Fecho.DeviceRootObstruction.no_unital_conjugacy
