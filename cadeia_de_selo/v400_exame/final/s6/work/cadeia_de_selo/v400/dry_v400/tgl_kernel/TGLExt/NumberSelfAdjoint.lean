import TGLExt.NumberOperator

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 2000000

/-!
# star(N) = N: A PAREDE ATRAVESSADA
  [TGLExt — v105, o incremento 24 do programa SemifiniteAnalysis]

A mathlib NÃO tem auto-adjunção essencial nem exemplo concreto de
operador ilimitado auto-adjunto. Esta pedra constrói O PRIMEIRO — o
operador número N do v105a, pelo argumento clássico do TRUNCAMENTO,
formalizado à mão:

* a INCLUSÃO DURA `adjoint_domain_le` : N†.domain ⊆ D_N —
  se x ↦ ⟪y, N x⟫ é contínuo (cota C), testa-se nas truncagens
  x_n = Σ_{j<n} (j·y_j)·e_j: φ(x_n) = S_n e ‖x_n‖² = S_n, logo
  S_n ≤ C·√S_n ⟹ S_n ≤ C² UNIFORME ⟹ Σ j²|y_j|² < ∞;
* ★★★ `numberOp_selfadjoint` — star(N) = N: com a inclusão dura,
  `adjoint_apply_eq` dá a concordância (o x₀ é o próprio N y, pela
  simetria v105a) e `le_adjoint` dá a outra metade — N† = N;
* a consequência imediata: ★★ `theGenuineDirac` —
  `GenuinelyUnboundedDiracData ellTwo` HABITADO (N auto-adjunto +
  kernel contém o Nome + gap quadrático em D_N ∩ span{e₀}^⊥ + a
  ilimitação v105a): A FACE DO CORNER FORTE TEM SEU OPERADOR.

O gap quadrático de N: ortogonal ao kernel ⟹ ‖Nx‖ ≥ ‖x‖ — mas o
kernel de N como LinearPMap pede cuidado; aqui entra a versão
honesta: ker_witness (e₀) + quad_gap com a hipótese de ortogonalidade
a TODO anulado do domínio (como o tipo v99 exige).

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped ENNReal

noncomputable section

/-! ## A — coordenadas das truncagens -/

theorem inscriptions_apply (k j : ℕ) :
    (inscriptions k) j = if j = k then 1 else 0 := by
  unfold inscriptions
  rcases eq_or_ne j k with rfl | hjk
  · rw [lp.single_apply_self, if_pos rfl]
  · rw [lp.single_apply_ne 2 k 1 hjk, if_neg hjk]

/-- a truncagem: x_n = Σ_{j ∈ s} c_j · e_j (elemento de ℓ², suporte finito). -/
def truncation (s : Finset ℕ) (c : ℕ → ℂ) : ellTwo :=
  ∑ k ∈ s, c k • inscriptions k

theorem truncation_mem_domain (s : Finset ℕ) (c : ℕ → ℂ) :
    truncation s c ∈ numberDomain := by
  unfold truncation
  refine Submodule.sum_mem numberDomain ?_
  intro k _
  exact Submodule.smul_mem numberDomain (c k) (single_mem_numberDomain k)

theorem truncation_apply (s : Finset ℕ) (c : ℕ → ℂ) (j : ℕ) :
    (truncation s c) j = if j ∈ s then c j else 0 := by
  unfold truncation
  have hcoe : ((∑ k ∈ s, c k • inscriptions k : ellTwo) : ℕ → ℂ) j
      = ∑ k ∈ s, (c k • inscriptions k : ellTwo) j := by
    induction s using Finset.induction_on with
    | empty => simp [lp.coeFn_zero]
    | insert a t ha ih =>
      rw [Finset.sum_insert ha, lp.coeFn_add, Pi.add_apply, ih,
        Finset.sum_insert ha]
  rw [hcoe]
  have hterm : ∀ k ∈ s, (c k • inscriptions k : ellTwo) j
      = if j = k then c k else 0 := by
    intro k _
    rw [lp.coeFn_smul, Pi.smul_apply, inscriptions_apply, smul_eq_mul]
    rcases eq_or_ne j k with rfl | hjk
    · simp
    · simp [hjk]
  rw [Finset.sum_congr rfl hterm, Finset.sum_ite_eq s j c]

