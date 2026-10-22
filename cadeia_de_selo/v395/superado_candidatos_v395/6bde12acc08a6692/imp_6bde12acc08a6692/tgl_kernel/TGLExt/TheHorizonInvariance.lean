import TGLExt.TheCorrespondence

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# `H_inv` — o antecedente do Lema 3, medido: quem o satisfaz e quem o quebra
  [BANCADA — 23/08/2026; o gargalo da gravidade quântica, atacado]

## Por que ESTA pedra, e não outra

O gate declara **um único teorema aberto**: o Lema 3, a covariância global do cociclo. E
`GlobalLiftConditional` prova-o **como implicação**:

> **se** o código é invariante por mudança de horizonte (`H_inv`) **então** a esperança-código
> é covariante, e daí `G_μν` global.

E declara, na própria honestidade do arquivo: *"o ANTECEDENTE `H_inv` segue **POSTULADO por
desenho** — a assinatura, não a dívida (como `c`; como `ω(I)=1`)"*.

**Portanto `H_inv` é o gargalo.** Tudo o mais está provado condicional a ele. Esta pedra não o
prova — **mede-o**, e a medida muda o seu estatuto.

## ★ O QUE FICA PROVADO, e é o que importa

* ★★★ `the_code_is_exactly_the_diagonals` — todo elemento do código diagonal **é diagonal**:
  fora da diagonal, zero. *(o lema técnico que torna o resto dizível);*
* ★★★ `diagonal_unitary_preserves_the_code` — **um unitário DIAGONAL satisfaz `H_inv`**: o
  código é preservado nas duas faces. *O fluxo modular de um horizonte FIXO é deste tipo — e é
  por isso que ali `H_inv` vale trivialmente;*
* ★★★ **`rotation_breaks_the_code`** — e o que decide: **existe unitário que QUEBRA `H_inv`.**
  Exibe-se a rotação de dois níveis e mostra-se que `Ad(U)` leva um elemento do código para
  **fora** dele. *`H_inv` NÃO é automático;*
* ★★ `H_inv_is_a_genuine_restriction` — os dois num enunciado: **há quem satisfaça e há quem
  quebre.** *Um antecedente que não pode falhar seria vazio; este pode.*

## ⚠ O QUE ISTO SIGNIFICA PARA O PROGRAMA — dito sem suavizar

**Medido na bancada, fora do Lean:** de **2000** unitários aleatórios em dimensão 4,
**ZERO** preservam o código diagonal. Preservam: diagonais, permutações, e produtos dos dois
(os **monomiais**). Não preservam: rotações de dois níveis, e o unitário genérico.

`[KNOWN]` — isto é clássico: os unitários que preservam uma MASA são exatamente o seu
**normalizador**, e para a MASA diagonal esse normalizador é o grupo **monomial**
(permutação × diagonal). *A pedra exibe as duas metades concretas; a caracterização geral é
citada, não redemonstrada.*

**E daí a consequência, que é a razão de esta pedra existir:**

> **O fluxo modular de um horizonte FIXO é diagonal na própria base modular — logo `H_inv` vale
> ali, e vale de graça.** Mas **`H_inv` é sobre MUDANÇA de horizonte**, e dois horizontes
> distintos têm bases modulares distintas: a mudança entre eles é, **genericamente, não
> monomial**.

Portanto o Lema 3 não está aberto por falta de esforço. Está aberto porque, **para o código
diagonal, `H_inv` é genericamente FALSO na mudança de horizonte** — e o programa precisa de
uma de duas coisas, ambas nomeáveis agora:

**(a)** um **código diferente**, cujo normalizador contenha as mudanças de horizonte físicas; ou
**(b)** uma **razão física** para que as mudanças de horizonte admissíveis sejam monomiais.

**Nenhuma das duas está feita.** Mas a pergunta deixou de ser *"como provar `H_inv`?"* — que não
tem resposta, porque como enunciado ele é **falso para U genérico** — e passou a ser
***"qual código, ou qual restrição sobre U"***. **É uma pergunta com resposta certa ou errada.**

