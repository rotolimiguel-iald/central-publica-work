import TGLExt.PPIndex

set_option autoImplicit false

/-!
# Os traços de Markov das duas torres   [TGLExt — Degrau 2, parte 2]

O traço normalizado `tr₁ = Tr_End/n²` de `End(H)`, `H = Mₙ(ℂ)`, computado
sobre os espelhos de Jones das duas inclusões da casa:

* `Tr_End(L_x·e_D) = Tr x` — peso de Markov da torre da MASA:
  `tr₁(L_x·e_D) = (1/n)·τ(x)`, e `τ₁(e_D) = 1/n = 1/Ind_PP` (COINCIDEM);
* `Tr_End(L_x·e_ℂ) = Tr x / n` — peso da torre escalar:
  `tr₁(L_x·e_ℂ) = (1/n²)·τ(x)`, e `τ₁(e_ℂ) = 1/n² = 1/‖Λ‖²`;
* O PAR HONESTO como teorema: para a MASA o índice de Pimsner–Popa e o
  peso da torre dão o MESMO n; para `ℂ ⊆ Mₙ` divergem (1/n ≠ 1/n² se
  n > 1) — o índice probabilístico e o índice da torre são objetos
  distintos em inclusões não-irredutíveis.

"O peso do espelho é o inverso do índice" (v27) — agora computado.
Tudo dimensão FINITA; β NÃO entra. Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-! ## Funcionais-coordenada e decomposições posto-um dos espelhos -/

/-- O funcional-coordenada diagonal `y ↦ y k k`. -/
def diagCoord (k : n) : Matrix n n ℂ →ₗ[ℂ] ℂ where
  toFun y := y k k
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

omit [Fintype n] [DecidableEq n] in
@[simp] theorem diagCoord_apply (k : n) (y : Matrix n n ℂ) :
    diagCoord k y = y k k := rfl

/-- O funcional do traço normalizado `y ↦ Tr y / n`. -/
def trCoord : Matrix n n ℂ →ₗ[ℂ] ℂ where
  toFun y := y.trace / (Fintype.card n : ℂ)
  map_add' a b := by simp [trace_add, add_div]
  map_smul' c a := by simp [trace_smul, smul_eq_mul, mul_div_assoc]

omit [DecidableEq n] in
@[simp] theorem trCoord_apply (y : Matrix n n ℂ) :
    trCoord y = y.trace / (Fintype.card n : ℂ) := rfl

omit [Fintype n] in
/-- `c • E_kk = single k k c` (a matriz-unidade absorve o escalar). -/
theorem smul_single_one (k : n) (c : ℂ) :
    c • Matrix.single k k (1 : ℂ) = Matrix.single k k c := by
  ext i j
  rw [Matrix.smul_apply, smul_eq_mul]
  by_cases hi : k = i
  · subst hi
    by_cases hj : k = j
    · subst hj
      rw [Matrix.single_apply_same, Matrix.single_apply_same, mul_one]
    · rw [Matrix.single_apply_of_col_ne _ _ hj, Matrix.single_apply_of_col_ne _ _ hj,
        mul_zero]
  · rw [Matrix.single_apply_of_row_ne hi, Matrix.single_apply_of_row_ne hi, mul_zero]

/-- A diagonal como soma de matrizes-unidade: `diagonal d = Σₖ single k k (d k)`. -/
theorem diagonal_eq_sum_single (d : n → ℂ) :
    diagonal d = ∑ k, Matrix.single k k (d k) := by
  ext i j
  rw [Matrix.sum_apply]
  by_cases h : i = j
  · subst h
    rw [Matrix.diagonal_apply_eq,
      Finset.sum_eq_single i
        (fun m _ hm => Matrix.single_apply_of_row_ne hm _ _ _)
        (fun hmem => absurd (Finset.mem_univ i) hmem),
      Matrix.single_apply_same]
  · rw [Matrix.diagonal_apply_ne _ h]
    refine (Finset.sum_eq_zero fun m _ => ?_).symm
    by_cases hm : m = i
    · subst hm
      exact Matrix.single_apply_of_col_ne _ _ h _
    · exact Matrix.single_apply_of_row_ne hm _ _ _