/-! ## B — a soma parcial S_n e as duas identidades do truncamento -/

/-- a soma parcial S_s = Σ_{j ∈ s} j²·‖y_j‖². -/
def partialWeight (s : Finset ℕ) (y : ellTwo) : ℝ :=
  ∑ j ∈ s, (j : ℝ) ^ 2 * ‖y j‖ ^ 2

theorem partialWeight_nonneg (s : Finset ℕ) (y : ellTwo) :
    0 ≤ partialWeight s y := by
  unfold partialWeight
  refine Finset.sum_nonneg ?_
  intro j _
  positivity

/-- a truncagem canônica de y: coeficientes c_j = j·y_j. -/
def yTrunc (s : Finset ℕ) (y : ellTwo) : ellTwo :=
  truncation s (fun j => (j : ℂ) * y j)

theorem yTrunc_apply (s : Finset ℕ) (y : ellTwo) (j : ℕ) :
    (yTrunc s y) j = if j ∈ s then (j : ℂ) * y j else 0 :=
  truncation_apply s _ j

theorem yTrunc_mem (s : Finset ℕ) (y : ellTwo) :
    yTrunc s y ∈ numberDomain :=
  truncation_mem_domain s _

/-- IDENTIDADE 1: ⟪y, N (x_s)⟫ = S_s (a leitura do truncamento é a
    soma parcial — real e não-negativa). -/
theorem inner_number_yTrunc (s : Finset ℕ) (y : ellTwo) :
    inner ℂ y (numberOp ⟨yTrunc s y, yTrunc_mem s y⟩)
      = ((partialWeight s y : ℝ) : ℂ) := by
  rw [lp.inner_eq_tsum]
  have hsupp : ∀ j ∉ s,
      inner ℂ (y j) ((numberOp ⟨yTrunc s y, yTrunc_mem s y⟩ : ellTwo) j) = 0 := by
    intro j hj
    rw [numberOp_apply, yTrunc_apply, if_neg hj]
    simp
  rw [tsum_eq_sum hsupp]
  unfold partialWeight
  rw [Complex.ofReal_sum]
  refine Finset.sum_congr rfl ?_
  intro j hj
  rw [RCLike.inner_apply, numberOp_apply, yTrunc_apply, if_pos hj]
  have hc : (j : ℂ) * ((j : ℂ) * y j) * (starRingEnd ℂ) (y j)
      = ((j : ℂ) * (j : ℂ)) * (y j * (starRingEnd ℂ) (y j)) := by ring
  rw [hc, Complex.mul_conj, Complex.normSq_eq_norm_sq]
  push_cast
  ring

/-- IDENTIDADE 2: ‖x_s‖² = S_s (a norma do truncamento é a mesma soma). -/
theorem norm_sq_yTrunc (s : Finset ℕ) (y : ellTwo) :
    ‖yTrunc s y‖ ^ 2 = partialWeight s y := by
  have h2 : (0 : ℝ) < (2 : ℝ≥0∞).toReal := by norm_num
  have hnorm := lp.norm_rpow_eq_tsum h2 (yTrunc s y)
  have htoReal : (2 : ℝ≥0∞).toReal = 2 := by norm_num
  rw [htoReal] at hnorm
  have hsupp : ∀ j ∉ s, ‖(yTrunc s y) j‖ ^ (2 : ℝ) = 0 := by
    intro j hj
    rw [yTrunc_apply, if_neg hj]
    simp
  rw [tsum_eq_sum hsupp] at hnorm
  have hterm : ∀ j ∈ s, ‖(yTrunc s y) j‖ ^ (2 : ℝ)
      = (j : ℝ) ^ 2 * ‖y j‖ ^ 2 := by
    intro j hj
    rw [yTrunc_apply, if_pos hj, Real.rpow_two, norm_mul,
      Complex.norm_natCast, mul_pow]
  rw [Finset.sum_congr rfl hterm] at hnorm
  calc ‖yTrunc s y‖ ^ 2 = ‖yTrunc s y‖ ^ (2 : ℝ) := (Real.rpow_two _).symm
    _ = partialWeight s y := hnorm

/-! ## C — A INCLUSÃO DURA: N†.domain ⊆ D_N -/