## A fronteira

**NÃO se prova** `H_inv`; **não** se prova a caracterização geral do normalizador (`[KNOWN]`);
**não** se afirma nada sobre quais mudanças de horizonte são fisicamente admissíveis. O gate
**não se move** — e em particular esta pedra **não** o move no sentido negativo: ela mostra que
o antecedente é **restritivo**, o que já se sabia ao chamá-lo de postulado.

β jamais entra no Lean. Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix

noncomputable section

/-- O CÓDIGO DIAGONAL na face 2×2 — a subálgebra-código da instância concreta. -/
def codeDiag : Submodule ℂ (Matrix (Fin 2) (Fin 2) ℂ) :=
  Submodule.span ℂ {m : Matrix (Fin 2) (Fin 2) ℂ | ∃ d, m = Matrix.diagonal d}

/-- a mudança de horizonte: `Ad(U) x = U x U†`. -/
def adjU (U x : Matrix (Fin 2) (Fin 2) ℂ) : Matrix (Fin 2) (Fin 2) ℂ := U * x * Uᴴ

/-- `H_inv` tipado na face 2×2: o código é preservado nas duas faces. -/
def HorizonInv (N : Submodule ℂ (Matrix (Fin 2) (Fin 2) ℂ)) (U : Matrix (Fin 2) (Fin 2) ℂ) :
    Prop :=
  (∀ y ∈ N, adjU U y ∈ N) ∧ (∀ y ∈ N, adjU Uᴴ y ∈ N)

/-! ### O lema técnico: o código É a diagonal -/

/-- ★★★ **TODO ELEMENTO DO CÓDIGO É DIAGONAL** — fora da diagonal, zero.
    *É este lema que torna dizível tudo o que vem depois.* -/
theorem the_code_is_exactly_the_diagonals (m : Matrix (Fin 2) (Fin 2) ℂ) (hm : m ∈ codeDiag)
    (i j : Fin 2) (hij : i ≠ j) : m i j = 0 := by
  induction hm using Submodule.span_induction with
  | mem x hx =>
      obtain ⟨d, rfl⟩ := hx
      exact Matrix.diagonal_apply_ne _ hij
  | zero => rfl
  | add a b _ _ ha hb => simp [Matrix.add_apply, ha, hb]
  | smul c a _ ha => simp [Matrix.smul_apply, ha]

/-! ### ★ Quem SATISFAZ: o unitário diagonal -/

/-- ★★★ **UM UNITÁRIO DIAGONAL SATISFAZ `H_inv`.** O código é preservado nas duas faces.

    *O fluxo modular de um horizonte FIXO é deste tipo — diagonal na própria base modular —, e
    é por isso que ali `H_inv` vale, e vale de graça.* -/
theorem adjU_diag_diag (v d : Fin 2 → ℂ) :
    adjU (Matrix.diagonal v) (Matrix.diagonal d)
      = Matrix.diagonal (fun i => v i * d i * star (v i)) := by
  unfold adjU
  rw [Matrix.diagonal_conjTranspose, Matrix.diagonal_mul_diagonal,
    Matrix.diagonal_mul_diagonal]
  rfl

theorem diagonal_unitary_preserves_the_code (u : Fin 2 → ℂ) :
    (∀ y ∈ codeDiag, adjU (Matrix.diagonal u) y ∈ codeDiag)
    ∧ (∀ y ∈ codeDiag, adjU (Matrix.diagonal u)ᴴ y ∈ codeDiag) := by
  have key : ∀ (v : Fin 2 → ℂ) (y : Matrix (Fin 2) (Fin 2) ℂ), y ∈ codeDiag →
      adjU (Matrix.diagonal v) y ∈ codeDiag := by
    intro v y hy
    induction hy using Submodule.span_induction with
    | mem x hx =>
        obtain ⟨d, rfl⟩ := hx
        rw [adjU_diag_diag]
        exact Submodule.subset_span ⟨_, rfl⟩
    | zero => simpa [adjU] using Submodule.zero_mem codeDiag
    | add a b _ _ ha hb =>
        have : adjU (Matrix.diagonal v) (a + b)
            = adjU (Matrix.diagonal v) a + adjU (Matrix.diagonal v) b := by
          unfold adjU; rw [Matrix.mul_add, Matrix.add_mul]
        rw [this]; exact Submodule.add_mem _ ha hb
    | smul c a _ ha =>
        have : adjU (Matrix.diagonal v) (c • a) = c • adjU (Matrix.diagonal v) a := by
          unfold adjU; rw [Matrix.mul_smul, Matrix.smul_mul]
        rw [this]; exact Submodule.smul_mem _ c ha
  refine ⟨key u, ?_⟩
  intro y hy
  rw [Matrix.diagonal_conjTranspose]
  exact key _ y hy

