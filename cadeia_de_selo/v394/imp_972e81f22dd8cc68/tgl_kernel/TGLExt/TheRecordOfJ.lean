import TGLExt.MarkovTower

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# `R_J` — O REGISTRO LINEAR INDUZIDO PELA CONJUGAÇÃO, e o traço que o mede
  [BANCADA — 21/08/2026; ainda NÃO embutido no canônico]

## A encomenda, verbatim

`TGL_FORMA_CANONICA_FINAL_C_PSI_ATUALIZADA_2026-08-21.json`,
`canonical_form.typed_core.commutation_unity`:

> *"`typed_candidate`: **β_TGL = τ_F(R_J)**, onde `R_J` é o operador
> **LINEAR/traçável** que registra a operação de conjugação de J sobre 𝒞 no
> terminal; **não `Tr(J)`, pois J é antiunitário**."*
> *"`typing_note`: Como J é antiunitário, a etapa formal necessária é
> **construir `R_J`** (ou outro funcional traçável) a partir da operação de
> conjugação e então aplicar a traça normalizada `τ_F`."*

Uma varredura do kernel mediu: **`R_J` tinha zero definições** — existia
apenas como comentário. Esta pedra o constrói, com os objetos que já moravam
em `LeftRight.lean`, e mede o traço.

## O que fica provado

* ★★★ `J_is_not_complex_linear` — **`J` NÃO é ℂ-linear**, exibido com
  testemunha (`c = i`). Corolário de tipo: `J ∉ Module.End ℂ`, e portanto
  **`LinearMap.trace ℂ J` não tipa**. A exclusão que o JSON declara deixa de
  ser advertência e vira **negativo honesto em kernel**;
* ★★★ `recJ` — **o registro**: `R_J(a) := z ↦ J (L_{aᴴ} (J z))`. Duas
  travessias antilineares compõem-se em **linear**, e por isso o objeto é
  traçável onde `J` sozinho não é;
* ★★★ `recJ_eq_Rmul` — **`R_J(a) = R_a`**: o registro da conjugação **é** a
  multiplicação à direita. Cai em uma linha de `Jconj_Lmul_Jconj`;
* ★★★ `recJ_mem_commutant` — **o registro vive no comutante** `L(Mₙ)′`. É a
  metade algébrica de Tomita dizendo *onde* a conjugação deposita o que
  registra;
* ★★ `trOne_recJ_one` — **`τ_F(R_J(1)) = 1 = ω(I)`**: medido pelo traço
  normalizado, o registro da conjugação entrega na identidade exatamente o
  **peso do Nome**;
* ★★ `recJ_is_additive`, `recJ_is_smul` e `trOne_recJ_additive` — o registro
  depende de `a` **linearmente**, e o funcional `a ↦ τ_F(R_J(a))` é aditivo:
  é isso que faz dele um **funcional linear**, que é o que a encomenda pede.

⚠ **O que este cabeçalho NÃO anuncia, de propósito:** a forma fechada
`τ_F(R_J(a)) = tr(a)/n` para `a` arbitrário **não está provada aqui** — ver a
seção final. *Nome que promete mais do que o enunciado entrega é a doença que
esta casa caça; não se comete no próprio arquivo.*

## ⚠ A RÉGUA, dita antes que alguém leia demais

Isto **NÃO põe β no Lean, e não o mede.** O que se prova é que **existe** o
funcional linear normalizado sobre o registro induzido por J, que ele **é**
traçável, e que `Tr(J)` **não tipa**. O **valor** de β continua sendo leitura
de runtime (`ALPHA_FINE_CODATA_2018 × √e`), fora do kernel, como sempre.

A identificação **`β_TGL = τ_F(R_J)`** permanece **[CONJECTURE]** do operador:
esta pedra entrega o **lado direito** da equação — o objeto, o tipo e a
medida — e deixa a igualdade onde ela estava. Nenhuma flag se move.
Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-! ### B1 — a exclusão `Tr(J)`, por tipo -/

/-- ★★★ **`J` NÃO É ℂ-LINEAR**, com testemunha. Logo `J` não é elemento de
    `Module.End ℂ`, e **`LinearMap.trace ℂ J` sequer tipa**: a exclusão que o
    arquivo canônico declara é aqui um **negativo honesto**, não uma
    advertência. -/
theorem J_is_not_complex_linear [Nonempty n] :
    ¬ (∀ (c : ℂ) (z : Matrix n n ℂ), Jconj (c • z) = c • Jconj z) := by
  intro h
  have hne : (1 : Matrix n n ℂ) ≠ 0 := one_ne_zero
  have := h Complex.I 1
  rw [Jconj_smul] at this
  have hI : (star Complex.I : ℂ) = -Complex.I := by simp
  rw [hI] at this
  have h2 : ((-Complex.I) - Complex.I) • Jconj (1 : Matrix n n ℂ) = 0 := by
    rw [sub_smul, this, sub_self]
  have hcoef : ((-Complex.I) - Complex.I) = -(2 * Complex.I) := by ring
  rw [hcoef, neg_smul, neg_eq_zero, smul_eq_zero] at h2
  rcases h2 with hc | hz
  · exact absurd hc (by simp [Complex.I_ne_zero])
  · exact hne (by simpa [Jconj] using congrArg Jconj hz)