theorem adjoint_domain_le :
    (LinearPMap.adjoint numberOp).domain ≤ numberOp.domain := by
  intro y hy
  -- a continuidade do funcional x ↦ ⟪y, N x⟫ dá a cota C
  rw [LinearPMap.mem_adjoint_domain_iff] at hy
  set φ : numberOp.domain →L[ℂ] ℂ :=
    ⟨(innerₛₗ ℂ y).comp numberOp.toFun, hy⟩ with hφ
  obtain ⟨C, hC0, hC⟩ := φ.bound
  -- a cota uniforme das somas parciais: S_s ≤ C²
  have hS : ∀ s : Finset ℕ, partialWeight s y ≤ C ^ 2 := by
    intro s
    have hx : φ ⟨yTrunc s y, yTrunc_mem s y⟩
        = ((partialWeight s y : ℝ) : ℂ) := inner_number_yTrunc s y
    have hb := hC ⟨yTrunc s y, yTrunc_mem s y⟩
    rw [hx] at hb
    have hnb : ‖((partialWeight s y : ℝ) : ℂ)‖ = partialWeight s y := by
      rw [Complex.norm_real]
      exact abs_of_nonneg (partialWeight_nonneg s y)
    rw [hnb] at hb
    -- hb : S_s ≤ C * ‖x_s‖ ; e ‖x_s‖² = S_s
    have hn2 : ‖(⟨yTrunc s y, yTrunc_mem s y⟩ : numberOp.domain)‖ ^ 2
        = partialWeight s y := norm_sq_yTrunc s y
    set B : ℝ := ‖(⟨yTrunc s y, yTrunc_mem s y⟩ : numberOp.domain)‖ with hB
    have hBnn : 0 ≤ B := norm_nonneg _
    nlinarith [sq_nonneg (B - C)]
  -- somabilidade de j²‖y_j‖² pelas somas parciais uniformes
  have hsummable : Summable (fun j : ℕ => (j : ℝ) ^ 2 * ‖y j‖ ^ 2) := by
    refine summable_of_sum_range_le (c := C ^ 2) ?_ ?_
    · intro j
      positivity
    · intro n
      exact hS (Finset.range n)
  -- Memℓp da sequência n·y_n
  show Memℓp (numberSeq y) 2
  have h2 : (0 : ℝ) < (2 : ℝ≥0∞).toReal := by norm_num
  refine memℓp_gen ?_
  have hcong : (fun j : ℕ => ‖numberSeq y j‖ ^ (2 : ℝ≥0∞).toReal)
      = fun j : ℕ => (j : ℝ) ^ 2 * ‖y j‖ ^ 2 := by
    funext j
    have htoReal : (2 : ℝ≥0∞).toReal = 2 := by norm_num
    rw [htoReal]
    show ‖(j : ℂ) * y j‖ ^ (2 : ℝ) = (j : ℝ) ^ 2 * ‖y j‖ ^ 2
    rw [Real.rpow_two, norm_mul, Complex.norm_natCast, mul_pow]
  rw [hcong]
  exact hsummable

/-! ## D — star(N) = N: o primeiro auto-adjunto ILIMITADO do kernel -/

/-- [KERNEL] ★★★ star(N) = N — a mathlib não tinha NENHUM exemplo
    concreto de operador ilimitado auto-adjunto; agora o canônico tem
    o seu, e ele carrega o Nome no kernel. -/
theorem numberOp_selfadjoint : IsSelfAdjoint numberOp := by
  rw [LinearPMap.isSelfAdjoint_def]
  apply le_antisymm
  · exact ⟨adjoint_domain_le, fun x z hxz =>
      LinearPMap.adjoint_apply_eq numberDomain_dense x
        (fun w => by rw [hxz]; exact numberOp_symmetric z w)⟩
  · exact numberOp_symmetric.le_adjoint numberDomain_dense

/-! ## E — o gap quadrático e o HABITANTE GENUÍNO -/

