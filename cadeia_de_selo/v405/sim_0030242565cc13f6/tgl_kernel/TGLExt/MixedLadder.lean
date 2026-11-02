import TGLExt.PowersLadder

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A MISTURA: a marca de III₁ — o reticulado de razões DENSO
  [TGLExt — v125, o incremento 44 do programa SemifiniteAnalysis]

A escada de Powers (v124) deu a UMA razão λ o seu reticulado λ^ℤ — a
assinatura de III_λ. O que separa III₁ de III_λ é a MISTURA: duas razões
INCOMENSURÁVEIS geram um espectro de razões DENSO — a S-invariante de
Connes preenche a semirreta inteira. Esta pedra prova essa marca:

* ★★ `mixed_chain_ratio` — a cadeia MISTA (a blocos λ₁ ⊗ b blocos λ₂)
  carrega a testemunha de razão λ₁^a·λ₂^b — as duas escadas COMPÕEM;
* ★★★ `mixed_log_dense` — SE log λ₁/log λ₂ é irracional, o subgrupo
  aditivo gerado por {log λ₁, log λ₂} é DENSO em ℝ (dense_or_cyclic +
  a exclusão do cíclico) — o espectro de razões em escala log toca
  TODO ponto: A MARCA DE III₁ (vs o reticulado discreto de III_λ);
* ★★ `irrational_log_two_div_log_three` — λ₁ = 1/2 e λ₂ = 1/3 SÃO
  incomensuráveis (2^b = 3^a é impossível: paridade);
* ★★★ `the_mixing_mark` — A MARCA HABITADA: o par concreto (1/2, 1/3)
  gera espectro log-denso — III₁ tem testemunha finita de sua
  assinatura espectral no kernel.

O QUE RESTA (nomeado, sem véu): o FATOR — o limite indutivo fraco-*
da cadeia mista com o estado-produto (ITPFI; III₁ de Araki–Woods).
A assinatura espectral está provada; o objeto-limite é o programa.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Kronecker Matrix

noncomputable section

/-! ## A — a cadeia mista: as duas escadas compõem -/

/-- [KERNEL] ★★ A CADEIA MISTA: a blocos de razão λ₁ ⊗ b blocos de razão
    λ₂ carregam a testemunha de razão λ₁^(a+1)·λ₂^(b+1) — as escadas
    COMPÕEM por Kronecker. -/
theorem mixed_chain_ratio (l1 l2 : ℝ) (h1 : 0 < l1) (h2 : 0 < l2)
    (a b : ℕ) :
    RatioWitness (chainDensity l1 a ⊗ₖ chainDensity l2 b)
      (chainUp a ⊗ₖ chainUp b) (chainDown a ⊗ₖ chainDown b)
      (l1 ^ (a + 1) * l2 ^ (b + 1)) :=
  ratioWitness_kron (powers_ladder l1 h1 a) (powers_ladder l2 h2 b)

/-! ## B — a densidade: a marca de III₁ -/

/-- [KERNEL] ★★★ A MARCA DE III₁: razões incomensuráveis geram espectro
    log-DENSO em ℝ — a S-invariante toca todo ponto (vs o reticulado
    discreto λ^ℤ de III_λ). -/
theorem mixed_log_dense (l1 l2 : ℝ)
    (hirr : Irrational (Real.log l1 / Real.log l2))
    (hl2 : Real.log l2 ≠ 0) :
    Dense ((AddSubgroup.closure {Real.log l1, Real.log l2}
      : AddSubgroup ℝ) : Set ℝ) := by
  rcases AddSubgroup.dense_or_cyclic
      (AddSubgroup.closure {Real.log l1, Real.log l2}) with hd | ⟨a, ha⟩
  · exact hd
  · exfalso
    have m1 : Real.log l1 ∈ AddSubgroup.closure {Real.log l1, Real.log l2} :=
      AddSubgroup.subset_closure (Set.mem_insert _ _)
    have m2 : Real.log l2 ∈ AddSubgroup.closure {Real.log l1, Real.log l2} :=
      AddSubgroup.subset_closure (Set.mem_insert_of_mem _ rfl)
    rw [ha] at m1 m2
    obtain ⟨m, hm⟩ := AddSubgroup.mem_closure_singleton.mp m1
    obtain ⟨n, hn⟩ := AddSubgroup.mem_closure_singleton.mp m2
    have hn0 : (n : ℝ) ≠ 0 := by
      intro h0
      apply hl2
      rw [← hn, zsmul_eq_mul, h0, zero_mul]
    have ha0 : a ≠ 0 := by
      intro h0
      apply hl2
      rw [← hn, h0, smul_zero]
    apply hirr
    refine ⟨(m : ℚ) / (n : ℚ), ?_⟩
    rw [← hm, ← hn, zsmul_eq_mul, zsmul_eq_mul]
    push_cast
    rw [mul_div_mul_right _ _ ha0]

