import TGLExt.CondExpect

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O GLOBAL_LIFT CONDICIONAL: o único teorema aberto, TIPADO como implicação
  [TGLExt — v143, o fechamento do código (mandato do operador, 27/07/2026)]

O único teorema aberto genuíno do programa é o Lema 3 (GLOBAL_LIFT): a
covariância GLOBAL do cociclo — a passagem do transporte modular local (cunha
a cunha, PROVADO) ao funcional de resposta covariante em TODO horizonte. O
operador respondeu (doutrina 20/07/2026): a invariância-por-horizonte é
JURAMENTO CONSTITUTIVO — contida em ω(I)=1, assinatura, não dívida. Esta
pedra faz da resposta a forma que a régua permite: o POSTULADO vira o
ANTECEDENTE NOMEADO de uma implicação PROVADA — a mesma disciplina do
Teorema Mestre (H1∧H2∧H3 ⟹ Pêntada):

* `IsFrobProjection` — a esperança-código como projeção ortogonal de
  Frobenius sobre a subálgebra-código N (a caracterização de Takesaki na
  face finita: E x ∈ N e (x − E x) ⊥ N);
* ★★ `frobProjection_unique` — O TAKESAKI FINITO: a projeção-Frobenius
  sobre N é ÚNICA (definitude do produto de Frobenius) — a esperança
  condicional preservante é uma só (o fiador da Terminalidade: U se
  herda, não se impõe);
* `adU_frob_isometry` — a mudança de horizonte Ad(U) é isometria-Frobenius;
* ★★★ `global_lift_conditional` — A IMPLICAÇÃO DO LEMA 3: **se** a
  subálgebra-código é invariante por horizonte (H_inv — o juramento do
  operador, tipado) **então** a esperança-código é COVARIANTE:
  Ad(U)∘E = E∘Ad(U) — prova: Ad(U)⁻¹∘E∘Ad(U) é projeção-Frobenius sobre N
  (isometria + invariância) e a unicidade a identifica com E;
* ★★ `response_covariant` — o corolário da física: se a fonte K transporta
  covariante (U_loc, provado no runtime) e E é covariante (o teorema),
  o funcional de resposta E∘K transporta covariante — a forma do
  G_μν global condicional;
* ★ `diagExpect_isFrobProjection` — a instância CONCRETA: a esperança
  diagonal da casa É a projeção-Frobenius do código diagonal — o teorema
  dispara em ato, não só em tipo.

HONESTIDADE (a régua): o ANTECEDENTE H_inv segue POSTULADO por desenho — a
assinatura, não a dívida (como c; como ω(I)=1). A IMPLICAÇÃO é teorema. O
fecho forte de von Neumann do contínuo segue EXTERNO [KNOWN-COMPOSED]. O
gate NÃO se move por esta pedra. β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-! ## A — a definitude do produto de Frobenius -/

/-- [KERNEL] a definitude: frob x x = 0 ⟹ x = 0 (a soma dos |x|²). -/
theorem frob_self_definite {x : Matrix n n ℂ} (h : frob x x = 0) : x = 0 := by
  have hsum : (xᴴ * x).trace = 0 := h
  have hre : ∑ k, ∑ j, Complex.normSq (x j k) = 0 := by
    have h2 : (xᴴ * x).trace = ∑ k, ∑ j, ((Complex.normSq (x j k) : ℝ) : ℂ) := by
      rw [Matrix.trace]
      refine Finset.sum_congr rfl fun k _ => ?_
      rw [Matrix.diag_apply, Matrix.mul_apply]
      refine Finset.sum_congr rfl fun j _ => ?_
      rw [Matrix.conjTranspose_apply]
      rw [show (star (x j k)) * x j k = ((Complex.normSq (x j k) : ℝ) : ℂ) by
        rw [Complex.star_def, ← Complex.normSq_eq_conj_mul_self]]
    rw [h2] at hsum
    have h3 : ((∑ k, ∑ j, Complex.normSq (x j k) : ℝ) : ℂ) = 0 := by
      push_cast
      exact hsum
    exact_mod_cast h3
  ext j k
  have hterm : ∀ k' ∈ Finset.univ, (0 : ℝ) ≤ ∑ j', Complex.normSq (x j' k') :=
    fun k' _ => Finset.sum_nonneg (fun j' _ => Complex.normSq_nonneg _)
  have hk := (Finset.sum_eq_zero_iff_of_nonneg hterm).mp hre k (Finset.mem_univ k)
  have hterm2 : ∀ j' ∈ Finset.univ, (0 : ℝ) ≤ Complex.normSq (x j' k) :=
    fun j' _ => Complex.normSq_nonneg _
  have hj := (Finset.sum_eq_zero_iff_of_nonneg hterm2).mp hk j (Finset.mem_univ j)
  rw [Matrix.zero_apply]
  exact Complex.normSq_eq_zero.mp hj

