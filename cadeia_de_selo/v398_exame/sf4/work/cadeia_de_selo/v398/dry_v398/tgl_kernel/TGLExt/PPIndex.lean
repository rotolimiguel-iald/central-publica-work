import TGLExt.CondExpect

set_option autoImplicit false

/-!
# O índice de Pimsner–Popa de `Mₙ(ℂ)`   [TGLExt — Degrau 2]

A COTA DE PIMSNER–POPA para as duas esperanças condicionais canônicas de
`Mₙ(ℂ)` (`trExpect`, sobre os escalares; `diagExpect`, sobre a MASA
diagonal), com otimalidade e o ÍNDICE COMPUTADO:

* (P1) DOMINÂNCIA DO TRAÇO: `x ⪰ 0 ⟹ (Tr x)·1 − x ⪰ 0` — nenhum estado
  excede seu peso total (decomposição rank-um + Cauchy–Schwarz);
* (P2) COTA DA MASA: `x ⪰ 0 ⟹ n·E_D(x) − x ⪰ 0` — Cauchy–Schwarz com
  peso `n` (`sq_sum_le_card_mul_sum_sq`);
* (P3) OTIMALIDADE: para todo `c > 1/n` existe testemunha psd que refuta a
  cota — para `E_ℂ` a matriz unidade `E_{i₀i₀}`, para `E_D` a matriz de
  uns `J = vecMulVec 1 1`;
* (P4) `IsGreatest {c | IsPPBound E c} (1/n)` para ambas as esperanças,
  `ppBest = 1/n` via `IsGreatest.csSup_eq`, e o índice
  `ppIndex = 1/ppBest = n` — o índice de Pimsner–Popa das inclusões
  `ℂ ⊆ Mₙ(ℂ)` e `D ⊆ Mₙ(ℂ)` em dimensão finita.

Espelha `TGL.NameIndex` do kernel da casa (`ppBest = sSup`,
`ppIndex = 1/ppBest`, otimalidade por `IsGreatest`) em versão concreta
matricial, sem acoplar os projetos Lake. β NÃO entra: infraestrutura pura.
Sem sorry, sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix
open scoped ComplexOrder

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-! ## Auxiliares: valores quadráticos e Cauchy–Schwarz real -/

omit [DecidableEq n] in
/-- `⟨y,y⟩ = Σᵢ |yᵢ|²` como coerção real. -/
theorem star_dotProduct_self (y : n → ℂ) :
    star y ⬝ᵥ y = ((∑ i, Complex.normSq (y i) : ℝ) : ℂ) := by
  push_cast
  simp only [dotProduct, Pi.star_apply, Complex.star_def]
  exact Finset.sum_congr rfl fun i _ => Complex.normSq_eq_conj_mul_self.symm

omit [DecidableEq n] in
/-- A conjugação troca a ordem do produto escalar: `⟨w,y⟩ = ⟨y,w⟩*`. -/
theorem star_dotProduct_rev (w y : n → ℂ) :
    star w ⬝ᵥ y = star (star y ⬝ᵥ w) := by
  simp only [dotProduct, star_sum, star_mul, star_star, Pi.star_apply]

omit [DecidableEq n] in
/-- [KERNEL] O valor quadrático do projetor rank-um: `⟨y, w w⋆ y⟩ = |⟨y,w⟩|²`. -/
theorem star_dotProduct_vecMulVec_mulVec (w y : n → ℂ) :
    star y ⬝ᵥ (vecMulVec w (star w) *ᵥ y)
      = ((Complex.normSq (star y ⬝ᵥ w) : ℝ) : ℂ) := by
  rw [vecMulVec_mulVec, op_smul_eq_smul, dotProduct_smul, smul_eq_mul,
    star_dotProduct_rev, Complex.star_def, ← Complex.normSq_eq_conj_mul_self]