/-- A entrada diagonal da compressão pela matriz-unidade: `(x·E_kk) k k = x k k`. -/
theorem mul_single_diag (x : Matrix n n ℂ) (k : n) :
    Matrix.diag (x * Matrix.single k k (1 : ℂ)) k = x k k := by
  rw [Matrix.diag_apply, Matrix.mul_apply,
    Finset.sum_eq_single k
      (fun m _ hm => by rw [Matrix.single_apply_of_row_ne (Ne.symm hm), mul_zero])
      (fun hmem => absurd (Finset.mem_univ k) hmem),
    Matrix.single_apply_same, mul_one]

/-- [KERNEL] O espelho diagonal é soma de posto-uns: `e_D = Σₖ ⟨δₖ,·⟩·E_kk`. -/
theorem eD_eq_sum_smulRight :
    (eD : Module.End ℂ (Matrix n n ℂ))
      = ∑ k : n, (diagCoord k).smulRight (Matrix.single k k 1) := by
  refine LinearMap.ext fun y => ?_
  rw [LinearMap.sum_apply, eD_apply]
  show diagonal y.diag = _
  rw [diagonal_eq_sum_single]
  refine Finset.sum_congr rfl fun k _ => ?_
  rw [LinearMap.smulRight_apply, diagCoord_apply, smul_single_one, Matrix.diag_apply]

/-- [KERNEL] O espelho escalar é posto-um: `e_ℂ = ⟨Tr/n,·⟩·1`. -/
theorem eTr_eq_smulRight :
    (eTr : Module.End ℂ (Matrix n n ℂ)) = trCoord.smulRight 1 := by
  refine LinearMap.ext fun y => ?_
  rw [LinearMap.smulRight_apply, trCoord_apply, eTr_apply]
  rfl

/-! ## Os traços dos espelhos comprimidos -/

/-- [KERNEL] `Tr_End(L_x·e_D) = Tr x` — o traço da torre da MASA. -/
theorem trace_Lmul_eD (x : Matrix n n ℂ) :
    LinearMap.trace ℂ (Matrix n n ℂ) (Lmul x * eD) = x.trace := by
  have hdec : (Lmul x * eD : Module.End ℂ (Matrix n n ℂ))
      = ∑ k : n, (diagCoord k).smulRight (x * Matrix.single k k 1) := by
    rw [eD_eq_sum_smulRight, Finset.mul_sum]
    refine Finset.sum_congr rfl fun k _ => LinearMap.ext fun y => ?_
    rw [Module.End.mul_apply, LinearMap.smulRight_apply, LinearMap.smulRight_apply,
      diagCoord_apply, Lmul_apply, Matrix.mul_smul]
  rw [hdec, map_sum, Matrix.trace]
  refine Finset.sum_congr rfl fun k _ => ?_
  rw [LinearMap.trace_smulRight, diagCoord_apply]
  exact mul_single_diag x k

/-- [KERNEL] `Tr_End(L_x·e_ℂ) = Tr x / n` — o traço da torre escalar. -/
theorem trace_Lmul_eTr (x : Matrix n n ℂ) :
    LinearMap.trace ℂ (Matrix n n ℂ) (Lmul x * eTr)
      = x.trace / (Fintype.card n : ℂ) := by
  have hdec : (Lmul x * eTr : Module.End ℂ (Matrix n n ℂ))
      = trCoord.smulRight x := by
    rw [eTr_eq_smulRight]
    refine LinearMap.ext fun y => ?_
    rw [Module.End.mul_apply, LinearMap.smulRight_apply, LinearMap.smulRight_apply,
      Lmul_apply, Matrix.mul_smul, mul_one]
  rw [hdec, LinearMap.trace_smulRight, trCoord_apply]

theorem Lmul_one_eq_one :
    (Lmul (1 : Matrix n n ℂ)) = (1 : Module.End ℂ (Matrix n n ℂ)) := by
  rw [Lmul, LinearMap.mulLeft_one]; rfl

/-- [KERNEL] `Tr_End(e_D) = n` (o posto do espelho diagonal). -/
theorem trace_eD :
    LinearMap.trace ℂ (Matrix n n ℂ) (eD (n := n)) = (Fintype.card n : ℂ) := by
  have h := trace_Lmul_eD (1 : Matrix n n ℂ)
  rwa [Lmul_one_eq_one, one_mul, Matrix.trace_one] at h

/-- [KERNEL] `Tr_End(e_ℂ) = 1` (o espelho escalar é posto-um). -/
theorem trace_eTr [Nonempty n] :
    LinearMap.trace ℂ (Matrix n n ℂ) (eTr (n := n)) = 1 := by
  have h := trace_Lmul_eTr (1 : Matrix n n ℂ)
  rw [Lmul_one_eq_one, one_mul, Matrix.trace_one] at h
  rw [h, div_self]
  exact Nat.cast_ne_zero.mpr Fintype.card_ne_zero

