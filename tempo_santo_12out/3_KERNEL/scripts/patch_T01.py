"""Patch T00 -> T01 da pedra candidata (correcoes de robustez antes da 1a compilacao). Cada substituicao exige
padrao UNICO; se algum falhar, nada e gravado."""
import sys

p = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\3_KERNEL\sandbox\TheTimeHasNoRank.lean"
s = open(p, encoding="utf-8").read()


def R(a, b):
    global s
    c = s.count(a)
    if c != 1:
        sys.exit(f"PADRAO nao unico ({c}): {a[:90]!r}")
    s = s.replace(a, b)


# 1 hle tipado (sem 'simp only at')
R("""  have hle := isMaxOn_iff.mp hmax (z + s) hzs
  have hpos : 0 < Complex.normSq s := Complex.normSq_pos.mpr hs""",
  """  have hle : ((z + s) * (starRingEnd ℂ) s).re ≤ (z * (starRingEnd ℂ) s).re :=
    isMaxOn_iff.mp hmax (z + s) hzs
  have hpos : 0 < Complex.normSq s := Complex.normSq_pos.mpr hs""")
R("""    rw [add_mul, Complex.add_re, Complex.mul_conj, Complex.ofReal_re]
  simp only at hle
  linarith""", """    rw [add_mul, Complex.add_re, Complex.mul_conj, Complex.ofReal_re]
  linarith""")
# 2
R("""  have h00 := congrFun (congrFun h 0) 0
  simp [rhoD, absoluteRho] at h00
  norm_num at h00""", """  have h00 := congrFun (congrFun h 0) 0
  norm_num [rhoD, absoluteRho] at h00""")
# 3 show explicito nas isometrias
R("""  refine Isometry.of_dist_eq fun x y => ?_
  rw [dist_eq_norm, dist_eq_norm, ← mul_sub, norm_mul, Complex.norm_exp_ofReal_mul_I, one_mul]""",
  """  refine Isometry.of_dist_eq fun x y => ?_
  show dist (Complex.exp ((φ : ℂ) * Complex.I) * x) (Complex.exp ((φ : ℂ) * Complex.I) * y) = dist x y
  rw [dist_eq_norm, dist_eq_norm, ← mul_sub, norm_mul, Complex.norm_exp_ofReal_mul_I, one_mul]""")
R("""  refine Isometry.of_dist_eq fun x y => ?_
  rw [dist_eq_norm, dist_eq_norm]
  have hsub""", """  refine Isometry.of_dist_eq fun x y => ?_
  show dist (U * x * Uᴴ) (U * y * Uᴴ) = dist x y
  rw [dist_eq_norm, dist_eq_norm]
  have hsub""")
# 4
R("""      rw [sigma_diagonal_apply d hd t x i j]
      congr 1
      push_cast
      ring_nf""", """      rw [sigma_diagonal_apply d hd t x i j]
      congr 2
      push_cast
      ring""")
# 5
R("""  simp_rw [← Complex.exp_sum]
  rw [← Complex.exp_sum]
  have hz""", """  simp_rw [← Complex.exp_sum]
  have hz""")
# 6
R("""theorem probe_gRate_one_sum : ∑ i : Fin 2, ∑ j : Fin 2, gRate 1 i j = 2 := by
  simp [gRate, Fin.sum_univ_two]
  norm_num""", """theorem probe_gRate_one_sum : ∑ i : Fin 2, ∑ j : Fin 2, gRate 1 i j = 2 := by
  norm_num [gRate, Fin.sum_univ_two]""")
# 7
R("""    have := Real.add_one_le_exp (2 : ℝ)
    linarith
  nlinarith [he]""", """    have := Real.add_one_le_exp (2 : ℝ)
    linarith
  linarith""")
# 8
R("""    Complex.normSq_ofReal, mul_zero, neg_zero, Real.exp_zero, mul_one]
  rw [show -(2 * (1 : ℝ)) = -2 by norm_num]
  ring""", """    Complex.normSq_ofReal, mul_zero, neg_zero, Real.exp_zero, mul_one]
  ring""")