/-- O valor quadrático da parte diagonal de `w w⋆`. -/
theorem star_dotProduct_diagonal_normSq_mulVec (w y : n → ℂ) :
    star y ⬝ᵥ (diagonal (fun i => ((Complex.normSq (w i) : ℝ) : ℂ)) *ᵥ y)
      = ((∑ i, Complex.normSq (w i) * Complex.normSq (y i) : ℝ) : ℂ) := by
  push_cast
  simp only [dotProduct, mulVec_diagonal, Pi.star_apply, Complex.star_def]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [mul_comm ((starRingEnd ℂ) (y i)), mul_assoc, Complex.mul_conj]

omit [DecidableEq n] in
/-- A desigualdade triangular do produto escalar, termo a termo. -/
theorem norm_star_dotProduct_le (y w : n → ℂ) :
    ‖star y ⬝ᵥ w‖ ≤ ∑ i, ‖w i‖ * ‖y i‖ := by
  simp only [dotProduct, Pi.star_apply]
  refine (norm_sum_le _ _).trans (le_of_eq (Finset.sum_congr rfl fun i _ => ?_))
  rw [norm_mul, norm_star, mul_comm]

omit [DecidableEq n] in
/-- [KERNEL] CAUCHY–SCHWARZ: `|⟨y,w⟩|² ≤ ‖w‖²·‖y‖²` (forma real, por somas). -/
theorem normSq_star_dotProduct_le (y w : n → ℂ) :
    Complex.normSq (star y ⬝ᵥ w)
      ≤ (∑ i, Complex.normSq (w i)) * ∑ i, Complex.normSq (y i) := by
  have h1 := norm_star_dotProduct_le y w
  have h2 := Finset.sum_mul_sq_le_sq_mul_sq Finset.univ
    (fun i => ‖w i‖) (fun i => ‖y i‖)
  have h3 : ‖star y ⬝ᵥ w‖ ^ 2 ≤ (∑ i, ‖w i‖ * ‖y i‖) ^ 2 :=
    pow_le_pow_left₀ (norm_nonneg _) h1 2
  calc Complex.normSq (star y ⬝ᵥ w)
      = ‖star y ⬝ᵥ w‖ ^ 2 := Complex.normSq_eq_norm_sq _
    _ ≤ (∑ i, ‖w i‖ * ‖y i‖) ^ 2 := h3
    _ ≤ (∑ i, ‖w i‖ ^ 2) * ∑ i, ‖y i‖ ^ 2 := h2
    _ = (∑ i, Complex.normSq (w i)) * ∑ i, Complex.normSq (y i) := by
        simp only [Complex.normSq_eq_norm_sq]

omit [DecidableEq n] in
/-- [KERNEL] CAUCHY–SCHWARZ com peso `n` — a forma exata da cota da MASA:
    `|⟨y,w⟩|² ≤ n·Σᵢ |wᵢ|²|yᵢ|²`. -/
theorem normSq_star_dotProduct_le_card (y w : n → ℂ) :
    Complex.normSq (star y ⬝ᵥ w)
      ≤ (Fintype.card n : ℝ) * ∑ i, Complex.normSq (w i) * Complex.normSq (y i) := by
  have h1 := norm_star_dotProduct_le y w
  have h2 : (∑ i, ‖w i‖ * ‖y i‖) ^ 2
      ≤ (Fintype.card n : ℝ) * ∑ i, (‖w i‖ * ‖y i‖) ^ 2 := by
    simpa using sq_sum_le_card_mul_sum_sq
      (s := (Finset.univ : Finset n)) (f := fun i => ‖w i‖ * ‖y i‖)
  have h3 : ‖star y ⬝ᵥ w‖ ^ 2 ≤ (∑ i, ‖w i‖ * ‖y i‖) ^ 2 :=
    pow_le_pow_left₀ (norm_nonneg _) h1 2
  calc Complex.normSq (star y ⬝ᵥ w)
      = ‖star y ⬝ᵥ w‖ ^ 2 := Complex.normSq_eq_norm_sq _
    _ ≤ (∑ i, ‖w i‖ * ‖y i‖) ^ 2 := h3
    _ ≤ (Fintype.card n : ℝ) * ∑ i, (‖w i‖ * ‖y i‖) ^ 2 := h2
    _ = (Fintype.card n : ℝ) * ∑ i, Complex.normSq (w i) * Complex.normSq (y i) := by
        simp only [mul_pow, Complex.normSq_eq_norm_sq]