/-! ### B4 — o registro linear induzido pela conjugação -/

/-- **`R_J`** — o registro da operação de conjugação de `J`, como aplicação
    linear: `R_J(a) : z ↦ J (L_{aᴴ} (J z))`. **Duas travessias antilineares
    compõem-se em linear** — é exatamente por isso que ele é traçável onde
    `J` sozinho não é. -/
def recJ (a : Matrix n n ℂ) : Module.End ℂ (Matrix n n ℂ) :=
  Rmul a

/-- ★★★ **O REGISTRO É A MULTIPLICAÇÃO À DIREITA.** `R_J(a) = R_a`, e a prova
    é a metade algébrica de Tomita já provada na casa. -/
theorem recJ_apply (a z : Matrix n n ℂ) :
    recJ a z = Jconj (Lmul aᴴ (Jconj z)) := by
  rw [Jconj_Lmul_Jconj]
  simp [recJ]

/-- ★★★ o registro **é** `Rmul` — dito como identidade de operadores. -/
theorem recJ_eq_Rmul (a : Matrix n n ℂ) : recJ a = Rmul a := rfl

/-- ★★★ **O REGISTRO VIVE NO COMUTANTE.** `R_J(a) ∈ L(Mₙ)′` — a conjugação
    deposita o que registra do outro lado da álgebra. -/
theorem recJ_mem_commutant (a : Matrix n n ℂ) :
    recJ a ∈ commutantSet (Set.range (Lmul (n := n))) := by
  rw [commutant_range_Lmul]
  exact ⟨a, rfl⟩

/-- ★★ o registro é **aditivo** em `a`. -/
theorem recJ_is_additive (a b : Matrix n n ℂ) :
    recJ (a + b) = recJ a + recJ b := by
  refine LinearMap.ext fun z => ?_
  simp [recJ, Rmul, mul_add]

/-- ★★ e **ℂ-homogêneo** em `a`. Junto com a aditividade: `a ↦ R_J(a)` é
    ℂ-linear, e é isso que faz de `τ_F ∘ R_J` um **funcional linear**. -/
theorem recJ_is_smul (c : ℂ) (a : Matrix n n ℂ) :
    recJ (c • a) = c • recJ a := by
  refine LinearMap.ext fun z => ?_
  simp [recJ, Rmul, mul_smul_comm]

/-! ### B5 — o traço normalizado do registro -/

/-- ★★ **NA IDENTIDADE, O REGISTRO PESA UM.** `τ_F(R_J(1)) = 1 = ω(I)`.
    O registro da conjugação, medido pelo traço normalizado, entrega
    exatamente o peso do Nome. -/
theorem trOne_recJ_one [Nonempty n] :
    trOne (recJ (1 : Matrix n n ℂ)) = 1 := by
  have h1 : (recJ (1 : Matrix n n ℂ)) = (1 : Module.End ℂ (Matrix n n ℂ)) := by
    refine LinearMap.ext fun z => ?_
    simp [recJ, Rmul]
  rw [trOne, h1, trace_end_one]
  have hn : (Fintype.card n : ℂ) ≠ 0 := by
    exact_mod_cast (Nat.cast_ne_zero (R := ℂ)).mpr Fintype.card_ne_zero
  field_simp

/-- ★ o funcional `a ↦ τ_F(R_J(a))` é **aditivo** — logo é funcional linear,
    que é o que a encomenda do JSON pede ("traça normalizada aplicada ao
    registro"). -/
theorem trOne_recJ_additive [Nonempty n] (a b : Matrix n n ℂ) :
    trOne (recJ (a + b)) = trOne (recJ a) + trOne (recJ b) := by
  rw [recJ_is_additive, trOne, trOne, trOne, map_add, add_div]

/-! ### O QUE FICA ABERTO NESTA PEDRA, dito

A forma fechada **`τ_F(R_J(a)) = tr(a)/n`** para `a` arbitrário exige o traço
de `Rmul a` como aplicação linear sobre `Mₙ`, que **não existe no mathlib**
(medido: não há `LinearMap.trace_mulRight`). O valor é `n·tr(a)` — a conta é
a decomposição em unidades matriciais, no padrão de `trace_Lmul_eD`
(`MarkovTower.lean:118-129`) — e fica como o próximo passo desta pedra.
O que está provado aqui basta para o essencial: **o registro existe, é
linear, vive no comutante, e o funcional normalizado o mede, valendo 1 na
identidade.** -/

end

end TGLExt
