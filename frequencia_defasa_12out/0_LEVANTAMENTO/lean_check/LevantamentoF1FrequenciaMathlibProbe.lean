/-
  LEVANTAMENTO F1.FREQUENCIA (12/10/2026) — SONDA DE NOMES DA MATHLIB PINADA NO NOS (posto, nulidade, pureza).
  Somente #check. Um nome ausente produz erro e fica registrado como ausente nesta versao; nao e falha do kernel.
-/
import Mathlib

#check @LinearMap.finrank_range_add_finrank_ker
#check @Matrix.rank
#check @Matrix.rank_mul_le_left
#check @Matrix.rank_mul_le_right
#check @Matrix.rank_mul_eq_left_of_isUnit_det
#check @Matrix.rank_mul_eq_right_of_isUnit_det
#check @Matrix.rank_diagonal
#check @Matrix.rank_conjTranspose_mul_self
#check @Matrix.IsHermitian.rank_eq_card_non_zero_eigs
#check @Matrix.rank_vecMulVec
#check @Matrix.rank_vecMulVec_le
#check @InnerProductSpace.rankOne
#check @InnerProductSpace.isStarProjection_rankOne_self
#check @finrank_span_singleton
#check @Matrix.trace_mul_comm
#check @Matrix.PosSemidef.eigenvalues_nonneg
#check @Matrix.IsHermitian.eigenvalues
#check @Matrix.IsHermitian.spectral_theorem
#check @Matrix.posSemidef_vecMulVec_self_star