/-! ## P1: dominância do traço -/

/-- [KERNEL] Caso rank-um de P1: `(Tr w w⋆)·1 − w w⋆ ⪰ 0` (Cauchy–Schwarz). -/
theorem trace_smul_one_sub_vecMulVec_posSemidef (w : n → ℂ) :
    ((vecMulVec w (star w)).trace • (1 : Matrix n n ℂ)
      - vecMulVec w (star w)).PosSemidef := by
  have htr : (vecMulVec w (star w)).trace
      = ((∑ i, Complex.normSq (w i) : ℝ) : ℂ) := by
    rw [trace_vecMulVec]
    push_cast
    simp only [dotProduct, Pi.star_apply, Complex.star_def, Complex.mul_conj]
  rw [htr]
  refine PosSemidef.of_dotProduct_mulVec_nonneg ?_ fun y => ?_
  · have hsc : (0 : ℂ) ≤ ((∑ i, Complex.normSq (w i) : ℝ) : ℂ) := by
      rw [Complex.zero_le_real]
      exact Finset.sum_nonneg fun i _ => Complex.normSq_nonneg _
    exact (Matrix.PosSemidef.one.smul hsc).1.sub
      (posSemidef_vecMulVec_self_star w).1
  · rw [sub_mulVec, dotProduct_sub, smul_mulVec, one_mulVec, dotProduct_smul,
      smul_eq_mul, star_dotProduct_self, star_dotProduct_vecMulVec_mulVec]
    have h0 : (0 : ℝ) ≤ (∑ i, Complex.normSq (w i)) * (∑ i, Complex.normSq (y i))
        - Complex.normSq (star y ⬝ᵥ w) :=
      sub_nonneg.mpr (normSq_star_dotProduct_le y w)
    exact_mod_cast h0

/-- [KERNEL] P1 — DOMINÂNCIA DO TRAÇO: `x ⪰ 0 ⟹ (Tr x)·1 − x ⪰ 0`. Na ordem
    de Loewner lê-se `x ≤ (Tr x)·1`: os autovalores de um psd somam ao traço,
    logo nenhum deles o excede. Rota rank-um: `x = Σ vₖvₖ⋆` + Cauchy–Schwarz
    termo a termo. -/
theorem trace_smul_one_sub_posSemidef {x : Matrix n n ℂ} (hx : x.PosSemidef) :
    (x.trace • (1 : Matrix n n ℂ) - x).PosSemidef := by
  obtain ⟨m, v, rfl⟩ := posSemidef_iff_eq_sum_vecMulVec.mp hx
  rw [trace_sum, Finset.sum_smul, ← Finset.sum_sub_distrib]
  exact posSemidef_sum _ fun k _ => trace_smul_one_sub_vecMulVec_posSemidef (v k)

/-! ## P2: a cota de Pimsner–Popa da MASA diagonal -/

/-- [KERNEL] Caso rank-um de P2: `n·E_D(w w⋆) − w w⋆ ⪰ 0` — Cauchy–Schwarz
    com peso `n` na diagonal. -/