/-! ## C — o par concreto: 1/2 e 1/3 são incomensuráveis -/

/-- [KERNEL] ★★ log 2 / log 3 é IRRACIONAL (2^b = 3^a é impossível). -/
theorem irrational_log_two_div_log_three :
    Irrational (Real.log 2 / Real.log 3) := by
  intro ⟨q, hq⟩
  have hlog2 : (0 : ℝ) < Real.log 2 := Real.log_pos (by norm_num)
  have hlog3 : (0 : ℝ) < Real.log 3 := Real.log_pos (by norm_num)
  have hqpos : (0 : ℚ) < q := by
    have : (0 : ℝ) < (q : ℝ) := by
      rw [hq]
      positivity
    exact_mod_cast this
  set a : ℕ := q.num.toNat with hadef
  set b : ℕ := q.den with hbdef
  have hb1 : 1 ≤ b := q.pos
  have hnum : (q.num : ℝ) = (a : ℝ) := by
    rw [hadef]
    norm_cast
    exact (Int.toNat_of_nonneg (le_of_lt (Rat.num_pos.mpr hqpos))).symm
  have hcast : (q : ℝ) = (a : ℝ) / (b : ℝ) := by
    rw [Rat.cast_def, hnum, hbdef]
  have hbne : (b : ℝ) ≠ 0 := by positivity
  have hkey : (b : ℝ) * Real.log 2 = (a : ℝ) * Real.log 3 := by
    have h1 : Real.log 2 / Real.log 3 = (a : ℝ) / (b : ℝ) := by
      rw [← hq, hcast]
    field_simp at h1
    linarith [h1]
  have hlogs : Real.log ((2 : ℝ) ^ b) = Real.log ((3 : ℝ) ^ a) := by
    rw [Real.log_pow, Real.log_pow, hkey]
  have hreal : (2 : ℝ) ^ b = (3 : ℝ) ^ a := by
    have h2 : (0 : ℝ) < (2 : ℝ) ^ b := by positivity
    have h3 : (0 : ℝ) < (3 : ℝ) ^ a := by positivity
    calc (2 : ℝ) ^ b = Real.exp (Real.log ((2 : ℝ) ^ b)) :=
          (Real.exp_log h2).symm
      _ = Real.exp (Real.log ((3 : ℝ) ^ a)) := by rw [hlogs]
      _ = (3 : ℝ) ^ a := Real.exp_log h3
  have hnat : (2 : ℕ) ^ b = 3 ^ a := by
    have := hreal
    push_cast at this
    exact_mod_cast this
  have heven : 2 ∣ 2 ^ b := dvd_pow_self 2 (by omega)
  have hodd : ¬ 2 ∣ 3 ^ a := by
    intro hdvd
    have h3odd : Odd ((3 : ℕ) ^ a) := Odd.pow (by decide)
    rw [Nat.odd_iff] at h3odd
    omega
  rw [hnat] at heven
  exact hodd heven

/-- [KERNEL] ★★★ A MARCA HABITADA: o par (1/2, 1/3) gera espectro de
    razões log-DENSO — a assinatura de III₁ com testemunha concreta. -/
theorem the_mixing_mark :
    Dense ((AddSubgroup.closure
      {Real.log ((1 : ℝ) / 2), Real.log ((1 : ℝ) / 3)}
      : AddSubgroup ℝ) : Set ℝ) := by
  have h2 : Real.log ((1 : ℝ) / 2) = -Real.log 2 := by
    rw [one_div, Real.log_inv]
  have h3 : Real.log ((1 : ℝ) / 3) = -Real.log 3 := by
    rw [one_div, Real.log_inv]
  have hlog3 : (0 : ℝ) < Real.log 3 := Real.log_pos (by norm_num)
  apply mixed_log_dense
  · rw [h2, h3, neg_div_neg_eq]
    exact irrational_log_two_div_log_three
  · rw [h3]
    exact neg_ne_zero.mpr (ne_of_gt hlog3)

end

end TGLExt