theorem numberOp_quad_gap (x : numberOp.domain)
    (h : ∀ z : numberOp.domain, numberOp z = 0 →
      inner ℂ (z : ellTwo) (x : ellTwo) = 0) :
    (1 : ℝ) * ‖(x : ellTwo)‖ ≤ ‖numberOp x‖ := by
  -- da ortogonalidade a e₀ (que é anulado): x₀ = 0 ⟹ ‖x‖² = Σ_{j≥1}‖x_j‖²
  have h0 : inner ℂ (firstInscription : ellTwo) (x : ellTwo) = 0 :=
    h ⟨firstInscription, single_mem_numberDomain 0⟩ numberOp_kills_first
  have hx0 : (x : ellTwo) 0 = 0 := by
    have hinner : inner ℂ (firstInscription : ellTwo) (x : ellTwo)
        = (x : ellTwo) 0 := by
      rw [lp.inner_eq_tsum]
      have hsupp : ∀ j ≠ (0 : ℕ),
          inner ℂ (firstInscription j) ((x : ellTwo) j) = 0 := by
        intro j hj
        unfold firstInscription
        rw [inscriptions_apply, if_neg hj]
        simp
      rw [tsum_eq_single 0 hsupp]
      unfold firstInscription
      rw [inscriptions_apply, if_pos rfl, RCLike.inner_apply, map_one, mul_one]
    rw [hinner] at h0
    exact h0
  -- coordenada a coordenada: ‖j·x_j‖ ≥ ‖x_j‖ (j=0: x_0 = 0)
  have hcoord : ∀ j : ℕ, ‖(x : ellTwo) j‖ ^ (2 : ℝ≥0∞).toReal
      ≤ ‖(numberOp x : ellTwo) j‖ ^ (2 : ℝ≥0∞).toReal := by
    intro j
    have htoReal : (2 : ℝ≥0∞).toReal = 2 := by norm_num
    rw [htoReal, Real.rpow_two, Real.rpow_two, numberOp_apply]
    rcases Nat.eq_zero_or_pos j with rfl | hj
    · rw [hx0]
      simp
    · rw [norm_mul, Complex.norm_natCast]
      have h1j : (1 : ℝ) ≤ (j : ℝ) := by exact_mod_cast hj
      have hjj : (1 : ℝ) ≤ (j : ℝ) ^ 2 := by nlinarith
      calc ‖(x : ellTwo) j‖ ^ 2
          = 1 * ‖(x : ellTwo) j‖ ^ 2 := (one_mul _).symm
        _ ≤ (j : ℝ) ^ 2 * ‖(x : ellTwo) j‖ ^ 2 :=
            mul_le_mul_of_nonneg_right hjj (by positivity)
        _ = ((j : ℝ) * ‖(x : ellTwo) j‖) ^ 2 := by ring
  -- soma: ‖x‖² ≤ ‖Nx‖²  ⟹  ‖x‖ ≤ ‖Nx‖
  have h2 : (0 : ℝ) < (2 : ℝ≥0∞).toReal := by norm_num
  have hnx := lp.norm_rpow_eq_tsum h2 (x : ellTwo)
  have hnN := lp.norm_rpow_eq_tsum h2 (numberOp x : ellTwo)
  have hsum_le : ‖(x : ellTwo)‖ ^ (2 : ℝ≥0∞).toReal
      ≤ ‖(numberOp x : ellTwo)‖ ^ (2 : ℝ≥0∞).toReal := by
    rw [hnx, hnN]
    exact Summable.tsum_le_tsum hcoord
      ((lp.memℓp (x : ellTwo)).summable h2)
      ((lp.memℓp (numberOp x : ellTwo)).summable h2)
  have htoReal : (2 : ℝ≥0∞).toReal = 2 := by norm_num
  rw [htoReal, Real.rpow_two, Real.rpow_two] at hsum_le
  rw [one_mul]
  have hnnx := norm_nonneg (x : ellTwo)
  have hnnN := norm_nonneg (numberOp x)
  nlinarith [hsum_le]

/-- [KERNEL] ★★ O HABITANTE GENUÍNO: `GenuinelyUnboundedDiracData`
    tem termo — o operador número auto-adjunto, ilimitado, com o Nome
    no kernel e gap 1 = ω(I). A FACE DO CORNER FORTE TEM SEU OPERADOR. -/
def theGenuineDirac : GenuinelyUnboundedDiracData ellTwo where
  D := numberOp
  selfadjoint := numberOp_selfadjoint
  gap := 1
  gap_pos := one_pos
  ker_witness :=
    ⟨⟨firstInscription, single_mem_numberDomain 0⟩,
      inscriptions_orthonormal.ne_zero 0,
      numberOp_kills_first⟩
  quad_gap := numberOp_quad_gap
  unbounded := numberOp_unbounded

end

end TGLExt