theorem card_smul_diagExpect_sub_vecMulVec_posSemidef (w : n → ℂ) :
    ((Fintype.card n : ℂ) • diagExpect (vecMulVec w (star w))
      - vecMulVec w (star w)).PosSemidef := by
  have hdiag : diagExpect (vecMulVec w (star w))
      = diagonal (fun i => ((Complex.normSq (w i) : ℝ) : ℂ)) := by
    have hfun : (vecMulVec w (star w)).diag
        = fun i => ((Complex.normSq (w i) : ℝ) : ℂ) := by
      funext i
      simp only [diag_vecMulVec, Pi.mul_apply, Pi.star_apply, Complex.star_def,
        Complex.mul_conj]
    simp only [diagExpect, hfun]
  rw [hdiag]
  refine PosSemidef.of_dotProduct_mulVec_nonneg ?_ fun y => ?_
  · have hdpsd : (diagonal (fun i => ((Complex.normSq (w i) : ℝ) : ℂ))).PosSemidef :=
      posSemidef_diagonal_iff.mpr fun i => by
        show (0 : ℂ) ≤ ((Complex.normSq (w i) : ℝ) : ℂ)
        rw [Complex.zero_le_real]
        exact Complex.normSq_nonneg _
    have hcard : (0 : ℂ) ≤ (Fintype.card n : ℂ) := by
      exact_mod_cast Nat.zero_le (Fintype.card n)
    exact (hdpsd.smul hcard).1.sub (posSemidef_vecMulVec_self_star w).1
  · rw [sub_mulVec, dotProduct_sub, smul_mulVec, dotProduct_smul, smul_eq_mul,
      star_dotProduct_diagonal_normSq_mulVec, star_dotProduct_vecMulVec_mulVec]
    have h0 : (0 : ℝ) ≤ (Fintype.card n : ℝ)
          * (∑ i, Complex.normSq (w i) * Complex.normSq (y i))
        - Complex.normSq (star y ⬝ᵥ w) :=
      sub_nonneg.mpr (normSq_star_dotProduct_le_card y w)
    exact_mod_cast h0

/-- [KERNEL] P2 — A COTA DE PIMSNER–POPA DA MASA: `x ⪰ 0 ⟹ n·E_D(x) − x ⪰ 0`.
    A esperança diagonal comprime no máximo por um fator `n`: é a
    desigualdade `E(x) ≥ λ·x` com `λ = 1/n`, a assinatura métrica da
    inclusão `D ⊆ Mₙ(ℂ)`. -/
theorem card_smul_diagExpect_sub_posSemidef {x : Matrix n n ℂ} (hx : x.PosSemidef) :
    ((Fintype.card n : ℂ) • diagExpect x - x).PosSemidef := by
  obtain ⟨m, v, rfl⟩ := posSemidef_iff_eq_sum_vecMulVec.mp hx
  have hsplit : diagExpect (∑ k, vecMulVec (v k) (star (v k)))
      = ∑ k, diagExpect (vecMulVec (v k) (star (v k))) := by
    have h := map_sum (eD (n := n)) (fun k => vecMulVec (v k) (star (v k)))
      Finset.univ
    simp only [eD_apply] at h
    exact h
  rw [hsplit, Finset.smul_sum, ← Finset.sum_sub_distrib]
  exact posSemidef_sum _ fun k _ =>
    card_smul_diagExpect_sub_vecMulVec_posSemidef (v k)

/-! ## P3: otimalidade — testemunhas que refutam qualquer `c > 1/n` -/

/-- [KERNEL] OTIMALIDADE para `E_ℂ`: se `c > 1/n`, a matriz unidade
    `E_{i₀i₀}` é psd mas `E_ℂ(E_{i₀i₀}) − c·E_{i₀i₀}` NÃO é — o valor
    quadrático no vetor `e_{i₀}` é `1/n − c < 0`. -/
