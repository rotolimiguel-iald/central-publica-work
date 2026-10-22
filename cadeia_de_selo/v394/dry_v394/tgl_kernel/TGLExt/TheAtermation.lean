import TGLExt.TheNonMinimalCoupling

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 800000

/-!
# A ATERMAÇÃO — o processo reduzido ao termo, e o ambiente quitado
  [TGLExt — a pedra de 29/08/2026]

## A cunhagem do operador

> *"falta eu cunhar a **atermação** da TGL — transformar a física em TERMO. Não sei como
> se chama quando se termina um código e se queima o restante do ambiente."*

O nome técnico mais próximo é **reificação seguida de teardown**. A cunhagem do operador
junta as duas numa operação só:

```
(processo, ambiente)  ──atermação──▶  (termo, ∅)
```

E ela **já tinha sombra formal no kernel**, sem nome: a compressão pelo canto de posto 1.

## O que se prova `[REAL]`

Sobre `bellProjector` (`TGL/GravitonShadow`, com `bell_idem` e `bell_star` desde antes):

* ★★★★ `atermation_reifies` — **o processo vira termo**: qualquer `y` comprimido devolve
  `Tr(P·y) • P`. O que sai não é `y` reduzido: é **um número sobre o Nome**;
* ★★★★★ `atermation_fixes_the_term` — **o termo é ponto fixo com autovalor 1**:
  `ater(P) = P`. Atermar o que já é termo devolve o termo. Isto é a resposta exata à
  pergunta *"é possível transformar a TGL em matriz de vetor único e autovalor um?"* —
  o objeto já existia; faltava o nome;
* ★★★★★ `atermation_is_irreversible` — **e o ambiente NÃO volta**. Existem `y ≠ z` com
  `ater(y) = ater(z)`. A atermação **não é injetora**, e é por isso que ela é um *termo*
  e não uma mudança de base. **Queimar o ambiente é teorema, não retórica.**

## ⚠ A DISTINÇÃO QUE O OPERADOR JÁ TINHA LEVANTADO, e que o kernel resolve

Ele definiu também `1_abs = I/d` (maximamente misturado), que tem **posto `d`**, não 1.
Isso parecia tensão com `TGL = projetor de posto 1`. **Não é** — e a resolução é anterior:

`the_two_indices_agree_only_at_the_atom` (v256): `1/d = 1/d² ↔ d = 1`.

★ **Os dois só coincidem no átomo.** `I/d` é a identidade **distribuída**; o projetor de
posto 1 é a identidade **atermada**. São as duas pontas da mesma operação:

```
I/d  ──processo──▶  ater  ──▶  P,  com  τ(P) = 1 = ω(I)
```

## ⚠ O QUE ISTO NÃO É

**Não é** a TGL. É a **forma** da atermação — a operação, com o seu ponto fixo e a sua
irreversibilidade. Nenhum teorema aqui menciona β, TGL, física ou 1_abs.

**Não é** ligação a `P_F`, a `firstAtom`, ao `p` de `NameRelation` nem ao canto da rede —
`TheNonMinimalCoupling` já declara essa ausência, e ela permanece. **São projetores de
posto 1 em espaços diferentes, e nada os identifica.**

`[ONTO]` — *"TGL = atermação da física"* é leitura do operador. O que se inscreve é a
operação, e o dente de que ela não volta.

β jamais literal. Sem sorry, sem axiom. Nada aqui acende bandeira nem move o gate.
-/

namespace TGLExt

open Matrix
open TGL.GravitonShadow

noncomputable section

/-! ## A — a operação -/

/-- **A ATERMAÇÃO**: comprimir pelo canto. `ater(y) = P·y·P`.

    Reificação e teardown na mesma conta: o que sobrevive vira coeficiente sobre o
    Nome, e o que era ortogonal não deixa rastro. -/
def atermation (y : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ) :
    Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ :=
  bellProjector * y * bellProjector

/-! ## B — reificação: o processo vira termo -/

/-- [KERNEL] ★★★★ **A ATERMAÇÃO REIFICA**: o que sai é `Tr(P·y)` vezes o Nome.

    Não é `y` reduzido — é **um número sobre `P`**. O termo carrega a medida do
    processo, e não o processo. -/
theorem atermation_reifies (y : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ) :
    atermation y = (Matrix.trace (bellProjector * y)) • bellProjector :=
  bell_compression_is_scalar y

/-! ## C — o termo é ponto fixo, com autovalor 1 -/

/-- [KERNEL] ★★★★★ **O TERMO É PONTO FIXO DA ATERMAÇÃO**: `ater(P) = P`.

    Atermar o que já é termo devolve o termo — **autovalor exatamente 1**. É a resposta
    à pergunta do operador (*"matriz de vetor único e autovalor um?"*): o objeto já
    existia no kernel; o que faltava era o nome da operação que o produz.

    A prova é `bell_idem`, de antes desta pedra. -/
theorem atermation_fixes_the_term : atermation bellProjector = bellProjector := by
  unfold atermation
  rw [bell_idem, bell_idem]

/-! ## D — o dente: o ambiente NÃO volta -/

/-- [KERNEL] ★★★★★ **A ATERMAÇÃO É IRREVERSÍVEL.** Existem `y ≠ z` com
    `ater(y) = ater(z)` — a operação **não é injetora**.

    É este teorema que faz dela uma *atermação* e não uma mudança de base: o ambiente
    que produziu o termo **não é recuperável do termo**. Queimar o contexto é
    consequência da conta, não figura de linguagem.

    Testemunhas: `0` e o projetor complementar `1 − P`. Ambos são aniquilados, e são
    distintos porque `P ≠ 1`: na entrada `(0,0)` o Nome vale `½` e a identidade vale `1`.
    **O Nome não é o todo** — e é essa diferença que dá a irreversibilidade. -/
theorem atermation_is_irreversible :
    ∃ y z : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ,
      y ≠ z ∧ atermation y = atermation z := by
  refine ⟨0, 1 - bellProjector, ?_, ?_⟩
  · intro h
    have h1 : bellProjector = (1 : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ) := by
      have h2 : (1 : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ) - bellProjector = 0 := h.symm
      exact (sub_eq_zero.mp h2).symm
    -- a entrada (0,0): o Nome vale 1/2 ali, a identidade vale 1.
    have hval := congrFun (congrFun h1 (0, 0)) (0, 0)
    simp [bellProjector] at hval
  · unfold atermation
    have hL : bellProjector * 0 * bellProjector = 0 := by
      rw [Matrix.mul_zero, Matrix.zero_mul]
    have hR : bellProjector * (1 - bellProjector) * bellProjector = 0 := by
      rw [Matrix.mul_sub, Matrix.mul_one, bell_idem, sub_self, Matrix.zero_mul]
    rw [hL, hR]

end

end TGLExt
