import TGLExt.TheAxiomAndTheFalseWitness
open TGLExt.TheAxiomAndTheFalseWitness

/-- teste da aferição (NÃO é pedra): a forma escrita «F = e^{−t·H_min}» é teorema? -/
theorem afericao_axiomFlow_eq_exp {A : Type*} [NormedRing A] [NormedAlgebra ℂ A] [CompleteSpace A]
    {P : A} (hP : IsIdempotentElem P) (t : ℝ) :
    NormedSpace.exp ((-(t : ℂ)) • (1 - P)) = axiomFlow P t := by
  set Q : A := 1 - P with hQdef
  have hQ : IsIdempotentElem Q := hP.one_sub
  set c : ℂ := -(t : ℂ) with hc
  have h1 := NormedSpace.exp_series_hasSum_exp' (𝕂 := ℂ) (c • Q)
  have hs : HasSum (fun n : ℕ => (n.factorial⁻¹ : ℂ) • c ^ n) (NormedSpace.exp c) :=
    NormedSpace.exp_series_hasSum_exp' (𝕂 := ℂ) c
  have h2 := hs.smul_const Q
  have h3 : HasSum (fun n : ℕ => if n = 0 then (1 - Q) else 0) (1 - Q) := hasSum_ite_eq 0 (1 - Q)
  have h4 := h2.add h3
  have heq : (fun n : ℕ => (n.factorial⁻¹ : ℂ) • (c • Q) ^ n)
      = (fun n : ℕ => ((n.factorial⁻¹ : ℂ) • c ^ n) • Q + (if n = 0 then (1 - Q) else 0)) := by
    funext n
    rcases Nat.eq_zero_or_pos n with h0 | hpos
    · subst h0; simp
    · have hn : n ≠ 0 := Nat.pos_iff_ne_zero.mp hpos
      rw [if_neg hn, add_zero, smul_pow, hQ.pow_eq hn, smul_smul, smul_eq_mul]
  rw [heq] at h1
  have hval := h1.unique h4
  rw [hval, ← Complex.exp_eq_exp_ℂ, hc, ← Complex.ofReal_neg, ← Complex.ofReal_exp]
  unfold axiomFlow
  rw [hQdef, sub_sub_cancel, add_comm]

#print axioms afericao_axiomFlow_eq_exp