theorem exists_witness_trExpect [Nonempty n] {c : ℝ}
    (hc : 1 / (Fintype.card n : ℝ) < c) :
    ∃ w : Matrix n n ℂ, w.PosSemidef ∧ ¬(trExpect w - (c : ℂ) • w).PosSemidef := by
  have i0 : n := Classical.arbitrary n
  have hstar : star (Pi.single i0 1 : n → ℂ) = (Pi.single i0 1 : n → ℂ) := by
    rw [Pi.star_single, star_one]
  refine ⟨Matrix.single i0 i0 1, ?_, fun hpsd => ?_⟩
  · rw [single_eq_single_vecMulVec_single]
    nth_rw 2 [← hstar]
    exact posSemidef_vecMulVec_self_star _
  · have hval := hpsd.dotProduct_mulVec_nonneg (Pi.single i0 (1 : ℂ))
    have hw : Matrix.single i0 i0 (1 : ℂ) *ᵥ Pi.single i0 (1 : ℂ)
        = Pi.single i0 (1 : ℂ) := by
      rw [single_mulVec_eq]
      simp
    have htrE : trExpect (Matrix.single i0 i0 (1 : ℂ))
        = ((1 : ℂ) / (Fintype.card n : ℂ)) • (1 : Matrix n n ℂ) := by
      simp only [trExpect, trace_single_eq_same]
    have hcompute : star (Pi.single i0 (1 : ℂ)) ⬝ᵥ
        ((trExpect (Matrix.single i0 i0 1) - (c : ℂ) • Matrix.single i0 i0 1)
          *ᵥ Pi.single i0 (1 : ℂ))
        = ((1 / (Fintype.card n : ℝ) - c : ℝ) : ℂ) := by
      rw [hstar, htrE, sub_mulVec, smul_mulVec, smul_mulVec, one_mulVec, hw,
        dotProduct_sub, dotProduct_smul, dotProduct_smul, smul_eq_mul,
        smul_eq_mul, dotProduct_single, Pi.single_eq_same]
      push_cast
      ring
    rw [hcompute, Complex.zero_le_real] at hval
    linarith

/-- [KERNEL] OTIMALIDADE para `E_D`: se `c > 1/n`, a matriz de uns
    `J = vecMulVec 1 1` é psd mas `E_D(J) − c·J` NÃO é — o valor quadrático
    no vetor constante `1` é `n·(1 − c·n) < 0`. -/