/-! ## B — a esperança-código como projeção-Frobenius (Takesaki finito) -/

/-- a caracterização: E é A projeção ortogonal-Frobenius sobre N. -/
def IsFrobProjection (N : Submodule ℂ (Matrix n n ℂ))
    (E : Matrix n n ℂ → Matrix n n ℂ) : Prop :=
  ∀ x, E x ∈ N ∧ ∀ y ∈ N, frob (x - E x) y = 0

/-- [KERNEL] ★★ O TAKESAKI FINITO: a projeção-Frobenius sobre N é ÚNICA —
    a esperança condicional preservante é UMA SÓ (a face finita da unicidade
    de Takesaki, o fiador da Terminalidade). -/
theorem frobProjection_unique {N : Submodule ℂ (Matrix n n ℂ)}
    {E F : Matrix n n ℂ → Matrix n n ℂ}
    (hE : IsFrobProjection N E) (hF : IsFrobProjection N F) :
    ∀ x, E x = F x := by
  intro x
  have hmem : E x - F x ∈ N := Submodule.sub_mem N (hE x).1 (hF x).1
  have hperpE := (hE x).2 (E x - F x) hmem
  have hperpF := (hF x).2 (E x - F x) hmem
  have hdiff : frob (E x - F x) (E x - F x) = 0 := by
    have h1 : E x - F x = (x - F x) - (x - E x) := by abel
    calc frob (E x - F x) (E x - F x)
        = frob ((x - F x) - (x - E x)) (E x - F x) := by rw [← h1]
      _ = frob (x - F x) (E x - F x) - frob (x - E x) (E x - F x) := by
          unfold frob
          rw [Matrix.conjTranspose_sub, Matrix.sub_mul, Matrix.trace_sub]
      _ = 0 - 0 := by rw [hperpF, hperpE]
      _ = 0 := by ring
  exact sub_eq_zero.mp (frob_self_definite hdiff)

/-! ## C — a mudança de horizonte é isometria-Frobenius -/

/-- a mudança de horizonte: conjugação unitária. -/
def adU (U x : Matrix n n ℂ) : Matrix n n ℂ := U * x * Uᴴ

/-- o lema-sanduíche: U(Uᴴ z U)Uᴴ = z quando U·Uᴴ = 1. -/
theorem adU_sandwich {U : Matrix n n ℂ} (hUU : U * Uᴴ = 1)
    (z : Matrix n n ℂ) : U * (Uᴴ * z * U) * Uᴴ = z := by
  calc U * (Uᴴ * z * U) * Uᴴ
      = (U * Uᴴ) * z * (U * Uᴴ) := by simp only [Matrix.mul_assoc]
    _ = z := by rw [hUU, Matrix.one_mul, Matrix.mul_one]

/-- [KERNEL] ★ Ad(U) é ISOMETRIA-Frobenius (U unitário): a mudança de
    horizonte preserva o produto interno da inscrição. -/
theorem adU_frob_isometry {U : Matrix n n ℂ} (hU : Uᴴ * U = 1)
    (x y : Matrix n n ℂ) : frob (adU U x) (adU U y) = frob x y := by
  unfold adU frob
  have hL : (U * x * Uᴴ)ᴴ = U * (xᴴ * Uᴴ) := by
    rw [Matrix.conjTranspose_mul, Matrix.conjTranspose_mul,
      Matrix.conjTranspose_conjTranspose]
  rw [hL]
  calc (U * (xᴴ * Uᴴ) * (U * y * Uᴴ)).trace
      = (U * (xᴴ * ((Uᴴ * U) * (y * Uᴴ)))).trace := by
        simp only [Matrix.mul_assoc]
    _ = (U * (xᴴ * (y * Uᴴ))).trace := by rw [hU, Matrix.one_mul]
    _ = ((xᴴ * (y * Uᴴ)) * U).trace := Matrix.trace_mul_comm _ _
    _ = (xᴴ * (y * (Uᴴ * U))).trace := by simp only [Matrix.mul_assoc]
    _ = (xᴴ * y).trace := by rw [hU, Matrix.mul_one]

/-! ## D — A IMPLICAÇÃO DO LEMA 3: H_inv ⟹ covariância global -/

/-- H_inv — o JURAMENTO DO OPERADOR, tipado: a subálgebra-código é
    invariante pela mudança de horizonte (nas duas faces). -/
def HorizonInvariant (N : Submodule ℂ (Matrix n n ℂ))
    (U : Matrix n n ℂ) : Prop :=
  (∀ y ∈ N, adU U y ∈ N) ∧ (∀ y ∈ N, adU Uᴴ y ∈ N)