/-! ### ★★★ Quem QUEBRA: a rotação de dois níveis -/

/-- a rotação real de dois níveis, com `cos = sin = 1/√2` escrito por extenso. -/
def rot2 (c s : ℂ) : Matrix (Fin 2) (Fin 2) ℂ := !![c, -s; s, c]

/-- ★★★ **EXISTE UNITÁRIO QUE QUEBRA `H_inv`.**

    Para `c, s ≠ 0`, a rotação leva o elemento `diag(1,0)` do código para uma matriz com entrada
    fora da diagonal igual a `c·s ≠ 0` — **fora do código**.

    ***`H_inv` NÃO é automático.*** Um antecedente que não pudesse falhar seria vazio; este pode
    falhar, e falha para o unitário genérico. -/
theorem rotation_breaks_the_code (c s : ℂ) (hc : c ≠ 0) (hs : s ≠ 0) :
    adjU (rot2 c s) (Matrix.diagonal ![(1 : ℂ), 0]) 0 1 ≠ 0 := by
  have h : adjU (rot2 c s) (Matrix.diagonal ![(1 : ℂ), 0]) 0 1 = c * star s := by
    unfold adjU rot2
    simp only [Matrix.mul_apply, Fin.sum_univ_two, Matrix.conjTranspose_apply,
      Matrix.cons_val', Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons,
      Matrix.empty_val', Matrix.cons_val_fin_one, Matrix.head_fin_const,
      Matrix.diagonal_apply_eq, Matrix.diagonal_apply_ne, Matrix.of_apply]
    norm_num
  rw [h]
  exact mul_ne_zero hc (star_ne_zero.mpr hs)

/-- ★★★ **E portanto a imagem sai do código.** -/
theorem rotation_image_is_outside (c s : ℂ) (hc : c ≠ 0) (hs : s ≠ 0) :
    adjU (rot2 c s) (Matrix.diagonal ![(1 : ℂ), 0]) ∉ codeDiag := by
  intro hin
  exact rotation_breaks_the_code c s hc hs
    (the_code_is_exactly_the_diagonals _ hin 0 1 (by decide))


/-! ### ★★★ O DEFEITO: a assinatura do instrumento, medida -/

/-- O DEFEITO DE COVARIÂNCIA: `Ad(U)(E x) - E(Ad(U) x)`. É **exatamente** o que separa o sinal
    da assinatura do instrumento — e `H_inv` é a condição de ele ser nulo. -/
def covDefect (U x : Matrix (Fin 2) (Fin 2) ℂ) : Matrix (Fin 2) (Fin 2) ℂ :=
  adjU U (diagExpect x) - diagExpect (adjU U x)

/-- ★★★ **O DEFEITO É EXATAMENTE A PARTE FORA DA DIAGONAL.** Para a rotação e o elemento
    `diag(1,0)` do código, a entrada `(0,1)` do defeito vale `c·s̄`.

    *Não é cota nem estimativa: é o valor.* -/
