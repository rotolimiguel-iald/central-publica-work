/- SONDA DE API 2 (3_KERNEL): nomes restantes. Nao e pedra. -/
import Mathlib

open Matrix
#check @Unitary.star_mul_self_of_mem
#check @Unitary.mul_star_self_of_mem
#check @Unitary.coe_star_mul_self
#check @Module.End.mul_eq_comp
#check @LinearMap.mul_eq_comp
#check @Matrix.mulVecLin_mul
#check @smul_mul_smul_comm
#check @smul_mul_smul
#check @Matrix.vecMulVec_mul
#check @Matrix.mul_vecMulVec
#check @Matrix.vecMulVec_smul
#check @Matrix.smul_vecMulVec
#check @Matrix.dotProduct_mulVec
#check @dotProduct_comm
#check @Matrix.dotProduct_comm
#check @Matrix.vecMul_vecMulVec
#check @Matrix.vecMulVec_mulVec
#check @Complex.nonneg_iff
#check @Real.sqrt_eq_zero'
#check @Real.sqrt_eq_zero
#check @Matrix.det_diagonal
#check @Fin.prod_univ_three
#check @Fin.sum_univ_three
#check @Fin.sum_univ_four
#check @Real.sin_pi_div_two
#check @Real.cos_pi_div_two
#check @Real.exp_lt_one
#check @Real.exp_eq_one_iff
#check @Real.sin_one_pos
#check @Real.sin_pos_of_pos_of_lt_pi
#check @Matrix.PosSemidef.smul
#check @Matrix.diagonal_injective
#check @LinearEquiv.map_eq_zero_iff
#check @Submodule.mem_span_singleton
#check @Submodule.span_le
#check @Matrix.trace_smul
#check @Matrix.cons_val'
#check @Complex.ofReal_eq_zero
#check @Complex.normSq_ofReal
#check @Matrix.IsHermitian.eigenvectorBasis
example (x : ℝ) : (RCLike.ofReal x : ℂ) = (x : ℂ) := rfl
example (n : Type) [Fintype n] [DecidableEq n] (A : Matrix n n ℂ) : A.rank = Module.finrank ℂ (LinearMap.range A.mulVecLin) := rfl
open Lean in
#eval show CoreM Unit from do
  let env ← getEnv
  let some idx := env.getModuleIdx? `Mathlib.LinearAlgebra.Matrix.Rank | throwError "x"
  IO.println s!"constNames: {(env.header.moduleData[idx.toNat]!).constNames.size}"