omit [DecidableEq n] in
/-- [KERNEL] `Tr_End(1) = n²` — a dimensão do palco. -/
theorem trace_end_one :
    LinearMap.trace ℂ (Matrix n n ℂ) (1 : Module.End ℂ (Matrix n n ℂ))
      = ((Fintype.card n : ℂ))^2 := by
  rw [LinearMap.trace_one, Module.finrank_matrix, Module.finrank_self]
  push_cast
  ring

/-! ## Os pesos de Markov normalizados -/

/-- O traço normalizado de `End(H)`: `tr₁ = Tr_End/n²` (com `tr₁(1)=1`). -/
def trOne (f : Module.End ℂ (Matrix n n ℂ)) : ℂ :=
  LinearMap.trace ℂ (Matrix n n ℂ) f / (Fintype.card n : ℂ)^2

/-- [KERNEL] PESO DE MARKOV DA MASA: `tr₁(L_x·e_D) = (1/n)·τ(x)` —
    o módulo da torre é `1/n` = `1/Ind_PP` (os dois índices COINCIDEM). -/
theorem markov_weight_eD [Nonempty n] (x : Matrix n n ℂ) :
    trOne (Lmul x * eD)
      = (1 / (Fintype.card n : ℂ)) * (x.trace / (Fintype.card n : ℂ)) := by
  have hc : (Fintype.card n : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr Fintype.card_ne_zero
  rw [trOne, trace_Lmul_eD]
  field_simp

/-- [KERNEL] PESO DE MARKOV ESCALAR: `tr₁(L_x·e_ℂ) = (1/n²)·τ(x)` —
    o módulo da torre escalar é `1/n² = 1/‖Λ‖²`. -/
theorem markov_weight_eTr [Nonempty n] (x : Matrix n n ℂ) :
    trOne (Lmul x * eTr)
      = (1 / (Fintype.card n : ℂ)^2) * (x.trace / (Fintype.card n : ℂ)) := by
  have hc : (Fintype.card n : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr Fintype.card_ne_zero
  rw [trOne, trace_Lmul_eTr]
  field_simp

/-- [KERNEL] `τ₁(e_D) = 1/n` — o peso do espelho é o inverso do índice (v27). -/
theorem tau_eD [Nonempty n] : trOne (eD (n := n)) = 1 / (Fintype.card n : ℂ) := by
  have hc : (Fintype.card n : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr Fintype.card_ne_zero
  rw [trOne, trace_eD]
  field_simp

/-- [KERNEL] `τ₁(e_ℂ) = 1/n²` — o peso do espelho escalar é `1/‖Λ‖²`. -/
theorem tau_eTr [Nonempty n] : trOne (eTr (n := n)) = 1 / (Fintype.card n : ℂ)^2 := by
  rw [trOne, trace_eTr, one_div]

/-! ## O par honesto: PP vs torre -/

/-- [KERNEL] Para a MASA os DOIS índices COINCIDEM: o peso da torre é
    exatamente `ppBestDiag = 1/n`. -/
theorem masa_tower_weight_eq_ppBest [Nonempty n] :
    trOne (eD (n := n)) = ((ppBestDiag (n := n) : ℝ) : ℂ) := by
  rw [tau_eD, ppBestDiag_eq_one_div_card]
  push_cast
  ring

omit [DecidableEq n] in
/-- [KERNEL] Para `ℂ ⊆ Mₙ` (n>1) os índices DIVERGEM: `1/n ≠ 1/n²` — o
    índice probabilístico (PP) e o índice da torre são objetos DISTINTOS
    em inclusões não-irredutíveis. Documentado como TEOREMA, não nota. -/
theorem pp_ne_tower_for_scalars (h : 1 < Fintype.card n) :
    (1 : ℝ) / (Fintype.card n : ℝ) ≠ 1 / (Fintype.card n : ℝ)^2 := by
  have hc : (0 : ℝ) < (Fintype.card n : ℝ) := by
    exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one h.le
  have hc1 : (1 : ℝ) < (Fintype.card n : ℝ) := by exact_mod_cast h
  intro heq
  rw [div_eq_div_iff hc.ne' (by positivity)] at heq
  nlinarith [heq]

end

end TGLExt