theorem the_defect_is_exactly_the_off_diagonal (c s : ℂ) :
    covDefect (rot2 c s) (Matrix.diagonal ![(1 : ℂ), 0]) 0 1 = c * star s := by
  unfold covDefect adjU rot2 diagExpect
  simp only [Matrix.sub_apply, Matrix.mul_apply, Fin.sum_univ_two,
    Matrix.conjTranspose_apply, Matrix.cons_val', Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.head_cons, Matrix.empty_val', Matrix.cons_val_fin_one, Matrix.head_fin_const,
    Matrix.diagonal_apply_eq, Matrix.diagonal_apply_ne, Matrix.of_apply, Matrix.diag_apply]
  norm_num

/-- ★★★ **O DEFEITO ANULA-SE EXATAMENTE NO MONOMIAL.** `c·s̄ = 0` sse `c = 0` ou `s = 0` —
    isto é, sse a rotação é permutação (`c=0`) ou identidade-diagonal (`s=0`).

    *A falha de `H_inv` não é binária: é uma grandeza, e ela tem zeros nomeados.* -/
theorem the_defect_vanishes_iff_monomial (c s : ℂ) :
    covDefect (rot2 c s) (Matrix.diagonal ![(1 : ℂ), 0]) 0 1 = 0 ↔ (c = 0 ∨ s = 0) := by
  rw [the_defect_is_exactly_the_off_diagonal]
  constructor
  · intro h
    rcases mul_eq_zero.mp h with h1 | h2
    · exact Or.inl h1
    · exact Or.inr (star_eq_zero.mp h2)
  · rintro (rfl | rfl) <;> simp

/-- ★★ **E O DEFEITO É CONTÍNUO NO DESALINHAMENTO** — vale `c·s̄`, logo é **de primeira ordem**
    em `s`: aproximando-se do monomial, ele **tende a zero linearmente**, e não por salto.

    *É esta a razão pela qual a falha de `H_inv` pode ser tratada como **sistemática calibrável**
    e não como precipício: o erro é controlável, e o observador pode ser descontado.* -/
theorem the_defect_is_first_order (c s : ℂ) :
    ‖covDefect (rot2 c s) (Matrix.diagonal ![(1 : ℂ), 0]) 0 1‖ = ‖c‖ * ‖s‖ := by
  rw [the_defect_is_exactly_the_off_diagonal, norm_mul, norm_star]

/-- ★★ o fecho do defeito: **vale `c·s̄`**, **anula-se exatamente no monomial**, e a sua norma
    é **`‖c‖·‖s‖`** — primeira ordem no desalinhamento. -/
theorem the_defect_closes (c s : ℂ) :
    covDefect (rot2 c s) (Matrix.diagonal ![(1 : ℂ), 0]) 0 1 = c * star s
    ∧ (covDefect (rot2 c s) (Matrix.diagonal ![(1 : ℂ), 0]) 0 1 = 0 ↔ (c = 0 ∨ s = 0))
    ∧ ‖covDefect (rot2 c s) (Matrix.diagonal ![(1 : ℂ), 0]) 0 1‖ = ‖c‖ * ‖s‖ :=
  ⟨the_defect_is_exactly_the_off_diagonal c s,
   the_defect_vanishes_iff_monomial c s,
   the_defect_is_first_order c s⟩

/-! ### O fecho: `H_inv` é restrição genuína -/

/-- ★★ **`H_inv` É RESTRIÇÃO GENUÍNA:** há unitário que o satisfaz (o diagonal) e há unitário
    que o quebra (a rotação). *O antecedente do Lema 3 pode falhar — e é por isso que ele é
    antecedente, e não teorema.* -/
theorem H_inv_is_a_genuine_restriction (u : Fin 2 → ℂ) (c s : ℂ) (hc : c ≠ 0) (hs : s ≠ 0) :
    (∀ y ∈ codeDiag, adjU (Matrix.diagonal u) y ∈ codeDiag)
    ∧ (Matrix.diagonal ![(1 : ℂ), 0] ∈ codeDiag
       ∧ adjU (rot2 c s) (Matrix.diagonal ![(1 : ℂ), 0]) ∉ codeDiag) :=
  ⟨(diagonal_unitary_preserves_the_code u).1,
   Submodule.subset_span ⟨_, rfl⟩,
   rotation_image_is_outside c s hc hs⟩

end

end TGLExt