# 9
R("""  simp [dotProduct, Matrix.mulVec, Fin.sum_univ_two]
  ring""", """  simp only [dotProduct, Matrix.mulVec, Fin.sum_univ_two, Pi.star_apply, Matrix.cons_val_zero,
    Matrix.cons_val_one, Matrix.head_cons, star_one, star_neg]
  ring""")
# 10
R("""  simp only [Matrix.trace, Fin.sum_univ_two, Matrix.diag_apply, psiPlus_apply]
  push_cast; norm_num""", """  simp only [Matrix.trace, Fin.sum_univ_two, Matrix.diag_apply, psiPlus_apply]
  norm_num""")
# 11
R("""  have h0 : (0 : ℂ) ≤ 1 / 2 := by
    rw [Complex.le_def]; norm_num
  have h1 := (Matrix.posSemidef_conjTranspose_mul_self (!![(1 : ℂ), 1] : Matrix (Fin 1) (Fin 2) ℂ)).smul h0
  rw [hB] at h1
  exact h1""", """  have hc : ((1 / 2 : ℝ) : ℂ) = (1 / 2 : ℂ) := by norm_num
  have h0 : (0 : ℂ) ≤ ((1 / 2 : ℝ) : ℂ) := Complex.zero_le_real.mpr (by norm_num)
  have h1 := (Matrix.posSemidef_conjTranspose_mul_self (!![(1 : ℂ), 1] : Matrix (Fin 1) (Fin 2) ℂ)).smul h0
  rw [hB, hc] at h1
  exact h1""")
# 12
R("""theorem gRate_nonneg {γ : ℝ} (hγ : 0 ≤ γ) (i j : Fin 2) : 0 ≤ gRate γ i j := by
  unfold gRate; split_ifs <;> linarith""", """theorem gRate_nonneg {γ : ℝ} (hγ : 0 ≤ γ) (i j : Fin 2) : 0 ≤ gRate γ i j := by
  show (0 : ℝ) ≤ if i = j then 0 else γ
  split_ifs <;> linarith""")
# 13
R("""  | succ k ih => rw [Function.iterate_succ]; exact ih.comp hf""", """  | succ k ih => exact ih.comp hf""")
# 14
R("""  rw [commutator_far_from_scalar]
  simp [purityR, Complex.normSq_I]
  norm_num""", """  rw [commutator_far_from_scalar]
  norm_num [purityR, Complex.normSq_I]""")
# 15
R("""  rw [absoluteRho, ← Matrix.smul_one_eq_diagonal]
  congr 1
  simp
  norm_num""", """  rw [absoluteRho, ← Matrix.smul_one_eq_diagonal]
  congr 1
  norm_num [Fintype.card_fin]""")
# 16
R("""  ⟨fun hf _ _ h => isometry_orbit_converges_only_if_fixed hf h,
   fun φ hgrp hiso _ _ h => isometric_flow_converges_only_if_fixed φ hgrp hiso h,
   fun g t => dephase_volume g t,
   fun g hg hpos _ ht => dephase_volume_lt_one g hg hpos ht,
   fun d t => modular_volume_one d t,
   fun g hg _ ht x _ _ hpos hx => purityR_dephase_lt g hg ht x hpos hx,
   fun hγ ht => inverse_dephasing_not_positive hγ ht,
   fun hκ t => clock_reads_modulo_period hκ t,
   frozen_clock⟩""", """by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro X _ f hf x z h; exact isometry_orbit_converges_only_if_fixed hf h
  · intro X _ φ hgrp hiso x z h; exact isometric_flow_converges_only_if_fixed φ hgrp hiso h
  · intro n _ _ g t; exact dephase_volume g t
  · intro n _ g hg hpos t ht; exact dephase_volume_lt_one g hg hpos ht
  · intro n _ _ d t; exact modular_volume_one d t
  · intro n _ g hg t ht x i₀ j₀ hpos hx; exact purityR_dephase_lt g hg ht x hpos hx
  · intro γ t hγ ht; exact inverse_dephasing_not_positive hγ ht
  · intro κ hκ t; exact clock_reads_modulo_period hκ t
  · exact frozen_clock""")