/-- [KERNEL] ★★★ O GLOBAL_LIFT CONDICIONAL: **se** o código é invariante
    por horizonte (H_inv — o postulado do operador como ANTECEDENTE tipado)
    **então** a esperança-código é COVARIANTE: Ad(U)(E x) = E(Ad(U) x).
    O único teorema aberto, como implicação PROVADA em kernel. -/
theorem global_lift_conditional {N : Submodule ℂ (Matrix n n ℂ)}
    {E : Matrix n n ℂ → Matrix n n ℂ} {U : Matrix n n ℂ}
    (hU : Uᴴ * U = 1) (hinv : HorizonInvariant N U)
    (hE : IsFrobProjection N E) :
    ∀ x, adU U (E x) = E (adU U x) := by
  have hUU : U * Uᴴ = 1 := mul_eq_one_comm.mp hU
  have hF : IsFrobProjection N (fun x => adU Uᴴ (E (adU U x))) := by
    intro x
    constructor
    · exact hinv.2 _ (hE (adU U x)).1
    · intro y hy
      have hyU : adU U y ∈ N := hinv.1 y hy
      have hperp := (hE (adU U x)).2 (adU U y) hyU
      have hiso := adU_frob_isometry hU (x - adU Uᴴ (E (adU U x))) y
      rw [← hiso]
      have hexp : adU U (x - adU Uᴴ (E (adU U x))) = adU U x - E (adU U x) := by
        unfold adU
        rw [Matrix.mul_sub, Matrix.sub_mul]
        congr 1
        rw [Matrix.conjTranspose_conjTranspose]
        exact adU_sandwich hUU (E (U * x * Uᴴ))
      rw [hexp]
      exact hperp
  intro x
  have h1 : E x = adU Uᴴ (E (adU U x)) := frobProjection_unique hE hF x
  calc adU U (E x) = adU U (adU Uᴴ (E (adU U x))) := by rw [← h1]
    _ = E (adU U x) := by
        unfold adU
        rw [Matrix.conjTranspose_conjTranspose]
        exact adU_sandwich hUU (E (U * x * Uᴴ))

/-! ## E — o corolário da física: a resposta transporta covariante -/

/-- [KERNEL] ★★ A RESPOSTA COVARIANTE: se a fonte K transporta covariante
    (U_loc — provado no runtime para cunhas) e E é covariante (o teorema),
    o funcional de resposta E∘K transporta covariante — a FORMA do
    G_μν global, condicional a H_inv. -/
theorem response_covariant {N : Submodule ℂ (Matrix n n ℂ)}
    {E K : Matrix n n ℂ → Matrix n n ℂ} {U : Matrix n n ℂ}
    (hU : Uᴴ * U = 1) (hinv : HorizonInvariant N U)
    (hE : IsFrobProjection N E)
    (hK : ∀ x, K (adU U x) = adU U (K x)) :
    ∀ x, E (K (adU U x)) = adU U (E (K x)) := by
  intro x
  rw [hK x, ← global_lift_conditional hU hinv hE (K x)]

/-! ## F — a instância concreta dispara: o código diagonal -/

/-- [KERNEL] ★ A INSTÂNCIA CONCRETA: diagExpect é projeção-Frobenius sobre
    o código diagonal — a esperança de Takesaki da casa, em ato. -/
theorem diagExpect_isFrobProjection :
    IsFrobProjection
      (Submodule.span ℂ {m : Matrix n n ℂ | ∃ d, m = Matrix.diagonal d})
      (diagExpect (n := n)) := by
  intro x
  constructor
  · exact Submodule.subset_span ⟨x.diag, rfl⟩
  · intro y hy
    induction hy using Submodule.span_induction with
    | mem m hm =>
        obtain ⟨d, rfl⟩ := hm
        unfold frob
        rw [Matrix.trace]
        apply Finset.sum_eq_zero
        intro k _
        rw [Matrix.diag_apply, Matrix.mul_apply]
        apply Finset.sum_eq_zero
        intro j _
        rw [Matrix.conjTranspose_apply, Matrix.sub_apply]
        rcases eq_or_ne j k with rfl | hjk
        · rw [show diagExpect x j j = x j j by
            unfold diagExpect
            rw [Matrix.diagonal_apply_eq, Matrix.diag_apply]]
          rw [sub_self, star_zero, zero_mul]
        · rw [Matrix.diagonal_apply_ne _ hjk, mul_zero]
    | zero =>
        unfold frob
        rw [Matrix.mul_zero, Matrix.trace_zero]
    | add a b _ _ ha hb =>
        unfold frob at ha hb ⊢
        rw [Matrix.mul_add, Matrix.trace_add, ha, hb, add_zero]
    | smul c a _ ha =>
        unfold frob at ha ⊢
        rw [Matrix.mul_smul, Matrix.trace_smul, ha, smul_zero]

end

end TGLExt