theorem exists_witness_diagExpect [Nonempty n] {c : ℝ}
    (hc : 1 / (Fintype.card n : ℝ) < c) :
    ∃ w : Matrix n n ℂ, w.PosSemidef ∧ ¬(diagExpect w - (c : ℂ) • w).PosSemidef := by
  have hstar1 : star (1 : n → ℂ) = 1 := star_one _
  refine ⟨vecMulVec 1 1, ?_, fun hpsd => ?_⟩
  · nth_rw 2 [← hstar1]
    exact posSemidef_vecMulVec_self_star _
  · have hval := hpsd.dotProduct_mulVec_nonneg (1 : n → ℂ)
    have hd : diagExpect (vecMulVec (1 : n → ℂ) 1) = 1 := by
      have hfun : (vecMulVec (1 : n → ℂ) 1).diag = 1 := by
        funext i
        simp only [diag_vecMulVec, Pi.mul_apply, Pi.one_apply, mul_one]
      simp only [diagExpect, hfun, diagonal_one']
    have hJ : vecMulVec (1 : n → ℂ) 1 *ᵥ (1 : n → ℂ)
        = (Fintype.card n : ℂ) • 1 := by
      rw [vecMulVec_mulVec, op_smul_eq_smul, one_dotProduct_one]
    have hcompute : star (1 : n → ℂ) ⬝ᵥ
        ((diagExpect (vecMulVec 1 1) - (c : ℂ) • vecMulVec 1 1) *ᵥ (1 : n → ℂ))
        = (((Fintype.card n : ℝ) * (1 - c * (Fintype.card n : ℝ)) : ℝ) : ℂ) := by
      rw [hstar1, hd, sub_mulVec, smul_mulVec, hJ, one_mulVec, dotProduct_sub,
        dotProduct_smul, dotProduct_smul, one_dotProduct_one, smul_eq_mul,
        smul_eq_mul]
      push_cast
      ring
    rw [hcompute, Complex.zero_le_real] at hval
    have hcard : (0 : ℝ) < (Fintype.card n : ℝ) := by
      exact_mod_cast Fintype.card_pos
    have h1 : (1 : ℝ) < c * (Fintype.card n : ℝ) := (div_lt_iff₀ hcard).mp hc
    have hneg : (Fintype.card n : ℝ) * (1 - c * (Fintype.card n : ℝ)) < 0 :=
      mul_neg_of_pos_of_neg hcard (by linarith)
    linarith

/-! ## P4: `IsGreatest`, `ppBest` e o índice computado -/

/-- [KERNEL] `c` é COTA DE PIMSNER–POPA de `E` quando `E(x) − c·x ⪰ 0` para
    todo `x ⪰ 0` — a desigualdade `E(x) ≥ c·x` de Pimsner–Popa, em versão
    concreta matricial (espelha `IsPPLowerBound` do kernel da casa). -/
def IsPPBound (E : Matrix n n ℂ → Matrix n n ℂ) (c : ℝ) : Prop :=
  ∀ x : Matrix n n ℂ, x.PosSemidef → (E x - (c : ℂ) • x).PosSemidef

/-- [KERNEL] `1/n` é cota de Pimsner–Popa de `E_ℂ` (P1 reescalado). -/
theorem isPPBound_trExpect [Nonempty n] :
    IsPPBound (trExpect (n := n)) (1 / (Fintype.card n : ℝ)) := by
  intro x hx
  have key : trExpect x - (((1 / (Fintype.card n : ℝ)) : ℝ) : ℂ) • x
      = (((1 / (Fintype.card n : ℝ)) : ℝ) : ℂ)
          • (x.trace • (1 : Matrix n n ℂ) - x) := by
    have hsc : (((1 / (Fintype.card n : ℝ)) : ℝ) : ℂ)
        = 1 / (Fintype.card n : ℂ) := by
      push_cast
      ring
    rw [hsc]
    simp only [trExpect, smul_sub, smul_smul]
    rw [show x.trace / (Fintype.card n : ℂ)
        = 1 / (Fintype.card n : ℂ) * x.trace by ring]
  rw [key]
  refine (trace_smul_one_sub_posSemidef hx).smul ?_
  rw [Complex.zero_le_real]
  positivity

/-- [KERNEL] `1/n` é cota de Pimsner–Popa de `E_D` (P2 reescalado). -/
theorem isPPBound_diagExpect [Nonempty n] :
    IsPPBound (diagExpect (n := n)) (1 / (Fintype.card n : ℝ)) := by
  intro x hx
  have hcard0 : ((Fintype.card n : ℂ)) ≠ 0 :=
    Nat.cast_ne_zero.mpr Fintype.card_ne_zero
  have key : diagExpect x - (((1 / (Fintype.card n : ℝ)) : ℝ) : ℂ) • x
      = (((1 / (Fintype.card n : ℝ)) : ℝ) : ℂ)
          • ((Fintype.card n : ℂ) • diagExpect x - x) := by
    have hsc : (((1 / (Fintype.card n : ℝ)) : ℝ) : ℂ)
        = 1 / (Fintype.card n : ℂ) := by
      push_cast
      ring
    rw [hsc, smul_sub, smul_smul, one_div, inv_mul_cancel₀ hcard0, one_smul]
  rw [key]
  refine (card_smul_diagExpect_sub_posSemidef hx).smul ?_
  rw [Complex.zero_le_real]
  positivity

/-- Nenhuma cota de `E_ℂ` excede `1/n` (contrapositiva de P3). -/
theorem le_of_isPPBound_trExpect [Nonempty n] {c : ℝ}
    (hc : IsPPBound (trExpect (n := n)) c) : c ≤ 1 / (Fintype.card n : ℝ) := by
  by_contra hlt
  rw [not_le] at hlt
  obtain ⟨w, hw, hnot⟩ := exists_witness_trExpect hlt
  exact hnot (hc w hw)

/-- Nenhuma cota de `E_D` excede `1/n` (contrapositiva de P3). -/
theorem le_of_isPPBound_diagExpect [Nonempty n] {c : ℝ}
    (hc : IsPPBound (diagExpect (n := n)) c) : c ≤ 1 / (Fintype.card n : ℝ) := by
  by_contra hlt
  rw [not_le] at hlt
  obtain ⟨w, hw, hnot⟩ := exists_witness_diagExpect hlt
  exact hnot (hc w hw)

/-- [KERNEL] `1/n` é a MAIOR cota de Pimsner–Popa de `E_ℂ`. -/
theorem isGreatest_ppBound_trExpect [Nonempty n] :
    IsGreatest {c : ℝ | IsPPBound (trExpect (n := n)) c}
      (1 / (Fintype.card n : ℝ)) :=
  ⟨isPPBound_trExpect, fun _ hc => le_of_isPPBound_trExpect hc⟩

/-- [KERNEL] `1/n` é a MAIOR cota de Pimsner–Popa de `E_D`. -/
theorem isGreatest_ppBound_diagExpect [Nonempty n] :
    IsGreatest {c : ℝ | IsPPBound (diagExpect (n := n)) c}
      (1 / (Fintype.card n : ℝ)) :=
  ⟨isPPBound_diagExpect, fun _ hc => le_of_isPPBound_diagExpect hc⟩

variable (n) in
/-- A MELHOR COTA de Pimsner–Popa de `E_ℂ` (espelha `ppBest` do kernel:
    supremo do conjunto das cotas). -/
def ppBestTr : ℝ := sSup {c : ℝ | IsPPBound (trExpect (n := n)) c}

variable (n) in
/-- A MELHOR COTA de Pimsner–Popa de `E_D`. -/
def ppBestDiag : ℝ := sSup {c : ℝ | IsPPBound (diagExpect (n := n)) c}

/-- [KERNEL] `ppBestTr = 1/n` — via `IsGreatest.csSup_eq`. -/
theorem ppBestTr_eq_one_div_card [Nonempty n] :
    ppBestTr n = 1 / (Fintype.card n : ℝ) :=
  isGreatest_ppBound_trExpect.csSup_eq

/-- [KERNEL] `ppBestDiag = 1/n` — via `IsGreatest.csSup_eq`. -/
theorem ppBestDiag_eq_one_div_card [Nonempty n] :
    ppBestDiag n = 1 / (Fintype.card n : ℝ) :=
  isGreatest_ppBound_diagExpect.csSup_eq

variable (n) in
/-- O ÍNDICE de Pimsner–Popa de `E_ℂ`: `1/ppBest` (espelha `ppIndex` do
    kernel). -/
def ppIndexTr : ℝ := 1 / ppBestTr n

variable (n) in
/-- O ÍNDICE de Pimsner–Popa de `E_D`: `1/ppBest`. -/
def ppIndexDiag : ℝ := 1 / ppBestDiag n

/-- [KERNEL] O ÍNDICE COMPUTADO: `[Mₙ(ℂ) : ℂ]_PP = 1/ppBestTr = n`. -/
theorem ppIndexTr_eq_card [Nonempty n] : ppIndexTr n = (Fintype.card n : ℝ) := by
  unfold ppIndexTr
  rw [ppBestTr_eq_one_div_card, one_div_one_div]

/-- [KERNEL] O ÍNDICE COMPUTADO: `[Mₙ(ℂ) : D]_PP = 1/ppBestDiag = n` — o
    índice da MASA diagonal é a dimensão, o mesmo valor da inclusão escalar:
    duas leituras do mesmo `n`. -/
theorem ppIndexDiag_eq_card [Nonempty n] :
    ppIndexDiag n = (Fintype.card n : ℝ) := by
  unfold ppIndexDiag
  rw [ppBestDiag_eq_one_div_card, one_div_one_div]

end

end TGLExt