# 17 sem smul_eq_zero
R("""    have h2 := add_left_cancel h1
    have h3 : (((Real.exp (-(t + t)) : ℝ) : ℂ) - ((Real.exp (-t) : ℝ) : ℂ)) • ((1 : A) - P) = 0 := by
      rw [sub_smul, h2, sub_self]
    rcases smul_eq_zero.mp h3 with h4 | h4
    · have h5 : Real.exp (-(t + t)) = Real.exp (-t) := by exact_mod_cast sub_eq_zero.mp h4
      have h6 := Real.exp_injective h5
      linarith
    · exact absurd h4 hP1""", """    have h2 := add_left_cancel h1
    have h3 : (((Real.exp (-(t + t)) : ℝ) : ℂ) - ((Real.exp (-t) : ℝ) : ℂ)) • ((1 : A) - P) = 0 := by
      rw [sub_smul, h2, sub_self]
    by_contra ht
    have hc : (((Real.exp (-(t + t)) : ℝ) : ℂ) - ((Real.exp (-t) : ℝ) : ℂ)) ≠ 0 := by
      intro hc0
      have h5 : Real.exp (-(t + t)) = Real.exp (-t) := by exact_mod_cast sub_eq_zero.mp hc0
      have h6 := Real.exp_injective h5
      exact ht (by linarith)
    apply hP1
    calc (1 : A) - P
        = ((((Real.exp (-(t + t)) : ℝ) : ℂ) - ((Real.exp (-t) : ℝ) : ℂ))⁻¹
            * (((Real.exp (-(t + t)) : ℝ) : ℂ) - ((Real.exp (-t) : ℝ) : ℂ))) • ((1 : A) - P) := by
          rw [inv_mul_cancel₀ hc, one_smul]
      _ = ((((Real.exp (-(t + t)) : ℝ) : ℂ) - ((Real.exp (-t) : ℝ) : ℂ))⁻¹)
            • ((((Real.exp (-(t + t)) : ℝ) : ℂ) - ((Real.exp (-t) : ℝ) : ℂ)) • ((1 : A) - P)) := by
          rw [mul_smul]
      _ = 0 := by rw [h3, smul_zero]""")
# 18 sonda sem nhds no enunciado
R("""/-- Sonda da cláusula composta T9.e em `A = M₂(ℂ)` (norma de operador L2), `P = diag(1, 0)`. -/
theorem probe_the_time_has_no_rank :
    ¬ IsUnit postDiag ∧
      Filter.Tendsto (TheAxiomAndTheFalseWitness.axiomFlow postDiag) Filter.atTop (nhds postDiag) :=
  ⟨(the_time_has_no_rank (A := Matrix (Fin 2) (Fin 2) ℂ) postDiag_idem postDiag_ne_one).2.2.2.1,
    (the_time_has_no_rank (A := Matrix (Fin 2) (Fin 2) ℂ) postDiag_idem postDiag_ne_one).2.2.2.2⟩""",
  """/-- Sonda da cláusula composta T9.e em `A = M₂(ℂ)` (norma de operador L2), `P = diag(1, 0)`: a conjunção
    inteira é instanciada (hipóteses habitadas); daqui se extrai `¬ IsUnit P`. -/
theorem probe_the_time_has_no_rank : ¬ IsUnit postDiag :=
  (the_time_has_no_rank (A := Matrix (Fin 2) (Fin 2) ℂ) postDiag_idem postDiag_ne_one).2.2.2.1

example : True := by
  have _h := (the_time_has_no_rank (A := Matrix (Fin 2) (Fin 2) ℂ) postDiag_idem postDiag_ne_one).2.2.2.2
  trivial""")
# 19
R("""  rw [Matrix.posSemidef_diagonal_iff]
  intro i
  fin_cases i
  · exact Complex.zero_le_real.mpr hp0
  · exact Complex.zero_le_real.mpr (by linarith)""", """  rw [Matrix.posSemidef_diagonal_iff]
  intro i
  fin_cases i
  · show (0 : ℂ) ≤ ((p : ℝ) : ℂ)
    exact Complex.zero_le_real.mpr hp0
  · show (0 : ℂ) ≤ (((1 - p : ℝ)) : ℂ)
    exact Complex.zero_le_real.mpr (by linarith)""")

with open(p, "w", encoding="utf-8", newline="\n") as fo:
    fo.write(s)
print("ok", len(s.encode("utf-8")))
