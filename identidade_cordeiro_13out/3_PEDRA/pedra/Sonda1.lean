import TGLExt.Fundacao
import TGLExt.TheVerbSelectsTheAction
open Matrix
#check @Matrix.trace_vecMulVec
#check @Matrix.vecMulVec_mul_vecMulVec
#check @Matrix.rank_vecMulVec_le
#check @Matrix.rank_of_isUnit
#check @Matrix.det_fin_two
#check @Matrix.isUnit_iff_isUnit_det
#check @Matrix.vecMulVec_mulVec
#check @Matrix.mulVec_vecMulVec
#check @inner_self_eq_norm_sq_to_K
#check @Real.sqrt_eq_zero_of_nonpos
#check @TGLExt.TheAxiomAndTheFalseWitness.the_power_has_two_fixed_points
#check @TGLExt.the_power_has_two_fixed_points
#check @Complex.conj_ofReal
#check @Matrix.dotProduct_comm
example : ("a" : String) ≠ "b" := by decide
